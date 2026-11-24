# Hugging Face 模型分享 / Public model sharing — 2026-11-24

三个模型已上传并公开，已通过匿名模型元数据和配置下载校验；远端LFS权重SHA256与本地原始适配器一致。GitHub没有提交或推送。

|本地ID / Local ID|Public Hub|Pinned commit|
|---|---|---|
| `qwen35-08b-sft-r0` | [huaq99/mtrl-qwen35-08b-en-is-sft-r0](https://huggingface.co/huaq99/mtrl-qwen35-08b-en-is-sft-r0) | `c95800cbefea66cbe449a482c7515a74a6984564` |
| `qwen25-3b-sft-r0` | [huaq99/mtrl-qwen25-3b-en-is-sft-r0](https://huggingface.co/huaq99/mtrl-qwen25-3b-en-is-sft-r0) | `ae660dd4ea272fff7caf840d2c9ccc76401e6780` |
| `qwen25-3b-dapo-shortmid` | [huaq99/mtrl-qwen25-3b-en-is-dapo-shortmid-v1](https://huggingface.co/huaq99/mtrl-qwen25-3b-en-is-dapo-shortmid-v1) | `1ec9cfaa813582bda509676497da2ffb2e69e6bc` |

这是LoRA适配器，不是完整Qwen基座。朋友可按基座许可推理或继续SFT/RL；无需你的HF登录或令牌。3B基座采用qwen-research许可，0.8B采用Apache-2.0；公开下载不取消原许可及数据条款。

## 从本地代码仓库下载 / Download using this repository

```bash
pip install huggingface_hub
python scripts/download_models.py --model all-hosted
python scripts/models.py verify --model qwen35-08b-sft-r0
python scripts/models.py verify --model qwen25-3b-sft-r0
python scripts/models.py verify --model qwen25-3b-dapo-shortmid
```

下载器只下载注册的三个适配器，并按固定commit与SHA256校验；其他历史版本使用完整本地ZIP。大权重被Git忽略，不能仅靠git clone取得。

GPU环境安装匹配的PyTorch和`setup/requirements-checkpoint-use.txt`后：

```bash
python scripts/models.py generate --model qwen25-3b-sft-r0 --text "Put the book on the table."
python scripts/models.py generate --model qwen25-3b-dapo-shortmid --text "Put the book on the table."
```

默认FP32路径显存需求较高。普通推理可显式使用`--precision float16`或支持的`bfloat16`；这不保证复现FP32评测分数。

无需GitHub上已有代码的独立Colab入口：[use_hf_models.ipynb](../notebooks/use_hf_models.ipynb)。下载本地notebook并上传Colab即可；本次没有启动GPU训练或运行该notebook。

HF的标准`adapter_config.json`已改为可迁移的基座ID和revision；`original_adapter_config.json`保存原始配置。权重字节完全不变。仓库下载器使用原配置恢复本地冻结哈希，统一加载器显式指定正确基座。

验证记录：[hf_publication.json](hf_publication.json)；结果：[LATEST_RESULTS.md](../LATEST_RESULTS.md)。完整本地模型包仍保留14份适配器。

The three public research adapters are pinned above. Public downloads require no account. The verified weight hashes match the source files; no merging, quantization or retraining occurred. Only three selected adapters are hosted; fourteen are preserved locally. GitHub code and results remain uncommitted and unpushed for your review.
