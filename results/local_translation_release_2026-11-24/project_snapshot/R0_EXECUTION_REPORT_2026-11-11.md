# R0 实际执行结果 / Actual execution results

记录日期 / Record date: 2026-11-11；生成时间 / Generated: 2026-11-12T00:07:04+01:00

**未通过 R0 自动筛查，保留为诊断候选 / R0 screen not passed; diagnostic candidate only。**

正式训练实际更新 **199,856** 个目标 token，要求预算为 200,000，该预算完成标记为 `True`。开发集选中的检查点位于 step 176、175,027 个目标 token，chrF++ **25.92**，结构失败率 **16.28%**，非冰岛语率 **0.00%**。不能仅凭 chrF++ 判断有效翻译。没有运行 DAPO，也没有测得创新方法的收益。

The formal run optimized 199,856 target tokens against a requested budget of 200,000. The dev-selected checkpoint has chrF++ 25.92, structural failure 16.28%, and wrong-language rate 0.00%. This is a single-seed SFT result. No DAPO updates or novel-method gains are claimed.

同一正式开发集上的原始基座为chrF++ **13.43**、结构失败 **38.37%**；这些是与本次候选匹配的描述性对照。 / On the same formal dev pool, the original base scores **13.43 chrF++**, with **38.37% structural failure**. This provides a matched descriptive comparison for this run.

## 训练协议 / Protocol

原始模型 `Qwen/Qwen3.5-0.8B`，固定 revision `2fc06364715b967f1860aea9cf38778875588b17`；LoRA r16/alpha32/dropout0.05。Tesla T4 使用 FP16、初始 loss scale512、SDPA；缺少 FLA/causal_conv1d 时使用参考实现。Microbatch2、effective batch16。目标 token 与 EOS 参与 CE，提示和填充不计入；按实际目标 token 归一化，不截断标签。

两个20k学习率试跑使用相同100k调度，各从原模型开始；正式阶段也重新从原模型开始，训练前固定300k最大调度，首次停止预算100k。后续预算决策只查看开发集，最后测试前冻结适配器 SHA256。试跑32条与正式86条生成dev口径不同，必须分开比较。

Both equal-budget pilots and the formal run start from the same original base. The formal 300k-token LR schedule was frozen before formal updates. Any continuation retains optimizer, scaler, RNG, data cursor and schedule. Pilot scores use 32 prompts; formal scores use 86 prompts. They are separate evaluation pools.

`formal_100k`目录名沿用首次预算点，实际累计token与请求预算以summary及本报告为准。 / The directory name `formal_100k` denotes the initial stop; the summary and this report record the actual continued budget and token count.

生成配置：thinking关闭、贪心解码；dev最多768prompt token、256new token。最终短句最多128new token，文档最多512new token，prompt仍最多768。文档可能受输入截断或输出预算约束，属于有限预算迁移诊断，不能据此断言模型在任何配置下都不能翻译文档。 / Generation uses greedy decoding with thinking disabled. Dev allows 768 prompt and 256 new tokens; final sentences allow 128 new tokens and documents 512, with the same 768-prompt-token cap. Document input/output limits constrain interpretation; this is a bounded transfer diagnostic, not a length-complete document benchmark.

## 数据与质量限制 / Data and limitations

最终5,085train /375dev，生成dev86条；1,198Tatoeba、3,887ParIce，训练目标共320,534token，平均63.04token。保留全部200条历史dev。915条train与25条新dev被最终OCR/对齐规则隔离。源文和参考译文精确去重，训练源文与完整WMT测试文档、旧探针精确隔离。没有文档ID、近重复检验或冰岛语母语者语义认证。ParIce法律技术文本占主导，不能宣称广泛领域覆盖。

The data are aligned sentences/short spans, not full-document training examples. Exact deduplication and automatic filtering do not establish semantic gold quality or document-level independence. The 60-pair AI-assisted audit is not native-speaker certification.

100k目标token仅约0.312epoch；300k约0.936epoch。长目标下相同token预算带来的完整句子/EOS暴露次数较少，不能把相同token数当作与旧短句训练相同的收敛程度。 / A 100k budget covers about 0.312 epoch; 300k covers about 0.936 epoch. Longer targets yield fewer complete-example/EOS exposures for the same token budget, so equal tokens do not imply equal convergence to the historical short-sentence run.

## 学习率试跑 / Learning-rate pilots


### pilot_lr5e-5

