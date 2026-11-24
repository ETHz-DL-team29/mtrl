"""CPU-only portability/integrity contracts; no model imports or downloads."""
import hashlib
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mtrl.checkpoints import registry, verify_model, inside


def fixture_registry(tmp_path):
    folder = tmp_path / "artifacts/test"
    folder.mkdir(parents=True)
    data = b"portable-weight-fixture"
    (folder / "adapter_model.safetensors").write_bytes(data)
    models = tmp_path / "models"
    models.mkdir()
    entry = dict(id="fixture", base_revision="a" * 40, adapter_path="artifacts/test",
                 files={"adapter_model.safetensors": dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())})
    (models / "registry.json").write_text(json.dumps(dict(schema_version=1, models=[entry])))
    return entry


def test_registry_survives_relocation_and_detects_tampering(tmp_path):
    fixture_registry(tmp_path)
    assert verify_model("fixture", tmp_path)["verified"]
    (tmp_path / "artifacts/test/adapter_model.safetensors").write_bytes(b"corrupted")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_model("fixture", tmp_path)


def test_escaped_and_absolute_artifact_paths_are_rejected(tmp_path):
    for relative in ["../outside", "D:/external", "/external"]:
        with pytest.raises(ValueError):
            inside(tmp_path, relative)


def test_duplicate_model_ids_and_missing_artifacts_are_clear(tmp_path):
    entry = fixture_registry(tmp_path)
    (tmp_path / "artifacts/test/adapter_model.safetensors").unlink()
    with pytest.raises(FileNotFoundError, match="git clone alone"):
        verify_model("fixture", tmp_path)
    (tmp_path / "models/registry.json").write_text(json.dumps(dict(schema_version=1, models=[entry, entry])))
    with pytest.raises(ValueError, match="Duplicate"):
        registry(tmp_path)
