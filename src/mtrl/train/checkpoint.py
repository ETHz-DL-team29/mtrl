"""Checkpoints: {ckpt_dir}/step_{N:06d}/ with
    adapter/            PEFT adapter (save_pretrained: adapter_config.json + safetensors),
                        loadable by PeftModel.from_pretrained and by scripts/eval_adapter.py
    trainer_state.pt    optimizer state, step, RNG states, extra counters
and a text file {ckpt_dir}/latest naming the newest complete step directory.

A step directory is written under a temporary name and renamed when complete, and
`latest` is replaced atomically, so a run killed mid-save (cluster time limit, Colab
disconnect) resumes from the previous checkpoint. Only the newest `keep` are kept.
"""
from __future__ import annotations

import os
import random
import shutil
from pathlib import Path

LATEST = "latest"


def step_dir(ckpt_dir: Path, step: int) -> Path:
    return Path(ckpt_dir) / f"step_{step:06d}"


def latest_dir(ckpt_dir) -> Path | None:
    p = Path(ckpt_dir) / LATEST
    if not p.exists():
        return None
    d = Path(ckpt_dir) / p.read_text().strip()
    return d if (d / "trainer_state.pt").exists() else None


def latest_adapter(ckpt_dir) -> Path | None:
    d = latest_dir(ckpt_dir)
    return d / "adapter" if d else None


def save(ckpt_dir, step: int, model, optimizer, extra: dict | None = None, keep: int = 3) -> Path:
    import numpy as np
    import torch

    ckpt_dir = Path(ckpt_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    final = step_dir(ckpt_dir, step)
    tmp = final.with_name(final.name + ".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    model.save_pretrained(tmp / "adapter")
    state = {"step": step, "optimizer": optimizer.state_dict(), "extra": extra or {},
             "rng": {"python": random.getstate(), "numpy": np.random.get_state(),
                     "torch": torch.get_rng_state(),
                     "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None}}
    torch.save(state, tmp / "trainer_state.pt")
    shutil.rmtree(final, ignore_errors=True)
    os.replace(tmp, final)
    pointer = ckpt_dir / (LATEST + ".tmp")
    pointer.write_text(final.name)
    os.replace(pointer, ckpt_dir / LATEST)
    steps = sorted(p for p in ckpt_dir.glob("step_*") if p.is_dir() and not p.name.endswith(".tmp"))
    for old in steps[:-keep] if keep > 0 else []:
        shutil.rmtree(old, ignore_errors=True)
    return final


def load_into(ckpt: Path, model, optimizer) -> dict:
    """Load adapter weights + optimizer + RNG from a step directory; returns the state dict."""
    import numpy as np
    import torch
    from peft import set_peft_model_state_dict
    from safetensors.torch import load_file

    ckpt = Path(ckpt)
    set_peft_model_state_dict(model, load_file(str(ckpt / "adapter" / "adapter_model.safetensors")))
    state = torch.load(ckpt / "trainer_state.pt", map_location="cpu", weights_only=False)
    optimizer.load_state_dict(state["optimizer"])
    rng = state["rng"]
    random.setstate(rng["python"])
    np.random.set_state(rng["numpy"])
    torch.set_rng_state(rng["torch"])
    if rng.get("cuda") is not None and torch.cuda.is_available():
        torch.cuda.set_rng_state_all(rng["cuda"])
    return state
