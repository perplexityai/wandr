# WANDR

WANDR is a benchmark for wide and deep research: structured, high-volume information
work that requires broad discovery, extensive enrichment, systematic extraction,
precise entity disambiguation, and evidence-backed answer synthesis.

Its implementation is split into four independently useful layers:

1. **WANDR source data.** `reference/wandr_tasks/` contains the editable task
   configs, schemas, prompts, and artifacts in WANDR's source format. The source
   tree is portable data and can be hosted independently of this repository.
2. **WANDR-to-Harbor adapter.** `adapters/wandr/` consumes a WANDR source tree
   and deterministically produces Harbor task packages. It owns format
   translation and packaging, not benchmark semantics.
3. **Harbor-format WANDR tasks.** `datasets/wandr/` contains the generated,
   self-contained task packages that are also published through the Harbor
   registry. Each package carries its instruction, environment, evaluator, and
   task-specific scoring material.
4. **Relay.** `agents/relay/` is a generic Harbor agent for repository-patch and
   file-output benchmarks. It adapts standard request/completion-style remote
   endpoints to Harbor by collecting their output files and materializing them
   in the task workspace; it is not WANDR-specific.

Harbor supplies the task environment and lifecycle. WANDR defines correctness
and scoring; Relay defines how endpoint output becomes workspace files.

## Quick Start

### Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Docker with a running daemon for local task environments
- API keys for the providers used by the selected config

Clone the repository and install the locked workspace:

```bash
git clone https://github.com/ppl-ai/wandr.git
cd wandr
uv --no-config sync --locked
```

Create a local environment file:

```bash
cp .env.example .env
```

Set the keys you intend to use, then run the repository checks:

```bash
./scripts/wandr check
```

The cheapest end-to-end run uses the `smoke` task and one low-effort OpenAI
solver. It still makes paid OpenAI and Perplexity API calls:

```bash
./scripts/wandr smoke-local
```

The first local run builds the task image and can take longer than subsequent
runs. Harbor writes run state and results under `jobs/`.

### E2B

E2B is optional and may add execution charges. Set `E2B_API_KEY` in `.env`, then
run the same smoke workflow in an E2B environment:

```bash
./scripts/wandr smoke-e2b
```

The E2B path builds from the checked-in task Dockerfile. It uses the same task,
Relay, and verifier contracts as the local Docker path.

## Credentials

`.env` is ignored by Git. The wrapper parses it as dotenv data before invoking
Harbor; it never executes the file as shell code. Exported environment variables
take precedence over values in `.env`.

| Variable | Used for |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI Relay runs and WANDR judge calls |
| `ANTHROPIC_API_KEY` | Anthropic Managed Agents Relay runs |
| `PERPLEXITY_API_KEY` | Perplexity Relay runs and verifier page fetching |
| `EXA_API_KEY` | Exa Agent Relay runs |
| `PARALLEL_API_KEY` | Parallel Task API Relay runs |
| `GEMINI_API_KEY` or `GOOGLE_API_KEY` | Gemini Deep Research Relay runs |
| `E2B_API_KEY` | Optional E2B execution environment |

`configs/smoke.yaml` needs OpenAI and Perplexity keys. The all-provider configs
need all six provider keys. E2B runs additionally need `E2B_API_KEY`.

## Run Configs

The checked-in configs form an increasing cost and coverage ladder:

| Config | Coverage | Purpose |
| --- | --- | --- |
| `configs/smoke.yaml` | One smoke task, one low-effort endpoint | Fast local end-to-end check |
| `configs/smoke-all.yaml` | One smoke task, all Relay endpoints at low/fast settings | Provider integration check |
| `configs/validation.yaml` | Two representative tasks across all endpoints | Standard release validation |
| `configs/wandr.yaml` | Full scored task set across all endpoints | Full benchmark run |

Run the all-provider smoke config directly through the wrapper:

```bash
./scripts/wandr run -y -c configs/smoke-all.yaml
```

Run the standard two-task validation:

```bash
./scripts/wandr validate
```

Run the full benchmark only after smoke and validation have passed:

```bash
./scripts/wandr run -y -c configs/wandr.yaml
```

These commands make paid calls to solver, fetch, and judge APIs. The validation
and full configs fan out across six providers; the full config applies that
matrix to the entire dataset and can be very expensive. Check each provider's
current pricing and account limits before starting them. Harbor does not impose
a spending cap.

