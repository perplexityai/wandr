"""Public data-center cooling capability claims from source-labeled evidence.

Structure:
  data_center_cooling:
      [claim_type, vendor, solution_claim, source_class, url]

The task is open-set over vendors, solution families, deployments, studies, and
claims. `claim_type` is a small closed dispatch axis so technical product
capabilities, exact metrics, deployment/customer references, and validated
reference-design or study claims all get coverage without forcing every vendor
to satisfy every claim arm. `vendor` is separated from the solution/claim key so
the hierarchy enforces vendor breadth. `source_class` preserves source-class
fanout and requires multiple source surfaces per claim.
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
    alias_map_set,
    exact_match,
    url_norm,
)
from schemas.judgment import (
    DataCenterCoolingJudgment,
)

HERE = Path(__file__).parent

CLAIM_TYPES = {
    "technical_product_capability": (
        "Named-product or named-solution technical capability claims, such as direct-to-chip, "
        "immersion, CDU/HDU, rear-door/rack, chiller/heat-rejection, hybrid air-liquid, "
        "waterless, evaporative, retrofit, or high-density operating capability, when the "
        "page ties that capability to a concrete product, model family, or source-framed solution."
    ),
    "numeric_metric": (
        "Exact numeric capacity, density, efficiency, water, temperature, facility-scale, "
        "or study/model metric claims."
    ),
    "deployment_or_customer_reference": (
        "Named deployment, customer/operator, counterparty, installation, case-study, or "
        "project-reference claims that include cooling-capability substance."
    ),
    "validated_reference_or_study": (
        "Validated reference-design, standards/OCP collaboration, official engineering-study, "
        "or modeled-design claims with named design scope, assumptions, or measured/model outputs."
    ),
}

CLAIM_TYPE_ALIASES = {
    "technical_product_capability": (
        "technical capability",
        "product capability",
        "solution capability",
        "named product capability",
        "cooling capability",
        "architecture capability",
    ),
    "numeric_metric": (
        "numeric",
        "metric",
        "numeric claim",
        "capacity",
        "density",
        "capacity or density",
        "efficiency metric",
        "quantitative metric",
    ),
    "deployment_or_customer_reference": (
        "deployment",
        "case study",
        "customer reference",
        "deployment reference",
        "operator announcement",
        "counterparty announcement",
        "installation",
        "project reference",
    ),
    "validated_reference_or_study": (
        "reference",
        "reference design",
        "validated design",
        "study",
        "engineering study",
        "official study",
        "modeled design",
        "ocp collaboration",
        "standards collaboration",
        "blueprint",
    ),
}

SOURCE_CLASSES = {
    "product_page": (
        "Official vendor product, product-family, or named solution page with concrete "
        "capability details, not a generic solution overview."
    ),
    "datasheet_download": "Official datasheet, brochure, technical manual, or downloadable product document.",
    "press_release": "Official vendor, investor-relations, or newsroom press release.",
    "case_study": "Official case study, customer-story, or project-reference page.",
    "operator_counterparty_page": "Official operator, customer, partner, buyer, or counterparty page.",
    "engineering_explainer": (
        "Official engineering blog, white paper, technical explainer, or study summary with "
        "capability-specific substance."
    ),
    "reference_design": "Official reference design, validated architecture, blueprint, or standards/OCP-style design page.",
}

SOURCE_CLASS_ALIASES = {
    "product_page": (
        "product",
        "product family",
        "official product page",
        "vendor product page",
        "named solution page",
    ),
    "datasheet_download": (
        "datasheet",
        "data sheet",
        "download",
        "brochure",
        "technical manual",
        "technical document",
    ),
    "press_release": (
        "press",
        "news release",
        "newsroom",
        "announcement",
        "investor release",
    ),
    "case_study": (
        "customer story",
        "deployment case study",
        "project reference",
        "case-study",
        "case study",
    ),
    "operator_counterparty_page": (
        "operator page",
        "counterparty page",
        "customer page",
        "partner page",
        "buyer page",
        "counterparty announcement",
    ),
    "engineering_explainer": (
        "blog",
        "official blog",
        "engineering blog",
        "white paper",
        "explainer",
        "study",
        "study summary",
    ),
    "reference_design": (
        "reference",
        "reference design",
        "validated design",
        "blueprint",
        "ocp design",
        "standards page",
    ),
}

CLAIM_TYPE = KeySpec("claim_type", required=len(CLAIM_TYPES))
VENDOR = KeySpec("vendor", required=10)
SOLUTION_CLAIM = KeySpec(
    "solution_claim",
    fields=("vendor", "solution", "claim"),
    required=2,
)
SOURCE_CLASS = KeySpec("source_class", required=2)
URL = KeySpec("url", required=1)

_VENDOR_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_vendor_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_VENDOR_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_vendor_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_SOLUTION_CLAIM_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_solution_claim_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_SOLUTION_CLAIM_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_solution_claim_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="data_center_cooling",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={
        "claim_types": CLAIM_TYPES,
        "source_classes": SOURCE_CLASSES,
    },
    key_hierarchy=[CLAIM_TYPE, VENDOR, SOLUTION_CLAIM, SOURCE_CLASS, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "claim_type": CanonKeyConfig(
                    norm=alias_map_set(CLAIM_TYPE_ALIASES), llm=False
                ),
                "source_class": CanonKeyConfig(
                    norm=alias_map_set(SOURCE_CLASS_ALIASES), llm=False
                ),
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=DataCenterCoolingJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "vendor": _VENDOR_JUDGE,
                "solution_claim": _SOLUTION_CLAIM_JUDGE,
            },
        ),
        dedup=DedupConfig(
            keys={
                "claim_type": DedupKeyConfig(distance=exact_match, llm=False),
                "vendor": _VENDOR_DEDUP,
                "solution_claim": _SOLUTION_CLAIM_DEDUP,
                "source_class": DedupKeyConfig(distance=exact_match, llm=False),
                "url": _URL_DEDUP,
            },
        ),
    ),
)
