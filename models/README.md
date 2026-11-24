**最新WMT对照 / Latest WMT comparison: [SFT与本轮DAPO结果](../LATEST_RESULTS.md)**

# 模型与结果交付 / Models and research handoff

2026-11-24 · **三个核心适配器已公开上传Hugging Face；GitHub未提交或推送。 / Three core adapters are public on HF; GitHub remains uncommitted and unpushed.**

[公开模型链接与下载 / Public links and downloads](HUGGING_FACE.md)

朋友从这里开始 / Start here:

1. 可按[HF指南](HUGGING_FACE.md)下载三个核心模型；完整本地包可解压 `deliveries/mtrl-models-2026-11-24-hf-linked.zip`，进入其中的 `mtrl`。它含代码、报告和实际适配器。单独git clone不会取得被忽略的大权重。
2. `python scripts/models.py list` 列出可用版本；`python scripts/models.py verify` 校验本地文件。两条命令不加载模型，不需要torch/GPU，也不会联网。
3. 在自己的GPU环境安装PyTorch及 `pip install -r setup/requirements-checkpoint-use.txt`，然后运行下面的推理命令。首次需要下载固定版本的公开Qwen基座；已有同版缓存可用 `--base-path` 和 `--offline`。

Extract the recipient ZIP, enter its `mtrl` directory, then list and verify adapters without neural dependencies or network access. Install a GPU-compatible PyTorch and the listed inference requirements. The first explicit generation downloads the pinned public base unless an appropriate local base is supplied. The ZIP contains LoRA deltas, not full base weights.

## 推荐入口 / Recommended entry points

| ID | 用途 / Role | 阶段 / Stage |
|---|---|---|
| `qwen25-3b-sft-r0` | 当前共同3B起点P18 / shared 3B baseline | SFT |
| `qwen35-08b-sft-r0` | 保留的0.8B基线 / preserved 0.8B R0 | SFT |
| `qwen35-08b-sft-technical` | 0.8B技术补强候选，非已证明最优 / technical candidate | SFT |
| `qwen25-3b-dapo-shortmid` | 本轮P25开发集选中120步 / current dev-selected step120 | DAPO |
| `qwen25-3b-dapo-reference` | 前一轮P22 DAPO-120 / previous comparison | DAPO |

此外保留有明确推理目录的历史SFT版本，见下方完整清单。它们不是每次训练的全部中间快照，也不表示越晚或名字含best就一定更好。原始文件未移动或覆盖。

Historical SFT adapters with explicit inference folders are also preserved below. These are not every intermediate training snapshot and are not ranked by quality. Original files remain unchanged.

## 推理与继续训练 / Inference and further training

```bash
python scripts/models.py generate --model qwen25-3b-sft-r0 --text "Put the book on the table."
python scripts/models.py generate --model qwen35-08b-sft-r0 --text "Put the book on the table."
python scripts/models.py generate --model qwen25-3b-dapo-shortmid --text "Put the book on the table." --samples 8
```

默认是与记录匹配的FP32路径（0.8B先按BF16载入基座，再提升到FP32）。3B的该模式需要比11–12GB显存更多的空间；小显存普通推理可显式选择 `--precision bfloat16`（支持BF16的GPU）或 `--precision float16`。改变精度不保证复现报告数值。没有在本机重新运行神经推理或训练。

The default is the recorded-style FP32 path. For ordinary inference on smaller GPUs choose a supported reduced precision explicitly; this is not a promise of score equivalence. No neural inference or training was rerun on the packaging computer.

```bash
python scripts/models.py generate --model qwen25-3b-sft-r0 --precision float16 --text "Hello."
python scripts/models.py generate --model qwen25-3b-sft-r0 --base-path /path/to/pinned/qwen-base --offline --text "Hello."
```

Python API，适合接入朋友自己的SFT/RL代码 / Integrate into your own SFT/RL code:

```python
from mtrl.checkpoints import load_translation_model, translate

model, tokenizer, info = load_translation_model(
    "qwen25-3b-sft-r0", device="cuda", trainable=True,
)
# Existing LoRA parameters are trainable. No optimizer step happens here.
# Exact historical DAPO additionally requires its archived dropout/optimizer/sampling settings.
```

先 `pip install -e .` 或将repo的 `src` 加到PYTHONPATH。任意迁移任务的能力未验证；这些权重主要针对英语→冰岛语。模型仍会错译关键术语和否定。训练API是普通继续微调入口，完整优化器/RNG未放入朋友模型包，不能声称精确续跑旧优化器状态。

Install the local package or add `src` to PYTHONPATH. English-to-Icelandic is the demonstrated task. Other tasks are not validated. These research models can mistranslate critical facts. The API exposes adapter continuation, not an exact historical optimizer/RNG resume.

