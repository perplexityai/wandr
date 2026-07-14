"""Async tqdm progress bars with incremental total discovery."""

import asyncio
from typing import NotRequired, Required, TypedDict

from tqdm import tqdm

from src.runtime.utils import public_stderr

BOUNDED_BAR = "{desc} {bar:20} {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
UNBOUNDED_BAR = "{desc} {n_fmt} [{elapsed}]"


class _BarState(TypedDict):
    name: str
    total: int | None
    finalized: bool
    success_count: int
    failure_count: int
    tqdm_bar: tqdm | None


class _ProgressUpdate(TypedDict, total=False):
    bar_id: Required[int]
    successes: NotRequired[int]
    failures: NotRequired[int]
    expected: NotRequired[int]
    finalize: NotRequired[bool]


def _bar_state(name: str, total: int | None = None) -> _BarState:
    return {
        "name": name,
        "total": total,
        "finalized": False,
        "success_count": 0,
        "failure_count": 0,
        "tqdm_bar": None,
    }


def _bar_format(total: int | None, suffix: str = "") -> str:
    return (BOUNDED_BAR if total is not None else UNBOUNDED_BAR) + suffix


def _validate_count(name: str, count: int) -> None:
    if count < 0:
        raise ValueError(f"{name} must be >= 0")


def _count_suffix(state: _BarState) -> str:
    if not state["success_count"] and not state["failure_count"]:
        return ""
    return (
        f" {state['success_count']}\u2713{state['failure_count']}\u2717"
        if state["failure_count"]
        else f" {state['success_count']}\u2713"
    )


def _state_format(state: _BarState) -> str:
    return _bar_format(state["total"], _count_suffix(state))


class ProgressBar:
    def __init__(
        self, updates: asyncio.Queue[_ProgressUpdate | None], bar_id: int
    ) -> None:
        self._updates = updates
        self._bar_id = bar_id

    async def ok(self) -> None:
        await self._updates.put({"bar_id": self._bar_id, "successes": 1})

    async def fail(self) -> None:
        await self._updates.put({"bar_id": self._bar_id, "failures": 1})

    async def add_expected(self, count: int) -> None:
        _validate_count("expected", count)
        await self._updates.put({"bar_id": self._bar_id, "expected": count})

    async def finalize_total(self) -> None:
        await self._updates.put({"bar_id": self._bar_id, "finalize": True})


class ProgressTracker:
    def __init__(self) -> None:
        self._updates: asyncio.Queue[_ProgressUpdate | None] = asyncio.Queue()
        self._bars: dict[int, _BarState] = {}
        self._next_id = 0

    def register(self, name: str, total: int | None = None) -> ProgressBar:
        if total is not None:
            _validate_count("total", total)
        bar_id = self._next_id
        self._next_id += 1
        self._bars[bar_id] = _bar_state(name, total)
        return ProgressBar(self._updates, bar_id)

    def _ensure_bar(self, state: _BarState) -> tqdm:
        bar = state["tqdm_bar"]
        if bar is None:
            bar = tqdm(
                total=state["total"],
                desc=f"  {state['name']:>10}",
                unit="rec",
                leave=True,
                ncols=80,
                file=public_stderr(),
                # mininterval=0: tqdm's default 0.1s suppresses rapid updates,
                # making bars jump from 0 to N for fast cached stages and
                # small totals. Fine at eval scale (<10k records).
                # At millions of records, reintroduce a small mininterval.
                mininterval=0,
                bar_format=_bar_format(state["total"]),
            )
            state["tqdm_bar"] = bar
        return bar

    def _apply_update(self, update: _ProgressUpdate) -> None:
        state = self._bars[update["bar_id"]]

        had_total = state["total"] is not None
        if "expected" in update:
            state["total"] = (state["total"] or 0) + update["expected"]
        if update.get("finalize"):
            state["finalized"] = True
            state["total"] = state["total"] or 0

        bar = self._ensure_bar(state)

        if "successes" in update:
            state["success_count"] += update["successes"]
        if "failures" in update:
            state["failure_count"] += update["failures"]
        if "successes" in update or "failures" in update:
            bar.bar_format = _state_format(state)
            bar.update(update.get("successes", 0) + update.get("failures", 0))

        if "expected" in update:
            if not state["finalized"]:
                bar.total = state["total"]
                if not had_total:
                    bar.bar_format = _bar_format(state["total"])
                bar.refresh()

        if update.get("finalize"):
            bar.total = state["total"]
            bar.bar_format = _state_format(state)
            bar.refresh()

    async def run(self) -> None:
        try:
            while (update := await self._updates.get()) is not None:
                self._apply_update(update)
        finally:
            for state in self._bars.values():
                if (bar := state["tqdm_bar"]) is not None:
                    bar.close()

    def stop(self) -> None:
        self._updates.put_nowait(None)
