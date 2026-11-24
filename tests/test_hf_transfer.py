"""No-network contracts for pinned Hub downloads and original-config restoration."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import types
import pytest


def module():
    path = Path(__file__).resolve().parents[1] / "scripts/download_models.py"
    spec = importlib.util.spec_from_file_location("model_download_fixture", path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def setup(tmp_path, monkeypatch, corrupt=False):
    root = tmp_path / "relocated-repo"
    remote = tmp_path / "remote"
    remote.mkdir()
    weights = b"frozen-adapter-weights"
    original = b'{"base_model_name_or_path":"/historical/base"}'
    (remote / "adapter_model.safetensors").write_bytes(b"bad" if corrupt else weights)
    (remote / "original_adapter_config.json").write_bytes(original)
    (remote / "adapter_config.json").write_bytes(b'{"base_model_name_or_path":"portable/base"}')
    files = {name: dict(bytes=len(value), sha256=hashlib.sha256(value).hexdigest()) for name, value in
             [("adapter_model.safetensors", weights), ("adapter_config.json", original)]}
    entry = dict(id="fixture", base_revision="a" * 40, adapter_path="artifacts/fixture", files=files,
                 hub_repo_id="owner/fixture", hub_revision="b" * 40, uploaded=True,
                 hub_file_map={"adapter_model.safetensors":"adapter_model.safetensors", "adapter_config.json":"original_adapter_config.json"})
    (root / "models").mkdir(parents=True)
    (root / "models/registry.json").write_text(json.dumps(dict(schema_version=1, models=[entry])))
    calls = []
    def download(repo_id, filename, revision):
        assert repo_id == "owner/fixture" and revision == "b" * 40
        calls.append(filename)
        return str(remote / filename)
    monkeypatch.setitem(sys.modules, "huggingface_hub", types.SimpleNamespace(hf_hub_download=download))
    obj = module()
    monkeypatch.setattr(obj, "ROOT", root)
    return obj, root, original, calls


def test_pinned_download_restores_original_config_not_normalized_config(tmp_path, monkeypatch):
    obj, root, original, calls = setup(tmp_path, monkeypatch)
    assert obj.fetch("fixture")["verified"]
    assert (root / "artifacts/fixture/adapter_config.json").read_bytes() == original
    assert calls == ["adapter_model.safetensors", "original_adapter_config.json"]
    obj.fetch("fixture")
    assert len(calls) == 2  # Valid local artifacts do not trigger another network fetch.


def test_corrupt_remote_does_not_replace_local_artifact(tmp_path, monkeypatch):
    obj, root, _, _ = setup(tmp_path, monkeypatch, corrupt=True)
    with pytest.raises(ValueError, match="does not match"):
        obj.fetch("fixture")
    assert not (root / "artifacts/fixture/adapter_model.safetensors").exists()
