import asyncio
import base64
import binascii
import json
import re
from collections.abc import Awaitable, Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from functools import lru_cache
from importlib.resources import files
from pathlib import PurePosixPath
from typing import Any, Literal, Protocol

from jinja2 import Environment, StrictUndefined, Template

type RelaySemanticType = Literal[
    "artifact",
    "lifecycle",
    "narration",
    "reasoning",
    "tool_call",
    "tool_result",
    "usage",
]
type RelayEventName = Literal[
    "workspace.snapshot.started",
    "workspace.snapshot.completed",
    "workspace.materialize.started",
    "workspace.materialize.completed",
    "endpoint.submitted",
    "endpoint.poll",
    "endpoint.message",
    "endpoint.tool_call",
    "endpoint.tool_result",
    "endpoint.usage",
    "endpoint.cancelled",
    "endpoint.cancel_failed",
    "delivery.artifact_found",
    "delivery.files_collected",
]
type DeliveryName = Literal["sandbox", "share", "stdout", "output"]
type RelayObserver = Callable[["RelayEvent"], None]
type EndpointFactory = Callable[..., "Endpoint"]
type PromptSink = Callable[[str], None]
type Sleep = Callable[[float], Awaitable[None]]
type UsageSink = Callable[[dict[str, Any], float | None], None]

OUTPUT_ROOT = PurePosixPath("relay-out")
RELAY_EVENT_NAMES: frozenset[RelayEventName] = frozenset(
    (
        "workspace.snapshot.started",
        "workspace.snapshot.completed",
        "workspace.materialize.started",
        "workspace.materialize.completed",
        "endpoint.submitted",
        "endpoint.poll",
        "endpoint.message",
        "endpoint.tool_call",
        "endpoint.tool_result",
        "endpoint.usage",
        "endpoint.cancelled",
        "endpoint.cancel_failed",
        "delivery.artifact_found",
        "delivery.files_collected",
    )
)
RELAY_SEMANTIC_TYPES: frozenset[RelaySemanticType] = frozenset(
    (
        "artifact",
        "lifecycle",
        "narration",
        "reasoning",
        "tool_call",
        "tool_result",
        "usage",
    )
)
_DEFAULT_EVENT_SEMANTIC_TYPE: dict[RelayEventName, RelaySemanticType] = {
    "workspace.snapshot.started": "lifecycle",
    "workspace.snapshot.completed": "lifecycle",
    "workspace.materialize.started": "lifecycle",
    "workspace.materialize.completed": "lifecycle",
    "endpoint.submitted": "lifecycle",
    "endpoint.poll": "lifecycle",
    "endpoint.message": "narration",
    "endpoint.tool_call": "tool_call",
    "endpoint.tool_result": "tool_result",
    "endpoint.usage": "usage",
    "endpoint.cancelled": "lifecycle",
    "endpoint.cancel_failed": "lifecycle",
    "delivery.artifact_found": "artifact",
    "delivery.files_collected": "artifact",
}
_FENCE_RE = re.compile(r"```\s*([^\n`]*)\n(.*?)```", re.DOTALL)
_FILE_TAG_RE = re.compile(
    r"\[(file(?:-base64)?):([^\]\r\n]+)\](.*?)\[/file\]",
    re.DOTALL,
)
_PROMPT_TEMPLATE = "system.md.jinja"
TOOL_ARGUMENTS = "tool_arguments"
TOOL_RESULT = "tool_result"
LOG_FIELDS = "log_fields"
EVENT_TEXT = "text"
EVENT_TEXT_PREVIEW = "text_preview"
USAGE_INPUT_TOKENS = "input_tokens"
USAGE_TOTAL_INPUT_TOKENS = "total_input_tokens"
USAGE_UNCACHED_INPUT_TOKENS = "uncached_input_tokens"
USAGE_OUTPUT_TOKENS = "output_tokens"
USAGE_TOTAL_TOKENS = "total_tokens"
USAGE_CACHE_READ_INPUT_TOKENS = "cache_read_input_tokens"
USAGE_REASONING_TOKENS = "reasoning_tokens"
USAGE_DETAILS = "details"
DEFAULT_FULL_RESTART_INITIAL_DELAY_SEC = 60.0
DEFAULT_FULL_RESTART_MAX_DELAY_SEC = 480.0
_USAGE_EVENT_NON_USAGE_KEYS = frozenset(
    {
        "cost_usd",
        "endpoint",
        "model",
        "response_id",
        "session_id",
        "status",
        LOG_FIELDS,
    }
)


