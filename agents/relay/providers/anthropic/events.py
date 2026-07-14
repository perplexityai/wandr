import json
from typing import Any

import httpx

from relay.core import (
    EVENT_TEXT,
    EVENT_TEXT_PREVIEW,
    RelayError,
    RelayObserver,
    RelaySemanticType,
    TOOL_ARGUMENTS,
    TOOL_RESULT,
    USAGE_CACHE_READ_INPUT_TOKENS,
    USAGE_DETAILS,
    USAGE_INPUT_TOKENS,
    USAGE_OUTPUT_TOKENS,
    USAGE_TOTAL_INPUT_TOKENS,
    USAGE_UNCACHED_INPUT_TOKENS,
    emit_event,
    log_fields,
)

_ANTHROPIC_CACHE_CREATION_5M_INPUT_TOKENS = "cache_creation_5m_input_tokens"
_ANTHROPIC_CACHE_CREATION_1H_INPUT_TOKENS = "cache_creation_1h_input_tokens"
_ANTHROPIC_PRICING: dict[str, dict[str, float]] = {
    "claude-opus-4-7": {
        USAGE_UNCACHED_INPUT_TOKENS: 5.0,
        USAGE_CACHE_READ_INPUT_TOKENS: 0.5,
        _ANTHROPIC_CACHE_CREATION_5M_INPUT_TOKENS: 6.25,
        _ANTHROPIC_CACHE_CREATION_1H_INPUT_TOKENS: 10.0,
        USAGE_OUTPUT_TOKENS: 25.0,
    },
    "claude-opus-4-8": {
        USAGE_UNCACHED_INPUT_TOKENS: 5.0,
        USAGE_CACHE_READ_INPUT_TOKENS: 0.5,
        _ANTHROPIC_CACHE_CREATION_5M_INPUT_TOKENS: 6.25,
        _ANTHROPIC_CACHE_CREATION_1H_INPUT_TOKENS: 10.0,
        USAGE_OUTPUT_TOKENS: 25.0,
    },
}


class AnthropicSessionExhaustedError(RelayError):
    """Managed Agents ended the current turn after exhausting its retry budget."""


