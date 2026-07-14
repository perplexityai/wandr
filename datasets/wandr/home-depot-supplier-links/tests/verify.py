"""Harbor verifier entrypoint for one WANDR task directory."""

import argparse
import asyncio
import logging
import os
import traceback
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from artifacts import (
    ArtifactPaths,
    artifact_refs,
    artifact_paths,
    clear_artifacts,
    write_error,
    write_json,
    write_rewards,
    write_text,
)
from rewards import (
    reward_details,
    scoremap_rewards,
    wandr_diagnostics,
    zero_rewards,
)
from sidecars.report import (
    render_scoremap,
    report_from_metrics,
    viewer_context,
)
from sidecars.viewer import render_report_html
from sidecars.viewer_text import render_report_text
from src.config import (
    TaskConfig,
    flatten_tasks,
    load_task_config,
)
from src.components import DEBUG_DIR_NAME
from src.runtime.clients import openai_api_key_values
from src.runtime.types import Record
from src.runtime.utils import (
    public_print,
    setup_eval_logging,
)
from src.metrics import (
    metrics_for_tasks,
)
from src.pipeline import run_pipeline
from src.submissions import (
    load_submission,
    seed_submissions,
    submission_subtrees,
)
from submissions import (
    Manifest,
    SubmissionInputs,
    load_manifest,
    submission_inputs,
    validate_tasks,
)
from utils import capture_stdio

LOGGER = logging.getLogger("wandr_harbor.verify")
DEFAULT_LOGS_DIR = Path("/logs/verifier")
DEFAULT_HEAL_RETRIES = 9
DEFAULT_HEAL_MIN_COVERAGE = 0.90


class InvalidSubmissionError(ValueError):
    """Submission files are missing or do not satisfy the task JSONL schema."""


def _heal_retries(env: Mapping[str, str]) -> int:
    raw = env.get("WANDR_HEAL_RETRIES", str(DEFAULT_HEAL_RETRIES))
    value = int(raw)
    if value < 0:
        raise ValueError("WANDR_HEAL_RETRIES must be >= 0")
    return value


def _heal_min_coverage(env: Mapping[str, str]) -> float:
    raw = env.get("WANDR_HEAL_MIN_COVERAGE", str(DEFAULT_HEAL_MIN_COVERAGE))
    value = float(raw)
    if value <= 0 or value > 1:
        raise ValueError("WANDR_HEAL_MIN_COVERAGE must be in (0, 1]")
    return value


def _coverage_satisfied(*, judged_count: int, submitted_count: int, min_coverage: float) -> bool:
    return judged_count >= submitted_count or (
        submitted_count > 0 and judged_count / submitted_count >= min_coverage
    )


def _validate_runtime_env(env: Mapping[str, str]) -> None:
    if not openai_api_key_values(env):
        raise RuntimeError("Missing *OPENAI_API_KEY* env var for WANDR judge calls.")


def _load_task_configs(manifest: Manifest, task_dir: Path) -> tuple[TaskConfig, list[TaskConfig]]:
    root_task_config = load_task_config(manifest["task_name"], task_dir)
    task_configs = flatten_tasks(root_task_config)
    validate_tasks(manifest, (task_config.name for task_config in task_configs))
    return root_task_config, task_configs


def _load_submission_inputs(manifest: Manifest, workspace_dir: Path) -> SubmissionInputs:
    try:
        return submission_inputs(manifest, workspace_dir)
    except (FileNotFoundError, ValueError) as exc:
        raise InvalidSubmissionError(str(exc)) from exc


async def _validate_submission_records(
    root_task_config: TaskConfig,
    submissions: SubmissionInputs,
) -> None:
    queue: asyncio.Queue[Record | None] = asyncio.Queue()
    seed_submissions(
        queue,
        submission_subtrees([root_task_config]),
        submissions["paths_by_task"],
    )
    while (record := await queue.get()) is not None:
        try:
            await load_submission(None, record)
        except (FileNotFoundError, ValueError) as exc:
            raise InvalidSubmissionError(str(exc)) from exc


def _build_metrics_report(
    *,
    metrics_json_path: Path,
    manifest: Manifest,
    instruction_path: Path | None,
    root_task_config: TaskConfig,
    task_configs: list[TaskConfig],
    submitted_rows_by_task: dict[str, int],
    judged_records: list[Record],
    output_dir: Path,
) -> dict[str, Any]:
    return {
        "records": len(judged_records),
        "submitted_rows_by_task": submitted_rows_by_task,
        "manifest": manifest["document"],
        "output_dir": str(output_dir),
        "metrics_json": str(metrics_json_path),
        "viewer_context": viewer_context(root_task_config, instruction_path),
        "metrics": metrics_for_tasks(judged_records, task_configs),
    }


