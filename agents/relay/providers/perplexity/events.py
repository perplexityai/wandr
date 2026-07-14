from collections.abc import Mapping
from typing import Any

from relay.core import (
    EVENT_TEXT,
    EVENT_TEXT_PREVIEW,
    RelayObserver,
    RelaySemanticType,
    TOOL_ARGUMENTS,
    TOOL_RESULT,
    TokenPricing,
    USAGE_CACHE_READ_INPUT_TOKENS,
    USAGE_INPUT_TOKENS,
    USAGE_OUTPUT_TOKENS,
    USAGE_REASONING_TOKENS,
    USAGE_TOTAL_INPUT_TOKENS,
    USAGE_TOTAL_TOKENS,
    USAGE_UNCACHED_INPUT_TOKENS,
    emit_event,
    log_fields,
    token_cost_usd,
)

PERPLEXITY_TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})
PERPLEXITY_TERMINAL_EVENTS = frozenset({"response.completed", "response.failed"})
_PERPLEXITY_PRICING: dict[str, TokenPricing] = {
    "openai/gpt-5.5": TokenPricing(
        uncached_input=1.25,
        cached_input=0.125,
        output_tokens=10.0,
    ),
}


def response_text_from_perplexity_output(response: Mapping[str, Any]) -> str:
    text = response.get("output_text")
    if isinstance(text, str):
        return text.strip()
    parts = [
        content["text"]
        for item in _list(response.get("output"))
        if _dict(item).get("type") == "message"
        for content in _list(_dict(item).get("content"))
        if isinstance(content, dict) and isinstance(content.get("text"), str)
    ]
    return "\n".join(parts).strip()


def perplexity_usage(response: Mapping[str, Any]) -> dict[str, Any]:
    usage = _dict(response.get("usage"))
    if not usage:
        return {}

    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    input_details = _dict(usage.get("input_tokens_details"))
    cache_read_input_tokens = int(input_details.get("cached_tokens") or 0)
    result: dict[str, Any] = {
        USAGE_INPUT_TOKENS: input_tokens,
        USAGE_TOTAL_INPUT_TOKENS: input_tokens,
        USAGE_UNCACHED_INPUT_TOKENS: max(0, input_tokens - cache_read_input_tokens),
        USAGE_OUTPUT_TOKENS: output_tokens,
        USAGE_TOTAL_TOKENS: int(usage.get("total_tokens") or 0),
        USAGE_CACHE_READ_INPUT_TOKENS: cache_read_input_tokens,
    }
    output_details = _dict(usage.get("output_tokens_details"))
    if output_details:
        result[USAGE_REASONING_TOKENS] = int(
            output_details.get("reasoning_tokens") or 0
        )
    return result


def perplexity_cost_usd(
    model_name: str,
    usage: dict[str, Any],
    response: Mapping[str, Any],
) -> float | None:
    cost = _dict(_dict(response.get("usage")).get("cost"))
    total = cost.get("total_cost")
    if total is not None:
        return float(total)
    return token_cost_usd(usage, _PERPLEXITY_PRICING.get(model_name))


def emit_perplexity_stream_event(
    event: Mapping[str, Any],
    *,
    response_id: str,
    observer: RelayObserver | None,
) -> None:
    event_type = str(event.get("type") or "")
    if event_type.endswith(".delta"):
        return
    if event_type == "error":
        return

    if event_type == "response.sandbox.created":
        emit_event(
            observer,
            "endpoint.tool_call",
            "Created Perplexity sandbox.",
            endpoint="perplexity",
            response_id=response_id,
            event_type=event_type,
            tool_type="sandbox",
            tool_name="sandbox",
            tool_call_id=event.get("container_id") or "sandbox",
            container_id=event.get("container_id"),
            domain=event.get("domain"),
            **log_fields(response_id=response_id, container_id=event.get("container_id")),
        )
        return

    if event_type == "response.sandbox.command":
        stdout = str(event.get("stdout") or "")
        code = str(event.get("code") or "")
        arguments = {
            "event_type": event_type,
            "tool_type": "sandbox",
            "input_preview": _preview(code),
        }
        result = {
            **arguments,
            "tool_name": "sandbox",
            "exit_code": event.get("exit_code"),
            "duration_ms": event.get("duration_ms"),
            "stdout_preview": _preview(stdout),
            "stdout_bytes": len(stdout.encode()),
        }
        emit_event(
            observer,
            "endpoint.tool_result",
            "Observed Perplexity sandbox command.",
            endpoint="perplexity",
            response_id=response_id,
            event_type=event_type,
            tool_type="sandbox",
            tool_name="sandbox",
            tool_call_id=event.get("container_id") or event.get("sequence_number"),
            container_id=event.get("container_id"),
            exit_code=event.get("exit_code"),
            duration_ms=event.get("duration_ms"),
            input_preview=_preview(code),
            stdout_preview=_preview(stdout),
            stdout_bytes=len(stdout.encode()),
            **log_fields(
                response_id=response_id,
                container_id=event.get("container_id"),
            ),
            **{
                TOOL_ARGUMENTS: arguments,
                TOOL_RESULT: result,
            },
        )
        return

    if event_type == "response.sandbox.results":
        _emit_sandbox_result(
            response_id,
            stream_event_key(event),
            event,
            observer,
            event_type=event_type,
        )
        return

    if event_type == "response.output_item.done":
        item = _dict(event.get("item"))
        if item.get("type") == "share_file":
            _emit_share_file(
                response_id,
                stream_event_key(event),
                item,
                observer,
                event_type=event_type,
            )
        return

    message = _event_message(event)
    if message is None:
        return

    semantic_type = _semantic_type(event_type)
    emit_event(
        observer,
        "endpoint.message",
        "Observed Perplexity event message.",
        semantic_type=semantic_type,
        endpoint="perplexity",
        response_id=response_id,
        event_type=event_type,
        **{
            EVENT_TEXT: message,
            EVENT_TEXT_PREVIEW: _preview(message),
        },
        text_bytes=len(message.encode()),
    )