def dump_anthropic_model(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        dumped = value.model_dump(mode="json", warnings="none")
        return dumped if isinstance(dumped, dict) else {}
    if hasattr(value, "to_dict"):
        dumped = value.to_dict()
        return dumped if isinstance(dumped, dict) else {}
    return value if isinstance(value, dict) else {}


async def list_anthropic_events(
    client: Any,
    session_id: str,
    *,
    beta: str,
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    paginator = client.beta.sessions.events.list(
        session_id,
        order="asc",
        limit=100,
        betas=[beta],
    )
    async for event in paginator:
        events.append(dump_anthropic_model(event))
    return events


def merge_anthropic_events(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
) -> None:
    index_by_id = {
        event_id: index
        for index, event in enumerate(existing)
        if (event_id := event.get("id"))
    }
    for event in incoming:
        event_id = event.get("id")
        if event_id and event_id in index_by_id:
            _merge_event_details(existing[index_by_id[event_id]], event)
            continue
        existing.append(event)
        if event_id:
            index_by_id[event_id] = len(existing) - 1


def emit_anthropic_tool_calls(
    observer: RelayObserver | None,
    session_id: str,
    event_data: dict[str, Any],
    observed_tool_call_ids: set[str],
) -> None:
    if event_data.get("type") == "agent.tool_use":
        tool_call_id = str(event_data.get("id") or "agent.tool_use")
        if tool_call_id in observed_tool_call_ids:
            return
        observed_tool_call_ids.add(tool_call_id)
        emit_event(
            observer,
            "endpoint.tool_call",
            "Observed Anthropic managed-agent tool call.",
            endpoint="anthropic-managed",
            session_id=session_id,
            event_id=event_data.get("id"),
            event_type=event_data.get("type"),
            tool_type=event_data.get("type"),
            tool_name=event_data.get("name"),
            tool_call_id=tool_call_id,
            input_preview=_preview(event_data.get("input")),
            **log_fields(session_id=session_id, tool_name=event_data.get("name")),
            **{
                TOOL_ARGUMENTS: {
                    "event_type": event_data.get("type"),
                    "tool_type": event_data.get("type"),
                    "input_preview": _preview(event_data.get("input")),
                }
            },
        )
        return

    event_id = event_data.get("id")
    for index, block in enumerate(_list(event_data.get("content")), start=1):
        if not isinstance(block, dict):
            continue
        if block.get("type") not in {"server_tool_use", "tool_use"}:
            continue
        tool_call_id = str(block.get("id") or f"{event_id or 'event'}:{index}")
        if tool_call_id in observed_tool_call_ids:
            continue
        observed_tool_call_ids.add(tool_call_id)
        emit_event(
            observer,
            "endpoint.tool_call",
            "Observed Anthropic managed-agent tool call.",
            endpoint="anthropic-managed",
            session_id=session_id,
            event_id=event_id,
            event_type=event_data.get("type"),
            tool_type=block.get("type"),
            tool_name=block.get("name"),
            tool_call_id=tool_call_id,
            input_preview=_preview(block.get("input")),
            **log_fields(session_id=session_id, tool_name=block.get("name")),
            **{
                TOOL_ARGUMENTS: {
                    "event_type": event_data.get("type"),
                    "tool_type": block.get("type"),
                    "input_preview": _preview(block.get("input")),
                }
            },
        )


def is_retryable_anthropic_stream_error(error: BaseException) -> bool:
    if isinstance(error, httpx.TransportError):
        return True
    status_code = getattr(error, "status_code", None)
    if isinstance(status_code, int):
        return status_code in {408, 409, 429} or status_code >= 500
    return type(error).__name__ in {"APIConnectionError", "APIStatusError"}


def is_anthropic_session_complete(
    session_id: str,
    events: list[dict[str, Any]],
) -> bool:
    terminal, error = anthropic_session_terminal_state(session_id, events)
    if error is not None:
        raise error
    return terminal


def is_anthropic_session_terminal(
    session_id: str,
    events: list[dict[str, Any]],
) -> bool:
    terminal, _error = anthropic_session_terminal_state(session_id, events)
    return terminal


def anthropic_session_terminal_error(
    session_id: str,
    events: list[dict[str, Any]],
) -> RelayError | None:
    _terminal, error = anthropic_session_terminal_state(session_id, events)
    return error


def anthropic_session_terminal_state(
    session_id: str,
    events: list[dict[str, Any]],
) -> tuple[bool, RelayError | None]:
    for event in reversed(events):
        event_type = event.get("type")
        if event_type == "session.status_idle":
            stop_reason = _dict(event.get("stop_reason")).get("type")
            if stop_reason == "requires_action":
                return True, RelayError(
                    f"Anthropic session {session_id} requires action."
                )
            if stop_reason == "retries_exhausted":
                return True, AnthropicSessionExhaustedError(
                    f"Anthropic session {session_id} ended with retries_exhausted."
                )
            return (
                stop_reason == "end_turn" and bool(anthropic_agent_messages(events)),
                None,
            )
        if event_type == "session.error":
            retry_status = _anthropic_error_retry_status(event)
            if retry_status == "retrying":
                return False, None
            if retry_status == "exhausted":
                return True, AnthropicSessionExhaustedError(
                    f"Anthropic session {session_id} exhausted managed-agent "
                    f"retry budget: {event.get('error')}"
                )
            return True, RelayError(
                f"Anthropic session {session_id} error: {event.get('error')}"
            )
        if event_type in {"session.status_terminated", "session.deleted"}:
            return True, RelayError(f"Anthropic session {session_id} terminated.")
        if event_type in {"session.status_rescheduled", "session.status_running"}:
            return False, None
    return False, None


def latest_anthropic_idle_stop_reason(events: list[dict[str, Any]]) -> str | None:
    for event in reversed(events):
        if event.get("type") != "session.status_idle":
            continue
        stop_reason = _dict(event.get("stop_reason"))
        value = stop_reason.get("type")
        return value if isinstance(value, str) else None
    return None


def anthropic_agent_messages(events: list[dict[str, Any]]) -> list[str]:
    messages: list[str] = []
    for event in events:
        if event.get("type") != "agent.message":
            continue
        chunks = [
            block["text"]
            for block in _list(event.get("content"))
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        ]
        if chunks:
            messages.append("".join(chunks))
    return messages


def anthropic_output_text(events: list[dict[str, Any]]) -> str:
    return "\n".join(anthropic_agent_messages(events))


def anthropic_usage(
    session: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    usage = _dict(session.get("usage"))
    if usage:
        cache_creation = _dict(usage.get("cache_creation"))
        input_tokens = int(usage.get("input_tokens") or 0)
        output_tokens = int(usage.get("output_tokens") or 0)
        cache_read_input_tokens = int(usage.get("cache_read_input_tokens") or 0)
        cache_creation_5m_input_tokens = int(
            cache_creation.get("ephemeral_5m_input_tokens") or 0
        )
        cache_creation_1h_input_tokens = int(
            cache_creation.get("ephemeral_1h_input_tokens") or 0
        )
        return {
            USAGE_INPUT_TOKENS: input_tokens,
            USAGE_TOTAL_INPUT_TOKENS: (
                input_tokens
                + cache_read_input_tokens
                + cache_creation_5m_input_tokens
                + cache_creation_1h_input_tokens
            ),
            USAGE_UNCACHED_INPUT_TOKENS: input_tokens,
            USAGE_OUTPUT_TOKENS: output_tokens,
            USAGE_CACHE_READ_INPUT_TOKENS: cache_read_input_tokens,
            USAGE_DETAILS: {
                _ANTHROPIC_CACHE_CREATION_5M_INPUT_TOKENS: (
                    cache_creation_5m_input_tokens
                ),
                _ANTHROPIC_CACHE_CREATION_1H_INPUT_TOKENS: (
                    cache_creation_1h_input_tokens
                ),
            },
        }

    total = {USAGE_INPUT_TOKENS: 0, USAGE_OUTPUT_TOKENS: 0}
    for event in events:
        model_usage = _dict(event.get("model_usage"))
        total[USAGE_INPUT_TOKENS] += int(model_usage.get("input_tokens") or 0)
        total[USAGE_OUTPUT_TOKENS] += int(model_usage.get("output_tokens") or 0)
    return {
        **total,
        USAGE_TOTAL_INPUT_TOKENS: total[USAGE_INPUT_TOKENS],
        USAGE_UNCACHED_INPUT_TOKENS: total[USAGE_INPUT_TOKENS],
    }


def anthropic_cost_usd(model_name: str, usage: dict[str, Any]) -> float | None:
    pricing = _ANTHROPIC_PRICING.get(model_name)
    if pricing is None:
        return None

    details = _dict(usage.get(USAGE_DETAILS))
    line_items = (
        (
            _usage_count(usage, USAGE_UNCACHED_INPUT_TOKENS),
            pricing[USAGE_UNCACHED_INPUT_TOKENS],
        ),
        (
            _usage_count(usage, USAGE_CACHE_READ_INPUT_TOKENS),
            pricing[USAGE_CACHE_READ_INPUT_TOKENS],
        ),
        (
            _usage_count(details, _ANTHROPIC_CACHE_CREATION_5M_INPUT_TOKENS),
            pricing[_ANTHROPIC_CACHE_CREATION_5M_INPUT_TOKENS],
        ),
        (
            _usage_count(details, _ANTHROPIC_CACHE_CREATION_1H_INPUT_TOKENS),
            pricing[_ANTHROPIC_CACHE_CREATION_1H_INPUT_TOKENS],
        ),
        (_usage_count(usage, USAGE_OUTPUT_TOKENS), pricing[USAGE_OUTPUT_TOKENS]),
    )
    return sum(tokens * price / 1_000_000 for tokens, price in line_items)


def anthropic_event_meat(event: dict[str, Any]) -> dict[str, Any]:
    event_type = event.get("type")
    if event_type == "agent.tool_use":
        input_preview = _preview(event.get("input"))
        return {
            "tool_name": event.get("name"),
            "input_preview": input_preview,
            TOOL_ARGUMENTS: {
                "event_type": event_type,
                "tool_type": event_type,
                "input_preview": input_preview,
            },
        }

    chunks = [
        block["text"] if isinstance(block, dict) else block
        for block in _list(event.get("content"))
        if (
            isinstance(block, str)
            or (isinstance(block, dict) and isinstance(block.get("text"), str))
        )
    ]
    text = "".join(chunks)
    if (
        event_type in {"agent.message", "agent.thinking", "agent.tool_result"}
        and text.strip()
    ):
        meat: dict[str, Any] = {
            EVENT_TEXT: text,
            EVENT_TEXT_PREVIEW: _preview(text),
            "text_bytes": len(text.encode()),
        }
        if event_type == "agent.tool_result":
            meat[TOOL_RESULT] = text
        return meat
    return {}


def anthropic_event_semantic_type(event: dict[str, Any]) -> RelaySemanticType:
    return {
        "agent.message": "narration",
        "agent.thinking": "reasoning",
        "agent.tool_result": "tool_result",
        "agent.tool_use": "tool_call",
    }.get(str(event.get("type") or ""), "lifecycle")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _usage_count(usage: dict[str, Any], key: str) -> int:
    value = usage.get(key)
    if value is None or isinstance(value, bool):
        return 0
    return int(value)


def _anthropic_error_retry_status(event: dict[str, Any]) -> str | None:
    error = _dict(event.get("error"))
    retry_status = _dict(error.get("retry_status"))
    value = retry_status.get("type")
    return value if isinstance(value, str) else None


def _preview(value: Any, limit: int = 500) -> str | None:
    if value in (None, "", [], {}):
        return None
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    return " ".join(text.split())[:limit]


def _merge_event_details(
    existing: dict[str, Any],
    incoming: dict[str, Any],
) -> None:
    for key, value in incoming.items():
        if value in (None, [], {}):
            continue
        existing[key] = value