| 目标 token / Target tokens | NLL | chrF++ | 结构失败 / Failure | 非冰岛语 / Wrong language | 评估秒 / Eval s |
|---:|---:|---:|---:|---:|---:|
| 0 | 2.9754 | 12.55 | 34.38% | 0.00% | 321.8 |
| 11,043 | 2.8189 | 12.16 | 46.88% | 12.50% | 411.4 |
| 19,983 | 2.7418 | 14.03 | 40.62% | 0.00% | 358.4 |


### pilot_lr1e-4

| 目标 token / Target tokens | NLL | chrF++ | 结构失败 / Failure | 非冰岛语 / Wrong language | 评估秒 / Eval s |
|---:|---:|---:|---:|---:|---:|
| 0 | 2.9754 | 12.55 | 34.38% | 0.00% | 319.6 |
| 11,043 | 2.7680 | 14.22 | 43.75% | 3.12% | 381.8 |
| 19,983 | 2.6755 | 13.80 | 34.38% | 3.12% | 350.4 |


试跑按预定约束→chrF++→NLL规则选学习率。两组最佳分差很小、单随机种子，无显著性结论；未过约束的试跑也不能叫合格R0。

## 正式开发集曲线 / Formal development curve

| 目标 token / Target tokens | NLL | chrF++ | 结构失败 / Failure | 非冰岛语 / Wrong language | 评估秒 / Eval s |
|---:|---:|---:|---:|---:|---:|
| 0 | 2.9754 | 13.43 | 38.37% | 5.81% | 903.0 |
| 25,522 | 2.6494 | 15.24 | 39.53% | 1.16% | 1004.9 |
| 50,064 | 2.5047 | 17.53 | 27.91% | 1.16% | 822.5 |
| 75,966 | 2.4095 | 17.85 | 32.56% | 1.16% | 876.3 |
| 99,977 | 2.3340 | 24.16 | 15.12% | 0.00% | 631.3 |
| 100,791 | 2.3312 | 23.83 | 20.93% | 0.00% | 703.4 |
| 125,451 | 2.2747 | 21.31 | 25.58% | 1.16% | 750.2 |
| 150,066 | 2.2250 | 23.20 | 20.93% | 1.16% | 688.9 |
| 175,027 | 2.1788 | 25.92 | 16.28% | 0.00% | 630.0 |
| 199,856 | 2.1424 | 25.23 | 17.44% | 2.33% | 611.5 |

![Learning curves: pilot and formal pools are separate](R0_learning_curves_2026-11-11.png)

筛查规则：结构失败率与非冰岛语率均≤10%，然后按chrF++、NLL排序。10%是项目门槛，不是通用翻译能力标准。结构失败包含空输出、复制、截断及重复等自动规则；语言识别可能误判短句或专有名词。全部候选仍需检查否定、实体、数字和遗漏。

The selection rule prefers structurally eligible checkpoints, then higher chrF++ and lower NLL. Eligibility is necessary, not sufficient for semantic quality. Lower NLL alone does not justify readiness for RL.


### 选中检查点的开发集来源分组 / Selected-checkpoint dev source groups

| 开发集来源 / Dataset | 数量 | chrF++ | 结构失败 / Failure |
|---|---:|---:|---:|

| OPUS-tatoeba-v20230412-eng-isl | 32 | 19.85 | 3.12% |

| ParIce | 54 | 26.59 | 24.07% |

## 译文实例 / Translation examples

固定展示选中检查点开发集前4条，再补充最先出现的4条自动失败例并去重。不是挑选最佳译文；这些是已经用于选择的dev，不是盲测。 / Fixed display: first4 selected-checkpoint dev rows, plus first4 automatic failures, deduplicated. These are development examples, not a blind test.

**OPUS-tatoeba-v20230412-eng-isl:42** — gate=True, repetition=False, wrong_language=False

<pre><code>English: You know the phrase, we reap what we sow. I have sown the wind and this is my storm.
Reference: Þið þekkir orðatiltækið: „Við yrkjum það sem við höfum sáð.“ Ég hef sáð vindinum og þetta er stormurinn minn.
Model: Þú veitir að þessi sýnir er að við ræpa þér sem við sýr. Ég sýr þung og þessi er minn.</code></pre>

**ParIce:596349** — gate=True, repetition=False, wrong_language=False

<pre><code>English: That notification shall comprise the documentation and information set out in Annex IV.
Reference: Sú tilkynning skal taka til gagna og upplýsinga sem settar eru fram í IV. viðauka.
Model: Þessi upplýsingar skal innihalda skráningu og upplýsingar sem mælt er fyrir um í IV. viðauka.</code></pre>

