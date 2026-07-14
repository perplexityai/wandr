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
    ProducedFile,
    RelayError,
    RelayObserver,
    emit_event,
    files_from_output_message,
    log_fields,
    normalize_output_path,
    stop_observation_task,
)
from relay.lifecycle import (
    EndpointRun,
    attach_endpoint_run_error,
    cancel_endpoint_run,
    close_endpoint_run,
    register_endpoint_run,
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


EXA_BASE_URL = "https://api.exa.ai"
EXA_RUNS_PATH = "/agent/runs"
EXA_OUTPUT_DETAILS = output_delivery_details(
    tool_phrase="Use the available research tools"
)
EXA_HTTP_TIMEOUT_SEC = 120.0
EXA_REQUEST_RETRY_ATTEMPTS = 8
EXA_REQUEST_RETRY_INITIAL_BACKOFF_SEC = 1.0
EXA_REQUEST_RETRY_MAX_BACKOFF_SEC = 60.0
EXA_TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled", "timed_out"})
EXA_FILE_OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "files": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        }
    },
    "required": ["files"],
}


@dataclass(frozen=True)
class ExaRequest:
    effort: str | None = None
    output_schema: Mapping[str, Any] | None = None
    input: Mapping[str, Any] | None = None
    previous_run_id: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> Self:
        data = validate_request_mapping(
            value,
            provider="Exa",
            allowed={
                "effort",
                "output_schema",
                "outputSchema",
                "input",
                "previous_run_id",
                "previousRunId",
            },
        )
        return cls(
            effort=data.get("effort"),
            output_schema=data.get("output_schema") or data.get("outputSchema"),
            input=data.get("input"),
            previous_run_id=data.get("previous_run_id") or data.get("previousRunId"),
        )


