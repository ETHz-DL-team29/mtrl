# 有条件的单次低学习率恢复 / One conditional lower-LR recovery

Only if P18 stops for no semantic gain at1M: restart from exactly the same expanded original R0. Multiply the entire LR schedule by0.2 (peak1e-5,floor1e-6); keep rank64/alpha128, freshAdamW, data, order, batch, dropout, target objective and seeds fixed. No new fit model, no specialist weights, no third LR regime. This limited control is not a full hyperparameter sweep.

仅在P18的1M无语义改善停止后触发。完全相同的扩容原R0重新开始，整条学习率曲线乘0.2；其余训练因素保留。用既有留出开发集停止/选模；在最终候选权重封存前不查看最终测试质量。若1M仍无开发语义改善即停止，不进行第三轮调参。总截止仍为2026-11-22 04:40 CET，模型运算仍仅Colab，保留所有失败和成功检查点。

The development-only trigger is motivated by fitP30/32 with held-out P regression and worse NLL after500k, consistent with excessive updates or specialization but not proof of the cause. A lower-LR comparison tests that explanation while seeking a useful checkpoint. It does not establish a model ceiling if both fail. Independent final validation remains mandatory.

观察是训练句拟合成功而留出表现退化；这可能是更新过强或过度专门化，尚不能断言原因。该对照只检查其中一个可操作解释，不承诺低LR有效，也不以两点对照宣称充分调优。

Primary sources: [Learning Rate Matters,v2](https://arxiv.org/abs/2602.04998) finds LR tuning materially affects LoRA comparisons in other tasks; [author optimizer guidance](https://tinker-docs.thinkingmachines.ai/tinker/optimizers/) recommends validation-based LR choice and transferring tuned LR across ranks. Neither supplies an Icelandic optimum.
