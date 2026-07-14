import asyncio
import json
import shlex
import tempfile
import tomllib
from collections.abc import Awaitable, Callable, Iterable, Mapping, Sequence
from datetime import UTC, datetime
from fnmatch import fnmatch
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path, PurePosixPath
from typing import Any, override

from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext
from harbor.models.trajectories import (
    Agent as TrajectoryAgent,
    FinalMetrics,
    Metrics,
    Observation,
    ObservationResult,
    Step,
    ToolCall,
    Trajectory,
)
from harbor.utils.trajectory_utils import format_trajectory_json

from relay.core import (
    DEFAULT_FULL_RESTART_INITIAL_DELAY_SEC,
    DEFAULT_FULL_RESTART_MAX_DELAY_SEC,
    EndpointResult,
    Endpoint,
    EVENT_TEXT,
    EVENT_TEXT_PREVIEW,
    LOG_FIELDS,
    RelayError,
    Relay,
    ProducedFile,
    RelayEvent,
    RelayResult,
    TOOL_ARGUMENTS,
    TOOL_RESULT,
    USAGE_CACHE_READ_INPUT_TOKENS,
    USAGE_INPUT_TOKENS,
    USAGE_OUTPUT_TOKENS,
    USAGE_TOTAL_INPUT_TOKENS,
    WorkspaceFile,
    WorkspaceSnapshot,
    normalize_output_path,
    usage_from_event_metadata,
)
from relay.providers import endpoint_factory

_DEFAULT_ENV_EXCLUDES = (
    ".env*",
    "**/.env*",
)
_DEFAULT_CREDENTIAL_EXCLUDES = (
    "**/*.pem",
    "**/*.key",
    "**/*.crt",
    "**/*.cer",
    "**/*.p12",
    "**/*.pfx",
    "**/*.jks",
    "**/*.keystore",
    "**/.aws/**",
    "**/.azure/**",
    "**/.config/gcloud/**",
    "**/.docker/config.json",
    "**/.kube/**",
    "**/.ssh/**",
    "**/.git-credentials",
    "**/.netrc",
    "**/.npmrc",
    "**/.pypirc",
    "**/application_default_credentials.json",
)
_DEFAULT_EXCLUDES = (
    ".git/**",
    ".hg/**",
    ".svn/**",
    ".cache/**",
    ".pytest_cache/**",
    "__pycache__/**",
    *_DEFAULT_ENV_EXCLUDES,
    *_DEFAULT_CREDENTIAL_EXCLUDES,
)
_WORKSPACE_COMMAND_TIMEOUT_SEC = 60
_WORKSPACE_RETRY_ATTEMPTS = 5
_WORKSPACE_RETRY_INITIAL_DELAY_SEC = 1.0
_WORKSPACE_RETRY_MAX_DELAY_SEC = 20.0
_PRODUCED_FILE_ARTIFACT_ROOT = PurePosixPath("/logs/artifacts/relay-output")


