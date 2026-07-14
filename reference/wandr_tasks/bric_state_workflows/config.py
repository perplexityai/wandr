"""State and territory FEMA BRIC FY 2024/2025 workflow markers.

Structure:
  bric_state_workflows: [jurisdiction, marker_kind in {intake_path,state_review_path,rules_or_transition}, workflow_marker(fields=jurisdiction,marker_kind,workflow_marker), url]
      url.required=2 for corroboration; each URL independently supports a FY 2024/2025 BRIC state-specific workflow marker fitting the submitted marker_kind

The jurisdiction axis is open discovery over U.S. states, territories, and DC,
with canon used only to normalize jurisdiction names. The closed marker_kind
axis forces different local-process categories per jurisdiction. The workflow
marker axis stays open and deduped within jurisdiction/kind so distinct local
stages stay separate, while the two-URL leaf requirement makes a single
jurisdiction BRIC hub insufficient by itself.
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
    BRICStateWorkflowJudgment,
)

HERE = Path(__file__).parent

MARKER_KIND_DESCRIPTIONS = {
    "intake_path": (
        "local applicant intake or subapplicant action before state review, "
        "such as an LOI, NOI, preapplication, invited materials deadline, "
        "local FEMA GO packet due date, or required intake portal step"
    ),
    "state_review_path": (
        "state review, ranking, selection, revision, or state-to-FEMA "
        "submission handling after local intake, including review deadlines "
        "and state submission timing"
    ),
    "rules_or_transition": (
        "a BRIC-specific process rule, funding methodology, eligibility "
        "condition, procurement/applicant rule, technical-issue notice rule, "
        "or FY 2024 pending-subapplication migration, revision, resubmission, "
        "or withdrawal instruction"
    ),
}
MARKER_KINDS = set(MARKER_KIND_DESCRIPTIONS)

JURISDICTION = KeySpec("jurisdiction", required=35)
MARKER_KIND = KeySpec("marker_kind", required=len(MARKER_KIND_DESCRIPTIONS))
WORKFLOW_MARKER = KeySpec(
    "workflow_marker",
    fields=("jurisdiction", "marker_kind", "workflow_marker"),
    required=1,
)
URL = KeySpec("url", required=2)

_JURISDICTION_CANON = CanonKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "canon_jurisdiction_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_MARKER_KIND_CANON = CanonKeyConfig(norm=exact_set(MARKER_KINDS), llm=False)

_WORKFLOW_MARKER_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_workflow_marker_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)

_JURISDICTION_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)
_MARKER_KIND_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)
_WORKFLOW_MARKER_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_workflow_marker_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG: TaskConfig = TaskConfig(
    name="bric_state_workflows",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={
        "marker_kind_descriptions": MARKER_KIND_DESCRIPTIONS,
    },
    key_hierarchy=[JURISDICTION, MARKER_KIND, WORKFLOW_MARKER, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "jurisdiction": _JURISDICTION_CANON,
                "marker_kind": _MARKER_KIND_CANON,
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=BRICStateWorkflowJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "workflow_marker": _WORKFLOW_MARKER_JUDGE,
            },
        ),
        dedup=DedupConfig(
            keys={
                "jurisdiction": _JURISDICTION_DEDUP,
                "marker_kind": _MARKER_KIND_DEDUP,
                "workflow_marker": _WORKFLOW_MARKER_DEDUP,
                "url": _URL_DEDUP,
            },
        ),
    ),
)
