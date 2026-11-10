"""Run the whole zero-shot evaluation for one config:

    python scripts/run.py configs/quick.yaml
    python scripts/run.py configs/zeroshot.yaml

Stages, each in its own process (generation and scoring never share the GPU):
    download -> prepare -> generate -> score -> analyze
`generate` runs with the env config's python.generate interpreter (vLLM env), all other
stages with python.score (scoring env); without a `python` entry, the current interpreter.
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
# Which interpreter group runs each stage (env config key `python`): vLLM lives in the
# "generate" env; every other stage runs in the "score" env.
STAGE_GROUP = {"download": "score", "prepare": "score", "generate": "generate",
               "score": "score", "analyze": "score"}


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
    todo = [s for s in STAGES if s in stages]
    try:   # resolve every interpreter before starting, so a missing env fails immediately
        pythons = {s: cfg.env.python_for(STAGE_GROUP[s], default=sys.executable) for s in todo}
    except FileNotFoundError as e:
        raise SystemExit(str(e))

    for stage in todo:
        python = pythons[stage]
        cmd = [python, str(here / SCRIPTS[stage]), "--config", args.config, "--env", env_name]
        print(f"\n===== {stage} [{python}]: {' '.join(cmd[1:])}", flush=True)
        with open(log_dir / f"{stage}.log", "a", encoding="utf-8") as log:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            for line in proc.stdout:
                sys.stdout.write(line)
                log.write(line)
            rc = proc.wait()
        if rc != 0:
            raise SystemExit(f"stage '{stage}' failed (exit {rc}); see {log_dir / (stage + '.log')}. "
                             f"Fix it and re-run the same command to resume.")
    print(f"\ndone: {', '.join(todo)}. Run dir: {cfg.run_dir}")


if __name__ == "__main__":
    main()
