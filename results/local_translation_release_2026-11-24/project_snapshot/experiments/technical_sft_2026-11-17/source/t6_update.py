import torch,gc
from mtgrpo.r0_train import loss_sum
def update(policy,group,optimizer,microbatch,capture_rng,restore_rng):
 """Only retry OOM before optimizer.step; weights cannot be partially updated."""
 total=sum(len(x['target']) for x in group);saved=capture_rng();physical=0;retries=0
 while True:
  policy.model.train();optimizer.zero_grad(set_to_none=True);loss=0.
  try:
   for i in range(0,len(group),microbatch):
    batch=group[i:i+microbatch];physical+=sum(len(x['target']) for x in batch)
    value=loss_sum(policy.model,batch,policy.tokenizer,policy.device)
    if not torch.isfinite(value):raise FloatingPointError('Nonfinite SFT forward loss')
    loss+=float(value.detach());(value/total).backward()
  except torch.cuda.OutOfMemoryError:
   optimizer.zero_grad(set_to_none=True);gc.collect();torch.cuda.empty_cache();restore_rng(saved)
   if microbatch<=2:raise
   microbatch=2;retries+=1;continue
  break
 params=[p for p in policy.model.parameters() if p.requires_grad]
 norm=torch.nn.utils.clip_grad_norm_(params,1.,error_if_nonfinite=True)
 # An OOM here is fatal; never retry a potentially partial optimizer update.
 optimizer.step()
 return dict(mean_loss=loss/total,grad_norm=float(norm),physical_target_tokens=physical,OOM_backward_retries=retries,microbatch=microbatch)
