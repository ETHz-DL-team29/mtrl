from pathlib import Path
import json,time,hashlib,zipfile,torch,random,numpy as np
from mtgrpo.common import ROOT,write_json,sha256
def snapshot(checkpoint,tag):
 dest=ROOT/'snapshots'/tag;dest.mkdir(parents=True,exist_ok=False)
 files={p.relative_to(checkpoint).as_posix():sha256(p) for p in sorted(checkpoint.rglob('*')) if p.is_file()}
 archive=dest/'checkpoint.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  for n in files:z.write(checkpoint/n,n)
  z.writestr('snapshot_manifest.json',json.dumps(files,indent=2))
 data=archive.read_bytes();parts=[]
 for i,start in enumerate(range(0,len(data),6*1024**2)):
  b=data[start:start+6*1024**2];name=f'part_{i:03}.bin';(dest/name).write_bytes(b);parts.append(dict(name=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 write_json(dest/'info.json',dict(tag=tag,bytes=len(data),sha256=sha256(archive),parts=parts,files=files,unix=time.time()))
 index=ROOT/'snapshot_index.json';tags=json.loads(index.read_text()) if index.exists() else []
 tags.append(tag);write_json(index,tags)
def rng_state():return dict(python=random.getstate(),numpy=np.random.get_state(),torch=torch.get_rng_state(),cuda=torch.cuda.get_rng_state_all())
def restore_rng(r):
 random.setstate(r['python']);np.random.set_state(r['numpy']);torch.set_rng_state(r['torch']);torch.cuda.set_rng_state_all(r['cuda'])
