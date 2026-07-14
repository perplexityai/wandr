"""Pipeline-exercising smoke test with default `JudgmentResult` (no custom schema, no canon/dedup).

Structure:
  smoke:    [topic, url]
      leaf judge: generic JudgmentResult — verdict gates on universal signals only (excerpts_faithful AND requirements_all_satisfied AND requirements_all_supported); no per-task substantive criteria

Used to verify the framework end-to-end without measuring agent quality.
"""

from pathlib import Path

from src.config import (
    KeySpec,
    TaskConfig,
)

HERE = Path(__file__).parent

CONFIG = TaskConfig(
    name="smoke",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    key_hierarchy=[
        KeySpec("topic", required=3),
        KeySpec("url", required=2),
    ],
)
