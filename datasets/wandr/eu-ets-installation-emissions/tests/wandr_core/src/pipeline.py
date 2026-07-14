"""WANDR eval pipeline — two-lane stream graph over submitted JSONL outputs."""

import asyncio
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from src.components import (
    BROWSER_REPLAY_JSONL,
    BROWSER_URL_CACHE_JSONL,
    CANON_ENTITY_CACHE_JSONL,
    CANON_REPLAY_JSONL,
    DEBUG_DIR_NAME,
    DEDUP_REPLAY_JSONL,
    FETCH_REPLAY_JSONL,
    FETCH_URL_CACHE_JSONL,
    JUDGE_EVAL_CACHE_JSONL,
    JUDGE_REPLAY_JSONL,
    SUBMISSION_REPLAY_JSONL,
    TRIAGE_REPLAY_JSONL,
    TRIAGE_URL_CACHE_JSONL,
    assemble_page_text,
    browser_fetch,
    converge_group,
    dns_check,
    fetch_pages,
    make_canon,
    make_dedup,
    make_judge,
    make_triage,
)
from src.config import (
    TaskConfig,
    extract_raw_key,
    record_base_id,
)
from src.runtime.clients import (
    create_browser_pool,
    create_fetch_pool,
    create_openai_pool,
)
from src.runtime.flow import (
    buffer,
    explode,
    fan_in,
    fan_out,
    flatten,
    observe,
    spread,
    tee,
    transform,
)
from src.runtime.modifiers import (
    batched,
    dispatched,
    dropping,
    persisted,
    projected,
)
from src.runtime.node import (
    node,
    run_node,
)
from src.runtime.progress import ProgressTracker
from src.runtime.types import Record
from src.runtime.utils import (
    drain_queue,
    init_run,
    stable_hash,
)
from src.submissions import (
    SUBMISSION_RECORDS_FIELD,
    load_submission,
    normalize_submission_paths,
    run_fingerprint,
    submission_count,
    submission_record_provenance,
    submission_replay_provenance,
    submission_records,
    submission_scope,
    seed_submissions,
    submission_subtrees,
)


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    value = int(raw)
    if value < 1:
        raise ValueError(f"{name} must be >= 1")
    return value


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


SUBMISSION_CONCURRENCY = _env_int("WANDR_SUBMISSION_CONCURRENCY", 25)
FETCH_CONCURRENCY = _env_int("WANDR_FETCH_CONCURRENCY", 50)
DNS_CONCURRENCY = _env_int("WANDR_DNS_CONCURRENCY", FETCH_CONCURRENCY)
FETCH_BATCH_SIZE = _env_int("WANDR_FETCH_BATCH_SIZE", 25)
FETCH_CLIENT_LOAD = _env_int("WANDR_FETCH_CLIENT_LOAD", 25)
TRIAGE_CONCURRENCY = _env_int("WANDR_TRIAGE_CONCURRENCY", 50)
TRIAGE_CLIENT_LOAD = _env_int("WANDR_TRIAGE_CLIENT_LOAD", 25)
BROWSER_CONCURRENCY = _env_int("WANDR_BROWSER_CONCURRENCY", 4)
BROWSER_FALLBACK = _env_bool("WANDR_BROWSER_FALLBACK", False)
CANON_CONCURRENCY = _env_int("WANDR_CANON_CONCURRENCY", 20)
CANON_CLIENT_LOAD = _env_int("WANDR_CANON_CLIENT_LOAD", 25)
DEDUP_CONCURRENCY = _env_int("WANDR_DEDUP_CONCURRENCY", 10)
DEDUP_CLIENT_LOAD = _env_int("WANDR_DEDUP_CLIENT_LOAD", 25)
DEDUP_BUFFER_TTL = _env_int("WANDR_DEDUP_BUFFER_TTL", 180)
JUDGE_CONCURRENCY = _env_int("WANDR_JUDGE_CONCURRENCY", 50)
JUDGE_CLIENT_LOAD = _env_int("WANDR_JUDGE_CLIENT_LOAD", 25)
CONVERGENCE_TTL = _env_int("WANDR_CONVERGENCE_TTL", 300)
CONVERGENCE_TTL_RETRIES = _env_int("WANDR_CONVERGENCE_TTL_RETRIES", 10_000)


