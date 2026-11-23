"""Run one or more training configs end to end: data -> train -> evaluate -> compare.

    python scripts/run_experiments.py configs/train/ym/sft_full.yaml configs/train/ym/wide_all_ref.yaml
    python scripts/run_experiments.py my_try.yaml --data-cache /content/drive/MyDrive/mtrl/data_cache

The same command works on every platform (the env config comes from --env or MTRL_ENV);
setup/colab_run.ipynb is a thin wrapper around it. Steps:

  1. data      build the training / dev splits for the directions the configs use
               (scripts/prepare_train_data.py --directions ...; existing files are kept).
               With --data-cache DIR, data/processed is restored from DIR first and saved
               back afterwards (scripts/data_cache.py), so a fresh runtime skips the build.
  2. train     scripts/train.py per config, in order. A run that already has checkpoints
               resumes; a finished run returns at once. Output is filtered to progress
               lines; on failure the last 40 lines are printed in full.
  3. evaluate  scripts/eval_adapter.py per config on its eval split (skip: --no-eval).
  4. compare   scripts/compare_runs.py restricted to these runs.

A config may live outside the repo (e.g. on Drive) and inherit from one in it:
    base: /content/mtrl/configs/train/ym/wide_all_ref.yaml
    run_name: try_lr_5e-5
    optim: {lr: 5.0e-5}
The merged config and the git commit are saved in runs/{run_name}/config.resolved.yaml.
"""
import argparse
import collections
import subprocess
import sys
from pathlib import Path

from mtrl.common.config import REPO_ROOT, resolve_env_name
from mtrl.common.train_config import load_train_config

PY = sys.executable
PROGRESS = ("[train]", "[sft]", "[rl]", "[val]", "[scorer]", "[data]", "[eval]", "[cache]")


def run(cmd: list[str], tags=PROGRESS) -> None:
    """Run a step, print its progress lines, and on failure its last 40 lines in full."""
    print(f"\n$ {' '.join(cmd)}", flush=True)
    tail = collections.deque(maxlen=40)
    p = subprocess.Popen(cmd, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in p.stdout:
        tail.append(line.rstrip())
        if line.startswith(tags):
            print(line.rstrip()[:300], flush=True)
    if p.wait() != 0:
        print(f"\n*** FAILED (exit {p.returncode}): {' '.join(cmd)}\n--- last lines ---\n" + "\n".join(tail), flush=True)
        raise SystemExit(p.returncode)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("configs", nargs="+", help="training YAMLs, run in this order")
    ap.add_argument("--env")
    ap.add_argument("--data-cache", help="directory to restore / save data/processed (e.g. on Google Drive)")
    ap.add_argument("--no-eval", action="store_true", help="train only")
    ap.add_argument("--skip-data", action="store_true", help="assume the data is already built")
    args = ap.parse_args()
    env_name = resolve_env_name(args.env)
    runs = [load_train_config(c, env_name) for c in args.configs]   # fail fast on a bad config
    names = [r.train.run_name for r in runs]
    if len(set(names)) != len(names):
        raise SystemExit(f"two configs share a run_name: {names}")
    env = runs[0].env
    data_dir = env.path("data_dir")
    directions = sorted({d for r in runs for d in r.train.data["directions"]})
    print(f"[run] env {env_name}; runs {names}; directions {directions}", flush=True)

    if not args.skip_data:
        if args.data_cache:
            run([PY, "scripts/data_cache.py", "restore", args.data_cache, "--data-dir", str(data_dir)])
        run([PY, "scripts/prepare_train_data.py", "--env", env_name, "--directions", *directions])
        if args.data_cache:
            run([PY, "scripts/data_cache.py", "save", args.data_cache, "--data-dir", str(data_dir)])

    for cfg in args.configs:
        run([PY, "scripts/train.py", str(cfg), "--env", env_name])
    if args.no_eval:
        return
    splits = set()
    for cfg, r in zip(args.configs, runs):
        run([PY, "scripts/eval_adapter.py", str(cfg), "--env", env_name])
        splits.add(r.train.eval["split"])
    for split in sorted(splits):
        run([PY, "scripts/compare_runs.py", "--split", split, "--runs-dir", str(env.path("runs_dir")), "--runs", *names],
            tags=("",))


if __name__ == "__main__":
    main()
