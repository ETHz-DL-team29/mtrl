# R0-v3: minimum-NLL candidate / 末期候选适配器

Date:2026-11-13. Policy scale remains Qwen3.5-0.8B. This is a LoRA adapter, not merged base weights. Read the results report for measured adequacy and DAPO-readiness limits.

Required base: `Qwen/Qwen3.5-0.8B`, revision `2fc06364715b967f1860aea9cf38778875588b17`. Training used transformers5.22.1, peft0.21.2. Supply the base explicitly; the saved PEFT config retains a historical local base path for provenance.

```python
import torch
from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration, GenerationConfig
from peft import PeftModel

base_id = "Qwen/Qwen3.5-0.8B"
revision = "2fc06364715b967f1860aea9cf38778875588b17"
adapter_dir = r"D:/deep learning project/runs/r0_v3_colab_2026-11-13/nll_adapter"
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if device == "cuda" and torch.cuda.get_device_capability()[0] >= 8 else torch.float16 if device == "cuda" else torch.float32
tokenizer = AutoTokenizer.from_pretrained(base_id, revision=revision)
tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
model = Qwen3_5ForConditionalGeneration.from_pretrained(base_id, revision=revision, dtype=dtype, attn_implementation="sdpa").to(device)
model = PeftModel.from_pretrained(model, adapter_dir).eval()
source = "Put the book on the table."
# Exact row-level instruction used by all frozen train/dev/readiness records.
# It overrides the longer generic fallback in mtgrpo.models.make_prompt.
instruction = "Translate the following English text into Icelandic. Return only the Icelandic translation."
messages = [{"role":"user", "content":instruction + "\n\n" + source}]
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
inputs = tokenizer(prompt, add_special_tokens=False, return_tensors="pt").to(device)
config = GenerationConfig(do_sample=False, num_beams=1, max_new_tokens=320, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id, use_cache=True)
with torch.inference_mode():
    output = model.generate(**inputs, generation_config=config)
print(tokenizer.decode(output[0, inputs.input_ids.shape[1]:], skip_special_tokens=True))
```

The matched diagnostic uses T1/G8/top_p1/top_k0 and256 tokens; ordinary greedy use above is a different decoding protocol. Large documents are outside this run's demonstrated scope. Formal DAPO comparisons must freeze the same starting checkpoint, reward and budgets.

复现训练：使用同目录附带的Colab notebook及冻结源包；实际显式传入 `--microbatch 8`，覆盖源包初始默认4。源包默认值、资源预检、实际正式执行配置均保留，不能把丢弃的预检更新计入最终模型曝光。报告含完整源文、参考、贪心及G8候选，便于检查语义而不只看分数。

Checkpoint selection: lowest completed development NLL, expanded after an adaptive16-case diagnostic. This file does not certify DAPO readiness. Read the final results decision; the original greedy-selected adapter remains separately preserved.

## Auxiliary G8 sampling / 辅助采样

The primary comparison used T1; the additional calibration used T0.7. This example uses T0.7/G8. For exact reported-prompt reproduction, use the frozen `compare_helpers.prompt_seed(row["id"],20261112)` rule rather than the constant demonstration seed below.

```python
torch.manual_seed(20261112)
sampling = GenerationConfig(do_sample=True, temperature=0.7, top_p=1.0, top_k=0,
    num_beams=1, repetition_penalty=1.0, num_return_sequences=8,
    max_new_tokens=256, eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.pad_token_id, use_cache=True)
with torch.inference_mode():
    bank = model.generate(**inputs, generation_config=sampling)
for sequence in bank:
    print(tokenizer.decode(sequence[inputs.input_ids.shape[1]:], skip_special_tokens=True))
```
