# Local sharing delivery / 本地分享交付 — 2026-11-24

- 14份适配器真实副本：12 SFT、2 DAPO，含0.8B/3B默认基线和明确标记的历史版本；原文件未移动或覆盖。
- 首页和LATEST_RESULTS.md突出最新P25结果，主WMT对照、探索性子集、置信区间和未证明事项均保留。
- 统一命令：`python scripts/models.py list`、`python scripts/models.py verify`、`python scripts/models.py generate --model qwen25-3b-sft-r0 --text "Hello."`。
- Python继续训练入口：`mtrl.checkpoints.load_translation_model(...,trainable=True)`；不含完整优化器状态，不等同精确续跑旧实验。
- 完整41项CPU测试通过；14份模型哈希/张量结构通过。未在本机重新加载神经模型、推理或训练，未分配GPU。
- 已修改的原有文件只有README.md和.gitignore；原训练/评分代码保留。新代码和结果未git add/commit/push，三个核心适配器已公开上传HF。
- 可给朋友的完整ZIP在deliveries/mtrl-models-2026-11-24.zip，压缩包顶层为mtrl；大权重位于artifacts且被Git忽略。
- 单独git clone不会取得权重。ZIP包含LoRA而非完整Qwen基座；首次显式加载需要同一固定revision的公开基座，或使用自己的本地缓存。
- Hugging Face已公开托管两个SFT基线及最新DAPO候选；GitHub代码、注册表和报告只保留本地，待用户审核后自行推送。
- 基座许可不同：0.8B Apache-2.0；3B qwen-research。朋友的使用仍须遵守对应许可及数据条款。

GitHub code/results remain local; three selected adapters are public on Hugging Face. The original research files and collaborator implementation remain preserved. The recipient ZIP contains code, reports and14 hash-verified LoRA adapters, without base weights, credentials or private runtime sessions.41 CPU tests pass. No neural run, Git commit or push was performed; the three authorized HF model uploads were verified. See models/README.md for portable usage and LATEST_RESULTS.md for the latest evidence.

公开仓库与固定版本：[models/HUGGING_FACE.md](models/HUGGING_FACE.md)。更新交付ZIP：`deliveries/mtrl-models-2026-11-24-hf-linked.zip`；原ZIP保留。
