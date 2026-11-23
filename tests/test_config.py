import sys

import pytest

from mtrl.common.config import load_config, load_env


def test_env_config_name_checks():
    env = load_env("local_4070S_12G")
    assert env.name == "local_4070S_12G" and env.gpu["mem_gb"] == 12
    with pytest.raises(ValueError):
        load_env("bad-name")


def test_load_config_env_from_dotenv_var(monkeypatch):
    monkeypatch.setenv("MTRL_ENV", "local_4070S_12G")
    cfg = load_config("configs/quick.yaml")
    assert cfg.env.name == "local_4070S_12G"
    assert cfg.exp.limit == 5 and cfg.exp.split == "test"
    assert cfg.exp.models[0]["n_params"] == 0.8e9   # YAML string "0.8e9" converted to float


def test_python_for_uses_default_when_not_configured_and_checks_existence(tmp_path):
    env = load_env("local_4070S_12G")
    env.python = {}
    assert env.python_for("score", default=sys.executable) == sys.executable
    env.python = {"score": str(tmp_path / "missing" / "python")}
    with pytest.raises(FileNotFoundError):
        env.python_for("score", default=sys.executable)
    env.python = {"score": sys.executable}
    assert env.python_for("score", default="unused") == sys.executable


def test_all_env_configs_load_and_expand_vars(monkeypatch):
    from pathlib import Path

    monkeypatch.setenv("USER", "alice")
    for p in sorted(Path(__file__).resolve().parents[1].glob("configs/env/[!_]*.yaml")):
        env = load_env(p.stem)
        assert env.name == p.stem
    env = load_env("dinfk_1080Ti_11G")
    assert env.dtype == "fp16" and not env.use_vllm
    assert str(env.path("hf_home")) == "/scratch/users/alice/hf"


def test_env_base_inheritance_colab():
    l4, t4 = load_env("colab_L4_24G"), load_env("colab_T4_16G")
    assert (l4.dtype, t4.dtype) == ("bf16", "fp16")
    assert l4.paths == t4.paths and l4.python == t4.python          # shared from _colab.yaml
    assert l4.scoring["batch_size"] != t4.scoring["batch_size"]       # per-card override
    assert str(l4.path("runs_dir")) == "/content/drive/MyDrive/mtrl/runs"


@pytest.mark.parametrize("gpu,mem,expected", [
    ("Tesla T4", 15.8, "colab_T4_16G"),
    ("NVIDIA L4", 23.7, "colab_L4_24G"),
    ("NVIDIA A100-SXM4-40GB", 42.5, "colab_A100_40G"),
    ("NVIDIA A100-SXM4-80GB", 85.1, "colab_A100_80G"),
])
def test_pick_env_by_gpu(gpu, mem, expected):
    from mtrl.common.env_setup import pick_env

    assert pick_env("colab", gpu, mem) == expected


def test_pick_env_unknown_gpu_fails():
    from mtrl.common.env_setup import pick_env

    with pytest.raises(RuntimeError, match="0 colab env configs"):
        pick_env("colab", "NVIDIA RTX PRO 6000 Blackwell", 96.0)
