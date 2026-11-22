# Post-training: how to run it

This is the training half of mtrl (the zero-shot half is in the main README). The design
and the migration from `results/ym` are described in [train_merge_plan.md](train_merge_plan.md).

## 1. The flow

```
FLORES+ dev (train) ──► [optional SFT] ──► RL loop ──► checkpoints ──► greedy eval on FLORES+ devtest
                                            │
          ┌─────────────────────────────────┴────────────────────────────────┐
          │ 1 rollout   B sources x G samples      generation/hf_generate.py │
          │ 2 reward    gate x (1 - MetricX/25)    scoring/reward.py         │
          │ 3 advantage standardise per group      train/advantage.py        │
          │ 4 mask      token weights              train/masks.py            │
          │ 5 update    clipped PG, token-level    train/losses.py, train/rl │
          └──────────────────────────────────────────────────────────────────┘
```

Every box is chosen in the training YAML; a new method is usually one registered
function plus one YAML.

| Knob (YAML) | Options | Code |
|---|---|---|
| `method` | `rl`, `sft` | `train/rl.py`, `train/sft.py` |
| `init.from` | `base`, a run name, an adapter dir | `train/common.py` |
| `adapter` | LoRA `targets: all/attn/mlp`, `layers`, `r`, `alpha` | `train/policy.py` |
| `algorithm` | `group`, `prompts_per_step`, `ppo_epochs`, `clip_low/high`, `zero_var_retries`, `ent_coef` | `train/rl.py`, `train/losses.py` |
| `reward` | `mode: qe/ref`, `gate: main/ym_compat` | `scoring/reward.py`, `scoring/rule_gate.py` |
| `mask` | `full`, `randpos`, `semi`, `block`, `vocab`, `content`, `highent`, `lowent`, `translation` | `train/masks.py` |

`ppo_epochs: 1` (default) is purely on-policy: the importance ratio is exactly 1 and the
clip never acts. That is what `results/ym` ran under the name "DAPO". Set `ppo_epochs > 1`
to reuse each batch of rollouts for several updates with the clip active.

## 2. Two processes, two envs

Training and evaluation run in the `mtrl` env (transformers 5.x, peft). MetricX needs
the `mtrl-score` env (transformers 4.x), so it runs as a small HTTP service
(`scripts/scorer_server.py`, port 8765) that the trainer starts on its own when nothing
answers. Both share the GPU: Qwen3.5-0.8B + LoRA training and MetricX-24-large fit in
12 GB with G = 8 and 224 new tokens.

## 3. Commands

```bash
conda activate mtrl
python scripts/prepare_train_data.py configs/train/quick_rl.yaml      # FLORES+ -> data/processed (once)
python scripts/train.py configs/train/quick_rl.yaml                   # 6-step smoke test
python scripts/train.py configs/train/ym/wide_all_ref.yaml            # a real run; re-run to resume
python scripts/eval_adapter.py configs/train/ym/wide_all_ref.yaml     # latest checkpoint on FLORES+ devtest
python scripts/eval_adapter.py configs/train/quick_rl.yaml --base     # base model, same data and prompt
python scripts/compare_runs.py                                        # table over runs/*/eval
```

FLORES+ is gated on Hugging Face: accept its terms with the account of `HF_TOKEN` first.
`scripts/check_language_drift.py` reports, for en-lij and en-lld, how many outputs are closer
to the Italian FLORES+ reference than to the target one: MetricX cannot tell these
languages from Italian, and RL from the base model drifts into Italian (see
train_merge_plan.md, section 3). Watch it on every RL run for these directions.

`scripts/convert_ym_ckpt.py` turns a `results/ym` checkpoint (`latest.pt`) into an adapter
directory for `eval_adapter.py --adapter` or `init.from`.

## 4. Outputs

`runs/{run_name}/`:

| File | Content |
|---|---|
| `config.resolved.yaml` | merged config, env, git commit |
| `train_log.jsonl` | one line per step: reward, MetricX, gate pass and reasons, entropy, ratio, clip fraction, grad norm, token counts, B_test / B_back FLOPs, timings, VRAM, one sample |
| `val_log.jsonl` | in-training greedy validation (`data.val_limit` per direction) |
| `ckpt/step_NNNNNN/` | `adapter/` (PEFT) + `trainer_state.pt`; `ckpt/latest` names the newest |
| `eval/{split}_summary.json` | per direction: chrF++, reference MetricX, QE on all outputs, reward, gate pass (main and ym gate), truncation rate, gate reasons |
| `eval/{split}_segments.jsonl` | every output with its scores |

## 5. Platforms

One env config per machine (`configs/env/`); the training YAML never changes.

| Env | GPU | dtype | vLLM | Status |
|---|---|---|---|---|
| `local_4070S_12G` | RTX 4070 SUPER | bf16 | yes | tested |
| `dinfk_1080Ti_11G` | GTX 1080 Ti (D-INFK student cluster) | fp16 | no | written, not tested |
| `colab_T4_16G` | T4 | fp16 | no | written, not tested |

Set `max_hours` in `schedule` below the job limit (12 h on the cluster); the run stops
with a checkpoint and the same command resumes it.

## 6. Data

| Split | Source | Use |
|---|---|---|
| `flores_dev` | FLORES+ dev, 997 sentences per language | training |
| `flores_devtest` | FLORES+ devtest, 1012 sentences | validation and development evaluation |
| `test` | WMT26 General MT, 198 documents per direction | final evaluation only (zero-shot pipeline) |

Default directions: en-is, en-lij, en-lld (WMT26 directions with references and FLORES+
coverage). lid.176 has no label for Ligurian or Ladin, so for those the gate only rejects
outputs identified as English (`configs/languages.yaml`).
