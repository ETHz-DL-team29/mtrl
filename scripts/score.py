"""Stage 2: gate + metrics + reward -> runs/{run}/scores.jsonl.

Resumable per part file (runs/{run}/score_parts/{gate,<metric>}.jsonl); each part is
keyed by (seg_id, sample_idx, model, thinking). scores.jsonl is re-assembled from the
parts at the end of every run, so it always reflects everything scored so far.
"""
import datetime as dt
import time
import warnings
from collections import defaultdict

from _cli import base_parser

from mtrl.common.config import load_config, save_resolved
from mtrl.common.env_setup import check_capabilities, gpu_mem_used_gb, setup_env

GATE_CHUNK = 1000   # rollouts per append for the (CPU, fast) gate stage


def main():
    ap = base_parser(__doc__)
    ap.add_argument("--metric", action="append", help="only this metric (repeatable); default: config")
    args = ap.parse_args()
    cfg = load_config(args.config, args.env)
    setup_env(cfg.env)
    caps = check_capabilities(cfg.env)

    from mtrl.scoring import metrics as M
    from mtrl.common.flops_accounting import scoring_cost
    from mtrl.scoring.rule_gate import gate, load_lid
    from mtrl.common.jsonl_io import append_jsonl, done_keys, read_jsonl, write_jsonl
    from mtrl.scoring.reward import reward
    from mtrl.common.records import KEY_FIELDS, Rollout, Score, Segment, direction_of
    from mtrl.data.segment_loader import segments_path

    e = cfg.exp
    run_dir = cfg.run_dir
    parts = run_dir / "score_parts"
    cp_path = run_dir / "compute.jsonl"
    save_resolved(cfg, run_dir)
    append_jsonl(cp_path, [{"type": "header", "stage": "score", "env": cfg.env.name,
                            "time": dt.datetime.now().isoformat(timespec="seconds"), **caps}])

    # ---- select rollouts
    rollouts = [Rollout.from_dict(d) for d in read_jsonl(run_dir / "rollouts.jsonl")]
    rollouts = [r for r in rollouts if (not args.model or r.model in args.model)
                and (args.thinking is None or r.thinking == args.thinking)]
    segs = {}
    for d in {direction_of(r.seg_id) for r in rollouts}:
        for s in read_jsonl(segments_path(cfg.env.path("data_dir"), d, e.split)):
            segs[s["seg_id"]] = Segment.from_dict(s)
    limit = args.limit if args.limit is not None else e.limit
    if limit:
        keep = set()
        for d in {direction_of(r.seg_id) for r in rollouts}:
            ids = sorted({r.seg_id for r in rollouts if direction_of(r.seg_id) == d})
            keep.update(ids[:limit])
        rollouts = [r for r in rollouts if r.seg_id in keep]
    print(f"[score] {len(rollouts)} rollouts selected")

    # ---- gate (CPU)
    gpath = parts / "gate.jsonl"
    gdone = done_keys(gpath, KEY_FIELDS)
    todo = [r for r in rollouts if r.key() not in gdone]
    if todo:
        lid = load_lid(cfg.env.path("fasttext_lid"))
        for c in range(0, len(todo), GATE_CHUNK):
            recs = []
            for r in todo[c:c + GATE_CHUNK]:
                ok, why = gate(segs[r.seg_id], r.translation, r.parse_ok, cfg.lang(direction_of(r.seg_id)),
                               lid_model=lid, copy_ratio_max=e.gate["copy_ratio_max"])
                recs.append({**dict(zip(KEY_FIELDS, r.key())), "gate_ok": ok, "gate_reason": why})
            append_jsonl(gpath, recs)
    print(f"[score] gate: {len(todo)} new")

    # ---- metrics (GPU, one model at a time)
    for metric in args.metric or e.metrics:
        fn = M.METRICS[metric]
        mpath = parts / f"{metric}.jsonl"
        mdone = done_keys(mpath, KEY_FIELDS)
        groups = defaultdict(list)
        for r in rollouts:
            seg = segs[r.seg_id]
            if r.key() in mdone or not r.parse_ok or not r.translation.strip():
                continue
            if metric in M.NEEDS_REF and not seg.ref:
                continue
            groups[(direction_of(r.seg_id), r.model, r.thinking)].append(r)
        print(f"[score] {metric}: {sum(map(len, groups.values()))} pending")
        try:
            for (d, model, thinking), rs in sorted(groups.items()):
                by_seg = defaultdict(list)
                for r in rs:
                    by_seg[r.seg_id].append(r)
                seg_ids = sorted(by_seg)
                for c in range(0, len(seg_ids), e.chunk_size):
                    chunk = [r for sid in seg_ids[c:c + e.chunk_size] for r in by_seg[sid]]
                    srcs = [segs[r.seg_id].src for r in chunk]
                    hyps = [r.translation for r in chunk]
                    refs = [segs[r.seg_id].ref for r in chunk] if metric in M.NEEDS_REF else None
                    t0 = time.time()
                    vals = fn(srcs, hyps, refs, batch_size=cfg.env.scoring["batch_size"], env_cfg=cfg.env)
                    wall = time.time() - t0
                    append_jsonl(mpath, [{**dict(zip(KEY_FIELDS, r.key())), "value": float(v)}
                                         for r, v in zip(chunk, vals)])
                    n_tok = M.count_scorer_tokens(metric, srcs, hyps, refs)
                    n_par = e.scorer_params.get(metric, 0.0)
                    append_jsonl(cp_path, [{
                        "type": "score", "metric": metric, "direction": d, "model": model,
                        "thinking": thinking, "n_inputs": len(chunk), "n_tokens": n_tok,
                        "flops": scoring_cost(len(chunk), n_tok / max(len(chunk), 1), n_par),
                        "wall_s": round(wall, 2), "gpu_mem_used_gb": gpu_mem_used_gb()}])
        except M.MetricUnavailable as ex:
            warnings.warn(f"skipping {metric}: {ex}")
        finally:
            M.release()

    # ---- assemble scores.jsonl from all parts
    gates = {tuple(g[k] for k in KEY_FIELDS): g for g in read_jsonl(gpath)}
    values = defaultdict(dict)
    for mpath in sorted(parts.glob("*.jsonl")):
        if mpath.stem == "gate":
            continue
        for rec in read_jsonl(mpath):
            values[tuple(rec[k] for k in KEY_FIELDS)][mpath.stem] = rec["value"]
    out = []
    for key, g in gates.items():
        mv = values.get(key, {})
        if not g["gate_ok"]:
            rw = 0.0
        elif "metricx24_qe" in mv:
            rw = reward(True, mv["metricx24_qe"])
        else:
            rw = None   # gate passed but QE not computed yet
        out.append(Score(seg_id=g["seg_id"], sample_idx=g["sample_idx"], model=g["model"],
                         thinking=g["thinking"], gate_ok=g["gate_ok"], gate_reason=g["gate_reason"],
                         metrics=mv, reward=rw).to_dict())
    write_jsonl(run_dir / "scores.jsonl", out)
    print(f"[score] wrote {len(out)} scores -> {run_dir / 'scores.jsonl'}")


if __name__ == "__main__":
    main()