class ExaAgentEndpoint:
    """Exa Agent async run endpoint with output transport."""

    def __init__(
        self,
        *,
        model_name: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        env: Mapping[str, str] | None = None,
        request: Mapping[str, Any] | None = None,
        delivery_channel: str = "output",
        poll_interval_sec: float = 10.0,
        **_: Any,
    ):
        if delivery_channel != "output":
            raise RelayError("Exa Agent currently supports output delivery.")
        self.model_name = model_name or "agent"
        self.api_key = api_key or _first_env(env, ("EXA_API_KEY",))
        self.base_url = (base_url or EXA_BASE_URL).rstrip("/")
        self.request = ExaRequest.from_mapping(request)
        self.poll_interval_sec = poll_interval_sec

    @property
    def delivery_method(self) -> DeliveryMethod:
        return DeliveryMethod(
            name="output",
            output_root=None,
            details=EXA_OUTPUT_DETAILS,
        )

    async def run(
        self,
        prompt: str,
        observer: RelayObserver | None = None,
    ) -> EndpointResult:
        if httpx is None:
            raise RelayError("httpx is not installed. Install `relay[remote]`.")

        async with httpx.AsyncClient(timeout=EXA_HTTP_TIMEOUT_SEC) as client:
            active_run: EndpointRun | None = None
            try:
                created = await self._create_run(client, prompt)
                run_id = _run_id(created)
                if not run_id:
                    raise RelayError("Exa Agent run creation returned no run id.")
                active_run = register_endpoint_run(
                    provider="exa",
                    run_id=run_id,
                    cancel=lambda: self._cancel_run_by_id(run_id),
                    observer=observer,
                )
                emit_event(
                    observer,
                    "endpoint.submitted",
                    "Submitted Exa Agent run.",
                    endpoint="exa",
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
                    final_state = await self._poll_until_terminal(
                        client,
                        run_id,
                        observer,
                        initial_state=created,
                    )
                finally:
                    stop_stream.set()
                    await stop_observation_task(
                        stream_task,
                        observer=observer,
                        endpoint="exa",
                        response_id=run_id,
                    )
                await self._replay_events_best_effort(
                    client,
                    run_id,
                    observer,
                    observed_texts=observed_texts,
                )
                output_text = _exa_output_text(final_state)
                files = _exa_output_files(final_state, output_text)
                terminal_error = _terminal_error(run_id, final_state)
                raise_if_terminal_without_delivery(terminal_error, files)
                emit_terminal_delivery_available(
                    observer=observer,
                    endpoint="exa",
                    response_id=run_id,
                    original_status=final_state.get("status"),
                    terminal_error=terminal_error,
                    files=files,
                )
                usage = _exa_usage(final_state)
                cost_usd = _exa_cost_usd(final_state)
                emit_event(
                    observer,
                    "endpoint.usage",
                    "Exa usage available.",
                    endpoint="exa",
                    response_id=run_id,
                    status=final_state.get("status"),
                    cost_usd=cost_usd,
                    **log_fields(
                        response_id=run_id,
                        status=final_state.get("status"),
                    ),
                    **usage,
                )
                return EndpointResult(
                    text=output_text,
                    files=tuple(files),
                    raw={"run": final_state},
                    usage=usage,
                    cost_usd=cost_usd,
                    response_id=run_id,
                )
            except BaseException as exc:
                attach_endpoint_run_error(exc, active_run)
                await cancel_endpoint_run(active_run, reason=type(exc).__name__)
                active_run = None
                raise
            finally:
                close_endpoint_run(active_run)

    async def _create_run(self, client: Any, prompt: str) -> dict[str, Any]:
        response = await _request_with_retries(
            lambda: client.post(
                f"{self.base_url}{EXA_RUNS_PATH}",
                headers=self._headers(),
                json=self._create_payload(prompt),
            )
        )
        return response.json()

    def _create_payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "query": prompt,
            "effort": self.request.effort or _effort_from_model(self.model_name),
        }
        payload["outputSchema"] = dict(
            self.request.output_schema or EXA_FILE_OUTPUT_SCHEMA
        )
        if self.request.input is not None:
            payload["input"] = dict(self.request.input)
        if self.request.previous_run_id is not None:
            payload["previousRunId"] = self.request.previous_run_id
        return payload

    async def _poll_until_terminal(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
        *,
        initial_state: Mapping[str, Any],
    ) -> dict[str, Any]:
        state = dict(initial_state)
        status = str(state.get("status") or "unknown")
        while status not in EXA_TERMINAL_STATUSES:
            await asyncio.sleep(self.poll_interval_sec)
            next_state = await self._retrieve_run_or_none(client, run_id, observer)
            if next_state is None:
                continue
            state = next_state
            status = str(state.get("status") or "unknown")
            emit_event(
                observer,
                "endpoint.poll",
                "Polled Exa Agent run.",
                endpoint="exa",
                response_id=run_id,
                status=status,
                **log_fields(response_id=run_id, status=status),
            )
        return state

    async def _retrieve_run_or_none(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
    ) -> dict[str, Any] | None:
        try:
            response = await client.get(
                f"{self.base_url}{EXA_RUNS_PATH}/{run_id}",
                headers=self._headers(),
            )
            if _retryable_status(response.status_code):
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Exa Agent poll returned a retryable status.",
                    endpoint="exa",
                    response_id=run_id,
                    status="poll_retrying",
                    status_code=response.status_code,
                    **log_fields(response_id=run_id, status="poll_retrying"),
                )
                return None
            response.raise_for_status()
            return response.json()
        except httpx.TransportError as exc:
            emit_event(
                observer,
                "endpoint.poll",
                "Exa Agent poll hit a transport error.",
                endpoint="exa",
                response_id=run_id,
                status="poll_transport_error",
                error_type=type(exc).__name__,
                **log_fields(response_id=run_id, status="poll_transport_error"),
            )
            return None

    async def _replay_events(
        self,
        client: Any,
        run_id: str,
        observer: RelayObserver | None,
        observed_texts: set[tuple[str, str]],
    ) -> None:
        cursor: str | None = None
        while True:
            response = await _request_with_retries(
                lambda: client.get(
                    f"{self.base_url}{EXA_RUNS_PATH}/{run_id}/events",
                    headers=self._headers(),
                    params={"cursor": cursor} if cursor else None,
                )
            )
            payload = response.json()
            for event in _list(payload.get("data")):
                _emit_exa_event(run_id, _dict(event), observer, observed_texts)
            cursor_value = payload.get("nextCursor")
            if not payload.get("hasMore") or not isinstance(cursor_value, str):
                return
            cursor = cursor_value

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
                "Exa Agent event replay failed.",
                endpoint="exa",
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
        backoff = EXA_REQUEST_RETRY_INITIAL_BACKOFF_SEC
        while not stop.is_set():
            try:
                await self._consume_events_stream_once(
                    client,
                    run_id,
                    observer,
                    observed_texts=observed_texts,
                    stop=stop,
                )
                backoff = EXA_REQUEST_RETRY_INITIAL_BACKOFF_SEC
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Exa Agent event stream interrupted.",
                    endpoint="exa",
                    response_id=run_id,
                    status="observation_retrying",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    **log_fields(response_id=run_id, status="observation_retrying"),
                )
            if not stop.is_set():
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, EXA_REQUEST_RETRY_MAX_BACKOFF_SEC)

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
            f"{self.base_url}{EXA_RUNS_PATH}/{run_id}/events",
            headers={**self._headers(), "Accept": "text/event-stream"},
            timeout=None,
        ) as response:
            response.raise_for_status()
            event_name: str | None = None
            data_lines: list[str] = []
            async for line in response.aiter_lines():
                if stop.is_set():
                    return
                if not line:
                    event = _sse_event(event_name, data_lines)
                    if event is not None:
                        _emit_exa_event(run_id, event, observer, observed_texts)
                    event_name = None
                    data_lines = []
                    continue
                if line.startswith("event:"):
                    event_name = line.removeprefix("event:").strip()
                elif line.startswith("data:"):
                    data_lines.append(line.removeprefix("data:").strip())

    async def _cancel_run(self, client: Any, run_id: str) -> None:
        await _request_with_retries(
            lambda: client.post(
                f"{self.base_url}{EXA_RUNS_PATH}/{run_id}/cancel",
                headers=self._headers(),
                json={},
            )
        )

    async def _cancel_run_by_id(self, run_id: str) -> None:
        if httpx is None:
            return
        async with httpx.AsyncClient(timeout=EXA_HTTP_TIMEOUT_SEC) as client:
            await self._cancel_run(client, run_id)

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise RelayError("missing env EXA_API_KEY; export it or pass api_key")
        return {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }


