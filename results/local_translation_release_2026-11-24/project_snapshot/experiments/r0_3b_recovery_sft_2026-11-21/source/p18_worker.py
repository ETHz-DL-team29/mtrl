"""Owned Colab-only SFT worker; pins actor, tests, exports results, never calls RL."""
from pathlib import Path
import os,sys,time,json,subprocess,hashlib,zipfile,traceback
ROOT=Path('/content/p18_project');os.chdir(ROOT);OUT=ROOT/'run';OUT.mkdir(exist_ok=True)
os.environ.update(HF_HOME=str(ROOT/'.cache/huggingface'),HF_HUB_DISABLE_XET='1',TOKENIZERS_PARALLELISM='false',USE_TF='0',USE_FLAX='0')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def dump(p,v):
 p.parent.mkdir(exist_ok=True,parents=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,indent=2));t.replace(p)
def event(phase,**kw):dump(OUT/'progress.json',dict(phase=phase,unix=time.time(),**kw));print('P18_SETUP:'+phase,flush=True)
try:
 assert not (OUT/'worker_started.json').exists();dump(OUT/'worker_started.json',dict(unix=time.time(),source_sha256=sha(ROOT/'p18_worker.py')))
 event('installing_dependencies')
 with (OUT/'unused_torchao_removal.log').open('w') as f:subprocess.run([sys.executable,'-m','pip','uninstall','-y','torchao'],stdout=f,stderr=subprocess.STDOUT,check=True,timeout=120)
 with (OUT/'pip_install.log').open('w') as f:subprocess.run([sys.executable,'-m','pip','install','--quiet','transformers==5.22.1','peft==0.21.2','accelerate','sentencepiece','sacrebleu==2.6.0','huggingface_hub','pytest','psutil'],stdout=f,stderr=subprocess.STDOUT,check=True,timeout=900)
 (OUT/'pip_freeze.txt').write_bytes(subprocess.check_output([sys.executable,'-m','pip','freeze']))
 from huggingface_hub import HfApi,snapshot_download
 p=json.loads((ROOT/'protocol.json').read_text());model=p['actor']['base'];rev=p['actor']['revision'];assert HfApi().model_info(model,revision=rev).sha==rev
 event('download_pinned_general_Qwen3B');folder=ROOT/'models/qwen2.5-3b-instruct';snapshot_download(model,revision=rev,local_dir=folder,allow_patterns=['config.json','tokenizer*.json','special_tokens_map.json','vocab.json','merges.txt','generation_config.json','*.safetensors','*.safetensors.index.json'],max_workers=2)
 dump(OUT/'actor_model_files.json',dict(model=model,revision=rev,files={q.name:dict(bytes=q.stat().st_size,sha256=sha(q)) for q in folder.iterdir() if q.is_file()}))
 event('frozen_input_tests');v=subprocess.run([sys.executable,'-m','pytest','tests','-q'],capture_output=True,text=True);(OUT/'pytest.txt').write_text(v.stdout+v.stderr);assert v.returncode==0
 event('fit_gate_then_targeted_SFT');import p18_train;p18_train.main()
except BaseException as ex:
 dump(OUT/'error.json',dict(type=type(ex).__name__,message=str(ex),traceback=traceback.format_exc(),unix=time.time()));event('failed',error_type=type(ex).__name__)
finally:
 event('exporting')
 inventory={q.relative_to(ROOT).as_posix():sha(q) for q in (OUT/'checkpoints').rglob('*') if q.is_file()};dump(OUT/'checkpoint_file_inventory.json',inventory)
 archive=ROOT/'final_export.zip'
 # Full recovery states arrive through immutable separately verified snapshots.
 # Final archive keeps logs,data,source,original and uniquely selected adapter.
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  for folder in ['run','data','initial_adapter','selected_adapter','tests','mtgrpo']:
   for q in (ROOT/folder).rglob('*'):
    if q.is_file() and '__pycache__' not in q.parts and not q.is_relative_to(OUT/'checkpoints'):z.write(q,q.relative_to(ROOT).as_posix())
  for q in ROOT.iterdir():
   if q.is_file() and q.suffix in ['.py','.json','.txt']:z.write(q,q.name)
 dest=ROOT/'export_parts';dest.mkdir(exist_ok=True);parts=[]
 with archive.open('rb') as f:
  i=0
  while True:
   chunk=f.read(6*1024**2)
   if not chunk:break
   name=f'part_{i:03}.bin';(dest/name).write_bytes(chunk);parts.append(dict(name=name,bytes=len(chunk),sha256=hashlib.sha256(chunk).hexdigest()));i+=1
 info=dict(bytes=archive.stat().st_size,sha256=sha(archive),parts=parts,all_GPU_work_finished=True,unix=time.time(),failed=(OUT/'error.json').exists());dump(ROOT/'final_export.json',info);event('export_ready',**info)
