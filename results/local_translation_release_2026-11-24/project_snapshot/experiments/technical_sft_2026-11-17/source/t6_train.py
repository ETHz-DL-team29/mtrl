"""Single registered technical SFT run and matched FP32 readiness evaluation."""
from pathlib import Path
import os,json,time,random,math,hashlib,gc,re,signal,traceback
import numpy as np
import torch
from mtgrpo.common import ROOT,read_jsonl,write_json,append_jsonl,sha256,copy_key,extract_translation
from mtgrpo.models import Policy,environment_info,output_gate,synchronize
from mtgrpo.sft_data import encode_example
from mtgrpo.r0_train import loss_sum
from mtgrpo.r0_core import lr_multiplier
from mtgrpo.r1_core import next_group
from mtgrpo.telemetry import ResourceSampler
from t6_core import score_records,choose
from t6_store import snapshot,rng_state,restore_rng
from t6_update import update as safe_update
OUT=ROOT/'run';OUT.mkdir(exist_ok=True);START=time.perf_counter();STOP=False
def handler(*args):
 global STOP;STOP=True
signal.signal(signal.SIGTERM,handler)
def emit(event,**values):
 r=dict(event=event,**values,unix=time.time(),elapsed_seconds=time.perf_counter()-START);append_jsonl(OUT/'events.jsonl',r);write_json(OUT/'progress.json',r);print(json.dumps(r),flush=True)
def seed(value):random.seed(value);np.random.seed(value%2**32);torch.manual_seed(value);torch.cuda.manual_seed_all(value)
def load(adapter,train=False,fp32=False):
 from peft import get_peft_model_state_dict
 from safetensors.torch import load_file
 p=Policy('cuda',adapter=str(adapter),trainable=train,checkpointing=True,disable_dropout=False,attention_implementation='sdpa')
 if fp32:p.model.float();p.dtype=torch.float32
 saved=load_file(str(Path(adapter)/'adapter_model.safetensors'));actual=get_peft_model_state_dict(p.model)
 assert saved.keys()==actual.keys() and all(torch.equal(v.to(actual[k].dtype),actual[k].detach().cpu()) for k,v in saved.items()),'Loaded adapter differs from saved weights'
 p.model.eval();return p
def decode(policy,rows,label,sampler,maximum=320):
 from transformers import GenerationConfig
 sampler.phase='greedy_'+label;dest=OUT/'evaluation'/f'{label}.jsonl';assert not dest.exists();records=[];st=time.perf_counter()
 for i,row in enumerate(rows):
  prompt=policy.prompt_ids(row,max_prompt_tokens=768,thinking=False)
  with torch.inference_mode():seq=policy.model.generate(input_ids=prompt,attention_mask=torch.ones_like(prompt),generation_config=GenerationConfig(max_new_tokens=maximum,do_sample=False,eos_token_id=policy.tokenizer.eos_token_id,pad_token_id=policy.tokenizer.pad_token_id,use_cache=True))
  ids=seq[0,prompt.shape[1]:].tolist();eos=policy.tokenizer.eos_token_id
  if eos in ids:ids=ids[:ids.index(eos)+1]
  raw=policy.tokenizer.decode(ids,skip_special_tokens=True);hyp=extract_translation(raw);truncated=len(ids)>=maximum and (not ids or ids[-1]!=eos)
  words=hyp.casefold().split();rep=len(words)>=12 and len(set(zip(words,words[1:],words[2:]))) / max(1,len(words)-2)<.45
  r=dict(row,raw_output=raw,hypothesis=hyp,completion_ids=ids,completion_tokens=len(ids),truncated=truncated,
   gate=output_gate(row['source'],hyp,truncated=truncated),repetition=rep)
  append_jsonl(dest,r);records.append(r)
  if (i+1)%16==0:emit('decode_progress',label=label,completed=i+1,total=len(rows))
 emit('decode_done',label=label,n=len(rows),seconds=time.perf_counter()-st)
 return records
