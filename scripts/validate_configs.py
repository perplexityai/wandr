#!/usr/bin/env python3
"""Validate run configs without starting a Harbor job or API request."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

import yaml
from harbor.models.job.config import JobConfig
from harbor.models.trial.config import AgentConfig
from pydantic import ValidationError

from relay.core import RelayError
from relay.providers import endpoint_factory


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATHS = (
    ROOT / "configs/smoke.yaml",
    ROOT / "configs/smoke-all.yaml",
    ROOT / "configs/validation.yaml",
    ROOT / "configs/wandr.yaml",
)

RELAY_AGENT_KWARGS = {
    "workspace_root",
    "include_globs",
    "exclude_globs",
    "max_files",
    "max_file_bytes",
    "max_total_file_bytes",
    "request",
    "endpoint",
    "extra_instruction",
    "extra_env",
    "require_files",
    "required_file_paths",
    "max_full_restarts",
    "full_restart_initial_delay_sec",
    "full_restart_max_delay_sec",
}

ENDPOINT_KWARGS = {
    "openai": {
        "base_url",
        "poll_interval_sec",
        "stream_bootstrap_timeout_sec",
        "stream_observation",
        "delivery_channel",
        "output_root",
    },
    "anthropic": {
        "delivery_channel",
        "output_root",
        "reconnect_delay_sec",
        "suite_tag",
    },
    "perplexity": {
        "base_url",
        "endpoint_path",
        "delivery_channel",
        "output_root",
        "poll_interval_sec",
        "stream_slice_sec",
    },
    "exa": {"base_url", "delivery_channel", "poll_interval_sec"},
    "parallel": {"base_url", "delivery_channel", "result_block_timeout_sec"},
    "gemini": {"base_url", "delivery_channel", "poll_interval_sec"},
}


def _is_bool(value: Any) -> bool:
    return isinstance(value, bool)


def _is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_nonnegative_number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and value >= 0


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


HARBORPATCH_FIELDS: dict[str, Callable[[Any], bool]] = {
    "n_concurrent_agent_phases": _is_positive_int,
    "n_concurrent_verifier_phases": _is_positive_int,
    "e2b_use_dockerfile": _is_bool,
    "e2b_domain": _is_nonempty_string,
    "e2b_validate_api_key": _is_bool,
    "e2b_stream_output": _is_bool,
    "e2b_share_template_by_hash": _is_bool,
    "e2b_template_cache_dir": _is_nonempty_string,
    "e2b_verifier_terminal_wait": _is_nonnegative_number,
    "nofile_soft_limit": _is_positive_int,
}


def _validate_harborpatch(path: Path, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{path}: harborpatch must be a mapping")
    unknown = sorted(set(value) - set(HARBORPATCH_FIELDS))
    if unknown:
        raise ValueError(f"{path}: unknown harborpatch keys: {', '.join(unknown)}")
    for name, item in value.items():
        if not HARBORPATCH_FIELDS[name](item):
            raise ValueError(f"{path}: invalid harborpatch.{name}: {item!r}")


def _validate_local_paths(path: Path, data: dict[str, Any]) -> None:
    for entry in data.get("tasks", []):
        raw_path = entry if isinstance(entry, str) else entry.get("path")
        if raw_path is None:
            continue
        task_path = (ROOT / raw_path).resolve()
        if not task_path.is_dir() or not (task_path / "task.toml").is_file():
            raise ValueError(f"{path}: local task does not exist: {raw_path}")

    for entry in data.get("datasets", []):
        if not isinstance(entry, dict) or entry.get("path") is None:
            continue
        raw_path = entry["path"]
        dataset_path = (ROOT / raw_path).resolve()
        if not dataset_path.is_dir() or not (dataset_path / "dataset.toml").is_file():
            raise ValueError(f"{path}: local dataset does not exist: {raw_path}")


def _validate_relay_agent(path: Path, index: int, agent: dict[str, Any]) -> None:
    unknown_agent_fields = sorted(set(agent) - set(AgentConfig.model_fields))
    if unknown_agent_fields:
        raise ValueError(
            f"{path}: agent {index} has unknown fields: " + ", ".join(unknown_agent_fields)
        )
    if agent.get("import_path") != "relay.agent:RelayAgent":
        raise ValueError(f"{path}: agent {index} must use relay.agent:RelayAgent")

    model_name = agent.get("model_name")
    if not isinstance(model_name, str):
        raise ValueError(f"{path}: agent {index} requires a provider-qualified model")
    provider, separator, endpoint_model = model_name.partition("/")
    if not separator or not provider or not endpoint_model:
        raise ValueError(f"{path}: agent {index} model must be provider-qualified: provider/model")

    kwargs = agent.get("kwargs", {})
    if not isinstance(kwargs, dict):
        raise ValueError(f"{path}: agent {index} kwargs must be a mapping")
    unknown_kwargs = sorted(set(kwargs) - RELAY_AGENT_KWARGS)
    if unknown_kwargs:
        raise ValueError(
            f"{path}: agent {index} has unknown Relay kwargs: " + ", ".join(unknown_kwargs)
        )

    request = kwargs.get("request", {})
    endpoint = kwargs.get("endpoint", {})
    if not isinstance(request, dict) or not isinstance(endpoint, dict):
        raise ValueError(f"{path}: agent {index} request and endpoint must be mappings")

    factory = endpoint_factory(provider)
    allowed_endpoint_kwargs = ENDPOINT_KWARGS.get(provider)
    if allowed_endpoint_kwargs is None:
        raise ValueError(f"{path}: agent {index} has no supported endpoint contract")
    unknown_endpoint_kwargs = sorted(set(endpoint) - allowed_endpoint_kwargs)
    if unknown_endpoint_kwargs:
        raise ValueError(
            f"{path}: agent {index} has unknown {provider} endpoint kwargs: "
            + ", ".join(unknown_endpoint_kwargs)
        )

    # Constructors parse provider-owned request options and delivery settings,
    # but do not make a network request.
    factory(model_name=endpoint_model, env={}, request=request, **endpoint)


def validate_config(path: Path) -> None:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: config root must be a mapping")

    data = dict(raw)
    harborpatch = data.pop("harborpatch", {})
    _validate_harborpatch(path, harborpatch)

    unknown_top_level = sorted(set(data) - set(JobConfig.model_fields))
    if unknown_top_level:
        raise ValueError(f"{path}: unknown Harbor config fields: {', '.join(unknown_top_level)}")
    JobConfig.model_validate(data)
    _validate_local_paths(path, data)

    agents = data.get("agents", [])
    if not isinstance(agents, list) or not agents:
        raise ValueError(f"{path}: at least one Relay agent is required")
    for index, agent in enumerate(agents, start=1):
        if not isinstance(agent, dict):
            raise ValueError(f"{path}: agent {index} must be a mapping")
        _validate_relay_agent(path, index, agent)


def main() -> int:
    try:
        for path in CONFIG_PATHS:
            if not path.is_file():
                raise ValueError(f"missing config: {path}")
            validate_config(path)
    except (OSError, RelayError, ValidationError, ValueError, yaml.YAMLError) as error:
        print(f"config validation failed: {error}", file=sys.stderr)
        return 1

    print(f"config validation OK ({len(CONFIG_PATHS)} configs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
