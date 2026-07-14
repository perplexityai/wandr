import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Self

from relay.core import (
    OUTPUT_ROOT,
    DeliveryMethod,
    EndpointResult,
    ProducedFile,
    RelayError,
    RelayObserver,
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
from relay.providers.perplexity.events import (
    PERPLEXITY_TERMINAL_EVENTS,
    PERPLEXITY_TERMINAL_STATUSES,
    emit_perplexity_output_items,
    emit_perplexity_stream_event,
    mark_stream_observed_output_items,
    perplexity_cost_usd,
    perplexity_usage,
    response_text_from_perplexity_output,
    stream_event_key,
    stream_observed_output_item_key,
)
from relay.providers.perplexity.files import (
    PERPLEXITY_SHARE_NAME_PREFIX,
    collect_perplexity_shared_files,
    declared_perplexity_shared_files,
)
from relay.providers.request import validate_request_mapping
try:
    import httpx
except ImportError:  # pragma: no cover - exercised only without optional deps
    httpx = None  # type: ignore[assignment]


PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
PERPLEXITY_ENDPOINT_PATH = "/v2/responses"
PERPLEXITY_SHARE_DETAILS = (
    "Use the sandbox tool to create final files under the output root. For each "
    "final file, call `share_file` with `path` set to the sandbox file path and "
    f"`name` set to `{PERPLEXITY_SHARE_NAME_PREFIX}<encoded-path>`, where "
    "`<encoded-path>` is "
    "`base64.urlsafe_b64encode(relative_path.encode()).decode().rstrip('=')`. "
    "The relative path is the file path below the output root, such as "
    "`nested/out.txt`. The final message may summarize what was shared; do not "
    "paste file contents. If `share_file` is temporarily unavailable or returns "
    "a transient error, wait (briefly) with a sandbox sleep command and retry the "
    "same final file (just a couple of times) before concluding delivery is impossible "
    "(which could still happen)."
)
PERPLEXITY_OUTPUT_DETAILS = (
    "You can and are encouraged to use web search and sandbox tooling during "
    "the run. Filesystem state and tool-output blocks are not externally "
    "observable as submitted files in this mode, so delivery must still be "
    "performed through the final response. Delivery should not affect the "
    "workflow or behavior: work as you normally would, regardless of delivery "
    "particularities, arriving at an in-sandbox final file. Delivery should "
    "adapt to the artifact, not the other way around: load the file in your "
    "context right before completion by whichever tool or method you prefer, "
    "then emit its contents as a fenced block verbatim, in full, without any "
    "omissions, line-by-line, every bit of it. Constructing fenced blocks "
    "on-the-fly without the reference risks performance degradation; omitting "
    "information relative to the exact in-sandbox reference is guaranteed to "
    "cost score. Do not reduce row count, detail coverage, schema richness, "
    "excerpt or answer-field fidelity, etc. to make emission easier; both "
    "vertical recall and horizontal row fidelity matter."
)
HTTP_TIMEOUT_SEC = 60.0
STREAM_SLICE_SEC = 30.0
REQUEST_RETRY_ATTEMPTS = 12
REQUEST_RETRY_INITIAL_BACKOFF_SEC = 1.0
REQUEST_RETRY_MAX_BACKOFF_SEC = 60.0
RETRYABLE_STATUS_CODES = frozenset({408, 409, 425, 429})


@dataclass(frozen=True)
class PerplexityRequest:
    reasoning_effort: str = "high"
    max_steps: int = 100
    max_output_tokens: int = 128000
    service_tier: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> Self:
        data = validate_request_mapping(
            value,
            provider="Perplexity",
            allowed={
                "reasoning_effort",
                "max_steps",
                "max_output_tokens",
                "service_tier",
            },
        )
        return cls(
            reasoning_effort=str(data.get("reasoning_effort", "high")),
            max_steps=int(data.get("max_steps", 100)),
            max_output_tokens=int(data.get("max_output_tokens", 128000)),
            service_tier=data.get("service_tier"),
        )


class PerplexityAgentAPIEndpoint:
    """Perplexity Agent API endpoint with share or final-output transport."""

    def __init__(
        self,
        *,
        model_name: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        endpoint_path: str | None = None,
        env: Mapping[str, str] | None = None,
        request: Mapping[str, Any] | None = None,
        delivery_channel: str = "share",
        output_root: str = OUTPUT_ROOT.as_posix(),
        poll_interval_sec: float = 2.0,
        stream_slice_sec: float = STREAM_SLICE_SEC,
        **_: Any,
    ):
        self.delivery_channel = _normalize_delivery_channel(delivery_channel)
        self.model_name = model_name or "gpt-5.5"
        self.api_model_name = _agent_api_model(self.model_name)
        self.api_key = api_key or _first_env(env, ("PERPLEXITY_API_KEY",))
        self.base_url = (base_url or PERPLEXITY_BASE_URL).rstrip("/")
        self.endpoint_path = endpoint_path or PERPLEXITY_ENDPOINT_PATH
        self.request = PerplexityRequest.from_mapping(request)
        self.output_root = PurePosixPath(output_root)
        self.poll_interval_sec = poll_interval_sec
        self.stream_slice_sec = stream_slice_sec

    @property
    def delivery_method(self) -> DeliveryMethod:
        if self.delivery_channel == "output":
            return DeliveryMethod(
                name="output",
                output_root=None,
                details=PERPLEXITY_OUTPUT_DETAILS,
            )
        return DeliveryMethod(
            name="share",
            output_root=self.output_root,
            details=PERPLEXITY_SHARE_DETAILS,
        )

    async def run(
        self,
        prompt: str,
        observer: RelayObserver | None = None,
    ) -> EndpointResult:
        if httpx is None:
            raise RelayError("httpx is not installed. Install `relay[remote]`.")

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SEC) as client:
            active_run: EndpointRun | None = None
            try:
                created = await self._create_response(client, prompt)
                response_id = str(created.get("id") or "")
                if not response_id:
                    raise RelayError(
                        "Perplexity Agent API response creation returned no id."
                    )
                active_run = register_endpoint_run(
                    provider="perplexity",
                    run_id=response_id,
                    cancel=lambda: self._cancel_response_by_id(response_id),
                    observer=observer,
                )
                emit_event(
                    observer,
                    "endpoint.submitted",
                    "Submitted Perplexity Agent API request.",
                    endpoint="perplexity",
                    response_id=response_id,
                    status=created.get("status"),
                    model=self.model_name,
                    **log_fields(
                        response_id=response_id,
                        status=created.get("status"),
                        model=self.model_name,
                    ),
                )

                final_state, events = await self._poll_until_terminal(
                    client,
                    response_id,
                    observer,
                )
                output_text = response_text_from_perplexity_output(final_state)
                files, artifacts = await self._collect_delivery(
                    client,
                    response_id,
                    final_state,
                    events,
                    output_text,
                    observer,
                )
                _raise_if_terminal_without_delivery(response_id, final_state, files)
                _emit_terminal_delivery_available(
                    response_id,
                    final_state,
                    files,
                    observer,
                )
                usage = perplexity_usage(final_state)
                cost_usd = perplexity_cost_usd(
                    self.api_model_name,
                    usage,
                    final_state,
                )
                emit_event(
                    observer,
                    "endpoint.usage",
                    "Perplexity usage available.",
                    endpoint="perplexity",
                    response_id=response_id,
                    status=final_state.get("status"),
                    cost_usd=cost_usd,
                    **log_fields(
                        response_id=response_id,
                        status=final_state.get("status"),
                    ),
                    **usage,
                )
                return EndpointResult(
                    text=output_text,
                    files=tuple(files),
                    artifacts=tuple(artifacts),
                    raw={"response": final_state, "events": events},
                    usage=usage,
                    cost_usd=cost_usd,
                    response_id=response_id,
                )
            except BaseException as exc:
                attach_endpoint_run_error(exc, active_run)
                await cancel_endpoint_run(active_run, reason=type(exc).__name__)
                active_run = None
                raise
            finally:
                close_endpoint_run(active_run)

    async def _create_response(self, client: Any, prompt: str) -> dict[str, Any]:
        body = self._create_payload(prompt)
        response = await _request_with_retries(
            lambda: client.post(
                f"{self.base_url}{self.endpoint_path}",
                headers=self._headers(),
                json=body,
            )
        )
        return response.json()

    def _create_payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.api_model_name,
            "input": prompt,
            "tools": [
                {"type": "web_search"},
                {"type": "sandbox"},
            ],
            "max_steps": self.request.max_steps,
            "max_output_tokens": self.request.max_output_tokens,
            "reasoning": {"effort": self.request.reasoning_effort},
            "background": True,
        }
        if self.request.service_tier is not None:
            payload["service_tier"] = self.request.service_tier
        return payload

    async def _collect_delivery(
        self,
        client: Any,
        response_id: str,
        final_state: Mapping[str, Any],
        events: list[dict[str, Any]],
        output_text: str,
        observer: RelayObserver | None = None,
    ) -> tuple[list[ProducedFile], list[Any]]:
        if self.delivery_channel == "output":
            return list(files_from_output_message(output_text)), []
        return await collect_perplexity_shared_files(
            get=lambda url: self._get(client, url),
            base_url=self.base_url,
            endpoint_path=self.endpoint_path,
            response_id=response_id,
            declarations=declared_perplexity_shared_files(final_state, events),
            observer=observer,
        )

    async def _poll_until_terminal(
        self,
        client: Any,
        response_id: str,
        observer: RelayObserver | None = None,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        events: list[dict[str, Any]] = []
        observed_stream_events: set[str] = set()
        observed_output_items: set[str] = set()
        last_sequence_number = -1
        consecutive_empty_streams = 0
        status = "in_progress"
        final_state: dict[str, Any] | None = None
        while status not in PERPLEXITY_TERMINAL_STATUSES:
            previous_sequence_number = last_sequence_number
            try:
                last_sequence_number, terminal_status = await asyncio.wait_for(
                    self._stream_once(
                        client,
                        response_id,
                        last_sequence_number + 1,
                        events,
                        observed_stream_events,
                        observed_output_items,
                        observer,
                    ),
                    timeout=self.stream_slice_sec,
                )
            except TimeoutError:
                last_sequence_number = _last_sequence_number(
                    events,
                    default=last_sequence_number,
                )
                terminal_status = None
            consecutive_empty_streams = (
                consecutive_empty_streams + 1
                if last_sequence_number == previous_sequence_number
                else 0
            )
            final_state = _terminal_response(events)
            if final_state is not None:
                mark_stream_observed_output_items(events, observed_output_items)
                emit_perplexity_output_items(
                    final_state,
                    observed_output_items,
                    observer,
                )
                status = str(final_state.get("status") or terminal_status or status)
                break

            if consecutive_empty_streams >= 2:
                final_state = await self._retrieve_response(client, response_id)
                mark_stream_observed_output_items(events, observed_output_items)
                emit_perplexity_output_items(
                    final_state,
                    observed_output_items,
                    observer,
                )
                status = str(final_state.get("status") or "unknown")
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Polled Perplexity Agent API request.",
                    endpoint="perplexity",
                    response_id=response_id,
                    status=status,
                    **log_fields(response_id=response_id, status=status),
                )
                consecutive_empty_streams = 0
            if status not in PERPLEXITY_TERMINAL_STATUSES:
                await asyncio.sleep(self.poll_interval_sec)

        if final_state is None:
            final_state = await self._retrieve_response(client, response_id)
        mark_stream_observed_output_items(events, observed_output_items)
        emit_perplexity_output_items(final_state, observed_output_items, observer)
        return final_state, events

    async def _stream_once(
        self,
        client: Any,
        response_id: str,
        starting_after: int,
        events: list[dict[str, Any]],
        observed_stream_events: set[str],
        observed_output_items: set[str],
        observer: RelayObserver | None,
    ) -> tuple[int, str | None]:
        last_sequence_number = starting_after - 1
        current_event_type: str | None = None
        try:
            async with client.stream(
                "GET",
                f"{self.base_url}{self.endpoint_path}/{response_id}",
                headers=self._headers(),
                params={
                    "stream": "true",
                    "starting_after": str(max(starting_after, 0)),
                },
            ) as response:
                if response.status_code != 200:
                    return last_sequence_number, None

                async for line in response.aiter_lines():
                    if line.startswith("event:"):
                        current_event_type = line[6:].strip()
                        continue
                    if not line.startswith("data:"):
                        continue

                    data = line[5:].strip()
                    try:
                        event = json.loads(data)
                    except json.JSONDecodeError as exc:
                        emit_event(
                            observer,
                            "endpoint.poll",
                            "Perplexity stream emitted malformed event.",
                            endpoint="perplexity",
                            response_id=response_id,
                            status="stream_malformed_event",
                            **log_fields(
                                response_id=response_id,
                                status="stream_malformed_event",
                            ),
                            error=str(exc),
                            data_preview=data[:200],
                        )
                        continue
                    event.setdefault("type", current_event_type or "")
                    sequence_number = event.get("sequence_number")
                    if isinstance(sequence_number, int):
                        last_sequence_number = max(
                            last_sequence_number, sequence_number
                        )
                    key = stream_event_key(event)
                    if key not in observed_stream_events:
                        observed_stream_events.add(key)
                        events.append(event)
                        output_item_key = stream_observed_output_item_key(event)
                        if output_item_key not in observed_output_items:
                            if output_item_key is not None:
                                observed_output_items.add(output_item_key)
                            emit_perplexity_stream_event(
                                event,
                                response_id=response_id,
                                observer=observer,
                            )
                    event_type = str(event.get("type") or "")
                    if event_type in PERPLEXITY_TERMINAL_EVENTS:
                        return last_sequence_number, event_type.split(".", 1)[1]
        except httpx.ReadTimeout:
            return last_sequence_number, None
        except httpx.HTTPError as exc:
            emit_event(
                observer,
                "endpoint.poll",
                "Perplexity stream request failed.",
                endpoint="perplexity",
                response_id=response_id,
                status="stream_error",
                **log_fields(response_id=response_id, status="stream_error"),
                error=str(exc),
            )
            return last_sequence_number, None
        return last_sequence_number, None

    async def _retrieve_response(self, client: Any, response_id: str) -> dict[str, Any]:
        response = await self._get(
            client,
            f"{self.base_url}{self.endpoint_path}/{response_id}",
        )
        return response.json()

    async def _cancel_response(self, client: Any, response_id: str) -> None:
        await _request_with_retries(
            lambda: client.post(
                f"{self.base_url}{self.endpoint_path}/{response_id}/cancel",
                headers=self._headers(),
                json={},
            )
        )

    async def _cancel_response_by_id(self, response_id: str) -> None:
        if httpx is None:
            return
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SEC) as client:
            await self._cancel_response(client, response_id)

    async def _get(self, client: Any, url: str) -> Any:
        return await _request_with_retries(
            lambda: client.get(
                url,
                headers=self._headers(),
            )
        )

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise RelayError("missing env PERPLEXITY_API_KEY; export it or pass api_key")
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


