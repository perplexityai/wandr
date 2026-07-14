"""Text rollup viewer for WANDR task outputs.

Renders the scoremap, composed tree, standalone trees, records, and optional
deep-dive sections as plain text with box-drawing tree connectors.

For large record content, the footer prints absolute paths to `debug/*.jsonl`
files so the main report stays compact.

Usage (CLI):

    uv --quiet --no-config run --locked python -m sidecars.viewer_text <wandr_metrics.json> -o out.txt
"""

from __future__ import annotations

import argparse
import shlex
from collections.abc import Callable, Mapping
from itertools import groupby
from pathlib import Path
from typing import Any

import orjson
from src.components import (
    BROWSER_REPLAY_JSONL,
    BROWSER_URL_CACHE_JSONL,
    CANON_ENTITY_CACHE_JSONL,
    CANON_REPLAY_JSONL,
    DEBUG_DIR_NAME,
    DEDUP_REPLAY_JSONL,
    FETCH_REPLAY_JSONL,
    FETCH_URL_CACHE_JSONL,
    JUDGE_EVAL_CACHE_JSONL,
    JUDGE_REPLAY_JSONL,
    SUBMISSION_REPLAY_JSONL,
    TRIAGE_REPLAY_JSONL,
    TRIAGE_URL_CACHE_JSONL,
)

from sidecars.report import (
    METRIC_LABELS,
    SCOREMAP_WIDTH,
    render_scoremap,
    report_from_metrics_file,
)

WIDTH = 120
ELLIPSIS = "…"
MODULE_NAME = "sidecars.viewer_text"
DEBUG_JSONL_FILES = (
    (
        "judge",
        JUDGE_REPLAY_JSONL,
        "per-record judge output (verdict, sub-criteria, scratch)",
    ),
    ("submission", SUBMISSION_REPLAY_JSONL, "per-record submitted output"),
    ("fetch-cache", FETCH_URL_CACHE_JSONL, "fetched page text per URL"),
    ("fetch", FETCH_REPLAY_JSONL, "per-record fetch-lane output"),
    ("triage", TRIAGE_REPLAY_JSONL, "triage / source-eligibility decisions"),
    (
        "triage-cache",
        TRIAGE_URL_CACHE_JSONL,
        "triage calls keyed by eval fingerprint and URL",
    ),
    ("browser", BROWSER_REPLAY_JSONL, "browser fallback output"),
    ("browser-cache", BROWSER_URL_CACHE_JSONL, "browser fallback cache keyed by URL"),
    ("canon", CANON_REPLAY_JSONL, "canonification output"),
    ("canon-cache", CANON_ENTITY_CACHE_JSONL, "canonification calls keyed by entity"),
    ("dedup", DEDUP_REPLAY_JSONL, "dedup calls"),
    ("judge-cache", JUDGE_EVAL_CACHE_JSONL, "judge calls keyed by judged evidence"),
)
DEBUG_JSONL_BY_LABEL = {
    label: (filename, desc) for label, filename, desc in DEBUG_JSONL_FILES
}
RECORD_DEBUG_LABELS = ("judge", "submission", "fetch-cache")
COLLAPSIBLE_NODE_TYPES = frozenset({"pad", "deficit_marker"})

__all__ = [
    "render_config",
    "render_instruction",
    "render_record",
    "render_report_text",
]

# Tree-drawing glyphs.  Stick to box-drawing block — universally rendered,
# stable widths, copy-paste-safe.
T_LAST = "└─ "
T_MORE = "├─ "
T_TRUNK = "│  "
T_PAST = "   "
type ReportNode = dict[str, Any]
type Report = dict[str, Any]


# ── helpers ──────────────────────────────────────────────────────────────


def _truncate(text: str, limit: int) -> str:
    text = (text or "").replace("\n", " ").replace("\r", " ").strip()
    if limit <= 0:
        return ""
    if len(text) <= limit:
        return text
    if limit == 1:
        return ELLIPSIS
    return text[: limit - 1] + ELLIPSIS


def _fmt_pct(value: Any) -> str:
    if value is None:
        return "  —  "
    return f"{value * 100:5.1f}%"


def _fmt_int(value: Any) -> str:
    if value is None:
        return "—"
    return f"{int(value):,}"


def _truth_glyph(value: Any) -> str:
    if value is True:
        return "✓"
    if value is False:
        return "✗"
    return "·"


