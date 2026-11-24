"""Colab-only fit gate and bounded fresh-optimizer higher-rank SFT."""
from pathlib import Path
import json,os,time,math,random,hashlib,gc,shutil
import numpy as np,torch
from safetensors.torch import load_file,save_file
from mtgrpo.common import ROOT,read_jsonl,write_json,append_jsonl,sha256
from mtgrpo.telemetry import ResourceSampler
from b3_update import update
from b3_store import rng_state,restore_rng,snapshot
import sft_helpers as h
OUT=ROOT/'run';OUT.mkdir(exist_ok=True);P=json.loads((ROOT/'protocol.json').read_text());B=json.loads((ROOT/'allocation_budget.json').read_text());END=B['deadline_unix'];TRAIN_END=B['training_deadline_unix'];h.DEADLINE=END
STOP=False
def emit(event,**kw):
 z=dict(event=event,unix=time.time(),**kw);append_jsonl(OUT/'events.jsonl',z);write_json(OUT/'progress.json',z);print(json.dumps(z),flush=True)
def seed(n):random.seed(n);np.random.seed(n%2**32);torch.manual_seed(n);torch.cuda.manual_seed_all(n)
def wait_review(path,seconds=600):
 end=min(time.time()+seconds,TRAIN_END-60)
 while time.time()<end:
  if path.exists():return json.loads(path.read_text())
  time.sleep(5)
 return None
def expand():
 seed(2026112118);old=load_file(str(ROOT/'initial_adapter/adapter_model.safetensors'));new={};tests=[]
 for name,value in old.items():
  if '.lora_A.' in name:
   assert value.shape[0]==16;z=torch.empty((64,value.shape[1]),dtype=value.dtype);torch.nn.init.kaiming_uniform_(z,a=math.sqrt(5));z[:16]=value;new[name]=z
  elif '.lora_B.' in name:
   assert value.shape[1]==16;z=torch.zeros((value.shape[0],64),dtype=value.dtype);z[:,:16]=value;new[name]=z
  else:raise AssertionError('Unexpected trainable tensor outside LoRA')
 for name,a in old.items():
  if '.lora_A.' not in name:continue
  bn=name.replace('.lora_A.','.lora_B.');x=torch.randn((3,a.shape[1]),dtype=torch.float32);u=(x@a.float().T)@old[bn].float().T*2;v=(x@new[name].float().T)@new[bn].float().T*2;delta=float((u-v).abs().max());assert delta<2e-5;tests.append(delta)
 cfg=json.loads((ROOT/'initial_adapter/adapter_config.json').read_text());assert cfg['r']==16 and cfg['lora_alpha']==32 and not cfg.get('use_rslora',False)
 cfg.update(r=64,lora_alpha=128,lora_dropout=.05)
 dest=ROOT/'expanded_adapter';dest.mkdir();(dest/'adapter_config.json').write_text(json.dumps(cfg,indent=2));save_file(new,str(dest/'adapter_model.safetensors'),metadata={'format':'pt'})
 write_json(OUT/'rank_expansion_audit.json',dict(old_rank=16,new_rank=64,old_scale=2,new_scale=2,old_blocks_identical=True,new_B_columns_zero=True,random_module_probe_max_delta=max(tests),original_adapter_sha256=sha256(ROOT/'initial_adapter/adapter_model.safetensors')))
 del old,new;gc.collect();return dest
def evaluate(p,dev,gdev,label,sampler):
 rr=rng_state();m=h.nll(p,[h.encode(p,r) for r in dev]);greedy=h.decode(p,dev,'dev_'+label,sampler);m.update(h.metrics(greedy));h.g8(p,gdev,'dev_g8_'+label,sampler);restore_rng(rr);write_json(OUT/'evaluation'/('dev_'+label+'_metrics.json'),m);return m
