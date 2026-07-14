"""Flow nodes: pure stream combinators with no compute or clients.

These are async coroutines that run beside compute nodes in the pipeline
task group. They move records between queues — routing, merging,
splitting, reshaping, transforming.

Single-input flow nodes accept n_inputs for sentinel counting: the number
of upstream writers. A sentinel (None) from each writer is expected; the
flow node propagates its own sentinel only after all input sentinels have
been received. fan_in encodes the same rule as a list of input queues.

Pipeline records are accretion-only by default: nodes add fields via dict
merge rather than mutating or narrowing records in place. `explode` and
`spread` accept `drop_sources` for the few fan-out points where carrying
the original collection field would duplicate large source data downstream.
"""

import asyncio
from collections.abc import AsyncIterator, Callable, Hashable
from typing import Any

from src.runtime.types import Record
from src.runtime.utils import (
    call_maybe_async,
    stable_hash,
    stable_repr,
)

type ExpectedSize = int | Callable[[Record], int] | None
type FlushIncomplete = bool | Callable[[list[Record]], bool]
type Fingerprint = Callable[[list[Record]], str] | None


def _list_value(value: Any, *, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be a list")
    return value


def _record_list(value: Any, *, label: str) -> list[Record]:
    records = _list_value(value, label=label)
    if any(not isinstance(record, dict) for record in records):
        raise TypeError(f"{label} must contain record objects")
    return records


def _validate_n_inputs(n_inputs: int) -> None:
    if n_inputs < 1:
        raise ValueError("flow nodes require n_inputs >= 1")


async def _records_until_done(
    input_queue: asyncio.Queue[Record | None],
    n_inputs: int = 1,
) -> AsyncIterator[Record]:
    _validate_n_inputs(n_inputs)
    sentinels = 0
    while sentinels < n_inputs:
        record = await input_queue.get()
        try:
            if record is None:
                sentinels += 1
                continue
            yield record
        finally:
            input_queue.task_done()


async def tee(
    input_queue: asyncio.Queue[Record | None],
    *output_queues: asyncio.Queue[Record | None],
    n_inputs: int = 1,
) -> None:
    """Duplicate each record to all output queues."""
    if not output_queues:
        raise ValueError("tee() requires at least one output queue")
    async for record in _records_until_done(input_queue, n_inputs):
        for output_queue in output_queues:
            await output_queue.put(record)
    for output_queue in output_queues:
        await output_queue.put(None)


async def fan_out(
    input_queue: asyncio.Queue[Record | None],
    route: Callable[[Record], Hashable],
    queues: dict[Hashable, asyncio.Queue[Record | None]],
    *,
    n_inputs: int = 1,
) -> None:
    """Route records by predicate to named queues.

    route: callable(record) -> queue_key
    queues: dict[key, asyncio.Queue]

    Sends None to ALL output queues when all input sentinels received.
    """
    if not queues:
        raise ValueError("fan_out() requires at least one output queue")
    async for record in _records_until_done(input_queue, n_inputs):
        route_key = route(record)
        output_queue = queues.get(route_key)
        if output_queue is None:
            expected = ", ".join(repr(key) for key in queues)
            raise ValueError(
                f"fan_out() unknown route key {route_key!r}; expected one of: {expected}"
            )
        await output_queue.put(record)
    for output_queue in queues.values():
        await output_queue.put(None)


async def fan_in(
    input_queues: list[asyncio.Queue[Record | None]],
    output_queue: asyncio.Queue[Record | None],
) -> None:
    """Merge multiple queues into one.

    Each drainer reads until sentinel. Sentinel is sent to output_queue only
    after ALL drainers have finished (all input queues exhausted).
    """
    if not input_queues:
        raise ValueError("fan_in() requires at least one input queue")

    async def drain(input_queue: asyncio.Queue[Record | None]) -> None:
        async for record in _records_until_done(input_queue):
            await output_queue.put(record)

    await asyncio.gather(*(drain(input_queue) for input_queue in input_queues))
    await output_queue.put(None)


async def explode(  # noqa: PLR0913 - declarative stream-graph DSL surface.
    input_queue: asyncio.Queue[Record | None],
    output_queue: asyncio.Queue[Record | None],
    *,
    items: str | Callable[[Record], list[Any]],
    label: str | None = None,
    drop_sources: list[str] | None = None,
    n_inputs: int = 1,
) -> None:
    """Unpack a collection field into individual records.

    items: field name containing a list, or callable(record) -> list.
    label: if set, each output record gets record[label] = element.
           If None, element must be a dict and is merged via record | element.
    drop_sources: field names to remove from the parent record before merging.
           Use to avoid carrying large source collections on every child.
    """

    def items_for_record(record: Record) -> list[Any]:
        raw_items = items(record) if callable(items) else record.get(items, [])
        return _list_value(raw_items, label="explode(items)")

    async for record in _records_until_done(input_queue, n_inputs):
        base_record = (
            {
                field_name: field_value
                for field_name, field_value in record.items()
                if field_name not in (drop_sources or ())
            }
            if drop_sources
            else record
        )
        for element in items_for_record(record):
            if label is not None:
                await output_queue.put(base_record | {label: element})
                continue
            if not isinstance(element, dict):
                raise TypeError("explode(label=None) requires dict elements")
            await output_queue.put(base_record | element)
    await output_queue.put(None)


async def spread(  # noqa: PLR0913 - declarative stream-graph DSL surface.
    input_queue: asyncio.Queue[Record | None],
    output_queue: asyncio.Queue[Record | None],
    *,
    into: str,
    value: str,
    over: str | list[str] | Callable[[Record], list[tuple[str, Any]]],
    drop_sources: list[str] | None = None,
    n_inputs: int = 1,
) -> None:
    """Pivot N named fields into N records with a label + value column.

    into: field name for the label (e.g. "_key_name").
    value: field name for the value (e.g. "_key_value_raw").
    over: fields to pivot. Either:
        - a list of field names: each becomes a record with into=name, value=record[name]
        - a callable(record) -> [(label, value), ...]: explicit label/value pairs
        - a string field name: shorthand for [field_name]
    drop_sources: field names to remove from the parent record before merging.
           Pivoted field names (from list form of `over`) are always dropped.
    """
    if isinstance(over, str):
        fields: list[str] = [over]

        def pairs_for_record(record: Record) -> list[tuple[str, Any]]:
            return [(over, record.get(over))]

    elif isinstance(over, list):
        fields = over

        def pairs_for_record(record: Record) -> list[tuple[str, Any]]:
            return [(field, record.get(field)) for field in fields]

    else:
        fields = []
        pairs_for_record = over

    drop = set(fields) | set(drop_sources or ())

    async for record in _records_until_done(input_queue, n_inputs):
        base_record = (
            {
                field_name: field_value
                for field_name, field_value in record.items()
                if field_name not in drop
            }
            if drop
            else record
        )
        for label_value, raw_value in pairs_for_record(record):
            await output_queue.put(base_record | {into: label_value, value: raw_value})
    await output_queue.put(None)


async def flatten(
    input_queue: asyncio.Queue[Record | None],
    output_queue: asyncio.Queue[Record | None],
    *,
    n_inputs: int = 1,
) -> None:
    """Expand buffered group records into their member records."""
    async for record in _records_until_done(input_queue, n_inputs):
        for member in _record_list(record.get("_members"), label="flatten(_members)"):
            await output_queue.put(member)
    await output_queue.put(None)


async def transform(
    input_queue: asyncio.Queue[Record | None],
    output_queue: asyncio.Queue[Record | None],
    transform_record: Callable[[Record], Record | None],
    *,
    n_inputs: int = 1,
) -> None:
    """Transform each record via transform_record(record) -> record | None.

    None return = drop (record not forwarded).
    """
    async for record in _records_until_done(input_queue, n_inputs):
        result = transform_record(record)
        if result is not None:
            await output_queue.put(result)
    await output_queue.put(None)


async def observe(
    input_queue: asyncio.Queue[Record | None],
    output_queue: asyncio.Queue[Record | None],
    observe_record: Callable[[Record | None], Any],
    *,
    n_inputs: int = 1,
) -> None:
    """Pass-through observer. Calls observe_record(record) for side effects on each record.

    observe_record receives None on sentinel (end of stream). Records pass
    through unmodified. observe_record can be sync or async.
    """
    async for record in _records_until_done(input_queue, n_inputs):
        await call_maybe_async(observe_record, record)
        await output_queue.put(record)
    await call_maybe_async(observe_record, None)
    await output_queue.put(None)


# ── Buffer ───────────────────────────────────────────────────


def _default_fingerprint(group: list[Record]) -> str:
    """Hash all member contents. Safe but over-specified."""
    return stable_hash(*sorted(group, key=stable_repr))


def _validate_buffer_args(
    *,
    expected_size: ExpectedSize,
    timeout: float | None,
    ttl: float | None,
    ttl_retries: int,
    n_inputs: int,
) -> None:
    if isinstance(expected_size, int) and expected_size < 1:
        raise ValueError("buffer() requires expected_size >= 1")
    if timeout is not None and timeout < 0:
        raise ValueError("buffer() requires timeout >= 0")
    if ttl is not None and ttl < 0:
        raise ValueError("buffer() requires ttl >= 0")
    if ttl_retries < 0:
        raise ValueError("buffer() requires ttl_retries >= 0")
    _validate_n_inputs(n_inputs)


async def buffer(  # noqa: PLR0913 - declarative stream-graph DSL surface.
    input_queue: asyncio.Queue[Record | None],
    output_queue: asyncio.Queue[Record | None],
    *,
    key: Callable[[Record], Hashable],
    expected_size: ExpectedSize = None,
    timeout: float | None = None,
    ttl: float | None = None,
    flush_incomplete: FlushIncomplete = True,
    ttl_retries: int = 0,
    allow_late_arrivals: bool = False,
    n_inputs: int = 1,
    fingerprint: Fingerprint = _default_fingerprint,
    fingerprint_field: str = "_fp",
) -> None:
    """Accumulate records by key and emit group records.

    Parameters
    ----------
    key : callable(record) -> hashable
        Routing function: which group does this record belong to.
    expected_size : int | callable(record) -> int | None
        Flush when group hits this size. Callable receives the first
        record in the group. None = flush only on sentinel/timeout/ttl.
    timeout : float | None
        Seconds after group creation before forced flush/drop (absolute).
    ttl : float | None
        Idle timeout — seconds since last arrival in this group. Resets
        on each new record. Fires when the group goes quiet.
    flush_incomplete : bool | callable(group) -> bool
        What to do when timeout/ttl fires or sentinel arrives with
        incomplete groups.
        - True: always emit incomplete groups
        - False: always discard incomplete groups
        - callable: receives the group's member list, returns True to
          emit or False to drop. Use for conditional flush (e.g. emit
          only if the fetch-lane record is present).
    ttl_retries : int
        When TTL fires and flush_incomplete returns False, retry the TTL
        this many times before dropping. 0 = drop immediately. Use a
        large value (e.g. 10_000) for "keep waiting indefinitely."
        Sentinel always overrides retries and forces flush/drop.
    allow_late_arrivals : bool
        When True, keys are never added to the closed set, so records
        arriving after a group has been emitted or dropped start a new
        group instead of being silently skipped. Useful when fractured
        delivery is acceptable (e.g. dedup batches or late convergence
        groups).
    n_inputs : int
        Number of upstream sentinels to expect.
    fingerprint : callable(group) -> str | None
        Custom fingerprint function. None = no fingerprint on output.
    """
    _validate_buffer_args(
        expected_size=expected_size,
        timeout=timeout,
        ttl=ttl,
        ttl_retries=ttl_retries,
        n_inputs=n_inputs,
    )
    pending: dict[Hashable, list[Record]] = {}
    timeout_tasks: dict[Hashable, asyncio.Task[None]] = {}
    ttl_tasks: dict[Hashable, asyncio.Task[None]] = {}
    expected_counts: dict[Hashable, int | None] = {}
    retries_remaining: dict[Hashable, int] = {}
    closed_groups: set[Hashable] = set()

    def cancel_timers(group_key: Hashable) -> None:
        for timers in (timeout_tasks, ttl_tasks):
            timer = timers.pop(group_key, None)
            if timer is not None and not timer.done():
                timer.cancel()

    def remove_group(group_key: Hashable) -> list[Record] | None:
        members = pending.pop(group_key, None)
        expected_counts.pop(group_key, None)
        retries_remaining.pop(group_key, None)
        cancel_timers(group_key)
        return members

    def resolve_expected(record: Record) -> int | None:
        if expected_size is None:
            return None
        resolved = expected_size(record) if callable(expected_size) else expected_size
        if resolved < 1:
            raise ValueError("buffer() requires expected_size >= 1")
        return resolved

    def should_emit(members: list[Record]) -> bool:
        return (
            flush_incomplete(members)
            if callable(flush_incomplete)
            else bool(flush_incomplete)
        )

    def close_group(group_key: Hashable) -> None:
        if not allow_late_arrivals:
            closed_groups.add(group_key)

    async def handle_incomplete_group(
        group_key: Hashable, *, force: bool = False
    ) -> None:
        if group_key in closed_groups:
            return
        members = pending.get(group_key)
        if members is None:
            return
        if should_emit(members):
            await emit_group(group_key)
            return
        if not force and retries_remaining[group_key] > 0:
            retries_remaining[group_key] -= 1
            reset_ttl(group_key)
            return
        discard_group(group_key)

    async def on_timer(
        group_key: Hashable,
        delay: float,
        timers: dict[Hashable, asyncio.Task[None]],
        *,
        force: bool = False,
    ) -> None:
        try:
            await asyncio.sleep(delay)
        except asyncio.CancelledError:
            return
        if timers.get(group_key) is asyncio.current_task():
            timers.pop(group_key, None)
        await handle_incomplete_group(group_key, force=force)

    def reset_ttl(group_key: Hashable) -> None:
        if ttl is None:
            return
        if (timer := ttl_tasks.get(group_key)) is not None and not timer.done():
            timer.cancel()
        ttl_tasks[group_key] = asyncio.create_task(on_timer(group_key, ttl, ttl_tasks))

    def start_group(group_key: Hashable, record: Record) -> None:
        pending[group_key] = []
        expected_counts[group_key] = resolve_expected(record)
        retries_remaining[group_key] = ttl_retries
        if timeout is not None:
            timeout_tasks[group_key] = asyncio.create_task(
                on_timer(group_key, timeout, timeout_tasks, force=True),
            )

    def is_complete(group_key: Hashable) -> bool:
        expected_count = expected_counts[group_key]
        return expected_count is not None and len(pending[group_key]) >= expected_count

    def add_record(record: Record) -> Hashable | None:
        group_key = key(record)
        if group_key in closed_groups:
            return None
        if group_key not in pending:
            start_group(group_key, record)
        pending[group_key].append(record)
        reset_ttl(group_key)
        return group_key

    async def emit_group(group_key: Hashable) -> None:
        if group_key in closed_groups:
            return
        close_group(group_key)
        if (members := remove_group(group_key)) is None:
            return
        group_record: Record = {"_group_key": group_key, "_members": members}
        if fingerprint is not None:
            group_record[fingerprint_field] = fingerprint(members)
        await output_queue.put(group_record)

    def discard_group(group_key: Hashable) -> None:
        if group_key in closed_groups:
            return
        close_group(group_key)
        remove_group(group_key)

    async def accept_record(record: Record) -> None:
        group_key = add_record(record)
        if group_key is None:
            return
        if is_complete(group_key):
            await emit_group(group_key)

    async def drain_input() -> None:
        async for record in _records_until_done(input_queue, n_inputs):
            await accept_record(record)

    async def flush_remaining() -> None:
        for group_key in list(pending):
            await handle_incomplete_group(group_key, force=True)

    try:
        await drain_input()
        await flush_remaining()
    finally:
        for group_key in list(pending):
            cancel_timers(group_key)
        await output_queue.put(None)
