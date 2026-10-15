#!/usr/bin/env python3
"""End-to-end offline verification for the WANDR Hugging Face export."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from datasets import load_dataset
from export import (
    EXPECTED_SCORED_NODES,
    EXPECTED_SMOKE_TASKS,
    EXPECTED_TEST_TASKS,
    EXPECTED_TREE_NODES,
    MAX_UPLOAD_FILE_BYTES,
    REPO_ROOT,
    SOURCE_BUNDLE_INDEX_PATH,
    SOURCE_COMMIT,
    SOURCE_SHARD_MAX_BYTES,
    SUBMISSION_CONTRACT,
    export,
    verify_source_bundle,
)
from huggingface_hub import DatasetCard
from publish_private import publish_private

EXPECTED_FEATURES = {
    "task_id": {"dtype": "string", "_type": "Value"},
    "source_commit": {"dtype": "string", "_type": "Value"},
    "source_url": {"dtype": "string", "_type": "Value"},
    "instruction": {"dtype": "string", "_type": "Value"},
    "instruction_sha256": {"dtype": "string", "_type": "Value"},
    "instruction_status": {"dtype": "string", "_type": "Value"},
    "instruction_source_url": {"dtype": "string", "_type": "Value"},
    "required_output_files": {
        "feature": {"dtype": "string", "_type": "Value"},
        "_type": "List",
    },
    "task_tree_json": {"dtype": "string", "_type": "Value"},
    "metadata_json": {"dtype": "string", "_type": "Value"},
    "submission_contract_json": {"dtype": "string", "_type": "Value"},
    "evaluator_index_path": {"dtype": "string", "_type": "Value"},
    "source_bundle_path": {"dtype": "string", "_type": "Value"},
    "external_dependencies_json": {"dtype": "string", "_type": "Value"},
    "self_contained": {"dtype": "bool", "_type": "Value"},
    "scored": {"dtype": "bool", "_type": "Value"},
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): _sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def verify_rows(output: Path) -> None:
    test = _jsonl(output / "data" / "test.jsonl")
    smoke = _jsonl(output / "data" / "smoke.jsonl")
    assert len(test) == EXPECTED_TEST_TASKS
    assert len(smoke) == EXPECTED_SMOKE_TASKS
    rows = test + smoke
    assert len({row["task_id"] for row in rows}) == len(rows)
    assert [row["task_id"] for row in test] == sorted(row["task_id"] for row in test)
    assert smoke[0]["task_id"] == "smoke"
    assert all(row["source_commit"] == SOURCE_COMMIT for row in rows)
    assert all(
        json.loads(row["submission_contract_json"]) == SUBMISSION_CONTRACT
        for row in rows
    )

    node_count = 0
    scored_node_count = 0
    for row in rows:
        nodes = json.loads(row["task_tree_json"])
        node_count += len(nodes)
        scored_node_count += len(nodes) if row["scored"] else 0
        assert nodes[0]["task_id"] == row["task_id"]
        assert [node["order"] for node in nodes] == list(range(len(nodes)))
        assert row["required_output_files"] == [
            node["required_output_file"] for node in nodes
        ]
        names = {node["task_id"] for node in nodes}
        for node in nodes:
            assert node["parent_id"] is None or node["parent_id"] in names
            expected_fields = []
            for key in node["key_hierarchy"]:
                if key["name"] == "url":
                    continue
                expected_fields.extend(
                    field for field in key["fields"] if field not in expected_fields
                )
            assert node["item_fields"] == expected_fields
    assert node_count == EXPECTED_TREE_NODES
    assert scored_node_count == EXPECTED_SCORED_NODES

    withheld = {row["task_id"] for row in rows if row["instruction"] is None}
    assert withheld == {
        "forbes_250_claims",
        "forbes_250_cross",
        "forbes_250_errors",
        "hbcu_proxy_directors",
    }
    for row in rows:
        instruction = (
            REPO_ROOT
            / "datasets"
            / "wandr"
            / row["task_id"].replace("_", "-")
            / "instruction.md"
        ).read_bytes()
        assert row["instruction_sha256"] == hashlib.sha256(instruction).hexdigest()
        if row["instruction"] is not None:
            assert row["instruction"].encode() == instruction
    affected = {row["task_id"] for row in rows if not row["self_contained"]}
    assert affected == {
        "forbes_250_claims",
        "forbes_250_cross",
        "forbes_250_errors",
        "hbcu_proxy_directors",
        "mozambique_districts",
        "portugal_municipalities",
    }

    answer_schema = SUBMISSION_CONTRACT["properties"]["answer"]
    assert answer_schema == {"type": "object", "additionalProperties": True}


def verify_assets(output: Path) -> None:
    secret_patterns = (
        re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        re.compile(rb"\bhf_[A-Za-z0-9]{30,}\b"),
        re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        re.compile(rb"\bAKIA[A-Z0-9]{16}\b"),
    )

    def assert_no_secrets(value: bytes, label: object) -> None:
        assert not any(pattern.search(value) for pattern in secret_patterns), label

    excluded = _jsonl(output / "auxiliary" / "excluded-artifacts.jsonl")
    excluded_paths = {record["path"] for record in excluded}
    actual_paths = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in REPO_ROOT.glob("reference/wandr_tasks/*/artifacts/**/*")
        if path.is_file()
    }
    assert excluded_paths == actual_paths
    assert all(record["included"] is False for record in excluded)

    package_files = [path for path in output.rglob("*") if path.is_file()]
    for record in excluded:
        artifact = REPO_ROOT / record["path"]
        assert record["sha256"] == _sha256(artifact)
        assert record["size"] == artifact.stat().st_size
        artifact_bytes = artifact.read_bytes()
        assert all(artifact_bytes not in path.read_bytes() for path in package_files)

    verify_source_bundle(output)
    source_index = json.loads(
        (output / SOURCE_BUNDLE_INDEX_PATH).read_text(encoding="utf-8")
    )
    bundled_paths = []
    for shard in source_index["shards"]:
        shard_path = output / shard["path"]
        assert shard_path.stat().st_size < SOURCE_SHARD_MAX_BYTES
        records = _jsonl(shard_path)
        bundled_paths.extend(record["path"] for record in records)
        for record in records:
            assert_no_secrets(record["content"].encode("utf-8"), record["path"])
            assert "artifacts" not in Path(record["path"]).parts
    assert bundled_paths == sorted(bundled_paths)
    assert len(bundled_paths) == 4_916
    assert source_index["file_count"] == len(bundled_paths)

    source_manifest = _jsonl(output / "auxiliary" / "source-files.jsonl")
    assert all(
        _sha256(REPO_ROOT / record["path"]) == record["sha256"]
        for record in source_manifest
    )
    evaluator = _jsonl(output / "evaluator" / "index.jsonl")
    assert len(evaluator) == EXPECTED_TREE_NODES
    source_paths = {record["path"] for record in source_manifest}
    assert all(set(record["spec_paths"]).issubset(source_paths) for record in evaluator)

    for path in package_files:
        path.read_text(encoding="utf-8", errors="strict")
        assert path.stat().st_size < MAX_UPLOAD_FILE_BYTES
        assert_no_secrets(path.read_bytes(), path)


def verify_card_and_stock_load(output: Path) -> None:
    metadata = DatasetCard.load(output / "README.md").data.to_dict()
    assert metadata["license"] == "other"
    assert metadata["license_name"] == "wandr-apache-2.0-with-third-party-notices"
    assert re.fullmatch(r"[a-z0-9-.]+", metadata["license_name"])
    assert metadata["license_link"] == "LICENSE"
    assert "arxiv:2608.14747" in metadata["tags"]
    assert "information-retrieval" in metadata["tags"]
    assert metadata["task_categories"] == ["question-answering", "text-retrieval"]
    assert "arxiv" not in metadata
    config = metadata["configs"][0]
    assert config["data_files"] == [
        {"split": "test", "path": "data/test.jsonl"},
        {"split": "smoke", "path": "data/smoke.jsonl"},
    ]

    citation = (output / "CITATION.bib").read_text(encoding="utf-8")
    assert "doi={10.48550/arXiv.2608.14747}" in citation
    assert "author={Polshkov, Vitaliy and Pitera, Marcin and Yang, Jeremy" in citation

    expected_test = _jsonl(output / "data" / "test.jsonl")
    expected_smoke = _jsonl(output / "data" / "smoke.jsonl")
    loaded = load_dataset(str(output))
    assert set(loaded) == {"test", "smoke"}
    loaded_test = loaded["test"]
    loaded_smoke = loaded["smoke"]
    assert len(loaded_test) == EXPECTED_TEST_TASKS
    assert len(loaded_smoke) == EXPECTED_SMOKE_TASKS
    assert loaded_test.to_list() == expected_test
    assert loaded_smoke.to_list() == expected_smoke
    assert loaded_test.features == loaded_smoke.features
    assert loaded_test.features.to_dict() == EXPECTED_FEATURES
    streamed_test = load_dataset(str(output), split="test", streaming=True)
    streamed_smoke = load_dataset(str(output), split="smoke", streaming=True)
    assert list(streamed_test) == expected_test
    assert list(streamed_smoke) == expected_smoke
    assert streamed_test.features == loaded_test.features
    assert streamed_smoke.features == loaded_smoke.features


def verify_manifest(output: Path) -> None:
    manifest = json.loads(
        (output / "release-manifest.json").read_text(encoding="utf-8")
    )
    records = {record["path"]: record for record in manifest["files"]}
    expected_paths = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file() and path.name != "release-manifest.json"
    }
    assert set(records) == expected_paths
    for relative_path, record in records.items():
        path = output / relative_path
        assert record["size"] == path.stat().st_size
        assert record["sha256"] == _sha256(path)


class FakeHubApi:
    def __init__(self, private_states: list[bool]) -> None:
        self.private_states = iter(private_states)
        self.calls: list[tuple[str, dict[str, object]]] = []

    def create_repo(self, **kwargs: object) -> None:
        self.calls.append(("create_repo", kwargs))

    def repo_info(self, **kwargs: object) -> object:
        self.calls.append(("repo_info", kwargs))
        return SimpleNamespace(private=next(self.private_states))

    def upload_folder(self, **kwargs: object) -> None:
        self.calls.append(("upload_folder", kwargs))


def verify_private_publish_guard(output: Path) -> None:
    api = FakeHubApi([True, True])
    publish_private(api, output, "perplexity-ai/wandr")
    assert api.calls[0][0] == "create_repo"
    assert api.calls[0][1]["private"] is True
    assert [name for name, _ in api.calls] == [
        "create_repo",
        "repo_info",
        "upload_folder",
        "repo_info",
    ]
    public_api = FakeHubApi([False])
    try:
        publish_private(public_api, output, "perplexity-ai/wandr")
    except RuntimeError:
        pass
    else:
        raise AssertionError("publish helper accepted a public repository")
    assert "upload_folder" not in [name for name, _ in public_api.calls]

    with tempfile.TemporaryDirectory(prefix="wandr-hf-tampered-") as directory:
        tampered = Path(directory) / "release"
        shutil.copytree(output, tampered)
        with (tampered / "README.md").open("a", encoding="utf-8") as card_file:
            card_file.write("\n")
        tampered_api = FakeHubApi([True, True])
        try:
            publish_private(tampered_api, tampered, "perplexity-ai/wandr")
        except ValueError:
            pass
        else:
            raise AssertionError(
                "publish helper accepted a file with a mismatched hash"
            )
        assert tampered_api.calls == []


def verify_determinism(output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="wandr-hf-repeat-") as directory:
        repeated = Path(directory) / "release"
        export(repeated)
        assert _file_hashes(output) == _file_hashes(repeated)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    export(output)
    verify_rows(output)
    verify_assets(output)
    verify_card_and_stock_load(output)
    verify_manifest(output)
    verify_private_publish_guard(output)
    verify_determinism(output)
    shutil.rmtree(output / "cache", ignore_errors=True)
    print(f"HF export verification OK: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
