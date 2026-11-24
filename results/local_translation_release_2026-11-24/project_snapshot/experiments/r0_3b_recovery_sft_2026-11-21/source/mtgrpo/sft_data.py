"""Prepare a new 2,000/200 SFT split without overwriting earlier experiments."""
from __future__ import annotations
import argparse
import random
from .common import ROOT, read_jsonl, sha256, source_key, write_json, write_jsonl
from .data import TRAIN_ID, TRAIN_URL, read_training_zip, english_icelandic_test_rows

INSTRUCTION = "Translate the following English text into Icelandic. Return only the Icelandic translation."


def encode_example(tokenizer, row, max_length):
    from .models import make_prompt
    text = tokenizer.apply_chat_template(make_prompt(row), tokenize=False, add_generation_prompt=True, enable_thinking=False)
    prompt = tokenizer(text, add_special_tokens=False)["input_ids"]
    target = tokenizer(row["reference"].strip(), add_special_tokens=False)["input_ids"]
    if not target:
        raise ValueError("Empty SFT target.")
    if target[-1] != tokenizer.eos_token_id:
        target.append(tokenizer.eos_token_id)
    if len(prompt) + len(target) > max_length:
        raise ValueError("SFT example exceeds max length; target is not silently truncated.")
    return {"id": row["id"], "prompt": prompt, "target": target, "tokens": len(prompt) + len(target)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-size", type=int, default=2000)
    parser.add_argument("--dev-size", type=int, default=200)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(ROOT/"models/qwen3.5-0.8b", local_files_only=True)
    archive = ROOT/"data/raw/train/Tatoeba-v2023-04-12-en-is.zip"
    excluded = {source_key(row["source"]) for row in english_icelandic_test_rows(
        read_jsonl(ROOT/"data/raw/wmt26/wmt26-genmt.jsonl"), max_chars=0, allow_multimodal=True)}
    old_dev = read_jsonl(ROOT/"data/processed/dev.jsonl")
    old_dev_keys = {source_key(row["source"]) for row in old_dev}
    pool = []
    seen = set()
    removed_length = 0
    for index, (source, reference) in enumerate(read_training_zip(archive)):
        key = source_key(source)
        if not source or not reference or key in excluded or key in seen:
            continue
        row = {"id": f"{TRAIN_ID}:{index}", "source": source, "reference": reference,
               "src_lang": "en", "tgt_lang": "is", "instruction": INSTRUCTION,
               "dataset": TRAIN_ID, "wmt26_recipe": "wmt26-eng-isl", "source_url": TRAIN_URL}
        try:
            encode_example(tokenizer, row, args.max_length)
        except ValueError:
            removed_length += 1
            continue
        seen.add(key)
        pool.append(row)
    preserved = [row for row in pool if source_key(row["source"]) in old_dev_keys]
    if len(preserved) != len(old_dev_keys):
        raise ValueError("Some legacy dev samples failed filtering. Choose a length that preserves the existing dev set.")
    if args.dev_size < len(preserved):
        raise ValueError("Requested dev size is smaller than preserved legacy dev set.")
    remainder = [row for row in pool if source_key(row["source"]) not in old_dev_keys]
    random.Random(args.seed).shuffle(remainder)
    extra = args.dev_size - len(preserved)
    dev = preserved + remainder[:extra]
    train = remainder[extra:extra+args.train_size]
    if len(train) != args.train_size:
        raise ValueError("Insufficient data for this split.")
    # Keep the old dev samples first so the same 50 can be decoded throughout.
    old_order = {source_key(row["source"]): index for index, row in enumerate(old_dev)}
    dev[:len(preserved)] = sorted(preserved, key=lambda row: old_order[source_key(row["source"])])
    for row in train:
        row.update(split="train", usage="training")
    for row in dev:
        row.update(split="dev", usage="development_only")
    directory = ROOT/"data/sft_round1"
    if (directory/"manifest.json").exists():
        raise ValueError("SFT split already exists. Preserve it for reproducibility instead of overwriting.")
    write_jsonl(directory/"train.jsonl", train)
    write_jsonl(directory/"dev.jsonl", dev)
    write_jsonl(directory/"debug_train.jsonl", train[:32])
    write_jsonl(directory/"debug_dev.jsonl", dev[:16])
    write_jsonl(directory/"decode_dev.jsonl", dev[:50])
    write_json(directory/"manifest.json", {
        "dataset_id": TRAIN_ID, "recipe": "wmt26-eng-isl", "archive_sha256": sha256(archive),
        "train_size": len(train), "dev_size": len(dev), "legacy_dev_preserved": len(preserved),
        "max_total_tokens": args.max_length, "excluded_for_length": removed_length,
        "eligible_unique_sources": len(pool), "seed": args.seed,
        "train_sha256": sha256(directory/"train.jsonl"), "dev_sha256": sha256(directory/"dev.jsonl"),
        "instruction": INSTRUCTION, "split_policy": "source-disjoint, full WMT26 en-is test excluded; legacy dev preserved",
    })
    print(f"Prepared {len(train)} SFT train, {len(dev)} dev; preserved {len(preserved)} previous dev samples.", flush=True)


if __name__ == "__main__":
    main()
