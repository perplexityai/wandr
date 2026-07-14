import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import Any, Self

from relay.core import (
    DeliveryMethod,
    EndpointResult,
    EVENT_TEXT,
    EVENT_TEXT_PREVIEW,
    RelayError,
    RelayObserver,
    emit_event,
    files_from_output_message,
    log_fields,
    stop_observation_task,
)
from relay.providers.output import (
    emit_terminal_delivery_available,
    output_delivery_details,
    raise_if_terminal_without_delivery,
)
from relay.providers.request import validate_request_mapping

try:
    import httpx
except ImportError:  # pragma: no cover - exercised only without optional deps
    httpx = None  # type: ignore[assignment]


PARALLEL_BASE_URL = "https://api.parallel.ai"
PARALLEL_RUNS_PATH = "/v1/tasks/runs"
PARALLEL_EVENTS_PATH_SUFFIX = "/events"
PARALLEL_OUTPUT_DETAILS = output_delivery_details(
    tool_phrase="Use the available research tools"
)
PARALLEL_HTTP_TIMEOUT_SEC = 360.0
PARALLEL_RESULT_BLOCK_TIMEOUT_SEC = 60
PARALLEL_REQUEST_RETRY_ATTEMPTS = 8
PARALLEL_REQUEST_RETRY_INITIAL_BACKOFF_SEC = 1.0
PARALLEL_REQUEST_RETRY_MAX_BACKOFF_SEC = 60.0
PARALLEL_STATUS_TERMINAL = frozenset({"completed", "failed", "cancelled", "timed_out"})
PARALLEL_TERMINAL_RESULT_MISS_LIMIT = 12
PARALLEL_PROCESSOR_COSTS = {
    "lite": 0.005,
    "base": 0.010,
    "core": 0.025,
    "core2x": 0.050,
    "pro": 0.100,
    "ultra": 0.300,
    "ultra2x": 0.600,
    "ultra4x": 1.200,
    "ultra8x": 2.400,
}


@dataclass(frozen=True)
class ParallelRequest:
    processor: str | None = None
    task_spec: Mapping[str, Any] | None = None
    enable_events: bool | None = None
    metadata: Mapping[str, str] | None = None
    source_policy: Mapping[str, Any] | None = None
    advanced_settings: Mapping[str, Any] | None = None
    previous_interaction_id: str | None = None
    mcp_servers: tuple[Mapping[str, Any], ...] = ()
    webhook: Mapping[str, Any] | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> Self:
        data = validate_request_mapping(
            value,
            provider="Parallel",
            allowed={
                "processor",
                "task_spec",
                "enable_events",
                "metadata",
                "source_policy",
                "advanced_settings",
                "previous_interaction_id",
                "mcp_servers",
                "webhook",
            },
        )
        mcp_servers = data.get("mcp_servers")
        return cls(
            processor=data.get("processor"),
            task_spec=data.get("task_spec"),
            enable_events=data.get("enable_events"),
            metadata=data.get("metadata"),
            source_policy=data.get("source_policy"),
            advanced_settings=data.get("advanced_settings"),
            previous_interaction_id=data.get("previous_interaction_id"),
            mcp_servers=tuple(mcp_servers) if isinstance(mcp_servers, list | tuple) else (),
            webhook=data.get("webhook"),
        )