def emit_perplexity_output_items(
    response: Mapping[str, Any],
    observed: set[str],
    observer: RelayObserver | None,
) -> None:
    response_id = str(response.get("id") or "")
    for index, item_value in enumerate(_list(response.get("output"))):
        item = _dict(item_value)
        item_type = str(item.get("type") or "")
        key = _output_item_key(item, index)
        if key in observed:
            continue
        observed.add(key)

        if item_type == "skill_loaded":
            _emit_skill_loaded(response_id, item, observer)
        elif item_type == "sandbox_results":
            _emit_sandbox_result(response_id, key, item, observer)
        elif item_type == "share_file":
            _emit_share_file(response_id, key, item, observer)
        elif message := _output_item_message(item):
            emit_event(
                observer,
                "endpoint.message",
                "Observed Perplexity output message.",
                endpoint="perplexity",
                response_id=response_id,
                event_type=item_type,
                **{
                    EVENT_TEXT: message,
                    EVENT_TEXT_PREVIEW: _preview(message),
                },
                text_bytes=len(message.encode()),
            )


def stream_event_key(event: Mapping[str, Any]) -> str:
    sequence_number = event.get("sequence_number")
    if isinstance(sequence_number, int):
        return f"seq:{sequence_number}"
    return repr(
        sorted(
            (key, str(value))
            for key, value in {
                "type": event.get("type"),
                "name": event.get("name"),
                "container_id": event.get("container_id"),
                "code": event.get("code"),
                "stdout": event.get("stdout"),
                "text": event.get("text"),
                "delta": event.get("delta"),
                "message": event.get("message"),
            }.items()
            if value
        )
    )


def mark_stream_observed_output_items(
    events: list[dict[str, Any]],
    observed: set[str],
) -> None:
    for event in events:
        if key := stream_observed_output_item_key(event):
            observed.add(key)


def stream_observed_output_item_key(event: Mapping[str, Any]) -> str | None:
    event_type = event.get("type")
    if event_type == "response.skill.loaded":
        return f"skill_loaded:{event.get('name') or ''}"
    if event_type == "response.output_text.done":
        text = event.get("text")
        return _message_key(text) if isinstance(text, str) and text.strip() else None
    if event_type == "response.sandbox.results" and event.get("call_id"):
        return str(event.get("call_id"))
    if event_type != "response.output_item.done":
        return None

    item = _dict(event.get("item"))
    if item.get("type") not in {"sandbox_results", "share_file"}:
        return None
    return _output_item_key(item, 0)


