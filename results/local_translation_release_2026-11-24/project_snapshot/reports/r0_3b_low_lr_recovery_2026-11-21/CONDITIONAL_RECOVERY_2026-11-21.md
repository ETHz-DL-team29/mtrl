# One conditional lower-LR recovery

Only if P18 stops for no semantic gain at1M: restart from exactly the same expanded original R0. Multiply the entire LR schedule by0.2 (peak1e-5,floor1e-6); keep rank64/alpha128, freshAdamW, data, order, batch, dropout, target objective and seeds fixed. No new fit model, no specialist weights, no third LR regime. This limited control is not a full hyperparameter sweep.

The development-only trigger is motivated by fitP30/32 with held-out P regression and worse NLL after500k, consistent with excessive updates or specialization but not proof of the cause. A lower-LR comparison tests that explanation while seeking a useful checkpoint. It does not establish a model ceiling if both fail. Independent final validation remains mandatory.

Primary sources: [Learning Rate Matters,v2](https://arxiv.org/abs/2602.04998) finds LR tuning materially affects LoRA comparisons in other tasks; [author optimizer guidance](https://tinker-docs.thinkingmachines.ai/tinker/optimizers/) recommends validation-based LR choice and transferring tuned LR across ranks. Neither supplies an Icelandic optimum.