class _HarborRelayObserver:
    def __init__(
        self,
        *,
        logs_dir: Path,
        logger: Any,
        context: AgentContext,
        endpoint_name: str,
        agent_name: str,
        agent_version: str,
        model_name: str | None,
    ):
        self._logs_dir = logs_dir
        self._logger = logger
        self._context = context
        self._endpoint_name = endpoint_name
        self._agent_name = agent_name
        self._agent_version = agent_version
        self._model_name = model_name
        self._events_path = logs_dir / "events.jsonl"
        self._status_path = logs_dir / "status.json"
        self._status: dict[str, Any] = {
            "endpoint": endpoint_name,
            "events_seen": 0,
        }
        self._prompt: str | None = None
        self.events: list[dict[str, Any]] = []
        self._logs_dir.mkdir(parents=True, exist_ok=True)

    def write_prompt(self, prompt: str) -> None:
        self._prompt = prompt
        _write_text_atomic(self._logs_dir / "prompt.md", prompt)
        self.write_trajectory()

    def __call__(self, event: RelayEvent) -> None:
        metadata = _jsonable(event.metadata)
        timestamp = datetime.now(UTC).isoformat()
        row = {
            "time": timestamp,
            "name": event.name,
            "semantic_type": event.semantic_type,
            "message": event.message,
            "metadata": metadata,
        }
        self.events.append(row)

        with self._events_path.open("a", encoding="utf-8") as event_file:
            event_file.write(json.dumps(row, sort_keys=True) + "\n")

        self._status["events_seen"] = int(self._status["events_seen"]) + 1
        self._status["updated_at"] = timestamp
        self._status["phase"] = event.name
        self._status["latest_event"] = row
        for key in ("response_id", "session_id", "status", "model"):
            if metadata.get(key) is not None:
                self._status[key] = metadata[key]
        _write_text_atomic(
            self._status_path,
            json.dumps(self._status, indent=2, sort_keys=True),
        )

        context_metadata = dict(self._context.metadata or {})
        context_metadata.update(
            {
                "endpoint": self._endpoint_name,
                "phase": event.name,
                "latest_event": {
                    "name": event.name,
                    "semantic_type": event.semantic_type,
                    "message": event.message,
                    "time": timestamp,
                },
            }
        )
        for key in ("response_id", "session_id"):
            if metadata.get(key) is not None:
                context_metadata[key] = metadata[key]
        self._context.metadata = context_metadata

        suffix = _event_log_suffix(metadata)
        self._logger.info(
            "Relay %s%s",
            event.name,
            f" {suffix}" if suffix else "",
        )
        self.write_trajectory()

    def write_trajectory(self, endpoint_result: EndpointResult | None = None) -> None:
        if self._prompt is None:
            return
        _write_text_atomic(
            self._logs_dir / "trajectory.json",
            _trajectory_json(
                self.events,
                agent_name=self._agent_name,
                agent_version=self._agent_version,
                model_name=self._model_name,
                endpoint_result=endpoint_result or self._partial_endpoint_result(),
                prompt=self._prompt,
            ),
        )

    def _partial_endpoint_result(self) -> EndpointResult:
        response_id = self._status.get("response_id")
        return EndpointResult(
            text="",
            response_id=response_id if isinstance(response_id, str) else None,
        )


def _relay_model(
    *,
    model_name: str | None,
    endpoint_impl: Endpoint | None,
) -> tuple[str, str | None]:
    if endpoint_impl is not None and (model_name is None or "/" not in model_name):
        return type(endpoint_impl).__name__, model_name
    if model_name is None:
        raise RelayError("Relay model_name must be provider-qualified: provider/model.")
    provider, separator, endpoint_model_name = model_name.partition("/")
    if not separator or not provider or not endpoint_model_name:
        raise RelayError("Relay model_name must be provider-qualified: provider/model.")
    return provider, endpoint_model_name


