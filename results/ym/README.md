# ym · night experiments

`_zh.html` 是中文实验报告（Tufte 1120，KaTeX/highlight.js 本地）。

## 训练
```
cd results/ym
bash train/run_dapo.sh train/configs/wide_all_ref.json   # DAPO
bash train/run_sft.sh  train/configs/sft_full.json        # SFT baseline
```
脚本从 config JSON 生成 CLI 参数；`train/code/` 是实际跑的代码副本。

## Checkpoints
`/scratch/users/yimiwang/night-exp/ckpt/<tag>/latest.pt`
备份：`/work/courses/dl/team-29/w_night-exp/ckpt/`
Drive：`night-2026-11-11/ckpt/`

## 关键结果（isl/lij/lld）
| run | QE | chrF |
|---|---|---|
| base | 13.18 | 13.9 |
| SFT 4h | 13.10 | 28.6 |
| long_attn | 6.59 | 18.4 |
| wide_all_ref | 7.38 | 20.0 |
