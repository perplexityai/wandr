import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Self

from relay.core import (
    DeliveryMethod,
    EndpointResult,
    EVENT_TEXT,
    EVENT_TEXT_PREVIEW,
    RelayError,
    RelayObserver,
    RelaySemanticType,
    TokenPricing,
    USAGE_CACHE_READ_INPUT_TOKENS,
    USAGE_DETAILS,
    USAGE_INPUT_TOKENS,
    USAGE_OUTPUT_TOKENS,
    USAGE_REASONING_TOKENS,
    USAGE_TOTAL_INPUT_TOKENS,
    USAGE_TOTAL_TOKENS,
    USAGE_UNCACHED_INPUT_TOKENS,
    emit_event,
    files_from_output_message,
    log_fields,
    stop_observation_task,
    token_cost_usd,
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


GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_INTERACTIONS_PATH = "/interactions"
GEMINI_OUTPUT_DETAILS = output_delivery_details(
    tool_phrase="You may use code execution and other tools"
)
GEMINI_REQUEST_TIMEOUT_SEC = 60.0
GEMINI_REQUEST_RETRY_ATTEMPTS = 6
GEMINI_REQUEST_RETRY_INITIAL_BACKOFF_SEC = 1.0
GEMINI_REQUEST_RETRY_MAX_BACKOFF_SEC = 30.0
GEMINI_POLL_RETRY_ATTEMPTS = 120
GEMINI_POLL_RETRY_STATUS_CODES = frozenset({400, 404})
GEMINI_CONTEXT_PRICE_BREAKPOINT_TOKENS = 200_000
GEMINI_STANDARD_LOW_CONTEXT_PRICING = TokenPricing(
    uncached_input=2.0,
    cached_input=0.20,
    output_tokens=12.0,
)
GEMINI_STANDARD_HIGH_CONTEXT_PRICING = TokenPricing(
    uncached_input=4.0,
    cached_input=0.40,
    output_tokens=18.0,
)
GEMINI_SEARCH_QUERY_USD = 14.0 / 1_000
GEMINI_USAGE_SEARCH_QUERIES = "search_queries"
GEMINI_USAGE_COST_ESTIMATE = "cost_estimate"
GEMINI_USAGE_TOOL_USE_TOKENS = "tool_use_tokens"
GEMINI_TERMINAL_STATUSES = frozenset(
    {"completed", "failed", "cancelled", "incomplete", "budget_exceeded", "requires_action"}
)


@dataclass(frozen=True)
class GeminiRequest:
    reasoning_effort: str | None = None
    agent_config: Mapping[str, Any] | None = None
    tools: tuple[Mapping[str, Any], ...] = (
        {"type": "google_search"},
        {"type": "url_context"},
        {"type": "code_execution"},
    )

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> Self:
        data = validate_request_mapping(
            value,
            provider="Gemini",
            allowed={"reasoning_effort", "agent_config", "tools"},
        )
        tools = data.get("tools")
        return cls(
            reasoning_effort=data.get("reasoning_effort"),
            agent_config=data.get("agent_config")
            or {"type": "deep-research", "thinking_summaries": "auto"},
            tools=tuple(tools) if isinstance(tools, list | tuple) else cls.tools,
        )


class GeminiDeepResearchEndpoint:
    """Google Gemini Deep Research Interactions endpoint with output transport."""

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
            raise RelayError("Gemini Deep Research currently supports output delivery.")
        self.model_name = model_name or "deep-research"
        self.api_key = api_key or _first_env(
            env,
            ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
        )
        self.base_url = (base_url or GEMINI_BASE_URL).rstrip("/")
        self.request = GeminiRequest.from_mapping(request)
        self.reasoning_effort = _gemini_reasoning_effort(
            self.model_name, self.request.reasoning_effort
        )
        self.agent_name = _gemini_agent_name(self.model_name, self.reasoning_effort)
        self.poll_interval_sec = poll_interval_sec

    @property
    def delivery_method(self) -> DeliveryMethod:
        return DeliveryMethod(
            name="output",
            output_root=None,
            details=GEMINI_OUTPUT_DETAILS,
        )

    async def run(
        self,
        prompt: str,
        observer: RelayObserver | None = None,
    ) -> EndpointResult:
        if httpx is None:
            raise RelayError("httpx is not installed. Install `relay[remote]`.")

        async with httpx.AsyncClient(timeout=GEMINI_REQUEST_TIMEOUT_SEC) as client:
            active_run: EndpointRun | None = None
            try:
                created = await self._create_interaction(client, prompt)
                interaction_id = str(created.get("id") or "")
                if not interaction_id:
                    raise RelayError(
                        "Gemini interaction creation returned no interaction id."
                    )
                active_run = register_endpoint_run(
                    provider="gemini",
                    run_id=interaction_id,
                    cancel=lambda: self._cancel_interaction_by_id(interaction_id),
                    observer=observer,
                )
                emit_event(
                    observer,
                    "endpoint.submitted",
                    "Submitted Gemini Deep Research interaction.",
                    endpoint="gemini",
                    response_id=interaction_id,
                    status=created.get("status"),
                    model=self.model_name,
                    agent=self.agent_name,
                    reasoning_effort=self.reasoning_effort,
                    **log_fields(
                        response_id=interaction_id,
                        status=created.get("status"),
                        model=self.model_name,
                    ),
                )

                observed_texts: set[tuple[str, str]] = set()
                stop_stream = asyncio.Event()
                stream_task = asyncio.create_task(
                    self._observe_stream(
                        client,
                        interaction_id,
                        observer,
                        observed_texts=observed_texts,
                        stop=stop_stream,
                    )
                )
                try:
                    final_state = await self._poll_until_terminal(
                        client,
                        interaction_id,
                        observer,
                        initial_state=created,
                        observed_texts=observed_texts,
                    )
                finally:
                    stop_stream.set()
                    await stop_observation_task(
                        stream_task,
                        observer=observer,
                        endpoint="gemini",
                        response_id=interaction_id,
                    )
                output_text = _interaction_output_text(final_state)
                files = list(files_from_output_message(output_text))
                terminal_error = _terminal_error(interaction_id, final_state)
                raise_if_terminal_without_delivery(terminal_error, files)
                emit_terminal_delivery_available(
                    observer=observer,
                    endpoint="gemini",
                    response_id=interaction_id,
                    original_status=final_state.get("status"),
                    terminal_error=terminal_error,
                    files=files,
                )
                usage = _gemini_usage(final_state)
                cost_usd = _gemini_cost_usd(usage)
                emit_event(
                    observer,
                    "endpoint.usage",
                    "Gemini usage available.",
                    endpoint="gemini",
                    response_id=interaction_id,
                    status=final_state.get("status"),
                    cost_usd=cost_usd,
                    **log_fields(
                        response_id=interaction_id,
                        status=final_state.get("status"),
                    ),
                    **usage,
                )
                return EndpointResult(
                    text=output_text,
                    files=tuple(files),
                    raw={"interaction": final_state},
                    usage=usage,
                    cost_usd=cost_usd,
                    response_id=interaction_id,
                )
            except BaseException as exc:
                attach_endpoint_run_error(exc, active_run)
                await cancel_endpoint_run(active_run, reason=type(exc).__name__)
                active_run = None
                raise
            finally:
                close_endpoint_run(active_run)

    async def _create_interaction(self, client: Any, prompt: str) -> dict[str, Any]:
        response = await _request_with_retries(
            lambda: client.post(
                f"{self.base_url}{GEMINI_INTERACTIONS_PATH}",
                headers=self._headers(),
                json=self._create_payload(prompt),
            )
        )
        return response.json()

    def _create_payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "agent": self.agent_name,
            "input": prompt,
            "background": True,
        }
        if self.request.agent_config is not None:
            payload["agent_config"] = dict(self.request.agent_config)
        if self.request.tools:
            payload["tools"] = [dict(tool) for tool in self.request.tools]
        return payload

    async def _poll_until_terminal(
        self,
        client: Any,
        interaction_id: str,
        observer: RelayObserver | None,
        *,
        initial_state: Mapping[str, Any],
        observed_texts: set[tuple[str, str]],
    ) -> dict[str, Any]:
        state = dict(initial_state)
        observed_steps: set[tuple[str, int, int]] = set()
        _emit_interaction_steps(state, observer, observed_steps, observed_texts)
        status = str(state.get("status") or "unknown")
        consecutive_poll_failures = 0
        while status not in GEMINI_TERMINAL_STATUSES:
            await asyncio.sleep(self.poll_interval_sec)
            next_state = await self._retrieve_interaction_or_none(
                client,
                interaction_id,
                observer,
            )
            if next_state is None:
                consecutive_poll_failures += 1
                if consecutive_poll_failures >= GEMINI_POLL_RETRY_ATTEMPTS:
                    raise RelayError(
                        f"Gemini interaction {interaction_id} poll did not recover "
                        f"after {consecutive_poll_failures} consecutive retryable "
                        "failures."
                    )
                continue
            consecutive_poll_failures = 0
            state = next_state
            status = str(state.get("status") or "unknown")
            _emit_interaction_steps(state, observer, observed_steps, observed_texts)
            emit_event(
                observer,
                "endpoint.poll",
                "Polled Gemini Deep Research interaction.",
                endpoint="gemini",
                response_id=interaction_id,
                status=status,
                **log_fields(response_id=interaction_id, status=status),
            )
        return state

    async def _retrieve_interaction_or_none(
        self,
        client: Any,
        interaction_id: str,
        observer: RelayObserver | None,
    ) -> dict[str, Any] | None:
        try:
            response = await client.get(
                f"{self.base_url}{GEMINI_INTERACTIONS_PATH}/{interaction_id}",
                headers=self._headers(),
            )
            if _retryable_poll_status(response.status_code):
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Gemini Deep Research poll returned a retryable status.",
                    endpoint="gemini",
                    response_id=interaction_id,
                    status="poll_retrying",
                    status_code=response.status_code,
                    error_body=_preview(str(getattr(response, "text", "")), limit=2_000),
                    **log_fields(
                        response_id=interaction_id,
                        status="poll_retrying",
                    ),
                )
                return None
            response.raise_for_status()
            return response.json()
        except httpx.TransportError as exc:
            emit_event(
                observer,
                "endpoint.poll",
                "Gemini Deep Research poll hit a transport error.",
                endpoint="gemini",
                response_id=interaction_id,
                status="poll_transport_error",
                error_type=type(exc).__name__,
                **log_fields(
                    response_id=interaction_id,
                    status="poll_transport_error",
                ),
            )
            return None

    async def _observe_stream(
        self,
        client: Any,
        interaction_id: str,
        observer: RelayObserver | None,
        *,
        observed_texts: set[tuple[str, str]],
        stop: asyncio.Event,
    ) -> None:
        last_event_id: str | None = None
        backoff = GEMINI_REQUEST_RETRY_INITIAL_BACKOFF_SEC
        while not stop.is_set():
            try:
                last_event_id = await self._consume_stream_once(
                    client,
                    interaction_id,
                    observer,
                    observed_texts=observed_texts,
                    last_event_id=last_event_id,
                    stop=stop,
                )
                backoff = GEMINI_REQUEST_RETRY_INITIAL_BACKOFF_SEC
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                emit_event(
                    observer,
                    "endpoint.poll",
                    "Gemini stream observation interrupted.",
                    endpoint="gemini",
                    response_id=interaction_id,
                    status="observation_retrying",
                    error_type=type(exc).__name__,
                    error=str(exc),
                    **log_fields(
                        response_id=interaction_id,
                        status="observation_retrying",
                    ),
                )
            if not stop.is_set():
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, GEMINI_REQUEST_RETRY_MAX_BACKOFF_SEC)

    async def _consume_stream_once(
        self,
        client: Any,
        interaction_id: str,
        observer: RelayObserver | None,
        *,
        observed_texts: set[tuple[str, str]],
        last_event_id: str | None,
        stop: asyncio.Event,
    ) -> str | None:
        params = {"stream": "true"}
        if last_event_id:
            params["last_event_id"] = last_event_id
        async with client.stream(
            "GET",
            f"{self.base_url}{GEMINI_INTERACTIONS_PATH}/{interaction_id}",
            headers=self._headers(),
            params=params,
            timeout=None,
        ) as response:
            response.raise_for_status()
            event_name: str | None = None
            data_lines: list[str] = []
            async for line in response.aiter_lines():
                if stop.is_set():
                    return last_event_id
                if not line:
                    last_event_id = _emit_stream_event(
                        interaction_id,
                        event_name,
                        "\n".join(data_lines),
                        observer,
                        observed_texts,
                    ) or last_event_id
                    event_name = None
                    data_lines = []
                    continue
                if line.startswith("event:"):
                    event_name = line.removeprefix("event:").strip()
                elif line.startswith("data:"):
                    data_lines.append(line.removeprefix("data:").strip())
                elif line.startswith("id:"):
                    last_event_id = line.removeprefix("id:").strip()
        return last_event_id

    async def _cancel_interaction(self, client: Any, interaction_id: str) -> None:
        await _request_with_retries(
            lambda: client.post(
                f"{self.base_url}{GEMINI_INTERACTIONS_PATH}/{interaction_id}/cancel",
                headers=self._headers(),
                json={},
            )
        )

    async def _cancel_interaction_by_id(self, interaction_id: str) -> None:
        if httpx is None:
            return
        try:
            async with httpx.AsyncClient(timeout=GEMINI_REQUEST_TIMEOUT_SEC) as client:
                await self._cancel_interaction(client, interaction_id)
        except Exception:
            return

    def _headers(self) -> dict[str, str]:
        if not self.api_key:
            raise RelayError(
                "missing env GEMINI_API_KEY or GOOGLE_API_KEY; export one or pass api_key"
            )
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }


