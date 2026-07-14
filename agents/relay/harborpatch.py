"""Opt-in Harbor concurrency and environment reliability patches.

Some workloads need to start many remote agents promptly while keeping verifier
pressure bounded as completed trials enter expensive judging pipelines. This
module also keeps Docker and E2B execution reliable for long verifier runs. It
patches Harbor only when explicitly enabled through environment variables.
"""

from __future__ import annotations

import asyncio
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import resource
import shlex
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from types import SimpleNamespace
from typing import Any

from harbor.environments.definition import environment_content_hash
from harbor.trial.single_step import SingleStepTrial
from harbor.trial.trial import Trial
from harbor.verifier.verifier import Verifier

try:
    from e2b.template_async.main import AsyncTemplate
except ImportError:  # pragma: no cover - Harbor installed without E2B support
    AsyncTemplate = None  # type: ignore[assignment,misc]

try:
    from harbor.environments.e2b import E2BEnvironment
except ImportError:  # pragma: no cover - Harbor installed without E2B support
    E2BEnvironment = None  # type: ignore[assignment,misc]

try:
    from harbor.trial.multi_step import MultiStepTrial
except ImportError:  # pragma: no cover - Harbor versions without multi-step trials
    MultiStepTrial = None  # type: ignore[assignment,misc]


AGENT_LIMIT_ENV = "HARBOR_N_CONCURRENT_AGENT_PHASES"
VERIFIER_LIMIT_ENV = "HARBOR_N_CONCURRENT_VERIFIER_PHASES"
E2B_USE_DOCKERFILE_ENV = "HARBOR_E2B_USE_DOCKERFILE"
E2B_STREAM_OUTPUT_ENV = "HARBOR_E2B_STREAM_OUTPUT"
E2B_SHARE_TEMPLATE_BY_HASH_ENV = "HARBOR_E2B_SHARE_TEMPLATE_BY_HASH"
NOFILE_SOFT_LIMIT_ENV = "HARBOR_NOFILE_SOFT_LIMIT"
E2B_TEMPLATE_CACHE_ENV = "HARBOR_E2B_TEMPLATE_CACHE_DIR"
E2B_TEMPLATE_REQUEST_TIMEOUT_ENV = "HARBOR_E2B_TEMPLATE_REQUEST_TIMEOUT"
E2B_TEMPLATE_REQUEST_TIMEOUT_DEFAULT = 600.0
E2B_FILESYSTEM_RETRY_ATTEMPTS_ENV = "HARBOR_E2B_FILESYSTEM_RETRY_ATTEMPTS"
E2B_FILESYSTEM_RETRY_ATTEMPTS_DEFAULT = 5
E2B_FILESYSTEM_RETRY_INITIAL_DELAY = 1.0
E2B_FILESYSTEM_RETRY_MAX_DELAY = 20.0
E2B_VERIFIER_TERMINAL_WAIT_ENV = "HARBOR_E2B_VERIFIER_TERMINAL_WAIT"
E2B_VERIFIER_TERMINAL_WAIT_DEFAULT = 900.0
E2B_VERIFIER_TERMINAL_POLL_INTERVAL = 2.0
E2B_VERIFIER_REWARD_SETTLE_SECONDS = 5.0
E2B_VERIFIER_SETUP_COMMAND_TIMEOUT_SEC = 60
E2B_VERIFIER_COMPLETE_PATH = "/logs/verifier/.complete"
E2B_VERIFIER_ERROR_PATH = "/logs/verifier/error.json"
E2B_VERIFIER_STDOUT_PATH = "/logs/verifier/test-stdout.txt"
E2B_VERIFIER_REDIRECT_COMMAND = f"(/tests/test.sh) > {E2B_VERIFIER_STDOUT_PATH} 2>&1"
E2B_VERIFIER_REDIRECT_COMMAND_ALIASES = (
    E2B_VERIFIER_REDIRECT_COMMAND,
    f"bash /tests/test.sh > {E2B_VERIFIER_STDOUT_PATH} 2>&1",
)
E2B_VERIFIER_LOG_SYNC_INTERVAL = 2.0
E2B_VERIFIER_REWARD_PATHS = (
    "/logs/verifier/reward.json",
    "/logs/verifier/reward.txt",
)
_ORIGINAL_ATTR = "__relay_harborpatch_original__"


