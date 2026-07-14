from collections.abc import Sequence

from relay.core import (
    ProducedFile,
    RelayError,
    RelayObserver,
    emit_event,
    log_fields,
)


def output_delivery_details(*, tool_phrase: str) -> str:
    return (
        f"{tool_phrase} during the run, but tool workspaces, sandbox state, "
        "and tool-output blocks are not externally reachable as submitted files "
        "after the run. To submit files, include each final file in your final "
        "response as a `file:<relative-path>` fenced block."
    )


def raise_if_terminal_without_delivery(
    terminal_error: RelayError | None,
    files: Sequence[ProducedFile],
) -> None:
    if terminal_error is not None and not files:
        raise terminal_error


def emit_terminal_delivery_available(
    *,
    observer: RelayObserver | None,
    endpoint: str,
    response_id: str,
    original_status: object,
    terminal_error: RelayError | None,
    files: Sequence[ProducedFile],
) -> None:
    if terminal_error is None or not files:
        return
    emit_event(
        observer,
        "endpoint.poll",
        f"{endpoint} terminal run was not completed, but delivery files are available.",
        endpoint=endpoint,
        response_id=response_id,
        status="terminal_delivery_available",
        original_status=original_status,
        paths=[file.path.as_posix() for file in files],
        bytes=sum(len(file.content) for file in files),
        **log_fields(response_id=response_id, status="terminal_delivery_available"),
    )