def _write_run_artifacts(
    *,
    artifacts: ArtifactPaths,
    manifest: Manifest,
    submissions: SubmissionInputs,
    output_dir: Path,
    eval_log_path: Path,
    stdio_log_path: Path,
    judged_records: list[Record],
    metrics_report: dict[str, Any],
) -> None:
    report = report_from_metrics(metrics_report)
    rewards = scoremap_rewards(report["scoremap"])
    report_html = render_report_html(report)
    report_txt = render_report_text(report)
    diagnostics = wandr_diagnostics(
        task_name=report.get("task_name"),
        submission_fp=report.get("submission_fp"),
        submitted_rows_by_task=submissions["rows_by_task"],
        judged_record_count=len(judged_records),
        report_record_count=len(report.get("records") or []),
        task_count=len(report.get("task_order") or []),
        rewards=rewards,
        scoremap=report["scoremap"],
        field_decompositions=report["field_decompositions"],
        artifacts=artifact_refs(
            artifacts,
            output_dir=output_dir,
            debug_dir=output_dir / DEBUG_DIR_NAME,
            eval_log_path=eval_log_path,
            stdio_log_path=stdio_log_path,
        ),
        manifest=manifest["document"],
    )
    write_json(artifacts["metrics_json"], metrics_report)
    write_text(artifacts["report_html"], report_html)
    write_text(artifacts["report_txt"], report_txt)
    write_text(artifacts["wandr_viewer_html"], report_html)
    write_text(artifacts["wandr_viewer_txt"], report_txt)
    write_rewards(artifacts, rewards)
    write_json(
        artifacts["reward_details_json"],
        reward_details(
            rewards,
            scoremap=report["scoremap"],
            field_decompositions=report["field_decompositions"],
        ),
    )
    write_json(artifacts["wandr_details_json"], diagnostics)
    artifacts["error_json"].unlink(missing_ok=True)
    public_print(render_scoremap(report["scoremap"]), end="")


async def _run_evaluation(
    *,
    artifacts: ArtifactPaths,
    workspace_dir: Path,
    task_dir: Path,
    instruction_path: Path | None,
    output_dir: Path,
    eval_log_path: Path,
    stdio_log_path: Path,
    env: Mapping[str, str],
) -> None:
    manifest = load_manifest()
    root_task_config, task_configs = _load_task_configs(manifest, task_dir)
    submissions = _load_submission_inputs(manifest, workspace_dir)
    await _validate_submission_records(root_task_config, submissions)
    _validate_runtime_env(env)
    attempts = 1 + _heal_retries(env)
    submitted_count = sum(submissions["rows_by_task"].values())
    min_coverage = _heal_min_coverage(env)
    last_error: BaseException | None = None
    succeeded = False
    for pass_index in range(attempts):
        public_print(f"\n========== WANDR verifier pass {pass_index + 1}/{attempts} ==========\n")
        try:
            judged_records = await run_pipeline(
                [root_task_config],
                output_dir,
                submission_paths=submissions["paths_by_task"],
            )
            metrics_report = _build_metrics_report(
                metrics_json_path=artifacts["metrics_json"],
                manifest=manifest,
                instruction_path=instruction_path,
                root_task_config=root_task_config,
                task_configs=task_configs,
                submitted_rows_by_task=submissions["rows_by_task"],
                judged_records=judged_records,
                output_dir=output_dir,
            )
            _write_run_artifacts(
                artifacts=artifacts,
                manifest=manifest,
                submissions=submissions,
                output_dir=output_dir,
                eval_log_path=eval_log_path,
                stdio_log_path=stdio_log_path,
                judged_records=judged_records,
                metrics_report=metrics_report,
            )
        except Exception as exc:
            last_error = exc
            LOGGER.exception("verification_pass_failed")
            continue
        succeeded = True
        judged_count = len(judged_records)
        if _coverage_satisfied(
            judged_count=judged_count,
            submitted_count=submitted_count,
            min_coverage=min_coverage,
        ):
            public_print(
                "\nWANDR verifier reached sufficient submitted-row coverage; "
                "stopping healing passes.\n"
            )
            break
    if not succeeded and last_error is not None:
        raise last_error


def _parse_args(default_output_dir: Path) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-dir", type=Path, default=Path("/workspace"))
    parser.add_argument("--task-dir", type=Path, default=Path("/tests/wandr_task"))
    parser.add_argument("--instruction-path", type=Path)
    parser.add_argument("--output-dir", type=Path, default=default_output_dir)
    return parser.parse_args()


def main() -> int:
    logs_dir = Path(os.environ.get("LOGS_DIR", str(DEFAULT_LOGS_DIR)))
    wandr_log_dir = Path(os.environ.get("WANDR_LOG_DIR", str(logs_dir / "wandr")))
    eval_log_path = Path(os.environ.get("WANDR_EVAL_LOG_PATH", str(wandr_log_dir / "eval.log")))
    stdio_log_path = Path(os.environ.get("WANDR_STDIO_LOG_PATH", str(wandr_log_dir / "stdio.log")))
    artifacts = artifact_paths(logs_dir)
    capture_stdio(stdio_log_path)
    setup_eval_logging(eval_log_path)
    clear_artifacts(artifacts)
    try:
        cli_args = _parse_args(logs_dir / "wandr")
        asyncio.run(
            _run_evaluation(
                artifacts=artifacts,
                workspace_dir=cli_args.workspace_dir,
                task_dir=cli_args.task_dir,
                instruction_path=cli_args.instruction_path,
                output_dir=cli_args.output_dir,
                eval_log_path=eval_log_path,
                stdio_log_path=stdio_log_path,
                env=os.environ,
            )
        )
        return 0
    except InvalidSubmissionError as exc:
        LOGGER.exception("invalid_submission")
        clear_artifacts(artifacts)
        write_rewards(artifacts, zero_rewards())
        public_print(f"\nInvalid WANDR submission: {exc}\n")
        return 0
    except Exception as exc:
        LOGGER.exception("verification_failed")
        clear_artifacts(artifacts)
        write_error(artifacts, f"{type(exc).__name__}: {exc}", traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
