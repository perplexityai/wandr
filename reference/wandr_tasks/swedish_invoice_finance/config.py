"""Swedish-market invoice-finance provider evidence.

Structure:
  swedish_invoice_finance:
      [provider,
       provider_service(fields=provider, service_surface),
       evidence_role in {service, identity},
       url]

The dispatch splits the two evidence jobs that should not be collapsed: public
service evidence for a Swedish-market invoice-finance / working-capital surface,
and legal / regulatory / registration identity evidence for the provider.
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
    SwedishInvoiceFinanceJudgment,
)

HERE = Path(__file__).parent

EVIDENCE_ROLES = {
    "service": "public service, product, marketplace, embedded-finance, or concrete channel/program evidence",
    "identity": "public legal, FI/regulatory, company-registration, or official identity evidence",
}

PROVIDER = KeySpec("provider", required=120)
PROVIDER_SERVICE = KeySpec(
    "provider_service",
    fields=("provider", "service_surface"),
    required=1,
)
EVIDENCE_ROLE = KeySpec("evidence_role", required=len(EVIDENCE_ROLES))
URL = KeySpec("url", required=1)

_PROVIDER_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_provider_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_PROVIDER_SERVICE_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_provider_service_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="swedish_invoice_finance",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    extra_bindings={
        "evidence_roles": EVIDENCE_ROLES,
    },
    key_hierarchy=[
        PROVIDER,
        PROVIDER_SERVICE,
        EVIDENCE_ROLE,
        URL,
    ],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "evidence_role": CanonKeyConfig(
                    norm=exact_set(set(EVIDENCE_ROLES)),
                    llm=False,
                ),
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=SwedishInvoiceFinanceJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "provider_service": JudgeKeyConfig(
                    prompt_section_template=(
                        HERE
                        / "prompts"
                        / "judge_provider_service_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
            },
        ),
        dedup=DedupConfig(
            keys={
                "provider": _PROVIDER_DEDUP,
                "provider_service": _PROVIDER_SERVICE_DEDUP,
                "evidence_role": DedupKeyConfig(distance=exact_match, llm=False),
                "url": _URL_DEDUP,
            },
        ),
    ),
)
