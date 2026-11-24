from pathlib import Path
import json,time,hashlib,torch,gc
from transformers import GenerationConfig
from mtgrpo.common import ROOT,read_jsonl,write_json,extract_translation,sha256
from mtgrpo.models import make_prompt
from peft import set_peft_model_state_dict,get_peft_model_state_dict
from safetensors.torch import load_file
from p25_metrics import paired
def reset(policy,path,verify=True):
 state=load_file(str(Path(path)/'adapter_model.safetensors'));set_peft_model_state_dict(policy.model,state)
 if verify:
  actual=get_peft_model_state_dict(policy.model);assert actual.keys()==state.keys() and all(torch.equal(v,actual[k].detach().cpu()) for k,v in state.items());del actual
 del state;policy.model.eval();torch.manual_seed(2026112325);torch.cuda.manual_seed_all(2026112325)
def emit(**v):write_json(ROOT/'run/progress.json',dict(unix=time.time(),**v))
def encode(policy,rr):
 text=[policy.tokenizer.apply_chat_template(make_prompt(r),tokenize=False,add_generation_prompt=True,enable_thinking=False) for r in rr];enc=policy.tokenizer(text,add_special_tokens=False,padding=True,return_tensors='pt');assert enc.input_ids.shape[1]<=2048,'Source prompt exceeds frozen limit;never truncate';return enc.to('cuda')
def preflight(policy):
 rr=[dict(source=s,instruction='Translate into Icelandic.') for s in ['Hello.','The dose is 3.5 mg.','Never take your inhaler apart.','An unexpected change in the speed was observed during the second test.']];enc=encode(policy,rr);pos=enc.attention_mask.cumsum(-1)-1;pos.masked_fill_(enc.attention_mask==0,0)
 with torch.inference_mode():batch=policy.model(**enc,position_ids=pos,use_cache=False,logits_to_keep=1).logits[:,-1,:].float()
 differences=[]
 for i,row in enumerate(rr):
  with torch.inference_mode():single=policy.model(**encode(policy,[row]),use_cache=False,logits_to_keep=1).logits[0,-1,:].float()
  delta=float((single-batch[i]).abs().max());assert delta<.002 and int(single.argmax())==int(batch[i].argmax());differences.append(delta)
 write_json(ROOT/'run/batch_preflight.json',dict(passed=True,max_logit_deltas=differences,top1_identical=True));del batch,enc,single;gc.collect();torch.cuda.empty_cache()
def evaluate(policy,arms,label,deadline):
 out=ROOT/'run'/label;out.mkdir(exist_ok=True);documents=read_jsonl(ROOT/'data/wmt_documents.jsonl');segments=read_jsonl(ROOT/'data/wmt_segments.jsonl');maps=read_jsonl(ROOT/'data/reconstruction_map.jsonl');bydoc={d['doc_id']:[s for s in segments if s['doc_id']==d['doc_id']] for d in documents};bank={a:{} for a in arms};batch_size=4;started=time.time()
 for start in range(0,198,8):
  docs=documents[start:start+8];work=sorted([s for d in docs for s in bydoc[d['doc_id']]],key=lambda s:(s['source_words'],s['id']))
  for arm,path in arms.items():
   reset(policy,path,verify=start==0);folder=out/arm/'batches';folder.mkdir(parents=True,exist_ok=True)
   for offset in range(0,len(work),batch_size):
    assert time.time()<deadline,'Evaluation time budget reached';rr=work[offset:offset+batch_size];p=folder/f'{start:03}_{offset:04}.json';expected=[r['id'] for r in rr]
    if p.exists():
     saved=json.loads(p.read_text());assert [r['id'] for r in saved]==expected
    else:
     enc=encode(policy,rr);eos=policy.model.generation_config.eos_token_id or policy.tokenizer.eos_token_id;eos=[eos] if isinstance(eos,int) else eos
     cfg=GenerationConfig(do_sample=False,num_beams=1,max_new_tokens=1024,repetition_penalty=1.,eos_token_id=eos,pad_token_id=policy.tokenizer.pad_token_id,use_cache=True);st=time.time()
     with torch.inference_mode():generated=policy.model.generate(**enc,generation_config=cfg)
     torch.cuda.synchronize();saved=[]
     for row,seq in zip(rr,generated):
      ids=seq[enc.input_ids.shape[1]:].tolist();hits=[i for i,t in enumerate(ids) if t in eos]
      if hits:ids=ids[:hits[0]+1]
      raw=policy.tokenizer.decode(ids,skip_special_tokens=True);saved.append(dict(row,hypothesis=extract_translation(raw),raw_output=raw,completion_tokens=len(ids),truncated=len(ids)>=1024 and ids[-1] not in eos,batch_seconds=time.time()-st,adapter_SHA256=sha256(Path(path)/'adapter_model.safetensors') if offset==0 else None))
     write_json(p,saved)
    for r in saved:assert r['id'] not in bank[arm];bank[arm][r['id']]=r
    emit(phase='WMT26_segment_inference',label=label,arm=arm,completed=len(bank[arm]),total=len(segments),documents_block=start//8)
  write_json(out/'coverage_progress.json',dict(documents_completed=min(198,start+8),segments_per_arm={a:len(z) for a,z in bank.items()}))
 reconstructed={}
 for arm,bb in bank.items():
  assert len(bb)==len(segments);rr=[]
  for doc,mapping in zip(documents,maps):
   oo=[bb[k] for k in mapping['segments']];hyp=''.join(o['separator_before']+o['hypothesis'] for o in oo)+mapping['tail'];rr.append(dict(doc_id=doc['doc_id'],domain=doc['domain'],source=doc['src_text'],reference=doc['refs']['refA'],hypothesis=hyp,truncated_segments=sum(o['truncated'] for o in oo),segment_count=len(oo)))
  (out/arm/'segment_outputs.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in bb.values()));(out/arm/'documents.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rr));reconstructed[arm]={x['doc_id']:x['hypothesis'] for x in rr}
 write_json(out/'summary.json',dict(documents_per_arm=198,segments_per_arm=len(segments),seconds=time.time()-started,truncated={a:sum(r['truncated'] for r in bb.values()) for a,bb in bank.items()}));return reconstructed,time.time()-started
def compare(documents,before,after,path):
 result=paired(documents,before,after);write_json(path,result);return result