class RelayError(RuntimeError):
    pass


@dataclass(frozen=True)
class RelayEvent:
    name: RelayEventName
    message: str | None = None
    semantic_type: RelaySemanticType = "lifecycle"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class WorkspaceFile:
    path: PurePosixPath
    content: str
    truncated: bool = False


@dataclass(frozen=True)
class WorkspaceSnapshot:
    root: PurePosixPath
    tree: str
    files: tuple[WorkspaceFile, ...] = ()


@dataclass(frozen=True)
class ProducedFile:
    path: PurePosixPath
    content: bytes
    mode: int | None = None
    source: str | None = None


@dataclass(frozen=True)
class DeliveryMethod:
    name: DeliveryName
    output_root: PurePosixPath | None
    details: str = ""


@dataclass(frozen=True)
class TokenPricing:
    uncached_input: float | None = None
    cached_input: float | None = None
    output_tokens: float | None = None


@dataclass(frozen=True)
class RemoteArtifact:
    name: str
    content: bytes
    source: str


@dataclass(frozen=True)
class RemoteToolOutput:
    command: str
    stdout: str
    source: str


@dataclass(frozen=True)
class EndpointResult:
    text: str
    files: tuple[ProducedFile, ...] = ()
    artifacts: tuple[RemoteArtifact, ...] = ()
    tool_outputs: tuple[RemoteToolOutput, ...] = ()
    raw: dict[str, Any] = field(default_factory=dict)
    usage: dict[str, Any] = field(default_factory=dict)
    cost_usd: float | None = None
    response_id: str | None = None


@dataclass(frozen=True)
class RelayResult:
    prompt: str
    endpoint_result: EndpointResult
    files: tuple[ProducedFile, ...]


@dataclass(frozen=True)
class _AttemptUsage:
    usage: dict[str, Any]
    cost_usd: float | None


class _CumulativeUsage:
    def __init__(self, sink: UsageSink | None):
        self._sink = sink
        self._attempts: dict[int, _AttemptUsage] = {}

    def observe(self, attempt: int, event: RelayEvent) -> None:
        if event.name != "endpoint.usage":
            return
        usage, cost_usd = usage_from_event_metadata(event.metadata)
        self._set(attempt, usage, cost_usd, preserve_existing=False)

    def record_result(self, attempt: int, result: EndpointResult) -> None:
        self._set(
            attempt,
            result.usage,
            result.cost_usd,
            preserve_existing=not result.usage and result.cost_usd is None,
        )

    def apply(self, result: EndpointResult) -> EndpointResult:
        if not self._attempts:
            return result
        usage, cost_usd = self.totals()
        return replace(result, usage=usage, cost_usd=cost_usd)

    def totals(self) -> tuple[dict[str, Any], float | None]:
        attempts = [self._attempts[index] for index in sorted(self._attempts)]
        usage: dict[str, Any] = {}
        for attempt in attempts:
            usage = _merge_usage(usage, attempt.usage)
        cost_usd = (
            sum(attempt.cost_usd for attempt in attempts if attempt.cost_usd is not None)
            if attempts and all(attempt.cost_usd is not None for attempt in attempts)
            else None
        )
        return usage, cost_usd

    def _set(
        self,
        attempt: int,
        usage: Mapping[str, Any],
        cost_usd: float | None,
        *,
        preserve_existing: bool,
    ) -> None:
        if preserve_existing and attempt in self._attempts:
            return
        if not usage and cost_usd is None:
            return
        self._attempts[attempt] = _AttemptUsage(
            usage={str(key): _copy_usage_value(value) for key, value in usage.items()},
            cost_usd=cost_usd,
        )
        if self._sink is not None:
            cumulative_usage, cumulative_cost = self.totals()
            self._sink(cumulative_usage, cumulative_cost)


class _AttemptUsageObserver:
    def __init__(
        self,
        *,
        observer: RelayObserver | None,
        cumulative_usage: _CumulativeUsage,
        attempt: int,
    ):
        self._observer = observer
        self._cumulative_usage = cumulative_usage
        self._attempt = attempt

    def __call__(self, event: RelayEvent) -> None:
        self._cumulative_usage.observe(self._attempt, event)
        if self._observer is not None:
            self._observer(event)


class Endpoint(Protocol):
    @property
    def delivery_method(self) -> DeliveryMethod: ...

    async def run(
        self,
        prompt: str,
        observer: RelayObserver | None = None,
    ) -> EndpointResult: ...


