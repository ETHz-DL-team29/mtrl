import copy,types,torch
from t6_core import choose,eligible
from t6_update import update
from mtgrpo.r0_train import loss_sum
def candidate(tag,tokens,score,general=40,failures=0,nll=2):
 return dict(tag=tag,target_tokens=tokens,metrics=dict(weighted_chrfpp=score,by_stratum=dict(general=dict(chrfpp=general)),failures=failures,technical_nll=nll))
def test_selection_rejects_general_regression_even_for_large_technical_score():
 base=candidate('R0',0,30);bad=candidate('bad',400000,50,general=38)
 assert choose([base,bad])==base
def test_selection_tie_rule_and_structural_guard():
 base=candidate('R0',0,30);a=candidate('100k',100000,35,nll=2);b=candidate('200k',200000,35.05,nll=2.2);c=candidate('400k',400000,40,failures=3)
 assert choose([base,a,b,c])==a
class Toy(torch.nn.Module):
 def __init__(self):super().__init__();self.e=torch.nn.Embedding(13,7);self.l=torch.nn.Linear(7,13)
 def forward(self,input_ids,attention_mask,use_cache=False,logits_to_keep=0):return types.SimpleNamespace(logits=self.l(self.e(input_ids))[:,-logits_to_keep:,:])
def test_target_only_shift_and_microbatch_equivalence():
 torch.manual_seed(7);model=Toy();other=copy.deepcopy(model);rows=[dict(prompt=[1,2,3],target=[4,5,12]),dict(prompt=[2],target=[7,12])];tok=types.SimpleNamespace(pad_token_id=0)
 manual=0.
 for r in rows:
  ids=torch.tensor([r['prompt']+r['target']]);logits=model(ids,torch.ones_like(ids),logits_to_keep=len(ids[0])).logits[0,len(r['prompt'])-1:-1]
  manual+=torch.nn.functional.cross_entropy(logits,torch.tensor(r['target']),reduction='sum')
 assert torch.allclose(loss_sum(model,rows,tok,'cpu'),manual,atol=1e-6)
 policies=[types.SimpleNamespace(model=m,tokenizer=tok,device='cpu') for m in [model,other]]
 for p,mb in zip(policies,[1,2]):update(p,rows,torch.optim.SGD(p.model.parameters(),lr=.01),mb,lambda:None,lambda r:None)
 assert all(torch.allclose(a,b,atol=1e-7) for a,b in zip(model.parameters(),other.parameters()))
def test_optimizer_and_rng_resume_exact(tmp_path):
 torch.manual_seed(11);m=Toy();o=torch.optim.AdamW(m.parameters(),lr=1e-3)
 def one(model,opt):
  opt.zero_grad();x=torch.randint(0,13,(2,4));loss=model.e(x).square().mean();loss.backward();opt.step()
 one(m,o);state=dict(model=copy.deepcopy(m.state_dict()),optimizer=copy.deepcopy(o.state_dict()),rng=torch.get_rng_state())
 torch.save(state,tmp_path/'state.pt');one(m,o);expected=copy.deepcopy(m.state_dict())
 saved=torch.load(tmp_path/'state.pt',weights_only=True);other=Toy();other.load_state_dict(saved['model']);op=torch.optim.AdamW(other.parameters(),lr=1e-3);op.load_state_dict(saved['optimizer']);torch.set_rng_state(saved['rng']);one(other,op)
 assert all(torch.equal(v,other.state_dict()[k]) for k,v in expected.items())
def test_snapshot_manifest_and_chunks(tmp_path,monkeypatch):
 import t6_store,json,hashlib,zipfile
 monkeypatch.setattr(t6_store,'ROOT',tmp_path);p=tmp_path/'checkpoint';p.mkdir();(p/'adapter.bin').write_bytes(b'known-weights');(p/'optimizer_rng.pt').write_bytes(b'known-state')
 t6_store.snapshot(p,'t100000');dest=tmp_path/'snapshots/t100000';info=json.loads((dest/'info.json').read_text());payload=b''.join((dest/x['name']).read_bytes() for x in info['parts'])
 assert hashlib.sha256(payload).hexdigest()==info['sha256']
 with zipfile.ZipFile(dest/'checkpoint.zip') as z:
  assert z.testzip() is None and all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in info['files'].items())
