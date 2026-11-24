"""Frozen official MetricX-24 QE/reference protocols; FP32 regression."""
import time,torch,json
from .models import METRICX_DIR,METRICX_TOKENIZER_DIR,synchronize
from .common import ROOT,write_json,append_jsonl

class Scorer:
    def __init__(self,device='cuda',maximum=1536):
        from transformers import AutoTokenizer,MT5ForConditionalGeneration
        self.device=device;self.maximum=maximum
        self.tokenizer=AutoTokenizer.from_pretrained(METRICX_TOKENIZER_DIR,local_files_only=True,use_fast=False)
        self.model,info=MT5ForConditionalGeneration.from_pretrained(METRICX_DIR,local_files_only=True,dtype=torch.float32,output_loading_info=True)
        bad={k:info.get(k) for k in ['missing_keys','unexpected_keys','mismatched_keys','error_msgs'] if info.get(k)}
        if bad:raise RuntimeError(str(bad))
        self.model.to(device).eval()
    def score(self,source,hypotheses,reference,mode):
        if mode=='ensemble':
            ref=self.score(source,hypotheses,reference,'reference');qe=self.score(source,hypotheses,reference,'qe')
            return [dict(score=.75*a['score']+.25*b['score'],raw_score=.75*a['raw_score']+.25*b['raw_score'],reference_component=a,qe_component=b,input_tokens=a['input_tokens']+b['input_tokens'],truncated=a['truncated'] or b['truncated'],scoring_batch_seconds=a['scoring_batch_seconds']+b['scoring_batch_seconds']) for a,b in zip(ref,qe)]
        assert mode in ['qe','reference'];results=[]
        # Small deterministic batch reduces padding and peak FP32 attention memory.
        for start in range(0,len(hypotheses),2):
            texts=[f'source: {source} candidate: {h}'+(f' reference: {reference}' if mode=='reference' else '') for h in hypotheses[start:start+2]]
            encoded=[self.tokenizer(t,add_special_tokens=True)['input_ids'] for t in texts]
            ids=[x[:self.maximum][:-1] for x in encoded]
            inputs=self.tokenizer.pad(dict(input_ids=ids),padding=True,return_tensors='pt').to(self.device)
            synchronize(self.device);st=time.perf_counter()
            with torch.inference_mode():
                out=self.model(**inputs,decoder_input_ids=torch.zeros((len(ids),1),dtype=torch.long,device=self.device),use_cache=False)
                raw=out.logits[:,0,250089].float()
                if not torch.isfinite(raw).all():raise FloatingPointError('Non-finite MetricX before clipping')
                scores=raw.clamp(0,25).tolist();raw=raw.tolist()
            synchronize(self.device);seconds=time.perf_counter()-st
            results.extend(dict(score=s,raw_score=v,input_tokens=len(x),truncated=len(e)>self.maximum,scoring_batch_seconds=seconds) for s,v,x,e in zip(scores,raw,ids,encoded))
        return results

    def close(self):
        import gc
        del self.model
        gc.collect()
        if torch.cuda.is_available():torch.cuda.empty_cache()

def calibration(scorer,out):
    controls=json.loads((ROOT/'data/controls.json').read_text());old=json.loads((ROOT/'data/historical_controls.json').read_text())
    cases=controls['cases']+[dict(c,id='historical-'+c['case'],split='historical_regression',controls=[dict(x,correct=x['expected']=='meaning_preserving') for x in c['controls']]) for c in old['cases']]
    records=[]
    for case in cases:
        for mode in ['qe','reference']:
            scores=scorer.score(case['source'],[c['hypothesis'] for c in case['controls']],case['reference'],mode)
            row=dict(case=case['id'],source=case['source'],reference=case['reference'],split=case['split'],mode=mode,controls=[dict(c,**s) for c,s in zip(case['controls'],scores)])
            append_jsonl(out/'calibration_scores.jsonl',row);records.append(row)
        print('R3_CALIBRATION',case['id'],flush=True)
    summaries={}
    for split in ['calibration','validation','historical_regression']:
        summaries[split]={}
        for mode in ['qe','reference']:
            pairs=[]
            for row in records:
                if row['split']!=split or row['mode']!=mode:continue
                for good in row['controls']:
                    if not good['correct']:continue
                    for bad in row['controls']:
                        if bad['correct']:continue
                        pairs.append(dict(case=row['case'],positive_kind=good['kind'],negative_kind=bad['kind'],margin=bad['score']-good['score'],passed=good['score']+.01<bad['score']))
            para=[p for p in pairs if p['positive_kind']=='paraphrase']
            summaries[split][mode]=dict(pairs=len(pairs),accuracy=sum(p['passed'] for p in pairs)/len(pairs),paraphrase_accuracy=sum(p['passed'] for p in para)/len(para),failures=[p for p in pairs if not p['passed']])
    # Prespecified ordering: prefer paraphrase ordering, then all comparisons;
    # the validation partition never selects the mode or modifies any weight.
    cal=summaries['calibration']
    selected=max(['reference','qe'],key=lambda m:(cal[m]['paraphrase_accuracy'],cal[m]['accuracy']))
    valid=summaries['validation'][selected]
    passes=all(summaries[s][selected]['accuracy']>=.8 and summaries[s][selected]['paraphrase_accuracy']>=.7 for s in ['calibration','validation'])
    # Also verify batch padding does not materially change regression readout.
    probe=cases[0];hyps=[x['hypothesis'] for x in probe['controls'][:2]]
    bat=scorer.score(probe['source'],hyps,probe['reference'],selected)
    one=[scorer.score(probe['source'],[h],probe['reference'],selected)[0] for h in hyps]
    parity=max(abs(a['score']-b['score']) for a,b in zip(bat,one));passes=passes and parity<.02
    decision=dict(selected_mode=selected,passes=passes,selection='Calibration-only lexicographic paraphrase accuracy then total accuracy; tie reference',thresholds=dict(total_accuracy=.8,paraphrase_accuracy=.7,strict_margin=.01,batch_parity_tolerance=.02),batch_single_max_delta=parity,summaries=summaries,frozen_unix=time.time(),reward='1 - clip(MetricX,0,25)/25; plus prespecified soft length penalty',limitations=controls['authoring'])
    write_json(out/'reward_decision.json',decision)
    if not passes:raise RuntimeError('Prespecified reward sanity gates failed; no RL update permitted')
    return decision

