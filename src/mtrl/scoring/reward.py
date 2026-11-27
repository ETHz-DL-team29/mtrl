"""Reward: gate x (1 - MetricX / 25). MetricX range is 0 (best) .. 25 (worst).

The zero-shot stage uses MetricX-QE. Training can also use reference-based MetricX
(`reward.mode: ref`); the formula is the same.
"""
from __future__ import annotations


def reward(gate_ok: bool, metricx_qe: float) -> float:
    return float(gate_ok) * (1.0 - min(max(metricx_qe, 0.0), 25.0) / 25.0)


def score_translations(items, *, mode: str, gate_mode: str, scorer, lid_model=None,
                       copy_ratio_max: float = 0.8) -> list[dict]:
    """Gate + MetricX + reward for training rollouts / evaluation outputs.

    items: [(segment, translation, parse_ok, lang_cfg)]. MetricX is computed only for
    outputs that pass the gate (failing ones get reward 0 and metricx None), in one
    request. Returns [{gate_ok, gate_reason, metricx, reward}] in input order.
    """
    from mtrl.scoring.rule_gate import gate, ym_gate

    out = []
    for seg, hyp, ok, lang in items:
        if gate_mode == "ym_compat":
            g = ym_gate(seg, hyp, ok, lang)
        else:
            g = gate(seg, hyp, ok, lang, lid_model=lid_model, copy_ratio_max=copy_ratio_max)
        out.append({"gate_ok": g[0], "gate_reason": g[1], "metricx": None, "reward": 0.0})
    todo = [i for i, o in enumerate(out) if o["gate_ok"]]
    if todo:
        srcs = [items[i][0].src for i in todo]
        hyps = [items[i][1].strip() for i in todo]
        refs = [items[i][0].ref for i in todo] if mode == "ref" else None
        if refs is not None and not all(refs):
            raise ValueError("reward.mode=ref needs a reference for every training segment")
        for i, v in zip(todo, scorer.metricx(srcs, hyps, refs)):
            out[i]["metricx"] = v
            out[i]["reward"] = reward(True, v)
    return out