def _effort_from_model(model_name: str) -> str:
    normalized = model_name.strip().lower().replace("_", "-")
    if normalized in {"low", "agent-low", "exa-agent-low"}:
        return "low"
    if normalized in {"medium", "agent-medium", "exa-agent-medium"}:
        return "medium"
    if normalized in {"high", "agent", "agent-high", "exa-agent", "exa-agent-high"}:
        return "high"
    if normalized in {"xhigh", "agent-xhigh", "exa-agent-xhigh"}:
        return "xhigh"
    if normalized in {"auto", "agent-auto", "exa-agent-auto"}:
        return "auto"
    return "high"


def _run_id(run: Mapping[str, Any]) -> str:
    return str(run.get("id") or run.get("run_id") or "")


def _exa_output_text(run: Mapping[str, Any]) -> str:
    output = _dict(run.get("output"))
    for key in ("text", "answer", "content"):
        value = output.get(key)
        if isinstance(value, str):
            return value
    for key in ("text", "answer"):
        value = run.get(key)
        if isinstance(value, str):
            return value
    structured = output.get("structured")
    if structured is not None:
        return json.dumps(structured, sort_keys=True)
    return ""


def _exa_output_files(run: Mapping[str, Any], output_text: str) -> list[ProducedFile]:
    structured = _dict(_dict(run.get("output")).get("structured"))
    structured_files = _exa_structured_files(structured)
    if structured_files:
        return structured_files
    return list(files_from_output_message(output_text))