class Workspace(Protocol):
    @property
    def root(self) -> PurePosixPath: ...

    async def snapshot(self) -> WorkspaceSnapshot: ...

    async def materialize(self, files: Sequence[ProducedFile]) -> None: ...


def emit_event(
    observer: RelayObserver | None,
    name: RelayEventName,
    message: str | None = None,
    semantic_type: RelaySemanticType | None = None,
    **metadata: Any,
) -> None:
    if observer is None:
        return
    observer(
        RelayEvent(
            name=name,
            message=message,
            semantic_type=semantic_type or _DEFAULT_EVENT_SEMANTIC_TYPE[name],
            metadata=metadata,
        )
    )


def log_fields(**fields: Any) -> dict[str, Any]:
    visible = {key: value for key, value in fields.items() if value is not None}
    return {LOG_FIELDS: visible} if visible else {}


async def stop_observation_task(
    task: asyncio.Task[Any] | None,
    *,
    observer: RelayObserver | None = None,
    endpoint: str | None = None,
    response_id: str | None = None,
) -> None:
    if task is None:
        return
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        return
    except Exception as exc:
        emit_event(
            observer,
            "endpoint.poll",
            "Endpoint observation task failed during shutdown.",
            endpoint=endpoint,
            response_id=response_id,
            status="observation_task_failed",
            error_type=type(exc).__name__,
            error=str(exc),
            **log_fields(response_id=response_id, status="observation_task_failed"),
        )


def build_prompt(
    instruction: str,
    workspace: WorkspaceSnapshot,
    delivery_method: DeliveryMethod,
    *,
    extra_instruction: str | None = None,
) -> str:
    return _template().render(
        instruction=instruction,
        workspace=workspace,
        delivery=delivery_method,
        extra_instruction=extra_instruction,
    )


def token_cost_usd(
    usage: Mapping[str, Any],
    pricing: TokenPricing | None,
) -> float | None:
    if pricing is None:
        return None

    cached_input_tokens = _usage_count(usage, USAGE_CACHE_READ_INPUT_TOKENS)
    uncached_input_tokens = usage.get(USAGE_UNCACHED_INPUT_TOKENS)
    if uncached_input_tokens is None:
        uncached_input_tokens = max(
            0, _usage_count(usage, USAGE_INPUT_TOKENS) - cached_input_tokens
        )

    line_items = (
        (int(uncached_input_tokens), pricing.uncached_input),
        (cached_input_tokens, pricing.cached_input),
        (_usage_count(usage, USAGE_OUTPUT_TOKENS), pricing.output_tokens),
    )
    if any(tokens > 0 and price is None for tokens, price in line_items):
        return None

    priced_items = [
        tokens * price / 1_000_000
        for tokens, price in line_items
        if tokens > 0 and price is not None
    ]
    return sum(priced_items) if priced_items else None


def usage_from_event_metadata(
    metadata: Mapping[str, Any],
) -> tuple[dict[str, Any], float | None]:
    raw_cost = metadata.get("cost_usd")
    cost_usd = (
        float(raw_cost)
        if isinstance(raw_cost, int | float) and not isinstance(raw_cost, bool)
        else None
    )
    usage = {
        str(key): _copy_usage_value(value)
        for key, value in metadata.items()
        if key not in _USAGE_EVENT_NON_USAGE_KEYS and value is not None
    }
    return usage, cost_usd


def _merge_usage(
    accumulated: Mapping[str, Any],
    new: Mapping[str, Any],
) -> dict[str, Any]:
    merged = {str(key): _copy_usage_value(value) for key, value in accumulated.items()}
    for key, value in new.items():
        key = str(key)
        if key not in merged:
            merged[key] = _copy_usage_value(value)
            continue
        merged[key] = _merge_usage_value(merged[key], value)
    return merged


def _merge_usage_value(accumulated: Any, new: Any) -> Any:
    if (
        isinstance(accumulated, int | float)
        and not isinstance(accumulated, bool)
        and isinstance(new, int | float)
        and not isinstance(new, bool)
    ):
        return accumulated + new
    if isinstance(accumulated, Mapping) and isinstance(new, Mapping):
        return _merge_usage(accumulated, new)
    if accumulated == new:
        return _copy_usage_value(accumulated)
    return _copy_usage_value(new)


def _copy_usage_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _copy_usage_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_copy_usage_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_copy_usage_value(item) for item in value)
    return value


