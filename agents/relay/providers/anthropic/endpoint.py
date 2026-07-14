import asyncio
import hashlib
import json
import os
from collections.abc import Awaitable, Callable, Mapping
from pathlib import PurePosixPath
from typing import Any, ClassVar

from relay.core import (
    DeliveryMethod,
    EndpointResult,
    ProducedFile,
    RelayError,
    RelayObserver,
    RemoteArtifact,
    emit_event,
    files_from_output_message,
    log_fields,
)
from relay.lifecycle import (
    EndpointRun,
    attach_endpoint_run_error,
    cancel_endpoint_run,
    close_endpoint_run,
    register_endpoint_run,
)
from relay.providers.anthropic.events import (
    anthropic_cost_usd,
    anthropic_event_meat,
    anthropic_event_semantic_type,
    anthropic_output_text,
    anthropic_session_terminal_error,
    anthropic_usage,
    dump_anthropic_model,
    emit_anthropic_tool_calls,
    is_anthropic_session_terminal,
    is_retryable_anthropic_stream_error,
    latest_anthropic_idle_stop_reason,
    list_anthropic_events,
    merge_anthropic_events,
)
from relay.providers.anthropic.files import collect_anthropic_output_files
from relay.providers.request import validate_request_mapping

try:
    from anthropic import AsyncAnthropic
except ImportError:  # pragma: no cover - exercised only without optional deps
    AsyncAnthropic = None  # type: ignore[assignment]


MANAGED_AGENTS_BETA = "managed-agents-2026-04-01"
ANTHROPIC_MODEL_SPEEDS = frozenset(("standard", "fast"))
ANTHROPIC_SANDBOX_OUTPUT_ROOT = PurePosixPath("/mnt/session/outputs")
ANTHROPIC_HTTP_TIMEOUT_SEC = 120.0
ANTHROPIC_SANDBOX_DETAILS = (
    "Your managed-agent sandbox exposes `/mnt/session/outputs` as the output "
    "root. Create final files under that directory, for example "
    "`/mnt/session/outputs/results_<task>.jsonl`. You may keep scratch copies "
    "elsewhere, read files back, or validate them locally. Only final files "
    "present under `/mnt/session/outputs` are collected."
)
ANTHROPIC_OUTPUT_DETAILS = (
    "You may use the managed-agent sandbox during the run and may prepare or "
    "validate files under `/mnt/session/outputs` or scratch paths. In this "
    "delivery mode, sandbox files are not collected directly; final files are "
    "submitted only through `file:<relative-path>` fenced blocks in the final "
    "response. If you prepare a file in the sandbox, read it back before "
    "finishing and emit the exact file contents in the fenced block, without "
    "summaries, previews, JSON escaping, or omitted rows."
)
ANTHROPIC_REQUEST_RETRY_ATTEMPTS = 12
ANTHROPIC_REQUEST_RETRY_INITIAL_DELAY_SEC = 1.0
ANTHROPIC_REQUEST_RETRY_MAX_DELAY_SEC = 30.0