class ParallelTaskEndpoint:
    """Parallel Task API endpoint with output transport."""

    def __init__(
        self,
        *,
        model_name: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        env: Mapping[str, str] | None = None,
        request: Mapping[str, Any] | None = None,
        delivery_channel: str = "output",
        result_block_timeout_sec: int = PARALLEL_RESULT_BLOCK_TIMEOUT_SEC,
        **_: Any,
    ):
        if delivery_channel != "output":
            raise RelayError("Parallel Task API currently supports output delivery.")
        self.model_name = model_name or "taskapi"
        self.api_key = api_key or _first_env(env, ("PARALLEL_API_KEY",))
        self.base_url = (base_url or PARALLEL_BASE_URL).rstrip("/")
        self.request = ParallelRequest.from_mapping(request)
        self.result_block_timeout_sec = result_block_timeout_sec

    @property
    def delivery_method(self) -> DeliveryMethod:
        return DeliveryMethod(
            name="output",
            output_root=None,
            details=PARALLEL_OUTPUT_DETAILS,
        )

    async def run(
        self,
        prompt: str,
        observer: RelayObserver | None = None,
    ) -> EndpointResult:
        if httpx is None:
            raise RelayError("httpx is not installed. Install `relay[remote]`.")

        async with httpx.AsyncClient(timeout=PARALLEL_HTTP_TIMEOUT_SEC) as client:
            created = await self._create_run(client, prompt)
            run_id = str(created.get("run_id") or created.get("interaction_id") or "")
            if not run_id:
                raise RelayError("Parallel task creation returned no run id.")
            emit_event(
                observer,
                "endpoint.submitted",
                "Submitted Parallel Task API run.",
                endpoint="parallel",
                response_id=run_id,
                status=created.get("status"),
                model=self.model_name,
                **log_fields(
                    response_id=run_id,
                    status=created.get("status"),
                    model=self.model_name,
                ),
            )

            observed_texts: set[tuple[str, str]] = set()
            stop_stream = asyncio.Event()
            stream_task = asyncio.create_task(
                self._observe_events_stream(
                    client,
                    run_id,
                    observer,
                    observed_texts=observed_texts,
                    stop=stop_stream,
                )
            )
            try:
                final_state = await self._poll_until_terminal(client, run_id, observer)
            finally:
                stop_stream.set()
                await stop_observation_task(
                    stream_task,
                    observer=observer,
                    endpoint="parallel",
                    response_id=run_id,
                )
            await self._replay_events_best_effort(
                client,
                run_id,
                observer,
                observed_texts=observed_texts,
            )
            output_text = _parallel_output_text(final_state)
            files = list(files_from_output_message(output_text))
            terminal_error = _terminal_error(run_id, final_state)
            raise_if_terminal_without_delivery(terminal_error, files)
            emit_terminal_delivery_available(
                observer=observer,
                endpoint="parallel",
                response_id=run_id,
                original_status=_parallel_status(final_state),
                terminal_error=terminal_error,
                files=files,
            )
            usage = _parallel_usage(final_state, processor=self._processor())
            cost_usd = _parallel_cost_usd(usage)
            emit_event(
                observer,
                "endpoint.usage",
                "Parallel usage available.",
                endpoint="parallel",
                response_id=run_id,
                status=_parallel_status(final_state),
                cost_usd=cost_usd,
                **log_fields(response_id=run_id, status=_parallel_status(final_state)),
                **usage,
            )
            return EndpointResult(
                text=output_text,
                files=tuple(files),
                raw={"result": final_state},
                usage=usage,
                cost_usd=cost_usd,
                response_id=run_id,
            )

    async def _create_run(self, client: Any, prompt: str) -> dict[str, Any]:
        response = await _request_with_retries(
            lambda: client.post(
                f"{self.base_url}{PARALLEL_RUNS_PATH}",
                headers=self._headers(),
                json=self._create_payload(prompt),
            )
        )
        return response.json()

    def _create_payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "input": prompt,
            "processor": self._processor(),
            "task_spec": self.request.task_spec
            or {
                "output_schema": (
                    "A free-text response. End with one fenced "
                    "`file:results_<task>.jsonl` block per requested task as "
                    "instructed in the input."
                )
            },
            "enable_events": (
                True
                if self.request.enable_events is None
                else self.request.enable_events
            ),
        }
        optional_values = {
            "metadata": self.request.metadata,
            "source_policy": self.request.source_policy,
            "advanced_settings": self.request.advanced_settings,
            "previous_interaction_id": self.request.previous_interaction_id,
            "webhook": self.request.webhook,
        }
        for key, value in optional_values.items():
            if value is not None:
                payload[key] = value
        if self.request.mcp_servers:
            payload["mcp_servers"] = [dict(server) for server in self.request.mcp_servers]
        return payload

    def _processor(self) -> str:
        if self.request.processor:
            return self.request.processor
        normalized = self.model_name.strip().lower().replace("_", "-")
        aliases = {
            "parallel-taskapi": "ultra4x",
            "taskapi": "ultra4x",
            "parallel-task-api": "ultra4x",
            "task-api": "ultra4x",
            "baseline": "ultra4x",
            "x8": "ultra8x",
        }
        return aliases.get(normalized, normalized)

    async def _poll_until_terminal(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
    ) -> dict[str, Any]:
        terminal_result_misses = 0
        while True:
            payload = await self._get_result_or_none(
                client,
                run_id,
                api_timeout_seconds=self.result_block_timeout_sec,
                observer=observer,
            )
            if payload is not None:
                return payload

            status = await self._status_or_unknown(client, run_id, observer)
            if status in PARALLEL_STATUS_TERMINAL:
                payload = await self._get_result_or_none(
                    client,
                    run_id,
                    api_timeout_seconds=1,
                    observer=observer,
                )
                if payload is not None:
                    return payload
                terminal_result_misses += 1
                if terminal_result_misses >= PARALLEL_TERMINAL_RESULT_MISS_LIMIT:
                    raise RelayError(
                        f"Parallel task run {run_id} reached terminal status "
                        f"{status}, but the result endpoint stayed unavailable."
                    )
            else:
                terminal_result_misses = 0

            await asyncio.sleep(5.0)

    async def _get_result_or_none(
        self,
        client: Any,
        run_id: str,
        *,
        api_timeout_seconds: int,
        observer: RelayObserver | None,
    ) -> dict[str, Any] | None:
        try:
            response = await client.get(
                f"{self.base_url}{PARALLEL_RUNS_PATH}/{run_id}/result",
                params={"api_timeout_seconds": str(api_timeout_seconds)},
                headers=self._headers(),
                timeout=api_timeout_seconds + 30.0,
            )
            if response.status_code == 408:
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Parallel Task API run is still running.",
                    endpoint="parallel",
                    response_id=run_id,
                    status="running",
                    **log_fields(response_id=run_id, status="running"),
                )
                return None
            if response.status_code == 404:
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Parallel result is not available yet.",
                    endpoint="parallel",
                    response_id=run_id,
                    status="result_not_found",
                    status_code=response.status_code,
                    **log_fields(response_id=run_id, status="result_not_found"),
                )
                return None
            if _retryable_status(response.status_code):
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Parallel result poll returned a retryable status.",
                    endpoint="parallel",
                    response_id=run_id,
                    status="result_retrying",
                    status_code=response.status_code,
                    **log_fields(response_id=run_id, status="result_retrying"),
                )
                return None
            response.raise_for_status()
            return response.json()
        except httpx.ReadTimeout:
            emit_event(
                observer,
                "endpoint.poll",
                "Parallel result poll timed out.",
                endpoint="parallel",
                response_id=run_id,
                status="result_timeout",
                **log_fields(response_id=run_id, status="result_timeout"),
            )
            return None
        except httpx.TransportError as exc:
            emit_event(
                observer,
                "endpoint.poll",
                "Parallel result poll hit a transport error.",
                endpoint="parallel",
                response_id=run_id,
                status="result_transport_error",
                error_type=type(exc).__name__,
                **log_fields(response_id=run_id, status="result_transport_error"),
            )
            return None

    async def _status_or_unknown(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
    ) -> str:
        try:
            response = await client.get(
                f"{self.base_url}{PARALLEL_RUNS_PATH}/{run_id}",
                headers=self._headers(),
                timeout=PARALLEL_HTTP_TIMEOUT_SEC,
            )
            response.raise_for_status()
            status = _parallel_status(response.json())
        except httpx.HTTPError as exc:
            emit_event(
                observer,
                "endpoint.poll",
                "Parallel status poll failed.",
                endpoint="parallel",
                response_id=run_id,
                status="status_error",
                error_type=type(exc).__name__,
                **log_fields(response_id=run_id, status="status_error"),
            )
            return "unknown"
        emit_event(
            observer,
            "endpoint.poll",
            "Polled Parallel Task API run status.",
            endpoint="parallel",
            response_id=run_id,
            status=status,
            **log_fields(response_id=run_id, status=status),
        )
        return status

    async def _replay_events(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
        observed_texts: set[tuple[str, str]],
    ) -> None:
        response = await _request_with_retries(
            lambda: client.get(
                f"{self.base_url}{PARALLEL_RUNS_PATH}/{run_id}{PARALLEL_EVENTS_PATH_SUFFIX}",
                headers={**self._headers(), "Accept": "text/event-stream"},
                timeout=PARALLEL_HTTP_TIMEOUT_SEC,
            )
        )
        for event in _parse_sse_events(response.text):
            _emit_parallel_event(run_id, event, observer, observed_texts)

    async def _replay_events_best_effort(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
        *,
        observed_texts: set[tuple[str, str]],
    ) -> None:
        try:
            await self._replay_events(client, run_id, observer, observed_texts)
        except Exception as exc:
            emit_event(
                observer,
                "endpoint.poll",
                "Parallel Task API event replay failed.",
                endpoint="parallel",
                response_id=run_id,
                status="event_replay_failed",
                error_type=type(exc).__name__,
                **log_fields(response_id=run_id, status="event_replay_failed"),
            )

    async def _observe_events_stream(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
        *,
        observed_texts: set[tuple[str, str]],
        stop: asyncio.Event,
    ) -> None:
        backoff = PARALLEL_REQUEST_RETRY_INITIAL_BACKOFF_SEC
        while not stop.is_set():
            try:
                await self._consume_events_stream_once(
                    client,
                    run_id,
                    observer,
                    observed_texts=observed_texts,
                    stop=stop,
                )
                backoff = PARALLEL_REQUEST_RETRY_INITIAL_BACKOFF_SEC
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Parallel Task API event stream interrupted.",
                    endpoint="parallel",
                    response_id=run_id,
                    status="observation_retrying",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    **log_fields(response_id=run_id, status="observation_retrying"),
                )
            if not stop.is_set():
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, PARALLEL_REQUEST_RETRY_MAX_BACKOFF_SEC)

    async def _consume_events_stream_once(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
        *,
        observed_texts: set[tuple[str, str]],
        stop: asyncio.Event,
    ) -> None:
        async with client.stream(
            "GET",
            f"{self.base_url}{PARALLEL_RUNS_PATH}/{run_id}{PARALLEL_EVENTS_PATH_SUFFIX}",
            headers={**self._headers(), "Accept": "text/event-stream"},
            timeout=None,
        ) as response:
            response.raise_for_status()
            event_type: str | None = None
            data_lines: list[str] = []
            async for line in response.aiter_lines():
                if stop.is_set():
                    return
                if not line:
                    event = _sse_event(event_type, data_lines)
                    if event is not None:
                        _emit_parallel_event(run_id, event, observer, observed_texts)
                    event_type = None
                    data_lines = []
                    continue
                if line.startswith("event:"):
                    event_type = line.removeprefix("event:").strip()
                elif line.startswith("data:"):
                    data_lines.append(line.removeprefix("data:").strip())

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise RelayError("missing env PARALLEL_API_KEY; export it or pass api_key")
        return {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }


