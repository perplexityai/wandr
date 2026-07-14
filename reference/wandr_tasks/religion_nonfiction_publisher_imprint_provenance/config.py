"""Religion-adjacent nonfiction publisher/imprint public provenance.

Structure:
  religion_nonfiction_publisher_imprint_provenance:
      [publisher_type in {religious_trade_publisher, academic_religion_press, general_house_religion_imprint},
       publisher_or_imprint,
       evidence_facet in {submission_posture, catalog_representation, ecosystem_context},
       url]

The closed publisher_type axis preserves distribution across trade, academic, and general-house imprint contexts while the open publisher_or_imprint key preserves discovery value. The evidence_facet dispatch forces official submission posture, official catalog/list representation, and entity-specific ecosystem context per publisher or imprint, reducing collapse into directory harvesting, repeated about pages, or recommendation-style publisher lists.
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
    ReligionNonfictionPublisherImprintProvenanceJudgment,
)

HERE = Path(__file__).parent

PUBLISHER_TYPES = {
    "religious_trade_publisher": (
        "a trade, independent, denominational, or ministry-facing publisher or imprint whose public nonfiction list "
        "is framed around Christian, theology, faith-and-culture, church/ministry, spirituality, or comparable "
        "religion-adjacent readerships"
    ),
    "academic_religion_press": (
        "a university press, academic-society press, scholarly publisher, or scholarly imprint/program with public "
        "religious studies, theology, biblical studies, church history, philosophy-of-religion, or comparable "
        "religion nonfiction publishing"
    ),
    "general_house_religion_imprint": (
        "a distinct religion, faith, spirituality, theology, or religion-adjacent nonfiction imprint or publishing "
        "program inside a broader general trade or mainstream publishing house"
    ),
}

EVIDENCE_FACETS = {
    "submission_posture": (
        "the entity's public book-proposal or manuscript-submission posture, including direct, agented-only, "
        "invited, conference-only, closed, or no-unsolicited posture"
    ),
    "catalog_representation": (
        "the entity's official catalog, list, series, subject, or title evidence showing representative in-scope "
        "nonfiction publishing"
    ),
    "ecosystem_context": (
        "entity-specific publishing-ecosystem context from a parent house, association, conference, directory/profile, "
        "trade article, or comparable public source"
    ),
}

PUBLISHER_TYPE = KeySpec("publisher_type", required=len(PUBLISHER_TYPES))
PUBLISHER_OR_IMPRINT = KeySpec("publisher_or_imprint", required=20)
EVIDENCE_FACET = KeySpec("evidence_facet", required=len(EVIDENCE_FACETS))
URL = KeySpec("url", required=1)

_PUBLISHER_OR_IMPRINT_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_publisher_or_imprint_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_PUBLISHER_OR_IMPRINT_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_publisher_or_imprint_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="religion_nonfiction_publisher_imprint_provenance",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={
        "publisher_types": PUBLISHER_TYPES,
        "evidence_facets": EVIDENCE_FACETS,
    },
    key_hierarchy=[PUBLISHER_TYPE, PUBLISHER_OR_IMPRINT, EVIDENCE_FACET, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "publisher_type": CanonKeyConfig(
                    norm=exact_set(set(PUBLISHER_TYPES)),
                    llm=False,
                ),
                "evidence_facet": CanonKeyConfig(
                    norm=exact_set(set(EVIDENCE_FACETS)),
                    llm=False,
                ),
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=ReligionNonfictionPublisherImprintProvenanceJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "publisher_or_imprint": _PUBLISHER_OR_IMPRINT_JUDGE,
            },
        ),
        dedup=DedupConfig(
            keys={
                "publisher_type": DedupKeyConfig(distance=exact_match, llm=False),
                "publisher_or_imprint": _PUBLISHER_OR_IMPRINT_DEDUP,
                "evidence_facet": DedupKeyConfig(distance=exact_match, llm=False),
                "url": _URL_DEDUP,
            },
        ),
    ),
)
