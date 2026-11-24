from pathlib import Path
import json,zipfile,hashlib,time
from mtgrpo.common import ROOT,write_json
def make_snapshot(checkpoint,tag,include_optimizer=False):
 dest=ROOT/'snapshots'/str(tag);dest.mkdir(parents=True,exist_ok=False);archive=dest/'checkpoint.zip'
 files=[p for p in sorted(checkpoint.rglob('*')) if p.is_file() and (include_optimizer or p.name!='optimizer_rng.pt')]
 manifest={p.relative_to(checkpoint).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  for p in files:z.write(p,p.relative_to(checkpoint).as_posix())
  z.writestr('snapshot_manifest.json',json.dumps(manifest,indent=2))
 data=archive.read_bytes();parts=[]
 for i,start in enumerate(range(0,len(data),6*1024**2)):
  b=data[start:start+6*1024**2];name=f'part_{i:03}.bin';(dest/name).write_bytes(b);parts.append(dict(name=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 write_json(dest/'info.json',dict(step=tag,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),parts=parts,files=manifest,optimizer_included=include_optimizer,unix=time.time()))
