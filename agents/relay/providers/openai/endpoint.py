import asyncio
import json
import os
import time
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any, Self

from relay.core import (
    DeliveryMethod,
    EndpointResult,
    OUTPUT_ROOT,
    ProducedFile,
    RelayError,
    RelayObserver,
    RemoteArtifact,
    RemoteToolOutput,
    TOOL_ARGUMENTS,
    TOOL_RESULT,
    emit_event,
    files_from_final_message,
    files_from_stdout_sequence,
    log_fields,
    stop_observation_task,
)
from relay.lifecycle import (
    EndpointRun,
    attach_endpoint_run_error,
    cancel_endpoint_run,
    close_endpoint_run,
    register_endpoint_run,
)
from relay.providers.openai.events import (
    dump_openai_model,
    emit_openai_output_messages,
    emit_openai_stream_message,
    emit_openai_stream_tool_call,
    emit_openai_tool_calls,
    openai_field,
    openai_stream_response_id,
    openai_stream_response_status,
    openai_stream_sequence_number,
    openai_cost_usd,
    openai_usage,
    response_text_from_openai_output,
)
from relay.providers.openai.files import (
    collect_openai_container_output_files,
    collect_openai_shell_outputs,
)
from relay.providers.request import validate_request_mapping

try:
    from openai import AsyncOpenAI
except ImportError:  # pragma: no cover - exercised only without optional deps
    AsyncOpenAI = None  # type: ignore[assignment]


OAI_TERMINAL_EVENT_TYPES = frozenset(
    {"response.completed", "response.failed", "response.incomplete"}
)
OAI_STREAM_RECONNECT_ATTEMPTS = 12
OAI_STREAM_RECONNECT_INITIAL_BACKOFF_SEC = 2.0
OAI_STREAM_RECONNECT_MAX_BACKOFF_SEC = 60.0
OAI_REQUEST_RETRY_ATTEMPTS = 12
OAI_REQUEST_RETRY_INITIAL_BACKOFF_SEC = 1.0
OAI_REQUEST_RETRY_MAX_BACKOFF_SEC = 60.0
OAI_HTTP_TIMEOUT_SEC = 120.0
OAI_REQUEST_TIMEOUT_SEC = 180.0
OAI_STREAM_BOOTSTRAP_TIMEOUT_SEC = 180.0
OAI_POLL_HEARTBEAT_SEC = 60.0
OPENAI_SANDBOX_OUTPUT_ROOT = PurePosixPath("/mnt/data/relay-out")
OPENAI_SANDBOX_DETAILS = (
    "Use the python tool for final file writes. Scratch work may live elsewhere "
    "in the container. In the final response, refer to each written file path so "
    "the API registers the generated container file; do not paste file contents. "
    "Content-policy filters may reject corpus-heavy tool inputs, especially the "
    "larger ones. For large artifacts, it can be safer to accrete output in "
    "flushed batches, including directly to the required final file if that "
    "matches your submission strategy. Do not let delivery mechanics lower "
    "result quality; delivery should adapt to the artifact you intend to submit, "
    "not the other way around. "
    "The OpenAI sandbox will die after about 1 hour; you can set one small "
    "timer; start wrapping up the work at the 50 minute mark."
)
OPENAI_STDOUT_DETAILS = "Use the shell tool for final file emission."
OPENAI_OUTPUT_DETAILS = (
    "You can and are encouraged to use the sandbox tooling (e.g. the python tool) "
    "during the run. However, filesystem states / tool output blocks aren't "
    "externally observable, so output delivery must still be performed via "
    "output-token emission on your side. "
    "**Delivery shouldn't affect the workflow / behavior**: work as you normally "
    "would, regardless of delivery particularities, arriving at an in-sandbox "
    "final file. "
    "**Delivery should adapt to the artifact, not the other way around**: load "
    "the file in your context right before completion by whichever tool / method "
    "you prefer, and then emit its contents as a fenced block --- verbatim, in "
    "full, without omissions, line-by-line. Do not construct fenced blocks "
    "on-the-fly without the reference. Do not omit information relative to the "
    "exact in-sandbox reference: do not reduce row count, detail coverage, "
    "schema richness, excerpt/answer-field fidelity, etc. to make emission "
    "easier. Both vertical recall and horizontal row fidelity matter."
)


