from pathlib import Path
import json,hashlib,collections
R=Path('/content/p18_project')
def rows(n):return [json.loads(s) for s in (R/'data'/n).read_text().splitlines() if s]
def test_frozen_data():
 p=json.loads((R/'protocol.json').read_text())
 for n,h in p['data_manifest'].items():assert hashlib.sha256((R/'data'/n).read_bytes()).hexdigest()==h
def test_disjoint_and_counts():
 a,b,c=rows('train.jsonl'),rows('dev.jsonl'),rows('final_test.jsonl');assert len(b)==len(c)==128
 for field in ['source','reference']:
  aa={r[field].casefold().strip() for r in a};bb={r[field].casefold().strip() for r in b};cc={r[field].casefold().strip() for r in c};assert not(aa&bb or aa&cc or bb&cc)
def test_fit_and_stream():
 f=rows('fit.jsonl');assert len(f)==64;assert collections.Counter(r['stratum'] for r in f)=={'technical_medium':32,'technical_long':32}
 ids=json.loads((R/'data/fit_audit_ids.json').read_text());assert len(ids)==32 and set(ids)<={r['id'] for r in f}
 order=json.loads((R/'data/exposure_order.json').read_text());assert max(collections.Counter(order).values())<=2
def test_global_target_mask_alignment():
 from mtgrpo.r0_core import collate
 x=collate([dict(prompt=[10,11],target=[20,21]),dict(prompt=[12],target=[22,23,24])],0,'cpu')
 assert x['input_ids'].tolist()==[[10,11,20,21],[12,22,23,24]] and x['labels'].tolist()==[[-100,20,21],[22,23,24]]
 assert int((x['labels']!=-100).sum())==5