def _parallel_output_text(result: Mapping[str, Any]) -> str:
    output = _dict(result.get("output"))
    content = output.get("content")
    if isinstance(content, str):
        return content
    if content is not None:
        return json.dumps(content, sort_keys=True)
    return ""


def _emit_parallel_event(
    run_id: str,
    event: Mapping[str, Any],
    observer: RelayObserver | None,
    observed_texts: set[tuple[str, str]],
) -> None:
    output = _dict(event.get("output"))
    content = _parallel_output_text(event)
    status = _parallel_status(event)
    basis = _list(output.get("basis"))
    for index, item in enumerate(basis):
        reasoning = _dict(item).get("reasoning")
        if not isinstance(reasoning, str) or not reasoning.strip():
            continue
        text_key = ("reasoning", reasoning)
        if text_key in observed_texts:
            continue
        observed_texts.add(text_key)
        emit_event(
            observer,
            "endpoint.message",
            "Received Parallel Task API reasoning.",
            semantic_type="reasoning",
            endpoint="parallel",
            response_id=run_id,
            status=status,
            event_id=event.get("event_id"),
            event_type=event.get("type"),
            basis_index=index,
            text_bytes=len(reasoning.encode()),
            **{EVENT_TEXT: reasoning, EVENT_TEXT_PREVIEW: _preview(reasoning)},
            **log_fields(response_id=run_id, status=status),
        )
    if not content.strip():
        return
    text_key = ("narration", content)
    if text_key in observed_texts:
        return
    observed_texts.add(text_key)
    emit_event(
        observer,
        "endpoint.message",
        "Received Parallel Task API output.",
        semantic_type="narration",
        endpoint="parallel",
        response_id=run_id,
        status=status,
        event_id=event.get("event_id"),
        event_type=event.get("type"),
        basis_count=len(basis),
        text_bytes=len(content.encode()),
        **{EVENT_TEXT: content, EVENT_TEXT_PREVIEW: _preview(content)},
        **log_fields(response_id=run_id, status=status),
    )