def _box_line(width: int, content: str) -> str:
    avail = width - 2
    return "│" + _truncate(content, avail).ljust(avail) + "│"


def _box_top(width: int, title: str) -> str:
    inner_width = width - 2
    label = _truncate(f" {title.strip()} ", inner_width - 4)
    return "╭" + "──" + label + ("─" * (inner_width - 2 - len(label))) + "╮"


# ── tree walker ──────────────────────────────────────────────────────────


def _task_label(node: ReportNode) -> str:
    return f"[{node.get('name') or '?'}]"


def _key_level_label(node: ReportNode) -> str:
    required = node.get("required")
    supplied = node.get("supplied_count")
    invalid = node.get("invalid") or {}
    meta_bits = [
        *(
            [f"{supplied or 0}/{required if required is not None else '—'}"]
            if supplied is not None or required is not None
            else []
        ),
        *([f"invalid={invalid['count']}"] if invalid.get("count") else []),
    ]
    return " ".join(
        [
            f".{node.get('key') or '?'}",
            *(["(" + " · ".join(meta_bits) + ")"] if meta_bits else []),
        ]
    )


def _entity_label(node: ReportNode) -> str:
    value = node.get("value") or node.get("entity_id") or "?"
    marker = "*" if node.get("is_canonical") else " "
    return f"{marker} {_truncate(str(value), 80)}"


def _leaf_label(node: ReportNode) -> str:
    record_index = node.get("record_idx")
    record_tag = f" #{record_index}" if record_index is not None else ""
    return f"{_truth_glyph(node.get('verdict'))} {_truncate(node.get('url') or '', 80)}{record_tag}"


NODE_LABELS: dict[str, Callable[[ReportNode], str]] = {
    "task": _task_label,
    "key_level": _key_level_label,
    "entity": _entity_label,
    "merged_group": lambda _n: "[merged_group]",
    "leaf": _leaf_label,
    "deficit_marker": lambda _n: "[deficit]",
    "deficit_marker_run": lambda node: f"[deficit ×{node.get('count')}]",
    "pad": lambda _n: "[pad]",
    "pad_run": lambda node: f"[pad ×{node.get('count')}]",
}


def _node_label(node: ReportNode) -> str:
    node_type = str(node.get("type") or "?")
    return NODE_LABELS.get(node_type, lambda _node: f"[{node_type}]")(node)


def _node_scores_tag(node: ReportNode) -> str:
    scores = (node.get("scores") or {}).get("full") or {}
    if all(scores.get(metric) is None for metric, _label in METRIC_LABELS):
        return ""
    return "  " + " ".join(
        f"{label}={_fmt_pct(scores.get(metric)).strip()}"
        for metric, label in METRIC_LABELS
    )


def _collapse_marker_runs(children: list[ReportNode]) -> list[ReportNode]:
    collapsed: list[ReportNode] = []
    for node_type, run_iter in groupby(children, key=lambda child: child.get("type")):
        run = list(run_iter)
        if node_type in COLLAPSIBLE_NODE_TYPES and len(run) > 1:
            collapsed.append({"type": f"{node_type}_run", "count": len(run)})
        else:
            collapsed.extend(run)
    return collapsed


def _render_tree(node: ReportNode) -> list[str]:
    lines: list[str] = []
    _render_tree_inner(node, "", True, lines, root=True)
    return lines


def _render_tree_inner(
    node: ReportNode,
    prefix: str,
    is_last: bool,
    lines: list[str],
    root: bool = False,
) -> None:
    if root:
        label = _node_label(node) + _node_scores_tag(node)
        lines.append(label)
    else:
        leg = T_LAST if is_last else T_MORE
        label = _node_label(node) + _node_scores_tag(node)
        lines.append(prefix + leg + label)

    children = _collapse_marker_runs(list(node.get("children") or []))
    next_prefix = "" if root else prefix + (T_PAST if is_last else T_TRUNK)
    for index, child in enumerate(children):
        _render_tree_inner(
            child, next_prefix, index == len(children) - 1, lines, root=False
        )


# ── sections ─────────────────────────────────────────────────────────────


def _section_rule(title: str, width: int) -> str:
    """`── TITLE ──────────────…` rule for section boundaries."""
    head = f"── {title} "
    return head + "─" * max(3, width - len(head))