def _gemini_reasoning_effort(
    model_name: str, reasoning_effort: str | None = None
) -> str:
    effort = reasoning_effort or "speed"
    return effort.strip().lower().replace("_", "-")


def _gemini_agent_name(model_name: str, reasoning_effort: str | None = None) -> str:
    normalized = model_name.strip().lower().replace("_", "-")
    effort = _gemini_reasoning_effort(model_name, reasoning_effort)
    if normalized in {
        "deep-research-max-preview-04-2026",
        "deep-research-preview-04-2026",
    }:
        return model_name
    if normalized != "deep-research":
        return model_name
    aliases = {
        "max": "deep-research-max-preview-04-2026",
        "speed": "deep-research-preview-04-2026",
    }
    return aliases.get(effort, model_name)


def _interaction_output_text(interaction: Mapping[str, Any]) -> str:
    parts: list[str] = []
    for output in _list(interaction.get("outputs")):
        item = _dict(output)
        if text := _text_part(item):
            parts.append(text)
    for step in _list(interaction.get("steps")):
        item = _dict(step)
        if str(item.get("type") or "") != "model_output":
            continue
        for content in _list(item.get("content")):
            item = _dict(content)
            if text := _text_part(item):
                parts.append(text)
    return "\n\n".join(parts)


def _emit_interaction_steps(
    interaction: Mapping[str, Any],
    observer: RelayObserver | None,
    observed_steps: set[tuple[str, int, int]],
    observed_texts: set[tuple[str, str]],
) -> None:
    interaction_id = str(interaction.get("id") or "")
    status = str(interaction.get("status") or "unknown")
    for step_index, step in enumerate(_list(interaction.get("steps"))):
        item = _dict(step)
        step_type = str(item.get("type") or "")
        if step_type == "thought":
            _emit_step_text_items(
                interaction_id,
                status,
                step_index,
                step_type,
                _content_items(item.get("summary")),
                observer,
                observed_steps,
                observed_texts,
                semantic_type="reasoning",
                message="Received Gemini thought summary.",
                field="summary",
            )
        if step_type == "model_output":
            _emit_step_text_items(
                interaction_id,
                status,
                step_index,
                step_type,
                _content_items(item.get("content")),
                observer,
                observed_steps,
                observed_texts,
                semantic_type="narration",
                message="Received Gemini model output.",
                field="content",
            )


