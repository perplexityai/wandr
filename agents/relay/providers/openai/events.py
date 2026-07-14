from typing import Any

from relay.core import (
    EVENT_TEXT,
    EVENT_TEXT_PREVIEW,
    RelayObserver,
    RelaySemanticType,
    TOOL_ARGUMENTS,
    TokenPricing,
    USAGE_CACHE_READ_INPUT_TOKENS,
    USAGE_INPUT_TOKENS,
    USAGE_OUTPUT_TOKENS,
    USAGE_TOTAL_INPUT_TOKENS,
    USAGE_TOTAL_TOKENS,
    USAGE_UNCACHED_INPUT_TOKENS,
    emit_event,
    log_fields,
    token_cost_usd,
)

OAI_TOOL_ITEM_TYPES = frozenset(
    {"code_interpreter_call", "shell_call", "web_search_call"}
)
_OPENAI_PRICING: dict[str, TokenPricing] = {
    "gpt-5.5": TokenPricing(
        uncached_input=1.25,
        cached_input=0.125,
        output_tokens=10.0,
    ),
}


def dump_openai_model(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        dumped = value.model_dump(mode="json", warnings="none")
        return dumped if isinstance(dumped, dict) else {}
    if hasattr(value, "to_dict"):
        dumped = value.to_dict()
        return dumped if isinstance(dumped, dict) else {}
    return value if isinstance(value, dict) else {}


def openai_field(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def openai_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def response_text_from_openai_output(output: Any) -> str:
    parts = [
        text
        for item in openai_list(output)
        if openai_field(item, "type") == "message"
        for content in openai_list(openai_field(item, "content"))
        if isinstance(text := openai_field(content, "text"), str)
    ]
    return "\n".join(parts).strip()


def emit_openai_tool_calls(
    response: Any,
    observer: RelayObserver | None = None,
    observed_tool_call_ids: set[str] | None = None,
) -> None:
    observed = set() if observed_tool_call_ids is None else observed_tool_call_ids
    for index, item in enumerate(openai_list(openai_field(response, "output"))):
        item_type = openai_field(item, "type")
        if item_type not in OAI_TOOL_ITEM_TYPES:
            continue

        preview = _tool_call_preview(item)
        if item_type == "web_search_call" and preview is None:
            continue

        call_id = openai_field(item, "call_id") or openai_field(item, "id") or index
        if str(call_id) in observed:
            continue
        observed.add(str(call_id))

        metadata = {
            "endpoint": "openai",
            "response_id": openai_field(response, "id"),
            "tool_type": item_type,
            "tool_name": _openai_tool_name(str(item_type)),
            "tool_call_id": call_id,
            TOOL_ARGUMENTS: _tool_arguments(item_type, preview=preview),
        }
        container_id = openai_field(item, "container_id")
        if container_id:
            metadata["container_id"] = container_id
        metadata.update(
            log_fields(response_id=metadata["response_id"], container_id=container_id)
        )
        if preview:
            metadata["input_preview"] = preview
        emit_event(
            observer,
            "endpoint.tool_call",
            "Observed OpenAI tool call.",
            **metadata,
        )


def emit_openai_stream_tool_call(
    event_data: dict[str, Any],
    response_id: str,
    observed_tool_call_ids: set[str],
    observer: RelayObserver | None = None,
) -> None:
    item = _dict(event_data.get("item"))
    item_type = item.get("type")
    if item_type not in OAI_TOOL_ITEM_TYPES:
        return

    preview = _tool_call_preview(item)
    if item_type in {"shell_call", "web_search_call"} and preview is None:
        return

    call_id = str(
        item.get("call_id")
        or item.get("id")
        or event_data.get("output_index")
        or event_data.get("sequence_number")
        or "stream_tool_call"
    )
    if call_id in observed_tool_call_ids:
        return
    observed_tool_call_ids.add(call_id)

    metadata = {
        "endpoint": "openai",
        "response_id": response_id or event_data.get("response_id"),
        "event_type": event_data.get("type"),
        "tool_type": item_type,
        "tool_name": _openai_tool_name(str(item_type)),
        "tool_call_id": call_id,
        TOOL_ARGUMENTS: _tool_arguments(
            item_type,
            event_type=event_data.get("type"),
            preview=preview,
        ),
    }
    container_id = item.get("container_id")
    if container_id:
        metadata["container_id"] = container_id
    metadata.update(
        log_fields(response_id=metadata["response_id"], container_id=container_id)
    )
    if preview:
        metadata["input_preview"] = preview
    emit_event(
        observer,
        "endpoint.tool_call",
        "Observed OpenAI tool call.",
        **metadata,
    )


def emit_openai_stream_message(
    event_data: dict[str, Any],
    response_id: str,
    buffers: dict[tuple[str, str], list[str]],
    observer: RelayObserver | None = None,
    *,
    sequence_number: int | None = None,
    status: str | None = None,
) -> tuple[str, str] | None:
    message = _stream_message(event_data)
    if message is None:
        return None

    key = (
        message["kind"],
        str(
            event_data.get("item_id")
            or event_data.get("output_index")
            or event_data.get("content_index")
            or event_data.get("summary_index")
            or "0"
        ),
    )
    event_type = str(event_data.get("type") or "")
    if event_type.endswith(".delta"):
        delta = event_data.get("delta")
        if isinstance(delta, str):
            buffers.setdefault(key, []).append(delta)
        return None

    text = _done_text(event_data) or "".join(buffers.pop(key, []))
    if not text.strip():
        return None

    metadata = {
        "endpoint": "openai",
        "response_id": response_id or event_data.get("response_id"),
        "event_type": event_type,
        "item_type": message["item_type"],
        EVENT_TEXT: text,
        EVENT_TEXT_PREVIEW: _preview(text),
        "text_bytes": len(text.encode()),
    }
    if sequence_number is not None:
        metadata["sequence_number"] = sequence_number
    if status:
        metadata["status"] = status
    emit_event(
        observer,
        "endpoint.message",
        message["description"],
        semantic_type=message["semantic_type"],
        **metadata,
    )
    return key


def emit_openai_output_messages(
    response: Any,
    observer: RelayObserver | None = None,
    observed_message_keys: set[tuple[str, str]] | None = None,
) -> None:
    observed = set() if observed_message_keys is None else observed_message_keys
    response_id = openai_field(response, "id")
    for index, item in enumerate(openai_list(openai_field(response, "output"))):
        item_type = openai_field(item, "type")
        item_key = str(openai_field(item, "id") or index)
        if item_type == "message":
            _emit_final_message(
                response_id,
                ("output_text", item_key),
                response,
                _message_item_text(item),
                observer,
                observed,
            )
        if item_type == "reasoning":
            for summary_index, summary in enumerate(
                openai_list(openai_field(item, "summary"))
            ):
                _emit_final_message(
                    response_id,
                    ("reasoning_summary", f"{item_key}:{summary_index}"),
                    response,
                    openai_field(summary, "text"),
                    observer,
                    observed,
                    semantic_type="reasoning",
                    item_type="reasoning",
                    description="Received OpenAI reasoning summary.",
                )


def openai_usage(response: Any) -> dict[str, Any]:
    usage = openai_field(response, "usage")
    if usage is None:
        return {}
    input_tokens = int(openai_field(usage, "input_tokens", 0) or 0)
    output_tokens = int(openai_field(usage, "output_tokens", 0) or 0)
    cache_read_input_tokens = int(
        openai_field(
            openai_field(usage, "input_tokens_details", {}),
            "cached_tokens",
            0,
        )
        or 0
    )
    return {
        USAGE_INPUT_TOKENS: input_tokens,
        USAGE_TOTAL_INPUT_TOKENS: input_tokens,
        USAGE_UNCACHED_INPUT_TOKENS: max(0, input_tokens - cache_read_input_tokens),
        USAGE_OUTPUT_TOKENS: output_tokens,
        USAGE_TOTAL_TOKENS: int(openai_field(usage, "total_tokens", 0) or 0),
        USAGE_CACHE_READ_INPUT_TOKENS: cache_read_input_tokens,
    }


def openai_cost_usd(model_name: str, usage: dict[str, Any]) -> float | None:
    return token_cost_usd(usage, _OPENAI_PRICING.get(model_name))


def openai_stream_sequence_number(event_data: dict[str, Any]) -> int | None:
    sequence_number = event_data.get("sequence_number")
    if isinstance(sequence_number, bool):
        return None
    if isinstance(sequence_number, int):
        return sequence_number
    if isinstance(sequence_number, str) and sequence_number.isdecimal():
        return int(sequence_number)
    return None


def openai_stream_response_id(
    event_data: dict[str, Any],
    response: Any,
) -> str | None:
    item = _dict(event_data.get("item"))
    for value in (
        openai_field(response, "id"),
        event_data.get("response_id"),
        item.get("response_id"),
    ):
        if isinstance(value, str) and value:
            return value
    return None


def openai_stream_response_status(response: Any) -> str | None:
    status = openai_field(response, "status")
    return status if isinstance(status, str) and status else None


def openai_event_semantic_type(event_data: dict[str, Any]) -> RelaySemanticType:
    event_type = str(event_data.get("type") or "")
    item_type = _dict(event_data.get("item")).get("type")
    if event_type.startswith("response.reasoning_summary"):
        return "reasoning"
    if event_type.startswith("response.output_text"):
        return "narration"
    if item_type in OAI_TOOL_ITEM_TYPES:
        return "tool_call"
    if _event_tool_type(event_type) is not None:
        return "tool_result" if event_type.endswith(".completed") else "tool_call"
    return "lifecycle"


def openai_event_meat(event_data: dict[str, Any]) -> dict[str, Any]:
    meat: dict[str, Any] = {}
    event_type = str(event_data.get("type") or "")
    delta = event_data.get("delta")
    if isinstance(delta, str) and delta.strip():
        meat[EVENT_TEXT] = delta
        meat[EVENT_TEXT_PREVIEW] = _preview(delta)
        meat["text_bytes"] = len(delta.encode())

    item = _dict(event_data.get("item"))
    item_type = item.get("type") or _event_tool_type(event_type)
    if isinstance(item_type, str) and item_type:
        meat["item_type"] = item_type
        if item_type in OAI_TOOL_ITEM_TYPES:
            meat["tool_type"] = item_type
            meat["tool_name"] = _openai_tool_name(item_type)
            meat[TOOL_ARGUMENTS] = _tool_arguments(item_type)
    preview = _tool_call_preview(item)
    if not preview and isinstance(delta, str) and item_type in OAI_TOOL_ITEM_TYPES:
        preview = _preview(delta)
    if preview:
        meat["input_preview"] = preview
        if isinstance(meat.get(TOOL_ARGUMENTS), dict):
            meat[TOOL_ARGUMENTS]["input_preview"] = preview

    response = _dict(event_data.get("response"))
    output = response.get("output")
    if isinstance(output, list):
        meat["output_count"] = len(output)
    return meat


def _stream_message(event_data: dict[str, Any]) -> dict[str, Any] | None:
    event_type = str(event_data.get("type") or "")
    if event_type.startswith("response.reasoning_summary_text."):
        return {
            "kind": "reasoning_summary",
            "item_type": "reasoning",
            "semantic_type": "reasoning",
            "description": "Received OpenAI reasoning summary.",
        }
    if event_type.startswith("response.output_text."):
        return {
            "kind": "output_text",
            "item_type": "message",
            "semantic_type": "narration",
            "description": "Received OpenAI output text.",
        }
    if event_type.startswith("response.code_interpreter_call_code."):
        return {
            "kind": "code_interpreter_code",
            "item_type": "code_interpreter_call",
            "semantic_type": "tool_call",
            "description": "Received OpenAI code interpreter code.",
        }
    return None


def _done_text(event_data: dict[str, Any]) -> str | None:
    for key in ("text", "delta"):
        value = event_data.get(key)
        if isinstance(value, str):
            return value
    return None


def _emit_final_message(
    response_id: Any,
    key: tuple[str, str],
    response: Any,
    text: Any,
    observer: RelayObserver | None,
    observed: set[tuple[str, str]],
    *,
    semantic_type: RelaySemanticType = "narration",
    item_type: str = "message",
    description: str = "Received OpenAI output text.",
) -> None:
    if key in observed or not isinstance(text, str) or not text.strip():
        return
    observed.add(key)
    emit_event(
        observer,
        "endpoint.message",
        description,
        semantic_type=semantic_type,
        endpoint="openai",
        response_id=response_id,
        status=openai_field(response, "status"),
        item_type=item_type,
        source="final_response",
        text_bytes=len(text.encode()),
        **{
            EVENT_TEXT: text,
            EVENT_TEXT_PREVIEW: _preview(text),
        },
    )


def _message_item_text(item: Any) -> str:
    parts = [
        text
        for content in openai_list(openai_field(item, "content"))
        if isinstance(text := openai_field(content, "text"), str)
    ]
    return "\n".join(parts).strip()


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _openai_tool_name(item_type: str) -> str:
    return {
        "code_interpreter_call": "code_interpreter",
        "shell_call": "shell",
        "web_search_call": "web_search",
    }[item_type]


def _tool_arguments(
    item_type: Any,
    *,
    event_type: Any = None,
    preview: str | None = None,
) -> dict[str, Any]:
    arguments = {"tool_type": item_type}
    if event_type is not None:
        arguments["event_type"] = event_type
    if preview:
        arguments["input_preview"] = preview
    return arguments


def _tool_call_preview(item: Any, limit: int = 500) -> str | None:
    action = openai_field(item, "action")
    for value in (
        openai_field(item, "code"),
        openai_field(item, "input"),
        openai_field(action, "commands"),
        openai_field(action, "query"),
    ):
        if _empty(value):
            continue
        text = value if isinstance(value, str) else str(value)
        return _preview(text, limit=limit)
    if not _empty(action) and not _empty(openai_field(action, "type")):
        text = action if isinstance(action, str) else str(action)
        return _preview(text, limit=limit)
    return None


def _empty(value: Any) -> bool:
    if value in (None, "", [], {}):
        return True
    if isinstance(value, dict):
        return all(_empty(item) for item in value.values())
    return False


def _event_tool_type(event_type: str) -> str | None:
    if event_type.startswith("response.code_interpreter_call"):
        return "code_interpreter_call"
    if event_type.startswith("response.shell_call"):
        return "shell_call"
    if event_type.startswith("response.web_search_call"):
        return "web_search_call"
    return None


def _preview(value: str, limit: int = 500) -> str:
    return " ".join(value.split())[:limit]
