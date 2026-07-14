# Relay

Relay is a Harbor agent for remote endpoints that produce files. It snapshots a
task workspace, renders one provider-neutral prompt, invokes a configured
endpoint, validates the returned paths, and materializes the files back into
the Harbor workspace.

Tasks can declare required outputs in `task.toml`. Relay discovers that contract
automatically and requires every declared file before the verifier starts.

## Setup

Relay is a member of the repository's uv workspace. From the repository root:

```bash
uv --no-config sync --locked
```

The root wrapper adds `agents/` to `PYTHONPATH`, which makes
`relay.agent:RelayAgent` importable by Harbor.

## Harbor Configuration

Relay models are provider-qualified. The prefix selects a provider adapter and
the suffix is passed to that provider as its model or product name:

```yaml
agents:
  - import_path: relay.agent:RelayAgent
    model_name: openai/gpt-5.5
    kwargs:
      max_full_restarts: 1
      request:
        reasoning_effort: low
      endpoint:
        delivery_channel: sandbox
```

`kwargs.request` contains provider request options. `kwargs.endpoint` contains
session and delivery options. Relay core treats both mappings as opaque and
keeps provider-specific behavior in `providers/`.

## Providers

Relay includes these provider integrations:

| Provider prefix | Credential | Delivery | Primary request option |
| --- | --- | --- | --- |
| `openai` | `OPENAI_API_KEY` | `sandbox` | `reasoning_effort` |
| `anthropic` | `ANTHROPIC_API_KEY` | `sandbox` | `speed` |
| `perplexity` | `PERPLEXITY_API_KEY` | `share` | `reasoning_effort` |
| `exa` | `EXA_API_KEY` | `output` | `effort` |
| `parallel` | `PARALLEL_API_KEY` | `output` | `processor` |
| `gemini` | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `output` | `reasoning_effort` |

The provider's configured delivery method is authoritative:

- `sandbox`: collect files written in a provider sandbox;
- `share`: collect files exposed through a provider file-sharing API;
- `stdout`: collect files emitted by dedicated file-read tool calls;
- `output`: parse explicit file fences from the final response.

Relay does not silently fall back to another delivery method.

## File Contract

A task declares required outputs as literal workspace-relative paths:

```toml
[metadata]
required_file_paths = [
  "result.jsonl",
  "reports/details.json",
]
```

Relay reads this metadata from Harbor's resolved task directory, normalizes and
deduplicates the paths in declaration order, adds them to the endpoint prompt,
and requires each file to be present and non-empty. If the metadata key is
absent, the task has no task-owned output contract. Agent-level
`required_file_paths` are additive and normalized against the same workspace
root; unlike task metadata, they may use an absolute path below that root.

All produced paths are normalized relative to the Harbor workspace. Relative
paths and absolute paths below the configured workspace root (by default,
`/workspace`) are accepted. Empty or non-normalized paths, absolute paths
outside that root, duplicate normalized paths, missing required files, and
empty required files fail the attempt.

Before writing, Relay rejects existing symlink components below the workspace
root and existing symlink file targets. Harbor exposes uploads by path rather
than by a directory file descriptor, so this check is not race-free if another
process mutates the workspace during materialization. Relay assumes exclusive
workspace access for that short phase.

The default snapshot exclusions omit VCS/cache directories, `.env` variants
except `.env.example`, common private-key and certificate bundles, and common
AWS, Azure, Google Cloud, Docker, Kubernetes, and SSH credential locations.
Explicit `exclude_globs` replace those defaults, so callers that override them
are responsible for excluding credentials.

Useful agent options include:

- `include_globs` and `exclude_globs` for workspace snapshot selection;
- `max_files`, `max_file_bytes`, and `max_total_file_bytes` for prompt bounds;
- `required_file_paths` for additional required output paths;
- `max_full_restarts` for explicit whole-attempt restarts.

Providers retain and poll an existing durable run identity across transient
status or result failures. A full restart creates a new provider run and occurs
only through Relay's bounded restart policy.

Token usage and cost are cumulative across full restarts. A returned endpoint
result is authoritative for its attempt; a final `endpoint.usage` event remains
the fallback when an attempt fails after reporting usage. If any billed attempt
reports usage without a known cost, the cumulative cost remains unknown rather
than understating spend.

## Observability

Each Harbor trial records Relay artifacts under its `agent/` directory:

- `events.jsonl`: provider-neutral lifecycle, reasoning, tool, usage, and file
  events;
- `trajectory.json`: ATIF projection of the event ledger;
- `status.json`: current or terminal Relay state;
- `prompt.md`: rendered endpoint prompt;
- `final-message.md`: provider final text;
- `result.json`: normalized result metadata and produced files.

Observability never substitutes for delivery. A successful run must still
materialize every required file into the workspace.
