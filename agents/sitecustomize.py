"""Optional Harbor startup compatibility hooks."""

from __future__ import annotations

import os
from pathlib import Path
import sys
import traceback
from typing import Any

import yaml

from relay.harborpatch import install_from_env


_PHASE_LIMIT_ENVS = (
    "HARBOR_N_CONCURRENT_AGENT_PHASES",
    "HARBOR_N_CONCURRENT_VERIFIER_PHASES",
)
_E2B_ENVS = (
    "HARBOR_E2B_USE_DOCKERFILE",
    "HARBOR_E2B_STREAM_OUTPUT",
    "HARBOR_E2B_SHARE_TEMPLATE_BY_HASH",
    "HARBOR_E2B_TEMPLATE_CACHE_DIR",
    "HARBOR_E2B_TEMPLATE_REQUEST_TIMEOUT",
    "HARBOR_E2B_FILESYSTEM_RETRY_ATTEMPTS",
    "HARBOR_E2B_VERIFIER_TERMINAL_WAIT",
)
_RESOURCE_LIMIT_ENVS = ("HARBOR_NOFILE_SOFT_LIMIT",)


def _enabled() -> bool:
    return any(
        os.environ.get(name)
        for name in (
            *_PHASE_LIMIT_ENVS,
            *_E2B_ENVS,
            *_RESOURCE_LIMIT_ENVS,
        )
    )


def _looks_like_harbor(argv: list[str]) -> bool:
    return bool(argv) and Path(argv[0]).name == "harbor"


def _config_path_from_argv(argv: list[str]) -> Path | None:
    if not _looks_like_harbor(argv):
        return None

    args = argv[1:]
    for index, arg in enumerate(args):
        if arg in {"-c", "--config"} and index + 1 < len(args):
            return Path(args[index + 1])
        if arg.startswith("--config="):
            return Path(arg.split("=", 1)[1])
    return None


def _ensure_docker_cli_plugins_for_harbor() -> None:
    if not _looks_like_harbor(sys.argv):
        return

    docker_config = os.environ.get("DOCKER_CONFIG")
    if not docker_config:
        return

    docker_config_path = Path(docker_config)
    cli_plugins_path = docker_config_path / "cli-plugins"
    if cli_plugins_path.exists() or cli_plugins_path.is_symlink():
        return

    home_cli_plugins_path = Path.home() / ".docker" / "cli-plugins"
    if not home_cli_plugins_path.is_dir():
        return

    docker_config_path.mkdir(parents=True, exist_ok=True)
    try:
        cli_plugins_path.symlink_to(home_cli_plugins_path, target_is_directory=True)
    except FileExistsError:
        pass


def _is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _apply_config_phase_limits() -> None:
    config_path = _config_path_from_argv(sys.argv)
    if config_path is None or not config_path.exists():
        return

    data = yaml.safe_load(config_path.read_text()) or {}
    if not isinstance(data, dict):
        return

    section = data.get("harborpatch") or {}
    if not isinstance(section, dict):
        return

    agent_limit = section.get("n_concurrent_agent_phases")
    verifier_limit = section.get("n_concurrent_verifier_phases")
    e2b_use_dockerfile = section.get("e2b_use_dockerfile")
    e2b_domain = section.get("e2b_domain")
    e2b_validate_api_key = section.get("e2b_validate_api_key")
    e2b_stream_output = section.get("e2b_stream_output")
    e2b_share_template_by_hash = section.get("e2b_share_template_by_hash")
    e2b_template_cache_dir = section.get("e2b_template_cache_dir")
    e2b_verifier_terminal_wait = section.get("e2b_verifier_terminal_wait")
    nofile_soft_limit = section.get("nofile_soft_limit")

    if agent_limit is not None:
        os.environ.setdefault("HARBOR_N_CONCURRENT_AGENT_PHASES", str(agent_limit))
    if verifier_limit is not None:
        os.environ.setdefault(
            "HARBOR_N_CONCURRENT_VERIFIER_PHASES",
            str(verifier_limit),
        )
    if e2b_use_dockerfile is not None:
        os.environ.setdefault(
            "HARBOR_E2B_USE_DOCKERFILE",
            "1" if _is_truthy(e2b_use_dockerfile) else "0",
        )
    if e2b_domain is not None:
        os.environ.setdefault("E2B_DOMAIN", str(e2b_domain))
    if e2b_validate_api_key is not None:
        os.environ.setdefault(
            "E2B_VALIDATE_API_KEY",
            "1" if _is_truthy(e2b_validate_api_key) else "0",
        )
    if e2b_stream_output is not None:
        os.environ.setdefault(
            "HARBOR_E2B_STREAM_OUTPUT",
            "1" if _is_truthy(e2b_stream_output) else "0",
        )
    if e2b_share_template_by_hash is not None:
        os.environ.setdefault(
            "HARBOR_E2B_SHARE_TEMPLATE_BY_HASH",
            "1" if _is_truthy(e2b_share_template_by_hash) else "0",
        )
    if e2b_template_cache_dir is not None:
        os.environ.setdefault(
            "HARBOR_E2B_TEMPLATE_CACHE_DIR",
            str(e2b_template_cache_dir),
        )
    if e2b_verifier_terminal_wait is not None:
        os.environ.setdefault(
            "HARBOR_E2B_VERIFIER_TERMINAL_WAIT",
            str(e2b_verifier_terminal_wait),
        )
    if nofile_soft_limit is not None:
        os.environ.setdefault("HARBOR_NOFILE_SOFT_LIMIT", str(nofile_soft_limit))


def _fail() -> None:
    sys.stderr.write("Failed to install Harbor compatibility hooks.\n")
    traceback.print_exc(file=sys.stderr)
    raise SystemExit(78)


try:
    _ensure_docker_cli_plugins_for_harbor()
    _apply_config_phase_limits()
except Exception:
    _fail()

if _enabled():
    try:
        install_from_env()
    except ModuleNotFoundError as exc:
        if exc.name != "harbor":
            _fail()
    except Exception:
        _fail()
