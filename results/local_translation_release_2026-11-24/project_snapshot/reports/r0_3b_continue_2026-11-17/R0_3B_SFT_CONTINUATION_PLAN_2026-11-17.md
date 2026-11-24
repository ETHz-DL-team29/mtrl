# 3B R0有界SFT续训方案与今晚启动指南 / Bounded 3B R0 SFT Continuation and Tonight’s Launch Guide

日期 / Date: 2026-11-17。状态：代码、数据和notebook已准备，尚未申请本轮GPU，尚未执行新一轮3B训练。 / Prepared locally;no continuation GPU allocation or training has been executed.

**本轮继续训练现有Qwen2.5-3B，不重新初始化LoRA，不更换模型，不运行DAPO。目标是验证多一轮合理SFT能否增加正确翻译候选，而不是保证今晚一定得到合格R0。 / Continue the saved Qwen2.5-3B weights without fresh LoRA,model replacement or DAPO. Test whether another bounded SFT stage improves correct candidate availability;qualification is not guaranteed.**

今晚直接使用 [Colab notebook](../../experiments/r0_3b_continue_2026-11-17/R0_3B_CONTINUE_2026-11-17.ipynb) 和 [配套代码数据包](../../experiments/r0_3b_continue_2026-11-17/continuation_bundle.zip)。两者必须配套。 / Use the matching notebook and bundle linked here.

## 1. 为什么继续SFT / Why continue SFT

首轮开发集加权chrF++为20.07→28.67→32.83→36.48，仍在改善，尚未观察到平台；这支持再做一轮有停止条件的续训。旧0.8B已有多轮SFT，新3B约100万目标token的训练历史并不相等。不能因为暂时不如旧模型就宣称容量上限，也不能由上升曲线推断再训必成功。 / Selection-development scores keep improving without an observed plateau. Historical SFT exposure differs,so the result does not establish a capacity ceiling;continued improvement also does not guarantee qualification.

| 首轮结果 / Round1 measure | 实测 / Observed |
| --- | --- |
| Actual targets / 实际目标token | 999931 |
| Dev64 weighted chrF++ / 开发选模 | 36.476431290709485 |
| Dev64 general chrF++ / 通用选模 | 35.54763100658314 |
| Dev64 technical-long chrF++ / 技术长句选模 | 38.29559574729537 |
| Separate diagnostic128 chrF++ / 另一组诊断 | 34.457398965701834 |
| Old0.8B SFT200 same128 / 旧模型同128 | 36.03694982273706 |
| Technical G8 groups with G / 技术好候选组 | 2/24;old SFT2003/24 |
| Long G8 groups with G / 长句好候选组 | 0/10 in both |

36.48是加权开发选模分数，34.46是另一组128条语料分数，不可混成同一指标。原始首轮报告保留不改；本方案记录后续讨论后选择“先有界续训”的新决定。 / These two scores use different data/aggregation. Preserve the original report as history;this document records the subsequent bounded-continuation decision.

## 2. 精确起点与保留范围 / Exact parent and preservation

| Item | Value |
| --- | --- |
| Base | Qwen/Qwen2.5-3B-Instruct |
| Base revision | aa8e72537993ba99e69dfaafa59ed015b17504d1 |
| Parent adapter | D:\deep learning project\runs\r0_3b_round1_2026-11-17\selected_candidate_adapter |
| Parent SHA256 | 1ecf014712c7eb0004eaa20de58f54b0346cc4bd67b0ce07e3c7e30084e6c41f |
| Parent step / targets | 926 /999931 |
| New local experiment | D:\deep learning project\experiments\r0_3b_continue_2026-11-17 |
| New local result destination | D:\deep learning project\runs\r0_3b_continue_2026-11-17 |
| Drive destination | MyDrive/deep learning project/r0_3b_continue_2026-11-17/ |

这是权重续训、新阶段AdamW重置；不是恢复首轮最后一步的优化器继续执行。首轮adapter、优化器/RNG快照和所有0.8B路径保持原位。本轮新快照保存当前阶段optimizer、RNG、数据cursor、plateau状态和配置哈希。 / Weight continuation uses a fresh stage optimizer,not exact round1 optimizer resume. Preserve all earlier files;new full states include optimizer,RNG,cursor,plateau state and identities.

## 3. 冻结数据与预算选择 / Frozen data and budget

原计划上限约100万新增目标token。实际在原配比及每对累计最多3次约束下，技术中句最多可安排223758 token，因此将名义预算设为90万，实际898707；不提高重复上限硬凑100万。累计完成时该3B链约1898638目标token，但这仍不等于与旧0.8B完全匹配的训练消融。 / The medium bucket supplies223758 targets under the exposure cap. Use a nominal900k stage,actual898707,instead of increasing repetition to force1M. Cumulative 3B targets would be1898638;this is not an exposure-matched cross-model ablation.