**ParIce:407070** — gate=True, repetition=False, wrong_language=False

<pre><code>English: disease sometimes refractory to treatment with pyrimethamine, and therefore an alternative is required.
Reference: meðferð með pýrimetamíni nægir stundum ekki til að ráða niðurlögum sjúkdómsins og því er þörf á öðrum valkosti.
Model: hættur eðlið oft ekki meðferð með pyrimetamína og þar með er nauðsynlegt að taka viðeigandi aðferð.</code></pre>

**OPUS-tatoeba-v20230412-eng-isl:6206** — gate=True, repetition=False, wrong_language=False

<pre><code>English: It&#x27;s nothing to worry about.
Reference: Það er ekkert til að hafa áhyggjur af.
Model: Það er ekki að hafa áhættu við.</code></pre>

**ParIce:509289** — gate=False, repetition=False, wrong_language=False

<pre><code>English: (13) In accordance with the UNFCCC, the Kyoto Protocol and subsequent decisions adopted for their implementation, the Commission and the Member States should support capacity building activities in developing countries and countries with economies in transition in order to help them take full advantage of JI and the CDM in a manner that supports their sustainable development strategies.
Reference: 13) Í samræmi við rammasamning Sameinuðu þjóðanna um loftslagsbreytingar, Kýótóbókunina og síðari ákvarðanir, sem hafa verið samþykktar til framkvæmdar þeim, skulu framkvæmdastjórnin og aðildarríkin styðja aðgerðir til uppbyggingar færni í þróunarlöndum og löndum með umbreytingarhagkerfi í því skyni að aðstoða þau við að nýta sér kerfi sameiginlegrar framkvæmdar og kerfi hreinleikaþróunar til fulls á þann hátt sem hæfir áætlunum þeirra um sjálfbæra þróun.
Model: 13) Í samræmi við aðildarríkiþinginu, viðyrim ákvæði Evrópusambandsins og framkvæmdarákvæðum sem þeirra hefur verið átt við að framkvæma þau skal framkvæmdastjórnin og aðildarríkið stjórnast með því að stjórnast með þeim aðgerðum sem þeirra hefur verið átt við að gera aðgerðir í aðgerðarþingum aðildarríkja og aðgerðir í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í aðgerðarþingum aðildarríkja með aðgerðum í</code></pre>

**ParIce:804526** — gate=False, repetition=True, wrong_language=False

<pre><code>English: A pensioner who is entitled to draw pensions under the legislation of two or more Member States, of which one is that of the Member State in whose territory he resides, and who is entitled to benefits under the legislation of the latter Member State, taking account where appropriate of the provisions of Article 18 and Annex VI, shall, with the members of his family, receive such benefits from the institution of the place of residence and at the expense of that institution as though the person concerned were a pensioner whose pension was payable solely under the legislation of the latter Member State.
Reference: Lífeyrisþegi sem á rétt á lífeyri samkvæmt löggjöf tveggja eða fleiri aðildarríkja, að meðtalinni löggjöf þess aðildarríkis sem hann er búsettur í, þar sem hann á rétt á bótum samkvæmt löggjöf þess ríkis, með tilliti til ákvæða 18. gr. og VI. viðauka eftir því sem við á, skal, ásamt aðstandendum, fá bætur frá stofnun á búsetustaðnum og á kostnað hennar eins og sá sem í hlut á væri lífeyrisþegi sem ætti eingöngu rétt á lífeyri samkvæmt löggjöf þess ríkis.
Model: Aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, og sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarríkjanna sem þeir eru aðildarríki, sem er aðildarríki þeirra aðildarrí</code></pre>

**ParIce:1697793** — gate=False, repetition=False, wrong_language=False

<pre><code>English: • The European Food Safety Authority (‘the Authority) concluded in its opinion of 27 January 2015 (2) that, under the proposed conditions of use, the preparation of carvacrol, cinnamaldehyde and capsicum oleoresin does not have an adverse effect on animal health, human health or the environment, and that it has a potential to improve the feed to gain ratio in chickens for fattening.
Reference: • Matvælaöryggisstofnun Evrópu (hér á eftir nefnd Matvælaöryggisstofnunin) komst að þeirri niðurstöðu í áliti sínu frá 27. janúar 2015 (2) að við tillögð notkunarskilyrði hafi blanda með karvakróli, sinnamaldehýði og óleóresíni úr Capsicum ekki skaðleg áhrif á heilbrigði dýra eða manna eða á umhverfið og að hún geti bætt fóðurstuðul hjá eldiskjúklingum.
Model: • Evrópskið húðvæðisvísindasjúkdóttur („vísindasjúkdótturinn“) samþykkti í þeirri ófyrirtæku ákvæði frá 27. janúar 2015 (2) að, í samræmi við ákvæðum um notkun, ekki hafi áhrif á þjónustu þjóðar, þjónustu þjóðar eða umhverfið á vegna framleiðslu ácarvórls, cinnamáldeýls og capsicum ólersins og að það hafi mögulega áhrif á fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreiningu fræðilega skilgreining</code></pre>

