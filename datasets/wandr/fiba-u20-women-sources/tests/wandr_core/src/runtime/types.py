"""Shared type definitions for the pipeline."""

from collections.abc import Awaitable, Callable
from typing import Any, NamedTuple

type Record = dict[str, Any]
type Stoppable = Callable[..., Awaitable[Any]]
type Component = Callable[[Any, Record], Awaitable[Record | None]]
type BatchComponent = Callable[
    [Any, list[Record]], Awaitable[list[Record | None] | None]
]
type StopHook = Callable[[], Awaitable[None]]


class RunContext(NamedTuple):
    id: str
    timestamp: str