Colab示例 / Colab example: [notebooks/use_shared_models.ipynb](../notebooks/use_shared_models.ipynb). It performs inference only unless you separately write a training loop.

## 结果与代码 / Results and executed code

- [完整结果入口 / Results index](../results/local_translation_release_2026-11-24/README.md)
- [模型元数据与SHA256 / Registry and hashes](registry.json)
- `results/local_translation_release_2026-11-24/project_snapshot/experiments/`保存P18 SFT、0.8B技术SFT及P25 DAPO执行源码，旧绝对路径/预算只作历史记录，不应直接重跑旧截止文件。
- 原有合作者 `src/mtrl/train/`、评分器及实验实现未被替换。新增加载器只负责已保存权重的使用。

Executed historical scripts are archived separately; the collaborator's original training/scoring code was not replaced. Historical scripts include fixed Colab paths and expired absolute budgets and are not a new training launch command.

## 本地存放与未来分享 / Storage and future sharing

当前权重真实文件在repo内 `artifacts/translation_models_2026-11-24/<ID>/`，注册表使用相对路径，因此完整ZIP可移动到朋友电脑。该目录及 `deliveries/` 已被Git忽略；代码、注册表、模型卡与结果是正常repo文件。模型原副本均保留。

Three selected models are now hosted publicly with pinned commits and verified weights. See [HUGGING_FACE.md](HUGGING_FACE.md). The full local ZIP preserves all14 adapters; historical variants were not uploaded.

## 使用许可 / Base licenses

朋友可以按项目授权加载推理、继续微调；“可以使用”不意味着取消基座或原始数据许可。Qwen3.5-0.8B标注Apache-2.0；Qwen2.5-3B-Instruct标注qwen-research，不能统称为无限制商业使用。没有替你们选择或修改repo/适配器的独立许可证。

Base-model and source-data terms still apply. This handoff does not relicense the repository or adapters. Official pinned model cards:

- [Qwen3.5-0.8B / Apache-2.0](https://huggingface.co/Qwen/Qwen3.5-0.8B/blob/2fc06364715b967f1860aea9cf38778875588b17/README.md)
- [Qwen2.5-3B-Instruct / qwen-research](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/aa8e72537993ba99e69dfaafa59ed015b17504d1/README.md)

## 完整本地模型清单 / Complete local adapter inventory

|ID|Stage|LoRA r|Weight MiB|Card|
|---|---|---:|---:|---|
|`qwen25-3b-sft-r0`|sft|64|456.81|[card](cards/qwen25-3b-sft-r0.md)|
|`qwen25-3b-dapo-shortmid`|dapo|64|456.81|[card](cards/qwen25-3b-dapo-shortmid.md)|
|`qwen35-08b-sft-r0`|sft|16|41.34|[card](cards/qwen35-08b-sft-r0.md)|
|`qwen35-08b-sft-technical`|sft|16|41.34|[card](cards/qwen35-08b-sft-technical.md)|
|`qwen25-3b-dapo-reference`|dapo|64|456.81|[card](cards/qwen25-3b-dapo-reference.md)|
|`archive-r0-3b-coverage-sft-2026-11-20-final-selected-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-coverage-sft-2026-11-20-final-selected-adapter.md)|
|`archive-r0-3b-filtered-sft-resume-2026-11-20-final-selected-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-filtered-sft-resume-2026-11-20-final-selected-adapter.md)|
|`archive-r0-3b-overnight-2026-11-18-final-selected-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-overnight-2026-11-18-final-selected-adapter.md)|
|`archive-r0-3b-round1-2026-11-17-final-trained-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-round1-2026-11-17-final-trained-adapter.md)|
|`archive-r0-3b-round1-2026-11-17-selected-candidate-adapter`|sft|16|114.25|[card](cards/archive-r0-3b-round1-2026-11-17-selected-candidate-adapter.md)|
|`archive-r0-colab-2026-11-11-best-adapter`|sft|16|41.34|[card](cards/archive-r0-colab-2026-11-11-best-adapter.md)|
|`archive-r0-technical-sft-2026-11-17-final-trained-adapter`|sft|16|41.34|[card](cards/archive-r0-technical-sft-2026-11-17-final-trained-adapter.md)|
|`archive-r0-v2-colab-2026-11-12-best-adapter`|sft|16|41.34|[card](cards/archive-r0-v2-colab-2026-11-12-best-adapter.md)|
|`archive-r0-v3-colab-2026-11-13-best-adapter`|sft|16|41.34|[card](cards/archive-r0-v3-colab-2026-11-13-best-adapter.md)|
