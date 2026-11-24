"""Fixed-P18 single-arm bounded DAPO; automatic reward requires heldout gate."""
from pathlib import Path
import os,time,json,math,random,gc,hashlib
import numpy as np
import torch
from p25_helpers import preflight,sampled,evaluate,parity,parity_gate,rng,restore
from mtgrpo.common import ROOT,read_jsonl,write_json,append_jsonl,sha256
from mtgrpo.models import Policy,environment_info
from mtgrpo.dapo_core import clipped_terms,log_probabilities,generate_group,group_advantages,soft_length_penalty
from mtgrpo.telemetry import ResourceSampler
from peft import get_peft_model_state_dict,set_peft_model_state_dict
from safetensors.torch import load_file
from p25_scorer import Scorer
from p25_guard import reward,check
OUT=ROOT/'run/shortmid_train';OUT.mkdir(exist_ok=True);SEED=2026112325;BUDGET=json.loads((ROOT/'allocation_budget.json').read_text())
def emit(event,**v):
 z=dict(event=event,unix=time.time(),**v);append_jsonl(OUT/'events.jsonl',z);write_json(OUT/'progress.json',z);print('P25_'+event+':'+json.dumps(v),flush=True)
def reset(policy,path):
 state=load_file(str(path/'adapter_model.safetensors'));set_peft_model_state_dict(policy.model,state);actual=get_peft_model_state_dict(policy.model)
 assert actual.keys()==state.keys() and all(torch.equal(v.to(actual[k].dtype),actual[k].detach().cpu()) for k,v in state.items());del actual,state
 policy.model.eval();torch.manual_seed(SEED);torch.cuda.manual_seed_all(SEED);random.seed(SEED);np.random.seed(SEED)
def devcheck(policy,rows,step):
 from sacrebleu.metrics import CHRF,BLEU
 saved=rng();rr=[]
 for row in rows:
  prompt=policy.prompt_ids(row,max_prompt_tokens=1024);o=generate_group(policy,prompt,g=1,maximum=512,sample=False)[0];rr.append(dict(row,**o));append_jsonl(OUT/f'dev/step_{step:03}.jsonl',rr[-1])
 restore(saved);result=dict(step=step,subsets={})
 for key in ['overall','general','technical',*['technical_short','technical_medium']]:
  group=[r for r in rr if key=='overall' or (r['stratum']!='general' if key=='technical' else r['stratum']==key)];hyps=[r['hypothesis'] for r in group];refs=[[r['reference'] for r in group]]
  result['subsets'][key]=dict(n=len(group),chrfpp=CHRF(word_order=2).corpus_score(hyps,refs).score,bleu=BLEU().corpus_score(hyps,refs).score,truncated=sum(r['truncated'] for r in group))
 write_json(OUT/f'dev/step_{step:03}_metrics.json',result);emit('dev_checked',**result);return result
def snapshot(policy,optimizer,step,cursor,tag,full_export=False):
 dest=OUT/'checkpoints'/tag;assert not dest.exists();dest.mkdir(parents=True)
 policy.model.save_pretrained(dest/'adapter',safe_serialization=True);torch.save(dict(optimizer=optimizer.state_dict(),rng=rng(),step=step,cursor=cursor),dest/'optimizer_rng.pt')
 write_json(dest/'checkpoint.json',dict(step=step,cursor=cursor,weights_sha256=sha256(dest/'adapter/adapter_model.safetensors'),unix=time.time(),full_state_in_cloud=True,optimizer_in_durable_export=full_export))
 from p25_snapshot import make_snapshot
 make_snapshot(dest,tag,include_optimizer=full_export);index=ROOT/'snapshot_index.json';tags=json.loads(index.read_text()) if index.exists() else [];tags.append(tag);write_json(index,tags);emit('checkpoint',step=step,tag=tag,full_state_export=full_export);return dest
