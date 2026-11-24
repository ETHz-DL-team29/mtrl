# R0-v3: saved text LoRA

Date:2026-11-13. Policy scale remains Qwen3.5-0.8B. This is a LoRA adapter, not merged base weights. Read the results report for measured adequacy and DAPO-readiness limits.

Required base: `Qwen/Qwen3.5-0.8B`, revision `2fc06364715b967f1860aea9cf38778875588b17`. Training used transformers5.22.1, peft0.21.2. Supply the base explicitly; the saved PEFT config retains a historical local base path for provenance.

```python
import torch
from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration, GenerationConfig
from peft import PeftModel

base_id = "Qwen/Qwen3.5-0.8B"
revision = "2fc06364715b967f1860aea9cf38778875588b17"
adapter_dir = r"D:/deep learning project/runs/r0_v3_colab_2026-11-13/best_adapter"
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

Checkpoint selection: lowest completed development NLL, expanded after an adaptive16-case diagnostic. This file does not certify DAPO readiness. Read the final results decision; the original greedy-selected adapter remains separately preserved.
