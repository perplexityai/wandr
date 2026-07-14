"""Fielded perception-guided robot deployments.

Structure:
  robot_vision_deployments:
      [use_case in {warehouse_parcel_handling, manufacturing_line_operations,
       recycling_material_sorting, agri_food_field_operations},
       use_case_deployment_case(fields=use_case,deployment_case),
       evidence_role in {provider_stack_detail,
       independent_deployment_confirmation},
       url]

The task is deliberately use-case-first rather than vendor-first. Closed
use-case and evidence-role keys set the coverage target; the open compound
use_case_deployment_case key dedups by customer/operator, site or bounded
rollout, task/process, and provider/technology context. Source-role dispatch
separates provider-origin technical stack evidence from non-provider confirmation
so one rich case study cannot satisfy every evidence role for a deployment case.
"""

from pathlib import Path

from src.config import (
    CanonConfig,
    CanonKeyConfig,
    DedupConfig,
    DedupKeyConfig,
    EvalConfig,
    exact_match,
    exact_set,
    JudgeConfig,
    JudgeKeyConfig,
    KeySpec,
    TaskConfig,
    url_norm,
)
from schemas.judgment import (
    RobotVisionDeploymentJudgment,
)

HERE = Path(__file__).parent

USE_CASES = {
    "warehouse_parcel_handling",
    "manufacturing_line_operations",
    "recycling_material_sorting",
    "agri_food_field_operations",
}

EVIDENCE_ROLES = {
    "independent_deployment_confirmation",
    "provider_stack_detail",
}

assert len(USE_CASES) == 4, f"USE_CASES must have 4 entries, has {len(USE_CASES)}"
assert len(EVIDENCE_ROLES) == 2, (
    f"EVIDENCE_ROLES must have 2 entries, has {len(EVIDENCE_ROLES)}"
)

USE_CASE = KeySpec("use_case", required=len(USE_CASES))
USE_CASE_DEPLOYMENT_CASE = KeySpec(
    "use_case_deployment_case",
    fields=("use_case", "deployment_case"),
    required=18,
)
EVIDENCE_ROLE = KeySpec("evidence_role", required=len(EVIDENCE_ROLES))
URL = KeySpec("url", required=1)

_USE_CASE_DEPLOYMENT_CASE_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_use_case_deployment_case_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)

_USE_CASE_DEPLOYMENT_CASE_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_use_case_deployment_case_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)

_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="robot_vision_deployments",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    key_hierarchy=[USE_CASE, USE_CASE_DEPLOYMENT_CASE, EVIDENCE_ROLE, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "use_case": CanonKeyConfig(norm=exact_set(USE_CASES), llm=False),
                "evidence_role": CanonKeyConfig(
                    norm=exact_set(EVIDENCE_ROLES),
                    llm=False,
                ),
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=RobotVisionDeploymentJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={"use_case_deployment_case": _USE_CASE_DEPLOYMENT_CASE_JUDGE},
        ),
        dedup=DedupConfig(
            keys={
                "use_case": DedupKeyConfig(distance=exact_match, llm=False),
                "use_case_deployment_case": _USE_CASE_DEPLOYMENT_CASE_DEDUP,
                "evidence_role": DedupKeyConfig(distance=exact_match, llm=False),
                "url": _URL_DEDUP,
            },
        ),
    ),
)
