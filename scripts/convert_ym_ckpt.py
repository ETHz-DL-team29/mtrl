"""Convert a results/ym checkpoint (latest.pt) into a PEFT adapter directory that
scripts/eval_adapter.py --adapter (and train configs' init.from) can load:

    python scripts/convert_ym_ckpt.py /path/to/ckpt/wide_all_ref/latest.pt adapters/ym_wide_all_ref

results/ym saved {"model": get_peft_model_state_dict(...), "optim": ..., "step": ...} for
a LoRA (r=16, alpha=32) on Qwen3_5ForConditionalGeneration, whose language-model modules
are named model.language_model.layers.*; mtrl loads the text-only Qwen3_5ForCausalLM
(model.layers.*). The key prefix is rewritten and the target-module list is read off
the keys, so all / attn / mlp / layer-subset checkpoints all convert.
"""
import argparse
import json
import re
from pathlib import Path

OLD, NEW = "base_model.model.model.language_model.", "base_model.model.model."


def convert_keys(state: dict) -> tuple[dict, list[str]]:
    out, targets = {}, set()
    for k, v in state.items():
        if not k.startswith(OLD):
            raise ValueError(f"unexpected key {k!r}: not a language-model LoRA weight")
        nk = NEW + k[len(OLD):]
        out[nk] = v
        m = re.match(r"base_model\.model\.(.+)\.lora_[AB]\.weight$", nk)
        if not m:
            raise ValueError(f"unexpected key {nk!r}")
        targets.add(m.group(1))
    return out, sorted(targets)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ckpt")
    ap.add_argument("out_dir")
    ap.add_argument("--base-model", default="Qwen/Qwen3.5-0.8B")
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=32)
    args = ap.parse_args()

    import torch
    from peft import LoraConfig
    from safetensors.torch import save_file

    st = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    weights, targets = convert_keys(st["model"])
    rank = next(v.shape[0] for k, v in weights.items() if k.endswith("lora_A.weight"))
    if rank != args.r:
        raise SystemExit(f"checkpoint has LoRA rank {rank}, expected --r {args.r}")
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    LoraConfig(r=args.r, lora_alpha=args.alpha, lora_dropout=0.0, bias="none", target_modules=targets,
               task_type="CAUSAL_LM", base_model_name_or_path=args.base_model).save_pretrained(out)
    save_file({k: v.contiguous() for k, v in weights.items()}, str(out / "adapter_model.safetensors"))
    meta = {"source": str(args.ckpt), "step": st.get("step"), "n_modules": len(targets)}
    (out / "converted_from_ym.json").write_text(json.dumps(meta, indent=1))
    print(f"converted {len(weights)} tensors ({len(targets)} modules, step {st.get('step')}) -> {out}")


if __name__ == "__main__":
    main()
