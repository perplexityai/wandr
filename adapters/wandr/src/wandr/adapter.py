#!/usr/bin/env python3
"""Stamp a WANDR task source tree into Harbor task layout."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
PACKAGE_DIR = Path(__file__).resolve().parent
ORIGIN_DIR = PACKAGE_DIR / "origin"
REFERENCE_TASKS_DIR = REPO_ROOT / "reference" / "wandr_tasks"
TASK_TEMPLATE_DIR = PACKAGE_DIR / "task-template"
WANDR_CORE_DIR = ORIGIN_DIR / "wandr_core"
WANDR_CORE_DEPS_FILES = ("pyproject.toml", "uv.lock")
TASK_NAME_RE = re.compile(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*")

if str(WANDR_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(WANDR_CORE_DIR))

from src.config import (  # noqa: E402
    flatten_tasks,
    instruction_bindings,
    instruction_tree,
    load_task_config,
)
from src.markup import bind, expand  # noqa: E402

from .utils.consistency import DATASET_DIR, update_dataset_manifest  # noqa: E402
from .utils.source_files import ignore_source_files  # noqa: E402


def _ignore(_dir: str, names: list[str]) -> set[str]:
    return ignore_source_files(_dir, names)


def _copytree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, ignore=_ignore)


def _copy_wandr_core_deps(dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for name in WANDR_CORE_DEPS_FILES:
        shutil.copy2(WANDR_CORE_DIR / name, dst / name)


def _slug(task_name: str) -> str:
    return task_name.replace("_", "-")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8")


def _load_config(task_name: str, output_dir: Path) -> Any:
    _clear_task_source_modules()
    task_dir = output_dir / "tests" / "wandr_task"
    return load_task_config(task_name, task_dir)


def _clear_task_source_modules() -> None:
    """Drop task-local imports before loading another WANDR task in-process."""
    for name, module in list(sys.modules.items()):
        paths = []
        module_file = getattr(module, "__file__", None)
        if module_file:
            paths.append(Path(module_file))
        module_path = getattr(module, "__path__", None)
        if module_path:
            paths.extend(Path(path) for path in module_path)
        if any(_is_task_source_path(path) for path in paths):
            sys.modules.pop(name, None)


def _is_task_source_path(path: Path) -> bool:
    parts = path.parts
    return "wandr_task" in parts or ("reference" in parts and "wandr_tasks" in parts)


def _render_instruction(config: Any) -> str:
    macro = _read_text(ORIGIN_DIR / "instruction_macro.md.jinja")
    bindings = instruction_bindings(config, isolate_bindings={"url"})
    expanded = expand(
        macro,
        task_tree=instruction_tree(config, isolate_bindings={"url"}),
        instruction_section_template="",
        share_bindings=bindings,
    )
    return bind(expanded, bindings)


def _validated_task_names(task_name: str, task_names: list[str]) -> list[str]:
    if not task_names:
        raise ValueError(f"WANDR task {task_name!r} has no configured task nodes")
    invalid = [name for name in task_names if not TASK_NAME_RE.fullmatch(name)]
    if invalid:
        raise ValueError(f"WANDR task {task_name!r} has invalid task node names: {invalid}")
    if len(set(task_names)) != len(task_names):
        raise ValueError(f"WANDR task {task_name!r} has duplicate task node names")
    if task_names[0] != task_name:
        raise ValueError(f"WANDR task {task_name!r} must be the first configured task node")
    prefix = f"{task_name}."
    unrelated = [name for name in task_names[1:] if not name.startswith(prefix)]
    if unrelated:
        raise ValueError(f"WANDR task {task_name!r} has task nodes outside its tree: {unrelated}")
    return list(task_names)


def _required_file_paths(task_names: list[str]) -> list[str]:
    if not task_names:
        raise ValueError("task names must not be empty")
    return [f"results_{task_name}.jsonl" for task_name in task_names]


def _write_manifest(
    output_dir: Path,
    *,
    task_name: str,
    task_names: list[str],
) -> list[str]:
    task_names = _validated_task_names(task_name, task_names)
    required_file_paths = _required_file_paths(task_names)
    manifest = {
        "name": _slug(task_name),
        "wandr_task": task_name,
        "task_names": task_names,
    }
    (output_dir / "tests" / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    return required_file_paths


VERIFIER_ENV_TOML = """[verifier.env]
OPENAI_API_KEY = "${OPENAI_API_KEY:-}"
PERPLEXITY_API_KEY = "${PERPLEXITY_API_KEY:-}"
WANDR_FETCH_BASE_URL = "${WANDR_FETCH_BASE_URL:-}"
WANDR_FETCH_MODEL = "${WANDR_FETCH_MODEL:-google/gemini-3.1-flash-lite}"
WANDR_FETCH_TIMEOUT_SEC = "${WANDR_FETCH_TIMEOUT_SEC:-540}"
WANDR_FETCH_REQUEST_TIMEOUT_SEC = "${WANDR_FETCH_REQUEST_TIMEOUT_SEC:-30}"
WANDR_FETCH_POLL_INTERVAL_SEC = "${WANDR_FETCH_POLL_INTERVAL_SEC:-2}"
WANDR_FETCH_FILE_WAIT_SEC = "${WANDR_FETCH_FILE_WAIT_SEC:-10}"
WANDR_FETCH_MAX_STEPS = "${WANDR_FETCH_MAX_STEPS:-5}"
WANDR_FETCH_MAX_OUTPUT_TOKENS = "${WANDR_FETCH_MAX_OUTPUT_TOKENS:-4096}"
WANDR_FETCH_HTTP_ATTEMPTS = "${WANDR_FETCH_HTTP_ATTEMPTS:-3}"
WANDR_HEAL_RETRIES = "${WANDR_HEAL_RETRIES:-9}"
WANDR_DNS_CONCURRENCY = "${WANDR_DNS_CONCURRENCY:-8}"
WANDR_FETCH_CONCURRENCY = "${WANDR_FETCH_CONCURRENCY:-16}"
WANDR_FETCH_BATCH_SIZE = "${WANDR_FETCH_BATCH_SIZE:-16}"
WANDR_FETCH_CLIENT_LOAD = "${WANDR_FETCH_CLIENT_LOAD:-16}"
WANDR_TRIAGE_CONCURRENCY = "${WANDR_TRIAGE_CONCURRENCY:-16}"
WANDR_TRIAGE_CLIENT_LOAD = "${WANDR_TRIAGE_CLIENT_LOAD:-16}"
WANDR_BROWSER_FALLBACK = "${WANDR_BROWSER_FALLBACK:-0}"
WANDR_BROWSER_CONCURRENCY = "${WANDR_BROWSER_CONCURRENCY:-1}"
WANDR_CANON_CONCURRENCY = "${WANDR_CANON_CONCURRENCY:-6}"
WANDR_CANON_CLIENT_LOAD = "${WANDR_CANON_CLIENT_LOAD:-6}"
WANDR_DEDUP_CONCURRENCY = "${WANDR_DEDUP_CONCURRENCY:-3}"
WANDR_DEDUP_CLIENT_LOAD = "${WANDR_DEDUP_CLIENT_LOAD:-3}"
WANDR_JUDGE_CONCURRENCY = "${WANDR_JUDGE_CONCURRENCY:-16}"
WANDR_JUDGE_CLIENT_LOAD = "${WANDR_JUDGE_CLIENT_LOAD:-16}"
"""


def _write_task_toml(
    output_dir: Path,
    *,
    task_name: str,
    required_file_paths: list[str],
) -> None:
    slug = _slug(task_name)
    required_file_paths_toml = _required_file_paths_toml(required_file_paths)
    value = f'''schema_version = "1.1"

[task]
name = "wandr/{slug}"
description = "WANDR {slug} task"
authors = [{{ name = "Perplexity AI" }}]
keywords = ["wandr", "research", "retrieval", "citation"]

[metadata]
{required_file_paths_toml}
wandr_task = "{task_name}"

[verifier]
timeout_sec = 28800.0
network_mode = "public"

[agent]
timeout_sec = 57600.0
network_mode = "public"

[environment]
build_timeout_sec = 1200.0
cpus = 2
memory_mb = 8192
storage_mb = 20480
gpus = 0
network_mode = "public"

{VERIFIER_ENV_TOML}'''
    _write_text(output_dir / "task.toml", value)


def _replace_toml_string(text: str, key: str, value: str) -> str:
    pattern = rf'(?m)^{re.escape(key)}\s*=\s*"[^"]*"$'
    replacement = f'{key} = "{value}"'
    updated, count = re.subn(pattern, replacement, text)
    if count != 1:
        raise ValueError(f"expected exactly one {key!r} entry in existing task.toml")
    return updated


def _remove_toml_key(text: str, key: str) -> str:
    pattern = rf"(?m)^{re.escape(key)}\s*=\s*[^\n]*\n?"
    return re.sub(pattern, "", text)


def _required_file_paths_toml(required_file_paths: list[str]) -> str:
    lines = ["required_file_paths = ["]
    lines.extend(f"    {json.dumps(path)}," for path in required_file_paths)
    lines.append("]")
    return "\n".join(lines)


def _remove_toml_array_assignment(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}\s*=\s*", text)
    if match is None:
        return text

    value_start = match.end()
    if value_start >= len(text) or text[value_start] != "[":
        line_end = text.find("\n", value_start)
        return text[: match.start()] + text[len(text) if line_end < 0 else line_end + 1 :]

    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(value_start, len(text)):
        char = text[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\" and quote == '"':
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                assignment_end = index + 1
                if assignment_end < len(text) and text[assignment_end] == "\n":
                    assignment_end += 1
                return text[: match.start()] + text[assignment_end:]
    raise ValueError(f"unterminated TOML array for {key!r}")


def _refresh_required_file_paths(text: str, required_file_paths: list[str]) -> str:
    pattern = r"(?ms)^\[metadata\]\n(?P<body>.*?)(?=^\[|\Z)"
    match = re.search(pattern, text)
    if match is None:
        raise ValueError("expected exactly one [metadata] table in task.toml")
    if len(re.findall(r"(?m)^\[metadata\]\s*$", text)) != 1:
        raise ValueError("expected exactly one [metadata] table in task.toml")

    body = _remove_toml_array_assignment(match.group("body"), "required_file_paths")
    body = body.lstrip("\n")
    contract = _required_file_paths_toml(required_file_paths)
    updated_body = f"{contract}\n{body}"
    return text[: match.start("body")] + updated_body + text[match.end("body") :]


def _refresh_task_toml_environment(text: str) -> str:
    pattern = r"(?ms)^\[verifier\.env\]\n.*?(?=^\[|\Z)"
    updated, count = re.subn(pattern, VERIFIER_ENV_TOML, text)
    if count != 1:
        raise ValueError("expected exactly one [verifier.env] table in task.toml")
    return updated


def _refresh_task_toml(
    text: str,
    *,
    task_name: str,
    required_file_paths: list[str],
) -> str:
    text = _replace_toml_string(text, "wandr_task", task_name)
    text = _remove_toml_key(text, "docker_image")
    text = _refresh_required_file_paths(text, required_file_paths)
    return _refresh_task_toml_environment(text)


def port_task(
    task_name: str,
    *,
    source_dir: Path,
    output_dir: Path,
    force: bool,
    update_manifest: bool = True,
) -> None:
    existing_task_toml = None
    if output_dir.exists():
        if not force:
            raise FileExistsError(f"{output_dir} already exists; pass --force to replace it")
        existing_task_toml_path = output_dir / "task.toml"
        if existing_task_toml_path.is_file():
            existing_task_toml = _read_text(existing_task_toml_path)
        shutil.rmtree(output_dir)

    if not source_dir.is_dir():
        raise FileNotFoundError(f"WANDR task source not found: {source_dir}")

    _copytree(TASK_TEMPLATE_DIR, output_dir)
    _copy_wandr_core_deps(output_dir / "environment" / "wandr_core_deps")
    _copytree(WANDR_CORE_DIR, output_dir / "tests" / "wandr_core")
    _copytree(source_dir, output_dir / "tests" / "wandr_task")

    config = _load_config(task_name, output_dir)
    _write_text(output_dir / "instruction.md", _render_instruction(config))

    required_file_paths = _write_manifest(
        output_dir,
        task_name=task_name,
        task_names=[task.name for task in flatten_tasks(config)],
    )
    if existing_task_toml is None:
        _write_task_toml(
            output_dir,
            task_name=task_name,
            required_file_paths=required_file_paths,
        )
    else:
        _write_text(
            output_dir / "task.toml",
            _refresh_task_toml(
                existing_task_toml,
                task_name=task_name,
                required_file_paths=required_file_paths,
            ),
        )

    if update_manifest and output_dir.resolve().parent == DATASET_DIR.resolve():
        update_dataset_manifest()


class WandrAdapter:
    def __init__(
        self,
        output_dir: Path = DATASET_DIR,
        *,
        limit: int | None = None,
        overwrite: bool = False,
        task_ids: list[str] | None = None,
    ) -> None:
        self.output_dir = output_dir
        self.limit = limit
        self.overwrite = overwrite
        self.task_ids = task_ids

    def _task_names(self) -> list[str]:
        task_names = self.task_ids or [
            path.name
            for path in sorted(REFERENCE_TASKS_DIR.iterdir())
            if path.is_dir() and (path / "config.py").is_file()
        ]
        if self.limit is not None:
            task_names = task_names[: self.limit]
        return task_names

    def run(self) -> None:
        for task_name in self._task_names():
            source_dir = REFERENCE_TASKS_DIR / task_name
            output_dir = self.output_dir / _slug(task_name)
            port_task(
                task_name,
                source_dir=source_dir,
                output_dir=output_dir,
                force=self.overwrite,
                update_manifest=False,
            )
            try:
                display_path = output_dir.relative_to(REPO_ROOT)
            except ValueError:
                display_path = output_dir
            print(f"Wrote {display_path}")
        if self.output_dir.resolve() == DATASET_DIR.resolve():
            update_dataset_manifest()