class RelayAgent(BaseAgent):
    SUPPORTS_ATIF = True
    SUPPORTS_WINDOWS = False

    def __init__(
        self,
        logs_dir: Path,
        model_name: str | None = None,
        *,
        endpoint_impl: Endpoint | None = None,
        workspace_root: str = "/workspace",
        include_globs: Sequence[str] | str | None = None,
        exclude_globs: Sequence[str] | str | None = _DEFAULT_EXCLUDES,
        max_files: int = 200,
        max_file_bytes: int = 200_000,
        max_total_file_bytes: int = 2_000_000,
        request: dict[str, Any] | None = None,
        endpoint: dict[str, Any] | None = None,
        extra_instruction: str | None = None,
        extra_env: Mapping[str, str] | None = None,
        require_files: bool = True,
        required_file_paths: Sequence[str] | str | None = None,
        max_full_restarts: int = 0,
        full_restart_initial_delay_sec: float = DEFAULT_FULL_RESTART_INITIAL_DELAY_SEC,
        full_restart_max_delay_sec: float = DEFAULT_FULL_RESTART_MAX_DELAY_SEC,
        **kwargs: Any,
    ):
        super().__init__(
            logs_dir=logs_dir,
            model_name=model_name,
            **kwargs,
        )
        self._endpoint = endpoint_impl
        self._provider, self._endpoint_model_name = _relay_model(
            model_name=model_name,
            endpoint_impl=endpoint_impl,
        )
        self._endpoint_name = self._provider
        self._workspace_root = PurePosixPath(workspace_root)
        self._include_globs = _coerce_patterns(include_globs)
        self._allow_env_examples = exclude_globs is _DEFAULT_EXCLUDES
        self._exclude_globs = _coerce_patterns(exclude_globs)
        self._max_files = max_files
        self._max_file_bytes = max_file_bytes
        self._max_total_file_bytes = max_total_file_bytes
        self._request = request or {}
        self._endpoint_config = endpoint or {}
        self._extra_instruction = extra_instruction
        self._extra_env = dict(extra_env or {})
        self._require_files = require_files
        self._required_file_paths = tuple(
            normalize_output_path(
                path,
                workspace_root=self._workspace_root,
            )
            for path in _coerce_patterns(required_file_paths)
        )
        self._max_full_restarts = max_full_restarts
        self._full_restart_initial_delay_sec = full_restart_initial_delay_sec
        self._full_restart_max_delay_sec = full_restart_max_delay_sec

    @staticmethod
    @override
    def name() -> str:
        return "relay"

    @override
    def version(self) -> str | None:
        try:
            return version("relay")
        except PackageNotFoundError:
            return "0.1.0"

    @override
    async def setup(self, environment: BaseEnvironment) -> None:
        await _exec_checked(
            environment,
            f"mkdir -p {shlex.quote(self._workspace_root.as_posix())}",
            retry_transient=True,
        )

    @override
    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        observer = _HarborRelayObserver(
            logs_dir=self.logs_dir,
            logger=self.logger,
            context=context,
            endpoint_name=self._endpoint_name,
            agent_name=self.name(),
            agent_version=self.version() or "unknown",
            model_name=self.model_name,
        )
        endpoint = self._make_endpoint()
        required_file_paths = self._required_file_paths_for_run(environment)
        relay_result = await Relay(
            endpoint=endpoint,
            workspace=_HarborWorkspace(
                environment=environment,
                root=self._workspace_root,
                include_globs=self._include_globs,
                exclude_globs=self._exclude_globs,
                allow_env_examples=self._allow_env_examples,
                max_files=self._max_files,
                max_file_bytes=self._max_file_bytes,
                max_total_file_bytes=self._max_total_file_bytes,
            ),
            observer=observer,
            prompt_sink=observer.write_prompt,
            extra_instruction=_join_extra_instructions(
                self._extra_instruction,
                _required_files_instruction(required_file_paths),
            ),
            require_files=self._require_files,
            required_file_paths=required_file_paths,
            max_full_restarts=self._max_full_restarts,
            full_restart_initial_delay_sec=self._full_restart_initial_delay_sec,
            full_restart_max_delay_sec=self._full_restart_max_delay_sec,
            usage_sink=lambda usage, cost_usd: _populate_context_usage(
                context,
                usage,
                cost_usd,
            ),
        ).run(instruction)
        self._write_logs(relay_result, observer)
        self._populate_context(context, relay_result)

    def _make_endpoint(self) -> Endpoint:
        if self._endpoint is not None:
            return self._endpoint
        factory = endpoint_factory(self._provider)
        return factory(
            model_name=self._endpoint_model_name,
            env=self._extra_env,
            request=self._request,
            **self._endpoint_config,
        )

    def _required_file_paths_for_run(
        self,
        environment: BaseEnvironment,
    ) -> tuple[PurePosixPath, ...]:
        task_paths = _task_required_file_paths(
            environment,
            workspace_root=self._workspace_root,
        )
        return tuple(dict.fromkeys((*task_paths, *self._required_file_paths)))

    def _write_logs(
        self,
        relay_result: RelayResult,
        observer: _HarborRelayObserver,
    ) -> None:
        _write_text_atomic(self.logs_dir / "final-message.md", relay_result.endpoint_result.text)
        _write_text_atomic(
            self.logs_dir / "result.json",
            json.dumps(_result_summary(relay_result), indent=2, sort_keys=True),
        )
        observer.write_trajectory(relay_result.endpoint_result)

    def _populate_context(
        self,
        context: AgentContext,
        relay_result: RelayResult,
    ) -> None:
        usage = relay_result.endpoint_result.usage
        _populate_context_usage(
            context,
            usage,
            relay_result.endpoint_result.cost_usd,
        )
        metadata = dict(context.metadata or {})
        metadata.update(
            {
                "endpoint": self._endpoint_name,
                "response_id": relay_result.endpoint_result.response_id,
                "cost_usd": relay_result.endpoint_result.cost_usd,
                "produced_files": [
                    {
                        "path": file.path.as_posix(),
                        "bytes": len(file.content),
                        "source": file.source,
                    }
                    for file in relay_result.files
                ],
            }
        )
        context.metadata = metadata