def _emit_step_text_items(
    interaction_id: str,
    status: str,
    step_index: int,
    step_type: str,
    items: Sequence[Mapping[str, Any]],
    observer: RelayObserver | None,
    observed_steps: set[tuple[str, int, int]],
    observed_texts: set[tuple[str, str]],
    *,
    semantic_type: RelaySemanticType,
    message: str,
    field: str,
) -> None:
    for item_index, item in enumerate(items):
        text = _text_part(item)
        if not text or not text.strip():
            continue
        key = (field, step_index, item_index)
        if key in observed_steps:
            continue
        text_key = (semantic_type, text)
        if text_key in observed_texts:
            continue
        observed_steps.add(key)
        observed_texts.add(text_key)
        emit_event(
            observer,
            "endpoint.message",
            message,
            semantic_type=semantic_type,
            endpoint="gemini",
            response_id=interaction_id,
            status=status,
            step_index=step_index,
            step_type=step_type,
            content_index=item_index,
            content_type=item.get("type"),
            text_bytes=len(text.encode()),
            **{EVENT_TEXT: text, EVENT_TEXT_PREVIEW: _preview(text)},
            **log_fields(response_id=interaction_id, status=status),
        )


def _emit_stream_event(
    interaction_id: str,
    event_name: str | None,
    data: str,
    observer: RelayObserver | None,
    observed_texts: set[tuple[str, str]],
) -> str | None:
    if not data.strip():
        return None
    try:
        payload = json.loads(data)
    except json.JSONDecodeError:
        return None

    item = _dict(payload)
    event_type = str(item.get("event_type") or event_name or "")
    if event_type == "step.delta":
        _emit_stream_delta(interaction_id, item, observer, observed_texts)
    elif event_type == "step.end":
        _emit_stream_step_end(interaction_id, item, observer, observed_texts)

    event_id = item.get("event_id")
    return event_id if isinstance(event_id, str) else None


