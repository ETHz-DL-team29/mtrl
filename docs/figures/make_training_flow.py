"""Draws docs/figures/training_flow.png (the post-training flow in docs/training.md).

    python docs/figures/make_training_flow.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).with_name("training_flow.png")
INK, MUTED, LINE = "#1f2328", "#57606a", "#8c959f"
STAGE, OPTIONAL, LOOP, STEP = "#dbe9f7", "#eef1f4", "#fff4d6", "#ffffff"


def box(ax, x, y, w, h, text, fc, ec=LINE, size=10.5, dashed=False, weight="normal", sub=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec,
                                lw=1.2, ls="--" if dashed else "-"))
    if sub:
        ax.text(x + w / 2, y + h * 0.62, text, ha="center", va="center", fontsize=size, color=INK, weight=weight)
        ax.text(x + w / 2, y + h * 0.28, sub, ha="center", va="center", fontsize=8.5, color=MUTED)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK, weight=weight)


def arrow(ax, x0, y0, x1, y1, style="-|>", color=LINE, rad=0.0):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=12, color=color, lw=1.3,
                                 connectionstyle=f"arc3,rad={rad}"))


def main():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=160)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    # top row: the pipeline
    top_y, h = 4.9, 0.9
    stages = [(0.2, 2.1, "Training data", "WMT26 mtdata corpora", STAGE, False),
              (2.75, 1.9, "SFT (optional)", "train/sft.py", OPTIONAL, True),
              (5.1, 1.9, "RL loop", "train/rl.py", LOOP, False),
              (7.45, 1.8, "Checkpoints", "train/checkpoint.py", STAGE, False),
              (9.7, 2.1, "Greedy evaluation", "NTREX-128 / WMT26", STAGE, False)]
    for x, w, t, s, fc, dashed in stages:
        box(ax, x, top_y, w, h, t, fc, dashed=dashed, weight="bold", sub=s)
    for (x, w, *_), (nx, *_ ) in zip(stages, stages[1:]):
        arrow(ax, x + w + 0.03, top_y + h / 2, nx - 0.03, top_y + h / 2)
    arrow(ax, 0.2 + 2.1 / 2 + 0.6, top_y - 0.02, 5.1 + 0.3, top_y - 0.02, color=MUTED, rad=0.25)  # data straight to RL
    ax.text(3.75, 4.16, "RL can also start from the base model", fontsize=8, color=MUTED, ha="center")

    # the RL loop, expanded
    lx, ly, lw, lh = 0.6, 0.25, 10.8, 3.75
    ax.add_patch(FancyBboxPatch((lx, ly), lw, lh, boxstyle="round,pad=0.02,rounding_size=0.12", fc=LOOP, ec=LINE, lw=1.2))
    ax.text(lx + 0.2, ly + lh - 0.3, "One RL step (every box is set in the training YAML)", fontsize=10.5,
            color=INK, weight="bold", va="center")
    arrow(ax, 6.05, top_y - 0.02, 6.05, ly + lh + 0.02, color=LINE)

    steps = [("1  Rollout", "B sources x G samples", "hf_generate.py"),
             ("2  Reward", "gate x (1 - MetricX/25)", "scoring/reward.py"),
             ("3  Advantage", "standardise per group", "train/advantage.py"),
             ("4  Mask", "per-token weights", "train/masks.py"),
             ("5  Update", "clipped PG, token-level", "train/losses.py")]
    sw, sh, gap, sy = 1.86, 1.55, 0.24, 1.45
    xs = [lx + 0.3 + i * (sw + gap) for i in range(len(steps))]
    for x, (t, d, f) in zip(xs, steps):
        ax.add_patch(FancyBboxPatch((x, sy), sw, sh, boxstyle="round,pad=0.02,rounding_size=0.08", fc=STEP, ec=LINE, lw=1.1))
        ax.text(x + sw / 2, sy + sh * 0.74, t, ha="center", va="center", fontsize=10.5, color=INK, weight="bold")
        ax.text(x + sw / 2, sy + sh * 0.46, d, ha="center", va="center", fontsize=8.2, color=INK)
        ax.text(x + sw / 2, sy + sh * 0.2, f, ha="center", va="center", fontsize=7.6, color=MUTED, family="monospace")
    for x0, x1 in zip(xs, xs[1:]):
        arrow(ax, x0 + sw + 0.02, sy + sh / 2, x1 - 0.02, sy + sh / 2)
    # back to the next step
    arrow(ax, xs[-1] + sw / 2, sy - 0.03, xs[0] + sw / 2, sy - 0.03, color=MUTED, rad=-0.18)
    ax.text((xs[0] + xs[-1] + sw) / 2, 0.42, "next step: new sources, updated policy", fontsize=8.5, color=MUTED, ha="center")
    ax.text(xs[2] + sw / 2, sy + sh + 0.2, "zero-variance groups are resampled (DAPO dynamic sampling)",
            fontsize=8, color=MUTED, ha="center")

    fig.savefig(OUT, bbox_inches="tight", facecolor="white")
    print(OUT)


if __name__ == "__main__":
    main()
