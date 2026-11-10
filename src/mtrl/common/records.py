"""Record types exchanged between pipeline stages (one object per jsonl line).

Unique key of a Rollout / Score: (seg_id, sample_idx, model, thinking).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields

KEY_FIELDS = ("seg_id", "sample_idx", "model", "thinking")


class _Record:
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict):
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in names})

    def key(self) -> tuple:
        return tuple(getattr(self, k) for k in KEY_FIELDS)


@dataclass
class Segment(_Record):
    seg_id: str            # globally unique, e.g. "en-is/dev/000123"
    direction: str         # "en-is"
    src: str
    ref: str | None        # many directions have no reference
    meta: dict = field(default_factory=dict)

    def key(self) -> tuple:  # segments are keyed by seg_id only
        return (self.seg_id,)


@dataclass
class Rollout(_Record):
    seg_id: str
    sample_idx: int        # greedy = -1; samples = 0..G-1
    model: str
    thinking: bool
    temperature: float
    raw_output: str
    reasoning: str         # "" if no reasoning
    translation: str
    n_prompt_tokens: int
    n_reasoning_tokens: int
    n_translation_tokens: int
    finish_reason: str     # "stop" / "length" / ...
    parse_ok: bool
    prefix_id: str | None = None   # reasoning-prefix reuse (later); always None now


@dataclass
class Score(_Record):
    seg_id: str
    sample_idx: int
    model: str
    thinking: bool
    gate_ok: bool
    gate_reason: str       # ok / parse_fail / empty / copy_source / wrong_lang / length_ratio
    metrics: dict          # {"metricx24_qe": 3.2, ...}; missing metrics are omitted
    reward: float


# Value set of Score.gate_reason, in the order the gate checks them ("ok" first).
GATE_REASONS = ["ok", "parse_fail", "empty", "copy_source", "wrong_lang", "length_ratio"]


def direction_of(seg_id: str) -> str:
    return seg_id.split("/", 1)[0]
