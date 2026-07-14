"""Attributed furniture objects with maker documentation.

Structure:
  furniture_maker_object_attributions:
      [maker, object_source_type in {collection_record, external_object_record},
       maker_object(fields=maker,object), url]
  .maker_documentation:
      [maker, url]

The root proves object-to-maker attribution across two object-source roles so a
single collection database cannot satisfy the object surface by itself.
The subtask proves maker-scope British/Irish furniture-trade documentation.
Those facts have different identity scopes, so they are composed rather than
forced into a single URL leaf.
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
from maker_documentation.schemas.judgment import (
    MakerDocumentationJudgment,
)
from schemas.judgment import (
    MakerObjectAttributionJudgment,
)

HERE = Path(__file__).parent

OBJECT_SOURCE_TYPES = {
    "collection_record",
    "external_object_record",
}

MAKER = KeySpec("maker", required=90)
OBJECT_SOURCE_TYPE = KeySpec("object_source_type", required=len(OBJECT_SOURCE_TYPES))
MAKER_OBJECT = KeySpec("maker_object", fields=("maker", "object"), required=2)
URL = KeySpec("url", required=1)

_MAKER_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_maker_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_MAKER_OBJECT_DEDUP = DedupKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "dedup_maker_object_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_MAKER_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_maker_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_MAKER_OBJECT_JUDGE = JudgeKeyConfig(
    prompt_section_template=(
        HERE / "prompts" / "judge_maker_object_section_template.md.jinja"
    )
    .read_text()
    .strip(),
)
_URL_CANON = CanonKeyConfig(norm=url_norm, llm=False)
_URL_DEDUP = DedupKeyConfig(distance=exact_match, llm=False)

CONFIG = TaskConfig(
    name="furniture_maker_object_attributions",
    task_template=(HERE / "prompts" / "task_template.md.jinja").read_text().strip(),
    key_hierarchy=[MAKER, OBJECT_SOURCE_TYPE, MAKER_OBJECT, URL],
    eval=EvalConfig(
        canon=CanonConfig(
            keys={
                "object_source_type": CanonKeyConfig(
                    norm=exact_set(OBJECT_SOURCE_TYPES),
                    llm=False,
                ),
                "url": _URL_CANON,
            },
        ),
        judge=JudgeConfig(
            schema=MakerObjectAttributionJudgment,
            prompt_section_template=(
                HERE / "prompts" / "judge_section_template.md.jinja"
            ).read_text(),
            keys={
                "maker": _MAKER_JUDGE,
                "maker_object": _MAKER_OBJECT_JUDGE,
            },
        ),
        dedup=DedupConfig(
            keys={
                "maker": _MAKER_DEDUP,
                "object_source_type": DedupKeyConfig(distance=exact_match, llm=False),
                "maker_object": _MAKER_OBJECT_DEDUP,
                "url": _URL_DEDUP,
            },
        ),
    ),
    subtasks={
        "maker_documentation": TaskConfig(
            name="maker_documentation",
            task_template=(
                HERE / "maker_documentation" / "prompts" / "task_template.md.jinja"
            )
            .read_text()
            .strip(),
            key_hierarchy=[MAKER, URL],
            eval=EvalConfig(
                canon=CanonConfig(keys={"url": _URL_CANON}),
                judge=JudgeConfig(
                    schema=MakerDocumentationJudgment,
                    prompt_section_template=(
                        HERE
                        / "maker_documentation"
                        / "prompts"
                        / "judge_section_template.md.jinja"
                    ).read_text(),
                    keys={"maker": _MAKER_JUDGE},
                ),
                dedup=DedupConfig(
                    keys={
                        "maker": _MAKER_DEDUP,
                        "url": _URL_DEDUP,
                    },
                ),
            ),
        ),
    },
)
