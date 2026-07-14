"""Consistency helpers for generated WANDR Harbor tasks."""

from __future__ import annotations

import filecmp
import fnmatch
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

REPO_ROOT = Path(__file__).resolve().parents[5]
PACKAGE_DIR = Path(__file__).resolve().parents[1]
ORIGIN_DIR = PACKAGE_DIR / "origin"
WANDR_CORE_DIR = ORIGIN_DIR / "wandr_core"
REFERENCE_TASKS_DIR = REPO_ROOT / "reference" / "wandr_tasks"
TASK_TEMPLATE_DIR = PACKAGE_DIR / "task-template"
DATASET_DIR = REPO_ROOT / "datasets" / "wandr"
DATASET_TOML = DATASET_DIR / "dataset.toml"
DEFAULT_IGNORES = [
    "__pycache__/",
    "*.pyc",
    ".pytest_cache/",
    ".venv/",
    "_workdir/",
    ".DS_Store",
    "*.swp",
    "*.swo",
    "*~",
]

HARBOR_TEMPLATE_TEST_FILES = (
    "artifacts.py",
    "rewards.py",
    "submissions.py",
    "test.sh",
    "utils.py",
    "verify.py",
)
WANDR_CORE_DEPS_FILES = ("pyproject.toml", "uv.lock")
TASK_NAME_RE = re.compile(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*")

if str(WANDR_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(WANDR_CORE_DIR))

from src.config import flatten_tasks, load_task_config  # noqa: E402

try:  # noqa: E402
    from harbor.publisher.packager import Packager
except ModuleNotFoundError:  # pragma: no cover - standalone adapter fallback
    Packager = None  # type: ignore[assignment,misc]


def task_dirs(dataset_dir: Path = DATASET_DIR) -> list[Path]:
    return sorted(path for path in dataset_dir.iterdir() if (path / "task.toml").is_file())


def task_name(task_dir: Path) -> str:
    data = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))
    return data["task"]["name"]


def wandr_task_name(task_dir: Path) -> str:
    data = json.loads((task_dir / "tests" / "manifest.json").read_text(encoding="utf-8"))
    return data["wandr_task"]


def _clear_task_source_modules() -> None:
    for name, module in list(sys.modules.items()):
        paths: list[Path] = []
        module_file = getattr(module, "__file__", None)
        if module_file:
            paths.append(Path(module_file))
        module_path = getattr(module, "__path__", None)
        if module_path:
            paths.extend(Path(path) for path in module_path)
        if any("wandr_task" in path.parts for path in paths):
            sys.modules.pop(name, None)


def configured_task_names(task_dir: Path, root_task_name: str) -> list[str]:
    _clear_task_source_modules()
    task_source_dir = task_dir / "tests" / "wandr_task"
    config = load_task_config(root_task_name, task_source_dir)
    return [task.name for task in flatten_tasks(config)]


def required_file_path_errors(task_dir: Path) -> list[str]:
    task_data = tomllib.loads((task_dir / "task.toml").read_text(encoding="utf-8"))
    manifest = json.loads((task_dir / "tests" / "manifest.json").read_text(encoding="utf-8"))
    expected_fields = {"name", "wandr_task", "task_names"}
    if unknown := sorted(set(manifest) - expected_fields):
        return [f"{task_dir.name}/tests/manifest.json: unknown fields: {unknown}"]
    if missing := sorted(expected_fields - set(manifest)):
        return [f"{task_dir.name}/tests/manifest.json: missing fields: {missing}"]

    task_names = manifest.get("task_names")
    if not isinstance(task_names, list) or not task_names:
        return [f"{task_dir.name}/tests/manifest.json: task_names must not be empty"]
    for index, task_name in enumerate(task_names):
        if not isinstance(task_name, str) or not TASK_NAME_RE.fullmatch(task_name):
            return [
                f"{task_dir.name}/tests/manifest.json: "
                f"task_names[{index}] is invalid: {task_name!r}"
            ]
    if len(set(task_names)) != len(task_names):
        return [f"{task_dir.name}/tests/manifest.json: task_names must be unique"]

    root_task_name = manifest.get("wandr_task")
    if not isinstance(root_task_name, str) or not TASK_NAME_RE.fullmatch(root_task_name):
        return [f"{task_dir.name}/tests/manifest.json: wandr_task is invalid"]
    if task_names[0] != root_task_name:
        return [f"{task_dir.name}/tests/manifest.json: wandr_task must be the first task name"]
    prefix = f"{root_task_name}."
    if unrelated := [name for name in task_names[1:] if not name.startswith(prefix)]:
        return [f"{task_dir.name}/tests/manifest.json: task names outside root: {unrelated}"]
    configured = configured_task_names(task_dir, root_task_name)
    if task_names != configured:
        return [
            f"{task_dir.name}/tests/manifest.json: task_names order "
            f"does not match config: configured={configured}, manifest={task_names}"
        ]

    expected = [f"results_{task_name}.jsonl" for task_name in task_names]
    actual = task_data.get("metadata", {}).get("required_file_paths")
    if actual != expected:
        return [
            f"{task_dir.name}/task.toml: required_file_paths mismatch: "
            f"expected={expected}, actual={actual}"
        ]
    return []