async def run_pipeline(
    task_roots: list[TaskConfig],
    output_dir: Path,
    *,
    submission_paths: Mapping[str, Path],
) -> list[Record]:
    subtrees = submission_subtrees(task_roots)
    submission_paths = normalize_submission_paths(subtrees, submission_paths)
    # Replay caches live under <output_dir>/debug/, separate from durable
    # run outputs such as reports and metrics files.
    debug_dir = output_dir / DEBUG_DIR_NAME
    debug_dir.mkdir(parents=True, exist_ok=True)
    init_run()

    configs = {task.name: task for _, subtree in subtrees for task in subtree}
    task_names_by_root_key = dict(
        reversed(
            [
                ((task_root.name, key_name), task_names)
                for task_root, subtree in subtrees
                for task in subtree
                for key_name, task_names in task.task_names_by_key.items()
            ]
        )
    )
    dedup_group_counts_by_root = {
        task_root.name: sum(
            1 for root_name, _ in task_names_by_root_key if root_name == task_root.name
        )
        for task_root, _ in subtrees
    }

    # ── Fingerprints / graph keys ─────────────────────────

    triage_fps = {name: config.eval.triage.fingerprint for name, config in configs.items()}
    canon_fps = {
        (name, key_name): config.eval.canon.keys_resolved[key_name].fingerprint
        for name, config in configs.items()
        for key_name in (key_spec.name for key_spec in config.key_hierarchy)
    }
    dedup_fps = {
        (name, key_name): config.eval.dedup.keys_resolved[key_name].fingerprint
        for name, config in configs.items()
        for key_name in (key_spec.name for key_spec in config.key_hierarchy)
    }
    judge_fps = {name: config.eval.judge.fingerprint for name, config in configs.items()}

    def fetch_lane_replay_id(record: Record) -> tuple[Any, ...]:
        return (
            *run_fingerprint(record),
            *record_base_id(record, configs[record["_task"]].key_hierarchy),
        )

    def entity_lane_replay_id(record: Record) -> tuple[Any, ...]:
        return (
            *fetch_lane_replay_id(record),
            record.get("_key_name", ""),
            record.get("_key_value_raw", ""),
        )

    def judge_lane_replay_id(record: Record) -> tuple[Any, ...]:
        return (
            *fetch_lane_replay_id(record),
            stable_hash(record.get("page_text", "")),
            stable_hash(record.get("_dedup_aka", {})),
        )

    def triage_cache_key(record: Record) -> tuple[str, str]:
        return (triage_fps.get(record.get("_task", ""), ""), record.get("url", ""))

    def canon_cache_key(record: Record) -> tuple[str, ...]:
        return (
            canon_fps.get((record.get("_task", ""), record.get("_key_name", "")), ""),
            record.get("_key_value_raw", ""),
        )

    def dedup_cache_key(record: Record) -> tuple[Any, ...]:
        first = (record.get("_members", []) or [{}])[0]
        return (
            dedup_fps.get((first.get("_task", ""), first.get("_key_name", "")), ""),
            record.get("_dedgroup_fp", ""),
        )

    def judge_cache_key(record: Record) -> tuple[Any, ...]:
        return (
            judge_fps.get(record.get("_task", ""), ""),
            *record_base_id(record, configs[record["_task"]].key_hierarchy),
            stable_hash(record.get("page_text", "")),
            stable_hash(record.get("_dedup_aka", {})),
        )

    def judge_replay_provenance(record: Record) -> Record:
        return submission_record_provenance(record) | {
            "_dedup_clusters": record.get("_dedup_clusters", {})
        }

    def entity_lane_expected_size(record: Record) -> int:
        counts = record.get("_record_counts", {}) or {}
        return sum(
            counts.get(task_name, 0) * len(configs[task_name].key_hierarchy) for task_name in counts
        )

    def dedup_expected_groups(record: Record) -> int:
        return dedup_group_counts_by_root.get(record.get("_task", ""), 0)

    def task_name(record: Record) -> str:
        return record.get("_task", "")

    def member_task_name(record: Record) -> str:
        return (record.get("_members") or [{}])[0].get("_task", "")

    def triage_route_key(record: Record) -> str:
        return "usable" if record.get("_triage", {}).get("usable") else "browser"

    def entity_spread_key(record: Record) -> list[tuple[str, Any]]:
        return [
            (key_spec.name, extract_raw_key(record, key_spec))
            for key_spec in configs[record["_task"]].key_hierarchy
        ]

    def dedup_buffer_key(record: Record) -> tuple[str, str, str]:
        return (*submission_scope(record), record.get("_key_name", ""))

    def dedup_group_fingerprint(members: list[Record]) -> str:
        return stable_hash(
            sorted(
                {
                    (
                        member.get("_key_value_raw", ""),
                        member.get("_canon", {}).get("canonical", ""),
                    )
                    for member in members
                }
            )
        )

    def dedup_expected_size(record: Record) -> int:
        record_counts = record.get("_record_counts", {}) or {}
        return sum(
            record_counts.get(task_name, 0)
            for task_name in task_names_by_root_key[
                (record.get("_task_root", ""), record.get("_key_name", ""))
            ]
        )

    # ── Nodes ─────────────────────────────────────────────

    triage_dispatch = dispatched(
        {name: make_triage(config.eval.triage) for name, config in configs.items()},
        by=task_name,
    )
    canon_dispatch = {name: make_canon(config.eval.canon) for name, config in configs.items()}
    dedup_dispatch = {name: make_dedup(config.eval.dedup) for name, config in configs.items()}
    judge_dispatch = {name: make_judge(config.eval.judge) for name, config in configs.items()}

    async def browser_fallback_disabled(_client: Any, _record: Record) -> None:
        return None

    browser_component = browser_fetch if BROWSER_FALLBACK else browser_fallback_disabled
    browser_pool_factory = create_browser_pool if BROWSER_FALLBACK else None

    nodes = {
        "submission": node(
            "submission",
            persisted(
                load_submission,
                key=run_fingerprint,
                path=debug_dir / SUBMISSION_REPLAY_JSONL,
                flush_period=1,
                provenance=submission_replay_provenance,
            ),
            concurrency=SUBMISSION_CONCURRENCY,
        ),
        "dns": node(
            "dns",
            projected(dns_check, key="url"),
            concurrency=DNS_CONCURRENCY,
        ),
        "fetch": node(
            "fetch",
            persisted(
                projected(
                    persisted(
                        batched(fetch_pages, size=FETCH_BATCH_SIZE),
                        key="url",
                        path=debug_dir / FETCH_URL_CACHE_JSONL,
                    ),
                    key="url",
                ),
                key=fetch_lane_replay_id,
                path=debug_dir / FETCH_REPLAY_JSONL,
            ),
            concurrency=FETCH_CONCURRENCY,
            client_pool_factory=create_fetch_pool,
            client_load=FETCH_CLIENT_LOAD,
        ),
        "triage": node(
            "triage",
            persisted(
                dropping(
                    projected(
                        persisted(
                            triage_dispatch,
                            key=triage_cache_key,
                            path=debug_dir / TRIAGE_URL_CACHE_JSONL,
                        ),
                        key=triage_cache_key,
                    ),
                    fields=["_consumption_triage"],
                ),
                key=fetch_lane_replay_id,
                path=debug_dir / TRIAGE_REPLAY_JSONL,
            ),
            concurrency=TRIAGE_CONCURRENCY,
            client_pool_factory=create_openai_pool,
            client_load=TRIAGE_CLIENT_LOAD,
        ),
        "browser": node(
            "browser",
            persisted(
                projected(
                    persisted(
                        browser_component,
                        key="url",
                        path=debug_dir / BROWSER_URL_CACHE_JSONL,
                        flush_period=1,
                    ),
                    key="url",
                ),
                key=fetch_lane_replay_id,
                path=debug_dir / BROWSER_REPLAY_JSONL,
                flush_period=1,
            ),
            concurrency=BROWSER_CONCURRENCY,
            client_pool_factory=browser_pool_factory,
        ),
        "canon": node(
            "canon",
            persisted(
                dropping(
                    projected(
                        persisted(
                            dispatched(canon_dispatch, by=task_name),
                            key=canon_cache_key,
                            path=debug_dir / CANON_ENTITY_CACHE_JSONL,
                        ),
                        key=canon_cache_key,
                    ),
                    fields=["_consumption_canon"],
                ),
                key=entity_lane_replay_id,
                path=debug_dir / CANON_REPLAY_JSONL,
            ),
            concurrency=CANON_CONCURRENCY,
            client_pool_factory=create_openai_pool,
            client_load=CANON_CLIENT_LOAD,
        ),
        "dedup": node(
            "dedup",
            persisted(
                dispatched(dedup_dispatch, by=member_task_name),
                key=dedup_cache_key,
                path=debug_dir / DEDUP_REPLAY_JSONL,
                flush_period=1,
            ),
            concurrency=DEDUP_CONCURRENCY,
            client_pool_factory=create_openai_pool,
            client_load=DEDUP_CLIENT_LOAD,
        ),
        "judge": node(
            "judge",
            persisted(
                dropping(
                    projected(
                        persisted(
                            dispatched(judge_dispatch, by=task_name),
                            key=judge_cache_key,
                            path=debug_dir / JUDGE_EVAL_CACHE_JSONL,
                        ),
                        key=judge_cache_key,
                    ),
                    fields=["_consumption_judge"],
                ),
                key=judge_lane_replay_id,
                path=debug_dir / JUDGE_REPLAY_JSONL,
                provenance=judge_replay_provenance,
            ),
            concurrency=JUDGE_CONCURRENCY,
            client_pool_factory=create_openai_pool,
            client_load=JUDGE_CLIENT_LOAD,
        ),
    }

    # ── Queues ────────────────────────────────────────────

    # Queue sizing: keep these unbounded on Python 3.12. On failure, a node's
    # `finally` path still has to publish its sentinel; with a bounded queue,
    # that can block forever if the downstream consumer already died. Python
    # 3.13's Queue.shutdown() gives bounded queues a clean failure path.
    queues: dict[str, asyncio.Queue[Record | None]] = {
        name: asyncio.Queue()
        for name in (
            "submission_inp",
            "submission_out",
            "record_stream",
            "observed_stream",
            "dns_inp",
            "entity_inp",
            "fetch_inp",
            "triage_inp",
            "post_triage",
            "usable_raw",
            "usable_out",
            "browser_raw",
            "browser_inp",
            "browser_out",
            "fetch_merged",
            "canon_inp",
            "canon_out",
            "dedup_buf_out",
            "dedup_out",
            "entity_out",
            "conv_inp",
            "conv_out",
            "judge_inp",
            "judge_out",
        )
    }

    # ── Feed ──────────────────────────────────────────────

    seed_submissions(queues["submission_inp"], subtrees, submission_paths)

    # ── Progress ──────────────────────────────────────────

    tracker = ProgressTracker()
    bars = {
        "submission": tracker.register("submission", total=len(task_roots)),
        "dns": tracker.register("dns"),
        "fetch": tracker.register("fetch"),
        "triage": tracker.register("triage"),
        "browser": tracker.register("browser"),
        "canon": tracker.register("canon"),
        "dedup": tracker.register("dedup"),
        "judge": tracker.register("judge"),
    }

    common_work = {
        bars["dns"]: submission_count,
        bars["fetch"]: submission_count,
        bars["triage"]: submission_count,
        bars["judge"]: submission_count,
        bars["canon"]: entity_lane_expected_size,
        bars["dedup"]: dedup_expected_groups,
    }

    async def count_common_work(record: Record | None) -> None:
        if record is None:
            for bar in common_work:
                await bar.finalize_total()
            return
        for bar, count in common_work.items():
            if n := count(record):
                await bar.add_expected(n)

    async def count_browser_work(record: Record | None) -> None:
        if record is None:
            await bars["browser"].finalize_total()
        else:
            await bars["browser"].add_expected(1)

    # ── Run ───────────────────────────────────────────────

    async def _pipeline() -> None:
        graph = (
            # Submission lane: tee into entity and fetch lanes
            run_node(
                nodes["submission"],
                queues["submission_inp"],
                queues["submission_out"],
                progress=bars["submission"],
            ),
            observe(queues["submission_out"], queues["record_stream"], count_common_work),
            explode(
                queues["record_stream"],
                queues["observed_stream"],
                items=submission_records,
                label=None,
                drop_sources=[SUBMISSION_RECORDS_FIELD],
            ),
            tee(queues["observed_stream"], queues["dns_inp"], queues["entity_inp"]),
            # Fetch lane
            run_node(
                nodes["dns"],
                queues["dns_inp"],
                queues["fetch_inp"],
                progress=bars["dns"],
            ),
            run_node(
                nodes["fetch"],
                queues["fetch_inp"],
                queues["triage_inp"],
                progress=bars["fetch"],
            ),
            run_node(
                nodes["triage"],
                queues["triage_inp"],
                queues["post_triage"],
                progress=bars["triage"],
            ),
            fan_out(
                queues["post_triage"],
                route=triage_route_key,
                queues={
                    "usable": queues["usable_raw"],
                    "browser": queues["browser_raw"],
                },
            ),
            transform(queues["usable_raw"], queues["usable_out"], assemble_page_text),
            observe(queues["browser_raw"], queues["browser_inp"], count_browser_work),
            run_node(
                nodes["browser"],
                queues["browser_inp"],
                queues["browser_out"],
                progress=bars["browser"],
            ),
            fan_in([queues["usable_out"], queues["browser_out"]], queues["fetch_merged"]),
            # Entity lane
            spread(
                queues["entity_inp"],
                queues["canon_inp"],
                into="_key_name",
                value="_key_value_raw",
                over=entity_spread_key,
            ),
            run_node(
                nodes["canon"],
                queues["canon_inp"],
                queues["canon_out"],
                progress=bars["canon"],
            ),
            # allow_late_arrivals: fractured dedup (partial batch flushes
            # via TTL, then late records form a new group) is a quality
            # degradation (fewer cross-record comparisons), not data loss.
            buffer(
                queues["canon_out"],
                queues["dedup_buf_out"],
                key=dedup_buffer_key,
                expected_size=dedup_expected_size,
                ttl=DEDUP_BUFFER_TTL,
                flush_incomplete=True,
                allow_late_arrivals=True,
                fingerprint=dedup_group_fingerprint,
                fingerprint_field="_dedgroup_fp",
            ),
            run_node(
                nodes["dedup"],
                queues["dedup_buf_out"],
                queues["dedup_out"],
                progress=bars["dedup"],
            ),
            flatten(queues["dedup_out"], queues["entity_out"]),
            # Convergence merges fetch-lane (page_text) and entity-lane
            # (canon/dedup annotations) records. TTL + high retries: entity-
            # only groups retry every CONVERGENCE_TTL seconds until the fetch
            # record arrives (flush_incomplete checks for page_text). Sentinel
            # overrides retries and force-flushes everything.
            # allow_late_arrivals: entity records arriving after convergence
            # emit late groups that get sentinel-flushed. Memory cost is bounded
            # by total record count.
            fan_in([queues["fetch_merged"], queues["entity_out"]], queues["conv_inp"]),
            buffer(
                queues["conv_inp"],
                queues["conv_out"],
                key=fetch_lane_replay_id,
                expected_size=lambda record: 1 + len(configs[record["_task"]].key_hierarchy),
                ttl=CONVERGENCE_TTL,
                flush_incomplete=lambda members: any(member.get("page_text") for member in members),
                ttl_retries=CONVERGENCE_TTL_RETRIES,
                allow_late_arrivals=True,
                fingerprint=None,
            ),
            transform(queues["conv_out"], queues["judge_inp"], converge_group),
            run_node(
                nodes["judge"],
                queues["judge_inp"],
                queues["judge_out"],
                progress=bars["judge"],
            ),
        )
        try:
            async with asyncio.TaskGroup() as task_group:
                for coro in graph:
                    task_group.create_task(coro)
        finally:
            tracker.stop()

    await asyncio.gather(tracker.run(), _pipeline())
    return drain_queue(queues["judge_out"])
