"""Load experiment YAML + configs/env/{env}.yaml into dataclasses.

Experiment config: what to run (no paths, no memory knobs).
Env config: hardware / paths. The two must not share top-level keys.
The env name defaults to MTRL_ENV (set once per machine in the git-ignored .env).
"""
from __future__ import annotations

import datetime as _dt
import os
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml


def _find_repo_root() -> Path:
    """First directory above this file that contains pyproject.toml."""
    for d in Path(__file__).resolve().parents:
        if (d / "pyproject.toml").exists():
            return d
    raise RuntimeError(f"no pyproject.toml found above {__file__}; run mtrl from a repository checkout")


REPO_ROOT = _find_repo_root()
ENV_NAME_RE = re.compile(r"^(?P<provider>[a-z]+)_(?P<gpu>[A-Za-z0-9]+)_(?P<gdram>\d+)G$")


@dataclass
class EnvConfig:
    name: str
    n_gpus: int
    gpu: dict              # {match: str, mem_gb: int}
    paths: dict            # hf_home, data_dir, runs_dir, fasttext_lid (+ optional torch_home, pip_cache)
    dtype: str             # bf16 / fp16 / fp32
    attn_impl: str
    use_vllm: bool
    vllm: dict
    scoring: dict
    python: dict = field(default_factory=dict)   # {generate, score}: interpreter per env; empty = one env

    def path(self, key: str) -> Path:
        p = Path(self.paths[key]).expanduser()
        return p if p.is_absolute() else (REPO_ROOT / p).resolve()

    def python_for(self, group: str, default: str) -> str:
        """Interpreter for a stage group ("generate" or "score"); `default` if not configured."""
        if group not in self.python:
            return default
        exe = Path(self.python[group]).expanduser()
        if not exe.exists():
            raise FileNotFoundError(f"env {self.name}: python.{group} = {exe} does not exist "
                                    f"(create the env with the setup/ install script)")
        return str(exe)


@dataclass
class ExpConfig:
    run_name: str
    seed: int
    directions: list
    split: str
    n_per_direction: int | None
    limit: int | None      # keep only the first N segments per direction (quick runs); null = all
    models: list           # [{name, n_params}]
    thinking: list
    greedy: bool
    sampling: dict         # {n, temperature, top_p}
    max_tokens: dict       # {thinking_off, thinking_on}
    chunk_size: int
    prompt_template: str
    metrics: list
    scorer_params: dict
    gate: dict
    analysis: dict


@dataclass
class Config:
    exp: ExpConfig
    env: EnvConfig
    languages: dict = field(default_factory=dict)

    @property
    def run_dir(self) -> Path:
        return self.env.path("runs_dir") / self.exp.run_name

    def lang(self, direction: str) -> dict:
        tgt = direction.split("-", 1)[1]
        if tgt not in self.languages:
            raise KeyError(f"target language {tgt!r} missing from configs/languages.yaml")
        return {"code": tgt, **self.languages[tgt]}

    def n_params(self, model_name: str) -> float:
        for m in self.exp.models:
            if m["name"] == model_name:
                return float(m["n_params"])
        raise KeyError(model_name)


def _read_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_env(env_name: str) -> EnvConfig:
    path = REPO_ROOT / "configs" / "env" / f"{env_name}.yaml"
    m = ENV_NAME_RE.match(env_name)
    if not m:
        raise ValueError(f"env name {env_name!r} does not follow [provider]_[gpu]_[gdram]G")
    d = _read_yaml(path)
    if d.get("name") != env_name:
        raise ValueError(f"{path.name}: name field {d.get('name')!r} != file name {env_name!r}")
    env = EnvConfig(**d)
    if int(env.gpu["mem_gb"]) != int(m["gdram"]):
        raise ValueError(f"{env_name}: gpu.mem_gb={env.gpu['mem_gb']} disagrees with name")
    return env


def load_dotenv() -> None:
    """Read REPO_ROOT/.env into os.environ (existing variables win)."""
    path = REPO_ROOT / ".env"
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def resolve_env_name(env_name: str | None) -> str:
    """Explicit --env wins; otherwise MTRL_ENV from the shell or .env."""
    if env_name:
        return env_name
    load_dotenv()
    if os.environ.get("MTRL_ENV"):
        return os.environ["MTRL_ENV"]
    raise SystemExit("no env given: pass --env or set MTRL_ENV in .env (e.g. MTRL_ENV=local_4070S_12G)")


def load_config(exp_path: str, env_name: str | None = None) -> Config:
    env_name = resolve_env_name(env_name)
    exp_d = _read_yaml(Path(exp_path))
    env_d = _read_yaml(REPO_ROOT / "configs" / "env" / f"{env_name}.yaml")
    clash = set(exp_d) & set(env_d)
    if clash:
        raise ValueError(f"keys defined in both experiment and env config: {sorted(clash)}")
    for m in exp_d.get("models", []):
        m["n_params"] = float(m["n_params"])  # YAML reads 0.8e9 as a string
    exp_d["scorer_params"] = {k: float(v) for k, v in exp_d.get("scorer_params", {}).items()}
    languages = _read_yaml(REPO_ROOT / "configs" / "languages.yaml")
    return Config(exp=ExpConfig(**exp_d), env=load_env(env_name), languages=languages)


def _git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def save_resolved(config: Config, run_dir: Path) -> Path:
    run_dir.mkdir(parents=True, exist_ok=True)
    out = {
        "exp": asdict(config.exp),
        "env": asdict(config.env),
        "languages": config.languages,
        "git_commit": _git_commit(),
        "time": _dt.datetime.now().isoformat(timespec="seconds"),
    }
    path = run_dir / "config.resolved.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(out, f, sort_keys=False, allow_unicode=True)
    return path
