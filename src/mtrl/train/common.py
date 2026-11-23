"""Setup shared by the RL and SFT trainers: environment, data, model + adapter,
optimizer, resume, scorer, logging and the wall-time budget."""
from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass, field
from pathlib import Path

from mtrl.common.jsonl_io import append_jsonl
from mtrl.common.train_config import INIT_BASE, TrainRunConfig, save_resolved


@dataclass
class Session:
    run: TrainRunConfig
    tok: object
    model: object
    optimizer: object
    params: list
    start_step: int
    train_segs: list
    val_segs: list
    extra: dict = field(default_factory=dict)       # counters persisted in checkpoints
    scorer: object = None
    scorer_proc: object = None
    lid: object = None
    t0: float = field(default_factory=time.time)

    @property
    def cfg(self):
        return self.run.train

    def lang_of(self, seg):
        return self.run.lang(seg.direction)

    def log(self, name: str, rec: dict) -> None:
        append_jsonl(self.run.run_dir / name, [rec])

    def out_of_time(self) -> bool:
        h = self.cfg.schedule.get("max_hours")
        return bool(h) and (time.time() - self.t0) / 3600 >= float(h)

    def close(self):
        if self.scorer_proc is not None:
            self.scorer_proc.terminate()


def load_split(run: TrainRunConfig, split: str, limit) -> list:
    from mtrl.data.segment_loader import load_segments

    segs = []
    for d in run.train.data["directions"]:
        s = load_segments(d, split, None, run.train.seed, data_dir=run.env.path("data_dir"))
        segs += s[:limit] if limit else s
    return segs


def resolve_init_adapter(run: TrainRunConfig, init: str) -> Path:
    """`init.from`: a run name (its latest checkpoint) or a path to an adapter directory."""
    from mtrl.train.checkpoint import latest_adapter

    p = Path(init)
    if (p / "adapter_config.json").exists():
        return p
    for ckpt_dir in [run.env.path("runs_dir") / init / "ckpt",
                     run.env.path("ckpt_dir") / init if "ckpt_dir" in run.env.paths else None]:
        if ckpt_dir is not None and latest_adapter(ckpt_dir):
            return latest_adapter(ckpt_dir)
    raise FileNotFoundError(f"init.from={init!r}: neither an adapter directory nor a run with checkpoints")


def start(run: TrainRunConfig, *, need_scorer: bool) -> Session:
    from mtrl.common.env_setup import check_capabilities, setup_env

    setup_env(run.env)
    caps = check_capabilities(run.env)   # wrong card / bf16 on a pre-Ampere GPU fails here, not mid-run
    print(f"[train] env {run.env.name}: {caps['gpu_name']} ({caps['gpu_mem_gb']} GB, cc {caps['compute_capability']}), "
          f"dtype {run.env.dtype}", flush=True)
    import numpy as np
    import torch

    from mtrl.train import checkpoint as C
    from mtrl.train.policy import attach_lora, load_adapter, load_base

    t = run.train
    random.seed(t.seed)
    np.random.seed(t.seed)
    torch.manual_seed(t.seed)
    run.run_dir.mkdir(parents=True, exist_ok=True)
    save_resolved(run)

    train_segs = load_split(run, t.data["train_split"], t.data.get("train_limit"))
    val_segs = load_split(run, t.data["val_split"], t.data.get("val_limit"))
    print(f"[train] {t.run_name}: {len(train_segs)} train / {len(val_segs)} val segments "
          f"({', '.join(t.data['directions'])})", flush=True)

    tok, model = load_base(t.model["name"], run.env.dtype, run.env.attn_impl)
    gc = run.env.train.get("grad_checkpointing", True)
    if t.init["from"] == INIT_BASE:
        model = attach_lora(model, t.adapter, grad_checkpointing=gc)
    else:
        path = resolve_init_adapter(run, t.init["from"])
        print(f"[train] init adapter {path} (config `adapter` section ignored)", flush=True)
        if gc:
            model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
            model.enable_input_require_grads()
        model = load_adapter(model, path, trainable=True)
    model.train()
    params = [p for p in model.parameters() if p.requires_grad]
    o = t.optim
    optimizer = torch.optim.AdamW(params, lr=o["lr"], betas=tuple(o["betas"]), weight_decay=o["weight_decay"])

    start_step, extra = 0, {}
    last = C.latest_dir(run.ckpt_dir)
    if last is not None:
        state = C.load_into(last, model, optimizer)
        start_step, extra = state["step"] + 1, state.get("extra", {})
        print(f"[train] resumed from {last} -> step {start_step}", flush=True)

    s = Session(run=run, tok=tok, model=model, optimizer=optimizer, params=params, start_step=start_step,
                train_segs=train_segs, val_segs=val_segs, extra=extra)
    if need_scorer or t.schedule.get("val_every"):
        from mtrl.scoring.client import ensure_server
        from mtrl.scoring.rule_gate import load_lid

        s.scorer, s.scorer_proc = ensure_server(run.env, log_path=run.run_dir / "scorer.log")
        s.lid = load_lid(run.env.path("fasttext_lid"))
    return s


def checkpoint(s: Session, step: int) -> None:
    from mtrl.train import checkpoint as C

    d = C.save(s.run.ckpt_dir, step, s.model, s.optimizer, extra=s.extra, keep=s.cfg.schedule.get("keep_ckpts", 3))
    print(f"[train] checkpoint {d}", flush=True)


def release_cuda_cache() -> None:
    """Hand cached-but-free memory back to the driver so the MetricX service can use it."""
    import torch

    torch.cuda.empty_cache()


def validate(s: Session, step: int) -> dict | None:
    """In-training validation; a failure is logged and training continues."""
    try:
        return _validate(s, step)
    except Exception as e:   # noqa: BLE001 - never lose a training run to a validation error
        msg = f"{type(e).__name__}: {e}"
        s.log("val_log.jsonl", {"step": step, "error": msg[:1000]})
        print(f"[val] step {step} FAILED, continuing: {msg[:300]}", flush=True)
        release_cuda_cache()
        return None


def _validate(s: Session, step: int) -> dict:
    from mtrl.train.evaluate import evaluate

    t = s.cfg
    release_cuda_cache()
    t0 = time.time()
    _, summary = evaluate(s.model, s.tok, s.val_segs, [s.lang_of(x) for x in s.val_segs],
                          template=t.prompt_template, thinking=t.thinking,
                          max_new_tokens=t.eval["max_new_tokens"], batch_size=t.eval["batch_size"],
                          model_name=t.model["name"], scorer=s.scorer, lid_model=s.lid,
                          copy_ratio_max=t.reward.get("copy_ratio_max", 0.8))
    rec = {"step": step, "sec": round(time.time() - t0, 1), **{f"val_{k}": v for k, v in summary["all"].items()},
           "by_direction": {d: v for d, v in summary.items() if d != "all"}}
    s.log("val_log.jsonl", rec)
    print("[val]", json.dumps({k: v for k, v in rec.items() if k != "by_direction"}), flush=True)
    return rec
