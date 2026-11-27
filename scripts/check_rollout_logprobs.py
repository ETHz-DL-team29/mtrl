"""Diagnostic: do the training forward's token log-probs match the sampler's?

    python scripts/check_rollout_logprobs.py configs/train/quick_rl.yaml [--prompts 2]

Samples G completions for `--prompts` training sources with the base policy, keeps the
raw logits that generate() saw (before temperature), and compares log_softmax of those
with mtrl.train.rl.token_logprobs on the same sequences. With one prompt there is no
left padding; with several, prompts of different length are left-padded, which shows
whether the loss forward needs explicit position ids. Prints max / mean |difference|
over valid tokens; values at numerical noise (~1e-2 in bf16) mean the PPO ratio starts
at 1 as it should.
"""
import argparse

from mtrl.common.train_config import load_train_config


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--env")
    ap.add_argument("--prompts", type=int, default=1)
    args = ap.parse_args()
    run = load_train_config(args.config, args.env)
    from mtrl.common.env_setup import setup_env

    setup_env(run.env)
    import torch

    from mtrl.generation.hf_generate import chat_prompts, completion_mask, eos_ids
    from mtrl.train.common import load_split
    from mtrl.train.policy import load_base
    from mtrl.train.rl import token_logprobs

    t = run.train
    tok, model = load_base(t.model["name"], run.env.dtype, run.env.attn_impl)
    segs = load_split(run, t.data["train_split"], 50)
    segs = sorted(segs, key=lambda s: len(s.src))[:: max(1, len(segs) // args.prompts)][:args.prompts]
    G = t.algorithm["group"]
    torch.manual_seed(0)
    enc = tok(chat_prompts(tok, segs, [run.lang(s.direction) for s in segs], t.prompt_template, t.thinking),
              return_tensors="pt", padding=True).to(model.device)
    P = enc.input_ids.shape[1]
    with torch.no_grad():
        out = model.generate(**enc, do_sample=True, temperature=t.rollout["temperature"], top_p=1.0, top_k=0,
                             max_new_tokens=64, num_return_sequences=G, output_logits=True,
                             return_dict_in_generate=True, pad_token_id=tok.pad_token_id)
        toks = out.sequences[:, P:]
        valid, _ = completion_mask(toks, eos_ids(tok, model))
        gen_lp = torch.stack([torch.log_softmax(x.float(), -1) for x in out.logits], 1)
        gen_lp = gen_lp.gather(2, toks[..., None]).squeeze(-1)
        att = torch.cat([enc.attention_mask.repeat_interleave(G, 0), valid.long()], 1)
        fwd = torch.cat([token_logprobs(model, out.sequences[i:i + 2], att[i:i + 2], toks[i:i + 2],
                                        want_entropy=False)[0] for i in range(0, toks.shape[0], 2)])
    d = (gen_lp - fwd).abs()[valid]
    print(f"prompts={args.prompts} rollouts={toks.shape[0]} valid_tokens={int(valid.sum())} "
          f"prompt_pad_tokens={int((enc.attention_mask == 0).sum())}")
    print(f"|logp_generate - logp_forward|: max {d.max():.4f}  mean {d.mean():.5f}  "
          f"share > 0.1: {(d > 0.1).float().mean():.4f}")


if __name__ == "__main__":
    main()