@dataclass(frozen=True)
class OpenAIRequest:
    reasoning_effort: str = "high"
    reasoning_summary: str | None = "auto"
    search_context_size: str = "high"
    max_tool_calls: int | None = None
    max_output_tokens: int | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> Self:
        data = validate_request_mapping(
            value,
            provider="OpenAI",
            allowed={
                "reasoning_effort",
                "reasoning_summary",
                "search_context_size",
                "max_tool_calls",
                "max_output_tokens",
            },
        )
        return cls(
            reasoning_effort=str(data.get("reasoning_effort", "high")),
            reasoning_summary=data.get("reasoning_summary", "auto"),
            search_context_size=str(data.get("search_context_size", "high")),
            max_tool_calls=_optional_int(data.get("max_tool_calls")),
            max_output_tokens=_optional_int(data.get("max_output_tokens")),
        )


@dataclass
class OpenAIStreamState:
    response_id: str | None = None
    last_sequence_number: int = 0
    submitted: bool = False
    terminal_seen: bool = False
    message_buffers: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    observed_message_keys: set[tuple[str, str]] = field(default_factory=set)


class OpenAIResponsesEndpoint:
    """OpenAI Responses endpoint with sandbox, stdout, or final-output transport."""

    def __init__(
        self,
        *,
        model_name: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        env: Mapping[str, str] | None = None,
        request: Mapping[str, Any] | None = None,
        poll_interval_sec: float = 2.0,
        stream_bootstrap_timeout_sec: float = OAI_STREAM_BOOTSTRAP_TIMEOUT_SEC,
        stream_observation: bool = False,
        delivery_channel: str = "sandbox",
        output_root: str | None = None,
        **_: Any,
    ):
        self.model_name = model_name or "gpt-5.5"
        self.api_key = api_key or _first_env(env, ("OPENAI_API_KEY",))
        self.base_url = base_url or _first_env(env, ("OPENAI_BASE_URL",))
        self.request = OpenAIRequest.from_mapping(request)
        self.poll_interval_sec = poll_interval_sec
        self.stream_bootstrap_timeout_sec = stream_bootstrap_timeout_sec
        self.stream_observation = stream_observation
        self.delivery_channel = _normalize_delivery_channel(delivery_channel)
        default_output_root = (
            OPENAI_SANDBOX_OUTPUT_ROOT
            if self.delivery_channel == "sandbox"
            else OUTPUT_ROOT
        )
        self.output_root = PurePosixPath(output_root or default_output_root.as_posix())

    @property
    def delivery_method(self) -> DeliveryMethod:
        if self.delivery_channel == "sandbox":
            return DeliveryMethod(
                name="sandbox",
                output_root=self.output_root,
                details=OPENAI_SANDBOX_DETAILS,
            )
        if self.delivery_channel == "stdout":
            return DeliveryMethod(
                name="stdout",
                output_root=self.output_root,
                details=OPENAI_STDOUT_DETAILS,
            )
        return DeliveryMethod(
            name="output",
            output_root=None,
            details=OPENAI_OUTPUT_DETAILS,
        )

    async def run(
        self,
        prompt: str,
        observer: RelayObserver | None = None,
    ) -> EndpointResult:
        if AsyncOpenAI is None:
            raise RelayError("openai is not installed. Install `relay[remote]`.")

        client = AsyncOpenAI(**self._client_kwargs())
        active_run: EndpointRun | None = None
        observation_task: asyncio.Task[None] | None = None

        def register_response(response_id: str) -> None:
            nonlocal active_run
            if active_run is None:
                active_run = register_endpoint_run(
                    provider="openai",
                    run_id=response_id,
                    cancel=lambda: self._cancel_response_by_id(response_id),
                    observer=observer,
                )

        try:
            created = await _openai_request_with_retries(
                lambda: client.responses.create(**self._create_payload(prompt)),
                observer=observer,
                operation="create_response",
            )
            observed_tool_call_ids: set[str] = set()
            observed_message_keys: set[tuple[str, str]] = set()
            if hasattr(created, "__aiter__"):
                response_id, stream, stream_state = await self._bootstrap_stream(
                    created,
                    observed_tool_call_ids,
                    observer,
                    on_response_id=register_response,
                )
                observed_message_keys = stream_state.observed_message_keys
                observation_task = asyncio.create_task(
                    self._observe_stream(
                        client,
                        stream,
                        stream_state,
                        observed_tool_call_ids,
                        observer,
                    )
                )
                response = await self._poll_response_id_until_terminal(
                    client,
                    response_id,
                    observer,
                )
                await stop_observation_task(
                    observation_task,
                    observer=observer,
                    endpoint="openai",
                    response_id=response_id,
                )
                observation_task = None
            else:
                response = created
                register_response(openai_field(response, "id"))
                emit_event(
                    observer,
                    "endpoint.submitted",
                    "Submitted OpenAI Responses request.",
                    endpoint="openai",
                    response_id=openai_field(response, "id"),
                    status=openai_field(response, "status"),
                    model=self.model_name,
                    **log_fields(
                        response_id=openai_field(response, "id"),
                        status=openai_field(response, "status"),
                        model=self.model_name,
                    ),
                )
                response = await self._poll_until_terminal(client, response, observer)

            emit_openai_output_messages(response, observer, observed_message_keys)
            emit_openai_tool_calls(response, observer, observed_tool_call_ids)
            output_text = openai_field(response, "output_text") or (
                response_text_from_openai_output(openai_field(response, "output", []))
            )
            files, artifacts, tool_outputs = await self._collect_delivery(
                client,
                response,
                output_text,
                observer,
            )
            _raise_if_terminal_without_delivery(response, files)
            _emit_terminal_delivery_available(response, files, observer)

            for output in tool_outputs:
                emit_event(
                    observer,
                    "endpoint.tool_result",
                    "Collected OpenAI tool stdout.",
                    tool_name="shell",
                    tool_call_id=output.source,
                    source=output.source,
                    command_bytes=len(output.command.encode()),
                    stdout_bytes=len(output.stdout.encode()),
                    **{
                        TOOL_ARGUMENTS: {"command": output.command},
                        TOOL_RESULT: {
                            "source": output.source,
                            "command_bytes": len(output.command.encode()),
                            "stdout_bytes": len(output.stdout.encode()),
                        },
                    },
                )

            usage = openai_usage(response)
            cost_usd = openai_cost_usd(self.model_name, usage)
            emit_event(
                observer,
                "endpoint.usage",
                "OpenAI usage available.",
                response_id=openai_field(response, "id"),
                cost_usd=cost_usd,
                **log_fields(response_id=openai_field(response, "id")),
                **usage,
            )
            return EndpointResult(
                text=output_text,
                files=tuple(files),
                artifacts=tuple(artifacts),
                tool_outputs=tuple(tool_outputs),
                raw=dump_openai_model(response),
                usage=usage,
                cost_usd=cost_usd,
                response_id=openai_field(response, "id"),
            )
        except BaseException as exc:
            await stop_observation_task(
                observation_task,
                observer=observer,
                endpoint="openai",
                response_id=active_run.id if active_run is not None else None,
            )
            observation_task = None
            attach_endpoint_run_error(exc, active_run)
            await cancel_endpoint_run(active_run, reason=type(exc).__name__)
            active_run = None
            raise
        finally:
            await stop_observation_task(
                observation_task,
                observer=observer,
                endpoint="openai",
                response_id=active_run.id if active_run is not None else None,
            )
            close_endpoint_run(active_run)
            await client.close()

    def _client_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {"timeout": OAI_HTTP_TIMEOUT_SEC}
        if self.api_key:
            kwargs["api_key"] = self.api_key
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return kwargs

    def _create_payload(self, prompt: str) -> dict[str, Any]:
        reasoning: dict[str, Any] = {"effort": self.request.reasoning_effort}
        if self.request.reasoning_summary is not None:
            reasoning["summary"] = self.request.reasoning_summary

        tools: list[dict[str, Any]] = [
            {
                "type": "web_search_preview",
                "search_context_size": self.request.search_context_size,
            },
        ]
        if self.delivery_channel in {"sandbox", "output"}:
            tools.append({"type": "code_interpreter", "container": {"type": "auto"}})
        if self.delivery_channel == "stdout":
            tools.append({"type": "shell", "environment": {"type": "container_auto"}})

        payload: dict[str, Any] = {
            "model": self.model_name,
            "input": [{"role": "user", "content": prompt}],
            "tools": tools,
            "reasoning": reasoning,
            "background": True,
            "stream": self.stream_observation,
            "store": True,
        }
        include = self._response_include()
        if include:
            payload["include"] = include
        if self.request.max_tool_calls is not None:
            payload["max_tool_calls"] = self.request.max_tool_calls
        if self.request.max_output_tokens is not None:
            payload["max_output_tokens"] = self.request.max_output_tokens
        return payload

    def _response_include(self) -> list[str]:
        if self.delivery_channel not in {"sandbox", "output"}:
            return []
        return ["code_interpreter_call.outputs"]

    async def _poll_until_terminal(
        self,
        client: Any,
        response: Any,
        observer: RelayObserver | None = None,
    ) -> Any:
        return await self._poll_response_id_until_terminal(
            client,
            str(openai_field(response, "id")),
            observer,
            initial_response=response,
        )

    async def _collect_delivery(
        self,
        client: Any,
        response: Any,
        output_text: str,
        observer: RelayObserver | None = None,
    ) -> tuple[list[ProducedFile], list[RemoteArtifact], list[RemoteToolOutput]]:
        artifacts = []
        tool_outputs: list[RemoteToolOutput] = []
        if self.delivery_channel == "sandbox":
            files, artifacts = await collect_openai_container_output_files(
                client,
                response,
                output_root=self.output_root,
                observer=observer,
            )
        elif self.delivery_channel == "stdout":
            tool_outputs = collect_openai_shell_outputs(response)
            files = list(
                files_from_stdout_sequence(
                    tool_outputs,
                    output_root=self.output_root,
                )
            )
        else:
            files = list(files_from_final_message(output_text))
        return files, artifacts, tool_outputs

    async def _bootstrap_stream(
        self,
        stream: Any,
        observed_tool_call_ids: set[str],
        observer: RelayObserver | None = None,
        *,
        on_response_id: Callable[[str], None] | None = None,
    ) -> tuple[str, Any, OpenAIStreamState]:
        state = OpenAIStreamState()
        stream_iter = stream.__aiter__()
        try:
            async with asyncio.timeout(self.stream_bootstrap_timeout_sec):
                while state.response_id is None:
                    event = await anext(stream_iter)
                    self._consume_stream_event(
                        event,
                        state,
                        observed_tool_call_ids,
                        observer,
                        on_response_id=on_response_id,
                    )
        except StopAsyncIteration as exc:
            raise RelayError(
                "OpenAI response stream ended before a response identifier."
            ) from exc
        except TimeoutError as exc:
            raise RelayError(
                "OpenAI response stream produced no response identifier within "
                f"{self.stream_bootstrap_timeout_sec:.0f}s."
            ) from exc
        return state.response_id, stream_iter, state

    async def _observe_stream(
        self,
        client: Any,
        stream: Any,
        state: OpenAIStreamState,
        observed_tool_call_ids: set[str],
        observer: RelayObserver | None = None,
    ) -> None:
        if state.terminal_seen:
            return

        reconnect_attempt = 0
        while True:
            try:
                await self._consume_stream_until_terminal(
                    stream,
                    state,
                    observed_tool_call_ids,
                    observer,
                )
                if state.terminal_seen:
                    return
                failure: BaseException = _OpenAIStreamEnded()
            except Exception as exc:
                failure = exc

            if reconnect_attempt >= OAI_STREAM_RECONNECT_ATTEMPTS:
                emit_event(
                    observer,
                    "endpoint.poll",
                    "OpenAI stream observation lost; polling remains authoritative.",
                    endpoint="openai",
                    response_id=state.response_id,
                    status="observation_lost",
                    error_type=type(failure).__name__,
                    last_sequence_number=state.last_sequence_number,
                    **log_fields(
                        response_id=state.response_id,
                        status="observation_lost",
                    ),
                )
                return

            backoff_sec = min(
                OAI_STREAM_RECONNECT_MAX_BACKOFF_SEC,
                OAI_STREAM_RECONNECT_INITIAL_BACKOFF_SEC * (2**reconnect_attempt),
            )
            reconnect_attempt += 1
            emit_event(
                observer,
                "endpoint.poll",
                "OpenAI stream interrupted; reconnecting.",
                endpoint="openai",
                response_id=state.response_id,
                status="reconnecting",
                error_type=type(failure).__name__,
                attempt=reconnect_attempt,
                backoff_sec=backoff_sec,
                last_sequence_number=state.last_sequence_number,
                **log_fields(
                    response_id=state.response_id,
                    status="reconnecting",
                ),
            )
            await asyncio.sleep(backoff_sec)
            try:
                stream = await self._retrieve_response_stream(
                    client,
                    str(state.response_id),
                    starting_after=state.last_sequence_number,
                )
            except Exception as exc:
                stream = _OpenAIStreamFailure(exc)

    async def _poll_response_id_until_terminal(
        self,
        client: Any,
        response_id: str,
        observer: RelayObserver | None = None,
        *,
        initial_response: Any = None,
    ) -> Any:
        response = initial_response
        last_status: str | None = None
        last_emit = 0.0
        while True:
            if response is None:
                response = await self._retrieve_response(
                    client,
                    response_id,
                    observer=observer,
                )
            status = str(openai_field(response, "status") or "")
            now = time.monotonic()
            if (
                status != last_status
                or status not in {"queued", "in_progress"}
                or now - last_emit >= OAI_POLL_HEARTBEAT_SEC
            ):
                _emit_openai_poll_event(observer, response)
                last_status = status
                last_emit = now
            if status not in {"queued", "in_progress"}:
                break
            await asyncio.sleep(self.poll_interval_sec)
            response = await self._retrieve_response(
                client,
                response_id,
                observer=observer,
            )

        return response

    async def _consume_stream_until_terminal(
        self,
        stream: Any,
        state: OpenAIStreamState,
        observed_tool_call_ids: set[str],
        observer: RelayObserver | None = None,
        *,
        on_response_id: Callable[[str], None] | None = None,
    ) -> Any | None:
        async for event in stream:
            response = self._consume_stream_event(
                event,
                state,
                observed_tool_call_ids,
                observer,
                on_response_id=on_response_id,
            )
            if response is not None:
                return response
        return None

    def _consume_stream_event(
        self,
        event: Any,
        state: OpenAIStreamState,
        observed_tool_call_ids: set[str],
        observer: RelayObserver | None = None,
        *,
        on_response_id: Callable[[str], None] | None = None,
    ) -> Any | None:
        event_data = dump_openai_model(event)
        sequence_number = openai_stream_sequence_number(event_data)
        if sequence_number is not None:
            state.last_sequence_number = max(
                state.last_sequence_number,
                sequence_number,
            )

        event_type = str(event_data.get("type") or "")
        response = event_data.get("response")
        response_id = openai_stream_response_id(event_data, response)
        if response_id is not None:
            state.response_id = response_id
            if on_response_id is not None:
                on_response_id(response_id)

        status = openai_stream_response_status(response)
        if state.response_id is not None and not state.submitted:
            state.submitted = True
            emit_event(
                observer,
                "endpoint.submitted",
                "Submitted OpenAI Responses request.",
                endpoint="openai",
                response_id=state.response_id,
                status=status,
                model=self.model_name,
                **log_fields(
                    response_id=state.response_id,
                    status=status,
                    model=self.model_name,
                ),
            )

        emit_openai_stream_tool_call(
            event_data,
            state.response_id or "",
            observed_tool_call_ids,
            observer,
        )

        message_key = emit_openai_stream_message(
            event_data,
            state.response_id or "",
            state.message_buffers,
            observer,
            sequence_number=sequence_number,
            status=status,
        )
        if message_key is not None:
            state.observed_message_keys.add(message_key)
        if event_type in OAI_TERMINAL_EVENT_TYPES:
            state.terminal_seen = True
            emit_event(
                observer,
                "endpoint.poll",
                "OpenAI Responses stream reached terminal event.",
                endpoint="openai",
                response_id=state.response_id,
                status=status,
                event_type=event_type,
                **_openai_terminal_metadata(response),
                **log_fields(response_id=state.response_id, status=status),
            )
            return response
        return None

    async def _cancel_response(self, client: Any, response_id: str) -> None:
        await _openai_request_with_retries(
            lambda: client.responses.cancel(response_id),
            operation="cancel_response",
            response_id=response_id,
        )

    async def _cancel_response_by_id(self, response_id: str) -> None:
        if AsyncOpenAI is None:
            return
        client = AsyncOpenAI(**self._client_kwargs())
        try:
            await self._cancel_response(client, response_id)
        finally:
            await client.close()

    async def _retrieve_response(
        self,
        client: Any,
        response_id: str,
        *,
        observer: RelayObserver | None = None,
    ) -> Any:
        retrieve_kwargs = {}
        include = self._response_include()
        if include:
            retrieve_kwargs["include"] = include
        return await _openai_request_with_retries(
            lambda: client.responses.retrieve(response_id, **retrieve_kwargs),
            observer=observer,
            operation="retrieve_response",
            response_id=response_id,
        )

    async def _retrieve_response_stream(
        self,
        client: Any,
        response_id: str,
        *,
        starting_after: int,
    ) -> Any:
        retrieve_kwargs: dict[str, Any] = {
            "stream": True,
            "starting_after": starting_after,
        }
        return await client.responses.retrieve(response_id, **retrieve_kwargs)