| Stratum / 类别 | Target tokens | Share | First-use pairs relative to round1 | First-use target tokens |
| --- | --- | --- | --- | --- |
| general | 359998 | 40.06% | 10211 | 183152 |
| technical_short | 44999 | 5.01% | 0 | 0 |
| technical_medium | 223758 | 24.90% | 0 | 0 |
| technical_long | 269952 | 30.04% | 686 | 127113 |

| Data item | Value |
| --- | --- |
| Eligible pool | 38640 |
| Selected unique pairs | 25381 |
| Example exposures | 26677 |
| Additional target tokens | 898707 |
| Max exposures this stage | 2 |
| Max cumulative exposures | 3 |
| Known semantic exclusions | {'known_semantic_quarantine': 31} |
| Candidate-pool SHA256 | 13393429c1234556cd7b5d6561408964fc39d44b33bffdd670503377ed9761b4 |

这不是全新采集的90万token：优先选未用于首轮的样本，新增首次使用样本主要是10211条通用与686条技术长句；技术短、中本轮没有首次使用的新样本，主要是在已过滤池内补充训练曝光。累计上限只针对这条3B训练链，不包括基础预训练或0.8B历史。 / This is not a newly collected corpus. First-use examples are mainly10211 general and686 technical-long pairs;short/medium are repeats from the protected pool. The cumulative cap covers this3B SFT chain,not pretraining or0.8B history.

继续使用已过滤候选池，排除31个已知语义问题ID，重新核对保留开发/评估源文和参考的标准化精确重叠；按本模型tokenizer编码，总长≤1024、目标≤384、不静默截断。样本检查为AI辅助抽查，不等于母语全量认证或完整文档隔离。 / Retain filtering/quarantine,check exact normalized protected sources/references,and encode with the same tokenizer without truncation. This is not full native or document-level certification.

## 4. 训练配方 / Training recipe

| Parameter | Value |
| --- | --- |
| GPU | L4 recommended;native BF16 required;A100 also possible |
| Precision | Frozen BF16 base + FP32 adapter;final evaluation FP32/TF32off |
| Trainable modules | Existing rank16/alpha32 LoRA:q/k/v/o/gate/up/down |
| Dropout / AdamW weight decay / clip | .05 / .01 /1 |
| Stage peak LR / final LR | 5e-5 /1e-5 |
| Schedule | 2% warmup,cosine to20% of peak |
| Effective batch / microbatch | 32 /4,OOM retry to2/1 |
| Seed | 2026111741 |
| Planned evaluation targets | 0,250000,500000,750000,stage end≈898707 |
| Additional target cap | 900000 |
| Training-loop wall cap | 100min,including in-loop development/backup |
| Overall worker budget | 180min from first code cell;reserve40min before ending updates |

降低峰值学习率是保守的阶段配方选择，不是已证明的最优值。学习率、数据顺序及曝光也变化，因此不能把所有差异单独归因于“多训90万”。本轮不加新adapter、不合并回base、不做量化变更。 / Lower peak LR is a conservative stage choice,not a demonstrated optimum. LR/order/exposure changes prevent attributing every difference solely to more tokens. Preserve the existing adapter structure and base.

## 5. 自动停训与选模 / Automatic stopping and selection

起点在本轮GPU重新生成128条greedy与64条开发输出；起点是已训练父模型，绝不是未经SFT的20.07分模型。每个节点开发加权chrF++的权重仍为.4/.05/.25/.3。 / Recompute parent outputs on the current GPU;the baseline is the trained parent,not the original raw3B.

候选必须满足通用开发chrF++≥本轮父模型重算值−1.5，结构失败数≤父模型+2。连续两个评估节点没有取得至少0.3分的合格加权改善，则提前结束。0.3是项目停训启发式，不是统计显著性；选模仍取合格最高分，0.1以内近似平局取更低技术NLL、再更早节点；父模型fallback始终在候选中。 / Enforce general retention and failure guards. Stop after two checkpoints without an eligible≥0.3 weighted gain. This heuristic is not significance testing;choose the best eligible checkpoint with the registered tie-breaks and parent fallback.

任何数值异常、超时或备份错误都记录为失败/部分完成，不能写成合格R0。达到时间上限可能只完成部分目标token，报告以实际token和最后完整状态为准。 / Record failures/partials honestly;wall limits can reduce completed targets.