@dataclass
class _LimitState:
    agent_limit: int | None = None
    verifier_limit: int | None = None
    e2b_use_dockerfile: bool = False
    e2b_stream_output: bool = False
    e2b_share_template_by_hash: bool = False
    agent_semaphores: dict[asyncio.AbstractEventLoop, asyncio.Semaphore] = field(
        default_factory=dict
    )
    verifier_semaphores: dict[asyncio.AbstractEventLoop, asyncio.Semaphore] = field(
        default_factory=dict
    )

    def configure(
        self,
        *,
        agent_limit: int | None,
        verifier_limit: int | None,
        e2b_use_dockerfile: bool,
        e2b_stream_output: bool,
        e2b_share_template_by_hash: bool,
    ) -> None:
        if agent_limit != self.agent_limit:
            self.agent_semaphores.clear()
        if verifier_limit != self.verifier_limit:
            self.verifier_semaphores.clear()
        self.agent_limit = agent_limit
        self.verifier_limit = verifier_limit
        self.e2b_use_dockerfile = e2b_use_dockerfile
        self.e2b_stream_output = e2b_stream_output
        self.e2b_share_template_by_hash = e2b_share_template_by_hash

    def agent_semaphore(self) -> asyncio.Semaphore:
        if self.agent_limit is None:
            raise RuntimeError("agent phase limit is not configured")
        return self._semaphore(self.agent_semaphores, self.agent_limit)

    def verifier_semaphore(self) -> asyncio.Semaphore:
        if self.verifier_limit is None:
            raise RuntimeError("verifier phase limit is not configured")
        return self._semaphore(self.verifier_semaphores, self.verifier_limit)

    @staticmethod
    def _semaphore(
        semaphores: dict[asyncio.AbstractEventLoop, asyncio.Semaphore],
        limit: int,
    ) -> asyncio.Semaphore:
        loop = asyncio.get_running_loop()
        semaphore = semaphores.get(loop)
        if semaphore is None:
            semaphore = asyncio.Semaphore(limit)
            semaphores[loop] = semaphore
        return semaphore


_STATE = _LimitState()


def _parse_optional_positive_int(value: str | None, *, env_name: str) -> int | None:
    if value is None or value.strip() == "":
        return None
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{env_name} must be a positive integer, got {value!r}") from exc
    if parsed < 1:
        raise ValueError(f"{env_name} must be a positive integer, got {value!r}")
    return parsed


def _parse_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def install_from_env() -> bool:
    """Install phase limits from environment variables.

    Returns True when at least one limit is configured. With neither env set,
    this is a no-op.
    """

    agent_limit = _parse_optional_positive_int(
        os.environ.get(AGENT_LIMIT_ENV),
        env_name=AGENT_LIMIT_ENV,
    )
    verifier_limit = _parse_optional_positive_int(
        os.environ.get(VERIFIER_LIMIT_ENV),
        env_name=VERIFIER_LIMIT_ENV,
    )
    e2b_use_dockerfile = _parse_bool(os.environ.get(E2B_USE_DOCKERFILE_ENV))
    e2b_stream_output = _parse_bool(os.environ.get(E2B_STREAM_OUTPUT_ENV))
    e2b_share_template_by_hash = _parse_bool(os.environ.get(E2B_SHARE_TEMPLATE_BY_HASH_ENV))
    nofile_soft_limit = _parse_optional_positive_int(
        os.environ.get(NOFILE_SOFT_LIMIT_ENV),
        env_name=NOFILE_SOFT_LIMIT_ENV,
    )
    _raise_nofile_limit(nofile_soft_limit)

    if (
        agent_limit is None
        and verifier_limit is None
        and not e2b_use_dockerfile
        and not e2b_stream_output
        and not e2b_share_template_by_hash
    ):
        return nofile_soft_limit is not None
    install(
        agent_limit=agent_limit,
        verifier_limit=verifier_limit,
        e2b_use_dockerfile=e2b_use_dockerfile,
        e2b_stream_output=e2b_stream_output,
        e2b_share_template_by_hash=e2b_share_template_by_hash,
    )
    return True


def _raise_nofile_limit(target_soft_limit: int | None) -> None:
    if target_soft_limit is None:
        return

    soft_limit, hard_limit = resource.getrlimit(resource.RLIMIT_NOFILE)
    if soft_limit >= target_soft_limit:
        return

    target = target_soft_limit
    if hard_limit != resource.RLIM_INFINITY:
        target = min(target, hard_limit)
    if target <= soft_limit:
        return

    resource.setrlimit(resource.RLIMIT_NOFILE, (target, hard_limit))


def install(
    *,
    agent_limit: int | None,
    verifier_limit: int | None,
    e2b_use_dockerfile: bool = False,
    e2b_stream_output: bool = False,
    e2b_share_template_by_hash: bool = False,
) -> None:
    """Install phase limits onto Harbor's trial classes."""

    _install_classes(
        agent_limit=agent_limit,
        verifier_limit=verifier_limit,
        e2b_use_dockerfile=e2b_use_dockerfile,
        e2b_stream_output=e2b_stream_output,
        e2b_share_template_by_hash=e2b_share_template_by_hash,
        trial_cls=Trial,
        single_step_cls=SingleStepTrial,
        multi_step_cls=MultiStepTrial,
        e2b_cls=(
            E2BEnvironment
            if e2b_use_dockerfile or e2b_stream_output or e2b_share_template_by_hash
            else None
        ),
        verifier_cls=Verifier,
    )