def _exa_structured_files(structured: Mapping[str, Any]) -> list[ProducedFile]:
    raw_files = structured.get("files")
    files: list[ProducedFile] = []
    if isinstance(raw_files, Mapping):
        for path, content in raw_files.items():
            if isinstance(path, str) and isinstance(content, str):
                files.append(
                    ProducedFile(
                        path=normalize_output_path(path),
                        content=content.encode(),
                        source="structured_output",
                    )
                )
        return files

    for item in _list(raw_files):
        data = _dict(item)
        path = data.get("path")
        content = data.get("content")
        if isinstance(path, str) and isinstance(content, str):
            files.append(
                ProducedFile(
                    path=normalize_output_path(path),
                    content=content.encode(),
                    source="structured_output",
                )
            )
    return files


def _emit_exa_event(
    run_id: str,
    event: Mapping[str, Any],
    observer: RelayObserver | None,
    observed_texts: set[tuple[str, str]],
) -> None:
    event_name = str(event.get("event") or "unknown")
    data = _dict(event.get("data")) or _dict(event)
    text = _exa_output_text(data)
    if not text.strip():
        return
    text_key = ("narration", text)
    if text_key in observed_texts:
        return
    observed_texts.add(text_key)
    status = str(data.get("status") or "unknown")
    grounding = _dict(data.get("output")).get("grounding")
    emit_event(
        observer,
        "endpoint.message",
        "Received Exa Agent output.",
        semantic_type="narration",
        endpoint="exa",
        response_id=run_id,
        status=status,
        event_id=event.get("id"),
        event_type=event_name,
        grounding_count=len(_list(grounding)),
        text_bytes=len(text.encode()),
        **{EVENT_TEXT: text, EVENT_TEXT_PREVIEW: _preview(text)},
        **log_fields(response_id=run_id, status=status),
    )


def _exa_usage(run: Mapping[str, Any]) -> dict[str, Any]:
    usage = _dict(run.get("usage"))
    result = {
        key: usage[key]
        for key in ("agentComputeUnits", "searches", "emails", "phoneNumbers")
        if key in usage
    }
    return result


def _exa_cost_usd(run: Mapping[str, Any]) -> float | None:
    cost = run.get("costDollars")
    value = cost.get("total") if isinstance(cost, Mapping) else cost
    if value is None or isinstance(value, bool):
        return None
    return float(value)


def _terminal_error(run_id: str, final_state: Mapping[str, Any]) -> RelayError | None:
    status = str(final_state.get("status") or "unknown")
    if status == "completed":
        return None
    details = final_state.get("error") or final_state.get("errors")
    suffix = f": {json.dumps(details, sort_keys=True)}" if details else "."
    return RelayError(f"Exa Agent run {run_id} ended with status {status}{suffix}")


async def _request_with_retries(operation: Callable[[], Awaitable[Any]]) -> Any:
    for attempt in range(EXA_REQUEST_RETRY_ATTEMPTS):
        try:
            response = await operation()
            if _retryable_status(response.status_code):
                if attempt == EXA_REQUEST_RETRY_ATTEMPTS - 1:
                    response.raise_for_status()
            else:
                response.raise_for_status()
                return response
        except httpx.TransportError:
            if attempt == EXA_REQUEST_RETRY_ATTEMPTS - 1:
                raise
        await asyncio.sleep(
            min(
                EXA_REQUEST_RETRY_INITIAL_BACKOFF_SEC * (2**attempt),
                EXA_REQUEST_RETRY_MAX_BACKOFF_SEC,
            )
        )
    raise RelayError("Exa request exhausted retries.")


def _retryable_status(status_code: int) -> bool:
    return status_code >= 500 or status_code in {408, 409, 425, 429}


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


def _sse_event(
    event_name: str | None,
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
    if event_name and "event" not in payload:
        payload["event"] = event_name
    return payload


def _preview(text: str, limit: int = 500) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."
