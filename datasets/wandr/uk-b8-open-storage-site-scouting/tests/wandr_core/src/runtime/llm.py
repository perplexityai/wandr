"""LLM request boundary. All pipeline LLM calls go through here."""

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any, NamedTuple

from pydantic import BaseModel

type Consumption = dict[str, int | None]

EMPTY_PARAMS: Mapping[str, Any] = MappingProxyType({})


class LLMRequest(NamedTuple):
    model: str
    system: str
    prompt: str
    response_format: type[BaseModel] | None = None
    max_completion_tokens: int = 1024
    params: Mapping[str, Any] = EMPTY_PARAMS


async def llm_completion(
    client: Any, request: LLMRequest
) -> tuple[dict[str, Any] | str | None, Consumption]:
    """Single LLM call. Returns (result, consumption).

    Structured (response_format is a BaseModel subclass):
        Returns (parsed.model_dump(), consumption) or (None, consumption).
    Unstructured (response_format is None):
        Returns (text, consumption).

    No try/except — errors propagate to the caller's @aexcepts.
    No retry — OpenAI SDK max_retries handles transport.
    """
    messages = [
        {"role": "system", "content": request.system},
        {"role": "user", "content": request.prompt},
    ]

    if request.response_format is not None:
        response = await client.beta.chat.completions.parse(
            model=request.model,
            messages=messages,
            response_format=request.response_format,
            max_completion_tokens=request.max_completion_tokens,
            **request.params,
        )
        parsed = response.choices[0].message.parsed
        result = parsed.model_dump() if parsed else None
    else:
        response = await client.chat.completions.create(
            model=request.model,
            messages=messages,
            max_completion_tokens=request.max_completion_tokens,
            **request.params,
        )
        result = (response.choices[0].message.content or "").strip()

    token_usage = response.usage
    consumption: Consumption = {
        "input_tokens": token_usage.prompt_tokens if token_usage else None,
        "output_tokens": token_usage.completion_tokens if token_usage else None,
    }
    return result, consumption
