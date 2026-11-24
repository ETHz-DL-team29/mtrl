"""Pure schedule, whole-example budgeting and registered development selection."""
import math

def learning_rate(tokens,peak=1e-5):
 return peak*(.5+.5*.5*(1+math.cos(math.pi*min(1.,tokens/4000000))))

def timing_target(consumed,step_records,available_train_seconds,stream_tokens,grid=(1000000,1500000,2000000,2500000,3000000,3500000,4000000)):
 import numpy as np
 assert available_train_seconds>=0
 rates=[r['group_target_tokens']/r['seconds'] for r in step_records[20:] if r['seconds']>0]
 if not rates:rates=[r['group_target_tokens']/r['seconds'] for r in step_records if r['seconds']>0]
 assert rates
 conservative=float(np.percentile(rates,25))
 cap=min(4000000,stream_tokens,consumed+.8*conservative*available_train_seconds)
 eligible=[n for n in grid if consumed<n and n<=cap+512]
 return dict(target_tokens=min(max(eligible),stream_tokens) if eligible else None,p25_step_tokens_per_second=conservative,projected_safe_token_cap=cap,remaining_train_seconds=available_train_seconds,safety_factor=.8,quality_used=False)

def next_group(encoded,order,cursor,remaining,effective=32):
 group=[];end=cursor
 while end<len(order) and len(group)<effective:
  row=encoded[order[end]];size=len(row['target'])
  if size>remaining:break
  group.append(row);remaining-=size;end+=1
 return group,end

def eligible(metrics,baseline):
 return metrics['by_stratum']['general']['chrfpp']>=baseline['by_stratum']['general']['chrfpp']-1.5 and metrics['failures']<=baseline['failures']+2

def choose(candidates,reviews):
 baseline=candidates[0];assert baseline['target_tokens']==0
 ok=[]
 for c in candidates:
  rev=reviews.get(c['tag'])
  if not rev or not rev.get('labels_locked') or rev.get('adapter_sha256')!=c['adapter_sha256']:continue
  assert rev['technical_sources']==24 and rev['greedy_sources']==32
  if eligible(c['metrics'],baseline['metrics']):ok.append((c,rev))
 if not ok:return dict(baseline,selection_reason='No reviewed eligible candidate; original A fallback')
 maximum=max(r['coverage_P'] for c,r in ok)
 tied=[(c,r) for c,r in ok if r['coverage_P']>=maximum-1]
 c,r=min(tied,key=lambda cr:(-cr[1]['greedy_P'],-cr[0]['metrics']['technical_medium_long_chrfpp'],cr[0]['target_tokens']))
 return dict(c,review_summary=r,selection_reason='Reviewed eligible maximum-coverage tie set,then greedy P,technical medium/long CHRF,earlier checkpoint')

def metric_plateau(candidates):
 if len(candidates)<4:return False
 recent=candidates[-3:]
 if recent[-1]['target_tokens']-recent[0]['target_tokens']<990000:return False
 first=recent[0]['metrics'];rest=[c['metrics'] for c in recent[1:]]
 return max(m['technical_chrfpp'] for m in rest)-first['technical_chrfpp']<.3 and first['technical_nll']-min(m['technical_nll'] for m in rest)<.01

def confirmed_plateau(candidates,reviews):
 if not metric_plateau(candidates):return False
 recent=candidates[-3:];rr=[]
 for c in recent:
  r=reviews.get(c['tag'])
  if not r or not r.get('labels_locked') or r.get('adapter_sha256')!=c['adapter_sha256']:return False
  rr.append(r)
 return max(r['coverage_P'] for r in rr[1:])<=rr[0]['coverage_P'] and max(r['greedy_P'] for r in rr[1:])<=rr[0]['greedy_P']
