"""Stage 1: generate rollouts (greedy + G samples) with vLLM -> runs/{run}/rollouts.jsonl.

Resumable: (seg_id, sample_idx, model, thinking) already in rollouts.jsonl are skipped.
"""
import datetime as dt
import gc
import time

from _cli import base_parser

from mtrl.common.config import load_config, save_resolved
from mtrl.common.env_setup import check_capabilities, gpu_mem_used_gb, setup_env


def main():
    args = base_parser(__doc__).parse_args()
    cfg = load_config(args.config, args.env)
    setup_env(cfg.env)
    caps = check_capabilities(cfg.env)

    from mtrl.common.flops_accounting import rollout_cost
    from mtrl.data.segment_loader import load_segments
    from mtrl.generation.vllm_generate import generate, load_llm
    from mtrl.common.jsonl_io import append_jsonl, done_keys
    from mtrl.common.records import KEY_FIELDS

    e = cfg.exp
    run_dir = cfg.run_dir
    save_resolved(cfg, run_dir)
    ro_path, cp_path = run_dir / "rollouts.jsonl", run_dir / "compute.jsonl"
    append_jsonl(cp_path, [{"type": "header", "stage": "generate", "env": cfg.env.name,
                            "time": dt.datetime.now().isoformat(timespec="seconds"), **caps}])
    done = done_keys(ro_path, KEY_FIELDS)

    passes = []
    if e.greedy:
        passes.append(("greedy", dict(n=1, temperature=0.0, top_p=1.0), [-1]))
    G = e.sampling["n"]
    passes.append(("sample", dict(n=G, temperature=e.sampling["temperature"],
                                  top_p=e.sampling["top_p"]), list(range(G))))

    limit = args.limit if args.limit is not None else e.limit
    segs_by_dir = {}
    for d in e.directions:
        segs = load_segments(d, e.split, e.n_per_direction, e.seed, data_dir=cfg.env.path("data_dir"))
        segs_by_dir[d] = segs[:limit] if limit else segs

    for m in e.models:
        name = m["name"]
        if args.model and name not in args.model:
            continue
        llm = None
        for thinking in e.thinking:
            if args.thinking is not None and thinking != args.thinking:
                continue
            max_tokens = e.max_tokens["thinking_on" if thinking else "thinking_off"]
            for d, segs in segs_by_dir.items():
                lang = cfg.lang(d)
                for pass_name, sp, idxs in passes:
                    pending = [s for s in segs
                               if any((s.seg_id, i, name, thinking) not in done for i in idxs)]
                    print(f"[generate] {name} thinking={thinking} {d} {pass_name}: "
                          f"{len(pending)}/{len(segs)} segments pending", flush=True)
                    for c in range(0, len(pending), e.chunk_size):
                        chunk = pending[c:c + e.chunk_size]
                        if llm is None:
                            llm = load_llm(name, cfg.env, e.seed)
                        t0 = time.time()
                        rolls = generate(llm, name, chunk, lang_cfg=lang, template=e.prompt_template,
                                         thinking=thinking, max_tokens=max_tokens, seed=e.seed, **sp)
                        wall = time.time() - t0
                        rolls = [r for r in rolls if r.key() not in done]
                        append_jsonl(ro_path, [r.to_dict() for r in rolls])
                        done.update(r.key() for r in rolls)
                        append_jsonl(cp_path, [{
                            "type": "gen", "direction": d, "model": name, "thinking": thinking,
                            "pass": pass_name, "n_segments": len(chunk), "n_rollouts": len(rolls),
                            **rollout_cost(rolls, cfg.n_params(name)),
                            "wall_s": round(wall, 2), "gpu_mem_used_gb": gpu_mem_used_gb()}])
        if llm is not None:
            del llm
            gc.collect()
    print(f"[generate] done -> {ro_path}")


if __name__ == "__main__":  # guard needed: vLLM may spawn worker processes
    main()
