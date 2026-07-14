"""Execute a command with values loaded safely from a dotenv file."""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys
from collections.abc import Mapping, Sequence

from dotenv import dotenv_values


_ENV_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")


def merged_environment(path: Path, environ: Mapping[str, str]) -> dict[str, str]:
    """Merge dotenv values without overriding the caller's environment."""
    merged = dict(environ)
    for name, value in dotenv_values(path).items():
        if not _ENV_NAME.fullmatch(name):
            raise ValueError(f"invalid environment variable name in {path}: {name!r}")
        if value is not None:
            merged.setdefault(name, value)
    return merged


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) < 2:
        print("usage: env_exec.py DOTENV COMMAND [ARG ...]", file=sys.stderr)
        return 2

    path = Path(args[0])
    environment = merged_environment(path, os.environ)
    environment["_WANDR_ENV_LOADED"] = "1"
    os.execvpe(args[1], args[1:], environment)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