def normalize_output_path(
    raw_path: str,
    *,
    workspace_root: str | PurePosixPath = "/workspace",
) -> PurePosixPath:
    value = raw_path.strip()
    if not value:
        raise RelayError("Produced file path is empty.")

    root = PurePosixPath(str(workspace_root))
    path = PurePosixPath(value)
    if path.is_absolute():
        if path == root:
            raise RelayError(f"Produced file path points at workspace root: {value}")
        try:
            path = path.relative_to(root)
        except ValueError as exc:
            raise RelayError(f"Produced file path is outside workspace root: {value}") from exc

    if path == PurePosixPath("."):
        raise RelayError("Produced file path points at current directory.")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise RelayError(f"Produced file path is not normalized: {value}")

    return path


def output_relative_path(
    raw_path: str,
    *,
    output_root: PurePosixPath = OUTPUT_ROOT,
) -> PurePosixPath | None:
    path = PurePosixPath(raw_path)
    root_parts = output_root.parts
    for index in range(len(path.parts) - len(root_parts) + 1):
        if path.parts[index : index + len(root_parts)] != root_parts:
            continue
        relative_parts = path.parts[index + len(root_parts) :]
        if not relative_parts:
            return None
        return normalize_output_path(PurePosixPath(*relative_parts).as_posix())
    return None


def _usage_count(usage: Mapping[str, Any], key: str) -> int:
    value = usage.get(key)
    if value is None or isinstance(value, bool):
        return 0
    return int(value)


def files_from_stdout_sequence(
    outputs: Iterable[RemoteToolOutput],
    *,
    output_root: PurePosixPath = OUTPUT_ROOT,
) -> tuple[ProducedFile, ...]:
    files = [
        ProducedFile(
            path=path,
            content=output.stdout.encode(),
            source=output.source,
        )
        for output in outputs
        for path in [_cat_output_path(output.command, output_root=output_root)]
        if path is not None
    ]
    return _validate_produced_files(files)


def files_from_final_message(text: str) -> tuple[ProducedFile, ...]:
    files: list[ProducedFile] = list(_files_from_file_tags(text))
    for info, body in _iter_fences(text):
        if info.startswith("file-base64:"):
            path = normalize_output_path(info.removeprefix("file-base64:"))
            try:
                content = base64.b64decode("".join(body.split()), validate=True)
            except binascii.Error as exc:
                raise RelayError(f"Invalid base64 file block for {path}.") from exc
            files.append(
                ProducedFile(
                    path=path,
                    content=content,
                    source="final_message",
                )
            )
        elif info.startswith("file:"):
            files.append(
                ProducedFile(
                    path=normalize_output_path(info.removeprefix("file:")),
                    content=_decode_linewise_json_string_escaped_block(body).encode(),
                    source="final_message",
                )
            )
    return _validate_produced_files(files)


def files_from_output_message(text: str) -> tuple[ProducedFile, ...]:
    return files_from_final_message(text)


