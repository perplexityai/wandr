# WANDR Harbor Adapter

This package generates self-contained Harbor tasks under
`datasets/wandr/<task-slug>`.

## Ownership

The adapter keeps replicated state explicit:

- `reference/wandr_tasks/<task-name>/` owns task-specific configuration,
  schemas, prompts, and required artifacts.
- `src/wandr/origin/instruction_macro.md.jinja` owns the shared solver
  instruction structure.
- `src/wandr/origin/wandr_core/` owns the shared evaluator runtime and its
  locked dependencies.
- `src/wandr/task-template/` owns the Harbor environment and verifier wrapper.
- `datasets/wandr/<task-slug>/` is generated output.

Generated tasks vendor their task source and `wandr_core` so each directory can
be packaged, published, and verified independently.

## Generation

From the repository root, generate one task by its underscore-delimited WANDR
name:

```bash
uv --no-config run --project adapters/wandr --locked wandr \
  pharma_former_rd_heads --overwrite
```

Generate a selected set:

```bash
uv --no-config run --project adapters/wandr --locked wandr \
  pharma_former_rd_heads ceo_cfo_appointments \
  --overwrite
```

Generate every task:

```bash
uv --no-config run --project adapters/wandr --locked wandr --overwrite
```

When output goes to `datasets/wandr`, generation refreshes
`datasets/wandr/dataset.toml`. Existing task metadata and resource settings are
retained where appropriate, while generated verifier environment and identity
fields are refreshed.

## Generated Shape

```text
datasets/wandr/<task-slug>/
├── instruction.md
├── task.toml
├── environment/
└── tests/
    ├── manifest.json
    ├── wandr_core/
    └── wandr_task/
```

`tests/manifest.json` records each ordered WANDR task-tree node. The adapter
publishes the corresponding literal `results_<task-name>.jsonl` paths as
`metadata.required_file_paths` in `task.toml`; generic agents can enforce that
contract without understanding the WANDR manifest. The verifier always reads
those files from the workspace and never seeds or replaces them. `task.toml`
also provides public network access to the agent and verifier and forwards only
the documented WANDR and provider environment variables.

## Consistency

Do not edit a generated task as an independent source of truth. Run the full
repository check after source, evaluator, template, or generator changes:

```bash
./scripts/wandr check
```

The adapter-specific check can also run directly:

```bash
uv --no-config run --locked python adapters/wandr/src/wandr/utils/consistency.py
```

It verifies that:

- every reference task has exactly one generated task;
- generated task sources match `reference/wandr_tasks`;
- every vendored evaluator matches `origin/wandr_core`;
- generic verifier and environment files match `task-template`;
- each task's `metadata.required_file_paths` matches its task-local verifier
  manifest;
- `dataset.toml` contains the current task set and content digests.

## Fetch Boundary

The evaluator pipeline owns batching, retry and bisection, `None` handling,
persistence, and replay. Page retrieval remains behind one client call:

```python
response = await client.content.fetch(urls=urls)
pages = response.pages
```

```text
WANDR fetch node
  -> client.content.fetch(...)
       -> create one background Perplexity Agent API response
       -> poll that response to terminal state
       -> run the fetch command in its sandbox
       -> share, list, and download one validated JSON artifact
```

Per-page errors remain page data. Missing pages stay missing so the fetch node
emits `None`; batch, terminal-response, and artifact failures raise to that
node. Transport retries, polling, and same-response file retries remain inside
the client.

Set `PERPLEXITY_API_KEY` for page retrieval. The default relay model is
`google/gemini-3.1-flash-lite`; `WANDR_FETCH_MODEL` can override it.
