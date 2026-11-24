# R0-TechSFT-v1 — inference / 推理入口

原R0完整保留：D:/deep learning project/runs/r0_v3_colab_2026-11-13/nll_adapter。
Original R0 remains unchanged.

固定开发选择得到：t200000,step165,targettokens200770。
Selected candidate: selected_candidate_adapter。训练末期：final_trained_adapter。若选中step0，此目录就是原R0权重，不能把它称作新的训练收益。
If selection is step0,the selected adapter is original R0. The trained-final checkpoint remains separate.

Base: Qwen/Qwen3.5-0.8B revision2fc06364715b967f1860aea9cf38778875588b17。
显式载入base后再PeftModel.from_pretrained(base,adapter_path,is_trainable=False)，不要让adapter_config中的旧/content路径决定base位置。
Load the base explicitly,then attach the chosen adapter. Do not rely on a saved remote /content path as a local base location.

匹配本报告FP32：先按原BF16路径载入base，再载入FP32 LoRA，最后model.float().eval()，TF32关闭；不要重新换另一份原始高精度base权重来冒充同一配置。
For the recorded FP32 path,promote the originally loaded BF16-rounded base+FP32 LoRA with model.float().eval(),TF32 disabled.

完整代码与固定数据在实验source bundle；Colab notebook是复现入口，重新运行将产生额外训练和CU，不是阅读报告所需。
The source bundle and notebook reproduce the run;re-running them consumes additional GPU time.
