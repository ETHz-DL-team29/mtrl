"""Make a local, relocatable repository+adapter ZIP. Never uploads or commits."""
from pathlib import Path
import argparse
import ctypes
import hashlib
import json
import os
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mtrl.checkpoints import registry, verify_model, inside


def digest_file(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(4 * 1024**2), b""):
        h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "deliveries/mtrl-models-2026-11-24.zip")
    args = parser.parse_args()
    if os.name == "nt":
        k = ctypes.windll.kernel32
        k.GetCurrentProcess.restype = ctypes.c_void_p
        k.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        k.SetPriorityClass(k.GetCurrentProcess(), 0x4000)
    entries = registry(ROOT)["models"]
    for entry in entries:
        verify_model(entry["id"], ROOT)
    if args.output.exists():
        raise FileExistsError("Preserve the previous delivery: choose a new --output")
    if (ROOT / ".git").is_dir():
        names = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"], check=True, capture_output=True).stdout.decode().split("\0")
        files = {ROOT / name for name in names if name and (ROOT / name).is_file()}
    else:
        files = {p for p in ROOT.rglob("*") if p.is_file() and p.relative_to(ROOT).parts[0] not in {"artifacts", "deliveries", "data", "runs"}}
    for entry in entries:
        files.update(p for p in inside(ROOT, entry["adapter_path"]).rglob("*") if p.is_file())
    safe = []
    for p in sorted(files):
        rel = p.relative_to(ROOT)
        if p.name == ".env" or any(x in rel.parts for x in [".git", ".venv", "__pycache__", ".pytest_cache", "colab_cli_private"]):
            continue
        if rel.parts[0] == "deliveries":
            continue
        if not p.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f"Refusing an external symlink: {rel}")
        safe.append(p)
    manifest = dict(schema_version=1, model_count=len(entries), base_weights_bundled=False,
                    uploads_performed_by_packaging=False, hosted_models_registered=[e["id"] for e in entries if e.get("uploaded")], files={})
    for p in safe:
        with p.open("rb") as stream:
            manifest["files"][p.relative_to(ROOT).as_posix()] = dict(bytes=p.stat().st_size, sha256=digest_file(stream))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(".zip.partial")
    with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=1, allowZip64=True) as archive:
        for p in safe:
            archive.write(p, "mtrl/" + p.relative_to(ROOT).as_posix())
        archive.writestr("mtrl/SHARE_MANIFEST.json", json.dumps(manifest, indent=2))
    with zipfile.ZipFile(temporary) as archive:
        for name, expected in manifest["files"].items():
            with archive.open("mtrl/" + name) as stream:
                if digest_file(stream) != expected["sha256"]:
                    raise ValueError(f"Packed artifact mismatch: {name}")
    temporary.replace(args.output)
    with args.output.open("rb") as stream:
        checksum = digest_file(stream)
    record = dict(path=str(args.output), bytes=args.output.stat().st_size, sha256=checksum,
                  model_count=len(entries), every_member_SHA256_verified=True, base_weights_bundled=False,
                  uploaded_by_packaging=False, git_commit_created=False, github_pushed=False)
    args.output.with_suffix(".verified.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps(record))


if __name__ == "__main__":
    main()