class AnthropicManagedEndpoint:
    """Anthropic Managed Agents endpoint with sandbox file transport."""

    _resource_cache: ClassVar[dict[str, tuple[str, str]]] = {}
    _resource_lock: ClassVar[asyncio.Lock | None] = None

    def __init__(
        self,
        *,
        model_name: str | None = None,
        api_key: str | None = None,
        env: Mapping[str, str] | None = None,
        request: Mapping[str, Any] | None = None,
        delivery_channel: str = "sandbox",
        output_root: str = ANTHROPIC_SANDBOX_OUTPUT_ROOT.as_posix(),
        reconnect_delay_sec: float = 5.0,
        suite_tag: str = "relay",
        **_: Any,
    ):
        if delivery_channel not in {"sandbox", "output"}:
            raise RelayError(
                "Anthropic Managed Agents currently supports sandbox or output delivery."
        )
        self.delivery_channel = delivery_channel
        self.model_name = model_name or "claude-opus-4-7"
        self.model_speed = _model_speed(request)
        self.api_key = api_key or _first_env(env, ("ANTHROPIC_API_KEY",))
        self.output_root = PurePosixPath(output_root)
        self.reconnect_delay_sec = reconnect_delay_sec
        self.suite_tag = suite_tag
        self.tools = [
            {
                "type": "agent_toolset_20260401",
                "default_config": {
                    "enabled": True,
                    "permission_policy": {"type": "always_allow"},
                },
            },
        ]
        self.environment_config = {
            "type": "cloud",
            "networking": {"type": "unrestricted"},
        }

    @property
    def delivery_method(self) -> DeliveryMethod:
        if self.delivery_channel == "output":
            return DeliveryMethod(
                name="output",
                output_root=None,
                details=ANTHROPIC_OUTPUT_DETAILS,
            )
        return DeliveryMethod(
            name="sandbox",
            output_root=self.output_root,
            details=ANTHROPIC_SANDBOX_DETAILS,
        )

    async def run(
        self,
        prompt: str,
        observer: RelayObserver | None = None,
    ) -> EndpointResult:
        if AsyncAnthropic is None:
            raise RelayError(
                "anthropic is not installed. Install `relay[remote]`."
            )

        client_kwargs: dict[str, Any] = {"timeout": ANTHROPIC_HTTP_TIMEOUT_SEC}
        if self.api_key:
            client_kwargs["api_key"] = self.api_key
        client = AsyncAnthropic(**client_kwargs)
        try:
            agent_id, environment_id = await self._ensure_resources(client)
            return await self._run_session_once(
                client, agent_id, environment_id, prompt, observer
            )
        finally:
            await client.close()

    async def _run_session_once(
        self,
        client: Any,
        agent_id: str,
        environment_id: str,
        prompt: str,
        observer: RelayObserver | None,
    ) -> EndpointResult:
        active_run: EndpointRun | None = None
        try:
            session = await self._create_session(client, agent_id, environment_id)
            active_run = register_endpoint_run(
                provider="anthropic-managed",
                run_id=session["id"],
                cancel=lambda: self._delete_session_by_id(session["id"]),
                observer=observer,
            )
            emit_event(
                observer,
                "endpoint.submitted",
                "Created Anthropic managed-agent session.",
                endpoint="anthropic-managed",
                session_id=session["id"],
                response_id=session["id"],
                agent_id=agent_id,
                environment_id=environment_id,
                model=self.model_name,
                model_speed=self.model_speed,
                **log_fields(
                    session_id=session["id"],
                    response_id=session["id"],
                    model=self.model_name,
                ),
            )
            await self._request_with_retries(
                lambda: client.beta.sessions.events.send(
                    session["id"],
                    events=[
                        {
                            "type": "user.message",
                            "content": [{"type": "text", "text": prompt}],
                        }
                    ],
                    betas=[MANAGED_AGENTS_BETA],
                ),
                observer=observer,
                session_id=session["id"],
                operation="send_prompt",
            )

            final_session, events = await self._poll_until_terminal(
                client,
                session["id"],
                observer,
            )
            output_text = anthropic_output_text(events)
            files, artifacts = await self._collect_delivery(
                client,
                session["id"],
                events,
                output_text,
                observer,
            )
            _raise_if_terminal_without_delivery(session["id"], events, files)
            _emit_terminal_delivery_available(session["id"], events, files, observer)
            usage = anthropic_usage(final_session, events)
            cost_usd = anthropic_cost_usd(self.model_name, usage)
            emit_event(
                observer,
                "endpoint.usage",
                "Anthropic usage available.",
                session_id=session["id"],
                response_id=session["id"],
                cost_usd=cost_usd,
                **log_fields(session_id=session["id"], response_id=session["id"]),
                **usage,
            )
            return EndpointResult(
                text=output_text,
                files=tuple(files),
                artifacts=tuple(artifacts),
                raw={"session": final_session, "events": events},
                usage=usage,
                cost_usd=cost_usd,
                response_id=session["id"],
            )
        except BaseException as exc:
            attach_endpoint_run_error(exc, active_run)
            await cancel_endpoint_run(active_run, reason=type(exc).__name__)
            active_run = None
            raise
        finally:
            close_endpoint_run(active_run)

    async def _collect_delivery(
        self,
        client: Any,
        session_id: str,
        events: list[dict[str, Any]],
        output_text: str,
        observer: RelayObserver | None,
    ) -> tuple[list[ProducedFile], list[RemoteArtifact]]:
        if self.delivery_channel == "output":
            return list(files_from_output_message(output_text)), []
        return await collect_anthropic_output_files(
            client,
            output_root=self.output_root,
            session_id=session_id,
            beta=MANAGED_AGENTS_BETA,
            observer=observer,
        )

    @classmethod
    def _lock(cls) -> asyncio.Lock:
        if cls._resource_lock is None:
            cls._resource_lock = asyncio.Lock()
        return cls._resource_lock

    def _cache_key(self) -> str:
        payload = json.dumps(
            {
                "model": self._model_config(),
                "tools": self.tools,
                "environment_config": self.environment_config,
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def _resource_name(self) -> str:
        return f"{self.suite_tag}-{self.model_name}-{self.model_speed}"[:256]

    def _model_config(self) -> dict[str, str]:
        return {"id": self.model_name, "speed": self.model_speed}

    async def _ensure_resources(self, client: Any) -> tuple[str, str]:
        key = self._cache_key()
        if key in self._resource_cache:
            return self._resource_cache[key]

        async with self._lock():
            if key in self._resource_cache:
                return self._resource_cache[key]

            environment = dump_anthropic_model(
                await self._request_with_retries(
                    lambda: client.beta.environments.create(
                        name=self._resource_name(),
                        metadata={"created_by": "relay", "suite": self.suite_tag},
                        config=self.environment_config,
                        betas=[MANAGED_AGENTS_BETA],
                    ),
                    observer=None,
                    session_id=None,
                    operation="create_environment",
                )
            )
            agent = dump_anthropic_model(
                await self._request_with_retries(
                    lambda: client.beta.agents.create(
                        name=self._resource_name(),
                        model=self._model_config(),
                        metadata={"created_by": "relay", "suite": self.suite_tag},
                        tools=self.tools,
                        betas=[MANAGED_AGENTS_BETA],
                    ),
                    observer=None,
                    session_id=None,
                    operation="create_agent",
                )
            )
            agent_id = str(agent.get("id") or "")
            environment_id = str(environment.get("id") or "")
            if not agent_id or not environment_id:
                raise RelayError("Anthropic resource creation returned empty IDs.")

            self._resource_cache[key] = (agent_id, environment_id)
            return agent_id, environment_id

    async def _create_session(
        self,
        client: Any,
        agent_id: str,
        environment_id: str,
    ) -> dict[str, Any]:
        session = dump_anthropic_model(
            await self._request_with_retries(
                lambda: client.beta.sessions.create(
                    agent=agent_id,
                    environment_id=environment_id,
                    title=self.suite_tag[:256],
                    metadata={"suite": self.suite_tag},
                    betas=[MANAGED_AGENTS_BETA],
                ),
                observer=None,
                session_id=None,
                operation="create_session",
            )
        )
        if not session.get("id"):
            raise RelayError("Anthropic session creation returned empty ID.")
        return session

    async def _poll_until_terminal(
        self,
        client: Any,
        session_id: str,
        observer: RelayObserver | None = None,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        events: list[dict[str, Any]] = []
        observed_tool_call_ids: set[str] = set()
        observed_message_ids: set[str] = set()

        await self._reconcile_events(
            client,
            session_id,
            observer,
            events,
            observed_tool_call_ids,
            observed_message_ids,
        )
        while not is_anthropic_session_terminal(session_id, events):
            stream = None
            try:
                stream = await client.beta.sessions.events.stream(
                    session_id,
                    betas=[MANAGED_AGENTS_BETA],
                )
                async for event in stream:
                    merge_anthropic_events(events, [dump_anthropic_model(event)])
                    self._emit_session_events(
                        observer,
                        session_id,
                        events,
                        observed_tool_call_ids,
                        observed_message_ids,
                    )
                    if is_anthropic_session_terminal(session_id, events):
                        break
            except Exception as exc:
                if not is_retryable_anthropic_stream_error(exc):
                    raise
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Anthropic managed-agent stream disconnected.",
                    endpoint="anthropic-managed",
                    session_id=session_id,
                    error_type=type(exc).__name__,
                    **log_fields(session_id=session_id, status="stream_error"),
                )
            finally:
                if stream is not None:
                    try:
                        await stream.close()
                    except Exception:
                        pass

            if is_anthropic_session_terminal(session_id, events):
                break

            await asyncio.sleep(self.reconnect_delay_sec)
            await self._reconcile_events(
                client,
                session_id,
                observer,
                events,
                observed_tool_call_ids,
                observed_message_ids,
            )

        await self._reconcile_events(
            client,
            session_id,
            observer,
            events,
            observed_tool_call_ids,
            observed_message_ids,
        )
        session = dump_anthropic_model(
            await self._request_with_retries(
                lambda: client.beta.sessions.retrieve(
                    session_id,
                    betas=[MANAGED_AGENTS_BETA],
                ),
                observer=observer,
                session_id=session_id,
                operation="retrieve_session",
            )
        )
        terminal_error = anthropic_session_terminal_error(session_id, events)
        completion_reason = (
            "session_completed" if terminal_error is None else "session_terminal_error"
        )
        emit_event(
            observer,
            "endpoint.poll",
            "Anthropic managed-agent run reached terminal state.",
            endpoint="anthropic-managed",
            session_id=session_id,
            event_count=len(events),
            completion_reason=completion_reason,
            terminal_error_type=(
                type(terminal_error).__name__ if terminal_error is not None else None
            ),
            stop_reason=latest_anthropic_idle_stop_reason(events),
            status=session.get("status"),
            **log_fields(
                session_id=session_id,
                status=session.get("status"),
                completion_reason=completion_reason,
            ),
        )
        return session, events

    async def _reconcile_events(
        self,
        client: Any,
        session_id: str,
        observer: RelayObserver | None,
        events: list[dict[str, Any]],
        observed_tool_call_ids: set[str],
        observed_message_ids: set[str],
    ) -> None:
        listed_events = await self._request_with_retries(
            lambda: list_anthropic_events(
                client,
                session_id,
                beta=MANAGED_AGENTS_BETA,
            ),
            observer=observer,
            session_id=session_id,
            operation="list_events",
        )
        merge_anthropic_events(events, listed_events)
        self._emit_session_events(
            observer,
            session_id,
            events,
            observed_tool_call_ids,
            observed_message_ids,
        )
        emit_event(
            observer,
            "endpoint.poll",
            "Reconciled Anthropic session events.",
            endpoint="anthropic-managed",
            session_id=session_id,
            event_count=len(events),
            stop_reason=latest_anthropic_idle_stop_reason(events),
            **log_fields(session_id=session_id, event_count=len(events)),
        )

    def _emit_session_events(
        self,
        observer: RelayObserver | None,
        session_id: str,
        events: list[dict[str, Any]],
        observed_tool_call_ids: set[str],
        observed_message_ids: set[str],
    ) -> None:
        for event_data in events:
            emit_anthropic_tool_calls(
                observer,
                session_id,
                event_data,
                observed_tool_call_ids,
            )
            event_id = str(event_data.get("id") or "")
            if event_id in observed_message_ids:
                continue
            meat = anthropic_event_meat(event_data)
            if not meat:
                continue
            observed_message_ids.add(event_id)
            emit_event(
                observer,
                "endpoint.message",
                "Received Anthropic session message.",
                semantic_type=anthropic_event_semantic_type(event_data),
                endpoint="anthropic-managed",
                session_id=session_id,
                event_id=event_data.get("id"),
                event_type=event_data.get("type"),
                event_count=len(events),
                stop_reason=latest_anthropic_idle_stop_reason(events),
                **meat,
            )

    async def _request_with_retries(
        self,
        operation_call: Callable[[], Awaitable[Any]],
        *,
        observer: RelayObserver | None,
        session_id: str | None,
        operation: str,
    ) -> Any:
        delay = ANTHROPIC_REQUEST_RETRY_INITIAL_DELAY_SEC
        for attempt in range(ANTHROPIC_REQUEST_RETRY_ATTEMPTS):
            try:
                return await operation_call()
            except Exception as exc:
                if (
                    attempt + 1 == ANTHROPIC_REQUEST_RETRY_ATTEMPTS
                    or not is_retryable_anthropic_stream_error(exc)
                ):
                    raise
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Retrying Anthropic managed-agent request.",
                    endpoint="anthropic-managed",
                    session_id=session_id,
                    operation=operation,
                    attempt=attempt + 1,
                    error_type=type(exc).__name__,
                    **log_fields(session_id=session_id),
                )
                await asyncio.sleep(delay)
                delay = min(delay * 2, ANTHROPIC_REQUEST_RETRY_MAX_DELAY_SEC)
        raise RuntimeError("Anthropic retry loop exhausted without result.")

    async def _delete_session(self, client: Any, session_id: str) -> None:
        await self._request_with_retries(
            lambda: client.beta.sessions.delete(
                session_id,
                betas=[MANAGED_AGENTS_BETA],
            ),
            observer=None,
            session_id=session_id,
            operation="delete_session",
        )

    async def _delete_session_by_id(self, session_id: str) -> None:
        if AsyncAnthropic is None:
            return
        client_kwargs: dict[str, Any] = {"timeout": ANTHROPIC_HTTP_TIMEOUT_SEC}
        if self.api_key:
            client_kwargs["api_key"] = self.api_key
        client = AsyncAnthropic(**client_kwargs)
        try:
            await self._delete_session(client, session_id)
        finally:
            await client.close()


def _raise_if_terminal_without_delivery(
    session_id: str,
    events: list[dict[str, Any]],
    files: list[ProducedFile],
) -> None:
    terminal_error = anthropic_session_terminal_error(session_id, events)
    if terminal_error is not None and not files:
        raise terminal_error


def _emit_terminal_delivery_available(
    session_id: str,
    events: list[dict[str, Any]],
    files: list[ProducedFile],
    observer: RelayObserver | None,
) -> None:
    if anthropic_session_terminal_error(session_id, events) is None or not files:
        return
    emit_event(
        observer,
        "endpoint.poll",
        "Anthropic terminal session was not completed, but delivery files are available.",
        endpoint="anthropic-managed",
        session_id=session_id,
        response_id=session_id,
        status="terminal_delivery_available",
        paths=[file.path.as_posix() for file in files],
        bytes=sum(len(file.content) for file in files),
        **log_fields(
            session_id=session_id,
            response_id=session_id,
            status="terminal_delivery_available",
        ),
    )


def _first_env(env: Mapping[str, str] | None, names: tuple[str, ...]) -> str | None:
    for source in (env or {}, os.environ):
        for name in names:
            value = source.get(name)
            if value:
                return value
    return None


def _model_speed(request: Mapping[str, Any] | None) -> str:
    if request is not None and "reasoning_effort" in request:
        raise RelayError(
            "Anthropic Managed Agents does not expose `reasoning_effort`; "
            "use request.speed with one of ['standard', 'fast']."
        )
    data = validate_request_mapping(
        request,
        provider="Anthropic",
        allowed={"speed"},
    )
    speed = str(data.get("speed", "standard"))
    if speed not in ANTHROPIC_MODEL_SPEEDS:
        raise RelayError(
            f"Unsupported Anthropic model speed {speed!r}; "
            f"expected one of {sorted(ANTHROPIC_MODEL_SPEEDS)}."
        )
    return speed
