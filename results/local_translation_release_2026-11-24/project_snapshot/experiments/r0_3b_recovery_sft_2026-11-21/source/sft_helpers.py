"""One bounded systematic general-Qwen SFT continuation; never uses final quality to select."""
from pathlib import Path
import os,json,time,random,math,gc,signal,traceback,hashlib
import numpy as np
import torch
from transformers import GenerationConfig
from peft import get_peft_model_state_dict
from safetensors.torch import load_file
from sacrebleu.metrics import CHRF,BLEU
from mtgrpo.common import ROOT,read_jsonl,write_json,append_jsonl,sha256,copy_key,extract_translation
from mtgrpo.models import Policy,environment_info,output_gate
from mtgrpo.r0_train import loss_sum
from mtgrpo.telemetry import ResourceSampler
from b3_store import snapshot,rng_state,restore_rng
from b3_update import update
from p18_core import learning_rate,timing_target,next_group,choose,confirmed_plateau,metric_plateau

OUT=ROOT/'run';OUT.mkdir(exist_ok=True);START=time.time();STOP=False
STRATA=['general','technical_short','technical_medium','technical_long']
def signal_stop(*_):
 global STOP;STOP=True
signal.signal(signal.SIGTERM,signal_stop)
def emit(event,**kw):
 v=dict(event=event,unix=time.time(),elapsed_seconds=time.time()-START,**kw);append_jsonl(OUT/'events.jsonl',v);write_json(OUT/'progress.json',v);print(json.dumps(v),flush=True)
def seed(n):random.seed(n);np.random.seed(n%2**32);torch.manual_seed(n);torch.cuda.manual_seed_all(n)
def close(p):p.close();gc.collect();torch.cuda.empty_cache()
def load(adapter,train=False,fp32=False):
 p=Policy('cuda',adapter=str(adapter),trainable=train,checkpointing=True,disable_dropout=False,attention_implementation='sdpa')
 state=load_file(str(Path(adapter)/'adapter_model.safetensors'));actual=get_peft_model_state_dict(p.model)
 assert state.keys()==actual.keys() and all(torch.equal(x.to(actual[k].dtype),actual[k].detach().cpu()) for k,x in state.items()),'Wrong adapter loading'
 if fp32:p.model.float();p.dtype=torch.float32
 p.model.eval();return p
def encode(p,r):
 text=p.tokenizer.apply_chat_template([dict(role='user',content=r['instruction']+'\n\n'+r['source'])],tokenize=False,add_generation_prompt=True,enable_thinking=False)
 prompt=p.tokenizer(text,add_special_tokens=False)['input_ids'];target=p.tokenizer(r['reference'].strip(),add_special_tokens=False)['input_ids']
 if not target or target[-1]!=p.tokenizer.eos_token_id:target.append(p.tokenizer.eos_token_id)
 assert len(prompt)<=1024 and len(target)<=512 and len(prompt)+len(target)<=1536
 return dict(id=r['id'],prompt=prompt,target=target,tokens=len(prompt)+len(target),stratum=r['stratum'])
def nll(p,rr):
 p.model.eval();loss=tokens=tech=tt=0
 with torch.inference_mode():
  for r in rr:
   value=float(loss_sum(p.model,[r],p.tokenizer,'cuda'));n=len(r['target']);loss+=value;tokens+=n
   if r['stratum']!='general':tech+=value;tt+=n
 return dict(nll=loss/tokens,technical_nll=tech/tt,dev_target_tokens=tokens)
def eos_ids(p):
 value=p.model.generation_config.eos_token_id or p.tokenizer.eos_token_id
 ids=[value] if isinstance(value,int) else list(value)
 if p.tokenizer.eos_token_id not in ids:ids.append(p.tokenizer.eos_token_id)
 return sorted(set(ids))
def output(p,row,ts):
 stops=eos_ids(p)
 for i,t in enumerate(ts):
  if t in stops:ts=ts[:i+1];break
 raw=p.tokenizer.decode(ts,skip_special_tokens=True);hyp=extract_translation(raw);words=hyp.casefold().split();trunc=len(ts)>=512 and (not ts or ts[-1] not in stops)
 return dict(hypothesis=hyp,raw_output=raw,completion_ids=ts,completion_tokens=len(ts),truncated=trunc,repetition=len(words)>=12 and len(set(zip(words,words[1:],words[2:]))) / max(1,len(words)-2)<.45,gate=output_gate(row['source'],hyp,truncated=trunc))
