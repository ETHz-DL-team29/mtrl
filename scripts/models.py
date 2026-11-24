"""Local checkpoint handoff; list/verify require only Python's standard library."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mtrl.checkpoints import registry, verify_model, model_entry, load_translation_model, translate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("list")
    verify = sub.add_parser("verify")
    verify.add_argument("--model", default="all")
    gen = sub.add_parser("generate")
    gen.add_argument("--model", default="qwen25-3b-sft-r0")
    gen.add_argument("--text", required=True)
    gen.add_argument("--device", default="cuda")
    gen.add_argument("--precision", choices=["recorded", "float32", "bfloat16", "float16"], default="recorded")
    gen.add_argument("--base-path")
    gen.add_argument("--offline", action="store_true")
    gen.add_argument("--samples", type=int, default=1)
    gen.add_argument("--temperature", type=float, default=.7)
    gen.add_argument("--max-new-tokens", type=int)
    args = parser.parse_args()
    if args.operation == "list":
        for item in registry(ROOT)["models"]:
            print(json.dumps({k: item[k] for k in ["id", "role", "base_model", "adapter_path"]}, ensure_ascii=False))
    elif args.operation == "verify":
        ids = [m["id"] for m in registry(ROOT)["models"]] if args.model == "all" else [args.model]
        for model_id in ids:
            print(json.dumps(verify_model(model_id, ROOT), ensure_ascii=False))
    else:
        entry = model_entry(args.model, ROOT)
        model, tokenizer, _ = load_translation_model(args.model, root=ROOT, device=args.device,
            precision=args.precision, base_path=args.base_path, offline=args.offline)
        for output in translate(model, tokenizer, args.text, samples=args.samples,
                                temperature=args.temperature,
                                max_new_tokens=args.max_new_tokens or entry["default_max_new_tokens"]):
            print(json.dumps(dict(model=args.model, source=args.text, **output), ensure_ascii=False))


if __name__ == "__main__":
    main()
