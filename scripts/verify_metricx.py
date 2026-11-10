"""Check that our MetricX-24 implementation matches the official one (GPU server).

    python scripts/verify_metricx.py configs/quick.yaml [--n 16] [--tol 0.05]

Ours (mtrl.scoring.metrics): HF MT5ForConditionalGeneration, one decoder step from
token 0, logit of token 250089, clamped to [0, 25]. Official: MT5ForRegression from
google-research/metricx (metricx24/models.py), cloned into data/external/metricx on
first use (data/ is git-ignored; the repo is never pip-installed).

Inputs: the first --n rollouts with a non-empty translation from runs/{run_name}/;
if there are none yet, processed segments with the reference used as hypothesis.
Both models see identical token ids (our metricx_tokenize). Exit 0 if the maximum
absolute score difference is within --tol, else exit 1.

Confirmed against the official sources (main branch, 2026-11-10):
  models.py:  class MT5ForRegression(MT5PreTrainedModel); forward(input_ids,
              attention_mask, ...) builds decoder_input_ids = [[0]] itself and returns
              MT5ForRegressionOutput(loss, predictions), where
              predictions = clamp(lm_logits[:, 0, 250089], 0, 25)
  predict.py: inputs "source: S candidate: H [reference: R]", truncated to
              max_input_length, trailing EOS dropped; model loaded with
              MT5ForRegression.from_pretrained(path, torch_dtype="auto")
"""
import argparse
import subprocess
import sys
import warnings
from pathlib import Path

from mtrl.common.config import load_config
from mtrl.common.env_setup import setup_env
from mtrl.common.jsonl_io import read_jsonl
from mtrl.data.segment_loader import segments_path

METRICX_GIT = "https://github.com/google-research/metricx"
# bf16 has an 8-bit mantissa: between 16 and 32 adjacent values are 0.125 apart, so
# batched (padded) vs single-example runs can differ by one bf16 step. Allow two steps.
DEFAULT_TOL = {"bf16": 0.25, "fp16": 0.05, "fp32": 1e-3}


def collect_inputs(cfg, n: int):
    """Return (srcs, hyps, refs_or_None_per_item) for up to n items."""
    data_dir, split = cfg.env.path("data_dir"), cfg.exp.split
    segs = {}
    for d in cfg.exp.directions:
        for s in read_jsonl(segments_path(data_dir, d, split)):
            segs[s["seg_id"]] = s
    items = []
    for r in read_jsonl(cfg.run_dir / "rollouts.jsonl"):
        if r["translation"].strip() and r["seg_id"] in segs:
            seg = segs[r["seg_id"]]
            items.append((seg["src"], r["translation"], seg["ref"]))
        if len(items) >= n:
            break
    if not items:
        print("[verify] no rollouts yet; using references as hypotheses")
        items = [(s["src"], s["ref"], s["ref"]) for s in segs.values() if s["ref"]][:n]
    if not items:
        raise SystemExit("no inputs: run generate first, or include a direction with references")
    return [i[0] for i in items], [i[1] for i in items], [i[2] for i in items]


def official_class(cfg, repo_path):
    path = repo_path or cfg.env.path("data_dir") / "external" / "metricx"
    if not (path / "metricx24" / "models.py").exists():
        print(f"[verify] cloning {METRICX_GIT} -> {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", METRICX_GIT, str(path)], check=True)
    sys.path.insert(0, str(path))
    try:
        from metricx24.models import MT5ForRegression
    except Exception as e:  # the official code reaches into transformers internals
        raise SystemExit(f"cannot import the official MT5ForRegression with this transformers "
                         f"version ({type(e).__name__}: {e})") from e
    return MT5ForRegression


def load_official(cls, cfg):
    """Same checkpoint, fallback rule and dtype as mtrl.scoring.metrics."""
    from mtrl.scoring import metrics as M

    dtype = M._torch_dtype(cfg.env)
    repo = M.METRICX_MODEL["bf16"] if cfg.env.dtype == "bf16" else M.METRICX_MODEL["default"]
    try:
        model = cls.from_pretrained(repo, torch_dtype=dtype)
    except OSError:
        warnings.warn(f"{repo} not available, falling back to {M.METRICX_MODEL['default']}")
        model = cls.from_pretrained(M.METRICX_MODEL["default"], torch_dtype=dtype)
    return model.to("cuda").eval()


def official_scores(model, srcs, hyps, refs):
    """Run the official model one example at a time (no padding effects)."""
    import torch

    from mtrl.scoring import metrics as M

    out = []
    with torch.inference_mode():
        for ids in M.metricx_tokenize(M.metricx_inputs(srcs, hyps, refs)):
            inp = torch.tensor([ids], device="cuda")
            # use_cache=False: with the cache on, the official forward fails under
            # transformers 4.57 (off-by-one size mismatch in decoder cross-attention).
            pred = model(input_ids=inp, attention_mask=torch.ones_like(inp), use_cache=False).predictions
            out.append(float(pred.float()[0]))
    return out


def report(mode, ours, theirs, tol) -> bool:
    diffs = [abs(a - b) for a, b in zip(ours, theirs)]
    print(f"\n[{mode}]  ours  official  |diff|")
    for a, b, d in zip(ours, theirs, diffs):
        print(f"  {a:8.4f}  {b:8.4f}  {d:.5f}")
    ok = max(diffs) <= tol
    print(f"[{mode}] n={len(diffs)} max|diff|={max(diffs):.5f} mean|diff|={sum(diffs) / len(diffs):.5f} "
          f"tol={tol} -> {'OK' if ok else 'MISMATCH'}")
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", help="experiment YAML, e.g. configs/quick.yaml")
    ap.add_argument("--env", help="env name (default: MTRL_ENV from .env)")
    ap.add_argument("--n", type=int, default=16, help="number of examples (default 16)")
    ap.add_argument("--metricx-repo", type=Path,
                    help="existing checkout of google-research/metricx (default: clone into data/external/)")
    ap.add_argument("--tol", type=float, help="max allowed |diff| (default 0.25 bf16, 0.05 fp16, 1e-3 fp32)")
    args = ap.parse_args()
    cfg = load_config(args.config, args.env)
    setup_env(cfg.env)
    tol = args.tol if args.tol is not None else DEFAULT_TOL[cfg.env.dtype]

    from mtrl.scoring import metrics as M

    srcs, hyps, refs = collect_inputs(cfg, args.n)
    has_ref = all(refs)
    bs = cfg.env.scoring["batch_size"]
    ours = {"qe": M.metricx24_qe(srcs, hyps, None, batch_size=bs, env_cfg=cfg.env)}
    if has_ref:
        ours["ref"] = M.metricx24_ref(srcs, hyps, refs, batch_size=bs, env_cfg=cfg.env)
    M.release()

    model = load_official(official_class(cfg, args.metricx_repo), cfg)
    ok = True
    for mode, r in [("qe", None), ("ref", refs)]:
        if mode in ours:
            ok &= report(mode, ours[mode], official_scores(model, srcs, hyps, r), tol)
    if not has_ref:
        print("[verify] reference mode skipped: not every example has a reference")
    if not ok:
        raise SystemExit("MetricX mismatch: do not trust rewards until mtrl.scoring.metrics is fixed")
    print("\n[verify] our MetricX matches the official implementation")


if __name__ == "__main__":
    main()