## 6. 验收与DAPO关系 / Acceptance and DAPO

结束后，对选中模型生成固定128条greedy和32组G8（每组8个，T=.7,top_p1,top_k0,max320，源句种子与前轮相同）。notebook仅自动输出数值预览，不自动给语义G/P/B/U评级，不自动调用MetricX、不训练DAPO。 / Generate the fixed128 and32 G8 banks. Automatic output is numeric preview only;semantic judgement and reward validation remain separate.

主要判断是关键概念、主客体、否定、数字、时限和完整主张是否保留，以及技术好候选是否从当前2/24明显增加、长句是否摆脱0/10，同时通用不明显退化。原工作目标12/24技术、4/10长句仍可作综合基座的参考目标，不是普遍RL硬门槛。较小改善可以讨论受限pilot，但不能仅凭chrF上涨宣布强R0。 / Judge core semantics,candidate availability and general retention. Earlier12/24 and4/10 targets remain project heuristics,not universal RL thresholds;smaller gains may justify a restricted pilot rather than broad qualification.

若开发进入平台且候选仍无实质改善，停止无上限SFT，再讨论更合适起点。若得到有用actor，另行冻结未用于选择的新质量留出、核对奖励，再跑固定小预算标准DAPO；有效后才开展选择性token更新和前缀复用比较。 / If plateau plus poor candidates persists,stop further automatic SFT and revisit starting-point fit. Validate a new untouched quality holdout and reward before bounded standard DAPO and later efficiency comparisons.

## 7. 今晚逐步启动 / Tonight’s steps

| Step | 操作 / Action | 确认 / Check |
| --- | --- | --- |
| 1 | 在Edge打开https://colab.research.google.com/，文件→上传notebook，选择本实验的R0_3B_CONTINUE_2026-11-17.ipynb。 / Upload the notebook in Edge. | 不要使用首轮ROUND1 notebook；那是fresh LoRA复现。 / Do not launch the old round1 replay. |
| 2 | 运行时→更改运行时类型→L4 GPU，连接。 / Select L4 and connect. | 首个单元必须显示实际L4/native BF16；仅有T4则此配方停止，不跳过检查。 / T4 is blocked. |
| 3 | 运行全部；在Google弹窗完成Drive授权。 / Run all and authorize Drive. | 显示Drive输出路径及写入核对成功。 / Verify the output path. |
| 4 | 文件选择框上传本目录continuation_bundle.zip。 / Upload the companion bundle. | 应显示Frozen code,data and trained parent verified；不需要HF令牌。 / Parent/hash verification passes. |
| 5 | 等待依赖安装、固定revision下载及CPU检查。 / Wait for setup/tests. | 预期8项CPU检查通过；出错就停，不跳过。 / Expect8 checks;do not bypass errors. |
| 6 | 训练单元只运行一次，保持前台任务执行。 / Launch the foreground worker once. | 先生成父模型基线，再看到Drive_checkpoint_verified t000000；此后才开始更新。 |
| 7 | 正常结束会生成quick_results及校验Drive最终ZIP，flush后自动释放本运行时。 / Verified export then flush/release. | 完成不等于合格；返回码0仅表示流程完成。 / No automatic R0 acceptance. |
| 8 | 明天从Drive下载continuation_export.zip和export_info.json，另存D盘，再运行导入工具。 / Download both to D: and import. | 不得覆盖旧round1或0.8B目录。 / Preserve old runs. |

建议至少确认首次t000000和随后首个恢复快照已出现在Drive，再离开。普通Colab不要求MCP连接；浏览器保持打开也不能保证平台永不断线。 / Confirm initial and first periodic backups before leaving. No MCP is required;an open browser does not guarantee runtime continuity.

## 8. 时间与计算单元 / Time and compute estimate

| Stage | L4 estimate |
| --- | --- |
| Authorization/upload/install/download | 15–30min,including user interaction |
| Parent baseline and initial dev | 10–20min |
| SFT updates for898707 targets | About74min at previous203 targets/s |
| In-loop dev/Drive backups | 15–30min,included in100min loop cap |
| Final greedy/G8/export/flush | 15–30min |
| Normal end-to-end target | About2.5–3h;180min worker budget,not a success guarantee |
| Estimated CU | About4.5–6 based on the previous observed round;actual Colab consumption applies |