def _emit_stream_delta(
    interaction_id: str,
    payload: Mapping[str, Any],
    observer: RelayObserver | None,
    observed_texts: set[tuple[str, str]],
) -> None:
    delta = _dict(payload.get("delta"))
    content = _dict(delta.get("content"))
    text = _text_part(content)
    if not text or not text.strip():
        return
    delta_type = str(delta.get("type") or "")
    semantic_type: RelaySemanticType = (
        "reasoning" if delta_type == "thought_summary" else "narration"
    )
    text_key = (semantic_type, text)
    if text_key in observed_texts:
        return
    observed_texts.add(text_key)
    status = str(payload.get("status") or "in_progress")
    emit_event(
        observer,
        "endpoint.message",
        (
            "Received Gemini thought summary."
            if semantic_type == "reasoning"
            else "Received Gemini stream output."
        ),
        semantic_type=semantic_type,
        endpoint="gemini",
        response_id=interaction_id,
        status=status,
        event_type=payload.get("event_type"),
        event_id=payload.get("event_id"),
        step_index=payload.get("index"),
        delta_type=delta_type,
        content_type=content.get("type"),
        text_bytes=len(text.encode()),
        **{EVENT_TEXT: text, EVENT_TEXT_PREVIEW: _preview(text)},
        **log_fields(response_id=interaction_id, status=status),
    )


