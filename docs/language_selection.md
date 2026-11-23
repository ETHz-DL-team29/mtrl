# 语言方向选择：数据盘点与试点（2026-11-22）

proposal 的设定：训练用 WMT26 general-MT 数据 + MTData 公开平行语料，开发用 WMT26 开发数据（往年测试集），主结果在 WMT26 测试集上，FLORES+ 不进主结果。原来的 is / lij / lld 是随手挑的，这里按数据和试点重新看一遍。

## 1. WMT26 测试集（2026-06-18 发布）

英语 → X 每个方向 198 个文档（新闻 14、社交 44、软件 7、语音 133），平均 852 字符。

| 有参考译文 | 没有参考译文 |
|---|---|
| ces, deu, jpn, isl, ekk（爱沙尼亚语）, arz（埃及阿拉伯语）, lij, lld, sme | hye, bel, kaz, ind, kor, rus, tha, ukr, zho, zho_TW |

**更新（2026-11-23）**：WMT26 仓库 2026-09-20 加了 `data/systems/PseudoRef.jsonl`（"add synthetic refs"），覆盖英语 → bel、hye、kaz、ind、kor、rus、tha、ukr、zho、zho_TW 以及 deu、ekk、isl、jpn。它是从 cESA 人工评分最高的系统输出里挑选、再修补低分片段得到的混合合成参考译文。所以 hy / be / kk 现在可以报 chrF++ / COMET-22，只是参考译文是合成的（偏向产生它的那些系统），要在报告里注明。cESA 人工标注也已发布（GitHub release `humeval`），可用于 proposal 里的 reward 审计。

## 2. 训练语料（WMT26 mtdata 配方 + OPUS 规模）

| 方向 | 平行语料 | 质量 |
|---|---|---|
| en-is | OPUS 约 4250 万对（CCMatrix、NLLB、HPLT、ParaCrawl…） | 充足 |
| en-et | 约 1.43 亿对 | 充足 |
| en-lij | 约 4.3 万对去重句子：ZenaMT 句级 3.3 万 + 文档级 1.9 万、OLDI seed 6200、SMOL 1700、Tatoeba 160；NLLB 1.1M 被官方注释掉（"noisy"） | 真句子，平均 14–23 词，可做 SFT |
| en-lld | 4.8 万对，其中 4.6 万来自 Motorola 手机界面字符串；≥5 个英文词的只有 1.7 万 | 基本是 UI 短语，平均 6 词 |
| en-sme | 7.8 万对，几乎全是 KDE / Ubuntu 界面和 opus100；有不少错位（英文配了别的语言） | 很差 |

ZenaMT、OLDI seed、SMOL 以及 lld / sme 的全部语料，和 FLORES+ dev/devtest、WMT26 测试集的英文句子没有任何重合（按归一化后整句精确匹配）。

注：mtdata 0.5.1 拉 ZenaMT（HF 配置名不匹配）和 OLDI seed（解析报错）会失败，直接用 huggingface_hub 下载。

## 3. 开发集覆盖

| 方向 | 可用开发集 |
|---|---|
| is, et | WMT25 测试集（87 文档，有参考）、WMT24++（998 句）、FLORES+、NTREX |
| arz | WMT25 en-ar_EG、WMT24++ ar_EG |
| cs | WMT25、WMT24++ |
| lij | ZenaMT validation/test（112 / 104 句）、FLORES+ |
| lld | 只有 FLORES+ |
| sme | 没有 |

WMT24++ 里埋了 canary GUID，用来检测是否被拿去训练过。

## 4. 试点：base 模型在各方向上的表现

设置：WMT24++ 里随机 120 句英文（所有方向同一批原文；社交 63、文学 29、新闻 16、语音 12），Qwen3.5-0.8B 和 2B，thinking 关，每句贪心 1 次 + 采样 8 次（T=1.0）。reward = gate × (1 − MetricX-QE/25)。配置 `configs/pilot_langs.yaml`，数据 `scripts/prepare_wmt24pp_pilot.py`，完整表 `docs/pilot_langs_summary.csv`。

