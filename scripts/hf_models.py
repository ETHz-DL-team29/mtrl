"""Prepare/upload the three authorized model adapters; never pushes the GitHub repo."""
from pathlib import Path
import argparse
import contextlib
import io
import json
import os
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from mtrl.checkpoints import registry, model_entry, verify_model, sha256, inside

NAMES = {
    "qwen35-08b-sft-r0": "mtrl-qwen35-08b-en-is-sft-r0",
    "qwen25-3b-sft-r0": "mtrl-qwen25-3b-en-is-sft-r0",
    "qwen25-3b-dapo-shortmid": "mtrl-qwen25-3b-en-is-dapo-shortmid-v1",
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def prepare(namespace):
    if not namespace or "/" in namespace or any(c.isspace() for c in namespace):
        raise ValueError("Expected one Hugging Face user/organization name")
    plans = []
    for model_id, suffix in NAMES.items():
        entry = model_entry(model_id, ROOT)
        verify_model(model_id, ROOT)
        original = inside(ROOT, entry["adapter_path"])
        dest = ROOT / "artifacts/hf_upload_payloads" / model_id
        dest.mkdir(parents=True, exist_ok=True)
        repo_id = namespace + "/" + suffix
        for name in ["adapter_model.safetensors", "adapter_config.json"]:
            target = dest / ("original_adapter_config.json" if name == "adapter_config.json" else name)
            if not target.exists() or sha256(target) != entry["files"][name]["sha256"]:
                shutil.copy2(original / name, target)
        config = json.loads((original / "adapter_config.json").read_text())
        config["base_model_name_or_path"] = entry["base_model"]
        config["revision"] = entry["base_revision"]
        dump(dest / "adapter_config.json", config)
        evaluation = {"task": "English to Icelandic", "stage": entry["stage"], "research_candidate": True}
        if model_id == "qwen25-3b-sft-r0":
            evaluation.update(dataset="WMT26 official198documents, source segmentation/document reconstruction", chrfpp=39.718915382450255, bleu=19.757162284647453)
        elif model_id == "qwen25-3b-dapo-shortmid":
            source = ROOT / "results/latest.json"
            evaluation.update(dataset="WMT26 official198documents, source segmentation/document reconstruction",
                              chrfpp=40.83466908840522, bleu=21.69729738999143,
                              matched_comparison=json.loads(source.read_text())["primary_latest"],
                              full_primary_gain_rule_passed=False, shortmedium_secondary_positive_but_exploratory=True,
                              optimizer_updates=240, dev_selected_step=120, new_SFT_updates=0)
        else:
            evaluation.update(dataset="Historical ParIce project holdout; not the matched WMT26 benchmark", matched_WMT26_score_available=False)
        dump(dest / "eval_results.json", evaluation)
        example = f'''# Explicit base loading avoids architecture ambiguity and historical local paths.
import torch
from transformers import AutoTokenizer, {"Qwen3_5ForConditionalGeneration" if entry["architecture"]=="qwen3_5" else "AutoModelForCausalLM"}
from peft import PeftModel
BASE="{entry['base_model']}"
BASE_REVISION="{entry['base_revision']}"
ADAPTER="{repo_id}"
tokenizer=AutoTokenizer.from_pretrained(BASE,revision=BASE_REVISION)
base={"Qwen3_5ForConditionalGeneration" if entry["architecture"]=="qwen3_5" else "AutoModelForCausalLM"}.from_pretrained(BASE,revision=BASE_REVISION,dtype=torch.{"bfloat16" if entry['architecture']=="qwen3_5" else "float32"},attn_implementation="sdpa")
model=PeftModel.from_pretrained(base,ADAPTER,revision="v1",is_trainable=False).float().to("cuda").eval()
# For new training use is_trainable=True. This does not restore an optimizer.
# Private repos require YOUR authorized Hugging Face login; never share write tokens.
'''
        (dest / "load_example.py").write_text(example, encoding="utf-8")
        header = f'''---
language:
- en
- is
library_name: peft
base_model: {entry['base_model']}
base_model_relation: adapter
tags:
- lora
- translation
- mtrl
- {entry['stage']}
---

# {suffix}

English→Icelandic research LoRA adapter

This repository contains a LoRA delta, not standalone base weights. It can be loaded for inference or further adapter training. The required base is **{entry['base_model']}**, pinned to **{entry['base_revision']}**. Base-license metadata: **{entry['base_license']}**; see BASE_MODEL_LICENSE.md. No additional commercial permission or new project-wide license is asserted by this model card.

This repository contains adapters only. Base-model, training-data and project terms remain applicable. It is not a certified production translation system and does not guarantee other-language/task capability.

## Load

See `load_example.py`. Authenticate with your own authorized Hugging Face account for private-repo access. The example reproduces the recorded-style FP32 path and needs enough GPU memory. Ordinary reduced-precision inference may use less memory but is not score-identical. No hosted inference service or paid endpoint was deployed.

To continue training, set `is_trainable=True` when attaching this adapter to the same pinned base, then create your own optimizer. This is not an exact optimizer/RNG resume.

## Evaluation

'''
        if model_id == "qwen25-3b-dapo-shortmid":
            header += '''Latest P25 arm:240actual updates, dev-selected step120. On all198WMT26documents, chrF++40.8347 and BLEU21.6973 versus original SFT39.7189/19.7572. Paired95%intervals for differences still include zero; the predeclared full-test reliable-gain rule is not met. The153-document short/medium secondary subset is positive but exploratory, while the55all-short subset shows no reliable gain. This candidate is not relabeled a stronger SFT R0.\n\n'''
        elif model_id == "qwen25-3b-sft-r0":
            header += '''P18 SFT R0, preserved as the shared starting point for the latest DAPO comparison. On all198WMT26documents, chrF++39.7189 and BLEU19.7572, using source segmentation, text-only translation and document reconstruction with unchanged official refA. These are our system scores, not an official human competition ranking.\n\n'''
        else:
            header += '''Preserved0.8B R0-v3 minimum-development-NLL adapter. Historical results are ParIce project holdouts and use different evaluation/selection settings. No matched WMT26 score is claimed for this adapter in the latest3B comparison. It is not the collaborator's multilingual isl/lij/lld model.\n\n'''
        header += f'''Full results/code are in the local mtrl project delivery. GitHub code publication is pending owner review; no GitHub push was performed during this model upload. See https://github.com/ETHz-DL-team29/mtrl for the project root, but do not assume the new local files are already published there.

## Provenance

- Local registry ID: `{model_id}`
- Adapter weight SHA256: `{entry['files']['adapter_model.safetensors']['sha256']}`
- Source experiment: `{entry['source_experiment']}`
- LoRA r={entry['lora_rank']}, alpha={entry['lora_alpha']}
- Weights were copied without retraining, merging or quantization.
- Published adapter_config uses a portable base ID/revision; original config is retained separately for exact local-package reconstruction.
'''
        (dest / "README.md").write_text(header, encoding="utf-8")
        (dest / "BASE_MODEL_LICENSE.md").write_text(f"# Base-model license notice\n\nBase: {entry['base_model']}\n\nUpstream license label: **{entry['base_license']}**.\n\nOfficial pinned model card: https://huggingface.co/{entry['base_model']}/blob/{entry['base_revision']}/README.md\n\nThis adapter card does not replace upstream terms or grant additional rights. Source-data terms and project permissions also remain applicable.\n", encoding="utf-8")
        shutil.copy2(ROOT / "setup/requirements-checkpoint-use.txt", dest / "requirements.txt")
        files = {p.name: dict(bytes=p.stat().st_size, sha256=sha256(p)) for p in dest.iterdir() if p.is_file() and p.name != "model_manifest.json"}
        manifest = dict(schema_version=1, registry_id=model_id, repo_id=repo_id, private=True,
                        base_model=entry["base_model"], base_revision=entry["base_revision"],
                        source_weight_sha256=entry["files"]["adapter_model.safetensors"]["sha256"],
                        normalized_adapter_config_only=True, original_weights_unchanged=True, files=files)
        dump(dest / "model_manifest.json", manifest)
        plans.append(dict(model_id=model_id, repo_id=repo_id, folder=str(dest), manifest=manifest))
    dump(ROOT / "models/hf_upload_plan.json", {"date": "2026-11-24", "private": True, "github_push": False, "models": plans})
    return plans


class CappedReader(io.BufferedReader):
    def __init__(self, path, rate):
        super().__init__(io.FileIO(path, "rb"), buffer_size=1024**2)
        self.rate = rate
        self.sent = 0
        self.started = time.monotonic()

    def read(self, size=-1):
        value = super().read(size)
        self.sent += len(value)
        delay = self.sent / self.rate - (time.monotonic() - self.started)
        while delay > 0:
            time.sleep(min(1., delay))
            delay = self.sent / self.rate - (time.monotonic() - self.started)
        return value


def upload(namespace, rate_mib):
    from huggingface_hub import HfApi, CommitOperationAdd, hf_hub_download
    api = HfApi()
    account = api.whoami()
    if namespace != account["name"] and namespace not in [o["name"] for o in account.get("orgs", [])]:
        raise ValueError("Namespace is not this authenticated user or a listed organization")
    plans = prepare(namespace)
    results = []
    for plan in plans:
        rid = plan["repo_id"]
        try:
            api.create_repo(rid, repo_type="model", private=True, exist_ok=False)
        except Exception as exc:
            if getattr(getattr(exc, "response", None), "status_code", None) != 409:
                raise
            existing = api.model_info(rid, files_metadata=True)
            if not existing.private:
                raise RuntimeError("Refusing to overwrite an existing public repository")
            manifest_path = hf_hub_download(rid, "model_manifest.json")
            if json.loads(Path(manifest_path).read_text())["source_weight_sha256"] != plan["manifest"]["source_weight_sha256"]:
                raise RuntimeError("Existing private repository does not match this delivery")
        print(json.dumps(dict(phase="uploading", repo_id=rid, rate_MiB_per_second=rate_mib)), flush=True)
        with contextlib.ExitStack() as stack:
            operations = []
            for path in sorted(Path(plan["folder"]).iterdir()):
                if not path.is_file():
                    continue
                op = CommitOperationAdd(path_in_repo=path.name, path_or_fileobj=str(path))
                # Hash the local file normally, then cap only HTTP streaming. A binary
                # file object uses the official HTTP/LFS path instead of parallel Xet.
                if path.suffix == ".safetensors":
                    assert op.upload_info.sha256.hex() == plan["manifest"]["source_weight_sha256"]
                    op.path_or_fileobj = stack.enter_context(CappedReader(path, rate_mib * 1024**2))
                operations.append(op)
            commit = api.create_commit(rid, repo_type="model", operations=operations,
                                       commit_message="Publish verified research adapter and evaluation card", num_threads=1)
        info = api.model_info(rid, revision=commit.oid, files_metadata=True)
        assert info.private
        weight = next(s for s in info.siblings if s.rfilename == "adapter_model.safetensors")
        remote_sha = getattr(weight.lfs, "sha256", None) if not isinstance(weight.lfs, dict) else weight.lfs.get("sha256")
        assert remote_sha == plan["manifest"]["source_weight_sha256"]
        for filename in ["adapter_config.json", "original_adapter_config.json"]:
            local = hf_hub_download(rid, filename, revision=commit.oid)
            assert sha256(Path(local)) == plan["manifest"]["files"][filename]["sha256"]
        api.create_tag(rid, tag="v1", revision=commit.oid, repo_type="model", exist_ok=True)
        result = dict(id=plan["model_id"], repo_id=rid, url="https://huggingface.co/" + rid,
                      revision=commit.oid, tag="v1", private=True, remote_weight_SHA256=remote_sha,
                      verified=True, hub_files=plan["manifest"]["files"])
        results.append(result)
        dump(ROOT / "models/hf_publication.json", dict(date="2026-11-24", github_pushed=False, models=results))
        print(json.dumps(dict(phase="verified", **{k: result[k] for k in ["repo_id", "revision", "private", "verified"]})), flush=True)
    data = registry(ROOT)
    for result in results:
        entry = next(m for m in data["models"] if m["id"] == result["id"])
        entry.update(hub_repo_id=result["repo_id"], hub_revision=result["revision"], hub_tag="v1",
                     hub_private=True, uploaded=True,
                     hub_file_map={"adapter_model.safetensors": "adapter_model.safetensors", "adapter_config.json": "original_adapter_config.json"})
    data["local_only"] = False
    data["github_code_pushed"] = False
    dump(ROOT / "models/registry.json", data)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["prepare", "upload", "status"])
    parser.add_argument("--namespace")
    parser.add_argument("--rate-mib", type=float, default=2.)
    args = parser.parse_args()
    if args.operation == "status":
        from huggingface_hub import HfApi
        info = HfApi().whoami()
        print(json.dumps(dict(username=info["name"], organizations=[o["name"] for o in info.get("orgs", [])])))
    else:
        if not args.namespace or args.rate_mib <= 0:
            parser.error("A namespace and positive transfer limit are required")
        results = prepare(args.namespace) if args.operation == "prepare" else upload(args.namespace, args.rate_mib)
        print(json.dumps(dict(completed=args.operation, models=len(results), github_pushed=False)))


if __name__ == "__main__":
    main()
