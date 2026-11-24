# Saved3B R0 candidate

Base: D:/deep learning project/models/qwen2.5-3b-instruct
Revision: aa8e72537993ba99e69dfaafa59ed015b17504d1
Selected adapter: final_selected_adapter/
Read verdict.json and the full report before claiming DAPO readiness.
See the verdict and complete report for promotion/DAPO eligibility. Successful persistence does not certify semantic or reward readiness.

Explicitly load the pinned base with AutoModelForCausalLM,then PeftModel.from_pretrained(base,adapter_path). Ignore stale /content base paths in the adapter configuration.
Explicitly load the base then attach the adapter; do not rely on the configuration's /content path.

Matched evaluation: BF16 base checkpoint loaded then full model.float(),FP32 adapter,TF32off,SDPA,greedy max320,prompt limit1024 with no silent source truncation,enable_thinking=False.
Matched evaluation: full-model FP32, TF32 disabled, greedy up to320tokens. Different precision/hardware can change outputs.

Selected and last-trained adapters may differ. Exact resume requires the matching full snapshot,optimizer/RNG/cursor,data order,protocol and source identities. Do not use the last optimizer with an earlier selected adapter. Cross-stage SFT uses fresh AdamW and is not exact optimizer resume.
Best and final weights can differ. Exact resumption requires the matching complete snapshot; do not combine different checkpoints. New stages use a fresh AdamW optimizer.

Old0.8B and original3B checkpoints were preserved. Budget records are historical fixed absolute timestamps;future runs require a separately authorized new directory and budget,not editing these frozen records.
Older models are preserved. Absolute budget deadlines are historical; new training requires a new directory and budget without rewriting frozen evidence.

Run `python inference.py --text "This is a test."` with the recorded Torch/Transformers/PEFT environment. Default CUDA requires sufficient VRAM; `--device cpu` is slower. This helper does not allocate Colab or train.