def score_group(scorer,row,outputs,gate):
 scores=scorer.score(row['source'],[o['hypothesis'] for o in outputs],row['reference']);active=[];rr=[];proxy=[]
 for o,s in zip(outputs,scores):
  reasons=check(row,o['hypothesis']);valid=not o['truncated'] and not s['truncated'] and not any(x in reasons for x in ['empty','exact_source_copy','severe_repetition_heuristic']);o.update(metricx=s,valid=valid,guard_reasons=reasons)
  base,_=reward(row,o['hypothesis'],s['error'],gate['recipe']) if not s['truncated'] else (0,[]);o['calibrated_reward']=base;o['proxy_positive']=valid and base>=gate['threshold_selection']['threshold'];o['reward']=base+soft_length_penalty(o['completion_tokens'],maximum=512,buffer=64)
  active.append(valid)
  if valid:rr.append(o['reward']);proxy.append(o['proxy_positive'])
 adv,std=group_advantages(rr) if rr else (torch.zeros(0),0);variants={tuple(__import__('re').findall(r'\w+|[^\w\s]',__import__('unicodedata').normalize('NFKC',o['hypothesis']))) for o,v in zip(outputs,active) if v};eligible=len(rr)>=2 and std>1e-6 and len(variants)>=2;ii=0;aa=[]
 for valid in active:
  aa.append(float(adv[ii]) if valid else 0);ii+=valid
 return dict(advantages=aa,loss_active=active,kept=eligible,reward_std=std,valid_candidates=len(rr),proxy_positive_candidates=sum(proxy),proxy_is_not_semantic_truth=True,absolute_proxy_not_used_for_eligibility=True,format_distinct_variants=len(variants),format_only_duplicates_rejected=True)
