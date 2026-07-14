"""Public RIA firm growth and operations signals.

Structure:
  ria_signals:
      [firm,
       signal_facet in {dated_growth_or_footprint_signal,
       operations_or_infrastructure_signal, transaction_or_integration_signal,
       platform_or_service_model_signal},
       url]

100 firms x 4 signal facets of public firm evidence. Regulatory and ADV-derived
profile evidence is useful for firm validity and identity context, but the
listed facets center on public growth, transactions, and dedicated operations
or platform / service-model signals. Ordinary acquisition announcements are not
intended to satisfy the non-transaction operations or platform facets merely by
mentioning post-close resources, support, or the acquired firm's generic
service offering.
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
    RIASignalsJudgment,
)

HERE = Path(__file__).parent

SIGNAL_FACETS = {
    "dated_growth_or_footprint_signal",
    "operations_or_infrastructure_signal",
    "transaction_or_integration_signal",
    "platform_or_service_model_signal",
}

FIRM = KeySpec("firm", required=100)
SIGNAL_FACET = KeySpec("signal_facet", required=len(SIGNAL_FACETS))
URL = KeySpec("url", required=1)

CONFIG = TaskConfig(
    name="ria_signals",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    key_hierarchy=[FIRM, SIGNAL_FACET, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "signal_facet": CanonKeyConfig(norm=exact_set(SIGNAL_FACETS), llm=False),
                "url": CanonKeyConfig(norm=url_norm, llm=False),
            },
        ),
        judge=JudgeConfig(
            schema=RIASignalsJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "firm": JudgeKeyConfig(
                    prompt_section_template=(
                        HERE / "prompts" / "judge_firm_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
            },
        ),
        dedup=DedupConfig(
            keys={
                "firm": DedupKeyConfig(
                    prompt_section_template=(
                        HERE / "prompts" / "dedup_firm_section_template.md.jinja"
                    )
                    .read_text()
                    .strip(),
                ),
                "signal_facet": DedupKeyConfig(distance=exact_match, llm=False),
                "url": DedupKeyConfig(distance=exact_match, llm=False),
            },
        ),
    ),
)
