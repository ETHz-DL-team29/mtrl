# 数据：方向和数据集的取舍

本文说明后训练用哪些语言方向、哪些数据，以及每一项取舍的理由。数据由
`python scripts/prepare_train_data.py` 按 `configs/train_data.yaml` 生成。背后的试点数据见
[language_selection.md](language_selection.md)。

## 0. 约束（来自 proposal 和助教回信）

| 约束 | 出处 |
|---|---|
| 低资源 English→xx，WMT26 覆盖的方向 | proposal "Data and models" |
| 训练用 WMT26 general-MT 数据 + MTData 公开平行语料 | 同上 |
| 语言集合由试点决定：提升空间、G=8 / T=1.0 下的组内 reward 方差、gate 失败率 | 同上 |
| 主结果在 held-out WMT26 测试集上，chrF++、COMET-22（需要参考译文）+ COMETKiwi22 + cESA | proposal "Evaluation" |
| FLORES+ 不进主结果（可能已被 Qwen 训练过） | proposal；助教 10-21 回信 |
| 只在开发数据上调参 | proposal "Experiments" |

## 1. 语言方向

**选定：en-hy（亚美尼亚语）、en-kk（哈萨克语）、en-be（白俄罗斯语）、en-is（冰岛语），外加 en-cs（捷克语）做中等资源对照。** 主模型 Qwen3.5-2B。

每个候选都要过五道筛，任何一道不过就不选：

| 筛选条件 | 为什么 |
|---|---|
| ① WMT26 测试集有参考译文（人工或 PseudoRef） | 主结果要报 chrF++ / COMET-22 |
| ② 有训练语料（WMT26 mtdata 配方） | SFT 预热和"等计算量 SFT"基准都需要平行数据 |
| ③ 有不依赖 WMT26 测试集的开发集 | 调参不能碰测试集 |
| ④ reward 在这门语言上可信：base 模型偏离目标语言时，gate 能拦住 | 否则 RL 会钻空子（见下面的 lij） |
| ⑤ 2B 上有学习信号：低方差组少、还有提升空间 | 没有信号的组 GRPO 拿不到梯度，计算全浪费 |

| 方向 | ① 参考 | ② 语料 | ③ 开发集 | ④ reward 可信 | ⑤ 2B 信号 | 结论 |
|---|---|---|---|---|---|---|
| en-hy | PseudoRef | 有 | NTREX | 是：0.8B 漂向俄语，gate 按书写系统拦下 | 低方差 12%，chrF 26.7 | **选** |
| en-kk | PseudoRef | 有 | NTREX | 是：漂向俄语，fastText 拦下 | 6%，chrF 27.4 | **选** |
| en-be | PseudoRef | 有 | NTREX | 是：漂向俄语，fastText 拦下 | 2%，chrF 32.3 | **选** |
| en-is | 人工 | 有 | NTREX、WMT24++、WMT25 | 是 | 22%，chrF 27.0 | **选**：唯一有人工参考的低资源方向，主结果不全靠合成参考 |
| en-cs | 人工 | 有 | NTREX、WMT24++、WMT25 | 是 | 1%，chrF 41.7 | **对照**：看方法在"本来就会"的语言上是否也有效 |
| en-et | 人工 / PseudoRef | 有 | 有 | 是 | 15%，chrF 35.4 | 不选：中等资源（OPUS 1.4 亿对），角色和 cs 重复，多一个方向多一份计算 |
| en-lij | 人工 | 4.3 万对 | ZenaMT val | **否**：输出是意大利语，fastText 和 MetricX 都分不出 | — | 不选 |
| en-lld | 人工 | 几乎全是界面字符串 | 只有 FLORES+ | **否**：同上 | — | 不选 |
| en-sme | 人工 | 界面字符串、错位多 | 无 | **否**：输出是芬兰语，lid.176 没有萨米语标签 | — | 不选 |
| en-arz | 人工 | 有 | WMT24++、WMT25 | **否**：输出是标准阿拉伯语，fastText 和 MetricX 都当成目标语言 | — | 不选 |
| 其余英语→xx | 只有 PseudoRef | 有 | 有 | — | — | 不选：不是低资源（de、ja、ko、ru、uk、zh、th、id） |

试点数字（120 句，单次运行）见 [language_selection.md](language_selection.md) 第 4、4b 节。

**关于 PseudoRef**：WMT26 在 2026-09-20 发布了 `data/systems/PseudoRef.jsonl`，从 cESA 人工评分最高的系统输出里挑选、再修补低分片段得到。它让 hy / kk / be 可以算参考译文指标，但它偏向产生它的那些系统，报告里要单列注明。is 同时有人工参考和 PseudoRef，可以用来估计两者的差距（`meta.pseudoref` 里保存了 is 的 PseudoRef）。

## 2. 训练数据

**规则（对每个方向相同）：WMT26 constrained mtdata 配方里，人工翻译的通用领域语料。**

| 语料 | 内容 | 取舍 | 理由 |
|---|---|---|---|
| TED2020 | TED 演讲字幕，志愿者翻译 | 用 | 人工翻译，口语化，接近 WMT26 测试集的语音领域（占 2/3） |
| QED | 教育视频字幕，众包翻译 | 用 | 同上 |
| Wikimedia | 维基百科条目翻译（Content Translation） | 用 | 人工翻译 / 译后编辑，通用领域 |
| Tatoeba | 例句 | 用 | 人工翻译；句子短，最少 4 词的规则会滤掉一部分 |
| News Commentary | 新闻评论 | 用（kk、cs 有） | 人工翻译，新闻领域 |
| NLLB、CCMatrix、CCAligned、ParaCrawl、HPLT、WikiMatrix | 网页自动挖掘 | 不用 | 噪声大（配方自己就把 lij 的 NLLB 注释成 "noisy"）；人工语料量已经够用；要用就得设计过滤规则，过滤本身会变成一个研究变量 |
| GNOME、KDE、Ubuntu、translatewiki | 软件界面字符串 | 不用 | 领域不对，句子极短，带占位符 |
| XLEnt、wikititles | 实体名、标题 | 不用 | 不是句子 |
| Bible、Tanzil | 宗教文本 | 不用 | 文体古旧 |
| OpenSubtitles | 电影字幕 | 不用 | 按时间轴对齐，错位多；人工语料已够 |