| 方向 | 模型 | chrF（贪心，句均） | QE（贪心）↓ | gate 失败 | 低方差组比例 | 组内 reward 标准差 |
|---|---|---|---|---|---|---|
| en-cs（对照） | 0.8B | 29.2 | 15.3 | 12% | 42% | 0.075 |
| | 2B | 37.8 | 10.0 | 4% | 6% | 0.148 |
| en-is | 0.8B | 14.6 | 20.0 | 25% | **62%** | 0.035 |
| | 2B | 24.5 | 17.4 | 8% | 32% | 0.074 |
| en-et | 0.8B | 22.5 | 21.4 | 19% | **72%** | 0.025 |
| | 2B | 34.5 | 15.7 | 8% | 27% | 0.075 |
| en-arz | 0.8B | 21.7 | 8.8 | 5% | 1% | 0.147 |
| | 2B | 24.9 | 6.1 | 9% | 0% | 0.173 |
| en-lij | 0.8B | – | 13.0 | 17% | 2% | 0.147 |
| | 2B | – | 10.8 | 9% | 0% | 0.143 |
| en-lld | 0.8B | – | 17.3 | 37% | 5% | 0.142 |
| | 2B | – | 12.8 | 11% | 0% | 0.127 |
| en-sme | 0.8B | – | 16.1 | 31% | 10% | 0.111 |
| | 2B | – | 16.6 | 21% | 3% | 0.119 |

"低方差组"指 8 个样本 reward 标准差 < 0.02 的组，GRPO 在这些组上拿不到任何梯度。

### 输出到底是什么语言（fastText 对贪心输出的判断）

| 方向 | 0.8B | 2B |
|---|---|---|
| en-is | is 101/120 | is 114/120 |
| en-arz | ar 120/120 | ar 118/120，arz 1 |
| en-lij | it 49, fr 21, oc 13, en 13 | it 97, lmo 7 |
| en-lld | **en 41**, ku 8, sq 7 | it 54, ca 15, es 9 |
| en-sme | en 27, no 20, fi 20 | **fi 27**, en 18, cs 16 |

例子：同一句英文，2B 给 lij 和 lld 的输出几乎一样（"Congress ha non adoperà tuti i 12 lëgìs…" / "Congress ha non passàt tuti 12 lëgìs…"），都是一种泛北意大利方言的拼凑；给 sme 的输出是芬兰语（"Kongressa ei loppu 12 laissa…"）。

## 4b. 第二轮试点：NTREX-128（hy / kk / be）

设置同上，开发集换成 NTREX-128（newstest2019 英文 + 人工参考译文，覆盖 is、et、cs、hy、kk、be），120 句。配置 `configs/pilot_ntrex.yaml`，数据 `scripts/prepare_ntrex_pilot.py`，完整表 `docs/pilot_ntrex_summary.csv`。

| 方向 | 模型 | chrF（贪心） | QE ↓ | gate 失败 | 低方差组 | 组内 std | 贪心输出语种 |
|---|---|---|---|---|---|---|---|
| en-cs（对照） | 0.8B | 32.8 | 13.9 | 13% | 18% | 0.096 | cs 114 |
| | 2B | 41.7 | 7.6 | 6% | 1% | 0.174 | cs 119 |
| en-is | 0.8B | 16.7 | 20.7 | 21% | 48% | 0.040 | is 99 |
| | 2B | 27.0 | 15.9 | 11% | 22% | 0.083 | is 116 |
| en-et | 0.8B | 23.0 | 20.2 | 21% | 55% | 0.030 | et 105 |
| | 2B | 35.4 | 12.8 | 9% | 15% | 0.084 | et 119 |
| en-hy | 0.8B | **4.2** | 11.1 | **90%** | **98%** | 0.002 | **ru 70**, hy 26 |
| | 2B | 26.7 | 12.6 | 16% | 12% | 0.111 | hy 120 |
| en-kk | 0.8B | 14.5 | 14.4 | 60% | 54% | 0.032 | kk 65, **ru 45** |
| | 2B | 27.4 | 11.2 | 18% | 6% | 0.125 | kk 118 |
| en-be | 0.8B | 17.6 | 17.5 | 21% | 33% | 0.057 | be 96, ru 15 |
| | 2B | 32.3 | 9.8 | 8% | 2% | 0.138 | be 118 |