def decode(p,rr,label,sampler):
 p.model.eval();sampler.phase='greedy_'+label;dest=OUT/'evaluation'/f'{label}.jsonl';assert not dest.exists();results=[];st=time.perf_counter()
 for offset in range(0,len(rr),8):
  assert not STOP and time.time()<DEADLINE-900,'Export reserve reached'
  batch=rr[offset:offset+8]
  texts=[p.tokenizer.apply_chat_template([dict(role='user',content=row['instruction']+'\n\n'+row['source'])],tokenize=False,add_generation_prompt=True,enable_thinking=False) for row in batch]
  inp=p.tokenizer(texts,add_special_tokens=False,padding=True,return_tensors='pt').to('cuda');width=inp['input_ids'].shape[1];assert width<=1024
  with torch.inference_mode():seq=p.model.generate(**inp,generation_config=GenerationConfig(max_new_tokens=512,do_sample=False,eos_token_id=eos_ids(p),pad_token_id=p.tokenizer.pad_token_id,use_cache=True))
  for row,tokens in zip(batch,seq):
   x=dict(row,**output(p,row,tokens[width:].tolist()));append_jsonl(dest,x);results.append(x)
  emit('decode_progress',label=label,completed=min(len(rr),offset+8),total=len(rr))
 write_json(OUT/'evaluation'/f'{label}_timing.json',dict(seconds=time.perf_counter()-st,n=len(rr),precision=str(p.dtype)));return results
def g8(p,rr,label,sampler):
 p.model.eval();sampler.phase='G8_'+label;dest=OUT/'evaluation'/f'{label}.jsonl';assert not dest.exists()
 for i,row in enumerate(rr):
  assert not STOP and time.time()<DEADLINE-900,'Export reserve reached'
  sd=int.from_bytes(hashlib.sha256(('p13-g8-fixed-2026111894/'+row['id']).encode()).digest()[:4],'little')%2147483647;seed(sd);ids=p.prompt_ids(row,max_prompt_tokens=1024,thinking=False);st=time.perf_counter()
  with torch.inference_mode():seq=p.model.generate(input_ids=ids,attention_mask=torch.ones_like(ids),generation_config=GenerationConfig(max_new_tokens=512,do_sample=True,num_return_sequences=8,num_beams=1,temperature=.7,top_p=1.,top_k=0,repetition_penalty=1.,eos_token_id=eos_ids(p),pad_token_id=p.tokenizer.pad_token_id,use_cache=True))
  outputs=[dict(index=j,**output(p,row,t[ids.shape[1]:].tolist())) for j,t in enumerate(seq)]
  append_jsonl(dest,dict(row=row,seed=sd,prompt_ids=ids[0].tolist(),outputs=outputs,seconds=time.perf_counter()-st));emit('g8_progress',label=label,completed=i+1,total=len(rr))
def metrics(rr):
 by={}
 for st in STRATA:
  sub=[r for r in rr if r['stratum']==st];assert sub
  by[st]=dict(n=len(sub),chrfpp=CHRF(word_order=2).corpus_score([r['hypothesis'] for r in sub],[[r['reference'] for r in sub]]).score,bleu=BLEU().corpus_score([r['hypothesis'] for r in sub],[[r['reference'] for r in sub]]).score)
 def cf(sub):return CHRF(word_order=2).corpus_score([r['hypothesis'] for r in sub],[[r['reference'] for r in sub]]).score
 return dict(by_stratum=by,overall_chrfpp=cf(rr),technical_chrfpp=cf([r for r in rr if r['stratum']!='general']),technical_medium_long_chrfpp=cf([r for r in rr if r['stratum'] in ['technical_medium','technical_long']]),failures=sum(not r['gate']['gate'] or r['repetition'] for r in rr))
def loss_audit(p,enc):
 p.model.eval();checks=[]
 with torch.inference_mode():
  for row in [min(enc,key=lambda r:r['tokens']),max(enc,key=lambda r:r['tokens'])]:
   ids=torch.tensor([row['prompt']+row['target']],device='cuda');z=p.model(input_ids=ids,attention_mask=torch.ones_like(ids),use_cache=False,logits_to_keep=0).logits
   manual=float(torch.nn.functional.cross_entropy(z[0,len(row['prompt'])-1:-1].float(),torch.tensor(row['target'],device='cuda'),reduction='sum'));del z
   tail=float(loss_sum(p.model,[row],p.tokenizer,'cuda'));delta=abs(manual-tail)/len(row['target']);assert delta<1e-4;checks.append(dict(id=row['id'],per_token_difference=delta))
  group=[enc[i] for i in [0,len(enc)//2,-1]];nt=sum(len(r['target']) for r in group);batch=float(loss_sum(p.model,group,p.tokenizer,'cuda'))/nt;single=sum(float(loss_sum(p.model,[r],p.tokenizer,'cuda')) for r in group)/nt;assert abs(batch-single)<.02
 write_json(OUT/'loss_alignment_audit.json',dict(passed=True,explicit_shift_checks=checks,batch_nll=batch,single_nll=single,per_token_batch_delta=abs(batch-single)))
def read_reviews():
 path=ROOT/'review_summaries.json'
 try:return json.loads(path.read_text()).get('reviews',{}) if path.exists() else {}
 except (json.JSONDecodeError,FileNotFoundError):return {}