class Relay:
    def __init__(
        self,
        *,
        endpoint: Endpoint,
        workspace: Workspace,
        observer: RelayObserver | None = None,
        prompt_sink: PromptSink | None = None,
        extra_instruction: str | None = None,
        require_files: bool = True,
        required_file_paths: Sequence[str | PurePosixPath] | None = None,
        max_full_restarts: int = 0,
        full_restart_initial_delay_sec: float = DEFAULT_FULL_RESTART_INITIAL_DELAY_SEC,
        full_restart_max_delay_sec: float = DEFAULT_FULL_RESTART_MAX_DELAY_SEC,
        usage_sink: UsageSink | None = None,
        sleep: Sleep = asyncio.sleep,
    ):
        if max_full_restarts < 0:
            raise RelayError("max_full_restarts must be >= 0.")
        if full_restart_initial_delay_sec < 0:
            raise RelayError("full_restart_initial_delay_sec must be >= 0.")
        if full_restart_max_delay_sec < full_restart_initial_delay_sec:
            raise RelayError(
                "full_restart_max_delay_sec must be >= full_restart_initial_delay_sec."
            )
        self.endpoint = endpoint
        self.workspace = workspace
        self.observer = observer
        self.prompt_sink = prompt_sink
        self.extra_instruction = extra_instruction
        self.require_files = require_files
        self.required_file_paths = _normalize_required_file_paths(required_file_paths or ())
        self.max_full_restarts = max_full_restarts
        self.full_restart_initial_delay_sec = full_restart_initial_delay_sec
        self.full_restart_max_delay_sec = full_restart_max_delay_sec
        self.usage_sink = usage_sink
        self.sleep = sleep

    async def run(self, instruction: str) -> RelayResult:
        emit_event(
            self.observer,
            "workspace.snapshot.started",
            "Collecting workspace snapshot.",
            root=self.workspace.root.as_posix(),
        )
        workspace = await self.workspace.snapshot()
        emit_event(
            self.observer,
            "workspace.snapshot.completed",
            "Workspace snapshot collected.",
            root=workspace.root.as_posix(),
            file_count=len(workspace.files),
            tree_file_count=len(workspace.tree.splitlines()) if workspace.tree else 0,
            content_bytes=sum(len(file.content.encode()) for file in workspace.files),
        )

        prompt = build_prompt(
            instruction,
            workspace,
            self.endpoint.delivery_method,
            extra_instruction=self.extra_instruction,
        )
        if self.prompt_sink is not None:
            self.prompt_sink(prompt)

        relay_result = await self._run_endpoint_attempt(prompt)

        emit_event(
            self.observer,
            "workspace.materialize.started",
            "Materializing produced files.",
            count=len(relay_result.files),
            **log_fields(count=len(relay_result.files)),
        )
        await self.workspace.materialize(relay_result.files)
        emit_event(
            self.observer,
            "workspace.materialize.completed",
            "Produced files materialized.",
            count=len(relay_result.files),
            paths=[file.path.as_posix() for file in relay_result.files],
            **log_fields(count=len(relay_result.files)),
        )
        return relay_result

    async def _run_endpoint_attempt(self, prompt: str) -> RelayResult:
        delay = self.full_restart_initial_delay_sec
        cumulative_usage = _CumulativeUsage(self.usage_sink)
        for attempt in range(self.max_full_restarts + 1):
            endpoint_result: EndpointResult | None = None
            try:
                endpoint_result = await self.endpoint.run(
                    prompt,
                    observer=_AttemptUsageObserver(
                        observer=self.observer,
                        cumulative_usage=cumulative_usage,
                        attempt=attempt,
                    ),
                )
                cumulative_usage.record_result(attempt, endpoint_result)
                relay_result = _relay_result(
                    prompt,
                    endpoint_result,
                    self.observer,
                    workspace_root=self.workspace.root,
                )
                if self.require_files and not relay_result.files:
                    raise RelayError("Endpoint did not produce any files.")
                missing = _missing_required_file_paths(
                    relay_result.files,
                    self.required_file_paths,
                )
                if missing:
                    raise RelayError(
                        "Endpoint did not produce required files: "
                        + ", ".join(path.as_posix() for path in missing)
                    )
                empty = _empty_required_file_paths(
                    relay_result.files,
                    self.required_file_paths,
                )
                if empty:
                    raise RelayError(
                        "Endpoint produced empty required files: "
                        + ", ".join(path.as_posix() for path in empty)
                    )
                return replace(
                    relay_result,
                    endpoint_result=cumulative_usage.apply(endpoint_result),
                )
            except Exception as exc:
                if attempt == self.max_full_restarts:
                    raise
                emit_event(
                    self.observer,
                    "endpoint.poll",
                    "Restarting Relay endpoint run from scratch.",
                    restart=attempt + 1,
                    max_restarts=self.max_full_restarts,
                    delay_sec=delay,
                    restart_reason=type(exc).__name__,
                    restart_message=str(exc),
                    **_restart_endpoint_metadata(exc, endpoint_result),
                )
                await self.sleep(delay)
                delay = min(delay * 2, self.full_restart_max_delay_sec)
        raise RuntimeError("Relay full-run restart loop exhausted without result.")


@lru_cache
def _template() -> Template:
    source = files("relay.prompts").joinpath(_PROMPT_TEMPLATE).read_text(encoding="utf-8")
    return Environment(
        autoescape=False,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    ).from_string(source)


def _cat_output_path(
    command: str,
    *,
    output_root: PurePosixPath,
) -> PurePosixPath | None:
    parts = command.strip().split()
    if len(parts) != 2 or parts[0] != "cat":
        return None
    return output_relative_path(parts[1], output_root=output_root)


def _iter_fences(text: str) -> Iterable[tuple[str, str]]:
    for match in _FENCE_RE.finditer(text or ""):
        yield match.group(1).strip(), match.group(2)


def _files_from_file_tags(text: str) -> Iterable[ProducedFile]:
    for match in _FILE_TAG_RE.finditer(text or ""):
        kind = match.group(1)
        path = normalize_output_path(match.group(2))
        body = _remove_single_leading_newline(match.group(3))
        if kind == "file-base64":
            try:
                content = base64.b64decode("".join(body.split()), validate=True)
            except binascii.Error as exc:
                raise RelayError(f"Invalid base64 file block for {path}.") from exc
        else:
            content = _decode_linewise_json_string_escaped_block(body).encode()
        yield ProducedFile(path=path, content=content, source="final_message")


