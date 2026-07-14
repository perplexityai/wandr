# WANDR Task Sources

This directory contains the editable source definitions for WANDR tasks. Each
immediate child directory with a `config.py` file defines one root task. A root
may also contain nested task nodes.

Typical task sources include:

- `config.py`: the task tree, bindings, schemas, prompts, and scoring setup;
- `prompts/`: solver-facing and evaluator prompt fragments;
- `schemas/`: structured output and judgment models;
- `artifacts/`: task-owned source material required by the task or evaluator.

These directories are source data, not independently runnable Harbor packages.
The adapter renders them into self-contained packages under `datasets/wandr/`.

## Editing And Generation

Make semantic task changes here, then regenerate the corresponding Harbor
package from the repository root:

```bash
uv --no-config run --project adapters/wandr --locked wandr \
  <task_name> --overwrite
```

Regenerate the full dataset with:

```bash
uv --no-config run --project adapters/wandr --locked wandr --overwrite
```

Do not edit the generated copy under `datasets/wandr/` as a separate source of
truth. Run `./scripts/wandr check` after changing task sources or shared adapter
behavior.
