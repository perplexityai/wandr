"""Shared evaluator utilities: stable identity, JSONL IO, cleanup hooks, and logging."""

import asyncio
import hashlib
import inspect
import logging
import logging.handlers
import os
import sys
import time
import uuid
from collections.abc import Awaitable, Callable, Generator, Iterable
from contextvars import ContextVar
from pathlib import Path
from typing import IO, Any, TextIO, TypeVar

import orjson

from src.runtime.types import RunContext, StopHook, Stoppable

RUN_ID_ENV = "WANDR_RUN_ID"
PUBLIC_STDOUT_FD_ENV = "WANDR_PUBLIC_STDOUT_FD"
PUBLIC_STDERR_FD_ENV = "WANDR_PUBLIC_STDERR_FD"


_RUN_CONTEXT: ContextVar[RunContext | None] = ContextVar(
    "WANDR_RUN_CONTEXT", default=None
)
_STOP_HOOKS: dict[Stoppable, StopHook] = {}
_PUBLIC_STREAMS: dict[tuple[str, str], TextIO] = {}
logger = logging.getLogger(__name__)
TStoppable = TypeVar("TStoppable", bound=Stoppable)
TItem = TypeVar("TItem")


def normalize(value: Any) -> Any:
    """Recursively normalize a value into a stable, comparable structure."""
    match value:
        case str():
            return value
        case bytes():
            return value.hex()
        case dict():
            return [
                (key, normalize(item))
                for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
            ]
        case list():
            return [normalize(item) for item in value]
        case tuple():
            return tuple(normalize(item) for item in value)
        case set() | frozenset():
            return sorted((normalize(item) for item in value), key=str)
        case _:
            return str(value)


def stable_repr(value: Any) -> str:
    """Stable string form for values that participate in identity paths."""
    return str(normalize(value))


def stable_hash(*values: Any) -> str:
    """Hash arbitrary values via normalize/stable_repr. Always sha256, 16 hex chars."""
    hash_input = "\n".join(stable_repr(value) for value in values)
    return hashlib.sha256(hash_input.encode()).hexdigest()[:16]


def init_run() -> None:
    _RUN_CONTEXT.set(
        RunContext(
            id=os.environ.get(RUN_ID_ENV) or uuid.uuid4().hex[:12],
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )
    )


def current_run() -> RunContext:
    return _RUN_CONTEXT.get() or RunContext("", "")


def _json_default(value: Any) -> Any:
    if isinstance(value, (set, frozenset)):
        return sorted(value, key=str)
    raise TypeError(f"{type(value).__name__} is not JSON serializable")


def dumps_json(record: Any) -> bytes:
    return orjson.dumps(record, default=_json_default)


async def call_maybe_async(
    operation: Callable[..., Any], *args: Any, **kwargs: Any
) -> Any:
    return (
        await result
        if inspect.isawaitable(result := operation(*args, **kwargs))
        else result
    )


def drain_queue(queue: asyncio.Queue[TItem | None]) -> list[TItem]:
    drained = []
    while not queue.empty():
        if (item := queue.get_nowait()) is not None:
            drained.append(item)
    return drained


async def _stop_registered(stoppable: Stoppable) -> None:
    if hook := _STOP_HOOKS.pop(stoppable, None):
        await hook()


async def quiet_cleanup(
    logger: logging.Logger, label: str, awaitable: Awaitable[None]
) -> None:
    try:
        await awaitable
    except Exception as exc:
        logger.warning(
            "%s cleanup error: %s: %s", label, type(exc).__name__, exc, exc_info=True
        )


async def stop_quietly(
    stoppable: Stoppable,
    logger: logging.Logger,
    label: str = "stoppable",
) -> None:
    await quiet_cleanup(logger, label, _stop_registered(stoppable))


def with_stop(stoppable: TStoppable, stop: StopHook) -> TStoppable:
    _STOP_HOOKS[stoppable] = stop
    return stoppable


def _public_stream(env_name: str, fallback: TextIO) -> TextIO:
    raw_fd = os.environ.get(env_name)
    if raw_fd is None:
        return fallback
    key = (env_name, raw_fd)
    try:
        if key not in _PUBLIC_STREAMS:
            _PUBLIC_STREAMS[key] = os.fdopen(
                int(raw_fd), "w", buffering=1, closefd=False
            )
        return _PUBLIC_STREAMS[key]
    except (OSError, ValueError):
        return fallback


def public_stdout() -> TextIO:
    return _public_stream(PUBLIC_STDOUT_FD_ENV, sys.__stdout__ or sys.stdout)


