"""Foreground continuation, persistent source/data/checkpoints, no original overwrite."""
import pathlib,os,sys,json,time,hashlib,zipfile,subprocess,threading,signal,shutil
from google.colab import drive
if not pathlib.Path('/content/drive/MyDrive').is_dir():drive.mount('/content/drive',timeout_ms=300000)
ROOT=pathlib.Path('/content/drive/MyDrive/deep learning project/r1_sft_2026-11-12')
ROOT.mkdir(parents=True,exist_ok=True)
import psutil
existing=[p.info['pid'] for p in psutil.process_iter(['pid','cmdline']) if 'mtgrpo.r1_train' in (p.info['cmdline'] or [])]
assert not existing,f'An owned R1 trainer is already active: {existing}; inspect instead of starting another'
SOURCE_SHA='663360a350ea59b5d411e697ae395441a8e53d03f2882127de79b32c7d7d4a04';bundle=ROOT/'inputs'/(SOURCE_SHA+'.zip')
assert hashlib.sha256(bundle.read_bytes()).hexdigest()==SOURCE_SHA
PROJECT=pathlib.Path('/content/r1_sft_project');PROJECT.mkdir(exist_ok=True)
with zipfile.ZipFile(bundle) as z:
    assert all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts for n in z.namelist());z.extractall(PROJECT)
old_bundle=ROOT.parent/'g8_readiness_2026-11-12/inputs/bd86be2d13bf9e202693c388354284ea3f14462203f8954cf97e402bbe6283dc.zip'
assert hashlib.sha256(old_bundle.read_bytes()).hexdigest()=='bd86be2d13bf9e202693c388354284ea3f14462203f8954cf97e402bbe6283dc'
initial=PROJECT/'initial_adapter';initial.mkdir(exist_ok=True)
with zipfile.ZipFile(old_bundle) as z:
    for name in ['adapter_config.json','adapter_model.safetensors']:(initial/name).write_bytes(z.read('old_adapter/'+name))
assert hashlib.sha256((initial/'adapter_model.safetensors').read_bytes()).hexdigest()=='e32ae12d4ece8416352a6920d422766a5cf00e7b29ae5a528efda4dc4645a411'
preserved=ROOT.parent/'r0_2026-11-11/formal_100k/checkpoint-000176-000175027/adapter/adapter_model.safetensors'
assert hashlib.sha256(preserved.read_bytes()).hexdigest()=='81b369a5f6c6343c160c99c4d3271f2ecb63781363b05e9c89e7b2703b77785f'
os.chdir(PROJECT);os.environ.update(PYTHONUNBUFFERED='1',OPENBLAS_NUM_THREADS='1',TOKENIZERS_PARALLELISM='false')
import torch
assert torch.cuda.is_available(),'GPU runtime required'
write_metadata=dict(source_sha256=SOURCE_SHA,root=str(ROOT),gpu=torch.cuda.get_device_name(0),torch=torch.__version__,started_unix=time.time())
(ROOT/'runner_metadata.json').write_text(json.dumps(write_metadata,indent=2))
print('R1_SESSION:'+json.dumps(write_metadata),flush=True)
logs=ROOT/'logs';logs.mkdir(exist_ok=True)
def run(label,command):
    stop=threading.Event();started=time.time()
    path=logs/(label+'_'+str(int(started))+'.log')
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1,cwd=PROJECT,env=os.environ.copy(),start_new_session=True)
    def pulse():
        while not stop.wait(40):
            status={}
            try:status=json.loads((ROOT/'formal/progress.json').read_text())
            except (OSError,ValueError):pass
            print('R1_HEARTBEAT:'+json.dumps(dict(unix=time.time(),phase=label,step=status.get('step'),tokens=status.get('target_tokens'))),flush=True)
    watcher=threading.Thread(target=pulse,daemon=True);watcher.start()
    try:
        with path.open('a',buffering=1) as f:
            for line in process.stdout:f.write(line);print(line,end='',flush=True)
        if process.wait():raise subprocess.CalledProcessError(process.returncode,command)
    except BaseException:
        try:os.killpg(process.pid,signal.SIGTERM)
        except ProcessLookupError:pass
        raise
    finally:stop.set();watcher.join(timeout=2)
    print('R1_PHASE_DONE:'+json.dumps(dict(phase=label,seconds=time.time()-started)),flush=True)
