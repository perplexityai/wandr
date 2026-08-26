"""Tests for is_retryable_anthropic_stream_error.

Run directly (PYTHONPATH=agents python agents/relay/providers/anthropic/test_events_retry.py)
or via pytest.
"""

import anthropic
import httpx

from relay.providers.anthropic.events import is_retryable_anthropic_stream_error

_REQUEST = httpx.Request("POST", "https://api.anthropic.com/v1/messages")


def test_timeout_is_retryable() -> None:
    error = anthropic.APITimeoutError(request=_REQUEST)
    assert is_retryable_anthropic_stream_error(error)


def test_connection_error_is_retryable() -> None:
    error = anthropic.APIConnectionError(message="boom", request=_REQUEST)
    assert is_retryable_anthropic_stream_error(error)


def test_bad_request_is_not_retryable() -> None:
    response = httpx.Response(status_code=400, request=_REQUEST)
    error = anthropic.BadRequestError(
        "bad request", response=response, body=None
    )
    assert not is_retryable_anthropic_stream_error(error)


def test_server_error_is_retryable() -> None:
    response = httpx.Response(status_code=500, request=_REQUEST)
    error = anthropic.InternalServerError(
        "server error", response=response, body=None
    )
    assert is_retryable_anthropic_stream_error(error)


if __name__ == "__main__":
    for name, func in sorted(globals().items()):
        if name.startswith("test_") and callable(func):
            func()
            print(f"PASS {name}")
