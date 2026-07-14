"""Three-pass prompt markup.

Pass 1 (expand): {< >} / {<% %>} - insert section templates into macros
Pass 2 (bind):   {= =} / {=% =%} - resolve task-level parameters (bindings)
Pass 3 (render): {{ }} / {% %}   - fill record data at runtime
"""

import datetime
import re
from collections import Counter
from typing import Any

import jinja2
import jinja2.meta

from src.schemas.canon import CANONICAL_INVALID

TRIAGE_PREVIEW = 2000
PAGE_TEXT_LIMIT = 50_000
SHARE_BINDINGS_MIN_SIZE = 1024

_BIND_VAR_RE = re.compile(r"\{=\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\}")
_RAW_BLOCK_RE = re.compile(r"\{=%\s*raw\s*=%\}.*?\{=%\s*endraw\s*=%\}", re.DOTALL)


def _verbatim(value: Any) -> str:
    return "{=% raw =%}" + str(value) + "{=% endraw =%}"


def _wrap_overlap_key(text: str, key_name: str) -> str:
    """Keep a subtask overlap-key binding literal through the bind pass."""
    return _BIND_VAR_RE.sub(
        lambda match: (
            f"{{=% raw =%}}{match.group(0)}{{=% endraw =%}}"
            if match.group(1) == key_name
            else match.group(0)
        ),
        text,
    )


def _bind_ref_literal(name: Any) -> str:
    return "{=% raw =%}{= " + str(name) + " =}{=% endraw =%}"


MACRO_ENV = jinja2.Environment(
    variable_start_string="{<",
    variable_end_string=">}",
    block_start_string="{<%",
    block_end_string="%>}",
    comment_start_string="{<#",
    comment_end_string="#>}",
    undefined=jinja2.StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
    keep_trailing_newline=True,
)
MACRO_ENV.filters["verbatim"] = _verbatim
MACRO_ENV.filters["wrap_overlap_key"] = _wrap_overlap_key
MACRO_ENV.filters["bind_ref_literal"] = _bind_ref_literal


BIND_ENV = jinja2.Environment(
    variable_start_string="{=",
    variable_end_string="=}",
    block_start_string="{=%",
    block_end_string="=%}",
    comment_start_string="{=#",
    comment_end_string="#=}",
    undefined=jinja2.StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)


def _month_sub(value: Any, months: int) -> Any:
    if not isinstance(value, str):
        return value
    date = datetime.date.fromisoformat(value + "-01")
    month_offset = (date.year * 12 + date.month - 1) - months
    year, month_index = divmod(month_offset, 12)
    return datetime.date(year, month_index + 1, 1).strftime("%Y-%m")


def _month_human(value: Any) -> Any:
    return (
        datetime.date.fromisoformat(value + "-01").strftime("%B %Y")
        if isinstance(value, str)
        else value
    )


BIND_ENV.filters["month_sub"] = _month_sub
BIND_ENV.filters["month_human"] = _month_human

RENDER_ENV = jinja2.Environment(
    undefined=jinja2.StrictUndefined, trim_blocks=True, lstrip_blocks=True
)
RENDER_ENV.globals["CANONICAL_INVALID"] = CANONICAL_INVALID
RENDER_ENV.globals["TRIAGE_PREVIEW"] = TRIAGE_PREVIEW
RENDER_ENV.globals["PAGE_TEXT_LIMIT"] = PAGE_TEXT_LIMIT


def extract_bind_vars(template_str: str) -> set[str]:
    """Extract undeclared {= =} variable names from a bind-env template string."""
    return jinja2.meta.find_undeclared_variables(BIND_ENV.parse(template_str))


def expand(
    macro: str, *, share_bindings: dict[str, Any] | None = None, **kwargs: Any
) -> str:
    """Pass 1: expand a macro template with {< >} variables.

    When share_bindings is provided, bare {= name =} patterns that appear
    2+ times outside {=% raw =%} blocks AND whose bound value exceeds
    SHARE_BINDINGS_MIN_SIZE are replaced with inline references and the
    bindings are consolidated into a trailing References section. The bind
    pass then expands each shared binding exactly once. Small values stay
    inline: inlining is more readable than reference indirection.

    Operates post-expansion because only after expansion do verbatim filters
    materialize as {=% raw =%} blocks; we cannot tell from the expansions
    dict which values will be inserted raw vs verbatim-wrapped.
    """
    rendered = MACRO_ENV.from_string(macro).render(**kwargs)
    return (
        _dedup_shared_bindings(rendered, share_bindings) if share_bindings else rendered
    )


def _dedup_shared_bindings(text: str, bindings: dict[str, Any]) -> str:
    raw_spans = [match.span() for match in _RAW_BLOCK_RE.finditer(text)]

    def in_raw(position: int) -> bool:
        return any(start <= position < end for start, end in raw_spans)

    counts = Counter(
        match.group(1)
        for match in _BIND_VAR_RE.finditer(text)
        if not in_raw(match.start())
    )
    shared = {
        name
        for name, count in counts.items()
        if count >= 2 and len(str(bindings.get(name, ""))) >= SHARE_BINDINGS_MIN_SIZE
    }
    if not shared:
        return text

    def shared_binding_reference(match: re.Match[str]) -> str:
        name = match.group(1)
        return (
            f'[See "{name}" in References below]'
            if name in shared and not in_raw(match.start())
            else match.group(0)
        )

    referenced_text = _BIND_VAR_RE.sub(shared_binding_reference, text)
    references = "\n\n".join(
        f"### `{name}`\n\n{{= {name} =}}" for name in sorted(shared)
    )
    return f"{referenced_text}\n\n## References\n\n{references}\n"


def bind(template: str, bindings: dict[str, Any]) -> str:
    """Pass 2: bind {= =} task-level parameters into an expanded template."""
    return BIND_ENV.from_string(template).render(bindings)


_CONTROL_CHAR_TABLE = str.maketrans(
    {c: None for c in range(32) if c not in (9, 10, 13)}
)


def _sanitize_for_llm(value: Any) -> Any:
    return value.translate(_CONTROL_CHAR_TABLE) if isinstance(value, str) else value


def render(prompt: str, **record_vars: Any) -> str:
    """Pass 3: fill {{ }} record data into a bound prompt."""
    clean_vars = {name: _sanitize_for_llm(value) for name, value in record_vars.items()}
    return RENDER_ENV.from_string(prompt).render(**clean_vars)
