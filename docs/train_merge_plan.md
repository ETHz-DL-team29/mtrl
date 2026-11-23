# 后训练框架迁移合并（main + results/ym）

分支：`train/merge-ym`（基于 `origin/main` 482d8a2）
状态（2026-11-22）：迁移完成，已在本地 4070 SUPER 服务器上实测；集群和 Colab 的 env 配置已写，未实测。
使用说明见 [training.md](training.md)。

---

## 0. 背景

| | main（合并前） | results/ym |
|---|---|---|
| 定位 | 工整的框架，只做到 zero-shot 评测 | 最小化脚本，已经跑了约 80 组后训练 |
| 训练代码 | `src/mtrl/train/` 全是占位 | DAPO/GRPO、SFT、LoRA 范围、8 种 mask |
| 配置 | YAML，实验 / 硬件分开，带校验 | JSON 转命令行参数 |
| 数据 | WMT26 test | `data/train.jsonl`、`val.jsonl`，来源未提交 |
| gate | 空输出 / 抄原文 / fastText 语种 / 长度 | 空输出 / 词数比 / 书写系统 / `lang_gate`（文件缺失） |

目标：保留 main 的框架和约定，把 ym 验证过的训练逻辑拆成组件装进去，"换一种后训练方法 = 改一份 YAML，或加一个注册函数"。

## 1. 做了什么

### 1.1 新增和改动的模块

| 模块 | 内容 | 来自 ym 的哪部分 |
|---|---|---|
| `common/train_config.py` | 训练配置：`base:` 继承、按 method 校验必填项、与 env 配置不得同名 | `run_*.sh` 的 JSON 转参数 |
| `configs/train/` | `_common` / `_base_rl` / `_base_sft`，`quick_*` 冒烟，`ym/` 四个预设，`explore/` | `train/configs/*.json` |
| `data/flores_converter.py`、`scripts/prepare_train_data.py` | FLORES+ dev → 训练集，devtest → 验证集 | 替代来源不明的 `train.jsonl` |
| `generation/hf_generate.py` | 组采样（返回 token、有效位置）和贪心评测，产出标准 `Rollout` | `nightlib.rollout`、`generate_greedy` |
| `scoring/server.py`、`client.py` | MetricX HTTP 服务，内部调用 main 已验证的 `metrics.py`；OOM 时 batch 减半重试；训练端自动拉起 | `metricx_server.py`、`score_items` |
| `scoring/reward.py` | 批量 gate + MetricX（QE / ref）+ reward | `reward_and_gate` |
| `scoring/rule_gate.py` | 新增 `wrong_script` 规则；无 fastText 标签的语言只拒绝英文；`ym_gate` 兼容模式 | `gate.py` |
| `train/policy.py` | 只加载纯文本模型；LoRA 目标 all / attn / mlp + 层选择 | `build_targets`、`make_model` |
| `train/advantage.py`、`losses.py` | 组内标准化；非对称裁剪的策略梯度，按 token 归一化 | `run_dapo.py` 的 loss 段 |
| `train/masks.py` | mask 注册表：full、randpos、semi、block、vocab、content、highent、lowent、translation | `run_dapo.py` 的 mask 分支 |
| `train/rl.py`、`sft.py`、`common.py` | 两个训练器和共用的加载 / 续训 / 验证 / 计时 | `run_dapo.py`、`sft.py` |
| `train/checkpoint.py` | PEFT adapter + 优化器 / RNG，原子写入，保留最近 N 个 | `save_ckpt` |
| `train/evaluate.py`、`scripts/eval_adapter.py`、`compare_runs.py` | 统一评测（chrF++、ref MetricX、全量 QE、两种 gate、截断率）和汇总表 | `eval_suite.py`（写死的系统列表） |
| `scripts/convert_ym_ckpt.py` | ym 的 `latest.pt` → PEFT adapter（改写键名前缀） | — |
| `scripts/check_rollout_logprobs.py` | 核对采样与训练前向的 log-prob | — |
| `configs/env/` | `dinfk_1080Ti_11G`（替换原 euler 占位）、`colab_T4_16G`；路径支持 `${USER}` | — |

### 1.2 已定下的设计决策