class _HarborWorkspace:
    def __init__(
        self,
        *,
        environment: BaseEnvironment,
        root: PurePosixPath,
        include_globs: Sequence[str],
        exclude_globs: Sequence[str],
        allow_env_examples: bool = False,
        max_files: int,
        max_file_bytes: int,
        max_total_file_bytes: int,
    ):
        self._environment = environment
        self._root = root
        self._include_globs = include_globs
        self._exclude_globs = exclude_globs
        self._allow_env_examples = allow_env_examples
        self._max_files = max_files
        self._max_file_bytes = max_file_bytes
        self._max_total_file_bytes = max_total_file_bytes

    @property
    def root(self) -> PurePosixPath:
        return self._root

    async def snapshot(self) -> WorkspaceSnapshot:
        remote_root = self._root.as_posix()
        command = (
            f"if [ -d {shlex.quote(remote_root)} ]; then "
            f"cd {shlex.quote(remote_root)} && "
            "find . -type f | sed 's#^\\./##' | LC_ALL=C sort; "
            "fi"
        )

        async def list_files():
            return await self._environment.exec(
                command,
                timeout_sec=_WORKSPACE_COMMAND_TIMEOUT_SEC,
            )

        result = await _retry_workspace_operation(
            "snapshot_list",
            list_files,
        )
        if result.return_code != 0:
            output = result.stderr or result.stdout or "no output"
            raise RelayError(f"Failed to list workspace files: {output}")

        paths = tuple(
            path
            for line in (result.stdout or "").splitlines()
            if (path := _safe_relative_path(line)) is not None
        )
        visible_paths = tuple(path for path in paths if self._should_include(path))
        files = await self._download_file_contents(visible_paths)
        return WorkspaceSnapshot(
            root=self._root,
            tree="\n".join(path.as_posix() for path in visible_paths),
            files=files,
        )

    async def _download_file_contents(
        self,
        paths: Sequence[PurePosixPath],
    ) -> tuple[WorkspaceFile, ...]:
        files: list[WorkspaceFile] = []
        remaining_total = self._max_total_file_bytes

        with tempfile.TemporaryDirectory(prefix="relay-workspace-") as temp_dir:
            temp_root = Path(temp_dir)
            for index, path in enumerate(paths[: self._max_files], start=1):
                if remaining_total <= 0:
                    break

                local_path = temp_root / f"file-{index}"
                remote_path = (self._root / path).as_posix()
                await _retry_workspace_operation(
                    "download_file",
                    lambda remote_path=remote_path, local_path=local_path: (
                        self._environment.download_file(remote_path, local_path)
                    ),
                )
                raw = local_path.read_bytes()
                limit = min(self._max_file_bytes, remaining_total)
                truncated = len(raw) > limit
                content = raw[:limit].decode("utf-8", errors="replace")
                remaining_total -= len(raw[:limit])
                files.append(
                    WorkspaceFile(
                        path=path,
                        content=content,
                        truncated=truncated,
                    )
                )

        return tuple(files)

    async def materialize(self, files: Sequence[ProducedFile]) -> None:
        with tempfile.TemporaryDirectory(prefix="relay-produced-") as temp_dir:
            temp_root = Path(temp_dir)
            prepared: list[tuple[ProducedFile, PurePosixPath, str, Path]] = []
            for index, file in enumerate(files, start=1):
                relative_path = normalize_output_path(
                    file.path.as_posix(),
                    workspace_root=self._root,
                )
                target_path = (self._root / relative_path).as_posix()
                local_path = temp_root / f"produced-{index}"
                local_path.write_bytes(file.content)
                prepared.append((file, relative_path, target_path, local_path))

            await _prepare_materialization_paths(
                self._environment,
                trusted_root=self._root,
                relative_paths=[relative_path for _, relative_path, _, _ in prepared],
            )

            for file, _, target_path, local_path in prepared:
                await _retry_workspace_operation(
                    "upload_file",
                    lambda local_path=local_path, target_path=target_path: (
                        self._environment.upload_file(local_path, target_path)
                    ),
                )
                if file.mode is not None:
                    await _exec_checked(
                        self._environment,
                        f"chmod {file.mode:o} {shlex.quote(target_path)}",
                        retry_transient=True,
                    )

            await self._mirror_produced_files_to_artifacts(prepared)

    async def _mirror_produced_files_to_artifacts(
        self,
        prepared: Sequence[tuple[ProducedFile, PurePosixPath, str, Path]],
    ) -> None:
        artifact_paths = [
            PurePosixPath(_PRODUCED_FILE_ARTIFACT_ROOT.name) / relative_path
            for _, relative_path, _, _ in prepared
        ]
        if not artifact_paths:
            return

        try:
            await _prepare_materialization_paths(
                self._environment,
                trusted_root=_PRODUCED_FILE_ARTIFACT_ROOT.parent,
                relative_paths=artifact_paths,
            )
            for _, relative_path, _, local_path in prepared:
                target_path = (_PRODUCED_FILE_ARTIFACT_ROOT / relative_path).as_posix()
                await _retry_workspace_operation(
                    "upload_artifact",
                    lambda local_path=local_path, target_path=target_path: (
                        self._environment.upload_file(local_path, target_path)
                    ),
                )
        except Exception as exc:
            print(
                "Warning: failed to mirror produced files to relay-output artifacts: "
                f"{type(exc).__name__}: {exc}",
                flush=True,
            )

    def _should_include(self, path: PurePosixPath) -> bool:
        text = path.as_posix()
        if self._include_globs and not _matches_any(text, self._include_globs):
            return False
        if self._allow_env_examples and path.name == ".env.example":
            return True
        return not _matches_any(text, self._exclude_globs)


