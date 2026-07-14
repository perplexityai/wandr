"""CLI entrypoint for the WANDR Harbor adapter."""

from __future__ import annotations

import argparse
from pathlib import Path

from .adapter import (
    DATASET_DIR,
    REFERENCE_TASKS_DIR,
    REPO_ROOT,
    WandrAdapter,
    _slug,
    port_task,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "task_names",
        nargs="*",
        help="Optional WANDR task names, e.g. pharma_former_rd_heads",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DATASET_DIR,
        help="Directory to write generated Harbor tasks",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Single-task output directory",
    )
    parser.add_argument("--limit", type=int, help="Generate only the first N tasks")
    parser.add_argument(
        "--overwrite",
        "--force",
        action="store_true",
        help="Replace existing generated tasks",
    )
    parser.add_argument(
        "--task-ids",
        nargs="+",
        help="Only generate these WANDR task names",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        help="Single-task source directory",
    )
    return parser.parse_args()


def _run_single_task(args: argparse.Namespace, task_name: str) -> None:
    source_dir = args.source_dir or REFERENCE_TASKS_DIR / task_name
    output_dir = args.output or args.output_dir / _slug(task_name)
    port_task(
        task_name,
        source_dir=source_dir,
        output_dir=output_dir,
        force=args.overwrite,
    )
    try:
        display_path = output_dir.relative_to(REPO_ROOT)
    except ValueError:
        display_path = output_dir
    print(f"Wrote {display_path}")


def main() -> None:
    args = parse_args()
    task_ids = args.task_ids or args.task_names or None
    if args.output is not None or args.source_dir is not None:
        if not task_ids or len(task_ids) != 1:
            raise SystemExit("--output and --source-dir require exactly one task name")
        _run_single_task(args, task_ids[0])
        return

    adapter = WandrAdapter(
        args.output_dir,
        overwrite=args.overwrite,
        limit=args.limit,
        task_ids=task_ids,
    )
    adapter.run()


if __name__ == "__main__":
    main()
