"""Execution wrappers for components.

All components have signature (client, record) -> output | None.
Modifiers preserve this contract.

persisted() persists component outputs to JSONL. On hit, returns stored
output without calling the component. Supports multiple outputs per
key (for exact-duplicate input records).

batched() wraps a batch component (client, [records]) -> [output | None]
into the standard single-record contract.

projected() deduplicates I/O without dropping records: first caller
for a key executes the component, subsequent callers for the same key
get the cached result. Every record flows through. Composes with
batched() and persisted().
"""

import asyncio
import logging
import logging.handlers
import random
from collections.abc import Awaitable, Callable, Hashable, Iterator
from functools import partial, wraps
from pathlib import Path
from typing import Any, ParamSpec, TypeVar, overload

from src.runtime.types import (
    BatchComponent,
    Component,
    Record,
    Stoppable,
)
from src.runtime.utils import (
    call_maybe_async,
    current_run,
    dumps_json,
    iter_jsonl,
    setup_logging_file,
    stop_quietly,
    with_stop,
)


FLUSH_PERIOD = 25
logger = logging.getLogger(__name__)
P = ParamSpec("P")
R = TypeVar("R")
TStoppable = TypeVar("TStoppable", bound=Stoppable)
type _BatchCall = tuple[Record, asyncio.Future[Record | None], Any]
type _BatchQueue = asyncio.Queue[_BatchCall | None]


def _with_stops(wrapped: TStoppable, *stoppables: Stoppable) -> TStoppable:
    async def stop() -> None:
        for stoppable in stoppables:
            await stop_quietly(stoppable, logger)

    return with_stop(wrapped, stop)


def _serialize_key(cache_key: Hashable) -> str:
    if isinstance(cache_key, str):
        return cache_key
    return dumps_json(cache_key).decode()


def persisted(
    component: Component | None = None,
    *,
    key: str | Callable[[Record], Hashable],
    path: str | Path,
    flush_period: int = FLUSH_PERIOD,
    provenance: Callable[[Record], dict[str, Any]] | None = None,
) -> Component:
    """Persist component outputs to JSONL. On hit, return stored output.

    Supports multiple outputs per key: if the input stream has N records
    with the same key, the cache stores N outputs. On replay, each
    record gets the next cached output for its key (iterator-style).
    Extra records beyond the cached count fall through to recompute.
    """
    if component is None:
        return partial(
            persisted,
            key=key,
            path=path,
            flush_period=flush_period,
            provenance=provenance,
        )

    cache_path = Path(path)
    extract: Callable[[Record], Hashable | None] = (
        key if callable(key) else lambda record: record.get(key)
    )
    cache: dict[str, list[Record]] = {}
    iterators: dict[str, Iterator[Record]] = {}
    loaded = False
    cache_logger: logging.Logger | None = None
    handler: logging.handlers.MemoryHandler | None = None

    def ensure_loaded() -> None:
        nonlocal loaded, cache_logger, handler
        if loaded:
            return
        loaded = True
        if cache_path.exists():
            for record in iter_jsonl(cache_path, strict=False):
                record.pop("_prov", None)
                record.pop("_run_id", None)
                record.pop("_run_ts", None)
                if (cache_key := record.pop("_ck", None)) is None:
                    continue
                serialized_key = (
                    cache_key
                    if isinstance(cache_key, str)
                    else _serialize_key(
                        tuple(cache_key) if isinstance(cache_key, list) else cache_key
                    )
                )
                cache.setdefault(serialized_key, []).append(record)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_logger = logging.Logger(f"cached.{cache_path.stem}.{id(cache_path)}")
        handler = setup_logging_file(
            cache_logger, cache_path, flush_period, binary=True
        )

    def cached(cache_key: Hashable) -> tuple[bool, Record | None]:
        serialized_key = _serialize_key(cache_key)
        if (
            serialized_key not in iterators
            and (records := cache.get(serialized_key)) is not None
        ):
            iterators[serialized_key] = iter(records)
        if (iterator := iterators.get(serialized_key)) is None:
            return False, None
        try:
            return True, dict(next(iterator))
        except StopIteration:
            iterators.pop(serialized_key, None)
            return False, None

    def write(cache_key: Hashable, record: Record, result: Record | None) -> None:
        if result is None or cache_logger is None:
            return
        run = current_run()
        write_record = {
            **result,
            "_ck": cache_key,
            "_run_id": run.id,
            "_run_ts": run.timestamp,
        }
        if provenance is not None:
            write_record["_prov"] = provenance(record)
        cache_logger.info(dumps_json(write_record))

    def close() -> None:
        nonlocal cache_logger, handler
        memory_handler = handler
        active_logger = cache_logger
        handler = None
        cache_logger = None
        if memory_handler is not None:
            target = memory_handler.target
            memory_handler.close()
            if target is not None:
                target.close()
        if active_logger is not None:
            active_logger.handlers.clear()

    @wraps(component)
    async def wrapped(client: Any, record: Record) -> Record | None:
        ensure_loaded()
        cache_key = extract(record)
        if cache_key is None:
            return await component(client, record)

        hit, cached_result = cached(cache_key)
        if hit:
            return cached_result

        result = await component(client, record)
        write(cache_key, record, result)
        return result

    async def stop() -> None:
        try:
            await stop_quietly(component, logger, label="component")
        finally:
            close()

    return with_stop(wrapped, stop)