def _install_classes(
    *,
    agent_limit: int | None,
    verifier_limit: int | None,
    trial_cls: type[Any],
    single_step_cls: type[Any],
    multi_step_cls: type[Any] | None = None,
    e2b_cls: type[Any] | None = None,
    verifier_cls: type[Any] | None = None,
    e2b_use_dockerfile: bool = False,
    e2b_stream_output: bool = False,
    e2b_share_template_by_hash: bool = False,
) -> None:
    _STATE.configure(
        agent_limit=agent_limit,
        verifier_limit=verifier_limit,
        e2b_use_dockerfile=e2b_use_dockerfile,
        e2b_stream_output=e2b_stream_output,
        e2b_share_template_by_hash=e2b_share_template_by_hash,
    )

    if agent_limit is not None:
        _patch_agent_phase(trial_cls)
    if (
        verifier_limit is not None
        or e2b_use_dockerfile
        or e2b_stream_output
        or e2b_share_template_by_hash
    ):
        _patch_verifier_phase(single_step_cls, "_run_verifier")
        if multi_step_cls is not None and hasattr(multi_step_cls, "_run_step_verifier"):
            _patch_verifier_phase(multi_step_cls, "_run_step_verifier")
        if verifier_cls is not None:
            _patch_verifier_missing_reward_error(verifier_cls)
    if (e2b_use_dockerfile or e2b_share_template_by_hash) and e2b_cls is not None:
        _patch_e2b_use_dockerfile(e2b_cls)
        _patch_e2b_filesystem_retries(e2b_cls)
        _patch_e2b_verifier_exec_stream_disconnect(e2b_cls)
        _patch_e2b_template_build_timeout(e2b_cls)
    if e2b_share_template_by_hash and e2b_cls is not None:
        _patch_e2b_shared_template_start(e2b_cls)
    if e2b_stream_output and e2b_cls is not None:
        _patch_e2b_verifier_exec_stream_disconnect(e2b_cls)
        _patch_trial_log_context(trial_cls)
        _patch_e2b_stream_output(e2b_cls)


def _patch_agent_phase(trial_cls: type[Any]) -> None:
    method_name = "_run_agent_phase"
    current = getattr(trial_cls, method_name)
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def limited_agent_phase(self: Any, *args: Any, **kwargs: Any) -> Any:
        if _STATE.agent_limit is None:
            return await current(self, *args, **kwargs)
        async with _STATE.agent_semaphore():
            return await current(self, *args, **kwargs)

    setattr(limited_agent_phase, _ORIGINAL_ATTR, current)
    setattr(trial_cls, method_name, limited_agent_phase)


