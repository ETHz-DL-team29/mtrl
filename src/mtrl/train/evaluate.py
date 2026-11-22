"""Greedy evaluation of a policy on a segment set (in-training validation and
scripts/eval_adapter.py share this, so the numbers are comparable).

Per segment: gate result, MetricX-QE, reference MetricX and sentence chrF++ (when a
reference exists). Every non-empty output is scored with MetricX, also when it fails the
gate, so `qe_all` shows what a QE-only metric would report (a copied source scores well).
Per direction: means of those plus corpus chrF++ and `reward` (gate x (1 - QE/25)).
"""
from __future__ import annotations

from collections import defaultdict
from statistics import mean

from mtrl.common.records import direction_of


def score_outputs(segs, rollouts, lang_cfgs, *, scorer, lid_model, copy_ratio_max: float = 0.8) -> list[dict]:
    from sacrebleu.metrics import CHRF

    from mtrl.scoring.reward import reward
    from mtrl.scoring.rule_gate import gate, ym_gate

    chrf = CHRF(word_order=2)
    rows = []
    for seg, r, lang in zip(segs, rollouts, lang_cfgs):
        ok, why = gate(seg, r.translation, r.parse_ok, lang, lid_model=lid_model, copy_ratio_max=copy_ratio_max)
        rows.append({"seg_id": seg.seg_id, "direction": seg.direction, "src": seg.src, "ref": seg.ref,
                     "hyp": r.translation, "gate_ok": ok, "gate_reason": why,
                     "ym_gate_ok": ym_gate(seg, r.translation, r.parse_ok, lang)[0],
                     "finish_reason": r.finish_reason, "n_tokens": r.n_translation_tokens,
                     "qe": None, "metricx_ref": None,
                     "chrf": chrf.sentence_score(r.translation, [seg.ref]).score if seg.ref else None})
    idx = [i for i, row in enumerate(rows) if row["hyp"].strip()]
    if idx:
        srcs = [rows[i]["src"] for i in idx]
        hyps = [rows[i]["hyp"] for i in idx]
        for i, v in zip(idx, scorer.metricx(srcs, hyps)):
            rows[i]["qe"] = v
        ref_idx = [i for i in idx if rows[i]["ref"]]
        if ref_idx:
            vals = scorer.metricx([rows[i]["src"] for i in ref_idx], [rows[i]["hyp"] for i in ref_idx],
                                  [rows[i]["ref"] for i in ref_idx])
            for i, v in zip(ref_idx, vals):
                rows[i]["metricx_ref"] = v
    for row in rows:
        row["reward"] = reward(row["gate_ok"], row["qe"]) if row["qe"] is not None else 0.0
    return rows


def summarize(rows: list[dict]) -> dict:
    """{direction: {...}, "all": {...}}; "all" averages the per-direction values."""
    from sacrebleu.metrics import CHRF

    def m(xs):
        xs = [x for x in xs if x is not None]
        return round(mean(xs), 4) if xs else None

    by = defaultdict(list)
    for r in rows:
        by[r["direction"]].append(r)
    out = {}
    for d, rs in sorted(by.items()):
        reasons = defaultdict(int)
        for r in rs:
            reasons[r["gate_reason"]] += 1
        with_ref = [r for r in rs if r["ref"]]
        out[d] = {"n": len(rs), "gate_pass": m([float(r["gate_ok"]) for r in rs]),
                  "ym_gate_pass": m([float(r["ym_gate_ok"]) for r in rs]),
                  "qe_all": m([r["qe"] for r in rs]), "metricx_ref": m([r["metricx_ref"] for r in rs]),
                  "reward": m([r["reward"] for r in rs]),
                  "chrf": round(CHRF(word_order=2).corpus_score([r["hyp"] for r in with_ref],
                                                                 [[r["ref"] for r in with_ref]]).score, 2)
                  if with_ref else None,
                  "truncated": m([float(r["finish_reason"] == "length") for r in rs]),
                  "gate_reasons": dict(reasons)}
    keys = ["gate_pass", "ym_gate_pass", "qe_all", "metricx_ref", "reward", "chrf", "truncated"]
    out["all"] = {k: m([v[k] for v in out.values()]) for k in keys}
    out["all"]["n"] = len(rows)
    return out


def evaluate(model, tok, segs, lang_cfgs, *, template, thinking, max_new_tokens, batch_size,
             model_name, scorer, lid_model, copy_ratio_max=0.8):
    from mtrl.generation.hf_generate import generate_greedy

    was_training = model.training
    model.eval()
    rolls = generate_greedy(model, tok, segs, lang_cfgs, template=template, thinking=thinking,
                            max_new_tokens=max_new_tokens, batch_size=batch_size, model_name=model_name)
    if was_training:
        model.train()
    rows = score_outputs(segs, rolls, lang_cfgs, scorer=scorer, lid_model=lid_model, copy_ratio_max=copy_ratio_max)
    return rows, summarize(rows)


def directions_of(rows) -> list[str]:
    return sorted({direction_of(r["seg_id"]) for r in rows})