**ParIce:168696** — gate=False, repetition=True, wrong_language=False

<pre><code>English: • Following the suspension of operations of the Zambian flag carrier Zambian Airways in January 2009 and the publication by ICAO of a significant safety concern in February 2009 after the USOAP Audit visit regarding aircraft operations, certification and supervision exercised by the Civil Aviation Authority of Zambia, the Commission requested information from these auth orities in April 2009 to verify the implementation of corrective actions to redress this concern.
Reference: • Í kjölfar tímabundinnar ógildingar á starfrækslu sambíska flugrekandans Zambian Airways, sem tilnefndur er fánaberi (flag carrier) Sambíu, í janúar 2009, og þess að Alþjóðaflugmálastofnunin birti áhyggjur sínar af alvarlegum öryggisvandamálum í febrúar 2009 að lokinni úttektarheimsókn í tengslum við alþjóðlegt eftirlit með öryggismálum, að því er varðar flugrekstur, vottun og eftirlit flugmálayfirvalda í Sambíu, krafðist framkvæmdastjórnin upplýsinga frá þessum yfirvöldum, í apríl 2009, til að sannreyna framkvæmd aðgerða til úrbóta sem eiga að ráða bót á þessum öryggisvandamálum.
Model: • Þar sem Zambíusflugfélagið Zambíusíðar, sem flugfélag Zambíusíðar, varðarðar Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Zambíusíðar, varðaði Z</code></pre>

语义核查仍须关注否定、数字、实体和遗漏；流畅或语言检测通过不等于忠实翻译。 / Fluency and language-ID success do not establish faithful translation.

固定首4条开发译文仍有明显词义、语法与信息保留问题。例如 wind/storm 的意象没有清楚保留，worry 被表达成 risk 一类概念。结构gate与语言识别通过，并不表示句义忠实。

The first four fixed dev outputs still show lexical, grammatical and information-preservation problems. The wind/storm imagery is not clearly retained, and worry is rendered as a risk-related concept. Passing the structural gate and language ID does not establish faithful translation.

No corpus-wide semantic error rate is estimated. This is an AI screen, not a blind evaluation or native-speaker gold adjudication.

## 冻结后的留出诊断 / Frozen held-out diagnostics

| 诊断组 / Group | 数量 | chrF++ | Gate失败 | 截断 | 生成秒 |
|---|---:|---:|---:|---:|---:|

| legacy_sentence_probes | 12 | 29.39 | 1 | 1 | 29.9 |

| wmt_document_transfer | 3 | 14.28 | 2 | 1 | 80.7 |


此处Gate失败仅按最终评估脚本的输出规则计数；dev结构失败另外包含重复检测，readiness的strict筛查还包含语言检测。它们定义不同，均不覆盖全部语义错误。 / Held-out gate failures follow the final evaluator's output rules. Dev structural failures also include repetition; readiness strict validity additionally includes language ID. These definitions differ and do not cover all semantic errors.

这12条旧短句与3篇选取的WMT文档是小型诊断，历史上已经查看过，不是全量WMT或全新盲测集。旧SFT短句chrF++40.07、3篇文档12.82仅供描述；新旧推理后端、精度和短句长度上限不完全一致，不能当作严格匹配或显著性比较。测试后不再据此调整本次模型选择。

The historical probes are small and previously viewed. They are not a full WMT benchmark or a fresh blind test. Historical comparisons are descriptive because inference settings differ.

## RL 前置诊断 / RL readiness


未运行G=8诊断；开发集筛查未过时优先修复SFT质量。 / No G=8 diagnostic was run; address SFT quality before RL if the dev screen fails.


即使运行8prompt×G8，也只是一项小诊断；没有真实MetricX奖励排序验收，不能替代原计划64prompt的完整readiness，也不是DAPO训练结果。

## 时间与计算成本 / Time and compute


