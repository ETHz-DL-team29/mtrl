"""DAPO mathematics, independent of model/download infrastructure."""
import torch

def group_advantages(rewards, epsilon=1e-6):
    r=torch.as_tensor(rewards,dtype=torch.float32)
    if not torch.isfinite(r).all():raise FloatingPointError('Non-finite rewards')
    std=r.std(unbiased=False)
    return ((r-r.mean())/std if std>epsilon else torch.zeros_like(r)),float(std)

def soft_length_penalty(length,maximum=320,buffer=64):
    if not(0<buffer<=maximum):raise ValueError('Invalid length buffer')
    return -min(1.,max(0.,(length-(maximum-buffer))/buffer))

def clipped_terms(new,old,advantage,low=.2,high=.28):
    if new.shape!=old.shape:raise ValueError('Token alignment mismatch')
    ratio=torch.exp(new-old)
    raw=ratio*advantage
    clipped=ratio.clamp(1-low,1+high)*advantage
    loss=-torch.minimum(raw,clipped)
    active=(raw>clipped).float()
    return loss,dict(ratio=ratio.detach(),clip_active=active.detach())

def log_probabilities(policy,prompt,completion,temperature=.7,entropy=False):
    """Full categorical sampling distribution: T=.7, top-p=1, top-k=0.

    Every completion includes its sampled EOS, if present. Prompt and padding
    never enter the loss. Both old and new probabilities use this same T.
    """
    import torch.nn.functional as F
    if temperature<=0:raise ValueError('Temperature must be positive')
    policy.model.train(torch.is_grad_enabled())
    completion=completion.to(policy.device);n=len(completion)
    if n==0:raise ValueError('Empty completion')
    full=torch.cat((prompt,completion[None,:]),1)
    out=policy.model(input_ids=full,attention_mask=torch.ones_like(full),use_cache=False,logits_to_keep=n+1)
    logits=out.logits[0,-n-1:-1,:].float()/temperature
    lp=-F.cross_entropy(logits,completion,reduction='none')
    ent=None
    if entropy:
        with torch.no_grad():
            ls=F.log_softmax(logits.detach(),dim=-1)
            ent=-(ls.exp()*ls).sum(-1).mean().item()
    return lp,ent

def generate_group(policy,prompt,g=8,temperature=.7,maximum=320,sample=True):
    from transformers import GenerationConfig
    from .common import extract_translation
    from .models import synchronize
    import time
    policy.model.eval()
    config=GenerationConfig(max_new_tokens=maximum,do_sample=sample,num_return_sequences=g,
        num_beams=1,repetition_penalty=1.,eos_token_id=policy.model.generation_config.eos_token_id or policy.tokenizer.eos_token_id,
        pad_token_id=policy.tokenizer.pad_token_id,use_cache=True,
        **(dict(temperature=temperature,top_p=1.,top_k=0) if sample else {}))
    synchronize(policy.device);start=time.perf_counter()
    with torch.inference_mode():
        generated=policy.model.generate(input_ids=prompt,attention_mask=torch.ones_like(prompt),generation_config=config)
    synchronize(policy.device);elapsed=time.perf_counter()-start
    results=[];eos=policy.model.generation_config.eos_token_id or policy.tokenizer.eos_token_id;eos=[eos] if isinstance(eos,int) else list(eos)
    for seq in generated:
        ids=seq[prompt.shape[1]:].tolist()
        hits=[i for i,t in enumerate(ids) if t in eos]
        if hits:ids=ids[:hits[0]+1]
        raw=policy.tokenizer.decode(ids,skip_special_tokens=True)
        results.append(dict(completion_ids=ids,raw_output=raw,hypothesis=extract_translation(raw),
          completion_tokens=len(ids),truncated=len(ids)>=maximum and (not ids or ids[-1] not in eos),
          generation_group_seconds=elapsed))
    return results
