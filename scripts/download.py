"""Download everything a config needs. This is the only stage that uses the network,
so gated or missing files fail here instead of halfway through an overnight run.

  Hugging Face cache (env paths.hf_home):
    - policy models (config `models`)
    - scorer models for the configured metrics (MetricX, COMET family) and the
      tokenizers they load at run time (mT5; InfoXLM / XLM-R for COMET)
  Data dir (env paths.data_dir):
    - WMT26 General MT test set -> data/raw/wmt26-genmt.jsonl
    - fastText lid.176.bin      -> env paths.fasttext_lid
Files that are already present are skipped.
"""
import urllib.request

from _cli import base_parser

from mtrl.common.config import load_config
from mtrl.common.env_setup import setup_env
from mtrl.data.wmt26_converter import WMT26_URL, wmt26_raw_path

LID_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
TOKENIZER_FILES = ["*.json", "*.model", "*.txt"]   # tokenizer-only download (no weights)


def main():
    args = base_parser(__doc__).parse_args()
    cfg = load_config(args.config, args.env)
    setup_env(cfg.env)
    from huggingface_hub import snapshot_download
    from huggingface_hub.utils import GatedRepoError, RepositoryNotFoundError

    from mtrl.scoring import metrics as M

    def fetch(repo, **kw) -> bool:
        print(f"[download] {repo}", flush=True)
        try:
            snapshot_download(repo, **kw)
            return True
        except GatedRepoError:
            print(f"[download] {repo} is gated: accept its terms at https://huggingface.co/{repo} "
                  f"with the account of HF_TOKEN; the metric will be skipped until then")
        except RepositoryNotFoundError:
            print(f"[download] {repo} not found (or no access)")
        return False

    for m in cfg.exp.models:
        if not fetch(m["name"]):
            raise SystemExit(f"cannot download policy model {m['name']}")

    metrics = set(cfg.exp.metrics)
    if metrics & {"metricx24_qe", "metricx24_ref"}:
        repo = M.METRICX_MODEL["bf16"] if cfg.env.dtype == "bf16" else M.METRICX_MODEL["default"]
        if not fetch(repo) and not fetch(M.METRICX_MODEL["default"]):
            raise SystemExit("cannot download MetricX-24")
        fetch(M.METRICX_TOKENIZER, allow_patterns=TOKENIZER_FILES)
    for metric, repo in [("cometkiwi22", M.COMETKIWI_MODEL), ("comet22", M.COMET22_MODEL)]:
        if metric in metrics and fetch(repo):
            fetch(M.COMET_ENCODERS[repo], allow_patterns=TOKENIZER_FILES)

    for url, dest in [(WMT26_URL, wmt26_raw_path(cfg.env.path("data_dir"))),
                      (LID_URL, cfg.env.path("fasttext_lid"))]:
        if dest.exists():
            print(f"[download] {dest} exists, skipping")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"[download] {url} -> {dest}", flush=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        urllib.request.urlretrieve(url, tmp)
        tmp.replace(dest)   # no half-written file if interrupted
    print("[download] done")


if __name__ == "__main__":
    main()
