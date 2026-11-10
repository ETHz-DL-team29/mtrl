"""Run the whole zero-shot evaluation for one config:

    python scripts/run.py configs/quick.yaml
    python scripts/run.py configs/zeroshot.yaml

Stages, each in its own process (generation and scoring never share the GPU):
    download -> prepare -> generate -> score -> analyze
Every stage is resumable, so re-running the same command continues where it stopped.
Output of each stage is also written to runs/{run_name}/logs/{stage}.log.
"""
import argparse
import subprocess
import sys
from pathlib import Path

from mtrl.common.config import load_config

STAGES = ["download", "prepare", "generate", "score", "analyze"]
SCRIPTS = {"download": "download.py", "prepare": "prepare_data.py", "generate": "generate.py",
           "score": "score.py", "analyze": "analyze.py"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", help="experiment YAML, e.g. configs/zeroshot.yaml")
    ap.add_argument("--env", help="env name (default: MTRL_ENV from .env)")
    ap.add_argument("--stages", default=",".join(STAGES),
                    help=f"comma-separated subset of {','.join(STAGES)} (default: all)")
    args = ap.parse_args()

    stages = [s.strip() for s in args.stages.split(",") if s.strip()]
    unknown = set(stages) - set(STAGES)
    if unknown:
        ap.error(f"unknown stages: {sorted(unknown)}")
    cfg = load_config(args.config, args.env)          # validates config + env name up front
    env_name = cfg.env.name
    log_dir = cfg.run_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    here = Path(__file__).resolve().parent

    for stage in [s for s in STAGES if s in stages]:
        cmd = [sys.executable, str(here / SCRIPTS[stage]), "--config", args.config, "--env", env_name]
        print(f"\n===== {stage}: {' '.join(cmd[1:])}", flush=True)
        with open(log_dir / f"{stage}.log", "a", encoding="utf-8") as log:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in proc.stdout:
                sys.stdout.write(line)
                log.write(line)
            rc = proc.wait()
        if rc != 0:
            raise SystemExit(f"stage '{stage}' failed (exit {rc}); see {log_dir / (stage + '.log')}. "
                             f"Fix it and re-run the same command to resume.")
    print(f"\ndone: {', '.join(s for s in STAGES if s in stages)}. Run dir: {cfg.run_dir}")


if __name__ == "__main__":
    main()
