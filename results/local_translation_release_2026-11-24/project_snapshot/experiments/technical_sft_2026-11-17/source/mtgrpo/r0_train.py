"""Budgeted batched SFT, generative dev selection and complete optimizer resume."""
import argparse
import json
import math
import random
import time
from pathlib import Path
from .common import ROOT, read_jsonl, write_json, write_jsonl, append_jsonl, sha256, copy_key
from .r0_core import collate, next_group, lr_multiplier, selection_key
from .sft_data import encode_example

TARGETS = r'model\.language_model\.layers\.\d+\.(?:self_attn\.(?:q_proj|k_proj|v_proj|o_proj)|linear_attn\.(?:in_proj_qkv|in_proj_z|in_proj_a|in_proj_b|out_proj)|mlp\.(?:gate_proj|up_proj|down_proj))'


def loss_sum(model, examples, tokenizer, device):
    import torch.nn.functional as F
    batch = collate(examples, tokenizer.pad_token_id, device)
    labels = batch.pop('labels')
    output = model(**batch, use_cache=False, logits_to_keep=labels.shape[1]+1)
    return F.cross_entropy(output.logits[:, :-1].float().reshape(-1, output.logits.shape[-1]),
                           labels.reshape(-1), ignore_index=-100, reduction='sum')


def backward_update(policy,group,optimizer,scaler,microbatch):
    """Retry FP16 scale overflow without updating weights or advancing the data budget."""
    import torch
    target_tokens=sum(len(r['target']) for r in group)
    parameters=[p for p in policy.model.parameters() if p.requires_grad]
    for retry in range(8):
        policy.model.train();optimizer.zero_grad(set_to_none=True);loss=0.
        for i in range(0,len(group),microbatch):
            value=loss_sum(policy.model,group[i:i+microbatch],policy.tokenizer,policy.device)
            if not torch.isfinite(value):raise FloatingPointError('Nonfinite forward loss')
            loss+=float(value.detach());scaler.scale(value/target_tokens).backward()
        scaler.unscale_(optimizer)
        finite=bool(torch.stack([torch.isfinite(p.grad).all() for p in parameters if p.grad is not None]).all())
        if not finite:
            if not scaler.is_enabled():raise FloatingPointError('Nonfinite gradients without FP16 scaling')
            before=scaler.get_scale();scaler.step(optimizer);scaler.update()
            if scaler.get_scale()>=before:raise FloatingPointError('FP16 overflow was not skipped safely')
            continue
        norm=torch.nn.utils.clip_grad_norm_(parameters,1.,error_if_nonfinite=True)
        scaler.step(optimizer);scaler.update()
        return dict(mean_loss=loss/target_tokens,overflow_retries=retry,
            physical_target_tokens=target_tokens*(retry+1),grad_norm=float(norm),loss_scale=scaler.get_scale())
    raise FloatingPointError('FP16 gradients still nonfinite after eight safely skipped attempts')


def evaluate(policy, dev, decode_rows, directory, label, microbatch):
    evaluation_started=time.perf_counter()
    import torch
    from sacrebleu.metrics import CHRF
    from langid.langid import LanguageIdentifier, model
    from .models import output_gate
    lid = LanguageIdentifier.from_modelstring(model, norm_probs=True)
    policy.model.eval()
    nll, tokens = 0., 0
    with torch.inference_mode():
        for i in range(0,len(dev),microbatch):
            group = dev[i:i+microbatch]
            nll += float(loss_sum(policy.model,group,policy.tokenizer,policy.device))
            tokens += sum(len(r['target']) for r in group)
    if not math.isfinite(nll):raise FloatingPointError('Nonfinite dev likelihood')
    records=[]
    for row in decode_rows:
        result = policy.generate(policy.prompt_ids(row,max_prompt_tokens=768),max_new_tokens=256)
        result.pop('completion_ids')
        gate = output_gate(row['source'], result['hypothesis'],truncated=result['truncated'])
        hyp=result['hypothesis']
        wrong = len(hyp.split()) >= 4 and lid.classify(hyp)[0] != 'is'
        words=hyp.casefold().split()
        repetition = len(words)>=12 and len(set(zip(words,words[1:],words[2:]))) / max(1,len(words)-2) < .45
        records.append({**row,**result,**gate,'wrong_language':wrong,'repetition':repetition})
    chrf=CHRF(word_order=2)
    metrics=dict(nll=nll/tokens,chrfpp=chrf.corpus_score([r['hypothesis'] for r in records],
            [[r['reference'] for r in records]]).score,
        failure_rate=sum(not r['gate'] or r['repetition'] for r in records)/len(records),
        wrong_language_rate=sum(r['wrong_language'] for r in records)/len(records),
        count=len(records),chrf_signature=str(chrf.get_signature()),semantic_review='pending',
        dev_loss_target_tokens=tokens,dev_forward_calls=math.ceil(len(dev)/microbatch),
        generation_prompt_tokens=sum(r['prompt_tokens'] for r in records),
        generation_output_tokens=sum(r['completion_tokens'] for r in records),
        evaluation_wall_seconds=time.perf_counter()-evaluation_started)
    write_jsonl(directory/f'{label}_predictions.jsonl',records)
    write_json(directory/f'{label}_metrics.json',metrics)
    return metrics


