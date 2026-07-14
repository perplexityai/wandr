"""Harbor output paths and file writers."""

import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any, TypedDict

from rewards import PRIMARY_REWARD, normalize_rewards


class ArtifactPaths(TypedDict):
    logs_dir: Path
    artifacts_dir: Path
    reward_txt: Path
    reward_json: Path
    reward_details_json: Path
    wandr_details_json: Path
    metrics_json: Path
    report_html: Path
    report_txt: Path
    wandr_viewer_html: Path
    wandr_viewer_txt: Path
    error_json: Path
    setup_log: Path
    uv_bootstrap_log: Path


def artifact_paths(logs_dir: str | Path) -> ArtifactPaths:
    logs_dir = Path(logs_dir)
    artifacts_dir = logs_dir.parent / "artifacts"
    return {
        "logs_dir": logs_dir,
        "artifacts_dir": artifacts_dir,
        "reward_txt": logs_dir / "reward.txt",
        "reward_json": logs_dir / "reward.json",
        "reward_details_json": logs_dir / "reward-details.json",
        "wandr_details_json": logs_dir / "wandr-details.json",
        "metrics_json": logs_dir / "wandr_metrics.json",
        "report_html": logs_dir / "report.html",
        "report_txt": logs_dir / "report.txt",
        "wandr_viewer_html": artifacts_dir / "wandr_viewer.html",
        "wandr_viewer_txt": artifacts_dir / "wandr_viewer.txt",
        "error_json": logs_dir / "error.json",
        "setup_log": logs_dir / "setup.log",
        "uv_bootstrap_log": logs_dir / "uv-bootstrap.log",
    }


def _generated_artifacts(artifacts: ArtifactPaths) -> tuple[Path, ...]:
    return (
        artifacts["error_json"],
        artifacts["reward_txt"],
        artifacts["reward_json"],
        artifacts["reward_details_json"],
        artifacts["wandr_details_json"],
        artifacts["metrics_json"],
        artifacts["report_html"],
        artifacts["report_txt"],
        artifacts["wandr_viewer_html"],
        artifacts["wandr_viewer_txt"],
    )


def artifact_refs(
    artifacts: ArtifactPaths,
    *,
    output_dir: Path,
    debug_dir: Path,
    eval_log_path: Path,
    stdio_log_path: Path,
) -> dict[str, str]:
    return {
        "reward_txt": str(artifacts["reward_txt"]),
        "reward_json": str(artifacts["reward_json"]),
        "reward_details_json": str(artifacts["reward_details_json"]),
        "wandr_details_json": str(artifacts["wandr_details_json"]),
        "error_json": str(artifacts["error_json"]),
        "setup_log": str(artifacts["setup_log"]),
        "uv_bootstrap_log": str(artifacts["uv_bootstrap_log"]),
        "wandr_metrics_json": str(artifacts["metrics_json"]),
        "report_txt": str(artifacts["report_txt"]),
        "report_html": str(artifacts["report_html"]),
        "wandr_viewer_txt": str(artifacts["wandr_viewer_txt"]),
        "wandr_viewer_html": str(artifacts["wandr_viewer_html"]),
        "wandr_output_dir": str(output_dir),
        "wandr_debug_dir": str(debug_dir),
        "wandr_eval_log": str(eval_log_path),
        "wandr_stdio_log": str(stdio_log_path),
    }


def clear_artifacts(artifacts: ArtifactPaths) -> None:
    for artifact_path in _generated_artifacts(artifacts):
        artifact_path.unlink(missing_ok=True)


def write_rewards(artifacts: ArtifactPaths, rewards: Mapping[str, float]) -> None:
    normalized_rewards = normalize_rewards(rewards)
    artifacts["logs_dir"].mkdir(parents=True, exist_ok=True)
    write_text(artifacts["reward_txt"], f"{normalized_rewards[PRIMARY_REWARD]}\n")
    write_json(
        artifacts["reward_json"],
        {
            "grade": normalized_rewards[PRIMARY_REWARD],
            "reward": normalized_rewards[PRIMARY_REWARD],
            **normalized_rewards,
        },
    )


def write_error(
    artifacts: ArtifactPaths, message: str, traceback_text: str | None = None
) -> None:
    document = {"error": message}
    if traceback_text is not None:
        document["traceback"] = traceback_text
    write_json(artifacts["error_json"], document)


def write_failure(
    artifacts: ArtifactPaths, message: str, traceback_text: str | None = None
) -> None:
    clear_artifacts(artifacts)
    write_error(artifacts, message, traceback_text)


def _has_error(artifacts: ArtifactPaths) -> bool:
    return artifacts["error_json"].exists()


def write_json(target_path: Path, document: Any) -> None:
    write_text(target_path, json.dumps(document, indent=2, allow_nan=False) + "\n")


def write_text(target_path: Path, text: str) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(text)


def main(argv: list[str]) -> int:
    match argv:
        case ["clear", logs_dir]:
            clear_artifacts(artifact_paths(logs_dir))
            return 0
        case ["fail", logs_dir, message]:
            write_failure(artifact_paths(logs_dir), message)
            return 0
        case ["error", logs_dir, message]:
            write_error(artifact_paths(logs_dir), message)
            return 0
        case ["has-error", logs_dir]:
            return 0 if _has_error(artifact_paths(logs_dir)) else 1
    raise SystemExit(
        f"usage: {Path(sys.argv[0]).name} clear|fail|error|has-error "
        "LOGS_DIR [MESSAGE]"
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
