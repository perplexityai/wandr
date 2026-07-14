from pathlib import PurePosixPath
from typing import Any

from relay.core import (
    ProducedFile,
    RelayObserver,
    RemoteArtifact,
    RemoteToolOutput,
    emit_event,
    log_fields,
    output_relative_path,
)
from relay.providers.openai.events import openai_field, openai_list


async def collect_openai_container_output_files(
    client: Any,
    response: Any,
    *,
    output_root: PurePosixPath,
    observer: RelayObserver | None = None,
) -> tuple[list[ProducedFile], list[RemoteArtifact]]:
    files: list[ProducedFile] = []
    artifacts: list[RemoteArtifact] = []
    seen_file_ids: set[str] = set()
    for item in openai_list(openai_field(response, "output")):
        if openai_field(item, "type") != "code_interpreter_call":
            continue
        container_id = openai_field(item, "container_id")
        if not container_id:
            continue

        page = await client.containers.files.list(container_id=container_id)
        for file in openai_list(openai_field(page, "data")):
            file_id = openai_field(file, "id")
            output_path = output_relative_path(
                str(openai_field(file, "path", "")),
                output_root=output_root,
            )
            if not file_id or file_id in seen_file_ids or output_path is None:
                continue

            payload = await client.containers.files.content.retrieve(
                file_id,
                container_id=container_id,
            )
            content = payload.read()
            emit_event(
                observer,
                "delivery.artifact_found",
                "Downloaded OpenAI container artifact.",
                endpoint="openai",
                response_id=openai_field(response, "id"),
                container_id=container_id,
                file_id=file_id,
                artifact_name=output_path.as_posix(),
                bytes=len(content),
                **log_fields(
                    response_id=openai_field(response, "id"),
                    container_id=container_id,
                    file_id=file_id,
                    bytes=len(content),
                ),
            )

            source = f"openai_container:{container_id}:{file_id}"
            files.append(ProducedFile(path=output_path, content=content, source=source))
            artifacts.append(
                RemoteArtifact(
                    name=output_path.as_posix(),
                    content=content,
                    source=source,
                )
            )
            seen_file_ids.add(file_id)
    return files, artifacts


def collect_openai_shell_outputs(response: Any) -> list[RemoteToolOutput]:
    calls_by_id = {
        call_id: item
        for item in openai_list(openai_field(response, "output"))
        if openai_field(item, "type") == "shell_call"
        if (call_id := openai_field(item, "call_id") or openai_field(item, "id"))
    }

    outputs: list[RemoteToolOutput] = []
    for item in openai_list(openai_field(response, "output")):
        if openai_field(item, "type") != "shell_call_output":
            continue

        stdout = "\n".join(
            chunk
            for part in openai_list(openai_field(item, "output"))
            if isinstance(chunk := openai_field(part, "stdout"), str) and chunk
        )
        if not stdout.strip():
            continue

        call_id = openai_field(item, "call_id") or openai_field(item, "id")
        call = calls_by_id.get(call_id)
        command = "\n".join(
            str(command)
            for command in openai_list(
                openai_field(openai_field(call, "action"), "commands")
            )
        )
        outputs.append(
            RemoteToolOutput(
                command=command or "shell",
                stdout=stdout,
                source=f"openai_shell:{call_id}",
            )
        )
    return outputs
