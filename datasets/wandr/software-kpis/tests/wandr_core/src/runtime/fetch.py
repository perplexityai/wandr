"""Page-fetch client implemented through an Agent API sandbox relay."""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from perplexity import (
    APIConnectionError,
    APITimeoutError,
    AsyncPerplexity,
    InternalServerError,
    NotFoundError,
    RateLimitError,
)


logger = logging.getLogger(__name__)

FETCH_SCHEMA_VERSION = 1
FETCH_WORKSPACE = "/home/user/workspace"
DEFAULT_FETCH_MODEL = "google/gemini-3.1-flash-lite"
DEFAULT_FETCH_POLL_INTERVAL = 2.0
DEFAULT_FETCH_TIMEOUT = 540.0
DEFAULT_FETCH_REQUEST_TIMEOUT = 30.0
DEFAULT_FETCH_FILE_WAIT = 10.0
DEFAULT_FETCH_MAX_STEPS = 5
DEFAULT_FETCH_MAX_OUTPUT_TOKENS = 4096
DEFAULT_FETCH_HTTP_RETRIES = 2

_IN_PROGRESS_STATUSES = frozenset({"queued", "in_progress"})
_RETRYABLE_API_ERRORS = (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)
_CREATE_RECOVERY_ERRORS = (NotFoundError, *_RETRYABLE_API_ERRORS)
_PAGE_FIELDS = (
    "url",
    "title",
    "description",
    "author",
    "hostname",
    "published_date",
    "is_paywall",
    "content",
    "error",
)


class FetchError(RuntimeError):
    """A batch-wide failure inside one fetch invocation."""


@dataclass(slots=True)
class FetchPage:
    """Page shape consumed by ``components._parse_page``."""

    url: str
    title: str | None = None
    description: str | None = None
    author: str | None = None
    hostname: str | None = None
    published_date: str | None = None
    is_paywall: bool = False
    content: str | None = None
    error: str | None = None


@dataclass(slots=True)
class FetchResponse:
    """Page collection returned through the existing client contract."""

    pages: list[FetchPage]


def _env_float(env: Mapping[str, str], name: str, default: float) -> float:
    raw = env.get(name)
    if raw is None or raw == "":
        return default
    value = float(raw)
    if value <= 0:
        raise ValueError(f"{name} must be > 0")
    return value


def _env_int(env: Mapping[str, str], name: str, default: int) -> int:
    raw = env.get(name)
    if raw is None or raw == "":
        return default
    value = int(raw)
    if value < 1:
        raise ValueError(f"{name} must be >= 1")
    return value