def _event_message(event: Mapping[str, Any]) -> str | None:
    for key in ("text", "delta", "stdout", "message"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    if event.get("type") == "response.skill.loaded":
        name = event.get("name")
        return f"Loaded skill {name}." if name else "Loaded skill."

    return None


def _output_item_key(item: Mapping[str, Any], index: int) -> str:
    item_type = str(item.get("type") or "")
    if item_type == "skill_loaded":
        return f"skill_loaded:{item.get('name') or ''}"
    if item_type == "message" and (message := _output_item_message(item)):
        return _message_key(message)
    return str(item.get("id") or item.get("call_id") or f"{item_type}:{index}")


def _message_key(text: str) -> str:
    return f"message:{text.strip()}"


def _emit_skill_loaded(
    response_id: str,
    item: Mapping[str, Any],
    observer: RelayObserver | None,
) -> None:
    name = item.get("name")
    message = f"Loaded skill {name}." if name else "Loaded skill."
    emit_event(
        observer,
        "endpoint.message",
        "Observed Perplexity skill load.",
        endpoint="perplexity",
        response_id=response_id,
        event_type="skill_loaded",
        text=message,
        text_preview=message,
        text_bytes=len(message.encode()),
    )


def _emit_sandbox_result(
    response_id: str,
    key: str,
    item: Mapping[str, Any],
    observer: RelayObserver | None,
    *,
    event_type: str = "sandbox_results",
) -> None:
    result = _dict(next(iter(_list(item.get("results"))), {}))
    stdout = str(result.get("stdout") or "")
    code = str(item.get("code") or "")
    arguments = {
        "event_type": event_type,
        "tool_type": "sandbox",
        "language": item.get("language"),
        "input_preview": _preview(code),
    }
    display_result = {
        **arguments,
        "tool_name": "sandbox",
        "status": result.get("status") or item.get("status"),
        "exit_code": result.get("exit_code"),
        "duration_ms": result.get("duration_ms"),
        "stdout_preview": _preview(stdout),
        "stdout_bytes": len(stdout.encode()),
    }
    emit_event(
        observer,
        "endpoint.tool_result",
        "Observed Perplexity sandbox result.",
        endpoint="perplexity",
        response_id=response_id,
        event_type=event_type,
        tool_type="sandbox",
        tool_name="sandbox",
        tool_call_id=item.get("call_id") or key,
        container_id=item.get("container_id"),
        language=item.get("language"),
        status=result.get("status") or item.get("status"),
        exit_code=result.get("exit_code"),
        duration_ms=result.get("duration_ms"),
        input_preview=_preview(code),
        stdout_preview=_preview(stdout),
        stdout_bytes=len(stdout.encode()),
        **log_fields(response_id=response_id, container_id=item.get("container_id")),
        **{
            TOOL_ARGUMENTS: arguments,
            TOOL_RESULT: display_result,
        },
    )


def _emit_share_file(
    response_id: str,
    key: str,
    item: Mapping[str, Any],
    observer: RelayObserver | None,
    *,
    event_type: str = "share_file",
) -> None:
    filename = item.get("filename") or item.get("name")
    file_id = item.get("file_id")
    error = item.get("error")
    success = bool(file_id)
    if success:
        message = "Observed Perplexity shared file."
    elif error:
        message = "Observed Perplexity share_file failure."
    else:
        message = "Observed Perplexity share_file attempt without file id."
    arguments = {
        "event_type": event_type,
        "tool_type": "share_file",
        "filename": filename,
        "file_id": file_id,
        "input_preview": filename,
    }
    if error:
        arguments["error"] = error
    result = {
        **arguments,
        "tool_name": "share_file",
        "size_bytes": item.get("size_bytes") or item.get("bytes"),
        "url": item.get("url"),
        "success": success,
    }
    emit_event(
        observer,
        "endpoint.tool_result",
        message,
        endpoint="perplexity",
        response_id=response_id,
        event_type=event_type,
        tool_type="share_file",
        tool_name="share_file",
        tool_call_id=item.get("call_id") or key,
        file_id=file_id,
        filename=filename,
        size_bytes=item.get("size_bytes") or item.get("bytes"),
        url=item.get("url"),
        input_preview=filename,
        success=success,
        **({"error": error} if error else {}),
        **log_fields(response_id=response_id, file_id=file_id),
        **{
            TOOL_ARGUMENTS: arguments,
            TOOL_RESULT: result,
        },
    )


def _output_item_message(item: Mapping[str, Any]) -> str | None:
    if item.get("type") != "message":
        return None
    parts = [
        content["text"]
        for content in _list(item.get("content"))
        if isinstance(content, dict) and isinstance(content.get("text"), str)
    ]
    text = "\n".join(parts).strip()
    return text or None


def _semantic_type(event_type: str) -> RelaySemanticType:
    if "reasoning" in event_type:
        return "reasoning"
    if "sandbox" in event_type or "tool" in event_type:
        return "tool_result"
    return "narration"


def _preview(value: Any, limit: int = 240) -> str:
    text = value if isinstance(value, str) else repr(value)
    normalized = " ".join(text.split())
    return normalized[:limit]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
