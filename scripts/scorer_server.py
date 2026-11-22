"""Run the MetricX-24 scoring service (scoring env):

    conda activate mtrl-score && python scripts/scorer_server.py [--port 8765]

Training and adapter evaluation start it on their own when no server answers; run it
by hand to keep one server alive across several runs.
"""
import argparse

from mtrl.common.config import load_env, resolve_env_name
from mtrl.common.env_setup import setup_env
from mtrl.scoring.server import DEFAULT_PORT, serve


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--batch-size", type=int)
    args = ap.parse_args()
    env = load_env(resolve_env_name(args.env))
    setup_env(env)
    serve(env, args.port, args.batch_size)


if __name__ == "__main__":
    main()