async def _prepare_materialization_paths(
    environment: BaseEnvironment,
    *,
    trusted_root: PurePosixPath,
    relative_paths: Sequence[PurePosixPath],
) -> None:
    parent_paths = _materialization_parent_paths(trusted_root, relative_paths)
    if parent_paths:
        await _exec_checked(
            environment,
            _safe_parent_directories_command(parent_paths),
            retry_transient=True,
        )

    target_paths = tuple(trusted_root / path for path in relative_paths)
    if target_paths:
        await _exec_checked(
            environment,
            _reject_symlink_targets_command(target_paths),
            retry_transient=True,
        )


def _materialization_parent_paths(
    root: PurePosixPath,
    relative_paths: Sequence[PurePosixPath],
) -> tuple[PurePosixPath, ...]:
    parents: set[PurePosixPath] = set()
    for relative_path in relative_paths:
        current = root
        for part in relative_path.parent.parts:
            current /= part
            parents.add(current)
    return tuple(sorted(parents, key=lambda path: (len(path.parts), path.as_posix())))


def _safe_parent_directories_command(paths: Sequence[PurePosixPath]) -> str:
    arguments = " ".join(shlex.quote(path.as_posix()) for path in paths)
    return (
        f"set -e -- {arguments}\n"
        "for path\n"
        "do\n"
        '  if [ -L "$path" ]; then\n'
        "    printf '%s\\n' \"Refusing symlink materialization parent: $path\" >&2\n"
        "    exit 73\n"
        "  fi\n"
        '  if [ -e "$path" ]; then\n'
        '    if [ ! -d "$path" ]; then\n'
        "      printf '%s\\n' \"Materialization parent is not a directory: $path\" >&2\n"
        "      exit 73\n"
        "    fi\n"
        "  else\n"
        '    mkdir "$path"\n'
        "  fi\n"
        '  if [ -L "$path" ]; then\n'
        "    printf '%s\\n' \"Refusing symlink materialization parent: $path\" >&2\n"
        "    exit 73\n"
        "  fi\n"
        "done"
    )


def _reject_symlink_targets_command(paths: Sequence[PurePosixPath]) -> str:
    arguments = " ".join(shlex.quote(path.as_posix()) for path in paths)
    return (
        f"set -e -- {arguments}\n"
        "for path\n"
        "do\n"
        '  if [ -L "$path" ]; then\n'
        "    printf '%s\\n' \"Refusing symlink materialization target: $path\" >&2\n"
        "    exit 73\n"
        "  fi\n"
        "done"
    )


async def _exec_checked(
    environment: BaseEnvironment,
    command: str,
    *,
    retry_transient: bool = False,
) -> None:
    async def run_exec():
        return await environment.exec(
            command,
            timeout_sec=_WORKSPACE_COMMAND_TIMEOUT_SEC,
        )

    result = await (_retry_workspace_operation("exec", run_exec) if retry_transient else run_exec())
    if result.return_code == 0:
        return

    output = result.stderr or result.stdout or "no output"
    raise RelayError(f"Command failed: {command}\n{output}")


