"""Save / restore data/processed to a cache directory (e.g. Google Drive on Colab):

    python scripts/data_cache.py restore /content/drive/MyDrive/mtrl/data_cache
    python scripts/data_cache.py save    /content/drive/MyDrive/mtrl/data_cache

Building the training data downloads and cleans corpora (minutes per direction); a
fresh Colab runtime would redo it every session. The archive name carries a hash of
everything that decides the processed data (configs/train_data.yaml,
configs/languages.yaml, src/mtrl/data/*.py, scripts/prepare_train_data.py), so a change to
any of them makes the cache miss and the data is rebuilt. `save` replaces the archive
atomically; `restore` never overwrites existing files.
"""
import argparse
import hashlib
import tarfile
from pathlib import Path

from mtrl.common.config import REPO_ROOT

KEY_FILES = ["configs/train_data.yaml", "configs/languages.yaml", "scripts/prepare_train_data.py"]
KEY_GLOBS = ["src/mtrl/data/*.py"]


def cache_key() -> str:
    h = hashlib.sha256()
    files = [REPO_ROOT / f for f in KEY_FILES] + sorted(p for g in KEY_GLOBS for p in REPO_ROOT.glob(g))
    for p in files:
        h.update(p.relative_to(REPO_ROOT).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:12]


def archive_path(cache_dir: Path) -> Path:
    return Path(cache_dir) / f"processed-{cache_key()}.tar"


def restore(cache_dir: Path, data_dir: Path) -> int:
    arc = archive_path(cache_dir)
    if not arc.exists():
        print(f"[cache] miss: {arc.name} not in {cache_dir}")
        return 0
    n = 0
    with tarfile.open(arc) as tar:
        for m in tar.getmembers():
            if m.isfile() and not (data_dir / m.name).exists():
                tar.extract(m, data_dir, filter="data")
                n += 1
    print(f"[cache] restored {n} files from {arc}")
    return n


def save(cache_dir: Path, data_dir: Path) -> Path:
    src = data_dir / "processed"
    if not src.exists():
        raise SystemExit(f"{src} does not exist; nothing to cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    arc = archive_path(cache_dir)
    tmp = arc.with_suffix(".tmp")
    with tarfile.open(tmp, "w") as tar:
        tar.add(src, arcname="processed")
    tmp.replace(arc)
    for old in cache_dir.glob("processed-*.tar"):      # older keys are stale by construction
        if old != arc:
            old.unlink()
    print(f"[cache] saved {src} -> {arc} ({arc.stat().st_size / 1e6:.1f} MB)")
    return arc


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["save", "restore"])
    ap.add_argument("cache_dir")
    ap.add_argument("--data-dir", default=str(REPO_ROOT / "data"))
    args = ap.parse_args()
    (save if args.action == "save" else restore)(Path(args.cache_dir), Path(args.data_dir))


if __name__ == "__main__":
    main()