def _agent_api_model(model_name: str) -> str:
    return model_name if "/" in model_name else f"openai/{model_name}"


def _terminal_response(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    for event in reversed(events):
        if event.get("type") in PERPLEXITY_TERMINAL_EVENTS:
            response = event.get("response")
            return response if isinstance(response, dict) else None
    return None


def _last_sequence_number(events: list[dict[str, Any]], *, default: int) -> int:
    for event in reversed(events):
        sequence_number = event.get("sequence_number")
        if isinstance(sequence_number, int):
            return max(default, sequence_number)
    return default


def _terminal_error(
    response_id: str, final_state: Mapping[str, Any]
) -> RelayError | None:
    status = str(final_state.get("status") or "unknown")
    if status == "completed":
        return None
    return RelayError(f"Perplexity response {response_id} ended with status {status}.")


def _raise_if_terminal_without_delivery(
    response_id: str,
    final_state: Mapping[str, Any],
    files: list[ProducedFile],
) -> None:
    terminal_error = _terminal_error(response_id, final_state)
    if terminal_error is not None and not files:
        raise terminal_error


def _emit_terminal_delivery_available(
    response_id: str,
    final_state: Mapping[str, Any],
    files: list[ProducedFile],
    observer: RelayObserver | None,
) -> None:
    if _terminal_error(response_id, final_state) is None or not files:
        return
    emit_event(
        observer,
        "endpoint.poll",
        "Perplexity terminal response was not completed, but delivery files are available.",
        endpoint="perplexity",
        response_id=response_id,
        status="terminal_delivery_available",
        original_status=final_state.get("status"),
        paths=[file.path.as_posix() for file in files],
        bytes=sum(len(file.content) for file in files),
        **log_fields(
            response_id=response_id,
            status="terminal_delivery_available",
        ),
    )


async def _request_with_retries(operation: Callable[[], Awaitable[Any]]) -> Any:
    for attempt in range(REQUEST_RETRY_ATTEMPTS):
        try:
            response = await operation()
            if _retryable_status(response.status_code):
                if attempt == REQUEST_RETRY_ATTEMPTS - 1:
                    response.raise_for_status()
            else:
                response.raise_for_status()
                return response
        except httpx.TransportError:
            if attempt == REQUEST_RETRY_ATTEMPTS - 1:
                raise
        await asyncio.sleep(
            min(
                REQUEST_RETRY_INITIAL_BACKOFF_SEC * (2**attempt),
                REQUEST_RETRY_MAX_BACKOFF_SEC,
            )
        )
    raise RelayError("Perplexity request exhausted retries.")


def _retryable_status(status_code: int) -> bool:
    return status_code >= 500 or status_code in RETRYABLE_STATUS_CODES


def _normalize_delivery_channel(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    aliases = {
        "outrelay": "output",
        "output": "output",
        "share": "share",
    }
    if normalized not in aliases:
        raise RelayError(f"Unknown Perplexity delivery channel: {value}")
    return aliases[normalized]


def _first_env(env: Mapping[str, str] | None, names: tuple[str, ...]) -> str | None:
    for source in (env or {}, os.environ):
        for name in names:
            value = source.get(name)
            if value:
                return value
    return None