def task_digest(task_dir: Path) -> str:
    if Packager is not None:
        digest, _ = Packager.compute_content_hash(task_dir)
        return f"sha256:{digest}"
    digest, _ = _compute_content_hash(task_dir)
    return f"sha256:{digest}"


def _is_ignored(relative_path: str) -> bool:
    return any(
        fnmatch.fnmatch(relative_path, pattern.rstrip("/"))
        or fnmatch.fnmatch(Path(relative_path).name, pattern.rstrip("/"))
        or relative_path.startswith(pattern.rstrip("/") + "/")
        for pattern in DEFAULT_IGNORES
    )


def canonical_source_layout_errors(
    reference_tasks_dir: Path = REFERENCE_TASKS_DIR,
) -> list[str]:
    unsupported: list[str] = []
    for path in reference_tasks_dir.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(reference_tasks_dir)
        relative_text = relative.as_posix()
        if _is_ignored(relative_text):
            continue
        if relative == Path("README.md"):
            continue
        if "artifacts" in relative.parts[1:]:
            continue
        if path.suffix == ".py":
            continue
        if path.name.endswith(".md.jinja") and "prompts" in relative.parts[1:]:
            continue
        unsupported.append(relative_text)
    if not unsupported:
        return []
    return [
        "reference tasks contain unsupported files outside task artifact trees: "
        f"{unsupported}"
    ]


def _collect_files(task_dir: Path) -> list[Path]:
    task_dir = task_dir.resolve()
    files: list[Path] = []
    for single in ("task.toml", "instruction.md", "README.md"):
        path = task_dir / single
        if path.exists():
            files.append(path)
    for directory in ("environment", "tests", "solution", "steps"):
        root = task_dir / directory
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file())
    files = [path for path in files if not _is_ignored(path.relative_to(task_dir).as_posix())]
    return sorted(files, key=lambda path: path.relative_to(task_dir).as_posix())


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _compute_content_hash(task_dir: Path) -> tuple[str, list[Path]]:
    task_dir = task_dir.resolve()
    files = _collect_files(task_dir)
    outer = hashlib.sha256()
    for path in files:
        rel = path.relative_to(task_dir).as_posix()
        outer.update(f"{rel}\0{_file_hash(path)}\n".encode())
    return outer.hexdigest(), files


def expected_dataset_entries(dataset_dir: Path = DATASET_DIR) -> dict[str, str]:
    return {task_name(path): task_digest(path) for path in task_dirs(dataset_dir)}


def read_dataset_entries(dataset_toml: Path = DATASET_TOML) -> dict[str, str]:
    data = tomllib.loads(dataset_toml.read_text(encoding="utf-8"))
    return {entry["name"]: entry["digest"] for entry in data.get("tasks", [])}


def update_dataset_manifest(
    dataset_toml: Path = DATASET_TOML, dataset_dir: Path = DATASET_DIR
) -> None:
    expected = expected_dataset_entries(dataset_dir)
    current_text = dataset_toml.read_text(encoding="utf-8") if dataset_toml.exists() else ""
    header = current_text.split("[[tasks]]", 1)[0].rstrip()
    if not header:
        header = (
            "[dataset]\n"
            'name = "pplx/wandr"\n'
            'description = "WANDR benchmark tasks."\n'
            'keywords = ["wandr", "wide research", "deep research", "research", "search", "retrieval", "citation"]\n'
            "[[dataset.authors]]\n"
            'name = "Perplexity AI"'
        )

    current_order = re.findall(r'(?ms)^\[\[tasks\]\]\s*name\s*=\s*"([^"]+)"', current_text)
    ordered_names = [name for name in current_order if name in expected]
    ordered_names.extend(name for name in sorted(expected) if name not in ordered_names)

    blocks = [header, ""]
    for name in ordered_names:
        blocks.append(f'[[tasks]]\nname = "{name}"\ndigest = "{expected[name]}"\n')
    dataset_toml.write_text("\n".join(blocks).rstrip() + "\n", encoding="utf-8")


def dircmp_errors(left: Path, right: Path, *, label: str) -> list[str]:
    cmp = filecmp.dircmp(left, right, ignore=["__pycache__", ".pytest_cache", ".venv"])
    errors: list[str] = []
    if cmp.left_only:
        errors.append(f"{label}: only in {left}: {cmp.left_only}")
    if cmp.right_only:
        errors.append(f"{label}: only in {right}: {cmp.right_only}")
    if cmp.diff_files:
        errors.append(f"{label}: differing files: {cmp.diff_files}")
    if cmp.funny_files:
        errors.append(f"{label}: funny files: {cmp.funny_files}")
    for name, subcmp in cmp.subdirs.items():
        errors.extend(
            dircmp_errors(
                left / name,
                right / name,
                label=f"{label}/{name}",
            )
        )
    return errors


