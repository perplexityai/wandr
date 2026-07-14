import asyncio
from collections.abc import Awaitable, Callable
from pathlib import PurePosixPath
from typing import Any

from relay.core import (
    ProducedFile,
    RelayObserver,
    RemoteArtifact,
    emit_event,
    log_fields,
    normalize_output_path,
    output_relative_path,
)
from relay.providers.anthropic.events import (
    dump_anthropic_model,
    is_retryable_anthropic_stream_error,
)


type Sleep = Callable[[float], Awaitable[None]]

ANTHROPIC_FILE_RETRY_ATTEMPTS = 7
ANTHROPIC_FILE_RETRY_INITIAL_DELAY_SEC = 1.0
ANTHROPIC_FILE_RETRY_MAX_DELAY_SEC = 30.0
ANTHROPIC_FILES_API_BETA = "files-api-2025-04-14"


async def collect_anthropic_output_files(
    client: Any,
    *,
    output_root: PurePosixPath,
    session_id: str,
    beta: str,
    observer: RelayObserver | None = None,
    sleep: Sleep = asyncio.sleep,
    retry_attempts: int = ANTHROPIC_FILE_RETRY_ATTEMPTS,
    retry_initial_delay_sec: float = ANTHROPIC_FILE_RETRY_INITIAL_DELAY_SEC,
    retry_max_delay_sec: float = ANTHROPIC_FILE_RETRY_MAX_DELAY_SEC,
) -> tuple[list[ProducedFile], list[RemoteArtifact]]:
    file_metadata = await _wait_for_stable_output_files(
        client,
        output_root=output_root,
        session_id=session_id,
        beta=beta,
        observer=observer,
        sleep=sleep,
        retry_attempts=retry_attempts,
        retry_initial_delay_sec=retry_initial_delay_sec,
        retry_max_delay_sec=retry_max_delay_sec,
    )
    files = await _download_anthropic_files(
        client,
        file_metadata=file_metadata,
        output_root=output_root,
        beta=beta,
        session_id=session_id,
        observer=observer,
        sleep=sleep,
        retry_attempts=retry_attempts,
        retry_initial_delay_sec=retry_initial_delay_sec,
        retry_max_delay_sec=retry_max_delay_sec,
    )
    artifacts = [
        RemoteArtifact(
            name=file.path.as_posix(),
            content=file.content,
            source=file.source or "",
        )
        for file in files
    ]
    for file in files:
        file_id = file.source.removeprefix("anthropic_file:") if file.source else None
        emit_event(
            observer,
            "delivery.artifact_found",
            "Downloaded Anthropic output file.",
            endpoint="anthropic-managed",
            session_id=session_id,
            file_id=file_id,
            artifact_name=file.path.as_posix(),
            bytes=len(file.content),
            source=file.source,
            **log_fields(
                session_id=session_id,
                file_id=file_id,
                artifact_name=file.path.as_posix(),
                bytes=len(file.content),
            ),
        )
    return files, artifacts


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


async def _wait_for_stable_output_files(
    client: Any,
    *,
    output_root: PurePosixPath,
    session_id: str,
    beta: str,
    observer: RelayObserver | None,
    sleep: Sleep,
    retry_attempts: int,
    retry_initial_delay_sec: float,
    retry_max_delay_sec: float,
) -> list[dict[str, Any]]:
    delay = retry_initial_delay_sec
    previous_file_ids: tuple[str, ...] | None = None
    for attempt in range(retry_attempts):
        try:
            files = await _list_anthropic_output_files(
                client,
                output_root=output_root,
                session_id=session_id,
                beta=beta,
            )
        except Exception as exc:
            if (
                attempt + 1 == retry_attempts
                or not is_retryable_anthropic_stream_error(exc)
            ):
                raise
            emit_event(
                observer,
                "endpoint.poll",
                "Retrying Anthropic output file listing.",
                endpoint="anthropic-managed",
                session_id=session_id,
                attempt=attempt + 1,
                error_type=type(exc).__name__,
                **log_fields(session_id=session_id),
            )
            await sleep(delay)
            delay = min(delay * 2, retry_max_delay_sec)
            continue
        file_ids = tuple(sorted(str(file["id"]) for file in files))
        emit_event(
            observer,
            "endpoint.poll",
            "Polled Anthropic output files.",
            endpoint="anthropic-managed",
            session_id=session_id,
            attempt=attempt + 1,
            count=len(files),
            **log_fields(session_id=session_id, count=len(files)),
        )
        if files and file_ids == previous_file_ids:
            return files

        previous_file_ids = file_ids if files else None
        if attempt + 1 < retry_attempts:
            await sleep(delay)
            delay = min(delay * 2, retry_max_delay_sec)
    return files


async def _list_anthropic_output_files(
    client: Any,
    *,
    output_root: PurePosixPath,
    session_id: str,
    beta: str,
) -> list[dict[str, Any]]:
    files = []
    async for file in client.beta.files.list(
        scope_id=session_id,
        limit=1000,
        betas=_file_betas(beta),
    ):
        metadata = dump_anthropic_model(file)
        if metadata.get("downloadable", True):
            files.append(metadata)
    return sorted(
        files,
        key=lambda file: _output_path(file["filename"], output_root=output_root),
    )


async def _download_anthropic_file(
    client: Any,
    *,
    file_metadata: dict[str, Any],
    output_root: PurePosixPath,
    beta: str,
) -> ProducedFile:
    file_id = str(file_metadata["id"])
    payload = await client.beta.files.download(file_id, betas=_file_betas(beta))
    return ProducedFile(
        path=_output_path(file_metadata["filename"], output_root=output_root),
        content=await payload.read(),
        source=f"anthropic_file:{file_id}",
    )


async def _download_anthropic_files(
    client: Any,
    *,
    file_metadata: list[dict[str, Any]],
    output_root: PurePosixPath,
    beta: str,
    session_id: str,
    observer: RelayObserver | None,
    sleep: Sleep,
    retry_attempts: int,
    retry_initial_delay_sec: float,
    retry_max_delay_sec: float,
) -> list[ProducedFile]:
    delay = retry_initial_delay_sec
    for attempt in range(retry_attempts):
        try:
            return [
                await _download_anthropic_file(
                    client,
                    file_metadata=metadata,
                    output_root=output_root,
                    beta=beta,
                )
                for metadata in file_metadata
            ]
        except Exception as exc:
            if attempt + 1 == retry_attempts:
                raise
            emit_event(
                observer,
                "endpoint.poll",
                "Retrying Anthropic output file download.",
                endpoint="anthropic-managed",
                session_id=session_id,
                attempt=attempt + 1,
                error_type=type(exc).__name__,
                **log_fields(session_id=session_id),
            )
            await sleep(delay)
            delay = min(delay * 2, retry_max_delay_sec)
    return []


def _output_path(
    filename: str,
    *,
    output_root: PurePosixPath | None,
) -> PurePosixPath:
    if output_root is not None and (
        path := output_relative_path(filename, output_root=output_root)
    ):
        return path
    return normalize_output_path(filename)


def _file_betas(managed_agents_beta: str) -> list[str]:
    return [ANTHROPIC_FILES_API_BETA, managed_agents_beta]