要点：

- **2B 在 hy / kk / be 上信号很好**：输出基本都是目标语言，低方差组只有 2–12%，比 is / et（15–22%）还少。
- **0.8B 在 hy 上不可用**：70% 的输出是俄语，90% 被 gate 拒（主要是书写系统不对），98% 的组没有信号；kk 上也有一半输出变成俄语。
- **和 lij / lld 的关键区别**：这里"冒充目标语言"的是俄语，fastText 和书写系统检查都能识别，gate 真的拦得住（hy 0.8B 的俄语输出 QE 只有 11，单看 MetricX 反而像好译文）。lij / lld 冒充的是意大利语，gate 拦不住。
- 语料：hy 1870 万、kk 3570 万、be 4870 万对，但大部分来自 NLLB 挖掘数据，需要过滤。开发集：NTREX-128，hy / kk 另有 FLORES+，kk 还有 WMT19 newstest。

## 5. 结论

1. **lij / lld / sme 上 base 模型基本不会这些语言。** 输出是意大利语、方言拼凑、芬兰语或英语，而 MetricX QE 照样给 10–17 分，组内方差还挺大，看起来"信号很好"。这正是 RL 最容易钻空子的情形（FLORES 探索实验里已经看到 lij / lld 退化成意大利语）。RL 本身不能凭空教会模型一门语言，这些方向必须先 SFT，而且 reward 要有"是不是目标语言"的判断。
2. **lld、sme 没有像样的训练数据**（界面字符串为主），sme 连开发集都没有。不建议做。
3. **arz 的问题是方言**：模型输出的是现代标准阿拉伯语，fastText 几乎全判成 ar，MetricX 也给高分。和 lij 类似，是"相近的大语言冒充目标语言"。
4. **is / et 的 reward 可信，但 0.8B 在 T=1.0 下大多数组没信号**（62–72% 低方差，多数是 8 个样本全被 gate 拒或全部很差）。2B 降到 27–32%。0.8B 上做 RL 需要更低的采样温度或先 SFT。
5. **cs（中等资源对照）在 2B 上信号最好**，可以作为"方法在正常语言上是否有效"的对照。

6. **hy / kk / be 在 2B 上是最合适的低资源方向**（第二轮试点）：reward 可信（gate 能拦住俄语），学习信号足，提升空间大，有 PseudoRef 可评测。

## 6. 建议（第二轮试点后更新）

| 角色 | 方向 | 参考译文 | 说明 |
|---|---|---|---|
| 低资源主线 | en-hy、en-kk、en-be | WMT26 PseudoRef（合成） | 2B 上信号最好；三种语言都会往俄语漂，gate 能识别 |
| 低资源，人工参考 | en-is | WMT26 人工 | 保证至少一个方向的主结果不依赖合成参考 |
| 中等资源对照 | en-cs（可加 en-et） | WMT26 人工 | 看方法在"本来就会"的语言上是否也有效 |
| 不选 | lij、lld、sme、arz | — | reward 被相近大语言冒充，或没有训练数据 / 开发集 |

主模型 2B。0.8B 在 hy 上几乎全是俄语，如果要做 0.8B 的规模对比，需要先 SFT，或者只在 is / be / cs 上做。

限制：每个方向只有 120 句、单次采样，用来排除方向足够，具体数字要在正式开发集上复核。lij / lld / sme 在 WMT24++ 上没有参考译文，所以没有 chrF。
