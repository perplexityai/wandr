"""Airport biometric border-control deployments with program-level sidecars.

Structure:
  airport_biometric_border_gates:
      [border_jurisdiction,
       border_program{border_jurisdiction,program_or_authority},
       airport_deployment{border_jurisdiction,program_or_authority,airport,flow_or_checkpoint},
       url]
  .passenger_flow_rules:
      [border_program{border_jurisdiction,program_or_authority},
       passenger_flow_rule{border_jurisdiction,program_or_authority,flow_or_cohort},
       url]
  .biometric_governance:
      [border_program{border_jurisdiction,program_or_authority},
       url]

The root asks for concrete airport/checkpoint deployment proof. The sidecars
study the same named program or authority at program scope: official passenger
flow/use rules and official biometric-data governance.
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
    url_norm,
)
from biometric_governance.schemas.judgment import (
    BiometricGovernanceJudgment,
)
from passenger_flow_rules.schemas.judgment import (
    PassengerFlowRulesJudgment,
)
from schemas.judgment import (
    AirportBiometricBorderGatesJudgment,
)

HERE = Path(__file__).parent

BORDER_JURISDICTION = KeySpec("border_jurisdiction", required=20)
BORDER_PROGRAM_PER_JURISDICTION = KeySpec(
    "border_program",
    fields=("border_jurisdiction", "program_or_authority"),
    required=1,
)
BORDER_PROGRAM_TOTAL = KeySpec(
    "border_program",
    fields=("border_jurisdiction", "program_or_authority"),
    required=20,
)
AIRPORT_DEPLOYMENT = KeySpec(
    "airport_deployment",
    fields=("border_jurisdiction", "program_or_authority", "airport", "flow_or_checkpoint"),
    required=2,
)
PASSENGER_FLOW_RULE = KeySpec(
    "passenger_flow_rule",
    fields=("border_jurisdiction", "program_or_authority", "flow_or_cohort"),
    required=2,
)
URL = KeySpec("url", required=1)

_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)

_BORDER_JURISDICTION_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_border_jurisdiction_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_BORDER_PROGRAM_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_border_program_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_AIRPORT_DEPLOYMENT_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_airport_deployment_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_PASSENGER_FLOW_RULE_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE
        / "passenger_flow_rules"
        / "prompts"
        / "dedup_passenger_flow_rule_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

_BORDER_JURISDICTION_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_border_jurisdiction_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_BORDER_PROGRAM_JUDGE_ROOT = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_border_program_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_AIRPORT_DEPLOYMENT_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_airport_deployment_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_BORDER_PROGRAM_JUDGE_PASSENGER = JudgeKeyConfig(
    prompt_section_template=(
        HERE
        / "passenger_flow_rules"
        / "prompts"
        / "judge_border_program_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_PASSENGER_FLOW_RULE_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE
        / "passenger_flow_rules"
        / "prompts"
        / "judge_passenger_flow_rule_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_BORDER_PROGRAM_JUDGE_GOVERNANCE = JudgeKeyConfig(
    prompt_section_template=(
        HERE
        / "biometric_governance"
        / "prompts"
        / "judge_border_program_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)

CONFIG = TaskConfig(
    name="airport_biometric_border_gates",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    key_hierarchy=[
        BORDER_JURISDICTION,
        BORDER_PROGRAM_PER_JURISDICTION,
        AIRPORT_DEPLOYMENT,
        URL,
    ],
    eval=EvalConfig(
        canon=CanonConfig(keys={"url": _URL_CANON}),
        judge=JudgeConfig(
            schema=AirportBiometricBorderGatesJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "border_jurisdiction": _BORDER_JURISDICTION_JUDGE,
                "border_program": _BORDER_PROGRAM_JUDGE_ROOT,
                "airport_deployment": _AIRPORT_DEPLOYMENT_JUDGE,
            },
        ),
        dedup=DedupConfig(
            keys={
                "border_jurisdiction": _BORDER_JURISDICTION_DEDUP,
                "border_program": _BORDER_PROGRAM_DEDUP,
                "airport_deployment": _AIRPORT_DEPLOYMENT_DEDUP,
                "url": _URL_DEDUP,
            },
        ),
    ),
    subtasks={
        "passenger_flow_rules": TaskConfig(
            name="passenger_flow_rules",
            task_template=(
                HERE / "passenger_flow_rules" / "prompts" / "task_template.md.jinja"
            )
            .read_text()
            .strip(),
            key_hierarchy=[
                BORDER_PROGRAM_TOTAL,
                PASSENGER_FLOW_RULE,
                URL,
            ],
            eval=EvalConfig(
                canon=CanonConfig(keys={"url": _URL_CANON}),
                judge=JudgeConfig(
                    schema=PassengerFlowRulesJudgment,
                    prompt_section_template=(
                        HERE
                        / "passenger_flow_rules"
                        / "prompts"
                        / "judge_section_template.md.jinja"
                    ).read_text(),
                    keys={
                        "border_program": _BORDER_PROGRAM_JUDGE_PASSENGER,
                        "passenger_flow_rule": _PASSENGER_FLOW_RULE_JUDGE,
                    },
                ),
                dedup=DedupConfig(
                    keys={
                        "border_program": _BORDER_PROGRAM_DEDUP,
                        "passenger_flow_rule": _PASSENGER_FLOW_RULE_DEDUP,
                        "url": _URL_DEDUP,
                    },
                ),
            ),
        ),
        "biometric_governance": TaskConfig(
            name="biometric_governance",
            task_template=(
                HERE / "biometric_governance" / "prompts" / "task_template.md.jinja"
            )
            .read_text()
            .strip(),
            key_hierarchy=[
                BORDER_PROGRAM_TOTAL,
                URL,
            ],
            eval=EvalConfig(
                canon=CanonConfig(keys={"url": _URL_CANON}),
                judge=JudgeConfig(
                    schema=BiometricGovernanceJudgment,
                    prompt_section_template=(
                        HERE
                        / "biometric_governance"
                        / "prompts"
                        / "judge_section_template.md.jinja"
                    ).read_text(),
                    keys={"border_program": _BORDER_PROGRAM_JUDGE_GOVERNANCE},
                ),
                dedup=DedupConfig(
                    keys={
                        "border_program": _BORDER_PROGRAM_DEDUP,
                        "url": _URL_DEDUP,
                    },
                ),
            ),
        ),
    },
)
