"""US cardiac-surgery procedure segments and public evidence signals.

Structure:
  us_cardiac_surgery_signals: [procedure_segment, evidence_signal, url]
      leaf judge: dated public source evidence supports a procedure-segment signal while preserving source role, scope, denominator, methodology, and caveats

`procedure_segment` is open-set because public sources use overlapping grains
(isolated CABG, AVR+CABG, mitral repair/replacement, robotic CABG, adult
cardiac surgery totals, etc.). `evidence_signal` is a closed dispatch axis:
partial coverage across signal families is meaningful, so this is one task
rather than a rigid complete matrix or conjunctive subtask tree.
"""

from pathlib import Path

from src.config import (
    CanonConfig,
    CanonKeyConfig,
    DedupConfig,
    DedupKeyConfig,
    EvalConfig,
    JudgeConfig,
    JudgeKeyConfig,
    KeySpec,
    TaskConfig,
    exact_match,
    exact_set,
    url_norm,
)
from schemas.judgment import (
    CardiacSurgerySignalJudgment,
)

HERE = Path(__file__).parent

EVIDENCE_SIGNALS = [
    "procedure_volume",
    "disease_or_patient_pool",
    "economic_or_payment",
    "device_or_installed_base",
    "robotic_specific_or_limit",
    "methodology_scope_or_conflict",
]

PROCEDURE_SEGMENT = KeySpec("procedure_segment", required=12)
EVIDENCE_SIGNAL = KeySpec("evidence_signal", required=4)
URL = KeySpec("url", required=1)

_PROCEDURE_SEGMENT_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_procedure_segment_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_PROCEDURE_SEGMENT_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_procedure_segment_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_EVIDENCE_SIGNAL_CANON = CanonKeyConfig(
    norm=exact_set(set(EVIDENCE_SIGNALS)), llm=False
)
_EVIDENCE_SIGNAL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="us_cardiac_surgery_signals",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={
        "evidence_signals": EVIDENCE_SIGNALS,
    },
    key_hierarchy=[PROCEDURE_SEGMENT, EVIDENCE_SIGNAL, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "evidence_signal": _EVIDENCE_SIGNAL_CANON,
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=CardiacSurgerySignalJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "procedure_segment": _PROCEDURE_SEGMENT_JUDGE,
            },
        ),
        dedup=DedupConfig(
            keys={
                "procedure_segment": _PROCEDURE_SEGMENT_DEDUP,
                "evidence_signal": _EVIDENCE_SIGNAL_DEDUP,
                "url": _URL_DEDUP,
            },
        ),
    ),
)