async def _retry_workspace_operation[T](
    label: str,
    operation: Callable[[], Awaitable[T]],
) -> T:
    delay = _WORKSPACE_RETRY_INITIAL_DELAY_SEC
    for attempt in range(1, _WORKSPACE_RETRY_ATTEMPTS + 1):
        try:
            return await operation()
        except Exception as exc:
            if attempt >= _WORKSPACE_RETRY_ATTEMPTS or not _is_transient_workspace_error(exc):
                raise
            print(
                "Retrying workspace operation "
                f"{label} after transient {type(exc).__name__} "
                f"(attempt {attempt}/{_WORKSPACE_RETRY_ATTEMPTS})",
                flush=True,
            )
            await asyncio.sleep(delay)
            delay = min(delay * 2, _WORKSPACE_RETRY_MAX_DELAY_SEC)

    raise AssertionError("unreachable")


def _is_transient_workspace_error(error: BaseException) -> bool:
    module = type(error).__module__
    name = type(error).__name__
    if module.startswith(("httpcore", "httpx")):
        return name in {
            "ConnectError",
            "ConnectTimeout",
            "PoolTimeout",
            "ReadError",
            "ReadTimeout",
            "RemoteProtocolError",
            "TimeoutException",
            "WriteError",
            "WriteTimeout",
        }
    if module.startswith("h2") and name == "ProtocolError":
        return True
    return module.startswith("e2b") and name == "TimeoutException"


def _task_required_file_paths(
    environment: BaseEnvironment,
    *,
    workspace_root: PurePosixPath = PurePosixPath("/workspace"),
) -> tuple[PurePosixPath, ...]:
    task_toml_path = Path(environment.environment_dir).parent / "task.toml"
    if not task_toml_path.is_file():
        raise RelayError(f"Harbor task configuration is missing: {task_toml_path}")
    try:
        document = tomllib.loads(task_toml_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise RelayError(f"Failed to parse task metadata from {task_toml_path}.") from exc

    metadata = document.get("metadata")
    if metadata is None:
        return ()
    if not isinstance(metadata, Mapping):
        raise RelayError("task.toml metadata must be a table.")

    declared = metadata.get("required_file_paths")
    if declared is None:
        return ()
    if not isinstance(declared, list):
        raise RelayError("task.toml metadata.required_file_paths must be an array of strings.")

    paths: list[PurePosixPath] = []
    for index, raw_path in enumerate(declared):
        if not isinstance(raw_path, str):
            raise RelayError(f"task.toml metadata.required_file_paths[{index}] must be a string.")
        if not raw_path.strip():
            raise RelayError(f"task.toml metadata.required_file_paths[{index}] must not be empty.")
        if PurePosixPath(raw_path.strip()).is_absolute():
            raise RelayError(
                f"task.toml metadata.required_file_paths[{index}] must be workspace-relative."
            )
        paths.append(normalize_output_path(raw_path, workspace_root=workspace_root))
    return tuple(dict.fromkeys(paths))


def _required_files_instruction(
    required_file_paths: Sequence[PurePosixPath],
) -> str | None:
    if not required_file_paths:
        return None
    files = "\n".join(f"- `{path.as_posix()}`" for path in required_file_paths)
    return (
        "Required final files. The run is only complete if all of these exact "
        "relative paths are delivered with valid task output. Do not create "
        "empty placeholder files for required outputs; an empty required file "
        f"is not a completed deliverable:\n{files}"
    )


def _join_extra_instructions(*parts: str | None) -> str | None:
    visible = [part.strip() for part in parts if part and part.strip()]
    return "\n\n".join(visible) if visible else None


def _coerce_patterns(value: Sequence[str] | str | None) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return tuple(part.strip() for part in value.split(",") if part.strip())
    return tuple(str(part) for part in value)


def _safe_relative_path(raw_path: str) -> PurePosixPath | None:
    if not raw_path.strip():
        return None
    try:
        return normalize_output_path(raw_path)
    except RelayError:
        return None


def _matches_any(path: str, patterns: Iterable[str]) -> bool:
    return any(_fnmatch_path(path, pattern) for pattern in patterns)


def _fnmatch_path(path: str, pattern: str) -> bool:
    return fnmatch(path, pattern) or fnmatch(f"/{path}", pattern)


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list | tuple | set):
        return [_jsonable(item) for item in value]
    if isinstance(value, Path | PurePosixPath):
        return value.as_posix()
    if value is None or isinstance(value, str | int | float | bool):
        return value
    return str(value)


def _event_log_suffix(metadata: dict[str, Any]) -> str:
    fields = metadata.get(LOG_FIELDS)
    if not isinstance(fields, Mapping):
        return ""
    return " ".join(f"{key}={value}" for key, value in fields.items() if value is not None)


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(text, encoding="utf-8")
    temp_path.replace(path)


