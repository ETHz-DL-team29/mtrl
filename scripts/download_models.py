"""Explicitly fetch registered hosted adapters. Never downloads a full base model."""
from pathlib import Path
import argparse
import os
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mtrl.checkpoints import registry, model_entry, verify_model, sha256, inside


def fetch(model_id):
    entry = model_entry(model_id, ROOT)
    if not entry.get("hub_repo_id") or not entry.get("hub_revision"):
        raise ValueError(f"{model_id} is local-bundle-only; no published Hub revision is registered")
    from huggingface_hub import hf_hub_download
    folder = inside(ROOT, entry["adapter_path"])
    folder.mkdir(parents=True, exist_ok=True)
    for local_name, remote_name in entry["hub_file_map"].items():
        expected = entry["files"][local_name]
        destination = inside(folder, local_name)
        if destination.exists() and sha256(destination) == expected["sha256"]:
            continue
        cached = Path(hf_hub_download(entry["hub_repo_id"], remote_name, revision=entry["hub_revision"]))
        if cached.stat().st_size != expected["bytes"] or sha256(cached) != expected["sha256"]:
            raise ValueError(f"Hub file does not match the frozen local artifact:{model_id}/{remote_name}")
        temporary = destination.with_suffix(destination.suffix + ".download.tmp")
        shutil.copyfile(cached, temporary)
        temporary.replace(destination)
    return verify_model(model_id, ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Registry ID, or all-hosted")
    args = parser.parse_args()
    ids = [m["id"] for m in registry(ROOT)["models"] if m.get("uploaded")] if args.model == "all-hosted" else [args.model]
    if not ids:
        raise ValueError("No hosted models registered")
    import json
    for model_id in ids:
        print(json.dumps(fetch(model_id)))


if __name__ == "__main__":
    main()