Use the generic wrapper for custom Harbor arguments or edited configs:

```bash
./scripts/wandr run <harbor-run-arguments>
```

## How A Run Works

```text
Harbor task environment
  -> Relay snapshots the workspace and invokes one configured endpoint
  -> Relay materializes the endpoint's declared files in /workspace
  -> Harbor starts the task-local WANDR verifier
  -> WANDR fetches submitted pages, normalizes entities, deduplicates, and judges
  -> Harbor records rewards, diagnostics, reports, and Relay observability
```

Each generated task is independently runnable and contains:

- `instruction.md`: solver-facing task instructions;
- `task.toml`: Harbor metadata, resources, verifier environment, and the
  task-owned `metadata.required_file_paths` output contract;
- `environment/`: the public Docker build;
- `tests/wandr_task/`: task-specific configuration, schemas, prompt fragments,
  and required artifacts;
- `tests/wandr_core/`: a vendored copy of the evaluator runtime;
- `tests/manifest.json`: the ordered WANDR task names consumed by the verifier.

The task-local evaluator is deliberate. A task can be published, downloaded,
and verified without requiring a separate WANDR package at runtime.
Generated tasks do not ship example solver outputs or a bundled solver;
the verifier always grades the required files already present in `/workspace`.
Task-local tests may contain compact grader-only rubrics and task-owned public
evidence assets. Neither is copied into the agent workspace or rendered into
the solver instruction unless it is explicitly part of the task input.

## Outputs

Harbor creates `jobs/<run-id>/` with a directory per trial. The most useful
files are:

- `<trial>/result.json`: Harbor's trial result;
- `<trial>/agent/events.jsonl`: provider-neutral Relay events;
- `<trial>/agent/trajectory.json`: the ATIF trajectory;
- `<trial>/agent/status.json`: Relay lifecycle status;
- `<trial>/verifier/reward.json`: primary and named rewards;
- `<trial>/verifier/wandr_metrics.json`: WANDR metric rollups;
- `<trial>/verifier/report.html`: detailed human-readable report;
- `<trial>/verifier/wandr-details.json`: verifier diagnostics;
- `<trial>/verifier/error.json`: setup or evaluator failure, when present.

A completed zero reward is a scored result. An `error.json` means the verifier
did not produce a valid score.

## Task Development

The files under `datasets/wandr/` are generated. Make task edits in
`reference/wandr_tasks/`, shared evaluator edits in
`adapters/wandr/src/wandr/origin/wandr_core/`, and generic Harbor wrapper edits
in `adapters/wandr/src/wandr/task-template/`.

Regenerate one task by its underscore-delimited WANDR name:

```bash
uv --no-config run --project adapters/wandr --locked wandr \
  pharma_former_rd_heads --overwrite
```

Regenerate every task:

```bash
uv --no-config run --project adapters/wandr --locked wandr --overwrite
```

Generation also refreshes `datasets/wandr/dataset.toml`. Do not hand-edit a
generated task to diverge from its source or the adapter templates. The
repository check verifies task sources, vendored evaluator copies, wrapper files, and
dataset digests:

```bash
./scripts/wandr check
```

Adapter details live in [`adapters/wandr/README.md`](adapters/wandr/README.md).
Relay details live in [`agents/relay/README.md`](agents/relay/README.md).
Task-source details live in
[`reference/wandr_tasks/README.md`](reference/wandr_tasks/README.md).

## Data And Third-Party Sources

Required task artifacts can include derived public-record material. Third-party
source material remains subject to its own terms; follow linked source terms
when reusing or redistributing it.

## Troubleshooting

- `uv lock --check` failures: run `uv --no-config sync --locked` from the repository root
  and confirm that the checked-in lockfile has not been changed locally.
- Docker connection failures: start Docker and verify `docker info` succeeds.
- Missing credentials: compare `.env` with `.env.example`; the preflight check
  reports the required variables for the selected workflow.
- Provider failures: inspect `<trial>/agent/status.json`, `events.jsonl`, and
  `result.json` before retrying.
- Verifier failures: inspect `<trial>/verifier/error.json`, `setup.log`, and
  `wandr/stdio.log`. Missing reward files are verifier failures, not zero scores.
- Slow first run: allow time for the Docker or E2B image build and locked Python
  dependency installation. Later runs reuse those caches.