不需要通宵跑满。正常结束自动调用Google Colab官方runtime.unassign；Drive.flush_and_unmount先刷新待上传文件。授权/网络/Drive异常或未校验归档时可能停在报错处，需手动确认备份后“断开并删除运行时”；180分钟不是平台强制的计费上限。 / Healthy execution ends automatically after verified backup/Drive flush. Failed backup/authorization can require manual shutdown;the worker budget is not a platform-enforced billing cap. [Official runtime API](https://github.com/googlecolab/colabtools/blob/main/google/colab/runtime.py), [official Drive API](https://github.com/googlecolab/colabtools/blob/main/google/colab/drive.py).

## 9. 保存、断线与D盘导入 / Backups,interruptions and D: import

约每5分钟及每个评估点保存adapter、optimizer/RNG、cursor和plateau状态ZIP到Drive，复制后SHA256读回核验；所有阶段均保留。正常最终ZIP包括代码/数据/日志、所有128译文与256个G8候选、选中adapter及最后完整优化器状态；其他阶段由Drive/checkpoints与索引追溯。预留Drive约5–8GB，不自动购买空间。 / Periodic and stage archives contain full states and verified hashes. Final export contains all outputs,selected adapter and last full state;other stages stay in Drive checkpoint archives.

如果运行时断线，不要反复Run all：Drive/TRAINING_STARTED.json会阻止从父模型再次开始。完整状态已保存，但本notebook尚无一键自动恢复入口；应根据最后完整checkpoint恢复，不能仅加载adapter声称精确续跑。 / Do not silently restart after interruption. Full states are saved,but automatic resume is not implemented in this launch notebook.

Colab不能直接写本机D盘。正常流程是Colab→Drive持久化→浏览器“另存为”到本机D盘→导入。浏览器默认Downloads可能在C盘，请明确选择以下文件夹。 / Colab cannot directly write local D:. Use Drive then explicit Save as to D:.

下载两个文件到 / Save both files to: `D:/deep learning project/runs/r0_3b_continue_2026-11-17/night_download/`

然后在PowerShell执行 / Then in PowerShell run: `& "C:/Users/andre/AppData/Local/Programs/Python/Python313/python.exe" "D:/deep learning project/experiments/r0_3b_continue_2026-11-17/import_results.py"`

导入工具仅需Python标准库，核对ZIP及每个文件哈希，拒绝路径穿越和覆盖已有import，输出IMPORTED_RESULTS.md/html及import_verified.json。它不分配GPU，也不替代语义验收。 / The standard-library importer checks hashes,safe paths and no-overwrite;it creates a numeric preview without allocating a GPU or certifying semantics.

## 10. 验证状态与交付 / Verification and deliverables

已完成：本地数据/血缘/预算/损失与梯度/选模/plateau/备份不可覆盖CPU检查，notebook代码单元语法校验。未完成：新配方的真实L4执行、Google授权/Drive实际挂载及新模型质量；今晚首次运行才验证这些。 / Completed local CPU and syntax checks do not constitute an end-to-end GPU or live Drive test.

| File | Purpose |
| --- | --- |
| R0_3B_CONTINUE_2026-11-17.ipynb | User launch notebook |
| continuation_bundle.zip | 115.5 MiB;matching code/data/parent adapter |
| protocol.json / data_summary.json | Frozen parameters and actual exposure data |
| source/source_manifest.json | Every frozen file hash |
| import_results.py | CPU-only safe local import |
| PREPARED_NOT_STARTED.txt | Explicit not-started status |

Bundle SHA256: `49a7bb0f1508504161e7201242fac3bb3e4755441730fb4c6a8dcac3ba90f7d1`。准备过程不会更新首轮结果文件；本方案和notebook放入新的continue目录。 / Preparation preserves round1 results in their original locations.

<details><summary>冻结文件SHA256清单 / Frozen source SHA256 inventory</summary>

| File | SHA256 |
| --- | --- |
| b3_core.py | 7f9e7d40094d0e2f54a1f9d10c01923396fa8003119266acc6e7ea4747c42365 |
| b3_setup_worker.py | c619f14600634816c7cef5693b2bcf9075d6a7c51d0b331973dfde71041c9145 |
| b3_store.py | 95465eee6eb17e2ce58e02b817b9f9321ed4e28a9751dea260e9c4da1d64618d |
| b3_train.py | 6bafa4d35007be0db6055855ed6167b8a19d7444aac3c35ea18d51572747fd12 |
| b3_update.py | c9bb9ddb7f85901839f3a5f42b8534b7112c8e091bbd7c47b301b9ecd7089e8d |
| b3_worker.py | 063ed350739b273e64e7f967b84c26f67a56007567b289f00a0d2756756c6b7b |
| c3_rules.py | 89236a9896b8c26cb730258d25449670d9cfb1a28ef8a14a6bcfa9b057d10828 |
| data/decode_dev.jsonl | 643265919dadeaded9c37b2af74730158961f2f06373a41dd74536f32a5e4c4c |
| data/dev.jsonl | 505627c0de101bbfb86d4f90aaa83be58e4d3f50311e7d951c6676c09dfc97dd |
| data/encoded_train.json | efd634e0ab07bf4b741dd0a7e88d0553468de400b8732aa0153305ad439aa50b |
| data/evaluation128.jsonl | 082b3ca2d0dceaa3d9ffe635f97c9934fa960f06e005fc8ede47dc80d60c18eb |
| data/evaluation_reference_review.json | a3f2b4d05d6380128a63480ff8f7471fb01c8fad2f832f955126946b2a06bf98 |
| data/exclusions.json | 808b55fdd0430dd20225925e349e45c65a3a918dc3b03dfb22d928e6ff123529 |
| data/exposure_order.json | 89b9fcfd537fb58c74953247ab29814f8497f31c6b204885cf9a552756f120b3 |
| data/g8_32.jsonl | 2c14ef4dffa527199422ea446809e23586958d19c588a3a902ff5104d94d3724 |
| data/length_rejections.json | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 |
| data/preparation_summary.json | 2a1cd2a7cb77ffc756b06a4a841d9470b8ff3335f7349c6e8d78494c95d9ef5b |
| data/prior_exposure_counts.json | 9f3b2279409b3c05bf1a25f0c1e4a83379d118bc6e738d077afb775236363bb4 |
| data/quality_followup_lock.json | 122a5840083dac4b69aac259b191b2c58cf010df00b00e3852f54c7df9566dce |
| data/quality_review_lock.json | 5e67fa088a37a4b00a723ff842494c443e3d18d44f1b27df11e52558ef5e8eb6 |
| data/semantic_quarantine_ids.json | 96d16b50de07f92ba2be3aef17ae1c6f6ca3c8398a8a0a7ee3c88a9427ff1281 |
| data/train.jsonl | ca9ca4158d2fcc99c0735012ae0fe47be2890d32801654369ea84151623b0012 |
| data/training_quality_followup_reviews.json | 12b9c9a28ef96cbd91632230207afc37c925c4975571f4d48767fe23d56ecdbe |
| data/training_quality_reviews.json | e88f0d7ad46c2fc0fcad46dfcfb2c44677471c9e6a792ce10daaac2f421e4aee |
| mtgrpo/__init__.py | d841cefd0c317a840959ee520b7313acbb38e620c9844b22221cd6af2bd4b55d |
| mtgrpo/common.py | 5a8a0593f0d177010ee07a8591a6d563fe69d77a7dd71a980a2f53c79b7840f4 |
| mtgrpo/data.py | 6a008a7cc60064e236f9f8151d397471c77308f64e728427ea39f220b92b1302 |
| mtgrpo/models.py | 2e1df0d7a3bc5f1c7067e475256d5fc4473f4dc9595ba5eb530c9cb8824e62fe |
| mtgrpo/r0_core.py | 38399a0793e3f37305d85e0cc84ce94b24254cffeadae1ba75b738b0d97debee |
| mtgrpo/r0_train.py | 368815f1a7a83b4e9924bb33cb542768965d0803c2704a0823e6692804594cf4 |
| mtgrpo/r1_core.py | 1d66ba906f9e508682b1185ccd8185ccd283d4e963eada13e5083f3751026d39 |
| mtgrpo/sft_data.py | c7d40916075abda196a854a300e4d548ebd55dc3b16bfacdb74c1c4c89480329 |
| mtgrpo/telemetry.py | 398c39f80579c68bdba3745a2d3e1f1d2a6d6286f783885c83a2ed8081a6a3a3 |
| protocol.json | 36d341e499a8c24b60ed66b53d03d4e5e5a8912a8e22c674d8195efaa62dab90 |
| requirements-colab.txt | f3f3f47580d7a37d5899fa5b102b86c354c12d5a8b69f082c69eb6d0901c8889 |
| tests/test_b3.py | f24ebf012a6106cb6fa972b0b9cdb4ba2303a80f3a587410df6c7a35c89c21c6 |
| tests/test_continuation.py | 7532e8bb475ec4e5140eed3464b73777f518f00d27c1e665ba2603d3352eeae6 |
| warmstart_adapter/adapter_config.json | a7653e861a5aabe2bac359cb28a6318d2884ab96f4aa4e9470ff1df89cb23b4e |
| warmstart_adapter/adapter_model.safetensors | 1ecf014712c7eb0004eaa20de58f54b0346cc4bd67b0ce07e3c7e30084e6c41f |

</details>
