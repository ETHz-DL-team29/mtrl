from pathlib import Path
import os,sys,time,json,subprocess,hashlib,zipfile,traceback,gc
ROOT=Path('/content/p25_project');os.chdir(ROOT);OUT=ROOT/'run';OUT.mkdir(exist_ok=True)
os.environ.update(HF_HOME=str(ROOT/'.cache/huggingface'),HF_HUB_DISABLE_XET='1',TOKENIZERS_PARALLELISM='false',USE_TF='0',USE_FLAX='0')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2));t.replace(p)
def emit(phase,**v):dump(OUT/'progress.json',dict(phase=phase,unix=time.time(),**v));print('P25_'+phase+':'+json.dumps(v),flush=True)
try:
 assert not (OUT/'started.json').exists();dump(OUT/'started.json',dict(unix=time.time()));protocol=json.loads((ROOT/'protocol.json').read_text());budget=json.loads((ROOT/'allocation_budget.json').read_text());assert time.time()<budget['deadline_unix'];assert all(sha(ROOT/n)==h for n,h in json.loads((ROOT/'source_manifest.json').read_text()).items())
 emit('install_dependencies')
 with (OUT/'pip.log').open('w') as log:
  subprocess.run([sys.executable,'-m','pip','install','-q','transformers==5.22.1','peft==0.21.2','accelerate==1.15.0','safetensors==0.8.0','sentencepiece==0.2.2','sacrebleu==2.6.0','psutil','pytest'],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=900)
  subprocess.run([sys.executable,'-m','pip','uninstall','-y','torchao'],stdout=log,stderr=subprocess.STDOUT,timeout=120)
 from huggingface_hub import snapshot_download
 emit('download_base');snapshot_download('Qwen/Qwen2.5-3B-Instruct',revision=protocol['base_revision'],local_dir=ROOT/'models/qwen2.5-3b-instruct',allow_patterns=['config.json','tokenizer*.json','special_tokens_map.json','vocab.json','merges.txt','generation_config.json','*.safetensors','*.safetensors.index.json'],max_workers=2)
 import torch
 torch.set_num_threads(4);torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
 from mtgrpo.models import Policy,environment_info
 from mtgrpo.common import read_jsonl
 from mtgrpo.telemetry import ResourceSampler
 from p25_eval import evaluate,compare,preflight
 monitor=ResourceSampler(OUT/'resources.jsonl');monitor.start();monitor.phase='initial_WMT26';emit('load_actor')
 policy=Policy('cpu',adapter=str(ROOT/'initial_adapter'),trainable=False,checkpointing=False,attention_implementation='sdpa');policy.model.float().to('cuda').eval();policy.device='cuda';policy.dtype=torch.float32;assert not any(p.requires_grad for p in policy.model.parameters());dump(OUT/'environment.json',dict(environment_info(),precision='FP32',TF32=False));preflight(policy)
 docs=read_jsonl(ROOT/'data/wmt_documents.jsonl');arms=dict(before=ROOT/'initial_adapter',oldDAPO120=ROOT/'candidate_adapter');predictions,elapsed=evaluate(policy,arms,'wmt_initial',budget['evaluation_deadline_unix']);emit('initial_metrics');metrics=compare(docs,predictions['before'],predictions['oldDAPO120'],OUT/'wmt_initial/paired_metrics.json');overall=metrics['subsets']['overall'];improved=overall['chrfpp']['delta95CI'][0]>0 and overall['bleu']['delta']>=0
 reserve=max(5400,elapsed/2*1.3+3000);train_deadline=min(budget['training_deadline_unix'],budget['deadline_unix']-reserve);allowed=not improved and torch.cuda.get_device_capability()[0]>=8 and train_deadline-time.time()>=1800
 decision=dict(unix=time.time(),initial_WMT_complete=True,initial_reliable_gain=improved,conditional_training=allowed,measured_initial_seconds=elapsed,reserved_for_final_and_export_seconds=reserve,training_deadline_unix=train_deadline,reason='No reliable initial WMT gain;predeclared shortmid arm' if allowed else 'Initial gain,unsupportedGPU,or insufficientremainingtime');dump(OUT/'conditional_decision.json',decision);emit('conditional_decision',**{k:v for k,v in decision.items() if k!='unix'})
 del policy;gc.collect();torch.cuda.empty_cache()
 if allowed:
  monitor.phase='download_reward';emit('download_reward')
  for model,revision,folder,patterns in [('google/metricx-24-hybrid-large-v2p6','51e875ba5c525c81627cfd135ee10f43c87dce00','metricx-24-hybrid-large',['config.json','*.safetensors','*.safetensors.index.json','pytorch_model*.bin','pytorch_model*.bin.index.json']),('google/mt5-xl','63fc6450d80515b48e026b69ef2fbbd426433e84','metricx-tokenizer',['config.json','spiece.model','tokenizer*.json','special_tokens_map.json'])]:snapshot_download(model,revision=revision,local_dir=ROOT/'models'/folder,allow_patterns=patterns,max_workers=2)
  import p25_train
  p25_train.BUDGET['training_deadline_unix']=train_deadline;dump(OUT/'actual_training_schedule.json',decision);monitor.phase='shortmid_DAPO';p25_train.main();gc.collect();torch.cuda.empty_cache()
  summary=json.loads((OUT/'shortmid_train/summary.json').read_text());selected=ROOT/'run/shortmid_train/checkpoints'/summary['selected_tag']/'adapter';assert selected.exists();monitor.phase='new_endpoint_WMT';emit('new_endpoint_WMT',selected_step=summary['selected_step'])
  policy=Policy('cpu',adapter=str(selected),trainable=False,checkpointing=False,attention_implementation='sdpa');policy.model.float().to('cuda').eval();policy.device='cuda';policy.dtype=torch.float32
  new_predictions,new_elapsed=evaluate(policy,dict(shortmidDAPO=selected),'wmt_shortmid',budget['deadline_unix']-3000);compare(docs,predictions['before'],new_predictions['shortmidDAPO'],OUT/'wmt_shortmid/paired_metrics.json');del policy;gc.collect();torch.cuda.empty_cache()
 monitor.stop();dump(OUT/'summary.json',dict(unix=time.time(),initial_WMT_complete=True,initial_reliable_gain=improved,shortmid_training_executed=allowed,new_SFT_updates=0,all_GPU_work_finished=True,original_R0_preserved=True));emit('all_model_work_complete')
except BaseException as ex:
 dump(OUT/'error.json',dict(type=type(ex).__name__,message=str(ex),traceback=traceback.format_exc(),unix=time.time()));emit('failed',error_type=type(ex).__name__)
finally:
 emit('exporting');archive=ROOT/'final_export.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
  for folder in ['run','data','mtgrpo']:
   for p in (ROOT/folder).rglob('*'):
    if p.is_file() and 'checkpoints' not in p.parts and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT).as_posix())
  for p in ROOT.iterdir():
   if p.is_file() and p.suffix in ['.py','.json']:z.write(p,p.name)
 data=archive.read_bytes();dest=ROOT/'export_parts';dest.mkdir(exist_ok=True);parts=[]
 for i,start in enumerate(range(0,len(data),6*1024**2)):
  chunk=data[start:start+6*1024**2];n=f'part_{i:03}.bin';(dest/n).write_bytes(chunk);parts.append(dict(name=n,bytes=len(chunk),sha256=hashlib.sha256(chunk).hexdigest()))
 dump(ROOT/'final_export.json',dict(bytes=len(data),sha256=sha(archive),parts=parts,all_GPU_work_finished=True,failed=(OUT/'error.json').exists(),unix=time.time()));emit('export_ready')
