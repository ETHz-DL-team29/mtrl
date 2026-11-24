"""Pinned MetricX24 reference scoring; source-only actor never receives reference."""
import torch,time,json
from pathlib import Path
from transformers import AutoTokenizer,MT5ForConditionalGeneration
ROOT=Path('/content/p25_project')
class Scorer:
 def __init__(self):
  self.tokenizer=AutoTokenizer.from_pretrained(ROOT/'models/metricx-tokenizer',local_files_only=True,use_fast=False)
  self.model,info=MT5ForConditionalGeneration.from_pretrained(ROOT/'models/metricx-24-hybrid-large',local_files_only=True,dtype=torch.bfloat16,output_loading_info=True)
  assert not any(info.get(k) for k in ['missing_keys','unexpected_keys','mismatched_keys','error_msgs'])
  self.model.to('cuda').eval();self.device='cuda'
 def score(self,source,hyps,reference):
  answer=[]
  for start in range(0,len(hyps),2):
   texts=[f'source: {source} candidate: {h} reference: {reference}' for h in hyps[start:start+2]];encoded=[self.tokenizer(t,add_special_tokens=True)['input_ids'] for t in texts]
   for e in encoded:assert e[-1]==self.tokenizer.eos_token_id
   valid=[i for i,e in enumerate(encoded) if len(e)<=1536];temp={}
   if valid:
    ids=[encoded[i][:-1] for i in valid];inputs=self.tokenizer.pad(dict(input_ids=ids),padding=True,return_tensors='pt').to(self.device);torch.cuda.synchronize();st=time.perf_counter()
    with torch.inference_mode():out=self.model(**inputs,decoder_input_ids=torch.zeros((len(ids),1),dtype=torch.long,device=self.device),use_cache=False);raw=out.logits[:,0,250089].float();assert torch.isfinite(raw).all();scores=raw.clamp(0,25).tolist();rr=raw.tolist()
    torch.cuda.synchronize();seconds=time.perf_counter()-st
    for j,i in enumerate(valid):temp[i]=dict(error=scores[j],raw=rr[j],input_tokens=len(encoded[i])-1,truncated=False,batch_seconds=seconds)
   answer.extend(temp.get(i,dict(error=None,raw=None,input_tokens=len(e)-1,truncated=True,batch_seconds=0)) for i,e in enumerate(encoded))
  return answer
 def close(self):
  import gc
  del self.model;gc.collect();torch.cuda.empty_cache()
