"""Stage 3: zero-shot statistics -> runs/{run}/report/ (csv, md, png). CPU only."""
from _cli import base_parser

from mtrl.common.config import load_config


def main():
    args = base_parser(__doc__).parse_args()
    cfg = load_config(args.config, args.env)
    from mtrl.analysis.zeroshot_stats import run

    n_params = {m["name"]: m["n_params"] for m in cfg.exp.models}
    summary = run(cfg.run_dir, n_params, cfg.exp.analysis["low_variance_eps"])
    print(summary.to_string(max_cols=12))
    print(f"[analyze] report -> {cfg.run_dir / 'report'}")


if __name__ == "__main__":
    main()