def _usage_int(usage: dict[str, Any], key: str) -> int | None:
    value = usage.get(key)
    if value is None or isinstance(value, bool):
        return None
    return int(value)


def _populate_context_usage(
    context: AgentContext,
    usage: dict[str, Any],
    cost_usd: float | None,
) -> None:
    context.n_input_tokens = _usage_int(usage, USAGE_TOTAL_INPUT_TOKENS) or _usage_int(
        usage,
        USAGE_INPUT_TOKENS,
    )
    context.n_output_tokens = _usage_int(usage, USAGE_OUTPUT_TOKENS)
    context.n_cache_tokens = _usage_int(usage, USAGE_CACHE_READ_INPUT_TOKENS)
    context.cost_usd = cost_usd


def _trajectory_json(
    events: Sequence[dict[str, Any]],
    *,
    agent_name: str,
    agent_version: str,
    model_name: str | None,
    endpoint_result: EndpointResult,
    prompt: str,
) -> str:
    steps = [
        Step(
            step_id=1,
            source="user",
            message=prompt,
        )
    ]
    steps.extend(
        _trajectory_step(
            event,
            step_id=index,
            model_name=model_name,
        )
        for index, event in enumerate(events, start=2)
    )

    trajectory = Trajectory(
        session_id=endpoint_result.response_id,
        trajectory_id=endpoint_result.response_id,
        agent=TrajectoryAgent(
            name=agent_name,
            version=agent_version,
            model_name=model_name,
            extra=_agent_extra(endpoint_result),
        ),
        steps=steps,
        final_metrics=_final_metrics(
            endpoint_result.usage,
            endpoint_result.cost_usd,
            total_steps=len(steps),
        ),
    )
    return format_trajectory_json(trajectory.to_json_dict()) + "\n"


def _agent_extra(endpoint_result: EndpointResult) -> dict[str, Any] | None:
    if endpoint_result.response_id is None:
        return None
    return {"response_id": endpoint_result.response_id}


def _trajectory_step(
    event: dict[str, Any],
    *,
    step_id: int,
    model_name: str | None,
) -> Step:
    semantic_type = str(event.get("semantic_type") or "lifecycle")
    metadata = _jsonable(event.get("metadata") or {})
    timestamp = event.get("time")
    message = _event_text(event)

    if semantic_type == "reasoning":
        return Step(
            step_id=step_id,
            timestamp=timestamp,
            source="agent",
            model_name=model_name,
            message=str(event.get("message") or "Reasoning"),
            reasoning_content=message,
            extra=_step_extra(event, metadata),
        )
    if semantic_type == "narration":
        return Step(
            step_id=step_id,
            timestamp=timestamp,
            source="agent",
            model_name=model_name,
            message=message,
            extra=_step_extra(event, metadata),
        )
    if semantic_type == "tool_call":
        return Step(
            step_id=step_id,
            timestamp=timestamp,
            source="agent",
            model_name=model_name,
            message=str(event.get("message") or "Tool call."),
            tool_calls=[_tool_call(step_id, metadata)],
            extra=_step_extra(event, metadata),
        )
    if semantic_type == "tool_result":
        return Step(
            step_id=step_id,
            timestamp=timestamp,
            source="agent",
            model_name=model_name,
            message=str(event.get("message") or "Tool result."),
            tool_calls=[_tool_call(step_id, metadata)],
            observation=Observation(
                results=[
                    ObservationResult(
                        content=_tool_result_content(metadata, fallback=message),
                        extra=_visible_metadata(metadata),
                    )
                ]
            ),
            extra=_step_extra(event, metadata),
        )
    if semantic_type == "usage":
        usage, cost_usd = usage_from_event_metadata(metadata)
        return Step(
            step_id=step_id,
            timestamp=timestamp,
            source="agent",
            model_name=model_name,
            message=message,
            metrics=_metrics(usage, cost_usd),
            llm_call_count=1,
            extra=_step_extra(event, metadata),
        )
    return Step(
        step_id=step_id,
        timestamp=timestamp,
        source="system",
        message=message,
        observation=Observation(
            results=[ObservationResult(content=message, extra=metadata or None)]
        )
        if semantic_type == "artifact"
        else None,
        extra=_step_extra(event, metadata),
    )


def _event_text(event: dict[str, Any]) -> str:
    metadata = event.get("metadata") or {}
    for key in (EVENT_TEXT, EVENT_TEXT_PREVIEW):
        value = metadata.get(key)
        if isinstance(value, str) and value:
            return value
    return str(event.get("message") or event.get("name") or "Relay event.")


