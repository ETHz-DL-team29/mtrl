"""LoRA SFT baseline on the reference translations."""
import argparse, json, math, os, random, signal, time, torch
from run_dapo import make_model, save_ckpt

STOP=False
def _stop(s,f):
    global STOP; STOP=True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--train", default="data/train.jsonl")
    ap.add_argument("--langs", default="isl_Latn,lij_Latn,lld_Latn")
    ap.add_argument("--tag", default="sft_full")
    ap.add_argument("--bs", type=int, default=1)
    ap.add_argument("--accum", type=int, default=8)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--max-len", type=int, default=768)
    ap.add_argument("--ckpt-every", type=int, default=100)
    ap.add_argument("--outdir", default="results")
    ap.add_argument("--seed", type=int, default=0)
    args=ap.parse_args()
    signal.signal(signal.SIGTERM,_stop); signal.signal(signal.SIGINT,_stop)
    torch.manual_seed(args.seed); random.seed(args.seed)
    langs=set(args.langs.split(","))
    recs=[json.loads(l) for l in open(args.train)]
    recs=[r for r in recs if r["tgt_lang"] in langs and r.get("ref")]
    print("sft rows",len(recs),flush=True)
    tok,model=make_model("Qwen/Qwen3.5-0.8B",kind="all")
    params=[p for p in model.parameters() if p.requires_grad]
    opt=torch.optim.AdamW(params,lr=args.lr,betas=(0.9,0.99),weight_decay=0.0)
    pad=tok.pad_token_id or tok.eos_token_id
    ckpt_dir=os.path.join(os.environ.get("CKPT_ROOT","/scratch/users/yimiwang/night-exp/ckpt"),args.tag)
    log=os.path.join(args.outdir,f"sft_{args.tag}.jsonl")
    step=0; t0=time.time()
    while not STOP:
        batch=[recs[(step*args.bs+i)%len(recs)] for i in range(args.bs)]
        ids_list=[]; lab_list=[]
        for r in batch:
            ptext=tok.apply_chat_template([{"role":"user","content":r["prompt"]+"\n\n"+r["source"]}],
                                          tokenize=False,add_generation_prompt=True,enable_thinking=False)
            pids=tok(ptext,add_special_tokens=False).input_ids
            rids=tok(r["ref"],add_special_tokens=False).input_ids+[tok.eos_token_id]
            ids=pids+rids; lab=[-100]*len(pids)+rids
            ids=ids[:args.max_len]; lab=lab[:args.max_len]
            ids_list.append(ids); lab_list.append(lab)
        L=max(len(x) for x in ids_list)
        ii=torch.full((len(ids_list),L),pad,dtype=torch.long)
        aa=torch.zeros((len(ids_list),L),dtype=torch.long)
        ll=torch.full((len(ids_list),L),-100,dtype=torch.long)
        for j,(ids,lab) in enumerate(zip(ids_list,lab_list)):
            ii[j,:len(ids)]=torch.tensor(ids); aa[j,:len(ids)]=1; ll[j,:len(lab)]=torch.tensor(lab)
        ii=ii.cuda(); aa=aa.cuda(); ll=ll.cuda()
        out=model(input_ids=ii,attention_mask=aa,labels=ll,use_cache=False)
        if not torch.isfinite(out.loss):
            print("non-finite loss, skip", step, flush=True)
            opt.zero_grad(set_to_none=True); step+=1; continue
        loss=out.loss/args.accum
        loss.backward()
        if (step+1)%args.accum==0:
            gn=torch.nn.utils.clip_grad_norm_(params,1.0)
            opt.step(); opt.zero_grad(set_to_none=True)
        else:
            gn=torch.tensor(0.0)
        if step%10==0:
            rec={"step":step,"loss":float(out.loss),"grad":float(gn),"sec":round(time.time()-t0,1),
                 "vram":round(torch.cuda.max_memory_allocated()/2**30,2)}
            print(json.dumps(rec),flush=True)
            with open(log,"a") as f: f.write(json.dumps(rec)+"\n")
        if (step+1)%args.ckpt_every==0:
            save_ckpt(model,opt,step,args.tag,ckpt_dir)
        step+=1
    save_ckpt(model,opt,step,args.tag,ckpt_dir)
    print("SFT DONE",step,flush=True)

if __name__=="__main__":
    main()