def dispatched(
    components: dict[Hashable, Component],
    *,
    by: str | Callable[[Record], Hashable] = "_task",
    default: Record | None = None,
) -> Component:
    """Route to per-key components.

    by: string field name or callable(record) -> key. Default: "_task".
    components: {key_value: component} — one component per dispatch key.
    default: returned when the key has no registered component (None = fail).
    """
    dispatch_key: Callable[[Record], Hashable] = (
        by if callable(by) else lambda record: record.get(by, "")
    )

    async def wrapped(client: Any, record: Record) -> Record | None:
        if (component := components.get(dispatch_key(record))) is None:
            return default
        return await component(client, record)

    return _with_stops(wrapped, *components.values())


@overload
def timebox(
    operation: None = None,
    *,
    t: float | None = None,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]: ...


@overload
def timebox(
    operation: Callable[P, Awaitable[R]],
    *,
    t: float | None = None,
) -> Callable[P, Awaitable[R]]: ...


def timebox(
    operation: Callable[P, Awaitable[R]] | None = None, *, t: float | None = None
) -> Any:
    """Wrap any async callable with asyncio.wait_for(t). Signature-agnostic."""
    timeout = t
    if operation is None:
        return partial(timebox, t=t)
    if timeout is None:
        raise TypeError("timebox() requires t=")

    @wraps(operation)
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        return await asyncio.wait_for(operation(*args, **kwargs), timeout)

    return _with_stops(wrapped, operation)


@overload
def aexcepts(
    operation: None = None,
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    default: Any = None,
    handler: Callable[..., Any] | None = None,
) -> Callable[[Stoppable], Stoppable]: ...


@overload
def aexcepts(
    operation: Stoppable,
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    default: Any = None,
    handler: Callable[..., Any] | None = None,
) -> Stoppable: ...


def aexcepts(
    operation: Stoppable | None = None,
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    default: Any = None,
    handler: Callable[..., Any] | None = None,
) -> Stoppable | Callable[[Stoppable], Stoppable]:
    """Catch exceptions, call handler, return default. Signature-agnostic.

    Wraps any async callable. On caught exception:
    - `handler` is invoked as `handler(exc, *args, **kwargs)`: same args as the
      wrapped call, plus the exception. Async-aware (awaits if coroutine).
    - Returns `default(*args, **kwargs)` if `default` is callable, else `default`.
      Callable defaults are async-aware.

    Domain-specific naming (e.g., `record`, `url`) lives at the call site via
    closures: `handler=lambda exc, _client, record: logger.exception(...)`.
    """
    if operation is None:
        return partial(
            aexcepts, exceptions=exceptions, default=default, handler=handler
        )

    @wraps(operation)
    async def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return await operation(*args, **kwargs)
        except exceptions as exc:
            if handler is not None:
                await call_maybe_async(handler, exc, *args, **kwargs)
            return (
                await call_maybe_async(default, *args, **kwargs)
                if callable(default)
                else default
            )

    return _with_stops(wrapped, operation)


@overload
def on_error(
    operation: None = None,
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    handler: Callable[..., Any],
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]: ...


@overload
def on_error(
    operation: Callable[P, Awaitable[R]],
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    handler: Callable[..., Any],
) -> Callable[P, Awaitable[R]]: ...


def on_error(
    operation: Callable[P, Awaitable[R]] | None = None,
    *,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
    handler: Callable[..., Any],
) -> Any:
    """Run an async-aware handler on matching exceptions, then re-raise."""
    if operation is None:
        return partial(on_error, exceptions=exceptions, handler=handler)

    @wraps(operation)
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await operation(*args, **kwargs)
        except exceptions as exc:
            await call_maybe_async(handler, exc, *args, **kwargs)
            raise

    return _with_stops(wrapped, operation)