def _tool_call(step_id: int, metadata: dict[str, Any]) -> ToolCall:
    return ToolCall(
        tool_call_id=str(metadata.get("tool_call_id") or f"tool-{step_id}"),
        function_name=str(
            metadata.get("tool_name")
            or metadata.get("tool_type")
            or metadata.get("event_type")
            or "tool"
        ),
        arguments=_tool_arguments(metadata),
        extra=_visible_metadata(metadata),
    )


def _tool_arguments(metadata: dict[str, Any]) -> dict[str, Any]:
    arguments = metadata.get(TOOL_ARGUMENTS)
    if not isinstance(arguments, Mapping):
        return {}
    return {str(key): value for key, value in _jsonable(arguments).items() if value is not None}


def _tool_result_content(metadata: dict[str, Any], *, fallback: str) -> str:
    result = metadata.get(TOOL_RESULT)
    if result in (None, "", [], {}):
        return fallback
    if isinstance(result, str):
        return result
    return json.dumps(_without_none(_jsonable(result)), indent=2, sort_keys=True)


def _without_none(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _without_none(item) for key, item in value.items() if item is not None}
    if isinstance(value, list):
        return [_without_none(item) for item in value]
    return value


def _metrics(usage: dict[str, Any], cost_usd: float | None) -> Metrics:
    return Metrics(
        prompt_tokens=_usage_int(usage, USAGE_TOTAL_INPUT_TOKENS)
        or _usage_int(usage, USAGE_INPUT_TOKENS),
        completion_tokens=_usage_int(usage, USAGE_OUTPUT_TOKENS),
        cached_tokens=_usage_int(usage, USAGE_CACHE_READ_INPUT_TOKENS),
        cost_usd=cost_usd,
        extra=_usage_extra(usage),
    )


def _final_metrics(
    usage: dict[str, Any],
    cost_usd: float | None,
    *,
    total_steps: int,
) -> FinalMetrics:
    return FinalMetrics(
        total_prompt_tokens=_usage_int(usage, USAGE_TOTAL_INPUT_TOKENS)
        or _usage_int(usage, USAGE_INPUT_TOKENS),
        total_completion_tokens=_usage_int(usage, USAGE_OUTPUT_TOKENS),
        total_cached_tokens=_usage_int(usage, USAGE_CACHE_READ_INPUT_TOKENS),
        total_cost_usd=cost_usd,
        total_steps=total_steps,
        extra=_usage_extra(usage),
    )


def _usage_extra(usage: dict[str, Any]) -> dict[str, Any] | None:
    return {
        key: value
        for key, value in usage.items()
        if key
        not in {
            USAGE_INPUT_TOKENS,
            USAGE_TOTAL_INPUT_TOKENS,
            USAGE_OUTPUT_TOKENS,
            USAGE_CACHE_READ_INPUT_TOKENS,
        }
    } or None


def _step_extra(event: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    extra = {
        "relay_event": event.get("name"),
        "relay_semantic_type": event.get("semantic_type"),
    }
    metadata_extra = _visible_metadata(metadata)
    if metadata_extra is not None:
        extra["metadata"] = metadata_extra
    return extra


def _visible_metadata(metadata: dict[str, Any]) -> dict[str, Any] | None:
    value = {
        key: item
        for key, item in metadata.items()
        if key not in {LOG_FIELDS, TOOL_ARGUMENTS, TOOL_RESULT, EVENT_TEXT} and item is not None
    }
    return value or None


def _result_summary(relay_result: RelayResult) -> dict[str, Any]:
    endpoint_result = relay_result.endpoint_result
    return {
        "response_id": endpoint_result.response_id,
        "usage": endpoint_result.usage,
        "cost_usd": endpoint_result.cost_usd,
        "artifacts": [
            {
                "name": artifact.name,
                "bytes": len(artifact.content),
                "source": artifact.source,
            }
            for artifact in endpoint_result.artifacts
        ],
        "tool_outputs": [
            {
                "command": output.command,
                "bytes": len(output.stdout.encode()),
                "source": output.source,
            }
            for output in endpoint_result.tool_outputs
        ],
        "produced_files": [
            {
                "path": file.path.as_posix(),
                "bytes": len(file.content),
                "mode": file.mode,
                "source": file.source,
            }
            for file in relay_result.files
        ],
    }