import importlib.metadata
from packaging.requirements import Requirement
from packaging.version import Version
try:
    if Version(importlib.metadata.version('torchao'))<Version('0.16.0'):run('remove_optional_torchao',[sys.executable,'-m','pip','uninstall','-y','torchao'])
except importlib.metadata.PackageNotFoundError:pass
missing=[]
for line in (PROJECT/'requirements-colab.txt').read_text().splitlines():
    if not line.strip() or line.startswith('#'):continue
    req=Requirement(line)
    try:ok=Version(importlib.metadata.version(req.name)) in req.specifier
    except importlib.metadata.PackageNotFoundError:ok=False
    if not ok:missing.append(line)
if missing:run('dependencies',[sys.executable,'-m','pip','install',*missing])
run('unit_checks',[sys.executable,'-m','unittest','discover','-s','tests','-v'])
download=PROJECT/'download_policy.py'
download.write_text("from huggingface_hub import snapshot_download\nfrom pathlib import Path\nsnapshot_download('Qwen/Qwen3.5-0.8B',revision='2fc06364715b967f1860aea9cf38778875588b17',local_dir=Path(__file__).parent/'models/qwen3.5-0.8b',allow_patterns=['*.json','*.jinja','*.txt','*.safetensors','LICENSE'],max_workers=4)\n")
run('policy_download',[sys.executable,str(download)])
formal=ROOT/'formal'
summary=json.loads((formal/'summary.json').read_text()) if (formal/'summary.json').exists() else None
if not summary or not summary['completed']:
    command=[sys.executable,'-m','mtgrpo.r1_train','--run-dir',str(formal),'--initial-adapter',str(initial),'--data-dir',str(PROJECT/'data')]
    if (formal/'last.json').exists():command.append('--resume')
    run('sft_continuation',command)
summary=json.loads((formal/'summary.json').read_text())
assert summary['improved_over_warmstart'],'No selected improvement; preserve outputs for diagnosis rather than claim a stronger R0'
if summary['stop_reason']=='wall_budget':print('R1_WALL_STOP:Validating the best saved candidate within the wall budget.',flush=True)
download.write_text("from huggingface_hub import snapshot_download\nfrom pathlib import Path\np=Path(__file__).parent\nsnapshot_download('google/metricx-24-hybrid-large-v2p6',revision='51e875ba5c525c81627cfd135ee10f43c87dce00',local_dir=p/'models/metricx-24-hybrid-large',allow_patterns=['config.json','pytorch_model.bin','model.safetensors'],max_workers=4)\nsnapshot_download('google/mt5-xl',revision='63fc6450d80515b48e026b69ef2fbbd426433e84',local_dir=p/'models/metricx-tokenizer',allow_patterns=['spiece.model','tokenizer*.json','special_tokens_map.json','config.json'])\n")
run('scorer_download',[sys.executable,str(download)])
run('readiness',[sys.executable,'r1_readiness.py','--run-root',str(ROOT)])
assert hashlib.sha256(preserved.read_bytes()).hexdigest()=='81b369a5f6c6343c160c99c4d3271f2ecb63781363b05e9c89e7b2703b77785f'
best=json.loads((formal/'best.json').read_text());adapter=formal/best['checkpoint']/'adapter'
export=ROOT/'R1_EXPORT_2026-11-12.zip'
with zipfile.ZipFile(export,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        if not p.is_file() or p==export or rel.parts[0] in ['inputs'] or 'resume_slots' in rel.parts or 'checkpoints' in rel.parts:continue
        z.write(p,'results/'+str(rel))
    for p in adapter.glob('*'):
        if p.is_file():z.write(p,'best_adapter/'+p.name)
    for p in PROJECT.rglob('*'):
        rel=p.relative_to(PROJECT)
        if p.is_file() and rel.parts[0] not in ['models','initial_adapter','__pycache__'] and '__pycache__' not in rel.parts:z.write(p,'source/'+str(rel))
print('R1_EXPORT_DONE:'+json.dumps(dict(path=str(export),bytes=export.stat().st_size,sha256=hashlib.sha256(export.read_bytes()).hexdigest(),selected_checkpoint=best['checkpoint'])),flush=True)
