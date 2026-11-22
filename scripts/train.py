"""Train one run from a training config (training env, `conda activate mtrl`):

    python scripts/train.py configs/train/quick_rl.yaml
    python scripts/train.py configs/train/ym/wide_all_ref.yaml --env dinfk_1080Ti_11G

`method: rl` -> mtrl.train.rl, `method: sft` -> mtrl.train.sft. Outputs go to
runs/{run_name}/ (config.resolved.yaml, train_log.jsonl, val_log.jsonl, scorer.log) and
checkpoints to the run's ckpt dir. Re-running the same command resumes from the latest
checkpoint. The MetricX scoring service is started with the env's scoring interpreter
when none is running (see scripts/scorer_server.py).
Run scripts/prepare_train_data.py once first.
"""
import argparse

from mtrl.common.train_config import load_train_config


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--env")
    args = ap.parse_args()
    run = load_train_config(args.config, args.env)
    if run.train.method == "rl":
        from mtrl.train.rl import train
    else:
        from mtrl.train.sft import train
    train(run)


if __name__ == "__main__":
    main()