def g8(policy,rows,label,sampler):
 from transformers import GenerationConfig
 sampler.phase='g8_'+label;dest=OUT/'evaluation'/f'g8_{label}.jsonl';assert not dest.exists()
 for i,row in enumerate(rows):
  row=dict(row,instruction='Translate the following English text into Icelandic. Return only the Icelandic translation.')
  sd=int.from_bytes(hashlib.sha256(('t6-g8-fixed/'+row['id']).encode()).digest()[:4],'little')%2147483647;seed(sd)
  prompt=policy.prompt_ids(row,max_prompt_tokens=768,thinking=False);st=time.perf_counter()
  with torch.inference_mode():seq=policy.model.generate(input_ids=prompt,attention_mask=torch.ones_like(prompt),generation_config=GenerationConfig(max_new_tokens=320,do_sample=True,num_return_sequences=8,num_beams=1,temperature=.7,top_p=1.,top_k=0,repetition_penalty=1.,eos_token_id=policy.tokenizer.eos_token_id,pad_token_id=policy.tokenizer.pad_token_id,use_cache=True))
  outputs=[]
  for j,s in enumerate(seq):
   ids=s[prompt.shape[1]:].tolist();eos=policy.tokenizer.eos_token_id
   if eos in ids:ids=ids[:ids.index(eos)+1]
   raw=policy.tokenizer.decode(ids,skip_special_tokens=True);hyp=extract_translation(raw);truncated=len(ids)>=320 and (not ids or ids[-1]!=eos)
   outputs.append(dict(index=j,raw_output=raw,hypothesis=hyp,completion_ids=ids,completion_tokens=len(ids),truncated=truncated,gate=output_gate(row['source'],hyp,truncated=truncated)))
  append_jsonl(dest,dict(row=row,seed=sd,prompt_ids=prompt[0].tolist(),outputs=outputs,seconds=time.perf_counter()-st))
  emit('g8_progress',label=label,completed=i+1,total=len(rows))
def nll(policy,dev,microbatch):
 policy.model.eval();total=0.;tokens=0;technical=0.;tech_tokens=0
 with torch.inference_mode():
  for i in range(0,len(dev),microbatch):
   # Keep strata separate for correctly weighted technical NLL.
   for s in sorted(set(x['stratum'] for x in dev[i:i+microbatch])):
    b=[x for x in dev[i:i+microbatch] if x['stratum']==s];value=float(loss_sum(policy.model,b,policy.tokenizer,'cuda'));nt=sum(len(x['target']) for x in b)
    total+=value;tokens+=nt
    if s!='general':technical+=value;tech_tokens+=nt
 return dict(nll=total/tokens,technical_nll=technical/tech_tokens,dev_target_tokens=tokens)
def evaluate(policy,dev,decode_rows,tag,sampler,microbatch):
 sampler.phase='nll_'+tag;metrics=nll(policy,dev,microbatch);metrics.update(score_records(decode(policy,decode_rows,'selection_'+tag,sampler)))
 write_json(OUT/'evaluation'/f'selection_{tag}_metrics.json',metrics);return metrics
def original_baseline_and_G8(ROOT,OUT,data,evalrows,g8rows,sampler):
 policy=load(ROOT/'initial_adapter',fp32=True)
 # Reproduce two full greedy anchors before borrowing cached FP32 R0 outputs.
 cached=read_jsonl(data/'R5_fp32_R0_baseline128.jsonl');anchors=[evalrows[0],next(r for r in evalrows if r['stratum']=='technical_medium')]
 assert [(r['id'],r['source'],r['reference'],r.get('instruction')) for r in cached]==[(r['id'],r['source'],r['reference'],r.get('instruction')) for r in evalrows],'Cached baseline dataset/prompt mismatch'
 ar=decode(policy,anchors,'R0_cache_anchors',sampler);byid={r['id']:r for r in cached}
 cacheok=len(cached)==128 and all(a['hypothesis']==byid[a['id']]['hypothesis'] for a in ar)
 if cacheok:
  write_json(OUT/'baseline_cache.json',dict(reused=True,sha256=sha256(data/'R5_fp32_R0_baseline128.jsonl'),anchors_exact=True,precision='FP32',max_new_tokens=320))
  # Canonical baseline record format preserves original outputs unaltered.
  (OUT/'evaluation/R0_fp32_128.jsonl').write_bytes((data/'R5_fp32_R0_baseline128.jsonl').read_bytes())
 else:
  decode(policy,evalrows,'R0_fp32_128',sampler);write_json(OUT/'baseline_cache.json',dict(reused=False,reason='Cache-anchor mismatch; full baseline regenerated'))
 g8(policy,g8rows,'R0',sampler);policy.close();del policy;gc.collect();torch.cuda.empty_cache()
