#!/usr/bin/env bash
# Exploration batch (2026-11-21): SFT, two RL rewards, SFT->RL, then greedy eval of every
# run plus the base model on FLORES+ devtest (200 per direction). Sequential on one GPU.
#   nohup bash scripts/run_explore.sh > runs/explore.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python}
for cfg in configs/train/ym/sft_full.yaml configs/train/ym/wide_all_ref.yaml \
           configs/train/ym/long_attn.yaml configs/train/explore/sft_then_ref.yaml; do
  echo "=== train $cfg $(date +%T)"
  $PY scripts/train.py "$cfg" || echo "!!! train failed: $cfg"
done
for cfg in configs/train/ym/sft_full.yaml configs/train/ym/wide_all_ref.yaml \
           configs/train/ym/long_attn.yaml configs/train/explore/sft_then_ref.yaml; do
  echo "=== eval $cfg $(date +%T)"
  $PY scripts/eval_adapter.py "$cfg" --limit 200 || echo "!!! eval failed: $cfg"
done
$PY scripts/compare_runs.py
echo "=== all done $(date +%T)"
