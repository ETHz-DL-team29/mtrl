"""Registered checkpoint choice, independent of model state or final outputs."""
from sacrebleu.metrics import CHRF,BLEU
WEIGHTS=dict(general=.25,technical_short=.05,technical_medium=.35,technical_long=.35)
def score_records(records):
 result={}
 for s in WEIGHTS:
  r=[x for x in records if x['stratum']==s];assert r
  result[s]=dict(n=len(r),chrfpp=CHRF(word_order=2).corpus_score([x['hypothesis'] for x in r],[[x['reference'] for x in r]]).score,
   bleu=BLEU().corpus_score([x['hypothesis'] for x in r],[[x['reference'] for x in r]]).score)
 return dict(by_stratum=result,weighted_chrfpp=sum(WEIGHTS[s]*result[s]['chrfpp'] for s in WEIGHTS),failures=sum(not x['gate']['gate'] or x.get('repetition',False) for x in records))
def eligible(metrics,baseline):
 return metrics['by_stratum']['general']['chrfpp']>=baseline['by_stratum']['general']['chrfpp']-1.5 and metrics['failures']<=baseline['failures']+2
def choose(candidates):
 baseline=candidates[0]['metrics'];assert candidates[0]['target_tokens']==0
 ok=[x for x in candidates if eligible(x['metrics'],baseline)]
 high=max(x['metrics']['weighted_chrfpp'] for x in ok)
 tied=[x for x in ok if x['metrics']['weighted_chrfpp']>=high-.1]
 return min(tied,key=lambda x:(x['metrics']['technical_nll'],x['target_tokens']))