def main():
    invocation_started=time.perf_counter()
    p=argparse.ArgumentParser()
    p.add_argument('--data-dir',default=str(ROOT/'data/r0_2026-11-11'))
    p.add_argument('--run-dir',required=True)
    p.add_argument('--lr',type=float,default=1e-4)
    p.add_argument('--budget',type=int,default=100000)
    p.add_argument('--schedule-budget',type=int,default=100000)
    p.add_argument('--microbatch',type=int,default=2)
    p.add_argument('--effective-batch',type=int,default=16)
    p.add_argument('--eval-every-tokens',type=int,default=25000)
    p.add_argument('--wall-hours',type=float,default=4)
    p.add_argument('--attention',choices=['sdpa','eager'],default='sdpa')
    p.add_argument('--resume',action='store_true')
    p.add_argument('--seed',type=int,default=42)
    p.add_argument('--decode-count',type=int,default=96)
    args=p.parse_args()
    if args.budget > args.schedule_budget: raise ValueError('Budget exceeds frozen LR schedule')
    if min(args.microbatch,args.effective_batch,args.budget,args.eval_every_tokens,args.decode_count)<=0:
        raise ValueError('Budgets and batch sizes must be positive')
    import torch
    from peft import LoraConfig
    from .models import Policy, environment_info, synchronize
    from .telemetry import ResourceSampler
    if not torch.cuda.is_available(): raise RuntimeError('CUDA GPU required; do not silently train on CPU')
    torch.set_num_threads(4)
    random.seed(args.seed);torch.manual_seed(args.seed);torch.cuda.manual_seed_all(args.seed)
    d,run=Path(args.data_dir),Path(args.run_dir)
    run.mkdir(parents=True,exist_ok=True)
    hashes={k:sha256(d/f'{k}.jsonl') for k in ['train','dev','decode_dev']}
    frozen={k:v for k,v in vars(args).items() if k not in ['resume','wall_hours','budget','data_dir','run_dir']}
    frozen.update(data_hashes=hashes,model_revision='2fc06364715b967f1860aea9cf38778875588b17',
                  source_hashes={name:sha256(ROOT/'mtgrpo'/name) for name in
                      ['r0_core.py','r0_train.py','models.py','sft_data.py','common.py']},
                  lora=dict(r=16,alpha=32,dropout=.05,targets=TARGETS))
    state=None
    if (run/'config.json').exists():
        if not args.resume: raise FileExistsError('Existing run: explicitly resume, never overwrite')
        previous=json.loads((run/'config.json').read_text())
        if previous['frozen'] != frozen: raise ValueError('Resume configuration/data mismatch')
        pointer=json.loads((run/'last.json').read_text())
        ckpt=run/pointer['checkpoint']
        state=torch.load(ckpt/'state.pt',map_location='cpu',weights_only=False)
    elif args.resume: raise FileNotFoundError('No checkpoint to resume')
    policy=Policy('cuda',adapter=str(ckpt/'adapter') if state else None,trainable=True,
        lora_config=LoraConfig(task_type='CAUSAL_LM',r=16,lora_alpha=32,lora_dropout=.05,
                               target_modules=TARGETS,bias='none'),
        disable_dropout=False,attention_implementation=args.attention)
    append_jsonl(run/'invocations.jsonl',dict(unix_time=time.time(),resume=bool(state),
        environment=environment_info(),policy_dtype=str(policy.dtype),policy_load_seconds=policy.load_seconds))
    train_rows,dev_rows=read_jsonl(d/'train.jsonl'),read_jsonl(d/'dev.jsonl')
    if {copy_key(r['source']) for r in train_rows} & {copy_key(r['source']) for r in dev_rows}:
        raise ValueError('Train/dev source contamination')
    train=[encode_example(policy.tokenizer,r,768) for r in train_rows]
    dev=[encode_example(policy.tokenizer,r,768) for r in dev_rows]
    decode=read_jsonl(d/'decode_dev.jsonl')[:args.decode_count]
    optimizer=torch.optim.AdamW([v for v in policy.model.parameters() if v.requires_grad],lr=args.lr,weight_decay=.01)
    scaler=torch.amp.GradScaler('cuda',enabled=policy.dtype==torch.float16,init_scale=512.)
    cursor=consumed=step=0;best=None;training_seconds=0.;total_seconds=0.
    next_eval=args.eval_every_tokens
    if state:
        optimizer.load_state_dict(state['optimizer']);scaler.load_state_dict(state['scaler'])
        cursor,consumed,step=state['cursor'],state['consumed'],state['step']
        best=state['best'];training_seconds=state['training_seconds'];total_seconds=state['total_seconds']
        next_eval=state['next_eval']
        random.setstate(state['python_rng']);torch.set_rng_state(state['torch_rng'])
        torch.cuda.set_rng_state_all(state['cuda_rng'])
    else:
        write_json(run/'config.json',dict(frozen=frozen,environment=environment_info(),
            policy_dtype=str(policy.dtype),policy_load_seconds=policy.load_seconds,
            trainable_parameters=sum(p.numel() for p in policy.model.parameters() if p.requires_grad),
            quality_selection='structural constraints then dev chrF++; semantic review required',
            loss='sum target CE / actual target tokens incl EOS; prompts/padding ignored'))
    started=invocation_started;sampler=ResourceSampler(run/'resources.jsonl');sampler.start()
    last_save=started

    def checkpoint(reason):
        nonlocal last_save
        # Complete directory before publishing pointer; incomplete writes are ignored.
        name=f'checkpoint-{step:06d}-{consumed:09d}'
        target=run/name
        if target.exists():
            if (target/'complete.json').exists(): return
            raise RuntimeError('Incomplete checkpoint exists; retain it and use a new run after recovery')
        target.mkdir()
        policy.model.save_pretrained(target/'adapter',safe_serialization=True)
        policy.tokenizer.save_pretrained(target/'adapter')
        torch.save(dict(optimizer=optimizer.state_dict(),scaler=scaler.state_dict(),cursor=cursor,
            consumed=consumed,step=step,best=best,next_eval=next_eval,training_seconds=training_seconds,
            total_seconds=total_seconds+time.perf_counter()-started,python_rng=random.getstate(),
            torch_rng=torch.get_rng_state(),cuda_rng=torch.cuda.get_rng_state_all()),target/'state.pt')
        write_json(target/'complete.json',dict(reason=reason,step=step,target_tokens=consumed))
        write_json(run/'last.json',dict(checkpoint=name,step=step,target_tokens=consumed))
        if best and best.get('step')==step: write_json(run/'best.json',dict(checkpoint=name,metrics=best['metrics'],
            provisional=True,semantic_review='pending'))
        last_save=time.perf_counter()

    try:
        if not state:
            sampler.phase='baseline_dev'
            metrics=evaluate(policy,dev,decode,run,'dev-000000',args.microbatch)
            best=dict(step=0,metrics=metrics)
            checkpoint('baseline')
        while consumed < args.budget:
            if time.perf_counter()-started >= args.wall_hours*3600:
                checkpoint('wall_budget');break
            group,new_cursor=next_group(train,cursor,args.budget-consumed,args.effective_batch,args.seed)
            if not group: break
            target_tokens=sum(len(r['target']) for r in group)
            lr=args.lr*lr_multiplier(consumed+target_tokens,args.schedule_budget)
            for param_group in optimizer.param_groups: param_group['lr']=lr
            sampler.phase='train';synchronize('cuda');tick=time.perf_counter()
            update=backward_update(policy,group,optimizer,scaler,args.microbatch)
            synchronize('cuda');dt=time.perf_counter()-tick;training_seconds+=dt
            consumed+=target_tokens;cursor=new_cursor;step+=1
            record=dict(step=step,target_tokens=consumed,group_target_tokens=target_tokens,
                group_input_tokens=sum(len(r['prompt'])+len(r['target']) for r in group),
                padded_input_tokens=sum(len(batch)*max(len(r['prompt'])+len(r['target']) for r in batch)
                    for batch in [group[i:i+args.microbatch] for i in range(0,len(group),args.microbatch)]),
                examples=len(group),cursor=cursor,loss=update['mean_loss'],lr=lr,train_seconds=dt,
                overflow_retries=update['overflow_retries'],physical_target_tokens=update['physical_target_tokens'],
                grad_norm=update['grad_norm'],loss_scale=update['loss_scale'],
                target_tokens_per_second=target_tokens/dt,peak_vram_bytes=torch.cuda.max_memory_allocated(),
                elapsed_seconds=total_seconds+time.perf_counter()-started)
            append_jsonl(run/'train.jsonl',record);write_json(run/'progress.json',record)
            print(json.dumps(record),flush=True)
            ending=not next_group(train,cursor,args.budget-consumed,1,args.seed)[0]
            if consumed>=next_eval or ending:
                sampler.phase='dev'
                metrics=evaluate(policy,dev,decode,run,f'dev-{step:06d}',args.microbatch)
                append_jsonl(run/'dev.jsonl',dict(step=step,target_tokens=consumed,**metrics))
                if selection_key(metrics)>selection_key(best['metrics']): best=dict(step=step,metrics=metrics)
                next_eval=((consumed//args.eval_every_tokens)+1)*args.eval_every_tokens
                checkpoint('dev')
            elif time.perf_counter()-last_save>=600: checkpoint('periodic')
        checkpoint('budget_end')
        write_json(run/'summary.json',dict(target_tokens=consumed,requested_budget=args.budget,step=step,
            train_seconds=training_seconds,total_seconds=total_seconds+time.perf_counter()-started,
            cumulative_train_target_tokens_per_second=consumed/max(training_seconds,1e-9),best=best,
            completed=not next_group(train,cursor,args.budget-consumed,1,args.seed)[0],
            status='candidate_only_pending_semantic_review',
            compute_units='Read Colab resource panel; wall time is not an exact CU measurement'))
    finally:
        sampler.stop();policy.close()


if __name__=='__main__': main()