def _directory_files(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and not _is_ignored(path.relative_to(root).as_posix())
    }


def ported_wandr_task_errors(
    generated: Path,
    source: Path,
    *,
    label: str,
) -> list[str]:
    generated_files = _directory_files(generated)
    source_files = _directory_files(source)
    errors: list[str] = []

    generated_only = sorted(set(generated_files) - set(source_files))
    source_only = sorted(set(source_files) - set(generated_files))
    if generated_only:
        errors.append(f"{label}: only in {generated}: {generated_only}")
    if source_only:
        errors.append(f"{label}: only in {source}: {source_only}")

    differing = [
        path
        for path in sorted(set(generated_files) & set(source_files))
        if generated_files[path].read_bytes() != source_files[path].read_bytes()
    ]
    if differing:
        errors.append(f"{label}: differing files: {differing}")
    return errors


def task_template_errors(task_dir: Path) -> list[str]:
    errors: list[str] = []
    errors.extend(
        dircmp_errors(
            task_dir / "environment",
            TASK_TEMPLATE_DIR / "environment",
            label=f"{task_dir.name}/environment",
        )
    )
    if (task_dir / "solution").exists():
        errors.append(f"{task_dir.name}/solution: unexpected reference solution directory")
    for name in HARBOR_TEMPLATE_TEST_FILES:
        left = task_dir / "tests" / name
        right = TASK_TEMPLATE_DIR / "tests" / name
        if not filecmp.cmp(left, right, shallow=False):
            errors.append(f"{task_dir.name}/tests/{name}: differs from adapter task-template")
    return errors


def wandr_core_deps_errors() -> list[str]:
    errors: list[str] = []
    deps_dir = TASK_TEMPLATE_DIR / "environment" / "wandr_core_deps"
    for name in WANDR_CORE_DEPS_FILES:
        left = deps_dir / name
        right = ORIGIN_DIR / "wandr_core" / name
        if not left.is_file():
            errors.append(f"task-template/environment/wandr_core_deps/{name}: missing")
        elif not filecmp.cmp(left, right, shallow=False):
            errors.append(
                f"task-template/environment/wandr_core_deps/{name}: differs from origin/wandr_core"
            )
    return errors


def consistency_errors() -> list[str]:
    errors: list[str] = []
    errors.extend(wandr_core_deps_errors())
    errors.extend(canonical_source_layout_errors())
    if (TASK_TEMPLATE_DIR / "solution").exists():
        errors.append("task-template/solution: unexpected reference solution directory")
    canonical_solutions = sorted(
        path.relative_to(REFERENCE_TASKS_DIR).as_posix()
        for path in REFERENCE_TASKS_DIR.glob("**/solutions/*.jsonl")
    )
    if canonical_solutions:
        errors.append(f"reference tasks contain solution JSONL files: {canonical_solutions}")
    generated_task_dirs = task_dirs()
    generated_wandr_names = {wandr_task_name(path) for path in generated_task_dirs}
    reference_names = {
        path.name
        for path in REFERENCE_TASKS_DIR.iterdir()
        if path.is_dir() and (path / "config.py").is_file()
    }
    if generated_wandr_names != reference_names:
        errors.append(
            "generated/reference task set mismatch: "
            f"missing={sorted(reference_names - generated_wandr_names)}, "
            f"extra={sorted(generated_wandr_names - reference_names)}"
        )

    for task_dir in generated_task_dirs:
        wandr_name = wandr_task_name(task_dir)
        errors.extend(required_file_path_errors(task_dir))
        errors.extend(
            ported_wandr_task_errors(
                task_dir / "tests" / "wandr_task",
                REFERENCE_TASKS_DIR / wandr_name,
                label=f"{task_dir.name}/wandr_task",
            )
        )
        errors.extend(
            dircmp_errors(
                task_dir / "tests" / "wandr_core",
                ORIGIN_DIR / "wandr_core",
                label=f"{task_dir.name}/wandr_core",
            )
        )
        errors.extend(task_template_errors(task_dir))

    current = read_dataset_entries()
    expected = expected_dataset_entries()
    if current != expected:
        missing = sorted(set(expected) - set(current))
        extra = sorted(set(current) - set(expected))
        changed = sorted(
            name for name in set(expected) & set(current) if expected[name] != current[name]
        )
        errors.append(
            "datasets/wandr/dataset.toml mismatch: "
            f"missing={missing}, extra={extra}, changed={changed}"
        )

    return errors


def main() -> None:
    errors = consistency_errors()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("adapter consistency OK")


if __name__ == "__main__":
    main()