def _field(value: Any, name: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        return value.get(name, default)
    return getattr(value, name, default)


def _string(value: Any) -> str | None:
    if value is None:
        return None
    return value if isinstance(value, str) else str(value)


def _build_prompt(
    *, attempt_id: str, artifact_path: str, artifact_name: str, urls: list[str]
) -> str:
    manifest = json.dumps({"urls": urls}, separators=(",", ":")).encode()
    manifest_b64 = base64.b64encode(manifest).decode()
    attempt_literal = json.dumps(attempt_id)
    artifact_literal = json.dumps(artifact_path)
    manifest_literal = json.dumps(manifest_b64)
    fields_literal = repr(_PAGE_FIELDS)

    return f"""Execute this deterministic fetch relay. Run exactly one Python sandbox command using the program below. Do not alter the URL manifest, fetch method, output path, or output schema.

```python
import base64
import json
import os
import pplx_sdk

ATTEMPT_ID = {attempt_literal}
ARTIFACT_PATH = {artifact_literal}
MANIFEST_B64 = {manifest_literal}
PAGE_FIELDS = {fields_literal}

urls = json.loads(base64.b64decode(MANIFEST_B64).decode("utf-8"))["urls"]
pages = []
batch_error = None
try:
    fetched = pplx_sdk.content.fetch(urls)
    for page in fetched:
        item = {{}}
        for field in PAGE_FIELDS:
            value = getattr(page, field, None)
            if value is None or isinstance(value, (str, int, float, bool)):
                item[field] = value
            else:
                item[field] = str(value)
        pages.append(item)
except Exception as exc:
    batch_error = {{"type": type(exc).__name__, "message": str(exc)}}

payload = {{
    "schema_version": {FETCH_SCHEMA_VERSION},
    "attempt_id": ATTEMPT_ID,
    "requested_urls": urls,
    "pages": pages,
    "batch_error": batch_error,
}}
temporary_path = ARTIFACT_PATH + ".tmp"
with open(temporary_path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))
os.replace(temporary_path, ARTIFACT_PATH)
print(json.dumps({{"artifact": ARTIFACT_PATH, "pages": len(pages), "batch_error": batch_error is not None}}))
```

After the command succeeds, call `share_file` exactly once with path `{artifact_path}` and name `{artifact_name}`. Do not print or quote the artifact contents. End with a brief delivery confirmation."""


class _ContentResource:
    """Page retrieval exposed through ``client.content``."""

    def __init__(self, client: FetchClient) -> None:
        self._client = client

    async def fetch(
        self,
        urls: list[str],
    ) -> FetchResponse:
        return await self._client._fetch(list(urls))


class FetchClient:
    """Expose page retrieval through the evaluator's client contract."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str = DEFAULT_FETCH_MODEL,
        poll_interval: float = DEFAULT_FETCH_POLL_INTERVAL,
        operation_timeout: float = DEFAULT_FETCH_TIMEOUT,
        request_timeout: float = DEFAULT_FETCH_REQUEST_TIMEOUT,
        file_wait_timeout: float = DEFAULT_FETCH_FILE_WAIT,
        max_steps: int = DEFAULT_FETCH_MAX_STEPS,
        max_output_tokens: int = DEFAULT_FETCH_MAX_OUTPUT_TOKENS,
        http_retries: int = DEFAULT_FETCH_HTTP_RETRIES,
        api_client: Any | None = None,
    ) -> None:
        if poll_interval <= 0:
            raise ValueError("poll_interval must be > 0")
        if operation_timeout <= 0 or request_timeout <= 0 or file_wait_timeout <= 0:
            raise ValueError("Fetch timeouts must be > 0")
        if max_steps < 1 or max_output_tokens < 1 or http_retries < 0:
            raise ValueError("Fetch limits must be positive")

        if api_client is None:
            if not api_key:
                raise RuntimeError("Fetch client requires PERPLEXITY_API_KEY")
            kwargs: dict[str, Any] = {
                "api_key": api_key,
                "max_retries": http_retries,
            }
            if base_url:
                kwargs["base_url"] = base_url
            api_client = AsyncPerplexity(**kwargs)

        self._api = api_client
        self._model = model
        self._poll_interval = poll_interval
        self._operation_timeout = operation_timeout
        self._request_timeout = request_timeout
        self._file_wait_timeout = file_wait_timeout
        self._max_steps = max_steps
        self._max_output_tokens = max_output_tokens
        self.content = _ContentResource(self)

    @classmethod
    def from_env(
        cls, env: Mapping[str, str] | None = None, **overrides: Any
    ) -> FetchClient:
        env = os.environ if env is None else env
        api_key = env.get("PERPLEXITY_API_KEY")
        kwargs: dict[str, Any] = {
            "api_key": api_key,
            "base_url": env.get("WANDR_FETCH_BASE_URL") or None,
            "model": env.get("WANDR_FETCH_MODEL") or DEFAULT_FETCH_MODEL,
            "poll_interval": _env_float(
                env,
                "WANDR_FETCH_POLL_INTERVAL_SEC",
                DEFAULT_FETCH_POLL_INTERVAL,
            ),
            "operation_timeout": _env_float(
                env,
                "WANDR_FETCH_TIMEOUT_SEC",
                DEFAULT_FETCH_TIMEOUT,
            ),
            "request_timeout": _env_float(
                env,
                "WANDR_FETCH_REQUEST_TIMEOUT_SEC",
                DEFAULT_FETCH_REQUEST_TIMEOUT,
            ),
            "file_wait_timeout": _env_float(
                env,
                "WANDR_FETCH_FILE_WAIT_SEC",
                DEFAULT_FETCH_FILE_WAIT,
            ),
            "max_steps": _env_int(
                env, "WANDR_FETCH_MAX_STEPS", DEFAULT_FETCH_MAX_STEPS
            ),
            "max_output_tokens": _env_int(
                env,
                "WANDR_FETCH_MAX_OUTPUT_TOKENS",
                DEFAULT_FETCH_MAX_OUTPUT_TOKENS,
            ),
            "http_retries": _env_int(
                env,
                "WANDR_FETCH_HTTP_ATTEMPTS",
                DEFAULT_FETCH_HTTP_RETRIES + 1,
            )
            - 1,
        }
        kwargs.update(overrides)
        return cls(**kwargs)

    async def close(self) -> None:
        close = getattr(self._api, "close", None)
        if close is not None:
            await close()

    async def __aenter__(self) -> FetchClient:
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.close()

    async def _fetch(self, urls: list[str]) -> FetchResponse:
        if not urls:
            raise ValueError("content.fetch requires at least one URL")

        attempt_id = str(uuid.uuid4())
        artifact_name = f"wandr-fetch-{attempt_id}.json"
        artifact_path = f"{FETCH_WORKSPACE}/{artifact_name}"
        prompt = _build_prompt(
            attempt_id=attempt_id,
            artifact_path=artifact_path,
            artifact_name=artifact_name,
            urls=urls,
        )
        logger.info(
            "fetch.started attempt_id=%s urls=%s",
            attempt_id,
            len(urls),
        )

        try:
            return await asyncio.wait_for(
                self._run_attempt(
                    attempt_id=attempt_id,
                    artifact_name=artifact_name,
                    prompt=prompt,
                    urls=urls,
                ),
                timeout=self._operation_timeout,
            )
        except TimeoutError as exc:
            raise FetchError(
                f"Fetch timed out after {self._operation_timeout:g}s"
            ) from exc

    async def _run_attempt(
        self,
        *,
        attempt_id: str,
        artifact_name: str,
        prompt: str,
        urls: list[str],
    ) -> FetchResponse:
        response = await self._create_response(attempt_id, prompt)
        response_id = _string(_field(response, "id"))
        if not response_id:
            raise FetchError("Agent response creation returned no id")

        response = await self._poll_response(response_id, response)
        status = _string(_field(response, "status")) or "unknown"
        if status != "completed":
            error = _field(response, "error")
            raise FetchError(
                f"Agent response {response_id} ended with status {status}: {error}"
            )

        payload = await self._download_artifact(response_id, artifact_name)
        result = self._parse_artifact(payload, attempt_id=attempt_id, urls=urls)
        usage = _field(response, "usage")
        cost = _field(_field(usage, "cost"), "total_cost")
        logger.info(
            "fetch.completed response_id=%s urls=%s pages=%s cost_usd=%s",
            response_id,
            len(urls),
            len(result.pages),
            cost,
        )
        return result

    async def _create_response(self, attempt_id: str, prompt: str) -> Any:
        response_id = f"resp_{attempt_id}"
        try:
            return await self._api.responses.create(
                model=self._model,
                input=prompt,
                tools=[{"type": "sandbox"}],
                background=True,
                max_steps=self._max_steps,
                max_output_tokens=self._max_output_tokens,
                reasoning={"effort": "low"},
                extra_headers={"X-Request-Id": attempt_id},
                timeout=self._request_timeout,
            )
        except _RETRYABLE_API_ERRORS as create_error:
            logger.warning(
                "fetch.create_uncertain response_id=%s error=%s",
                response_id,
                type(create_error).__name__,
            )
            try:
                return await self._api.responses.retrieve(
                    response_id, timeout=self._request_timeout
                )
            except _CREATE_RECOVERY_ERRORS:
                raise create_error

    async def _poll_response(self, response_id: str, response: Any) -> Any:
        status = _string(_field(response, "status")) or "unknown"
        while status in _IN_PROGRESS_STATUSES:
            await asyncio.sleep(self._poll_interval)
            try:
                response = await self._api.responses.retrieve(
                    response_id, timeout=self._request_timeout
                )
            except _RETRYABLE_API_ERRORS as exc:
                logger.warning(
                    "fetch.poll_retry response_id=%s error=%s",
                    response_id,
                    type(exc).__name__,
                )
                continue
            status = _string(_field(response, "status")) or "unknown"
        return response

    async def _download_artifact(self, response_id: str, artifact_name: str) -> bytes:
        loop = asyncio.get_running_loop()
        deadline = loop.time() + self._file_wait_timeout
        matching: list[Any] = []
        while not matching:
            try:
                listing = await self._api.responses.files.list(
                    response_id, timeout=self._request_timeout
                )
            except _CREATE_RECOVERY_ERRORS as exc:
                if loop.time() >= deadline:
                    raise FetchError(
                        f"Agent response {response_id} file listing failed"
                    ) from exc
                logger.warning(
                    "fetch.file_list_retry response_id=%s error=%s",
                    response_id,
                    type(exc).__name__,
                )
                await asyncio.sleep(self._poll_interval)
                continue
            matching = [
                item
                for item in (_field(listing, "data", []) or [])
                if _field(item, "filename") == artifact_name
            ]
            if matching or loop.time() >= deadline:
                break
            await asyncio.sleep(self._poll_interval)

        if not matching:
            raise FetchError(
                f"Agent response {response_id} shared no {artifact_name} artifact"
            )

        file_id = _string(_field(matching[-1], "id"))
        if not file_id:
            raise FetchError(
                f"Agent response {response_id} returned an artifact without an id"
            )
        deadline = loop.time() + self._file_wait_timeout
        while True:
            try:
                content = await self._api.responses.files.content(
                    file_id,
                    response_id=response_id,
                    timeout=self._request_timeout,
                )
                return await content.read()
            except _CREATE_RECOVERY_ERRORS as exc:
                if loop.time() >= deadline:
                    raise FetchError(
                        f"Agent response {response_id} artifact download failed"
                    ) from exc
                logger.warning(
                    "fetch.file_download_retry response_id=%s file_id=%s error=%s",
                    response_id,
                    file_id,
                    type(exc).__name__,
                )
                await asyncio.sleep(self._poll_interval)

    @staticmethod
    def _parse_artifact(
        raw: bytes, *, attempt_id: str, urls: list[str]
    ) -> FetchResponse:
        try:
            payload = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
            raise FetchError("Fetch artifact is not valid JSON") from exc

        if not isinstance(payload, dict):
            raise FetchError("Fetch artifact must be a JSON object")
        if payload.get("schema_version") != FETCH_SCHEMA_VERSION:
            raise FetchError("Fetch artifact has an unsupported schema")
        if payload.get("attempt_id") != attempt_id:
            raise FetchError("Fetch artifact attempt id does not match")
        if payload.get("requested_urls") != urls:
            raise FetchError("Fetch artifact URL manifest does not match")
        if batch_error := payload.get("batch_error"):
            raise FetchError(f"Sandbox fetch failed: {batch_error}")

        raw_pages = payload.get("pages")
        if not isinstance(raw_pages, list):
            raise FetchError("Fetch artifact pages must be a list")

        pages: list[FetchPage] = []
        for raw_page in raw_pages:
            if not isinstance(raw_page, dict):
                raise FetchError("Fetch artifact contains a non-object page")
            pages.append(
                FetchPage(
                    url=_string(raw_page.get("url")) or "",
                    title=_string(raw_page.get("title")),
                    description=_string(raw_page.get("description")),
                    author=_string(raw_page.get("author")),
                    hostname=_string(raw_page.get("hostname")),
                    published_date=_string(raw_page.get("published_date")),
                    is_paywall=bool(raw_page.get("is_paywall", False)),
                    content=_string(raw_page.get("content")),
                    error=_string(raw_page.get("error")),
                )
            )
        return FetchResponse(pages=pages)