def calibration_v2(scorer,out):
    """Fixed V2 ensemble, tested against NEW validation after V1 failure.

    No weight search or selection on either validation partition occurs here.
    V1's original score files and failed gates remain preserved separately.
    """
    original=json.loads((ROOT/'data/controls.json').read_text())
    new=json.loads((ROOT/'data/controls_v2_validation.json').read_text())
    cases=[c for c in original['cases'] if c['split']=='calibration']+new['cases']
    results=[]
    for case in cases:
        scores=scorer.score(case['source'],[c['hypothesis'] for c in case['controls']],case['reference'],'ensemble')
        row=dict(case=case['id'],source=case['source'],reference=case['reference'],split=case['split'],mode='ensemble',controls=[dict(c,**s) for c,s in zip(case['controls'],scores)])
        append_jsonl(out/'calibration_scores.jsonl',row);results.append(row);print('R3_V2_CALIBRATION',case['id'],flush=True)
    summaries={}
    for split in ['calibration','validation_v2']:
        pairs=[]
        for row in results:
            if row['split']!=split:continue
            for good in row['controls']:
                if not good['correct']:continue
                for bad in row['controls']:
                    if bad['correct']:continue
                    pairs.append(dict(case=row['case'],positive_kind=good['kind'],negative_kind=bad['kind'],margin=bad['score']-good['score'],passed=good['score']+.01<bad['score']))
        para=[p for p in pairs if p['positive_kind']=='paraphrase']
        summaries['validation' if split=='validation_v2' else split]={'ensemble':dict(pairs=len(pairs),accuracy=sum(p['passed'] for p in pairs)/len(pairs),paraphrase_accuracy=sum(p['passed'] for p in para)/len(para),failures=[p for p in pairs if not p['passed']])}
    c=cases[-1];hyps=[x['hypothesis'] for x in c['controls'][:2]]
    bat=scorer.score(c['source'],hyps,c['reference'],'ensemble');one=[scorer.score(c['source'],[h],c['reference'],'ensemble')[0] for h in hyps]
    parity=max(abs(a['score']-b['score']) for a,b in zip(bat,one))
    passes=all(summaries[s]['ensemble']['accuracy']>=.8 and summaries[s]['ensemble']['paraphrase_accuracy']>=.7 for s in summaries) and parity<.02
    decision=dict(version=2,selected_mode='ensemble',weights=dict(reference=.75,qe=.25),passes=passes,batch_single_max_delta=parity,summaries=summaries,frozen_unix=time.time(),new_validation_registered_unix=new['registered_unix'],selection='Fixed ensemble selected on V1 calibration20 only; V1 validation diagnostic only; V2 new validation20 does not tune anything.',thresholds=dict(total_accuracy=.8,paraphrase_accuracy=.7,strict_margin=.01,batch_parity_tolerance=.02),limitations=['AI authored controls, no native certification.','Engineering sanity gate, not a guarantee of reward correctness.','V1 failure is retained in a separate durable archive.'])
    write_json(out/'reward_decision.json',decision)
    if not passes:raise RuntimeError('V2 fixed-ensemble sanity gates failed; no RL update permitted')
    return decision

def exploratory_reference_protocol(scorer,out):
    """Explicitly retain failed calibration; never relabel it as passed.

    V3 is a disclosed, nonconfirmatory failure-mode/learnability pilot. The
    original user-requested standard DAPO diagnostic uses the simple reference
    MetricX mode, not another validation-tuned ensemble. No new gate is fitted.
    """
    import shutil
    protocol=json.loads((ROOT/'protocol.json').read_text())
    assert protocol.get('version')==3 and protocol.get('classification')=='exploratory_known_noisy_reward'
    audit=out/'calibration_audit';audit.mkdir(exist_ok=True)
    for attempt in ['v1_calibration_failed','v2_calibration_failed']:
        src=ROOT/'attempts'/attempt/'run'
        assert src.exists()
        old=json.loads((src/'reward_decision.json').read_text());assert old['passes'] is False
        for name in ['reward_decision.json','calibration_scores.jsonl','error.json']:
            shutil.copy2(src/name,audit/(attempt+'_'+name))
    v1=json.loads((audit/'v1_calibration_failed_reward_decision.json').read_text())
    decision=dict(v1,version=3,selected_mode='reference',passes=False,
        exploratory_run=True,formal_efficiency_baseline_eligible=False,
        interpretation='Original80/70 gates remain failed. V3 explicitly tests learnability/reward exploitation under known-noisy reference MetricX; not a calibrated or confirmatory comparison baseline.',
        frozen_unix=time.time())
    write_json(out/'reward_decision.json',decision);return decision