def main(resume=False):
 assert torch.cuda.is_available() and torch.cuda.get_device_capability()[0]>=8,'Native BF16 GPU required'
 assert resume or not (OUT/'started.json').exists(),'Never silently duplicate/restart a run'
 if resume:assert (OUT/'started.json').exists() and (OUT/'last_checkpoint.json').exists(),'Explicit resume needs verified state and journals'
 protocol=json.loads((ROOT/'protocol.json').read_text());cfg=protocol['training'];data=ROOT/'data'
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 seed(cfg['seed'])
 if not resume:write_json(OUT/'started.json',dict(unix=time.time(),protocol_sha256=sha256(ROOT/'protocol.json')))
 else:assert json.loads((OUT/'started.json').read_text())['protocol_sha256']==sha256(ROOT/'protocol.json')
 append_jsonl(OUT/'invocations.jsonl',dict(unix=time.time(),resume=resume))
 write_json(OUT/'environment.json',environment_info());write_json(OUT/'execution_precision.json',dict(SFT='BF16 base+FP32 LoRA',evaluation='same loaded BF16-rounded base promoted toFP32',TF32=False,autocast=False))
 trainrows=read_jsonl(data/'train.jsonl');devrows=read_jsonl(data/'dev.jsonl');selectionrows=read_jsonl(data/'decode_dev.jsonl');evalrows=read_jsonl(data/'evaluation128.jsonl');g8rows=read_jsonl(data/'g8_32.jsonl')
 assert not {copy_key(r['source']) for r in trainrows}&{copy_key(r['source']) for r in devrows+selectionrows+evalrows+g8rows}
 assert sha256(ROOT/'initial_adapter/adapter_model.safetensors')==protocol['initial_adapter_sha256']
 sampler=ResourceSampler(OUT/'resources.jsonl');sampler.start();candidates=[]
 try:
  if not resume:
   original_baseline_and_G8(ROOT,OUT,data,evalrows,g8rows,sampler)
  else:
   assert len(read_jsonl(OUT/'evaluation/g8_R0.jsonl'))==32 and len(read_jsonl(OUT/'evaluation/R0_fp32_128.jsonl'))==128
  resume_state=None;adapter=ROOT/'initial_adapter'
  if resume:
   pointer=json.loads((OUT/'last_checkpoint.json').read_text());checkpoint=OUT/pointer['path'];adapter=checkpoint/'adapter'
   assert sha256(adapter/'adapter_model.safetensors')==pointer['adapter_sha256']
   assert sha256(checkpoint/'optimizer_rng.pt')==pointer['optimizer_rng_sha256']
   resume_state=torch.load(checkpoint/'optimizer_rng.pt',map_location='cpu',weights_only=False)
   state=resume_state['state'];assert state['code_manifest_sha256']==sha256(ROOT/'source_manifest.json') and state['order_sha256']==sha256(data/'exposure_order.json') and state['protocol_sha256']==sha256(ROOT/'protocol.json')
  policy=load(adapter,train=True);train=[];dev=[]
  encoded=json.loads((data/'encoded_train.json').read_text())
  for r in trainrows:
   x=encode_example(policy.tokenizer,r,768);assert x==encoded[r['id']];x['stratum']=r['stratum'];train.append(x)
  for r in devrows:
   x=encode_example(policy.tokenizer,r,768);x['stratum']=r['stratum'];dev.append(x)
  params=[p for p in policy.model.parameters() if p.requires_grad];assert sum(p.numel() for p in params)==10822656
  assert {p.dtype for p in params}=={torch.float32};write_json(OUT/'adapter_training_audit.json',dict(trainable=sum(p.numel() for p in params),dtype='float32',dropout=[m.p for m in policy.model.modules() if isinstance(m,torch.nn.Dropout) and m.p>0]))
  seed(cfg['seed']);optimizer=torch.optim.AdamW(params,lr=cfg['lr'],betas=(.9,.999),eps=1e-8,weight_decay=.01)
  order=json.loads((data/'exposure_order.json').read_text());micro=4
  step=cursor=consumed=0;train_seconds=0.;lastsave=time.perf_counter();trainstart=None
  if resume_state:
   optimizer.load_state_dict(resume_state['optimizer']);state=resume_state['state']
   step,cursor,consumed=state['step'],state['cursor'],state['target_tokens'];micro=state['microbatch'];train_seconds=state['train_seconds'];candidates=state['candidates'];restore_rng(resume_state['rng'])
   journal=OUT/'train.jsonl'
   if journal.exists():
    history=read_jsonl(journal);tail=[x for x in history if x['step']>step]
    if tail:
     prior=OUT/'resume_discarded_update_records';prior.mkdir(exist_ok=True);(prior/f'tail_{int(time.time())}.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in tail))
     journal.write_text(''.join(json.dumps(x)+'\n' for x in history if x['step']<=step))
   emit('explicit_resume',step=step,target_tokens=consumed,checkpoint=pointer['tag'])
   del resume_state
  def save(tag,metrics=None,immutable=True):
   nonlocal lastsave
   dest=OUT/'checkpoints'/tag;dest.mkdir(parents=True,exist_ok=False)
   policy.model.save_pretrained(dest/'adapter',safe_serialization=True)
   state=dict(step=step,cursor=cursor,target_tokens=consumed,train_seconds=train_seconds,microbatch=micro,candidates=candidates,metrics=metrics,
    order_sha256=sha256(data/'exposure_order.json'),code_manifest_sha256=sha256(ROOT/'source_manifest.json'),protocol_sha256=sha256(ROOT/'protocol.json'))
   write_json(dest/'state.json',state);torch.save(dict(optimizer=optimizer.state_dict(),rng=rng_state(),state=state),dest/'optimizer_rng.pt')
   meta=dict(tag=tag,step=step,target_tokens=consumed,adapter_sha256=sha256(dest/'adapter/adapter_model.safetensors'),optimizer_rng_sha256=sha256(dest/'optimizer_rng.pt'),path=str(dest.relative_to(OUT)))
   write_json(dest/'checkpoint.json',meta);write_json(OUT/'last_checkpoint.json',meta)
   if immutable:snapshot(dest,tag)
   lastsave=time.perf_counter();emit('checkpoint',**meta)
  if not resume:
   initial_rng=rng_state();torch.save(initial_rng,OUT/'initial_training_rng.pt')
   baseline=evaluate(policy,dev,selectionrows,'t000000',sampler,micro);restore_rng(initial_rng);candidates.append(dict(tag='t000000',step=0,target_tokens=0,metrics=baseline));save('t000000',baseline)
  else:baseline=candidates[0]['metrics']
  trainstart=time.perf_counter();next_eval=next((n for n in [100000,200000,400000] if n>consumed),400000);stop='frozen_budget_completed';trained_snapshots=[x['tag'] for x in candidates if x['step']>0]
  while cursor<len(order):
   if STOP or time.perf_counter()-trainstart>90*60 or time.perf_counter()-START>7200:
    stop='external_stop' if STOP else 'wall_budget';break
   group,end=next_group(train,order,cursor,400000-consumed,32)
   if not group:break
   group=sorted(group,key=lambda x:len(x['prompt'])+len(x['target']));nt=sum(len(x['target']) for x in group)
   lr=cfg['lr']*lr_multiplier(consumed+nt,400000)
   for g in optimizer.param_groups:g['lr']=lr
   sampler.phase='SFT_train';synchronize('cuda');tick=time.perf_counter()
   update=safe_update(policy,group,optimizer,micro,rng_state,restore_rng)
   if update['microbatch']!=micro:micro=update['microbatch'];emit('microbatch_fallback',microbatch=micro,effective_batch_unchanged=32)
   synchronize('cuda');dt=time.perf_counter()-tick;step+=1;cursor=end;consumed+=nt;train_seconds+=dt
   rec=dict(step=step,target_tokens=consumed,cursor=cursor,group_target_tokens=nt,group_examples=len(group),microbatch=micro,loss=update['mean_loss'],grad_norm=update['grad_norm'],lr=lr,seconds=dt,physical_target_tokens=update['physical_target_tokens'],
    group_tokens_by_stratum={s:sum(len(r['target']) for r in group if r['stratum']==s) for s in ['general','technical_short','technical_medium','technical_long']},
    input_tokens=sum(len(r['prompt'])+len(r['target']) for r in group),peak_torch_allocated=torch.cuda.max_memory_allocated(),peak_torch_reserved=torch.cuda.max_memory_reserved())
   append_jsonl(OUT/'train.jsonl',rec);emit('train_update',**rec)
   if step==20:write_json(OUT/'throughput_probe.json',dict(updates=20,target_tokens=consumed,seconds=train_seconds,tokens_per_second=consumed/train_seconds,projected_train_seconds=400000/(consumed/train_seconds),included_in_budget=True,quality_used=False))
   ending=cursor>=len(order) or not next_group(train,order,cursor,400000-consumed,1)[0]
   if consumed>=next_eval or ending:
    tag='t400000' if ending else f't{next_eval:06}'
    state_rng=rng_state();metrics=evaluate(policy,dev,selectionrows,tag,sampler,micro);restore_rng(state_rng)
    candidates.append(dict(tag=tag,step=step,target_tokens=consumed,metrics=metrics));write_json(OUT/'selection_candidates.json',candidates);save(tag,metrics);trained_snapshots.append(tag);next_eval=200000 if next_eval==100000 else 400000
   elif time.perf_counter()-lastsave>=300:
    save(f'recovery_{step:06}',immutable=False)
  if not trained_snapshots or candidates[-1]['step']!=step:
   tag=f'stopped_{step:06}';state_rng=rng_state();metrics=evaluate(policy,dev,selectionrows,tag,sampler,micro);restore_rng(state_rng)
   candidates.append(dict(tag=tag,step=step,target_tokens=consumed,metrics=metrics));save(tag,metrics)
  chosen=choose(candidates);write_json(OUT/'selected_candidate.json',chosen);write_json(OUT/'selection_candidates.json',candidates)
  policy.close();del policy;gc.collect();torch.cuda.empty_cache()
  adapter=OUT/'checkpoints'/chosen['tag']/'adapter';policy=load(adapter,fp32=True)
  decode(policy,evalrows,'SFT_fp32_128',sampler);g8(policy,g8rows,'SFT',sampler);policy.close();del policy;gc.collect();torch.cuda.empty_cache()
  sampler.phase='auxiliary_MetricX'
  from mtgrpo.dapo_reward import Scorer
  scorer=Scorer('cuda');a=read_jsonl(OUT/'evaluation/g8_R0.jsonl');b=read_jsonl(OUT/'evaluation/g8_SFT.jsonl')
  for i,(x,y) in enumerate(zip(a,b)):
   assert x['row']['id']==y['row']['id'];row=x['row'];o=[]
   for label,bank in [('R0',x),('SFT',y)]:
    hyps=[z['hypothesis'] for z in bank['outputs']];rr=scorer.score(row['source'],hyps,row['reference'],'reference');qq=scorer.score(row['source'],hyps,row['reference'],'qe')
    o.append(dict(label=label,scores=[dict(index=j,reference=r,qe=q) for j,(r,q) in enumerate(zip(rr,qq))]))
   append_jsonl(OUT/'evaluation/g8_rewards.jsonl',dict(id=row['id'],outputs=o));emit('scoring_progress',completed=i+1,total=32)
  scorer.close();del scorer
  summary=dict(status='completed_pending_locked_semantic_review',step=step,target_tokens=consumed,train_seconds=train_seconds,worker_seconds=time.perf_counter()-START,stop_reason=stop,
   selected_tag=chosen['tag'],selected_step=chosen['step'],selected_target_tokens=chosen['target_tokens'],initial_adapter_sha256=protocol['initial_adapter_sha256'],selected_adapter_sha256=sha256(adapter/'adapter_model.safetensors'),
   G8_sources=32,G8_candidates_per_side=256,selection_used_final_outputs=False)
  write_json(OUT/'summary.json',summary);emit('completed',step=step,target_tokens=consumed)
 finally:sampler.stop()
if __name__=='__main__':
 try:
  import argparse
  parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');main(parser.parse_args().resume)
 except BaseException as e:
  write_json(OUT/'error.json',dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc(),unix=time.time()));raise
