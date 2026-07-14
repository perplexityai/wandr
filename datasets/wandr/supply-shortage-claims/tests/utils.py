"""Small Harbor verifier utilities."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from src.runtime.utils import (
    PUBLIC_STDERR_FD_ENV,
    PUBLIC_STDOUT_FD_ENV,
)


def _preserve_stdio(env_name: str, fd: int) -> None:
    if env_name not in os.environ:
        os.environ[env_name] = str(os.dup(fd))


def _fd_points_to(fd: int, path: Path) -> bool:
    try:
        fd_stat = os.fstat(fd)
        path_stat = path.stat()
    except OSError:
        return False
    return (fd_stat.st_dev, fd_stat.st_ino) == (path_stat.st_dev, path_stat.st_ino)


def _stdio_points_to(path: Path) -> bool:
    return _fd_points_to(1, path) and _fd_points_to(2, path)


def capture_stdio(capture_path: Path) -> None:
    _preserve_stdio(PUBLIC_STDOUT_FD_ENV, 1)
    _preserve_stdio(PUBLIC_STDERR_FD_ENV, 2)
    capture_path.parent.mkdir(parents=True, exist_ok=True)
    if _stdio_points_to(capture_path):
        sys.stdout = os.fdopen(1, "w", buffering=1, closefd=False)
        sys.stderr = os.fdopen(2, "w", buffering=1, closefd=False)
        return
    capture_fd = os.open(capture_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.dup2(capture_fd, 1)
        os.dup2(capture_fd, 2)
    finally:
        os.close(capture_fd)
    sys.stdout = os.fdopen(1, "w", buffering=1, closefd=False)
    sys.stderr = os.fdopen(2, "w", buffering=1, closefd=False)