@overload
def retrying(
    operation: None = None,
    *,
    attempts: int,
    delay: float = 0.0,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]: ...


@overload
def retrying(
    operation: Callable[P, Awaitable[R]],
    *,
    attempts: int,
    delay: float = 0.0,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
) -> Callable[P, Awaitable[R]]: ...


def retrying(
    operation: Callable[P, Awaitable[R]] | None = None,
    *,
    attempts: int,
    delay: float = 0.0,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
) -> Any:
    """Retry an async callable, then re-raise the final exception."""
    if operation is None:
        return partial(retrying, attempts=attempts, delay=delay, exceptions=exceptions)
    if attempts < 1:
        raise TypeError("retrying() requires attempts >= 1")

    @wraps(operation)
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        for attempt in range(attempts):
            try:
                return await operation(*args, **kwargs)
            except exceptions:
                if attempt == attempts - 1:
                    raise
                if delay:
                    await asyncio.sleep(delay)
        raise RuntimeError("retrying attempts exhausted without result")

    return _with_stops(wrapped, operation)


def retrying_bisect(
    operation: BatchComponent | None = None,
    *,
    n_retries: int = 3,
    min_size: int = 1,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = Exception,
) -> BatchComponent:
    """Recursively bisect a batched call on exception.

    Wraps: async (client, records: list) -> list[result | None]
    On exception in `exceptions`, splits the record list in half and recurses
    on each half. Surrenders a record slice as `[None] * len(record_slice)`
    when either the retry budget is exhausted (`n_retries`) or the slice
    shrinks to `min_size`.

    Composes inside `batched`: a batch component decorated with this at
    definition time plugs straight into `batched(component, size=...)` in pipeline
    wiring, exactly like `@aexcepts` / `@timebox` do.
    """
    if operation is None:
        return partial(
            retrying_bisect,
            n_retries=n_retries,
            min_size=min_size,
            exceptions=exceptions,
        )
    if n_retries < 0:
        raise ValueError("retrying_bisect() requires n_retries >= 0")
    if min_size < 1:
        raise ValueError("retrying_bisect() requires min_size >= 1")

    @wraps(operation)
    async def wrapped(client: Any, records: list[Record]) -> list[Record | None]:
        async def attempt_slice(
            record_slice: list[Record], depth: int
        ) -> list[Record | None]:
            try:
                return await operation(client, record_slice) or [None] * len(
                    record_slice
                )
            except exceptions as exc:
                if depth >= n_retries or len(record_slice) <= min_size:
                    logger.warning(
                        "retrying_bisect.surrender operation=%s size=%s depth=%s error=%s",
                        getattr(operation, "__name__", type(operation).__name__),
                        len(record_slice),
                        depth,
                        type(exc).__name__,
                    )
                    return [None] * len(record_slice)
                split_at = len(record_slice) // 2
                left, right = await asyncio.gather(
                    attempt_slice(record_slice[:split_at], depth + 1),
                    attempt_slice(record_slice[split_at:], depth + 1),
                )
                return left + right

        return await attempt_slice(records, 0)

    return _with_stops(wrapped, operation)


def dropping(component: Component, *, fields: list[str]) -> Component:
    """Strip fields from component output before it's merged onto the record."""

    async def wrapped(client: Any, record: Record) -> Record | None:
        result = await component(client, record)
        if result is None:
            return None
        return {field: value for field, value in result.items() if field not in fields}

    return _with_stops(wrapped, component)