def _parallel_status(result: Mapping[str, Any]) -> str:
    run = _dict(result.get("run"))
    status = result.get("status")
    if isinstance(status, dict):
        status = status.get("status")
    return str(run.get("status") or status or "completed")


def _parallel_usage(result: Mapping[str, Any], *, processor: str) -> dict[str, Any]:
    usage = _dict(result.get("usage"))
    out = {key: usage[key] for key in ("input_tokens", "output_tokens", "total_tokens") if key in usage}
    out["processor"] = processor
    return out


def _parallel_cost_usd(usage: Mapping[str, Any]) -> float | None:
    processor = usage.get("processor")
    if not isinstance(processor, str):
        return None
    return PARALLEL_PROCESSOR_COSTS.get(processor)


def _terminal_error(run_id: str, final_state: Mapping[str, Any]) -> RelayError | None:
    status = _parallel_status(final_state)
    if status == "completed":
        return None
    details = final_state.get("error") or final_state.get("errors")
    suffix = f": {json.dumps(details, sort_keys=True)}" if details else "."
    return RelayError(f"Parallel task run {run_id} ended with status {status}{suffix}")


async def _request_with_retries(operation: Callable[[], Awaitable[Any]]) -> Any:
    for attempt in range(PARALLEL_REQUEST_RETRY_ATTEMPTS):
        try:
            response = await operation()
            if response.status_code < 400:
                return response
            if not _retryable_status(response.status_code):
                raise RelayError(_http_error_message(response))
            if attempt == PARALLEL_REQUEST_RETRY_ATTEMPTS - 1:
                raise RelayError(_http_error_message(response))
        except httpx.TransportError:
            if attempt == PARALLEL_REQUEST_RETRY_ATTEMPTS - 1:
                raise
        await asyncio.sleep(
            min(
                PARALLEL_REQUEST_RETRY_INITIAL_BACKOFF_SEC * (2**attempt),
                PARALLEL_REQUEST_RETRY_MAX_BACKOFF_SEC,
            )
        )
    raise RelayError("Parallel request exhausted retries.")