def _patch_verifier_phase(cls: type[Any], method_name: str) -> None:
    current = getattr(cls, method_name)
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def limited_verifier_phase(self: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            if _STATE.verifier_limit is None or _verifier_disabled(self):
                return await current(self, *args, **kwargs)
            async with _STATE.verifier_semaphore():
                return await current(self, *args, **kwargs)
        finally:
            await _refresh_e2b_convention_artifacts_after_verifier(self)

    setattr(limited_verifier_phase, _ORIGINAL_ATTR, current)
    setattr(cls, method_name, limited_verifier_phase)


def _patch_trial_log_context(trial_cls: type[Any]) -> None:
    current = getattr(trial_cls, "_log_context", None)
    if current is None or hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    def log_context_with_e2b_verifier_file_tee(
        self: Any,
        phase: str,
        environment: Any,
        step_name: str | None = None,
    ) -> contextlib.AbstractContextManager[None]:
        base_context = current(self, phase, environment, step_name)
        if not (
            _STATE.e2b_stream_output
            and phase == "verification"
            and _is_e2b_environment(environment)
        ):
            return base_context

        live_log_path = _verifier_live_stdout_path(self)
        if live_log_path is None:
            return base_context

        live_log = _LiveVerifierLog(live_log_path)

        async def tee_to_local_file(text: str, _stream: str) -> None:
            await asyncio.to_thread(live_log.append_stream, text)

        return _combined_contexts(
            base_context,
            environment.scoped_output_callback(tee_to_local_file),
            _e2b_live_log_sync_context(environment, live_log),
        )

    setattr(log_context_with_e2b_verifier_file_tee, _ORIGINAL_ATTR, current)
    setattr(trial_cls, "_log_context", log_context_with_e2b_verifier_file_tee)


@contextlib.contextmanager
def _combined_contexts(
    *contexts: contextlib.AbstractContextManager[None],
) -> Any:
    with contextlib.ExitStack() as stack:
        for context in contexts:
            stack.enter_context(context)
        yield


def _verifier_live_stdout_path(trial: Any) -> Path | None:
    paths = getattr(trial, "paths", None)
    verifier_dir = getattr(paths, "verifier_dir", None)
    if verifier_dir is None:
        return None
    return Path(verifier_dir) / "test-stdout.txt"


class _LiveVerifierLog:
    def __init__(self, path: Path):
        self.path = path
        self._content = ""
        self._stream_offset = 0
        self._lock = threading.Lock()

    def append_stream(self, text: str) -> None:
        if not text:
            return
        with self._lock:
            expected = self._content[self._stream_offset : self._stream_offset + len(text)]
            if expected == text:
                self._stream_offset += len(text)
                return

            self._content += text
            self._stream_offset = len(self._content)
            self._append_locked(text)

    def merge_remote_file(self, remote_path: Path) -> None:
        remote_content = remote_path.read_text(encoding="utf-8", errors="replace")
        with self._lock:
            if remote_content == self._content:
                return
            if remote_content.startswith(self._content):
                self._content = remote_content
            elif not self._content.startswith(remote_content):
                self._content = remote_content
            self._stream_offset = min(self._stream_offset, len(self._content))
            self._write_locked()

    def _write_locked(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(self._content, encoding="utf-8")

    def _append_locked(self, text: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(text)


@contextlib.contextmanager
def _e2b_live_log_sync_context(environment: Any, live_log: _LiveVerifierLog) -> Any:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        yield
        return

    task = loop.create_task(_sync_e2b_verifier_log(environment, live_log))
    task.add_done_callback(_consume_cancelled_task)
    try:
        yield
    finally:
        task.cancel()


async def _sync_e2b_verifier_log(
    environment: Any,
    live_log: _LiveVerifierLog,
) -> None:
    remote_target = live_log.path.with_name(f".{live_log.path.name}.remote")
    while True:
        try:
            remote_target.parent.mkdir(parents=True, exist_ok=True)
            await environment.download_file(E2B_VERIFIER_STDOUT_PATH, remote_target)
            await asyncio.to_thread(live_log.merge_remote_file, remote_target)
        except asyncio.CancelledError:
            raise
        except Exception:
            pass
        finally:
            with contextlib.suppress(FileNotFoundError):
                remote_target.unlink()
        await asyncio.sleep(E2B_VERIFIER_LOG_SYNC_INTERVAL)


def _consume_cancelled_task(task: asyncio.Task[Any]) -> None:
    if task.cancelled():
        return
    with contextlib.suppress(Exception):
        task.result()


def _patch_e2b_use_dockerfile(e2b_cls: type[Any]) -> None:
    current = getattr(e2b_cls, "__init__")
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    def init_with_task_dockerfile(
        self: Any,
        environment_dir: Path,
        environment_name: str,
        session_id: str,
        trial_paths: Any,
        task_env_config: Any,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if _STATE.e2b_use_dockerfile:
            task_env_config = task_env_config.model_copy(update={"docker_image": None})
        current(
            self,
            environment_dir,
            environment_name,
            session_id,
            trial_paths,
            task_env_config,
            *args,
            **kwargs,
        )
        if _STATE.e2b_share_template_by_hash:
            _set_e2b_shared_template_name(self)

    setattr(init_with_task_dockerfile, _ORIGINAL_ATTR, current)
    setattr(e2b_cls, "__init__", init_with_task_dockerfile)


def _patch_e2b_stream_output(e2b_cls: type[Any]) -> None:
    current = getattr(e2b_cls, "_dispatch_command")
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def dispatch_command_with_output_streaming(
        self: Any,
        command: str,
        *,
        cwd: str | None,
        env: dict[str, str] | None,
        timeout_sec: int | None,
        user: str,
    ) -> Any:
        if not _STATE.e2b_stream_output:
            return await current(
                self,
                command,
                cwd=cwd,
                env=env,
                timeout_sec=timeout_sec,
                user=user,
            )
        if not self._sandbox:
            raise RuntimeError("Sandbox not found. Please start the environment first.")

        callback = self._output_callback()
        command = _streamable_e2b_command(command)

        async def on_stdout(text: str) -> None:
            if callback is not None:
                await callback(text, "stdout")

        async def on_stderr(text: str) -> None:
            if callback is not None:
                await callback(text, "stderr")

        return await self._sandbox.commands.run(
            cmd=command,
            background=True,
            cwd=cwd,
            envs=env,
            timeout=timeout_sec or 0,
            user=user,
            on_stdout=on_stdout if callback is not None else None,
            on_stderr=on_stderr if callback is not None else None,
        )

    setattr(dispatch_command_with_output_streaming, _ORIGINAL_ATTR, current)
    setattr(e2b_cls, "_dispatch_command", dispatch_command_with_output_streaming)


def _streamable_e2b_command(command: str) -> str:
    if command.strip() not in E2B_VERIFIER_REDIRECT_COMMAND_ALIASES:
        return command
    script = f"set -o pipefail; (/tests/test.sh) 2>&1 | tee {shlex.quote(E2B_VERIFIER_STDOUT_PATH)}"
    return f"bash -lc {shlex.quote(script)}"


def _patch_e2b_filesystem_retries(e2b_cls: type[Any]) -> None:
    for method_name in (
        "upload_file",
        "upload_dir",
        "download_file",
        "download_dir",
        "is_file",
        "is_dir",
    ):
        if hasattr(e2b_cls, method_name):
            _patch_e2b_filesystem_method(e2b_cls, method_name)


def _patch_e2b_filesystem_method(e2b_cls: type[Any], method_name: str) -> None:
    current = getattr(e2b_cls, method_name)
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def filesystem_method_with_retries(
        self: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        attempts = _e2b_filesystem_retry_attempts()
        delay = E2B_FILESYSTEM_RETRY_INITIAL_DELAY
        for attempt in range(1, attempts + 1):
            try:
                return await current(self, *args, **kwargs)
            except Exception as exc:
                if attempt >= attempts or not _is_e2b_transport_error(exc):
                    raise
                logger = getattr(self, "logger", None)
                if logger is not None:
                    logger.warning(
                        "Retrying E2B filesystem method %s after transient %s (attempt %s/%s)",
                        method_name,
                        type(exc).__name__,
                        attempt,
                        attempts,
                    )
                await asyncio.sleep(delay)
                delay = min(delay * 2, E2B_FILESYSTEM_RETRY_MAX_DELAY)

    setattr(filesystem_method_with_retries, _ORIGINAL_ATTR, current)
    setattr(e2b_cls, method_name, filesystem_method_with_retries)


def _patch_e2b_verifier_exec_stream_disconnect(e2b_cls: type[Any]) -> None:
    if not hasattr(e2b_cls, "exec"):
        return
    current = getattr(e2b_cls, "exec")
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def exec_with_verifier_stream_disconnect_recovery(
        self: Any,
        command: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if _is_idempotent_verifier_setup_command(command):
            return await _exec_idempotent_e2b_command(
                self,
                current,
                command,
                args,
                kwargs,
            )
        try:
            result = await current(self, command, *args, **kwargs)
        except Exception as exc:
            if not (_is_verifier_test_command(command) and _is_command_stream_disconnect(exc)):
                raise
            return await _wait_for_e2b_verifier_terminal_file(self, exc)
        if (
            _STATE.e2b_stream_output
            and _is_verifier_test_command(command)
            and getattr(result, "return_code", None) == 0
        ):
            return await _wait_for_e2b_verifier_terminal_file_after_success(
                self,
                result,
            )
        return result

    setattr(exec_with_verifier_stream_disconnect_recovery, _ORIGINAL_ATTR, current)
    setattr(e2b_cls, "exec", exec_with_verifier_stream_disconnect_recovery)


def _is_idempotent_verifier_setup_command(command: str) -> bool:
    parts = command.strip().split()
    return len(parts) == 3 and parts[:2] == ["chmod", "+x"] and parts[2].startswith("/tests/")


async def _exec_idempotent_e2b_command(
    environment: Any,
    current: Callable[..., Any],
    command: str,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> Any:
    attempts = _e2b_filesystem_retry_attempts()
    adjusted_kwargs = dict(kwargs)
    adjusted_kwargs.setdefault("timeout_sec", E2B_VERIFIER_SETUP_COMMAND_TIMEOUT_SEC)
    delay = E2B_FILESYSTEM_RETRY_INITIAL_DELAY
    for attempt in range(1, attempts + 1):
        try:
            return await current(environment, command, *args, **adjusted_kwargs)
        except Exception as exc:
            if attempt >= attempts or not _is_e2b_transport_error(exc):
                raise
            logger = getattr(environment, "logger", None)
            if logger is not None:
                logger.warning(
                    "Retrying idempotent E2B command after transient %s (attempt %s/%s): %s",
                    type(exc).__name__,
                    attempt,
                    attempts,
                    command,
                )
            await asyncio.sleep(delay)
            delay = min(delay * 2, E2B_FILESYSTEM_RETRY_MAX_DELAY)
    raise AssertionError("unreachable")


def _is_verifier_test_command(command: str) -> bool:
    return "/tests/" in command and "test.sh" in command


def _is_command_stream_disconnect(error: BaseException) -> bool:
    return _is_e2b_transport_error(error)


def _is_e2b_transport_error(error: BaseException) -> bool:
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


def _patch_verifier_missing_reward_error(verifier_cls: type[Any]) -> None:
    current = getattr(verifier_cls, "verify")
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def verify_with_error_context(self: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return await current(self, *args, **kwargs)
        except Exception as exc:
            if type(exc).__name__ != "RewardFileNotFoundError":
                raise
            raise RuntimeError(_missing_reward_error_message(self, exc)) from exc

    setattr(verify_with_error_context, _ORIGINAL_ATTR, current)
    setattr(verifier_cls, "verify", verify_with_error_context)


def _missing_reward_error_message(verifier: Any, error: BaseException) -> str:
    paths = getattr(verifier, "trial_paths", None)
    verifier_dir = Path(getattr(paths, "verifier_dir", "verifier"))
    error_path = verifier_dir / "error.json"
    if error_path.exists():
        return (
            "Verifier failed before writing a reward file; "
            f"{error_path} says:\n{_read_verifier_error(error_path)}"
        )

    return "\n\n".join(
        part
        for part in (
            str(error),
            "Verifier finished without reward.json/reward.txt and did not write error.json.",
            _tail_file(verifier_dir / "test-stdout.txt", "verifier stdout"),
        )
        if part
    )


def _read_verifier_error(path: Path) -> str:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return path.read_text(encoding="utf-8", errors="replace").strip()
    if isinstance(parsed, dict) and isinstance(parsed.get("error"), str):
        return parsed["error"]
    return json.dumps(parsed, indent=2, ensure_ascii=False)


def _tail_file(path: Path, label: str, *, lines: int = 40) -> str:
    if not path.exists() or path.stat().st_size == 0:
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    tail = "\n".join(text.splitlines()[-lines:])
    return f"Last {label} lines from {path}:\n{tail}"


def _e2b_filesystem_retry_attempts() -> int:
    raw = os.environ.get(E2B_FILESYSTEM_RETRY_ATTEMPTS_ENV)
    if raw is None or raw.strip() == "":
        return E2B_FILESYSTEM_RETRY_ATTEMPTS_DEFAULT
    return (
        _parse_optional_positive_int(
            raw,
            env_name=E2B_FILESYSTEM_RETRY_ATTEMPTS_ENV,
        )
        or E2B_FILESYSTEM_RETRY_ATTEMPTS_DEFAULT
    )


async def _wait_for_e2b_verifier_terminal_file(
    environment: Any,
    disconnect_error: BaseException,
) -> Any:
    deadline = time.monotonic() + _e2b_verifier_terminal_wait_seconds()
    reward_seen_at: float | None = None
    while True:
        if await _e2b_file_exists(environment, E2B_VERIFIER_COMPLETE_PATH):
            return _e2b_verifier_stream_disconnect_result(
                disconnect_error,
                f"remote verifier completed: {E2B_VERIFIER_COMPLETE_PATH}",
                return_code=0,
            )
        if await _e2b_file_exists(environment, E2B_VERIFIER_ERROR_PATH):
            return _e2b_verifier_stream_disconnect_result(
                disconnect_error,
                f"remote verifier failed: {E2B_VERIFIER_ERROR_PATH}",
                return_code=1,
            )

        if reward_seen_at is None and await _e2b_any_file_exists(
            environment,
            E2B_VERIFIER_REWARD_PATHS,
        ):
            reward_seen_at = time.monotonic()
        if (
            reward_seen_at is not None
            and time.monotonic() - reward_seen_at >= E2B_VERIFIER_REWARD_SETTLE_SECONDS
        ):
            return _e2b_verifier_stream_disconnect_result(
                disconnect_error,
                "remote verifier reward file appeared",
                return_code=0,
            )

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return _e2b_verifier_stream_disconnect_result(
                disconnect_error,
                "timed out waiting for remote verifier terminal files",
                return_code=1,
            )
        await asyncio.sleep(min(E2B_VERIFIER_TERMINAL_POLL_INTERVAL, remaining))


async def _wait_for_e2b_verifier_terminal_file_after_success(
    environment: Any,
    result: Any,
) -> Any:
    if await _e2b_verifier_terminal_file_seen(environment):
        return result

    deadline = time.monotonic() + _e2b_verifier_terminal_wait_seconds()
    while True:
        if await _e2b_verifier_terminal_file_seen(environment):
            return result
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return _e2b_verifier_missing_terminal_result(result)
        await asyncio.sleep(min(E2B_VERIFIER_TERMINAL_POLL_INTERVAL, remaining))


async def _e2b_verifier_terminal_file_seen(environment: Any) -> bool:
    return (
        await _e2b_file_exists(environment, E2B_VERIFIER_COMPLETE_PATH)
        or await _e2b_file_exists(environment, E2B_VERIFIER_ERROR_PATH)
        or await _e2b_any_file_exists(environment, E2B_VERIFIER_REWARD_PATHS)
    )


def _e2b_verifier_missing_terminal_result(result: Any) -> Any:
    stderr = getattr(result, "stderr", "") or ""
    message = (
        "E2B verifier command ended before any terminal verifier artifact "
        f"appeared: {E2B_VERIFIER_COMPLETE_PATH}, {E2B_VERIFIER_ERROR_PATH}, "
        f"or {', '.join(E2B_VERIFIER_REWARD_PATHS)}"
    )
    return SimpleNamespace(
        stdout=getattr(result, "stdout", "") or "",
        stderr=f"{stderr}\n{message}".strip(),
        return_code=1,
    )


def _e2b_verifier_stream_disconnect_result(
    disconnect_error: BaseException,
    terminal_state: str,
    *,
    return_code: int,
) -> Any:
    return SimpleNamespace(
        stdout="",
        stderr=(
            "E2B command stream disconnected after verifier dispatch: "
            f"{disconnect_error}\n{terminal_state}"
        ),
        return_code=return_code,
    )


async def _e2b_any_file_exists(environment: Any, paths: tuple[str, ...]) -> bool:
    for path in paths:
        if await _e2b_file_exists(environment, path):
            return True
    return False


async def _e2b_file_exists(environment: Any, path: str) -> bool:
    try:
        return bool(await environment.is_file(path, user="root"))
    except TypeError:
        return bool(await environment.is_file(path))
    except Exception:
        return False


def _e2b_verifier_terminal_wait_seconds() -> float:
    raw = os.environ.get(E2B_VERIFIER_TERMINAL_WAIT_ENV)
    if raw is None or raw.strip() == "":
        return E2B_VERIFIER_TERMINAL_WAIT_DEFAULT
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(
            f"{E2B_VERIFIER_TERMINAL_WAIT_ENV} must be a non-negative number, got {raw!r}"
        ) from exc
    if value < 0:
        raise ValueError(
            f"{E2B_VERIFIER_TERMINAL_WAIT_ENV} must be a non-negative number, got {raw!r}"
        )
    return value


def _patch_e2b_template_build_timeout(e2b_cls: type[Any]) -> None:
    if e2b_cls.__module__ != "harbor.environments.e2b" or AsyncTemplate is None:
        return

    current = getattr(AsyncTemplate, "build")
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def build_with_request_timeout(*args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("request_timeout", _e2b_template_request_timeout())
        return await current(*args, **kwargs)

    setattr(build_with_request_timeout, _ORIGINAL_ATTR, current)
    setattr(AsyncTemplate, "build", staticmethod(build_with_request_timeout))


def _e2b_template_request_timeout() -> float:
    raw = os.environ.get(E2B_TEMPLATE_REQUEST_TIMEOUT_ENV)
    if raw is None or raw.strip() == "":
        return E2B_TEMPLATE_REQUEST_TIMEOUT_DEFAULT
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(
            f"{E2B_TEMPLATE_REQUEST_TIMEOUT_ENV} must be numeric, got {raw!r}"
        ) from exc
    if value <= 0:
        raise ValueError(f"{E2B_TEMPLATE_REQUEST_TIMEOUT_ENV} must be positive, got {raw!r}")
    return value


def _patch_e2b_shared_template_start(e2b_cls: type[Any]) -> None:
    current = getattr(e2b_cls, "start")
    if hasattr(current, _ORIGINAL_ATTR):
        return

    @wraps(current)
    async def start_with_shared_template(
        self: Any,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if not _STATE.e2b_share_template_by_hash:
            return await current(self, *args, **kwargs)

        force_build = _start_force_build(args, kwargs)
        await _ensure_e2b_template_ready(self, force_build=force_build)
        await _create_e2b_sandbox_with_template_rebuild(self)

        if not self._sandbox:
            raise RuntimeError("Sandbox not found but was just created. This should never happen.")

        await self.ensure_dirs(self._mount_targets(writable_only=True))
        await self._upload_environment_dir_after_start()
        return None

    setattr(start_with_shared_template, _ORIGINAL_ATTR, current)
    setattr(e2b_cls, "start", start_with_shared_template)


def _start_force_build(args: tuple[Any, ...], kwargs: dict[str, Any]) -> bool:
    if "force_build" in kwargs:
        return bool(kwargs["force_build"])
    if args:
        return bool(args[0])
    return False


async def _ensure_e2b_template_ready(obj: Any, *, force_build: bool) -> None:
    template_name = str(getattr(obj, "_template_name", "e2b-template"))
    ready_path = _e2b_template_ready_path(template_name)
    if ready_path.is_file() and not force_build:
        return

    async with _AsyncFileLock(_e2b_template_lock_path(template_name)):
        if ready_path.is_file() and not force_build:
            return
        if (
            not force_build
            and hasattr(obj, "_does_template_exist")
            and await obj._does_template_exist()
        ):
            _mark_e2b_template_ready(ready_path)
            return
        logger = getattr(obj, "logger", None)
        if logger is not None:
            logger.debug(f"Creating template {template_name}")
        await obj._create_template()
        _mark_e2b_template_ready(ready_path)


async def _create_e2b_sandbox_with_template_rebuild(obj: Any) -> None:
    try:
        await obj._create_sandbox()
        return
    except Exception as exc:
        if not _is_e2b_missing_default_tag_error(exc):
            raise

    template_name = str(getattr(obj, "_template_name", "e2b-template"))
    ready_path = _e2b_template_ready_path(template_name)
    observed_ready_mtime = _mtime_ns(ready_path)
    async with _AsyncFileLock(_e2b_template_lock_path(template_name)):
        current_ready_mtime = _mtime_ns(ready_path)
        if current_ready_mtime is None or current_ready_mtime == observed_ready_mtime:
            logger = getattr(obj, "logger", None)
            if logger is not None:
                logger.warning(
                    "Rebuilding E2B template %s after missing default tag",
                    template_name,
                )
            await obj._create_template()
            _mark_e2b_template_ready(ready_path)
    await obj._create_sandbox()


def _is_e2b_missing_default_tag_error(exc: Exception) -> bool:
    message = str(exc)
    return "tag 'default' does not exist" in message and "template" in message


def _mtime_ns(path: Path) -> int | None:
    try:
        return path.stat().st_mtime_ns
    except FileNotFoundError:
        return None


def _mark_e2b_template_ready(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{os.getpid()}\n", encoding="utf-8")


class _AsyncFileLock:
    def __init__(self, path: Path):
        self.path = path
        self.file: Any | None = None

    async def __aenter__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.path.open("w", encoding="utf-8")
        await asyncio.to_thread(fcntl.flock, self.file, fcntl.LOCK_EX)

    async def __aexit__(self, *_args: Any) -> None:
        if self.file is None:
            return
        try:
            await asyncio.to_thread(fcntl.flock, self.file, fcntl.LOCK_UN)
        finally:
            self.file.close()
            self.file = None


def _e2b_template_lock_path(template_name: str) -> Path:
    cache_root = _e2b_template_cache_root()
    digest = hashlib.sha256(template_name.encode("utf-8")).hexdigest()[:24]
    return cache_root / "template-locks" / f"{digest}.lock"


def _e2b_template_ready_path(template_name: str) -> Path:
    cache_root = _e2b_template_cache_root()
    digest = hashlib.sha256(template_name.encode("utf-8")).hexdigest()[:24]
    return cache_root / "template-ready" / f"{digest}.ready"


def _e2b_template_cache_root() -> Path:
    cache_root = Path(os.environ.get(E2B_TEMPLATE_CACHE_ENV) or "/tmp/harbor-e2b-template-cache")
    return cache_root


def _tail(value: str, lines: int) -> str:
    return "\n".join(value.splitlines()[-lines:])


def _set_e2b_shared_template_name(obj: Any) -> None:
    task_env_config = getattr(obj, "task_env_config", None)
    docker_image = getattr(task_env_config, "docker_image", None)
    env_hash = environment_content_hash(
        Path(getattr(obj, "environment_dir")),
        docker_image=docker_image,
    )
    setattr(obj, "_template_name", f"relay-harbor__{env_hash}".replace(".", "-"))


def _verifier_disabled(obj: Any) -> bool:
    config = getattr(obj, "config", None)
    verifier = getattr(config, "verifier", None)
    return bool(getattr(verifier, "disable", False))


async def _refresh_e2b_convention_artifacts_after_verifier(obj: Any) -> None:
    environment = getattr(obj, "agent_environment", None)
    if not _is_e2b_environment(environment):
        return
    if getattr(obj, "_is_agent_environment_stopped", False):
        return

    env_paths = getattr(obj, "agent_env_paths", None)
    source_dir = str(getattr(env_paths, "artifacts_dir", "/logs/artifacts"))
    target_dir = getattr(obj, "_main_artifacts_mount_dir", None)
    if target_dir is None:
        paths = getattr(obj, "paths", None)
        artifacts_dir = getattr(paths, "artifacts_dir", None)
        if artifacts_dir is None:
            return
        target_dir = Path(artifacts_dir) / "logs" / "artifacts"

    try:
        if hasattr(environment, "is_dir") and not await environment.is_dir(
            source_dir,
            user="root",
        ):
            return
        await environment.download_dir(source_dir, Path(target_dir))
    except Exception:
        logger = getattr(obj, "logger", None)
        if logger is not None:
            logger.warning(
                "Failed to refresh E2B convention artifacts after verifier",
                exc_info=True,
            )


def _is_e2b_environment(environment: Any) -> bool:
    if environment is None:
        return False
    env_type = getattr(environment, "type", None)
    if not callable(env_type):
        return False
    try:
        value = env_type()
        return str(getattr(value, "value", value)).lower() == "e2b"
    except Exception:
        return False


def _restore_classes(
    *,
    trial_cls: type[Any],
    single_step_cls: type[Any],
    multi_step_cls: type[Any] | None = None,
    e2b_cls: type[Any] | None = None,
    verifier_cls: type[Any] | None = None,
) -> None:
    _restore_method(trial_cls, "_run_agent_phase")
    _restore_method(trial_cls, "_log_context")
    _restore_method(single_step_cls, "_run_verifier")
    if multi_step_cls is not None and hasattr(multi_step_cls, "_run_step_verifier"):
        _restore_method(multi_step_cls, "_run_step_verifier")
    if e2b_cls is not None:
        _restore_method(e2b_cls, "__init__")
        _restore_method(e2b_cls, "start")
        _restore_method(e2b_cls, "exec")
        _restore_method(e2b_cls, "_dispatch_command")
        _restore_method(e2b_cls, "upload_file")
        _restore_method(e2b_cls, "upload_dir")
        _restore_method(e2b_cls, "download_file")
        _restore_method(e2b_cls, "download_dir")
        _restore_method(e2b_cls, "is_file")
        _restore_method(e2b_cls, "is_dir")
        _restore_e2b_template_build_timeout()
    if verifier_cls is not None:
        _restore_method(verifier_cls, "verify")
    _STATE.configure(
        agent_limit=None,
        verifier_limit=None,
        e2b_use_dockerfile=False,
        e2b_stream_output=False,
        e2b_share_template_by_hash=False,
    )


def _restore_method(cls: type[Any], method_name: str) -> None:
    if not hasattr(cls, method_name):
        return
    current = getattr(cls, method_name)
    original: Callable[..., Any] | None = getattr(current, _ORIGINAL_ATTR, None)
    if original is not None:
        setattr(cls, method_name, original)


def _restore_e2b_template_build_timeout() -> None:
    if AsyncTemplate is None:
        return
    _restore_method(AsyncTemplate, "build")