def batched(
    component: BatchComponent | None = None, *, size: int = 50, interval: float = 2.0
) -> Component:
    """Accumulate individual calls into batch dispatches.

    Wraps: async (client, records: list[dict]) -> list[dict | None]
    Into:  async (client, record) -> output | None
    A batch-level None result fans out as one None per input record.
    """
    if component is None:
        return partial(batched, size=size, interval=interval)
    if size < 1:
        raise ValueError("batched() requires size >= 1")
    if interval < 0:
        raise ValueError("batched() requires interval >= 0")

    call_queue: _BatchQueue | None = None
    dispatcher: asyncio.Task[None] | None = None
    in_flight: set[asyncio.Task[None]] = set()

    def outputs(
        batch_result: list[Record | None] | None, count: int
    ) -> list[Record | None]:
        if batch_result is None:
            return [None] * count
        if not isinstance(batch_result, list):
            raise TypeError(
                f"batched component returned {type(batch_result).__name__}; expected list or None"
            )
        if len(batch_result) > count:
            raise ValueError(
                f"batched component returned {len(batch_result)} outputs for {count} inputs"
            )
        return batch_result + [None] * (count - len(batch_result))

    def ensure_queue() -> _BatchQueue:
        nonlocal call_queue, dispatcher
        if call_queue is None:
            call_queue = asyncio.Queue()
            dispatcher = asyncio.create_task(dispatch_batches(call_queue))
        return call_queue

    async def flush(batch: list[_BatchCall]) -> None:
        records = [record for record, _, _ in batch]
        futures = [future for _, future, _ in batch]
        # Clients in a pool are interchangeable. Random selection spreads batch
        # calls across them without adding stateful load tracking here.
        _, _, client = random.choice(batch)

        try:
            batch_result = await component(client, records)
            results = outputs(batch_result, len(futures))
        except Exception as exc:
            for future in futures:
                if not future.done():
                    future.set_exception(exc)
            return

        for future, result in zip(futures, results, strict=True):
            if not future.done():
                future.set_result(result)

    async def dispatch_batches(queue: _BatchQueue) -> None:
        while True:
            if (first_call := await queue.get()) is None:
                return

            batch: list[_BatchCall] = [first_call]
            deadline = asyncio.get_running_loop().time() + interval

            while len(batch) < size:
                remaining = deadline - asyncio.get_running_loop().time()
                if remaining <= 0:
                    break
                try:
                    if (
                        next_call := await asyncio.wait_for(
                            queue.get(), timeout=remaining
                        )
                    ) is None:
                        await flush(batch)
                        return
                    batch.append(next_call)
                except asyncio.TimeoutError:
                    break

            task = asyncio.create_task(flush(batch))
            in_flight.add(task)
            task.add_done_callback(in_flight.discard)

    async def submit(client: Any, record: Record) -> Record | None:
        future: asyncio.Future[Record | None] = (
            asyncio.get_running_loop().create_future()
        )
        await ensure_queue().put((record, future, client))
        return await future

    async def stop_dispatcher() -> None:
        if call_queue is not None:
            await call_queue.put(None)
        if dispatcher is not None:
            await dispatcher
        if in_flight:
            await asyncio.gather(*in_flight, return_exceptions=True)

    @wraps(component)
    async def wrapped(client: Any, record: Record) -> Record | None:
        return await submit(client, record)

    async def stop() -> None:
        try:
            await stop_dispatcher()
        finally:
            await stop_quietly(component, logger, label="component")

    return with_stop(wrapped, stop)


def projected(
    component: Component | None = None, *, key: str | Callable[[Record], Hashable]
) -> Component:
    """Project cached component output onto records with duplicate keys.

    First record with a given key value: calls the component, caches result.
    Subsequent records with the same key: returns cached result without calling.

    Every record flows through — no dropping. The component's I/O happens
    once per unique key value. Each output record keeps its own context
    because run_node merges the returned dict into the originating record.

    Concurrent callers for the same in-flight key block until the first
    caller completes (singleflight pattern).

    Concurrency safety: relies on asyncio's cooperative scheduling. All dict
    operations (_results, _errors, _pending) happen in synchronous code between
    await points — no two coroutines execute simultaneously, so check-then-set
    sequences are atomic. No locks needed.

    Composes with batched()::

        projected(batched(fetch_page, size=50), key="url")
    """
    if component is None:
        return partial(projected, key=key)

    extract: Callable[[Record], Hashable | None] = (
        key if callable(key) else lambda record: record.get(key)
    )
    results: dict[Hashable, Record] = {}
    errors: dict[Hashable, Exception] = {}
    pending: dict[Hashable, asyncio.Event] = {}

    def cached(cache_key: Hashable) -> tuple[bool, Record | None]:
        if cache_key in results:
            result = results[cache_key]
            return True, dict(result) if result is not None else None
        if (exc := errors.get(cache_key)) is not None:
            raise exc
        return False, None

    async def first(client: Any, record: Record, cache_key: Hashable) -> Record | None:
        event = asyncio.Event()
        pending[cache_key] = event
        try:
            result = await component(client, record)
            if result is not None:
                results[cache_key] = dict(result)
            return result
        except Exception as exc:
            errors[cache_key] = exc
            raise
        finally:
            event.set()
            pending.pop(cache_key, None)

    @wraps(component)
    async def wrapped(client: Any, record: Record) -> Record | None:
        cache_key = extract(record)
        if cache_key is None:
            return await component(client, record)
        hit, cached_result = cached(cache_key)
        if hit:
            return cached_result
        if event := pending.get(cache_key):
            await event.wait()
            hit, cached_result = cached(cache_key)
            if hit:
                return cached_result
        return await first(client, record, cache_key)

    async def stop() -> None:
        await stop_quietly(component, logger, label="component")

    return with_stop(wrapped, stop)