def _normalize_delivery_channel(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    aliases = {
        "artifact": "sandbox",
        "cat": "stdout",
        "catrelay": "stdout",
        "container": "sandbox",
        "native": "sandbox",
        "outrelay": "output",
        "output": "output",
        "sandbox": "sandbox",
        "stdout": "stdout",
    }
    if normalized not in aliases:
        raise RelayError(f"Unknown OpenAI delivery channel: {value}")
    return aliases[normalized]


async def _openai_request_with_retries(
    operation_call: Callable[[], Awaitable[Any]],
    *,
    observer: RelayObserver | None = None,
    operation: str,
    response_id: str | None = None,
) -> Any:
    delay = OAI_REQUEST_RETRY_INITIAL_BACKOFF_SEC
    for attempt in range(OAI_REQUEST_RETRY_ATTEMPTS):
        try:
            async with asyncio.timeout(OAI_REQUEST_TIMEOUT_SEC):
                return await operation_call()
        except Exception as exc:
            if (
                attempt + 1 == OAI_REQUEST_RETRY_ATTEMPTS
                or not _is_retryable_openai_error(exc)
            ):
                raise
            emit_event(
                observer,
                "endpoint.poll",
                "Retrying OpenAI Responses request.",
                endpoint="openai",
                response_id=response_id,
                operation=operation,
                attempt=attempt + 1,
                error_type=type(exc).__name__,
                backoff_sec=delay,
                **log_fields(response_id=response_id),
            )
            await asyncio.sleep(delay)
            delay = min(delay * 2, OAI_REQUEST_RETRY_MAX_BACKOFF_SEC)
    raise RuntimeError("OpenAI retry loop exhausted without result.")


def _is_retryable_openai_error(error: BaseException) -> bool:
    status_code = getattr(error, "status_code", None)
    if isinstance(status_code, int):
        return status_code in {408, 409, 429} or status_code >= 500
    return type(error).__name__ in {
        "APIConnectionError",
        "APIError",
        "APITimeoutError",
        "InternalServerError",
        "RateLimitError",
        "TimeoutError",
    }


def _first_env(env: Mapping[str, str] | None, names: tuple[str, ...]) -> str | None:
    for source in (env or {}, os.environ):
        for name in names:
            value = source.get(name)
            if value:
                return value
    return None


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


class _OpenAIStreamEnded(RuntimeError):
    pass


class _OpenAIStreamFailure:
    def __init__(self, exc: Exception):
        self.exc = exc

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> Any:
        raise self.exc


def _emit_openai_poll_event(observer: RelayObserver | None, response: Any) -> None:
    status = openai_field(response, "status")
    response_id = openai_field(response, "id")
    emit_event(
        observer,
        "endpoint.poll",
        "Polled OpenAI Responses request.",
        endpoint="openai",
        response_id=response_id,
        status=status,
        **_openai_terminal_metadata(response),
        **log_fields(response_id=response_id, status=status),
    )


def _openai_terminal_metadata(response: Any) -> dict[str, Any]:
    metadata = {}
    error = _openai_detail(openai_field(response, "error"))
    incomplete_details = _openai_detail(openai_field(response, "incomplete_details"))
    if error is not None:
        metadata["error"] = error
    if incomplete_details is not None:
        metadata["incomplete_details"] = incomplete_details
    return metadata


def _raise_if_terminal_without_delivery(
    response: Any,
    files: list[ProducedFile],
) -> None:
    terminal_error = _openai_terminal_error(response)
    if terminal_error is not None and not files:
        raise terminal_error


def _emit_terminal_delivery_available(
    response: Any,
    files: list[ProducedFile],
    observer: RelayObserver | None,
) -> None:
    if _openai_terminal_error(response) is None or not files:
        return
    emit_event(
        observer,
        "endpoint.poll",
        "OpenAI terminal response was not completed, but delivery files are available.",
        endpoint="openai",
        response_id=openai_field(response, "id"),
        status="terminal_delivery_available",
        original_status=openai_field(response, "status"),
        paths=[file.path.as_posix() for file in files],
        bytes=sum(len(file.content) for file in files),
        **log_fields(
            response_id=openai_field(response, "id"),
            status="terminal_delivery_available",
        ),
    )


def _openai_terminal_error(response: Any) -> RelayError | None:
    response_id = openai_field(response, "id")
    status = openai_field(response, "status")
    if status == "completed":
        return None
    details = _openai_terminal_metadata(response)
    if details:
        return RelayError(
            f"OpenAI response {response_id} ended with status {status}: "
            f"{json.dumps(details, sort_keys=True, default=str)}"
        )
    return RelayError(f"OpenAI response {response_id} ended with status {status}.")


def _openai_detail(value: Any) -> Any:
    if value is None:
        return None
    dumped = dump_openai_model(value)
    return dumped or value
