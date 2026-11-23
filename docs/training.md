# Post-training: how to run it

This is the training half of mtrl (the zero-shot half is in the main README). The design
and the migration from `results/ym` are described in [train_merge_plan.md](train_merge_plan.md).

## 1. The flow

```
WMT26 mtdata corpora (train) ──► [optional SFT] ──► RL loop ──► checkpoints ──► greedy eval on NTREX-128
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
python scripts/prepare_train_data.py                                 # configs/train_data.yaml -> data/processed (once)
python scripts/train.py configs/train/quick_rl.yaml                   # 6-step smoke test
python scripts/train.py configs/train/ym/wide_all_ref.yaml            # a real run; re-run to resume
python scripts/eval_adapter.py configs/train/ym/wide_all_ref.yaml     # latest checkpoint on NTREX-128 (ntrex_dev)
python scripts/eval_adapter.py configs/train/quick_rl.yaml --base     # base model, same data and prompt
python scripts/compare_runs.py --split ntrex_dev                      # table over runs/*/eval
```

`scripts/prepare_train_data.py` needs the `mtdata` tool (env config `python.mtdata`, e.g. a
conda env with `pip install mtdata==0.5.1`).

Historical (FLORES+ era, en-lij / en-lld): `scripts/check_language_drift.py` reports, for en-lij and en-lld, how many outputs are closer
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

Which directions and datasets, and why: [data.md](data.md) (pilot behind it:
[language_selection.md](language_selection.md)). Built by `scripts/prepare_train_data.py`
from `configs/train_data.yaml`.

| Split | Source | Use |
|---|---|---|
| `wmt_train` | WMT26 mtdata recipe corpora (TED2020, QED, Wikimedia, Tatoeba, News Commentary), cleaned with the reward gate, deduplicated, decontaminated, 20k pairs per direction | training (SFT targets, RL sources) |
| `ntrex_val` | NTREX-128, 200 sentences | validation during training |
| `ntrex_dev` | NTREX-128, 1797 sentences | model selection, development evaluation |
| `wmt26_test` | WMT26 General MT, 198 documents per direction; human reference (is, cs) or PseudoRef (hy, kk, be) | final evaluation only |

Default directions: en-hy, en-kk, en-be, en-is (low-resource) and en-cs (mid-resource
control); default model Qwen3.5-2B. The `ym/` presets keep ym's Qwen3.5-0.8B.
