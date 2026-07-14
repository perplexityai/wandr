"""NTSB marine investigation public-record publication state.

Structure:
  ntsb_marine_publication_state: [investigation, url]
      docket_state:              [investigation, url]
      report_release:            [investigation, url]

The root verifies official per-investigation identity/status pages. The two
subtasks force distinct official evidence for docket state and report-product
release/probable-cause state, preventing a CAROL export row from satisfying the
whole investigation lifecycle claim.
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
from docket_state.schemas.judgment import (
    DocketStateJudgment,
)
from report_release.schemas.judgment import (
    ReportReleaseJudgment,
)
from schemas.judgment import (
    PublicationStateJudgment,
)

HERE = Path(__file__).parent

INVESTIGATION = KeySpec(
    "investigation",
    fields=("ntsb_number", "event_title"),
    required=40,
)
URL = KeySpec("url", required=1)

COMMON_BINDINGS = {
    "accident_start": "January 1, 2021",
    "accident_end": "December 31, 2025",
}

_INVESTIGATION_CANON = CanonKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "canon_investigation_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)

_INVESTIGATION_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_investigation_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

def _canon_config() -> CanonConfig:
    return CanonConfig(
        keys={
            "investigation": _INVESTIGATION_CANON,
            "url": _URL_CANON,
        },
    )


def _dedup_config() -> DedupConfig:
    return DedupConfig(
        keys={
            "investigation": _INVESTIGATION_DEDUP,
            "url": _URL_DEDUP,
        },
    )


def _investigation_judge_config() -> JudgeKeyConfig:
    return JudgeKeyConfig(
        prompt_section_template=(
            HERE / "prompts" / "judge_investigation_section_template.md.jinja"
        )
        .read_text()
        .strip(),
    )


CONFIG = TaskConfig(
    name="ntsb_marine_publication_state",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings=COMMON_BINDINGS,
    key_hierarchy=[INVESTIGATION, URL],
    eval=EvalConfig(
        canon=_canon_config(),
        judge=JudgeConfig(
            schema=PublicationStateJudgment,
            prompt_section_template=(HERE / "prompts" / "judge_section_template.md.jinja").read_text(),
            keys={"investigation": _investigation_judge_config()},
        ),
        dedup=_dedup_config(),
    ),
    subtasks={
        "docket_state": TaskConfig(
            name="docket_state",
            task_template=(
                HERE / "docket_state" / "prompts" / "task_template.md.jinja"
            )
            .read_text()
            .strip(),
            extra_bindings=COMMON_BINDINGS,
            key_hierarchy=[INVESTIGATION, URL],
            eval=EvalConfig(
                canon=_canon_config(),
                judge=JudgeConfig(
                    schema=DocketStateJudgment,
                    prompt_section_template=(
                        HERE / "docket_state" / "prompts" / "judge_section_template.md.jinja"
                    ).read_text(),
                    keys={"investigation": _investigation_judge_config()},
                ),
                dedup=_dedup_config(),
            ),
        ),
        "report_release": TaskConfig(
            name="report_release",
            task_template=(
                HERE / "report_release" / "prompts" / "task_template.md.jinja"
            )
            .read_text()
            .strip(),
            extra_bindings=COMMON_BINDINGS,
            key_hierarchy=[INVESTIGATION, URL],
            eval=EvalConfig(
                canon=_canon_config(),
                judge=JudgeConfig(
                    schema=ReportReleaseJudgment,
                    prompt_section_template=(
                        HERE / "report_release" / "prompts" / "judge_section_template.md.jinja"
                    ).read_text(),
                    keys={"investigation": _investigation_judge_config()},
                ),
                dedup=_dedup_config(),
            ),
        ),
    },
)
