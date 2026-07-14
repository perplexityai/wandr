import atexit
import asyncio
import os
import signal
import threading
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from types import FrameType
from typing import Any

from relay.core import RelayObserver, emit_event, log_fields

CANCEL_TIMEOUT_SEC = 10.0


@dataclass(frozen=True)
class EndpointRun:
    provider: str
    id: str


@dataclass(frozen=True)
class _ActiveRun:
    run: EndpointRun
    cancel: Callable[[], Awaitable[None]]
    observer: RelayObserver | None


_ACTIVE: dict[EndpointRun, _ActiveRun] = {}
_PREVIOUS_SIGNAL_HANDLERS: dict[signal.Signals, Any] = {}
_ENDPOINT_RUN_ERROR_ATTR = "_relay_endpoint_run"


def register_endpoint_run(
    *,
    provider: str,
    run_id: str,
    cancel: Callable[[], Awaitable[None]],
    observer: RelayObserver | None = None,
) -> EndpointRun:
    run = EndpointRun(provider=provider, id=run_id)
    _ACTIVE[run] = _ActiveRun(run=run, cancel=cancel, observer=observer)
    return run


def close_endpoint_run(run: EndpointRun | None) -> None:
    if run is not None:
        _ACTIVE.pop(run, None)


def attach_endpoint_run_error(exc: BaseException, run: EndpointRun | None) -> None:
    if run is not None:
        setattr(exc, _ENDPOINT_RUN_ERROR_ATTR, run)


async def cancel_endpoint_run(run: EndpointRun | None, *, reason: str) -> None:
    if run is None:
        return
    active = _ACTIVE.pop(run, None)
    if active is None:
        return
    await _cancel(active, reason=reason)


async def cancel_active_endpoint_runs(*, reason: str = "atexit") -> None:
    active_runs = tuple(_ACTIVE.values())
    _ACTIVE.clear()
    await asyncio.gather(*(_cancel(active, reason=reason) for active in active_runs))


async def _cancel(active: _ActiveRun, *, reason: str) -> None:
    try:
        await asyncio.wait_for(asyncio.shield(active.cancel()), CANCEL_TIMEOUT_SEC)
    except Exception as exc:
        emit_event(
            active.observer,
            "endpoint.cancel_failed",
            "Failed to cancel remote endpoint run.",
            endpoint=active.run.provider,
            response_id=active.run.id,
            reason=reason,
            error_type=type(exc).__name__,
            **log_fields(response_id=active.run.id),
        )
        return
    emit_event(
        active.observer,
        "endpoint.cancelled",
        "Cancelled remote endpoint run.",
        endpoint=active.run.provider,
        response_id=active.run.id,
        reason=reason,
        **log_fields(response_id=active.run.id),
    )


def _cancel_at_exit() -> None:
    _cancel_active_endpoint_runs_sync(reason="atexit")


def _cancel_active_endpoint_runs_sync(*, reason: str) -> None:
    if not _ACTIVE:
        return
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(cancel_active_endpoint_runs(reason=reason))
        return

    error: BaseException | None = None

    def target() -> None:
        nonlocal error
        try:
            asyncio.run(cancel_active_endpoint_runs(reason=reason))
        except BaseException as exc:
            error = exc

    thread = threading.Thread(target=target, daemon=False)
    thread.start()
    thread.join(CANCEL_TIMEOUT_SEC + 1.0)
    if error is not None:
        raise error


def _handle_signal(signum: int, frame: FrameType | None) -> None:
    signal_name = signal.Signals(signum)
    _cancel_active_endpoint_runs_sync(reason=f"signal:{signal_name.name}")
    previous = _PREVIOUS_SIGNAL_HANDLERS.get(signal_name)
    if callable(previous):
        previous(signum, frame)
        return
    if previous == signal.SIG_DFL:
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)
        return
    if signal_name == signal.SIGINT:
        raise KeyboardInterrupt
    raise SystemExit(128 + signum)


def _install_signal_handlers() -> None:
    if threading.current_thread() is not threading.main_thread():
        return
    for signal_name in (signal.SIGINT, signal.SIGTERM):
        previous = signal.getsignal(signal_name)
        if previous == _handle_signal:
            continue
        _PREVIOUS_SIGNAL_HANDLERS[signal_name] = previous
        signal.signal(signal_name, _handle_signal)


atexit.register(_cancel_at_exit)
_install_signal_handlers()