def _remove_single_leading_newline(text: str) -> str:
    if text.startswith("\r\n"):
        return text[2:]
    if text.startswith("\n"):
        return text[1:]
    return text


def _decode_linewise_json_string_escaped_block(body: str) -> str:
    if '\\"' not in body:
        return body
    lines = body.splitlines(keepends=True)
    content_lines = [line for line in lines if line.strip()]
    if not content_lines:
        return body
    decoded_lines: list[str] = []
    changed = False
    for line in lines:
        text, line_ending = _split_line_ending(line)
        if not text.strip():
            decoded_lines.append(line)
            continue
        if text != text.strip():
            return body
        if not (text.startswith('{\\"') or text.startswith('[\\"')):
            return body
        try:
            decoded = json.loads(f'"{text}"')
        except json.JSONDecodeError:
            return body
        if not isinstance(decoded, str) or not decoded.startswith(("{", "[")):
            return body
        decoded_lines.append(f"{decoded}{line_ending}")
        changed = changed or decoded != text
    if not changed:
        return body
    return "".join(decoded_lines)


def _split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def _validate_produced_files(
    files: Iterable[ProducedFile],
    *,
    workspace_root: str | PurePosixPath = "/workspace",
    sort_paths: bool = True,
) -> tuple[ProducedFile, ...]:
    by_path: dict[PurePosixPath, ProducedFile] = {}
    for file in files:
        path = normalize_output_path(
            file.path.as_posix(),
            workspace_root=workspace_root,
        )
        if path in by_path:
            raise RelayError(f"Duplicate produced file path after normalization: {path.as_posix()}")
        by_path[path] = file if file.path == path else replace(file, path=path)
    paths = sorted(by_path) if sort_paths else by_path
    return tuple(by_path[path] for path in paths)


def _normalize_required_file_paths(
    paths: Iterable[str | PurePosixPath],
) -> tuple[PurePosixPath, ...]:
    normalized = {
        normalize_output_path(path.as_posix() if isinstance(path, PurePosixPath) else path)
        for path in paths
    }
    return tuple(sorted(normalized))


def _missing_required_file_paths(
    files: Sequence[ProducedFile],
    required_paths: Sequence[PurePosixPath],
) -> tuple[PurePosixPath, ...]:
    if not required_paths:
        return ()
    produced = {normalize_output_path(file.path.as_posix()) for file in files}
    return tuple(path for path in required_paths if path not in produced)


def _empty_required_file_paths(
    files: Sequence[ProducedFile],
    required_paths: Sequence[PurePosixPath],
) -> tuple[PurePosixPath, ...]:
    if not required_paths:
        return ()
    produced = {normalize_output_path(file.path.as_posix()): file.content for file in files}
    return tuple(path for path in required_paths if path in produced and len(produced[path]) == 0)


def _restart_endpoint_metadata(
    exc: BaseException,
    endpoint_result: EndpointResult | None,
) -> dict[str, Any]:
    provider = None
    response_id = None
    run = getattr(exc, "_relay_endpoint_run", None)
    if run is not None:
        provider = getattr(run, "provider", None)
        response_id = getattr(run, "id", None)
    if response_id is None and endpoint_result is not None:
        response_id = endpoint_result.response_id
    metadata = {
        "had_provider_id": response_id is not None,
        "provider": provider,
        "response_id": response_id,
        "status": "full_restart",
    }
    metadata.update(log_fields(status="full_restart", response_id=response_id))
    return metadata


def _relay_result(
    prompt: str,
    endpoint_result: EndpointResult,
    observer: RelayObserver | None,
    *,
    workspace_root: str | PurePosixPath,
) -> RelayResult:
    files = _validate_produced_files(
        endpoint_result.files,
        workspace_root=workspace_root,
        sort_paths=False,
    )
    emit_event(
        observer,
        "delivery.files_collected",
        "Collected produced files.",
        count=len(files),
        paths=[file.path.as_posix() for file in files],
        bytes=sum(len(file.content) for file in files),
        **log_fields(
            count=len(files),
            bytes=sum(len(file.content) for file in files),
        ),
    )
    return RelayResult(
        prompt=prompt,
        endpoint_result=endpoint_result,
        files=files,
    )
