from pathlib import Path
import sys,os,time,json,subprocess,traceback,importlib.metadata
ROOT=Path('/content/t6_project');os.chdir(ROOT)
os.environ.update(HF_HOME=str(ROOT/'.cache/huggingface'),TOKENIZERS_PARALLELISM='false',OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='1')
def phase(name,**v):
 (ROOT/'setup_progress.json').write_text(json.dumps(dict(phase=name,unix=time.time(),**v)));print(name,flush=True)
def run(label,cmd):
 phase(label)
 with (ROOT/(label+'.log')).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError(label+' failed; inspect saved log')
try:
 from packaging.version import Version
 try:
  if Version(importlib.metadata.version('torchao'))<Version('0.16.0'):run('remove_optional_old_torchao',[sys.executable,'-m','pip','uninstall','-y','torchao'])
 except importlib.metadata.PackageNotFoundError:pass
 run('dependencies',[sys.executable,'-m','pip','install','-r',str(ROOT/'requirements-colab.txt')])
 phase('downloads')
 from huggingface_hub import snapshot_download
 for name,rev,path,allow in [('Qwen/Qwen3.5-0.8B','2fc06364715b967f1860aea9cf38778875588b17','qwen3.5-0.8b',['*.json','*.jinja','*.txt','*.safetensors','LICENSE']),('google/metricx-24-hybrid-large-v2p6','51e875ba5c525c81627cfd135ee10f43c87dce00','metricx-24-hybrid-large',['config.json','pytorch_model.bin','model.safetensors']),('google/mt5-xl','63fc6450d80515b48e026b69ef2fbbd426433e84','metricx-tokenizer',['spiece.model','tokenizer*.json','special_tokens_map.json','config.json'])]:
  snapshot_download(name,revision=rev,local_dir=ROOT/'models'/path,allow_patterns=allow,max_workers=4);phase('downloaded_'+path)
 run('unit_checks',[sys.executable,'-m','pytest','tests','-q'])
 phase('complete');(ROOT/'setup_done.json').write_text(json.dumps(dict(unix=time.time())))
except BaseException as e:
 (ROOT/'setup_error.json').write_text(json.dumps(dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc(),unix=time.time())));raise
