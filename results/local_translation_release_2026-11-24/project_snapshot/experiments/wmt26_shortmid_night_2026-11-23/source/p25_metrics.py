import numpy as np
from sacrebleu.metrics import CHRF,BLEU
def paired(documents,before,after,repetitions=2000):
 assert len(documents)==198 and set(before)==set(after)=={r['doc_id'] for r in documents}
 result=dict(n=198,subsets={},replicates=repetitions,bootstrap_unit='Original document,stratified within domain',not_official_human_rank=True)
 rng=np.random.default_rng(2026112325);metrics=dict(chrfpp=CHRF(word_order=2),bleu=BLEU())
 for subset in ['overall','news','social','software','speech']:
  dd=[r for r in documents if subset=='overall' or r['domain']==subset];refs=[[r['refs']['refA'] for r in dd]];result['subsets'][subset]=dict(n=len(dd));groups=[[i for i,r in enumerate(dd) if r['domain']==dom] for dom in sorted({r['domain'] for r in dd})]
  for key,metric in metrics.items():
   hh=[[bank[r['doc_id']] for r in dd] for bank in [before,after]];values=[metric.corpus_score(h,refs).score for h in hh];stats=[np.asarray(metric._extract_corpus_statistics(h,refs),dtype=float) for h in hh];boot=[]
   for _ in range(repetitions):
    jj=np.concatenate([rng.choice(g,size=len(g),replace=True) for g in groups]);boot.append(metric._compute_score_from_stats(stats[1][jj].sum(0).tolist()).score-metric._compute_score_from_stats(stats[0][jj].sum(0).tolist()).score)
   result['subsets'][subset][key]=dict(before=values[0],after=values[1],delta=values[1]-values[0],delta95CI=np.percentile(boot,[2.5,97.5]).tolist())
 result['signatures']={k:str(m.get_signature()) for k,m in metrics.items()};return result
