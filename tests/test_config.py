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