def main():
 assert torch.cuda.is_available() and torch.cuda.get_device_capability()[0]>=8
 assert not (OUT/'training_started.json').exists();write_json(OUT/'training_started.json',dict(unix=time.time(),protocol_sha256=sha256(ROOT/'protocol.json')))
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;seed(2026112118)
 for n,v in P['data_manifest'].items():assert sha256(ROOT/'data'/n)==v
 sampler=ResourceSampler(OUT/'resources.jsonl');sampler.start();p=None;opt=None
 try:
  emit('expanding_rank_preserving_initial_function');expanded=expand();fit=read_jsonl(ROOT/'data/fit.jsonl');audit_ids=set(json.loads((ROOT/'data/fit_audit_ids.json').read_text()));audit=[r for r in fit if r['id'] in audit_ids]
  p=h.load(expanded,train=True);[setattr(m,'p',0.) for m in p.model.modules() if isinstance(m,torch.nn.Dropout)];enc=[h.encode(p,r) for r in fit];h.loss_audit(p,enc)
  h.decode(p,audit,'fit_before',sampler);write_json(OUT/'fit_before_NLL.json',h.nll(p,enc));params=[x for x in p.model.parameters() if x.requires_grad];assert {x.dtype for x in params}=={torch.float32}
  opt=torch.optim.AdamW(params,lr=1e-4,betas=(.9,.999),eps=1e-8,weight_decay=0.);assert not opt.state
  consumed=step=cursor=0;fit_end=min(TRAIN_END,time.time()+45*60);micro=4;passed=False;next_check=25000;phase_updates=[]
  emit('fit_probe_training',maximum_targets=250000)
  while consumed<250000 and time.time()<fit_end:
   if cursor>=len(enc):random.shuffle(enc);cursor=0
   group=enc[cursor:cursor+8];cursor+=len(group);nt=sum(len(r['target']) for r in group)
   if consumed+nt>250000:break
   before=[x.detach().clone() for x in params] if step==0 else None
   u=update(p,sorted(group,key=lambda r:r['tokens']),opt,micro,rng_state,restore_rng);micro=u['microbatch'];step+=1;consumed+=nt
   delta=math.sqrt(sum(float((x.detach()-v).float().square().sum()) for x,v in zip(params,before))) if before is not None else None
   if step==1:assert delta>0
   rec=dict(phase='fit',step=step,target_tokens=consumed,lr=1e-4,parameter_L2_delta=delta,group_ids=[r['id'] for r in group],**u);append_jsonl(OUT/'fit_updates.jsonl',rec)
   if step%10==0:emit('fit_update',step=step,target_tokens=consumed,loss=u['mean_loss'])
   if consumed>=next_check or time.time()>fit_end-180:
    tag=f'fit_{consumed:07}';h.decode(p,audit,tag,sampler);write_json(OUT/'evaluation'/(tag+'_NLL.json'),h.nll(p,enc));emit('await_fit_review',tag=tag,step=step,target_tokens=consumed)
    decision=wait_review(ROOT/'reviews'/(tag+'.json'),min(600,max(30,fit_end-time.time())));phase_updates.append(dict(tag=tag,decision=decision))
    if decision and decision.get('passed'):
     assert decision['confirmed_P']>=26 and decision['long_P']>=12 and decision['reviewed']==32;passed=True;break
    next_check=100000 if next_check==25000 else 250000
  fitdest=OUT/'checkpoints/fit_diagnostic';fitdest.mkdir(parents=True);p.model.save_pretrained(fitdest/'adapter',safe_serialization=True);write_json(fitdest/'state.json',dict(diagnostic_only=True,production_start=False,steps=step,target_tokens=consumed,fit_gate_passed=passed));snapshot(fitdest,'fit_diagnostic')
  write_json(OUT/'fit_gate_outcome.json',dict(passed=passed,target_tokens=consumed,steps=step,reviews=phase_updates,production_weights_not_initialized_from_fit=True))
  h.close(p);p=None;del opt,params;opt=None;gc.collect();torch.cuda.empty_cache()
  if not passed:
   write_json(OUT/'summary.json',dict(status='FIT_GATE_FAILED_PRODUCTION_NOT_STARTED',production_updates=0,fit_updates=step,fit_target_tokens=consumed,reason='Tiny-set free generation gate did not pass within bound',new_checkpoint_not_qualified=True));emit('fit_gate_failed');return
  seed(2026112118);p=h.load(expanded,train=True);params=[x for x in p.model.parameters() if x.requires_grad];opt=torch.optim.AdamW(params,lr=5e-5,betas=(.9,.999),eps=1e-8,weight_decay=.01);assert not opt.state
  train=read_jsonl(ROOT/'data/train.jsonl');enc={r['id']:h.encode(p,r) for r in train};saved={r['id']:r for r in read_jsonl(ROOT/'data/encoded_train.jsonl')};assert enc==saved
  dev=read_jsonl(ROOT/'data/dev.jsonl');gdev=read_jsonl(ROOT/'data/dev_g8.jsonl');test=read_jsonl(ROOT/'data/final_test.jsonl');gtest=read_jsonl(ROOT/'data/final_g8.jsonl');order=json.loads((ROOT/'data/exposure_order.json').read_text());total=sum(len(enc[i]['target']) for i in order)
  main_end=min(TRAIN_END,time.time()+4*3600);baseline=evaluate(p,dev,gdev,'A',sampler);write_json(OUT/'baseline_dev.json',baseline);emit('baseline_development_ready');baseline_review=wait_review(ROOT/'reviews/A.json',600);assert baseline_review,'Baseline semantic review unavailable'
  candidates=[dict(tag='A',step=0,target_tokens=0,metrics=baseline,adapter_sha256=sha256(expanded/'adapter_model.safetensors'),path='expanded_adapter',review=baseline_review)]
  reviews_path=ROOT/'reviews/development.json';cursor=consumed=step=0;next_eval=500000;micro=4;seconds=0.;lock=None;stop='planned_stream_completed';prior_general=[]
  def save(tag,m=None,full=False):
   dest=OUT/'checkpoints'/tag;dest.mkdir(parents=True);p.model.save_pretrained(dest/'adapter',safe_serialization=True);s=dict(step=step,cursor=cursor,target_tokens=consumed,main_end_unix=main_end,budget_lock=lock,order_sha256=sha256(ROOT/'data/exposure_order.json'),full_optimizer_RNG=full)
   write_json(dest/'state.json',s)
   if full:torch.save(dict(optimizer=opt.state_dict(),rng=rng_state(),state=s),dest/'optimizer_rng.pt')
   info=dict(tag=tag,step=step,target_tokens=consumed,adapter_sha256=sha256(dest/'adapter/adapter_model.safetensors'),full_optimizer_RNG=full);write_json(dest/'checkpoint.json',info);snapshot(dest,tag);emit('checkpoint',**info);return dict(info,path=str((dest/'adapter').relative_to(ROOT)),metrics=m)
  while cursor<len(order) and consumed<total:
   if time.time()>main_end-300:stop='registered_training_cutoff';break
   limit=lock['target_tokens'] if lock else total;group=[];nt=0
   while cursor+len(group)<len(order) and len(group)<32 and nt<2048:
    r=enc[order[cursor+len(group)]]
    if consumed+nt+len(r['target'])>limit:break
    group.append(r);nt+=len(r['target'])
   if not group:break
   rate=5e-5*min(1.,max(1,consumed+nt)/50000)
   if consumed>50000:rate=5e-6+(5e-5-5e-6)*.5*(1+math.cos(math.pi*min(1.,(consumed-50000)/max(1,limit-50000))))
   for pg in opt.param_groups:pg['lr']=rate
   sampler.phase='SFT';start=time.perf_counter();u=update(p,sorted(group,key=lambda r:r['tokens']),opt,micro,rng_state,restore_rng);torch.cuda.synchronize();dt=time.perf_counter()-start;seconds+=dt;micro=u['microbatch'];step+=1;cursor+=len(group);consumed+=nt
   append_jsonl(OUT/'updates.jsonl',dict(step=step,target_tokens=consumed,cursor=cursor,lr=rate,seconds=dt,group_ids=[r['id'] for r in group],group_target_tokens=nt,**u))
   if step%10==0:emit('train_update',step=step,target_tokens=consumed,loss=u['mean_loss'],tokens_per_second=consumed/seconds)
   if step==30:
    available=max(0,main_end-time.time()-1200);cap=min(total,consumed+int(.75*(consumed/seconds)*available));grid=[n for n in [500000,1000000,1500000,2000000,total] if n<=cap+512];target=max(grid) if grid else consumed
    lock=dict(target_tokens=target,quality_used=False,measured_target_tokens_per_second=consumed/seconds,available_seconds=available,maximum_main_end=main_end);write_json(OUT/'frozen_budget.json',lock);emit('timing_budget_locked',**lock)
   ending=cursor>=len(order) or consumed>=limit-512 or time.time()>main_end-600
   if consumed>=next_eval or ending:
    tag=f't{consumed:07}';m=evaluate(p,dev,gdev,tag,sampler);candidate=save(tag,m,full=(consumed>=1000000 and (consumed//1000000)>((consumed-nt)//1000000)) or ending or next_eval%1000000==0);candidates.append(candidate);write_json(OUT/'selection_candidates.json',candidates);next_eval+=500000;emit('development_ready',tag=tag,target_tokens=consumed)
    review=wait_review(ROOT/'reviews'/(tag+'.json'),600)
    if not review:stop='missing_semantic_review_conservative_stop';break
    candidate['review']=review;write_json(OUT/'selection_candidates.json',candidates)
    if consumed>=1000000 and not any(c.get('review',{}).get('coverage_P',-1)>json.loads((ROOT/'reviews/A.json').read_text())['coverage_P'] or c.get('review',{}).get('greedy_P',-1)>json.loads((ROOT/'reviews/A.json').read_text())['greedy_P'] for c in candidates[1:]):stop='no_semantic_gain_at1M';break
    general=m['by_stratum']['general']['chrfpp'];base=baseline['by_stratum']['general']['chrfpp'];prior_general.append(general)
    if general<base-5 or len(prior_general)>=2 and all(v<base-2 for v in prior_general[-2:]):stop='general_regression';break
    if ending:break
  if not any(c['step']==step for c in candidates):
   tag=f't{consumed:07}';m=evaluate(p,dev,gdev,tag,sampler);c=save(tag,m,full=True);candidates.append(c);write_json(OUT/'selection_candidates.json',candidates);emit('development_ready',tag=tag,target_tokens=consumed);review=wait_review(ROOT/'reviews'/(tag+'.json'),600)
   if review:c['review']=review
  base_review=wait_review(ROOT/'reviews/A.json',300);assert base_review
  candidates[0]['review']=base_review
  eligible=[c for c in candidates if c.get('review') and c['metrics']['by_stratum']['general']['chrfpp']>=baseline['by_stratum']['general']['chrfpp']-1.5]
  assert eligible;best=max(eligible,key=lambda c:(c['review']['coverage_P'],c['review']['greedy_P'],c['metrics']['technical_medium_long_chrfpp'],-c['target_tokens']))
  write_json(OUT/'sealed_weights.json',dict(selected=best,unix=time.time(),final_outputs_not_generated=True,selection='Reviewed development coverage,greedy semanticP,technicalCF,earlier;general eligibility−1.5'))
  selected=ROOT/best['path'];shutil.copytree(selected,ROOT/'selected_adapter');h.close(p);p=None;del opt,params;opt=None;gc.collect();torch.cuda.empty_cache()
  for label,path in [('before',ROOT/'initial_adapter'),('after',ROOT/'selected_adapter')]:
   p=h.load(path,fp32=True);h.decode(p,test,label+'_greedy',sampler);h.g8(p,gtest,label+'_g8',sampler);h.close(p);p=None
  write_json(OUT/'summary.json',dict(status='GPU_WORK_FINISHED_REVIEW_PENDING',production_updates=step,target_tokens=consumed,train_seconds=seconds,selected=best,stop_reason=stop,fit_gate_passed=True,original_adapter_sha256=sha256(ROOT/'initial_adapter/adapter_model.safetensors'),selected_adapter_sha256=sha256(ROOT/'selected_adapter/adapter_model.safetensors'),final_greedy_sources=len(test),final_G8_sources=len(gtest),precision='MatchedFP32',DAPO_updates=0,MetricX_calls=0));emit('all_GPU_work_finished',step=step,target_tokens=consumed)
 finally:
  sampler.stop()
  if p is not None:h.close(p)
if __name__=='__main__':main()
