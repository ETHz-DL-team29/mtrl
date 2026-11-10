"""Zero-shot statistics: one row per (direction, model, thinking).

Inputs: rollouts.jsonl, scores.jsonl, compute.jsonl (score-stage FLOPs).
Outputs: report/summary.{csv,md} + report/*.png.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from mtrl.common.flops_accounting import rollout_cost
from mtrl.common.jsonl_io import read_jsonl
from mtrl.common.records import GATE_REASONS, KEY_FIELDS, direction_of

GROUP = ["direction", "model", "thinking"]
# Categorical slots 1..4 of the reference palette (fixed order, never cycled).
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def load_frame(run_dir: Path) -> pd.DataFrame:
    ro = pd.DataFrame(read_jsonl(run_dir / "rollouts.jsonl"))
    if ro.empty:
        raise SystemExit(f"no rollouts in {run_dir}")
    sc = pd.DataFrame(read_jsonl(run_dir / "scores.jsonl"))
    if sc.empty:
        sc = pd.DataFrame(columns=[*KEY_FIELDS, "gate_ok", "gate_reason", "metrics", "reward"])
    df = ro.merge(sc, on=list(KEY_FIELDS), how="left")
    df["direction"] = df["seg_id"].map(direction_of)
    metrics = pd.json_normalize(df["metrics"].map(lambda m: m if isinstance(m, dict) else {}))
    metrics.index = df.index
    return pd.concat([df.drop(columns=["metrics"]), metrics.add_prefix("m_")], axis=1)


def score_flops(run_dir: Path) -> dict:
    out: dict = {}
    for r in read_jsonl(run_dir / "compute.jsonl"):
        if r.get("type") == "score":
            k = (r["direction"], r["model"], r["thinking"])
            out[k] = out.get(k, 0.0) + r["flops"]
    return out


def _mean(s: pd.Series) -> float:
    s = s.dropna()
    return float(s.mean()) if len(s) else float("nan")


def summarize(df: pd.DataFrame, n_params: dict, scoring: dict, eps: float) -> pd.DataFrame:
    rows = []
    for (d, m, t), g in df.groupby(GROUP, sort=True):
        greedy, samp = g[g.sample_idx == -1], g[g.sample_idx >= 0]
        scored = g[g.gate_ok.notna()]
        row = {"direction": d, "model": m, "thinking": bool(t),
               "n_segments": g.seg_id.nunique(), "n_rollouts": len(g), "n_scored": len(scored)}
        for col in [c for c in g.columns if c.startswith("m_")]:
            row[f"{col[2:]}_greedy_mean"] = _mean(greedy[col])
        row["qe_greedy_mean"] = row.pop("metricx24_qe_greedy_mean", float("nan"))
        row["kiwi_greedy_mean"] = row.pop("cometkiwi22_greedy_mean", float("nan"))
        row["reward_greedy_mean"] = _mean(greedy.reward)
        row["reward_sample_mean"] = _mean(samp.reward)
        fail = scored.gate_ok == False  # noqa: E712  (object dtype after merge)
        row["gate_fail_rate"] = float(fail.mean()) if len(scored) else float("nan")
        for reason in GATE_REASONS[1:]:
            row[f"gate_fail_{reason}"] = float((scored.gate_reason == reason).mean()) if len(scored) else float("nan")

        grp = samp.dropna(subset=["reward"]).groupby("seg_id").reward
        if len(samp) and grp.ngroups:
            std = grp.std(ddof=0)
            row["reward_std_within_group_mean"] = float(std.mean())
            row["frac_low_variance_groups"] = float((std < eps).mean())
            row["best_of_G_minus_mean"] = float((grp.max() - grp.mean()).mean())
        else:
            row.update(reward_std_within_group_mean=float("nan"),
                       frac_low_variance_groups=float("nan"), best_of_G_minus_mean=float("nan"))

        row["reasoning_tokens_mean"] = float(g.n_reasoning_tokens.mean())
        row["translation_tokens_mean"] = float(g.n_translation_tokens.mean())
        gen = g.n_reasoning_tokens.sum() + g.n_translation_tokens.sum()
        row["reasoning_token_share"] = float(g.n_reasoning_tokens.sum() / gen) if gen else 0.0
        row["truncation_rate"] = float((g.finish_reason == "length").mean())
        row["parse_fail_rate"] = float((~g.parse_ok.astype(bool)).mean())
        gen_flops = rollout_cost(g.to_dict("records"), n_params[m])["total_flops"]
        row["gen_flops"] = gen_flops
        row["score_flops"] = scoring.get((d, m, bool(t)), 0.0)
        row["B_test_flops"] = gen_flops + row["score_flops"]
        rows.append(row)
    return pd.DataFrame(rows)


def to_markdown(summary: pd.DataFrame, cols: list[str]) -> str:
    def fmt(v):
        if isinstance(v, float):
            if np.isnan(v):
                return "-"
            return f"{v:.3g}" if abs(v) >= 1e4 or abs(v) < 1e-3 and v != 0 else f"{v:.3f}"
        return str(v)

    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in summary[cols].iterrows():
        lines.append("| " + " | ".join(fmt(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def plot_thinking(summary: pd.DataFrame, out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    models = list(summary.model.unique())
    fig, axes = plt.subplots(1, len(models), figsize=(5 * len(models), 3.6), squeeze=False, sharey=True)
    for ax, m in zip(axes[0], models):
        s = summary[summary.model == m]
        dirs = sorted(s.direction.unique())
        x = np.arange(len(dirs))
        for j, t in enumerate([False, True]):
            vals = [s[(s.direction == d) & (s.thinking == t)].reward_greedy_mean.mean() for d in dirs]
            ax.bar(x + (j - 0.5) * 0.36, vals, width=0.34, color=COLORS[j],
                   label=f"thinking {'on' if t else 'off'}")
        ax.set_xticks(x, dirs)
        ax.set_title(m.split("/")[-1], color=INK, fontsize=10, loc="left")
        _style(ax)
    axes[0][0].set_ylabel("greedy reward (mean)", color=INK2, fontsize=9)
    axes[0][-1].legend(frameon=False, fontsize=9, labelcolor=INK2)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


def plot_std_hist(df: pd.DataFrame, out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    samp = df[(df.sample_idx >= 0) & df.reward.notna()]
    fig, ax = plt.subplots(figsize=(6, 3.6))
    bins = np.linspace(0, 0.5, 26)
    for i, ((m, t), g) in enumerate(samp.groupby(["model", "thinking"], sort=True)):
        std = g.groupby(["direction", "seg_id"]).reward.std(ddof=0)
        ax.hist(std, bins=bins, histtype="step", linewidth=2, color=COLORS[i % len(COLORS)],
                label=f"{m.split('/')[-1]}, thinking {'on' if t else 'off'}")
    ax.set_xlabel("within-group reward std (G samples)", color=INK2, fontsize=9)
    ax.set_ylabel("# segments", color=INK2, fontsize=9)
    _style(ax)
    ax.legend(frameon=False, fontsize=8, labelcolor=INK2)
    fig.tight_layout()
    fig.savefig(out, dpi=150)
    plt.close(fig)


MD_COLS = ["direction", "model", "thinking", "n_segments", "qe_greedy_mean", "kiwi_greedy_mean",
           "reward_greedy_mean", "gate_fail_rate", "reward_std_within_group_mean",
           "frac_low_variance_groups", "best_of_G_minus_mean", "reasoning_tokens_mean",
           "translation_tokens_mean", "reasoning_token_share", "truncation_rate", "B_test_flops"]
GATE_COLS = ["direction", "model", "thinking", "gate_fail_rate"] + [f"gate_fail_{r}" for r in GATE_REASONS[1:]]


def run(run_dir: Path, n_params: dict, eps: float) -> pd.DataFrame:
    report = run_dir / "report"
    report.mkdir(parents=True, exist_ok=True)
    df = load_frame(run_dir)
    summary = summarize(df, n_params, score_flops(run_dir), eps)
    summary.to_csv(report / "summary.csv", index=False)
    md = ["# Zero-shot summary", "",
          f"Run: `{run_dir.name}`. MetricX-QE: lower is better (0-25). "
          f"Reward = gate x (1 - QE/25). Low-variance threshold eps = {eps}.", "",
          "## Main table", "", to_markdown(summary, MD_COLS), "",
          "## Gate failures by reason (share of scored rollouts)", "", to_markdown(summary, GATE_COLS), "",
          "Full columns: `summary.csv`. Figures: `reward_thinking.png`, `reward_std_hist.png`.", ""]
    (report / "summary.md").write_text("\n".join(md), encoding="utf-8")
    if df.reward.notna().any():
        plot_thinking(summary, report / "reward_thinking.png")
        plot_std_hist(df, report / "reward_std_hist.png")
    return summary
