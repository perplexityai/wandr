"""Public business-banking and fintech-banking product evidence.

Structure:
  business_banking_products:
      [provider,
       provider_product_plan(fields=provider,product_plan),
       evidence_facet in {product_feature, pricing_fee, rate_or_yield,
       eligibility_limit, bank_disclosure, app_platform, independent_review,
       customer_sentiment},
       url]

The task is an open-provider product evidence atlas. The closed facet set gives
source-role pressure without turning the provider universe into a canon list.
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
    BusinessBankingProductsJudgment,
)

HERE = Path(__file__).parent

EVIDENCE_FACET_DESCRIPTIONS = {
    "product_feature": "provider-owned product, help, legal, or app-platform pages that state a concrete capability, packaging claim, feature availability, or feature caveat.",
    "pricing_fee": "provider-owned pricing, fee-schedule, account-agreement, terms, or legal pages. Third-party reviews can mention prices only under `independent_review`, not as pricing truth.",
    "rate_or_yield": "provider-owned rate/APY/yield/legal pages. Third-party restatements and customer comments do not carry the rate truth.",
    "eligibility_limit": "provider-owned product/help/terms/legal pages carrying eligibility, geography, business-type, plan-availability, or transaction-limit evidence.",
    "bank_disclosure": "provider-owned legal or disclosure pages carrying partner-bank, FDIC, sweep/program-bank, card-issuer, not-a-bank, or pass-through-insurance language. Regulatory/bank pages can support bank identity, but a bank identity page alone does not prove the provider-product relationship.",
    "app_platform": "Apple App Store, Google Play, or comparable platform pages for app packaging, developer identity, platform feature descriptions, ratings, review counts, version history, or platform-visible disclosures.",
    "independent_review": "independent review, press, trade, or editorial pages for reviewer framing, public interpretation, noted strengths/limits, or source-visible tensions.",
    "customer_sentiment": "app reviews, Trustpilot-like surfaces, marketplace reviews, or other customer-review pages for customer-observable sentiment only.",
}
EVIDENCE_FACETS = set(EVIDENCE_FACET_DESCRIPTIONS)
EVIDENCE_FACET_BULLETS = "\n".join(
    f"- `{facet}`: {description}"
    for facet, description in EVIDENCE_FACET_DESCRIPTIONS.items()
)

PROVIDER = KeySpec("provider", required=30)
PROVIDER_PRODUCT_PLAN = KeySpec(
    "provider_product_plan",
    fields=("provider", "product_plan"),
    required=1,
)
EVIDENCE_FACET = KeySpec("evidence_facet", required=6)
URL = KeySpec("url", required=1)

_PROVIDER_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_provider_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_PROVIDER_PRODUCT_PLAN_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_provider_product_plan_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="business_banking_products",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={
        "evidence_facet_bullets": EVIDENCE_FACET_BULLETS,
    },
    key_hierarchy=[PROVIDER, PROVIDER_PRODUCT_PLAN, EVIDENCE_FACET, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "evidence_facet": CanonKeyConfig(
                    norm=exact_set(EVIDENCE_FACETS),
                    llm=False,
                ),
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=BusinessBankingProductsJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "provider": JudgeKeyConfig(
                    prompt_section_template=(
                        HERE / "prompts" / "judge_provider_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
                "provider_product_plan": JudgeKeyConfig(
                    prompt_section_template=(
                        HERE
                        / "prompts"
                        / "judge_provider_product_plan_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
            },
        ),
        dedup=DedupConfig(
            keys={
                "provider": _PROVIDER_DEDUP,
                "provider_product_plan": _PROVIDER_PRODUCT_PLAN_DEDUP,
                "evidence_facet": DedupKeyConfig(distance=exact_match, llm=False),
                "url": _URL_DEDUP,
            },
        ),
    ),
)
