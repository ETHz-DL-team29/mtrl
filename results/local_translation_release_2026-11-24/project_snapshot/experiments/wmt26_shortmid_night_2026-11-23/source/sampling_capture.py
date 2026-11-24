"""Capture actual processed sampling log-probs without retaining T*G*V logits.

Generation uses temperature1 internally; the custom processor applies the
registered temperature once. The stopping criterion gathers only the chosen
token and drops the vocabulary-sized buffer after each decode step.
This adds monitoring, not an importance-sampling correction or policy update.
"""
import torch
from transformers import GenerationConfig,LogitsProcessor,StoppingCriteria

class CaptureProcessor(LogitsProcessor):
 def __init__(self,book,temperature):
  if temperature<=0:raise ValueError('Temperature must be positive')
  self.book=book;self.temperature=temperature
 def __call__(self,input_ids,scores):
  if 'scores' in self.book:raise RuntimeError('Previous generation score was not consumed')
  scaled=scores.float()/self.temperature
  self.book['scores']=scaled.detach()
  return scaled

class CaptureCriterion(StoppingCriteria):
 def __init__(self,book):self.book=book
 def __call__(self,input_ids,scores,**kwargs):
  raw=self.book.pop('scores');selected=input_ids[:,-1]
  lp=raw.gather(1,selected[:,None]).squeeze(1)-torch.logsumexp(raw,dim=-1)
  self.book.setdefault('selected_logps',[]).append(lp.detach())
  return torch.zeros(input_ids.shape[0],dtype=torch.bool,device=input_ids.device)

def captured_generate(model,prompt,*,g,eos,pad,temperature=.7,maximum=320):
 book={};processor=CaptureProcessor(book,temperature);criterion=CaptureCriterion(book)
 config=GenerationConfig(max_new_tokens=maximum,do_sample=True,num_return_sequences=g,
  num_beams=1,temperature=1.,top_p=1.,top_k=0,repetition_penalty=1.,
  eos_token_id=eos,pad_token_id=pad,use_cache=True,output_scores=False,return_dict_in_generate=False)
 model.eval()
 with torch.no_grad():
  seq=model.generate(input_ids=prompt,attention_mask=torch.ones_like(prompt),generation_config=config,
   logits_processor=[processor],stopping_criteria=[criterion])
 assert 'scores' not in book and len(book['selected_logps'])==seq.shape[1]-prompt.shape[1]
 return seq,torch.stack(book['selected_logps'],dim=1)
