# R0-v2 / 0.8B continued-SFT adapter · 2026-11-12

R0-v2 is the strongest tested SFT candidate by matched reference metrics. It is not yet validated as a semantically reliable starting point for full-domain English-to-Icelandic DAPO.

This is a LoRA adapter, not a complete base model. No DAPO updates were run.
Base: Qwen/Qwen3.5-0.8B, pinned revision 2fc06364715b967f1860aea9cf38778875588b17.
Adapter SHA256: 806b9857024868131140da43ad3975d7c8653b97e5687420e4499a3769995847
Selected added target tokens: 750064.
The old SFT and previous R0 are retained at their original paths.

## Local inference example

Use the exact dependencies from source/requirements-colab.txt in the raw export.
Explicitly load the base first; the training adapter_config may contain a historical local path.

```python
import torch
from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration, GenerationConfig
from peft import PeftModel

base = r"D:\deep learning project\models\qwen3.5-0.8b"
adapter = r"D:\deep learning project\runs\r0_v2_colab_2026-11-12\best_adapter"
tokenizer = AutoTokenizer.from_pretrained(base, local_files_only=True)
if tokenizer.pad_token_id is None:
    tokenizer.pad_token = tokenizer.eos_token
device = 'cuda' if torch.cuda.is_available() else 'cpu'
dtype = torch.float16 if device == 'cuda' else torch.float32
model = Qwen3_5ForConditionalGeneration.from_pretrained(
    base, local_files_only=True, dtype=dtype, attn_implementation='sdpa').to(device)
model = PeftModel.from_pretrained(model, adapter).eval()
source = 'The room is hot.'
messages = [{'role': 'user', 'content':
    'Translate the following English text into Icelandic. Return only the Icelandic translation.\n\n' + source}]
text = tokenizer.apply_chat_template(messages, tokenize=False,
    add_generation_prompt=True, enable_thinking=False)
inputs = tokenizer(text, add_special_tokens=False, return_tensors='pt').to(device)
config = GenerationConfig(do_sample=False, num_beams=1, max_new_tokens=256,
    repetition_penalty=1., eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.pad_token_id, use_cache=True)
with torch.inference_mode():
    generated = model.generate(**inputs, generation_config=config)
print(tokenizer.decode(generated[0, inputs.input_ids.shape[1]:], skip_special_tokens=True))
```

CPU inference can be slow. Sampled G8 diagnostics use temperature1, top-p1 and top-k0;
the example above is greedy and is not expected to reproduce sampled candidates.
An adapter-only package cannot reproduce optimizer/RNG resume: use private Drive state.

## Limits

On the same32dev sources with G=8,T=1, the new model has expected random sentence-chrF++28.88, reward-top1=33.28 and reference oracle39.19. Older SFT gives20.21/23.59/28.68; original R0 gives20.68/20.83/26.84. Reference means improve for general/technical sources and all three lengths. Reward-top1 gain over older SFT is+9.69, with stratified paired95%interval[5.18,14.20]; versus original R0 it is+12.45,[7.86,17.58]. Nonconstant-reward groups24→29, all-zero groups8→3; reference-score gain from selection over random is+4.40,[1.60,7.76]. These are substantive relative improvements, not proof of semantic correctness rates.

On the same 32 development sources at G=8, T=1, random-expected sentence chrF++, reward top-1 and reference-oracle means are 28.88/33.28/39.19 for R0-v2, versus 20.21/23.59/28.68 for old SFT and 20.68/20.83/26.84 for previous R0. Reference means improve in both domains and all three length bins. Reward-top-1 gains are +9.69[5.18,14.20] against old SFT and +12.45[7.86,17.58] against previous R0, using stratified paired 95% intervals. Variable-reward groups rise 24→29, all-zero groups fall 8→3, and reward selection gains +4.40[1.60,7.76] over uniform sampling. These establish relative reference-metric gains, not semantic accuracy.

Lexical meaning and word forms remain bottlenecks: none of the eight inspected p04 samples clearly conveys dismissal from employment, and greedy also uses slökkvaður. Greedy p00 is exact, while its eight T=1 samples do not reproduce that correct sentence. An unreliable p24 output still receives about 0.93 reward. Of 64 technical-long candidates,26 contain Han/Cyrillic/Arabic intrusions absent from the source (40.6%), despite high form-filter validity. These proxies do not establish strong comprehensive translation or guarantee DAPO gains. Small signal diagnostics and formal method experiments must remain distinct.

See the full bilingual report and JSON results for domain/length trade-offs and reward failures.
This checkpoint does not establish native-speaker quality, WMT test performance or DAPO gains.
