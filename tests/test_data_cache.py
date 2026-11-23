"""scripts/data_cache.py: save / restore round trip, no overwrite, stale archives removed."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("data_cache", ROOT / "scripts" / "data_cache.py")
data_cache = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_cache)


def test_round_trip_and_no_overwrite(tmp_path):
    src, cache, dst = tmp_path / "data", tmp_path / "cache", tmp_path / "restored"
    (src / "processed" / "en-is").mkdir(parents=True)
    (src / "processed" / "en-is" / "wmt_train.jsonl").write_text("a\n")
    (cache).mkdir()
    (cache / "processed-oldkey000000.tar").write_text("stale")
    arc = data_cache.save(cache, src)
    assert arc.name == f"processed-{data_cache.cache_key()}.tar"
    assert [p.name for p in cache.iterdir()] == [arc.name]          # stale archive removed
    assert data_cache.restore(cache, dst) == 1
    assert (dst / "processed" / "en-is" / "wmt_train.jsonl").read_text() == "a\n"
    (dst / "processed" / "en-is" / "wmt_train.jsonl").write_text("local\n")
    assert data_cache.restore(cache, dst) == 0                       # existing files are kept
    assert (dst / "processed" / "en-is" / "wmt_train.jsonl").read_text() == "local\n"


def test_miss_returns_zero(tmp_path):
    assert data_cache.restore(tmp_path, tmp_path / "data") == 0


def test_key_is_stable():
    assert data_cache.cache_key() == data_cache.cache_key() and len(data_cache.cache_key()) == 12
