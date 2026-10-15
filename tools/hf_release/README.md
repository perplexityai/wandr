# Hugging Face dataset release

This directory exports the pinned WANDR source snapshot as a directly loadable,
dataset-only Hugging Face repository. It never runs WANDR tasks or evaluators.

Generate and verify the private-staging payload from the repository root:

```bash
uv --no-config run --project tools/hf_release --locked \
  python tools/hf_release/export.py --output /tmp/wandr-hf
uv --no-config run --project tools/hf_release --locked \
  python tools/hf_release/test_export.py --output /tmp/wandr-hf
```

The export is intentionally pinned to source commit
`ccb0baeb96f1c77a48e47f92122c57479ee99700`. It refuses to run if any release
input differs from that snapshot. To prove reproducibility, the test suite
exports twice and compares every byte.

The upload root is text-only. Primary data lives in `data/test.jsonl` and
`data/smoke.jsonl`; the dataset card explicitly selects only those files as
Hugging Face splits. The lossless source snapshot is represented by
`auxiliary/source-bundle-index.json` and deterministic compact JSONL shards
smaller than 5 MB. Each source record contains its repository path, exact UTF-8
content, byte size, SHA-256, role, and pinned source URL. Verification decodes
every shard, re-encodes every source, and compares it byte-for-byte with the
pinned checkout. No Parquet, tarball, dataset script, or other binary file is
placed in the upload root; every file is also checked to remain below 10 MB.

The exporter excludes every `reference/wandr_tasks/**/artifacts/**` file and
checks that excluded bytes do not enter the package. Four generated solver
instructions embed excluded material and are represented by a null
`instruction`, exact SHA-256, explicit dependency metadata, and a pinned source
link. This preserves the task inventory without silently editing benchmark
semantics or redistributing the evidence.

## Private upload

Only an authorized release owner should upload. The helper requires an explicit
confirmation flag, creates the dataset as private, and verifies privacy before
and after upload. It also re-hashes the complete manifest file set before making
any Hugging Face API call:

```bash
uv --no-config run --project tools/hf_release --locked \
  python tools/hf_release/publish_private.py \
  --folder /tmp/wandr-hf \
  --repo-id perplexity-ai/wandr \
  --confirm-private-staging
```

Do not change dataset visibility as part of staging. Publishing or running paid
evaluation remains a separate, explicitly approved operation.
