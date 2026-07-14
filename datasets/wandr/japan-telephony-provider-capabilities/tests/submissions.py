"""Submission manifest parsing and workspace input discovery."""

from __future__ import annotations

import json
import re
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any, TypedDict


MANIFEST_JSON = Path(__file__).resolve().parent / "manifest.json"
TASK_NAME_RE = re.compile(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*")
MANIFEST_FIELDS = frozenset({"name", "wandr_task", "task_names"})


class Manifest(TypedDict):
    document: dict[str, Any]
    task_name: str
    task_names: tuple[str, ...]


class SubmissionInputs(TypedDict):
    rows_by_task: dict[str, int]
    paths_by_task: dict[str, Path]


def _submission_filename(task_name: str) -> str:
    return f"results_{task_name}.jsonl"


def _task_name(value: Any, *, field_name: str) -> str:
    task_name = value if isinstance(value, str) else ""
    if not TASK_NAME_RE.fullmatch(task_name):
        raise ValueError(
            f"{field_name} must be a dotted filename-safe WANDR task name: {task_name!r}"
        )
    return task_name


def _string(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string: {value!r}")
    return value


def _object(value: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object: {value!r}")
    return value


def _duplicates(values: Iterable[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def _task_names(value: Any, *, root_task_name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"task_names must be a list: {value!r}")
    task_names = tuple(
        _task_name(item, field_name=f"task_names[{index}]") for index, item in enumerate(value)
    )
    if not task_names:
        raise ValueError("task_names must not be empty")
    if duplicates := _duplicates(task_names):
        raise ValueError(f"WANDR manifest has duplicate task_names: {duplicates}")
    if task_names[0] != root_task_name:
        raise ValueError("wandr_task must be the first task_names entry")
    prefix = f"{root_task_name}."
    unrelated = [name for name in task_names[1:] if not name.startswith(prefix)]
    if unrelated:
        raise ValueError(f"WANDR manifest task_names are outside {root_task_name!r}: {unrelated}")
    return task_names


def _submission_paths(manifest: Manifest, workspace_dir: Path) -> dict[str, Path]:
    return {
        task_name: workspace_dir / _submission_filename(task_name)
        for task_name in manifest["task_names"]
    }


def validate_tasks(manifest: Manifest, task_names: Iterable[str]) -> None:
    actual = tuple(task_names)
    if duplicates := _duplicates(actual):
        raise ValueError(f"WANDR task config has duplicate task names: {duplicates}")
    expected = manifest["task_names"]
    if actual != expected:
        raise ValueError(
            f"WANDR manifest task mismatch: configured={list(actual)}, manifest={list(expected)}"
        )


def _jsonl_count(path: Path) -> int:
    # This runs before uv enters the WANDR environment; keep it stdlib-only.
    row_count = 0
    with path.open() as jsonl_file:
        for line_number, line in enumerate(jsonl_file, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number} invalid JSON: {exc.msg}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number} must be a JSON object")
            row_count += 1
    return row_count


def submission_inputs(manifest: Manifest, workspace_dir: Path) -> SubmissionInputs:
    paths = _submission_paths(manifest, workspace_dir)
    if missing := [str(path) for path in paths.values() if not path.is_file()]:
        raise FileNotFoundError(f"Missing expected WANDR submission files: {missing}")
    rows_by_task = {task: _jsonl_count(path) for task, path in paths.items()}
    if empty := [task for task, row_count in rows_by_task.items() if row_count < 1]:
        raise ValueError(f"WANDR submission files must not be empty: {empty}")
    return {"rows_by_task": rows_by_task, "paths_by_task": paths}


def load_manifest(path: str | Path = MANIFEST_JSON) -> Manifest:
    path = Path(path)
    try:
        document = _object(json.loads(path.read_text()), field_name="manifest")
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} invalid JSON: {exc.msg}") from exc
    if unknown := sorted(set(document) - MANIFEST_FIELDS):
        raise ValueError(f"WANDR manifest has unknown fields: {unknown}")
    missing = sorted(MANIFEST_FIELDS - set(document))
    if missing:
        raise ValueError(f"WANDR manifest is missing fields: {missing}")

    root_task_name = _task_name(document["wandr_task"], field_name="wandr_task")
    _string(document["name"], field_name="name")
    return {
        "document": document,
        "task_name": root_task_name,
        "task_names": _task_names(document["task_names"], root_task_name=root_task_name),
    }
