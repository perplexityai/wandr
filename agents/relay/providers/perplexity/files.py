import base64
import binascii
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from relay.core import (
    ProducedFile,
    RelayError,
    RelayObserver,
    RemoteArtifact,
    emit_event,
    log_fields,
    normalize_output_path,
)

type ResponseGetter = Callable[[str], Awaitable[Any]]

PERPLEXITY_SHARE_NAME_PREFIX = "relaypath--"


@dataclass(frozen=True)
class SharedFileDeclaration:
    path: PurePosixPath
    file_id: str


def declared_perplexity_shared_files(
    response: Mapping[str, Any],
    events: list[dict[str, Any]],
) -> tuple[SharedFileDeclaration, ...]:
    declarations = [
        declaration
        for item in _share_file_items(response, events)
        for declaration in [_shared_file_declaration(item)]
        if declaration is not None
    ]
    return tuple({item.path: item for item in declarations}.values())


async def collect_perplexity_shared_files(
    *,
    get: ResponseGetter,
    base_url: str,
    endpoint_path: str,
    response_id: str,
    declarations: tuple[SharedFileDeclaration, ...],
    observer: RelayObserver | None = None,
) -> tuple[list[ProducedFile], list[RemoteArtifact]]:
    files_url = f"{base_url}{endpoint_path}/{response_id}/files"

    files: list[ProducedFile] = []
    artifacts: list[RemoteArtifact] = []
    for declaration in declarations:
        payload = await get(f"{files_url}/{declaration.file_id}/content")
        content = payload.content
        source = f"perplexity_files:{declaration.file_id}"
        files.append(ProducedFile(path=declaration.path, content=content, source=source))
        artifacts.append(
            RemoteArtifact(
                name=declaration.path.as_posix(),
                content=content,
                source=source,
            )
        )
        emit_event(
            observer,
            "delivery.artifact_found",
            "Downloaded Perplexity shared file.",
            endpoint="perplexity",
            response_id=response_id,
            file_id=declaration.file_id,
            artifact_name=declaration.path.as_posix(),
            bytes=len(content),
            source=source,
            **log_fields(
                response_id=response_id,
                file_id=declaration.file_id,
                bytes=len(content),
            ),
        )
    return files, artifacts


def perplexity_share_name(path: PurePosixPath) -> str:
    relative_path = normalize_output_path(path.as_posix()).as_posix()
    encoded = base64.urlsafe_b64encode(relative_path.encode()).decode().rstrip("=")
    return f"{PERPLEXITY_SHARE_NAME_PREFIX}{encoded}"


def _shared_file_path(entry: Mapping[str, Any]) -> PurePosixPath | None:
    filename = str(entry.get("filename") or entry.get("name") or "")
    if not filename.startswith(PERPLEXITY_SHARE_NAME_PREFIX):
        return None

    encoded = filename.removeprefix(PERPLEXITY_SHARE_NAME_PREFIX)
    padding = "=" * (-len(encoded) % 4)
    try:
        decoded = base64.urlsafe_b64decode(encoded + padding).decode()
        return normalize_output_path(decoded)
    except (binascii.Error, RelayError, UnicodeDecodeError):
        return None


def _shared_file_declaration(
    item: Mapping[str, Any],
) -> SharedFileDeclaration | None:
    file_id = str(item.get("file_id") or item.get("id") or "")
    path = _shared_file_path(item)
    if not file_id or path is None:
        return None
    return SharedFileDeclaration(path=path, file_id=file_id)


def _share_file_items(
    response: Mapping[str, Any],
    events: list[dict[str, Any]],
) -> list[Mapping[str, Any]]:
    return [
        item
        for item in [
            *[
                _dict(item)
                for item in _list(response.get("output"))
                if _dict(item).get("type") == "share_file"
            ],
            *[
                _dict(_dict(event).get("item"))
                for event in events
                if _dict(event).get("type") == "response.output_item.done"
                and _dict(_dict(event).get("item")).get("type") == "share_file"
            ],
        ]
        if item
    ]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
