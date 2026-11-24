from pathlib import Path
import subprocess,sys,time,json,hashlib,zipfile,os
ROOT=Path('/content/t6_project');os.chdir(ROOT);started=time.time()
with (ROOT/'trainer.log').open('w') as f:
 p=subprocess.Popen([sys.executable,'-u',str(ROOT/'t6_train.py')],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
 (ROOT/'trainer_pid.json').write_text(json.dumps(dict(pid=p.pid,unix=started)))
 try:code=p.wait(timeout=9600)
 except subprocess.TimeoutExpired:
  p.terminate()
  try:code=p.wait(timeout=180)
  except subprocess.TimeoutExpired:p.kill();code=p.wait()
(ROOT/'worker_exit.json').write_text(json.dumps(dict(returncode=code,unix=time.time(),seconds=time.time()-started)))
external=[];skip=set();last=json.loads((ROOT/'run/last_checkpoint.json').read_text())['tag'] if (ROOT/'run/last_checkpoint.json').exists() else None
for ack in sorted((ROOT/'snapshot_ack').glob('*.json')):
 v=json.loads(ack.read_text());info=json.loads((ROOT/'snapshots'/v['tag']/'info.json').read_text())
 assert v['sha256']==info['sha256'] and v['bytes']==info['bytes'] and v['durable_verified'];external.append(v)
 if v['tag']!=last:skip.add(f"run/checkpoints/{v['tag']}/optimizer_rng.pt")
(ROOT/'external_checkpoint_archives.json').write_text(json.dumps(external,indent=2))
archive=ROOT/'t6_export.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for folder in ['run','data','tests','mtgrpo','initial_adapter']:
  for f in sorted((ROOT/folder).rglob('*')):
   if f.is_file() and not any(k in f.parts for k in ['__pycache__','.pytest_cache']):
    rel=f.relative_to(ROOT).as_posix()
    if rel not in skip:z.write(f,rel)
 for f in sorted(ROOT.iterdir()):
  if f.is_file() and (f.suffix in ['.py','.json'] or f.name in ['requirements-colab.txt','trainer.log','unit_checks.log']):
   if f.name not in ['export_info.json','bundle_manifest.json']:z.write(f,f.name)
data=archive.read_bytes();parts=[];dest=ROOT/'export_parts';dest.mkdir(exist_ok=True)
for i,start in enumerate(range(0,len(data),6*1024**2)):
 b=data[start:start+6*1024**2];name=f'part_{i:03}.bin';(dest/name).write_bytes(b);parts.append(dict(name=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
tmp=ROOT/'export_info.json.tmp';tmp.write_text(json.dumps(dict(path=str(archive),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),parts=parts,unix=time.time(),external_checkpoint_archives=external)));tmp.replace(ROOT/'export_info.json')
