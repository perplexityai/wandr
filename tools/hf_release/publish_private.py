#!/usr/bin/env python3
"""Create and upload a WANDR Hugging Face dataset while enforcing privacy."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Protocol

from huggingface_hub import HfApi


class RepoInfo(Protocol):
    private: bool


class HubApi(Protocol):
    def create_repo(self, **kwargs: object) -> object: ...

    def repo_info(self, **kwargs: object) -> RepoInfo: ...

    def upload_folder(self, **kwargs: object) -> object: ...


def _assert_private(api: HubApi, repo_id: str, stage: str) -> None:
    info = api.repo_info(repo_id=repo_id, repo_type="dataset")
    if info.private is not True:
        raise RuntimeError(f"refusing {stage}: {repo_id} is not confirmed private")


def _verify_manifest(folder: Path) -> None:
    manifest_path = folder / "release-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest["files"]
    expected_paths = [record["path"] for record in records]
    if len(expected_paths) != len(set(expected_paths)):
        raise ValueError("release manifest contains duplicate paths")
    actual_paths = sorted(
        path.relative_to(folder).as_posix()
        for path in folder.rglob("*")
        if path.is_file() and path != manifest_path
    )
    if sorted(expected_paths) != actual_paths:
        raise ValueError("release manifest file set does not match upload folder")
    for record in records:
        path = folder / record["path"]
        data = path.read_bytes()
        if (
            len(data) != record["size"]
            or hashlib.sha256(data).hexdigest() != record["sha256"]
        ):
            raise ValueError(f"release manifest integrity mismatch: {record['path']}")


def publish_private(api: HubApi, folder: Path, repo_id: str) -> None:
    if not folder.is_dir() or not (folder / "release-manifest.json").is_file():
        raise ValueError(f"not a verified WANDR release folder: {folder}")
    _verify_manifest(folder)
    api.create_repo(
        repo_id=repo_id,
        repo_type="dataset",
        private=True,
        exist_ok=True,
    )
    _assert_private(api, repo_id, "before upload")
    api.upload_folder(
        repo_id=repo_id,
        repo_type="dataset",
        folder_path=str(folder),
        commit_message="Stage pinned WANDR dataset release privately",
    )
    _assert_private(api, repo_id, "after upload")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--repo-id", default="perplexity-ai/wandr")
    parser.add_argument(
        "--confirm-private-staging",
        action="store_true",
        help="Required acknowledgement that this upload must remain private",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.confirm_private_staging:
        raise SystemExit("refusing upload without --confirm-private-staging")
    publish_private(HfApi(), args.folder.resolve(), args.repo_id)
    print(f"Private staging upload verified: {args.repo_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