def main():
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 protocol=json.loads((ROOT/'protocol.json').read_text());gate=json.loads((ROOT/'reward_gate_decision.json').read_text());assert gate['passed'];assert sha256(ROOT/'reward_gate_decision.json')==protocol['reward_gate_SHA256']
 for n,h in protocol['data_manifest'].items():assert sha256(ROOT/'data'/n)==h
 assert not (OUT/'training_started.json').exists();write_json(OUT/'training_started.json',dict(unix=time.time(),protocol_SHA256=sha256(ROOT/'protocol.json')))
 train=read_jsonl(ROOT/'data/train.jsonl');dev=read_jsonl(ROOT/'data/dev.jsonl');test=read_jsonl(ROOT/'data/evaluation.jsonl');selection=json.loads((ROOT/'data/review_selection.json').read_text());monitor=ResourceSampler(OUT/'resources.jsonl');monitor.start();import p25_helpers; p25_helpers.OUT=OUT;scorer=None;step=0;cursor=0;history=[];points=[];stop_reason='maximum240_updates'
 try:
  policy=Policy('cpu',adapter=str(ROOT/'initial_adapter'),trainable=True,attention_implementation='sdpa');policy.model.float();policy.dtype=torch.float32;policy.model.to('cuda');policy.device='cuda';assert all(p.dtype==torch.float32 for p in policy.model.parameters() if p.is_floating_point());reset(policy,ROOT/'initial_adapter');write_json(OUT/'environment.json',dict(environment_info(),TF32=False,precision='FP32 base+LoRA'))
  preflight(policy,train);scorer=Scorer();row=next(r for r in train if r['stratum']=='technical_medium');scorer.score(row['source'],[row['reference']],row['reference']);emit('joint_residency_preflight',allocated=torch.cuda.memory_allocated(),reserved=torch.cuda.memory_reserved());base=devcheck(policy,dev,0)
  optimizer=torch.optim.AdamW([p for p in policy.model.parameters() if p.requires_grad],lr=3e-6,betas=(.9,.999),eps=1e-8,weight_decay=0.)
  while step<240:
   if time.time()>=BUDGET['training_deadline_unix'] or (ROOT/'stop_training.json').exists():stop_reason='training_deadline_or_external_stop';break
   attempts=[];accepted=[];start=time.perf_counter()
   while len(accepted)<4 and len(attempts)<32 and cursor<len(train) and time.time()<BUDGET['training_deadline_unix']:
    row=train[cursor];cursor+=1;seed=int.from_bytes(hashlib.sha256(('p25-train/'+row['id']).encode()).digest()[:4],'big');torch.manual_seed(seed);torch.cuda.manual_seed_all(seed);monitor.phase='rollout_generation';prompt=policy.prompt_ids(row,max_prompt_tokens=1024);oo=sampled(policy,prompt)
    optimizer.zero_grad(set_to_none=True);gc.collect();torch.cuda.empty_cache();monitor.phase='reward_scoring';quality=score_group(scorer,row,oo,gate);x=dict(row=row,outputs=oo,prompt_ids=prompt[0].cpu().tolist(),seed=seed,step=step,**quality);attempts.append(x)
    if x['kept']:accepted.append(x)
    emit('sampling',step=step,cursor=cursor,attempts=len(attempts),accepted=len(accepted))
   if len(accepted)<4:
    for x in attempts:append_jsonl(OUT/'rollouts.jsonl',dict(x,used_for_optimization=False))
    stop_reason='insufficient_proxy_mixed_groups_or_time_or_pool';break
   batch=[]
   for x in accepted:
    prompt=torch.tensor([x['prompt_ids']],device='cuda');details=[]
    for j,(o,adv,valid) in enumerate(zip(x['outputs'],x['advantages'],x['loss_active'])):
     if not valid:continue
     ids=torch.tensor(o['completion_ids'],device='cuda')
     with torch.no_grad():old,_=log_probabilities(policy,prompt,ids,temperature=.7)
     details.extend((old.cpu()-torch.tensor(o['sampler_logps'])).tolist());o['teacher_old_logps']=old.tolist();batch.append(dict(prompt=prompt,ids=ids,old=old.detach(),advantage=adv,id=x['row']['id'],candidate=j))
    x['probability_parity']=parity(details);parity_gate(x['probability_parity'])
   for x in attempts:append_jsonl(OUT/'rollouts.jsonl',dict(x,used_for_optimization=x['kept']))
   total=sum(len(x['ids']) for x in batch)
   for epoch in range(2):
    monitor.phase='optimization';optimizer.zero_grad(set_to_none=True);loss_value=clips=ratios=initial_delta=0.;us=time.perf_counter();old_parameters=[p.detach().clone() for p in policy.model.parameters() if p.requires_grad] if step==0 else None
    for x in batch:
     lp,_=log_probabilities(policy,x['prompt'],x['ids'],temperature=.7);terms,stats=clipped_terms(lp,x['old'],x['advantage'],low=.2,high=.28);assert torch.isfinite(terms).all()
     if epoch==0:initial_delta=max(initial_delta,float((stats['ratio']-1).abs().max()))
     loss=terms.sum()/total;loss.backward();loss_value+=float(loss.detach());clips+=float(stats['clip_active'].sum());ratios+=float(stats['ratio'].sum());append_jsonl(OUT/'new_logps.jsonl',dict(step=step+1,id=x['id'],candidate=x['candidate'],new_logps=lp.detach().tolist(),old_logps=x['old'].tolist(),advantage=x['advantage']))
    if epoch==0:assert initial_delta<=.0005
    params=[p for p in policy.model.parameters() if p.requires_grad];norm=float(torch.nn.utils.clip_grad_norm_(params,1.));assert math.isfinite(norm) and norm>0;optimizer.step();torch.cuda.synchronize();step+=1;delta=None
    if old_parameters is not None:
     delta=math.sqrt(sum(float((p.detach()-q).square().sum()) for p,q in zip(params,old_parameters)));assert delta>0;del old_parameters
    update=dict(step=step,epoch=epoch,loss=loss_value,grad_norm=norm,clip_fraction=clips/total,ratio_mean=ratios/total,initial_ratio_max_delta=initial_delta if epoch==0 else None,parameter_l2_delta=delta,active_tokens=total,seconds=time.perf_counter()-us,peak_allocated=torch.cuda.max_memory_allocated(),peak_reserved=torch.cuda.max_memory_reserved());append_jsonl(OUT/'updates.jsonl',update);emit('update',**update)
   optimizer.zero_grad(set_to_none=True);del batch;gc.collect();torch.cuda.empty_cache();append_jsonl(OUT/'rollout_timing.jsonl',dict(step=step,seconds=time.perf_counter()-start,accepted=4,attempted=len(attempts)))
   if step%20==0:
    current=devcheck(policy,dev,step);history.append(current);dest=snapshot(policy,optimizer,step,cursor,f'step_{step:03}');points.append(dict(step=step,cursor=cursor,path=str(dest),metrics=current));write_json(OUT/'dev_checkpoint_index.json',points);c=current['subsets'];b=base['subsets']
    if False and (c['overall']['chrfpp']<b['overall']['chrfpp']-2 or c['general']['chrfpp']<b['general']['chrfpp']-3):stop_reason='single_large_dev_regression';break
    if False and len(history)>=2 and all(h['subsets']['overall']['chrfpp']<b['overall']['chrfpp']-1.5 for h in history[-2:]):stop_reason='two_overall_dev_regressions';break
    if False and len(history)>=3:
     values=[h['subsets']['technical']['chrfpp']+h['subsets']['technical']['bleu'] for h in history]
     if max(values[-2:])<max(values[:-2])-.5:stop_reason='two_technical_checks_below_prior_best';break
  if step and step%20:
   current=devcheck(policy,dev,step);dest=snapshot(policy,optimizer,step,cursor,f'step_{step:03}');points.append(dict(step=step,cursor=cursor,path=str(dest),metrics=current));write_json(OUT/'dev_checkpoint_index.json',points)
  if not points:raise RuntimeError('No policy update completed; pool/automatic quality proxy insufficient')
  admissible=[p for p in points if all(p['metrics']['subsets'][k]['chrfpp']>=base['subsets'][k]['chrfpp']-1.5 for k in ['overall','general'])]
  chosen=max(admissible or points,key=lambda p:(sum(p['metrics']['subsets'][s]['chrfpp'] for s in ['technical_short','technical_medium'])/2,sum(p['metrics']['subsets'][s]['bleu'] for s in ['technical_short','technical_medium'])/2,-p['step']));reset(policy,Path(chosen['path'])/'adapter');state=torch.load(Path(chosen['path'])/'optimizer_rng.pt',map_location='cpu',weights_only=False);optimizer.load_state_dict(state['optimizer']);restore(state['rng']);del state
  snapshot(policy,optimizer,chosen['step'],chosen['cursor'],'shortmid_selected_full',full_export=True);write_json(OUT/'selection.json',dict(selected=chosen,admissible_steps=[p['step'] for p in admissible],basis='Dev only macro short/medium chrF++,thenBLEU; overall/general chrF retention within1.5; tie earliest; if none admissible diagnostic best without promotion',original_R0_remains_baseline=True));del optimizer;gc.collect();scorer.close();scorer=None;monitor.phase='final_evaluation'
  evaluate(policy,test,'after',selection['g8']);reset(policy,ROOT/'initial_adapter');evaluate(policy,test,'before',selection['g8'])
  write_json(OUT/'summary.json',dict(total_optimizer_updates=step,selected_step=chosen['step'],selected_tag='shortmid_selected_full',stop_reason=stop_reason,reward_recipe=gate['recipe'],new_SFT_updates=0,all_GPU_work_finished=True,source_attempts=cursor,automatic_proxy_not_human_semantic_truth=True));emit('training_complete',updates=step,selected_step=chosen['step'])
 finally:
  if scorer is not None:scorer.close()
  monitor.stop()