> **2026-11-23 更新**：第 1、2 条已被替换。按 proposal，训练数据改为 WMT26 mtdata 配方里的人工翻译语料，开发集改为 NTREX-128，方向改为 en-hy / en-kk / en-be / en-is + en-cs 对照，主模型改为 2B。理由见 [data.md](data.md) 和 [language_selection.md](language_selection.md)。第 3 节的 FLORES+ 探索实验保留为历史记录。

1. **训练数据用 FLORES+，不用 WMT26。** WMT26 只有 test 集；ym 的数据字段（`prompt`/`source`/`ref`/`tgt_lang`）和语言集合（isl/lij/lld/sme，正好是 WMT26 中带参考译文的方向）都指向它是从 WMT26 test 切出来的，这一点尚未向 ym 确认。如果属实，ym 的结果有测试集泄漏。FLORES+ dev（997 句）训练、devtest（1012 句）做验证和开发评测，WMT26 只留作最终测试。
2. **默认方向 en-is、en-lij、en-lld。** 这三个方向在 WMT26 有参考译文，FLORES+ 也有覆盖（FLORES+ 没有 sme）。
3. **lid.176 识别不了利古里亚语和拉登语。** 实测 FLORES+ dev 的参考译文：lij 被判成 it/fr/ro/pms…，lld 被判成 es/pt/rm/it…，没有一句判对。所以这两种语言的 gate 只拒绝"被判成英文"的输出（即没翻译），再加书写系统检查。
4. **算法命名如实。** ym 的"DAPO"每批 rollout 只更新一次，ratio 恒为 1，裁剪不起作用。框架默认 `ppo_epochs: 1` 复现这个行为（单测证明梯度与 ym 原式逐元素一致），`ppo_epochs > 1` 时旧 log-prob 由训练前向重新计算，裁剪真正生效。
5. **零方差组的 token 保留在归一化分母里**（advantage 为 0），与 ym 一致。
6. **评测统一走 HF 贪心解码。** 集群没有 vLLM；HF 后端在所有平台上结果一致。
7. **两个进程共享一张卡。** 训练在 `mtrl` 环境，MetricX 在 `mtrl-score` 环境，通过 HTTP 通信。训练端每步结束后释放缓存显存，打分服务 OOM 时自动减半 batch。

## 2. 验证

| 检查 | 结果 |
|---|---|
| 单测（CPU + torch） | 服务器上全部通过：配置继承与校验、LoRA 目标数（attn 114 / mlp 72 / all 186，与 ym 报告一致）、advantage、loss 与 ym 原式梯度一致、裁剪、9 种 mask、FLORES 配对、gate 新规则、ym 转换键名 |
| RL 冒烟（`quick_rl`） | rollout → 打分 → 更新 → checkpoint → 验证全通；预热后每步约 2 秒，显存 3.2 GB |
| 断点续训 | 从 step 5 的 checkpoint 恢复，从 step 6 继续 |
| SFT 冒烟（`quick_sft`） | 每步约 1.1 秒，loss 下降 |
| ym checkpoint 转换 | 把新框架的 adapter 改写成 ym 格式再转回，权重逐位一致 |
| log-prob 一致性 | 采样与训练前向的 token log-prob 平均差 0.03（bf16 下递推和并行两种计算方式的数值差），B=3 带左填充时也是 0.028，左填充影响可忽略 |
| 显存共享 | 第一次批量实验时，训练进程缓存的显存挤掉了打分服务，验证阶段 OOM。已修复：每步后释放缓存、`expandable_segments`、打分服务 OOM 时减半 batch、验证失败不中断训练。修复后整批跑完无报错 |

## 3. 探索实验（2026-11-22，本地 4070 SUPER）

设置：训练用 FLORES+ dev（en-is / en-lij / en-lld 各 997 句）；评测用 FLORES+ devtest 每个方向前 200 句，HF 贪心解码，`max_new_tokens` 256，单种子。脚本 `scripts/run_explore.sh`，总耗时约 2 小时（SFT 1000 步约 25 分钟，每组 RL 1000 步约 32 分钟）。

| 系统 | 配置 | chrF++ ↑ | ref MetricX ↓ | QE ↓ | gate 通过 | 截断 |
|---|---|---|---|---|---|---|
| base | Qwen3.5-0.8B 零样本 | 16.3 | 17.4 | 16.6 | 53% | 33% |
| SFT | `ym/sft_full`，全层 LoRA，1000 步 | 31.4 | 14.9 | 13.4 | 93% | 7% |
| RL，ref reward | `ym/wide_all_ref`，attn LoRA，1000 步 | 26.1 | 11.0 | 8.5 | 93% | 1% |
| RL，QE reward | `ym/long_attn`，attn LoRA，1000 步 | 21.6 | 10.1 | 6.8 | 84% | 7% |
| **SFT → RL，ref reward** | `explore/sft_then_ref`，500 步 | **31.7** | **12.6** | 11.5 | **97%** | 1% |