流水线累计记录墙钟：**3.60 小时 / hours**。包含恢复和部分控制开销，不等于纯GPU训练时间或CU账单。4小时预算在更新边界检查，长评估可以越过边界。实际CU余额和账单未获得，未购买额外额度。

| 阶段 / Stage | 记录的更新秒 | 已完成评估秒 | 原始日志物理目标token | 恢复重放/重试token |
|---|---:|---:|---:|---:|

| pilot_lr5e-5 | 170.8 | 1091.6 | 28,923 | 8,940 |

| pilot_lr1e-4 | 120.9 | 1051.9 | 19,983 | 0 |

| formal_100k | 1275.2 | 7622.1 | 200,613 | 757 |

从原始流水线起点到最终云端导出的总墙钟为 **3.66 小时**，包括最终诊断和恢复；本地下载、整理文档时间另计。 / Wall time from pipeline start to cloud export: **3.66 hours**, including final diagnostics and recovery; local transfer/report work is separate.

正式阶段已提交状态的纯更新平均吞吐为156.73target token/s；日志中峰值分配显存3.800GB，溢出重试共1次。 / Formal committed update throughput: 156.73target tokens/s; peak recorded allocated VRAM: 3.800GB; recorded overflow retries: 1.


原始日志保留恢复后重复步骤；中断的未落盘工作不一定完整计入。已完成评估秒按保存的指标文件累加，不包含所有中断评估。因此账本区分可核实的更新/评估与未分类墙钟，不把差值伪装为纯计算。一次短预检178.20目标token/s及恢复后235.11token/s不能代替端到端吞吐，也不能构成与旧Windows硬件的公平加速比。

上述墙钟不包含原始流水线起点之前的数据审计、登录、首次环境/模型准备及失败预检。若用于正式论文的完整准备成本比较，必须额外计入这些共同准备成本；本次没有完整CU或能耗账单。 / The recorded wall time excludes data auditing, login, initial environment/model preparation and failed preflights before the original pipeline start. A full study must account for those common preparation costs separately; no complete CU or energy bill was obtained.

实现中的预算边界会带来一次额外验证：首轮停在99,977token，续训到100,791后越过100k阈值，又评估一次。该点保留在完整曲线和耗时账本中，没有删除以美化效率。训练权重、优化器、样本与LR日程连续；本次未在运行中修改冻结训练源码。 / Resuming across the100k boundary triggered an additional evaluation at100,791 tokens after the99,977-token stop. It remains in the curve and cost ledger. The frozen training source, optimizer, data cursor and LR schedule were retained.

Recorded wall time includes recovery. Raw logs preserve replayed updates, while interrupted unlogged work may be missing. Completed-evaluation timings exclude incomplete evaluations. No Colab compute-unit bill was obtained. This SFT run contains no reward-model timing and cannot establish the MetricX fraction of a future RL pipeline.

## 产物、复现与下一步 / Artifacts, reproduction and next decision

- 原工作区：`D:\deep learning project`；旧`runs/sft_round1`完整保留。
- [可运行 Colab notebook](R0_Qwen35_08B_2026-11-11.ipynb)；[冻结源码和数据](R0_colab_bundle_2026-11-11.zip)。
- [选中适配器与完整评估证据](R0_best_adapter_2026-11-11.zip)；[机器可读结果](R0_RESULTS_2026-11-11.json)。
- Drive `MyDrive/deep learning project/r0_2026-11-11`保留完整恢复检查点；本地推理导出不包含AdamW/RNG等状态。
- [完整研究方案](EFFICIENT_ML_RESEARCH_PLAN_2026-11-11.html)；[实现说明](R0_IMPLEMENTATION_2026-11-11.md)。

加载时使用固定原始base加`best_adapter`。不要仅根据adapter_config中Colab临时路径寻找本地base。没有合并或覆盖旧模型。

若自动筛查失败，本次提供的是明确的失败诊断和可恢复候选，不能包装为“已获得可用于DAPO的合理R0”。若筛查通过，仍需目标长度与领域的语义核查，再做完整候选组与MetricX排序诊断。后续efficient-ML实验应冻结共同R0，用同硬件、同数据、同墙钟/目标token预算比较继续SFT、完整DAPO与效率方法；本次SFT实现自身不作为研究创新。

If screening fails, the outcome is a reproducible diagnostic candidate rather than an accepted RL baseline. If it passes, semantic and reward-order review still remain. Future efficiency claims require a common frozen R0 and matched end-to-end compute accounting; the SFT implementation itself is not the proposed novelty.