def _emit_stream_step_end(
    interaction_id: str,
    payload: Mapping[str, Any],
    observer: RelayObserver | None,
    observed_texts: set[tuple[str, str]],
) -> None:
    step = _dict(payload.get("step"))
    if not step:
        return
    step_index = _int_or_none(payload.get("index")) or 0
    step_type = str(step.get("type") or "")
    observed_steps: set[tuple[str, int, int]] = set()
    if step_type == "thought":
        _emit_step_text_items(
            interaction_id,
            "in_progress",
            step_index,
            step_type,
            _content_items(step.get("summary")),
            observer,
            observed_steps,
            observed_texts,
            semantic_type="reasoning",
            message="Received Gemini thought summary.",
            field="summary",
        )
    elif step_type == "model_output":
        _emit_step_text_items(
            interaction_id,
            "in_progress",
            step_index,
            step_type,
            _content_items(step.get("content")),
            observer,
            observed_steps,
            observed_texts,
            semantic_type="narration",
            message="Received Gemini model output.",
            field="content",
        )


def _content_items(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, str):
        return [{"type": "text", "text": value}]
    if isinstance(value, Mapping):
        return [value]
    if isinstance(value, list):
        return [_dict(item) for item in value if _dict(item)]
    return []


def _text_part(item: Mapping[str, Any]) -> str | None:
    for key in ("text", "result", "content"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return None


def _preview(text: str, limit: int = 500) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def _gemini_usage(interaction: Mapping[str, Any]) -> dict[str, Any]:
    usage = (
        _dict(interaction.get("usage"))
        or _dict(interaction.get("usageMetadata"))
        or _dict(interaction.get("usage_metadata"))
    )
    input_tokens = _first_int(
        usage.get("input_tokens"),
        usage.get("total_input_tokens"),
        usage.get("promptTokenCount"),
    )
    output_tokens = _first_int(
        usage.get("output_tokens"),
        usage.get("total_output_tokens"),
        usage.get("candidatesTokenCount"),
    )
    reasoning_tokens = _first_int(
        usage.get("reasoning_tokens"),
        usage.get("total_thought_tokens"),
        usage.get("thoughtsTokenCount"),
    )
    tool_use_tokens = _first_int(
        usage.get("tool_use_tokens"),
        usage.get("total_tool_use_tokens"),
        usage.get("toolUseTokenCount"),
    )
    total_tokens = _first_int(usage.get("total_tokens"), usage.get("totalTokenCount"))
    cache_tokens = _first_int(
        usage.get("total_cached_tokens"),
        usage.get("cache_read_input_tokens"),
        usage.get("cachedContentTokenCount"),
    )
    search_queries = _first_int(
        usage.get("search_queries"),
        usage.get("searches"),
        usage.get("google_search_queries"),
        usage.get("searchQueries"),
        usage.get("total_search_queries"),
    )
    result: dict[str, Any] = {}
    if input_tokens is not None:
        result[USAGE_INPUT_TOKENS] = input_tokens
        result[USAGE_TOTAL_INPUT_TOKENS] = input_tokens
    if output_tokens is not None:
        result[USAGE_OUTPUT_TOKENS] = output_tokens
    if reasoning_tokens is not None:
        result[USAGE_REASONING_TOKENS] = reasoning_tokens
    if total_tokens is not None:
        result[USAGE_TOTAL_TOKENS] = total_tokens
    if cache_tokens is not None:
        result[USAGE_CACHE_READ_INPUT_TOKENS] = cache_tokens
    if input_tokens is not None and cache_tokens is not None:
        result[USAGE_UNCACHED_INPUT_TOKENS] = max(0, input_tokens - cache_tokens)
    if search_queries is not None:
        result[GEMINI_USAGE_SEARCH_QUERIES] = search_queries
    if result:
        details = {
            GEMINI_USAGE_COST_ESTIMATE: (
                "estimated_from_reported_tokens; search_query_fees_added_when_reported"
            )
        }
        if tool_use_tokens is not None:
            details[GEMINI_USAGE_TOOL_USE_TOKENS] = tool_use_tokens
        result[USAGE_DETAILS] = details
    return result


def _gemini_cost_usd(usage: Mapping[str, Any]) -> float | None:
    pricing = _gemini_pricing(usage)
    token_cost = token_cost_usd(usage, pricing)
    reasoning_tokens = _int_or_none(usage.get(USAGE_REASONING_TOKENS))
    if (
        token_cost is not None
        and reasoning_tokens
        and pricing.output_tokens is not None
    ):
        token_cost += reasoning_tokens * pricing.output_tokens / 1_000_000
    search_queries = _int_or_none(usage.get(GEMINI_USAGE_SEARCH_QUERIES))
    search_cost = None
    if search_queries is not None:
        search_cost = search_queries * GEMINI_SEARCH_QUERY_USD
    if token_cost is None:
        return search_cost
    return token_cost + (search_cost or 0.0)


def _gemini_pricing(usage: Mapping[str, Any]) -> TokenPricing:
    input_tokens = _first_int(
        usage.get(USAGE_TOTAL_INPUT_TOKENS),
        usage.get(USAGE_INPUT_TOKENS),
    )
    if input_tokens is not None and input_tokens > GEMINI_CONTEXT_PRICE_BREAKPOINT_TOKENS:
        return GEMINI_STANDARD_HIGH_CONTEXT_PRICING
    return GEMINI_STANDARD_LOW_CONTEXT_PRICING


def _terminal_error(
    interaction_id: str,
    final_state: Mapping[str, Any],
) -> RelayError | None:
    status = str(final_state.get("status") or "unknown")
    if status == "completed":
        return None
    details = final_state.get("error") or final_state.get("incomplete_details")
    suffix = f": {json.dumps(details, sort_keys=True)}" if details else "."
    return RelayError(f"Gemini interaction {interaction_id} ended with status {status}{suffix}")


async def _request_with_retries(operation: Callable[[], Awaitable[Any]]) -> Any:
    for attempt in range(GEMINI_REQUEST_RETRY_ATTEMPTS):
        try:
            response = await operation()
            if _retryable_status(response.status_code):
                if attempt == GEMINI_REQUEST_RETRY_ATTEMPTS - 1:
                    _raise_for_gemini_status(response)
            else:
                _raise_for_gemini_status(response)
                return response
        except httpx.TransportError:
            if attempt == GEMINI_REQUEST_RETRY_ATTEMPTS - 1:
                raise
        await asyncio.sleep(
            min(
                GEMINI_REQUEST_RETRY_INITIAL_BACKOFF_SEC * (2**attempt),
                GEMINI_REQUEST_RETRY_MAX_BACKOFF_SEC,
            )
        )
    raise RelayError("Gemini request exhausted retries.")


def _raise_for_gemini_status(response: Any) -> None:
    if response.status_code < 400:
        return
    request = getattr(response, "request", None)
    url = getattr(request, "url", "unknown URL")
    body = _preview(str(getattr(response, "text", "")), limit=2_000)
    suffix = f": {body}" if body else "."
    raise RelayError(
        f"Gemini request failed with HTTP {response.status_code} for {url}{suffix}"
    )


def _retryable_status(status_code: int) -> bool:
    return status_code >= 500 or status_code in {408, 409, 425, 429}


def _retryable_poll_status(status_code: int) -> bool:
    return _retryable_status(status_code) or status_code in GEMINI_POLL_RETRY_STATUS_CODES


def _first_env(env: Mapping[str, str] | None, names: tuple[str, ...]) -> str | None:
    for source in (env or {}, os.environ):
        for name in names:
            value = source.get(name)
            if value:
                return value
    return None


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _first_int(*values: Any) -> int | None:
    for value in values:
        parsed = _int_or_none(value)
        if parsed is not None:
            return parsed
    return None


def _int_or_none(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    return int(value)
