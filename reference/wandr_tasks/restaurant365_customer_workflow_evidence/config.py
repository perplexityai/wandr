"""Restaurant365 customer/operator workflow evidence records.

Structure:
  restaurant365_customer_workflow_evidence:
      [customer_operator, workflow_evidence_record, url]

Open customer/operator discovery is deliberate: Restaurant365 customer evidence
is public-source-derived and drifting. The measured row is one named
customer/operator workflow-evidence record: a concise label for a source-stated
Restaurant365/R365 module, workflow, use case, rollout, implementation area, or
stack role for that operator. The leaf citation must independently support that
record and its source/date context.
"""

from pathlib import Path

from src.config import (
    CanonConfig,
    CanonKeyConfig,
    DedupConfig,
    DedupKeyConfig,
    EvalConfig,
    exact_match,
    JudgeConfig,
    JudgeKeyConfig,
    KeySpec,
    TaskConfig,
    url_norm,
)
from schemas.judgment import (
    Restaurant365WorkflowEvidenceJudgment,
)

HERE = Path(__file__).parent

CUTOFF_DATE = "May 5, 2026"
WORKFLOW_BUCKETS = (
    "accounting",
    "inventory",
    "workforce_labor_scheduling",
    "payroll_hr_training",
    "operations_task_management",
    "reporting_analytics",
    "ap_lease_accounting_stack",
    "multi_location_franchise_rollout",
    "purchasing_vendor_management",
    "other_source_stated_workflow",
)
WORKFLOW_BUCKETS_TEXT = ", ".join(WORKFLOW_BUCKETS)

CUSTOMER_OPERATOR = KeySpec("customer_operator", required=55)
WORKFLOW_EVIDENCE_RECORD = KeySpec("workflow_evidence_record", required=2)
URL = KeySpec("url", required=1)

CONFIG = TaskConfig(
    name="restaurant365_customer_workflow_evidence",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={
        "cutoff_date": CUTOFF_DATE,
        "workflow_buckets": WORKFLOW_BUCKETS_TEXT,
    },
    key_hierarchy=[
        CUSTOMER_OPERATOR,
        WORKFLOW_EVIDENCE_RECORD,
        URL,
    ],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "url": CanonKeyConfig(norm=url_norm, llm=False),
            },
        ),
        judge=JudgeConfig(
            schema=Restaurant365WorkflowEvidenceJudgment,
            prompt_section_template=(HERE / "prompts" / "judge_section_template.md.jinja").read_text(),
            keys={
                "customer_operator": JudgeKeyConfig(
                    prompt_section_template=(
                        HERE / "prompts" / "judge_customer_operator_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
                "workflow_evidence_record": JudgeKeyConfig(
                    prompt_section_template=(
                        HERE / "prompts" / "judge_workflow_evidence_record_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
            },
        ),
        dedup=DedupConfig(
            keys={
                "customer_operator": DedupKeyConfig(
                    prompt_section_template=(
                        HERE / "prompts" / "dedup_customer_operator_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
                "workflow_evidence_record": DedupKeyConfig(
                    prompt_section_template=(
                        HERE / "prompts" / "dedup_workflow_evidence_record_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
                "url": DedupKeyConfig(distance=exact_match, llm=False),
            },
        ),
    ),
)
