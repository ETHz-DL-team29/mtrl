"""Training config: configs/train/*.yaml + configs/env/{env}.yaml.

A training YAML may name a parent with `base: <file>` (resolved relative to its own
directory); dicts are merged recursively, the child wins. The env config is the same
one the zero-shot stages use; the two must not share top-level keys.

`method` selects the trainer: "rl" (group policy gradient, mtrl.train.rl) or "sft"
(mtrl.train.sft). Method-specific sections are validated here so a typo fails before
any model is loaded.
"""
from __future__ import annotations

import copy
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

from mtrl.common.config import REPO_ROOT, EnvConfig, _git_commit, load_env, resolve_env_name

METHODS = ("rl", "sft")
ADAPTER_TARGETS = ("all", "attn", "mlp")
REWARD_MODES = ("qe", "ref")
GATE_MODES = ("main", "ym_compat")
INIT_BASE = "base"

# Sections each method needs (beyond the common ones), with their required keys.
REQUIRED = {
    "rl": {"algorithm": ["group", "prompts_per_step", "ppo_epochs", "clip_low", "clip_high",
                         "zero_var_retries", "ent_coef"],
           "rollout": ["temperature", "top_p", "rep_penalty", "max_new_tokens"],
           "reward": ["mode", "gate", "copy_ratio_max"],
           "mask": ["name"]},
    "sft": {"sft": ["batch_size", "grad_accum", "max_len"]},
}


@dataclass
class TrainConfig:
    run_name: str
    method: str                 # rl | sft
    seed: int
    model: dict                 # {name, n_params}
    data: dict                  # {directions, train_split, val_split, train_limit, val_limit}
    thinking: bool
    prompt_template: str
    init: dict                  # {from: base | <run_name> | <adapter dir>}
    adapter: dict               # {r, alpha, dropout, targets: all|attn|mlp, layers: "0-23" | [0, 4]}
    optim: dict                 # {lr, betas, weight_decay, grad_clip}
    schedule: dict              # {steps, max_hours, ckpt_every, keep_ckpts, val_every, log_every}
    eval: dict                  # {split, limit, max_new_tokens, batch_size}
    algorithm: dict = field(default_factory=dict)   # rl
    rollout: dict = field(default_factory=dict)     # rl
    reward: dict = field(default_factory=dict)      # rl
    mask: dict = field(default_factory=dict)        # rl
    sft: dict = field(default_factory=dict)         # sft
    notes: str = ""


@dataclass
class TrainRunConfig:
    train: TrainConfig
    env: EnvConfig
    languages: dict
    source: str = ""            # path of the training YAML

    @property
    def run_dir(self) -> Path:
        return self.env.path("runs_dir") / self.train.run_name

    @property
    def ckpt_dir(self) -> Path:
        """env paths.ckpt_dir/{run_name} if set (e.g. scratch or Google Drive), else run_dir/ckpt."""
        if "ckpt_dir" in self.env.paths:
            return self.env.path("ckpt_dir") / self.train.run_name
        return self.run_dir / "ckpt"

    def lang(self, direction: str) -> dict:
        tgt = direction.split("-", 1)[1]
        if tgt not in self.languages:
            raise KeyError(f"target language {tgt!r} missing from configs/languages.yaml")
        return {"code": tgt, **self.languages[tgt]}


def deep_merge(base: dict, child: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in child.items():
        out[k] = deep_merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def read_train_yaml(path, _seen=()) -> dict:
    path = Path(path).resolve()
    if path in _seen:
        raise ValueError(f"cyclic `base:` chain at {path}")
    with open(path, encoding="utf-8") as f:
        d = yaml.safe_load(f) or {}
    parent = d.pop("base", None)
    if parent:
        d = deep_merge(read_train_yaml(path.parent / parent, _seen + (path,)), d)
    return d


def validate(cfg: TrainConfig) -> None:
    if cfg.method not in METHODS:
        raise ValueError(f"method must be one of {METHODS}, got {cfg.method!r}")
    if cfg.adapter.get("targets") not in ADAPTER_TARGETS:
        raise ValueError(f"adapter.targets must be one of {ADAPTER_TARGETS}")
    for section, keys in REQUIRED[cfg.method].items():
        missing = [k for k in keys if k not in getattr(cfg, section)]
        if missing:
            raise ValueError(f"{cfg.method}: {section} is missing {missing}")
    if cfg.method == "rl":
        if cfg.reward["mode"] not in REWARD_MODES:
            raise ValueError(f"reward.mode must be one of {REWARD_MODES}")
        if cfg.reward["gate"] not in GATE_MODES:
            raise ValueError(f"reward.gate must be one of {GATE_MODES}")
        if cfg.algorithm["group"] < 2:
            raise ValueError("algorithm.group must be >= 2 (advantages are relative within a group)")
        if cfg.algorithm["ppo_epochs"] < 1:
            raise ValueError("algorithm.ppo_epochs must be >= 1")
    if not cfg.data.get("directions"):
        raise ValueError("data.directions is empty")


def _numeric(d: dict, keys) -> None:
    for k in keys:   # YAML reads 2e-5 as a string
        if k in d and isinstance(d[k], str):
            d[k] = float(d[k])


def load_train_config(path, env_name: str | None = None) -> TrainRunConfig:
    env_name = resolve_env_name(env_name)
    d = read_train_yaml(path)
    env = load_env(env_name)
    clash = set(d) & set(asdict(env))
    if clash:
        raise ValueError(f"keys defined in both training and env config: {sorted(clash)}")
    d["model"]["n_params"] = float(d["model"]["n_params"])
    _numeric(d.get("optim", {}), ["lr", "weight_decay", "grad_clip"])
    cfg = TrainConfig(**d)
    validate(cfg)
    with open(REPO_ROOT / "configs" / "languages.yaml", encoding="utf-8") as f:
        languages = yaml.safe_load(f)
    run = TrainRunConfig(train=cfg, env=env, languages=languages, source=str(path))
    for direction in cfg.data["directions"]:
        run.lang(direction)   # fail early on unknown languages
    return run


def save_resolved(run: TrainRunConfig) -> Path:
    import datetime as dt

    run.run_dir.mkdir(parents=True, exist_ok=True)
    out = {"train": asdict(run.train), "env": asdict(run.env), "source": run.source,
           "git_commit": _git_commit(), "time": dt.datetime.now().isoformat(timespec="seconds")}
    path = run.run_dir / "config.resolved.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)
    return path