**清洗**（`src/mtrl/data/parallel_corpus.py`，被删的数量记在 `data/processed/{方向}/wmt_train.stats.json`）：

1. 英文 4–80 个词：太短的没有翻译内容，太长的超出 SFT 的 `max_len`。
2. 英文一侧 fastText 判为英语：去掉方向反了或错位的对。
3. **目标一侧必须通过 RL reward 用的同一个 gate**（非空、不是原文照抄、书写系统对、fastText 语种对、长度比合理）。理由：reward 会给 0 分的译文，不该拿来当 SFT 的模仿对象；训练数据和 reward 的标准一致。
4. 按归一化后的英文去重，保留先出现的。
5. **去污染**：英文出现在 NTREX-128、FLORES+ 或 WMT26 测试集里的对全部删掉。
6. 打乱后每个方向**最多取 2 万对**（固定种子）。

**为什么每个方向一样多（2 万对）**：比较不同语言时，训练数据量不能成为混杂因素。2 万对的依据：RL 1000 步只用 1000 个源句；SFT 1000 步 × 8 = 8000 个样本，2 万对够 2.5 个 epoch，等计算量 SFT 需要更多时也有余量。kk 的人工语料最少，上限按它定。

## 3. 开发数据

**NTREX-128**：newstest2019 的 1997 句英文，由专业译者译成 128 种语言，五个方向全覆盖。

| 切分 | 句数 | 用途 |
|---|---|---|
| `ntrex_val` | 200 | 训练中的贪心验证（训练曲线、早停） |
| `ntrex_dev` | 1797 | 选模型、开发评测 |

理由：
- 五个方向用**同一批英文**，各语言的开发结果可以直接比较。
- 都是**人工参考**。
- 是 WMT26 任务页推荐的开发集之一。
- 英文 2019 年就公开了，可能也被预训练见过（和 FLORES+ 一样），所以只用于开发，不报主结果。

没选的：WMT24++、WMT25 只覆盖 is / cs；FLORES+ 不含 be，而且 proposal 明确不用它。

## 4. 测试数据

**WMT26 General MT 测试集**，每个方向 198 个文档（语音 133、社交 44、新闻 14、软件 7）。

| 方向 | 参考译文 |
|---|---|
| en-is、en-cs | 人工（`meta.ref_type: human`） |
| en-hy、en-kk、en-be | PseudoRef（`meta.ref_type: pseudoref`） |

只在最后对选定的系统评测一次。输入是整篇文档（平均 852 字符），评测前要处理长度，这一步还没做。

## 5. 构建结果（2026-11-23，本地 4070 SUPER 服务器）

### 训练数据

| 方向 | 读入 | 清洗后 | 取用 | 删得最多的原因 | 取用的 2 万对来自 |
|---|---|---|---|---|---|
| en-hy | 99,095 | 55,850 | 20,000 | 重复 21,719（QED 和 TED 大量重叠）、太短 10,639 | TED 12.1k、Wikimedia 3.9k、QED 3.8k、Tatoeba 0.2k |
| en-kk | 41,286 | 31,346 | 20,000 | 重复 2,609、太短 2,389、长度比 2,036 | News Commentary 8.7k、TED 5.2k、Wikimedia 4.8k、QED 1.1k |
| en-be | 62,048 | 44,728 | 20,000 | 太短 6,716、重复 3,752、目标语种不对 2,078 | Wikimedia 7.1k、QED 6.6k、TED 4.2k、Tatoeba 2.1k |
| en-is | 44,093 | 30,799 | 20,000 | 太短 5,187、重复 3,273、目标语种不对 2,580 | QED 12.1k、Tatoeba 4.7k、Wikimedia 1.9k、TED 1.3k |
| en-cs | 1,057,291 | 798,835 | 20,000 | 重复 87,966、太短 70,531、长度比 55,859 | News Commentary 6.6k、QED 6.2k、TED 3.9k、Wikimedia 2.6k |

- 和开发 / 测试集撞车被删的：hy 17、kk 6、be 26、is 26、cs 150 句。
- 清洗后最少的是 is（3.08 万）和 kk（3.13 万），2 万的上限对每个方向都不卡。
- 每个方向被删的明细在 `data/processed/{方向}/wmt_train.stats.json`。

### 开发和测试数据

| 方向 | `ntrex_val` | `ntrex_dev` | `wmt26_test` |
|---|---|---|---|
| en-hy、en-kk、en-be | 200 | 1797 | 198 篇，PseudoRef |
| en-is、en-cs | 200 | 1797 | 198 篇，人工参考 |

### gate 校准检查

用 RL 的 gate 去检查人工参考译文本身：如果它拒掉很多人工译文，说明阈值（长度比、语种）对这门语言不合适。

| 方向 | NTREX 人工参考通过率 | WMT26 参考通过率 |
|---|---|---|
| en-hy | 99.2% | 197/198 |
| en-kk | 98.4% | 197/198 |
| en-be | 98.1% | 197/198 |
| en-is | 98.3% | 198/198 |
| en-cs | 98.6% | 198/198 |

被拒的少数主要是长度比（意译、省略）和 fastText 把很短的句子判错。阈值保持不变。