def _retryable_status(status_code: int) -> bool:
    return status_code >= 500 or status_code in {408, 409, 425, 429}


def _http_error_message(response: Any) -> str:
    body = _response_body(response)
    suffix = f": {body}" if body else ""
    return f"Parallel request failed with HTTP {response.status_code}{suffix}"


def _response_body(response: Any) -> str:
    text = getattr(response, "text", "")
    if isinstance(text, str) and text.strip():
        return text.strip()[:2000]
    try:
        return json.dumps(response.json(), sort_keys=True)[:2000]
    except Exception:
        return ""


def _first_env(env: Mapping[str, str] | None, names: tuple[str, ...]) -> str | None:
    for source in (env or {}, os.environ):
        for name in names:
            value = source.get(name)
            if value:
                return value
    return None


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _parse_sse_events(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    event_type: str | None = None
    data_lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r")
        if not line:
            _append_sse_event(events, event_type, data_lines)
            event_type = None
            data_lines = []
            continue
        if line.startswith("event:"):
            event_type = line.removeprefix("event:").strip()
        if line.startswith("data:"):
            data_lines.append(line.removeprefix("data:").strip())
    _append_sse_event(events, event_type, data_lines)
    return events


def _append_sse_event(
    events: list[dict[str, Any]],
    event_type: str | None,
    data_lines: list[str],
) -> None:
    event = _sse_event(event_type, data_lines)
    if event is not None:
        events.append(event)


def _sse_event(
    event_type: str | None,
    data_lines: list[str],
) -> dict[str, Any] | None:
    if not data_lines:
        return None
    try:
        payload = json.loads("\n".join(data_lines))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    if event_type and "type" not in payload:
        payload["type"] = event_type
    return payload


def _preview(text: str, limit: int = 500) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."