def _pre_lines(text: str, width: int, indent: str = "  ") -> list[str]:
    if not text:
        return [f"{indent}(empty)"]
    lines: list[str] = []
    for para in text.rstrip().splitlines() or [""]:
        lines.extend(_wrap(para, width, indent=indent) or [indent.rstrip()])
    return lines


def _variant_items(variants: Mapping[str, Any]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    items = []
    for mode in ("raw", "bound", "rendered"):
        text = str(variants.get(mode) or "")
        if not text or text in seen:
            continue
        seen.add(text)
        items.append((mode, text))
    return items


def _variant_lines(label: str, variants: Mapping[str, Any], width: int) -> list[str]:
    lines: list[str] = []
    for mode, text in _variant_items(variants):
        lines.append(f"  {label} / {mode}")
        lines.extend(_pre_lines(text, width, indent="    "))
        lines.append("")
    return lines


def _component_prompt_lines(
    kind: str, prompt_variants: dict[str, Any], width: int
) -> list[str]:
    if not prompt_variants:
        return []
    lines = [f"  {kind}"]
    component = prompt_variants.get("component") or {}
    for part in ("section", "full"):
        lines.extend(
            _variant_lines(f"{kind}.component.{part}", component.get(part) or {}, width)
        )
    for key, key_variants in (prompt_variants.get("per_key") or {}).items():
        for part in ("section", "full"):
            lines.extend(
                _variant_lines(
                    f"{kind}.{key}.{part}", (key_variants or {}).get(part) or {}, width
                )
            )
    return lines


def _field_count(groups: list[dict[str, Any]]) -> int:
    return sum(
        len(group.get("fields") or []) + 2 * len(group.get("pairs") or [])
        for group in groups
    )


def _prompt_variant_count(prompt_variants: dict[str, Any]) -> int:
    if not prompt_variants:
        return 0
    component = prompt_variants.get("component") or {}
    count = sum(
        len(_variant_items(component.get(part) or {})) for part in ("section", "full")
    )
    return count + sum(
        len(_variant_items((key_variants or {}).get(part) or {}))
        for key_variants in (prompt_variants.get("per_key") or {}).values()
        for part in ("section", "full")
    )


def _overview_summary_lines(node: dict[str, Any], depth: int = 0) -> list[str]:
    pad = "  " * depth
    name = node.get("name") or "?"
    summary = node.get("key_summary") or ""
    schema_count = _field_count(node.get("schema_groups") or [])
    prompt_count = sum(
        _prompt_variant_count(node.get(f"{kind}_variants") or {})
        for kind in ("judge", "canon", "dedup")
    )
    lines = [
        f"{pad}- {name} {summary}  schema_fields={schema_count} prompt_views={prompt_count}".rstrip()
    ]
    for child in node.get("children") or []:
        lines.extend(_overview_summary_lines(child, depth + 1))
    return lines


def _schema_lines(node: dict[str, Any]) -> list[str]:
    groups = node.get("schema_groups") or []
    if not groups:
        return ["  schema: (empty)"]
    lines = ["  schema:"]
    for group in groups:
        lines.append(f"    {group.get('label') or '?'}")
        for field in group.get("fields") or []:
            desc = f" — {field.get('description')}" if field.get("description") else ""
            lines.append(f"      {field.get('name')} : {field.get('type')}{desc}")
        for pair in group.get("pairs") or []:
            lines.append(f"      {pair.get('stem')}")
            for slot in ("satisfied", "supported"):
                field = pair.get(slot) or {}
                desc = (
                    f" — {field.get('description')}" if field.get("description") else ""
                )
                lines.append(f"        {field.get('name')} : {field.get('type')}{desc}")
    return lines


def _overview_node_lines(node: dict[str, Any], width: int, depth: int = 0) -> list[str]:
    pad = "  " * depth
    name = node.get("name") or "?"
    summary = node.get("key_summary") or ""
    lines = [f"{pad}{name} {summary}".rstrip(), ""]
    lines.extend(f"{pad}{line}" for line in _schema_lines(node))
    lines.append("")
    lines.extend(
        f"{pad}{line}"
        for line in _variant_lines(
            "task_template", node.get("task_template_variants") or {}, width
        )
    )
    for kind in ("judge", "canon", "dedup"):
        component_lines = _component_prompt_lines(
            kind, node.get(f"{kind}_variants") or {}, width
        )
        if component_lines:
            lines.extend(f"{pad}{line}" for line in component_lines)
            lines.append("")
    for child in node.get("children") or []:
        lines.extend(_overview_node_lines(child, width, depth + 1))
    return lines


def _command_lines(report: Report, flag: str) -> list[str]:
    metrics_json = str(report.get("metrics_json") or "<wandr_metrics.json>")
    metrics_arg = (
        metrics_json if metrics_json.startswith("<") else shlex.quote(metrics_json)
    )
    return [
        f"  uv --quiet --no-config run --locked python -m {MODULE_NAME} \\",
        f"      {metrics_arg} {flag}",
    ]


def _config_section(report: Report, width: int, *, detailed: bool = False) -> list[str]:
    overview = report.get("overview") or {}
    lines = [_section_rule("CONFIGURATION", width), ""]
    if not detailed:
        lines.append(
            "Text view shows configuration as an index. Print the full schema/prompt material with:"
        )
        lines.append("")
        lines.extend(_command_lines(report, "--config"))
        lines.append("")
        lines.append("Task tree:")
        lines.extend(_overview_summary_lines(overview))
        return lines
    lines.extend(_overview_node_lines(overview, width))
    return lines


def _instruction_section(
    report: Report, width: int, *, detailed: bool = False
) -> list[str]:
    instruction = report.get("full_instruction") or {}
    variants = _variant_items(instruction)
    lines = [_section_rule("FULL INSTRUCTION", width), ""]
    if not variants:
        return [*lines, "Instruction is not embedded in this metrics file."]
    if not detailed:
        text = variants[0][1]
        lines.append(f"Instruction is {len(text):,} characters. Print it with:")
        lines.append("")
        lines.extend(_command_lines(report, "--instruction"))
        return lines
    lines.extend(_variant_lines("instruction", instruction, width))
    return lines


def _composed_section(report: Report, width: int) -> list[str]:
    composed_tree = report.get("composed_tree") or {}
    lines = [_section_rule("COMPOSED", width), ""]
    lines.extend(_render_tree(composed_tree))
    return lines


def _standalone_section(report: Report, width: int) -> list[str]:
    trees = report.get("standalone_trees") or []
    lines = [_section_rule("STANDALONE", width), ""]
    if not trees:
        lines.append("(no standalone trees)")
        return lines
    for index, standalone_tree in enumerate(trees):
        if index > 0:
            lines.append("")
        name = standalone_tree.get("name")
        lines.append(f"# {name}")
        lines.extend(_render_tree(standalone_tree.get("tree") or {}))
    return lines


def _field_decompositions_section(report: Report, width: int) -> list[str]:
    sections = report.get("field_decompositions") or []
    lines = [_section_rule("STANDALONE FIELD DECOMPOSITIONS", width), ""]
    for section in sections:
        if len(lines) > 2:
            lines.append("")
        lines.append(f"# {section.get('name')}")
        lines.extend(_field_decomposition_lines(section))
    if len(lines) == 2:
        lines.append("(no field decompositions)")
    return lines


def _field_decomposition_lines(section: Mapping[str, Any]) -> list[str]:
    fields = section.get("fields") or []
    if not fields:
        return []

    field_w = min(42, max(5, *(len(str(row.get("field") or "")) for row in fields)))
    lines: list[str] = []
    lines.append(
        f"  {'field':<{field_w}} {'true':>5} {'false':>5} "
        f"{'prec':>7} {'rec':>7} {'f1':>7}"
    )
    for row in fields:
        field = str(row.get("field") or "")
        lines.append(
            f"  {_truncate(field, field_w):<{field_w}} "
            f"{_fmt_int(row.get('true')):>5} "
            f"{_fmt_int(row.get('false')):>5} "
            f"{_fmt_pct(row.get('soft_precision')).strip():>7} "
            f"{_fmt_pct(row.get('soft_recall')).strip():>7} "
            f"{_fmt_pct(row.get('soft_f1')).strip():>7}"
        )
    return lines


def _records_section(report: Report, width: int) -> list[str]:
    """Short records summary — one row per record with a few key fields.
    For the full content, point at the JSONL files in the footer."""
    records = report.get("records") or []
    lines = [_section_rule("RECORDS", width), ""]
    if not records:
        lines.append("(no records)")
        return lines
    # Column widths chosen to fit `width=120` comfortably.
    # idx(4) · task(24) · verdict(2) · conf(4) · url-tail(42) · item-summary(rest)
    col_idx = 4
    col_task = 24
    col_v = 2
    col_c = 4
    col_url = 42
    col_item = max(20, width - col_idx - col_task - col_v - col_c - col_url - 6)

    header = (
        f"{'#':>{col_idx}}  "
        f"{'task':<{col_task}}  "
        f"{'v':<{col_v}}  "
        f"{'cnf':<{col_c}}  "
        f"{'url-tail':<{col_url}}  "
        f"item"
    )
    lines.append(header)
    lines.append("-" * width)

    for record in records:
        judge = record.get("judge") or {}
        confidence = judge.get("confidence")
        url = record.get("url") or ""
        url_tail = _truncate(url.rsplit("/", 1)[-1] or url, col_url)
        task = _truncate(record.get("task_name") or "", col_task)
        item_summary = _truncate(_format_item(record.get("item") or {}), col_item)
        record_index = record.get("_idx", "")
        lines.append(
            f"{record_index:>{col_idx}}  "
            f"{task:<{col_task}}  "
            f"{_truth_glyph(judge.get('verdict')):<{col_v}}  "
            f"{str(confidence) if confidence is not None else '—':<{col_c}}  "
            f"{url_tail:<{col_url}}  "
            f"{item_summary}"
        )
    return lines


def _format_item(item: dict) -> str:
    """Best-effort one-line summary of the entity-id keys."""
    # Strip helper fields (`url_canon`, `_*`).
    fields = {
        name: value
        for name, value in item.items()
        if not (name.startswith("_") or name.endswith("_canon"))
    }
    if not fields:
        return ""
    return "  ".join(
        f"{name}={_truncate(str(value), 60)!r}" for name, value in fields.items()
    )


def _debug_dir(report: Report) -> Path | None:
    output_dir = report.get("output_dir")
    if not output_dir:
        return None
    debug = Path(output_dir) / DEBUG_DIR_NAME
    return debug if debug.exists() else None


def _footer_jsonl(report: Report, width: int) -> list[str]:
    """Point at the underlying JSONL files so users can grep the raw content
    instead of waiting on the text rollup to surface it."""
    debug = _debug_dir(report)
    if debug is None:
        return []
    lines = [_section_rule("RAW (consult the JSONL directly)", width), ""]
    task = report.get("task_name") or ""
    submission_fp = report.get("submission_fp") or ""
    lines.append(
        f"# JSONL match fields: _prov._task_root={task!r} / _prov._submission_fp={submission_fp!r}"
    )
    lines.append("")
    for _, fname, desc in DEBUG_JSONL_FILES:
        path = debug / fname
        marker = "✓" if path.exists() else "✗"
        lines.append(f"  {marker}  {path}")
        lines.append(f"       {desc}")
    return lines


def _footer_deepdive(report: Report, width: int) -> list[str]:
    """How to drill into one record's full judgment breakdown.  The same
    module + `--idx <N>` does it — pull the index from the `#` column in the
    RECORDS section above.
    """
    lines = [_section_rule("DEEP-DIVE A RECORD", width), ""]
    lines.append(
        "Pretty-print one record's full judgment + excerpts + page-text preview:"
    )
    lines.append("")
    lines.extend(_command_lines(report, "--idx <N>"))
    lines.append("")
    lines.append("(N is the `#` column in the RECORDS section above.)")
    return lines


# ── per-record deep-dive ─────────────────────────────────────────────────


def _wrap(text: str, width: int, indent: str = "  ") -> list[str]:
    """Soft-wrap a long string to `width` cols, with `indent` prefixed to
    every line.  Preserves paragraph breaks on `\\n\\n`."""
    text = (text or "").strip()
    if not text:
        return []
    lines: list[str] = []
    for paragraph in text.split("\n\n"):
        words = paragraph.split()
        current_line = indent
        for word in words:
            if len(current_line) + len(word) + 1 > width and current_line.strip():
                lines.append(current_line.rstrip())
                current_line = indent + word + " "
            else:
                current_line += word + " "
        if current_line.strip():
            lines.append(current_line.rstrip())
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def _overview_node(root: dict[str, Any], name: str) -> dict[str, Any]:
    if root.get("name") == name:
        return root
    return next(
        (
            found
            for child in root.get("children") or []
            for found in [_overview_node(child, name)]
            if found
        ),
        {},
    )


def _judge_keys(report: Report, record: dict[str, Any]) -> list[str]:
    judge = record.get("judge") or {}
    node = _overview_node(report.get("overview") or {}, record.get("task_name") or "")
    ordered = [
        key
        for key in node.get("schema_field_order") or []
        if key in judge and key != "reasoning"
    ]
    seen = set(ordered) | {"reasoning"}
    return [*ordered, *(key for key in judge if key not in seen)]


def _record_at(report: Report, record_index: int) -> dict[str, Any]:
    records = report.get("records") or []
    record = next((item for item in records if item.get("_idx") == record_index), None)
    if record is None and 0 <= record_index < len(records):
        record = records[record_index]
    if record is None:
        raise IndexError(
            f"record #{record_index} not in report (have {len(records)} records)"
        )
    return record


def _record_item(record: dict[str, Any]) -> dict[str, Any]:
    return {
        name: value
        for name, value in (record.get("item") or {}).items()
        if not (name.startswith("_") or name.endswith("_canon"))
    }


def _record_header(
    report: Report, record: dict[str, Any], record_index: int, width: int
) -> list[str]:
    judge = record.get("judge") or {}
    verdict = judge.get("verdict")
    confidence = judge.get("confidence")
    title = f"{report.get('task_name') or '?'} #{record_index}  {_truth_glyph(verdict)} verdict={verdict} · confidence={confidence}"
    lines = [
        _box_top(width, title),
        _box_line(width, f"  task:  {record.get('task_name') or '?'}"),
        _box_line(width, f"  url:   {_truncate(record.get('url') or '', width - 12)}"),
    ]
    if record.get("page_title"):
        lines.append(
            _box_line(
                width, f"  page:  {_truncate(record.get('page_title'), width - 12)}"
            )
        )
    return [*lines, "╰" + ("─" * (width - 2)) + "╯", ""]


def _record_item_section(item: dict[str, Any], width: int) -> list[str]:
    lines = [_section_rule("ITEM (entity-id fields)", width)]
    if not item:
        return [*lines, "  (empty)", ""]
    key_width = max(len(name) for name in item)
    return [
        *lines,
        *(f"  {name.ljust(key_width)} : {value}" for name, value in item.items()),
        "",
    ]


def _record_excerpts_section(record: dict[str, Any], width: int) -> list[str]:
    excerpts = record.get("excerpts") or []
    lines = [_section_rule(f"EXCERPTS ({len(excerpts)})", width)]
    if not excerpts:
        return [*lines, "  (none)", ""]
    for index, excerpt in enumerate(excerpts, 1):
        lines.append(f"  {index}.")
        lines.extend(_wrap(str(excerpt), width, indent="     "))
    return [*lines, ""]


def _record_answer_section(record: dict[str, Any], width: int) -> list[str]:
    answer = record.get("answer") or {}
    lines = [_section_rule("ANSWER (task-specific)", width)]
    if not answer:
        return [*lines, "  (empty)", ""]
    encoded = orjson.dumps(answer, option=orjson.OPT_INDENT_2).decode().splitlines()
    return [*lines, *("  " + line for line in encoded), ""]


def _record_comment_section(record: dict[str, Any], width: int) -> list[str]:
    if not (comment := record.get("__comment")):
        return []
    return [
        _section_rule("RECORD COMMENT", width),
        *_wrap(str(comment), width, indent="  "),
        "",
    ]


def _record_judge_section(
    report: Report, record: dict[str, Any], width: int
) -> list[str]:
    judge = record.get("judge") or {}
    lines = [_section_rule("JUDGE", width)]
    if judge.get("reasoning"):
        lines.extend(
            ["  reasoning:", *_wrap(judge["reasoning"], width, indent="    "), ""]
        )
    sub_keys = _judge_keys(report, record)
    if sub_keys:
        key_width = max(len(key) for key in sub_keys)
        lines.extend(
            f"  {key.ljust(key_width)} : {str(judge.get(key)):<8}  "
            f"{_truth_glyph(judge.get(key)) if isinstance(judge.get(key), bool) else ' '}"
            for key in sub_keys
        )
    return [*lines, ""]


def _record_preview_section(record: dict[str, Any], width: int) -> list[str]:
    if not (preview := record.get("page_text_preview")):
        return []
    return [
        _section_rule("PAGE TEXT PREVIEW", width),
        *_wrap(preview, width, indent="  "),
        "",
    ]


def _record_raw_location_section(
    report: Report, record: dict[str, Any], item: dict[str, Any], width: int
) -> list[str]:
    if not (debug := _debug_dir(report)):
        return []
    label_width = max(map(len, RECORD_DEBUG_LABELS))
    return [
        _section_rule("RAW LOCATION (grep these)", width),
        f"  url:         {record.get('url') or ''}",
        f"  item:        {dict(item)}",
        "",
        *(
            f"  {label + ':':<{label_width + 1}} {debug / DEBUG_JSONL_BY_LABEL[label][0]}"
            for label in RECORD_DEBUG_LABELS
        ),
    ]


def render_record(report: Report, record_index: int, width: int = WIDTH) -> str:
    """Render the full judgment breakdown for one record."""
    record = _record_at(report, record_index)
    item = _record_item(record)
    sections = [
        _record_header(report, record, record_index, width),
        _record_item_section(item, width),
        _record_excerpts_section(record, width),
        _record_answer_section(record, width),
        _record_comment_section(record, width),
        _record_judge_section(report, record, width),
        _record_preview_section(record, width),
        _record_raw_location_section(report, record, item, width),
    ]
    lines = [line for section in sections for line in section]
    return "\n".join(lines) + "\n"


# ── entrypoint ───────────────────────────────────────────────────────────


def render_report_text(report: Report, width: int = WIDTH) -> str:
    """Render the full text rollup for one task report."""
    blocks: list[list[str]] = []
    blocks.append(
        render_scoremap(report.get("scoremap") or {}, max(width, SCOREMAP_WIDTH))
        .rstrip("\n")
        .splitlines()
    )
    blocks.append([""])
    blocks.append(_config_section(report, width, detailed=False))
    blocks.append([""])
    blocks.append(_instruction_section(report, width, detailed=False))
    blocks.append([""])
    blocks.append(_composed_section(report, width))
    blocks.append([""])
    blocks.append(_standalone_section(report, width))
    blocks.append([""])
    blocks.append(_field_decompositions_section(report, width))
    blocks.append([""])
    blocks.append(_records_section(report, width))
    blocks.append([""])
    blocks.append(_footer_deepdive(report, width))
    blocks.append([""])
    blocks.append(_footer_jsonl(report, width))
    lines: list[str] = []
    for block in blocks:
        lines.extend(block)
    return "\n".join(lines) + "\n"


def render_config(report: Report, width: int = WIDTH) -> str:
    return "\n".join(_config_section(report, width, detailed=True)) + "\n"


def render_instruction(report: Report, width: int = WIDTH) -> str:
    return "\n".join(_instruction_section(report, width, detailed=True)) + "\n"


def _emit(text: str, output: Path | None, label: str) -> None:
    if output is None:
        print(text, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text)
    print(f"{label} → {output}  ({len(text)} chars)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a text rollup from WANDR metrics.",
    )
    parser.add_argument("metrics_json", type=Path)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write to file instead of stdout.",
    )
    parser.add_argument("--width", type=int, default=WIDTH)
    parser.add_argument(
        "--idx",
        type=int,
        default=None,
        help="If set, print the full judgment breakdown for a single record "
        "(by `#` index from the RECORDS section) instead of the whole task.",
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Print the full configuration/schema/prompt section instead of the main report.",
    )
    parser.add_argument(
        "--instruction",
        action="store_true",
        help="Print the full agent instruction instead of the main report.",
    )
    args = parser.parse_args()

    report = report_from_metrics_file(args.metrics_json)
    report["metrics_json"] = str(args.metrics_json)
    if args.idx is not None:
        _emit(
            render_record(report, args.idx, width=args.width),
            args.output,
            f"{report['task_name']} #{args.idx}",
        )
        return
    if args.config or args.instruction:
        chunks = []
        if args.config:
            chunks.append(render_config(report, width=args.width))
        if args.instruction:
            chunks.append(render_instruction(report, width=args.width))
        _emit(
            "\n".join(chunk.rstrip() for chunk in chunks) + "\n",
            args.output,
            report["task_name"],
        )
        return
    _emit(
        render_report_text(report, width=args.width), args.output, report["task_name"]
    )


if __name__ == "__main__":
    main()