def public_print(*args: Any, **kwargs: Any) -> None:
    kwargs.setdefault("file", public_stdout())
    print(*args, **kwargs)


def public_stderr() -> TextIO:
    return _public_stream(PUBLIC_STDERR_FD_ENV, sys.__stderr__ or sys.stderr)


class _BinaryFileHandler(logging.Handler):
    stream: IO[Any]

    def __init__(self, filename: str | Path, mode: str = "ab") -> None:
        super().__init__()
        self.stream = open(filename, mode)  # noqa: SIM115 - handler owns lifecycle via close()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            message = (
                record.msg
                if isinstance(record.msg, bytes)
                else str(record.msg).encode("utf-8")
            )
            self.stream.write(message + b"\n")
        except Exception:
            self.handleError(record)

    def flush(self) -> None:
        if self.stream is not None:
            self.stream.flush()

    def close(self) -> None:
        if self.stream is not None:
            self.stream.close()
        super().close()


def setup_logging_file(
    logger: logging.Logger, path: str | Path, flush_period: int, binary: bool = False
) -> logging.handlers.MemoryHandler:
    if flush_period < 1:
        raise ValueError("setup_logging_file() requires flush_period >= 1")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    logger.propagate = False
    logger.handlers.clear()
    file_handler: logging.Handler = (
        _BinaryFileHandler(path) if binary else logging.FileHandler(path)
    )
    file_handler.setFormatter(logging.Formatter("%(message)s"))
    memory_handler = logging.handlers.MemoryHandler(
        target=file_handler,
        capacity=flush_period,
        flushOnClose=True,
    )
    logger.addHandler(memory_handler)
    return memory_handler


_NOISY_LOGGERS = (
    "aiohttp",
    "asyncio",
    "boto3",
    "botocore",
    "httpcore",
    "httpx",
    "openai",
    "requests",
    "urllib3",
)


_LOG_RECORD_KEYS = frozenset(
    logging.LogRecord("", 0, "", 0, None, None, None).__dict__
) | {"message", "asctime", "exc_info", "exc_text", "stack_info"}


class _ExtraFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        extra = {
            name: value
            for name, value in record.__dict__.items()
            if name not in _LOG_RECORD_KEYS
        }
        return (
            f"{base} {' '.join(f'{name}={value}' for name, value in extra.items())}"
            if extra
            else base
        )


def suppress_noisy_loggers(
    suppress: Iterable[str] | None = None,
    level: int = logging.WARNING,
) -> None:
    for name in suppress or _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(level)


def _is_console_handler(handler: logging.Handler) -> bool:
    return isinstance(handler, logging.StreamHandler) and not isinstance(
        handler, logging.FileHandler
    )


def _remove_console_handlers() -> None:
    for configured_logger in logging.Logger.manager.loggerDict.values():
        if not isinstance(configured_logger, logging.Logger):
            continue
        configured_logger.handlers = [
            handler
            for handler in configured_logger.handlers
            if not _is_console_handler(handler)
        ]
        configured_logger.propagate = True

    root = logging.getLogger()
    root.handlers = [
        handler for handler in root.handlers if not _is_console_handler(handler)
    ]


def setup_eval_logging(log_path: Path) -> None:
    """Route all logging and warnings to a file; leave stdout/stderr for tqdm and intentional prints."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    _remove_console_handlers()

    logging.captureWarnings(True)

    root = logging.getLogger()
    root.handlers.clear()
    file_handler = logging.FileHandler(log_path, mode="w")
    file_handler.setFormatter(
        _ExtraFormatter("%(asctime)s [%(levelname)s] %(name)s %(message)s")
    )
    root.addHandler(file_handler)
    root.setLevel(logging.INFO)

    suppress_noisy_loggers()


def iter_jsonl(
    path: str | Path, *, strict: bool = True
) -> Generator[dict[str, Any], None, None]:
    """Read JSONL from evaluator-sized files."""
    path = Path(path)
    if not path.exists():
        return
    skipped = 0
    with open(path, "rb") as file_handle:
        for line_number, line in enumerate(file_handle, start=1):
            if not (line := line.strip()):
                continue
            try:
                record = orjson.loads(line)
            except ValueError as exc:
                if strict:
                    raise ValueError(f"{path}:{line_number} invalid JSON") from exc
                skipped += 1
                continue
            if not isinstance(record, dict):
                if strict:
                    raise ValueError(f"{path}:{line_number} must be a JSON object")
                skipped += 1
                continue
            yield record
    if skipped:
        logger.warning("Skipped %s malformed JSONL rows in %s", skipped, path)
