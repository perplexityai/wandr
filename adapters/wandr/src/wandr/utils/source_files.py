"""Generic source-tree copy exclusions."""

from __future__ import annotations

import fnmatch


EXCLUDE_PATTERNS = {
    ".DS_Store",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "*.pyc",
    "*.swp",
    "*.swo",
    "*~",
    "_workdir",
}


def ignore_source_files(_dir: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDE_PATTERNS)
    }