三个方向的平均值；分方向的数字在服务器上的 `runs/compare_flores_devtest.csv`。

### 3.1 主要发现

**1. MetricX 分不清利古里亚语、拉登语和意大利语，RL 从 base 出发会退化成直接输出意大利语。** 把每条输出分别和目标语言参考译文、FLORES+ 意大利语参考译文比 chrF++（`scripts/check_language_drift.py`）：

| 系统 | lij：更像意大利语的比例 | lld：更像意大利语的比例 |
|---|---|---|
| base | 71% | 65% |
| SFT | 4% | 3% |
| RL，ref reward | 94% | 98% |
| RL，QE reward | 96% | 100% |
| SFT → RL，ref reward | 27% | 13% |

对照：人工的利古里亚语、拉登语参考译文与意大利语参考译文之间的 chrF++ 只有 28.5 和 25.1，两者区别明显。RL 输出的是标准意大利语，例如 "Siminoff ha dichiarato che le vendite sono aumentate…"，MetricX QE 却给到 1.5 的高分（0 最好）。lid.176 也帮不上忙，它本来就把真正的利古里亚语判成意大利语。这就是 RL 系统在 MetricX 上全面领先、chrF 却落后于 SFT 的原因。ym 报告里"QE 一路降、chrF 还在半山腰"，很可能有很大一部分也是这个原因。

**2. QE reward 在冰岛语上还会退化成乱码。** 例如 "viðjanjanjanjanjanju…" 拿到 QE 14.3，比正常译文还好；同一个模型有 80/200 句冰岛语输出被 gate 判为语种错误。QE reward 的验证集 chrF 在第 200 步达到最高（27.5），之后一路下降到 22.3。

**3. SFT 再接 RL 是目前唯一两头都好的组合。** chrF 与 SFT 持平（31.7 对 31.4），ref MetricX 和 QE 都明显更好，gate 通过率 97%。但 500 步里意大利语化已经从 4% 升到 27%（lij）、13%（lld），继续训下去大概率会重蹈覆辙。

**4. base 模型的主要毛病是不收尾。** 贪心解码时 33% 的输出被截断，被截断的输出里 77% 的词是重复的（如 "að vera að vera að vera…"）。SFT 和 RL 都基本治好了这一点（截断率 0–7%）。

### 3.2 对后续研究的含义

- reward 里需要一个"目标语言忠实度"项，单靠 MetricX 会被钻空子。可选做法：换用覆盖 lij / lld 的语种识别模型（例如 GlotLID，需核实）；或者对"比意大利语参考更像意大利语"的输出扣分；或者在 reward 里加入与参考译文的 chrF。
- 默认流程应当是先 SFT 再 RL，并监控意大利语化比例，用它来决定在哪一步停止。
- 以上都是单种子、每个方向 200 句的结果，结论方向明确，但具体数字需要多种子验证。由于数据不同（FLORES+ 对比 ym 的数据），这些数字不能直接和 ym 的报告比。

## 4. 还没做的

- [ ] 在 D-INFK 集群（1080 Ti，fp16）和 Colab 上实测 env 配置。
- [ ] 向 ym 确认训练数据来源（是否切自 WMT26 test），要回 `lang_gate.py`。
- [ ] 用 `convert_ym_ckpt.py` 转换集群上 `/work/courses/dl/team-29/w_night-exp/ckpt/` 里 ym 的 checkpoint，在 FLORES+ devtest 上和新训练的模型对比。
- [ ] 加速：编译安装 `causal_conv1d`；`prompts_per_step > 1`；用 vLLM 做 rollout。
- [ ] reward 加目标语言忠实度项（见 3.2），然后重跑 SFT → RL 的多种子对比。
- [ ] main 原计划的方法：thinking 打开时的 reasoning / translation mask、reasoning-prefix 复用（`train/prefixes.py` 仍是占位）。
- [ ] 最终在 WMT26 test 上评测（文档级输入，要先处理长度）。
