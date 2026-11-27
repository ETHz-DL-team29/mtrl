# ETH GitLab 与 D-INFK 集群使用手册

> 2026-11-27 · 给队友的 onboarding。只写 ETH 侧；UZH JupyterLab 不在本文范围。

## 0. 一分钟版

1. **账号**：ETH nethz（含 2FA）→ GitLab 用同一套登录；集群用同一套 SSH。
2. **GitLab**：`https://gitlab.ethz.ch`（全校）/ `https://gitlab.inf.ethz.ch`（D-INFK 课程常用）。加 SSH key 后 `git clone git@gitlab.ethz.ch:<group>/<repo>.git`。
3. **集群**：`ssh <nethz>@student-cluster.inf.ethz.ch`，Slurm 提交，`-A dl_jobs`，单 job 最长 12h、同时 1 个 running + 最多 2 个 queued。
4. **存储**：`/scratch/users/<nethz>`（100G，无备份）、`/work/courses/dl/team-XX`（50G，课程共享）、home 很小。
5. **大文件不进 Git**：ckpt / 数据放 scratch/work，Drive 存档；Git 只放代码、配置、报告。

---

## 1. 账号与权限：怎么获取

### 1.1 ETH 内部成员

- 用 **nethz 账号**（ETH username，例如 `yimiwang`）登录所有 ETH 服务；首次使用先在 [ETH 账户管理](https://accounts.ethz.ch) 激活并配 2FA。
- GitLab：打开 `https://gitlab.ethz.ch`，点 “ETH Login”，用 nethz 登录；D-INFK 的课程/组项目也可能在 `https://gitlab.inf.ethz.ch`，同样用 nethz。
- 集群：课程/课题组会把人加进对应的 LDAP/Slurm 账户组；登录 `student-cluster.inf.ethz.ch` 能进就说明权限已开。

### 1.2 外部合作者（没有 nethz）

- 需要 ETH 内部 sponsor 申请 **guest account**（guest 也有 nethz 用户名，但权限受限）。
- GitLab 侧由 group owner 邀请；集群侧需要课程/组管理员单独加 Slurm account。
- 没有 nethz 就没有 ETH GitLab/集群，别用个人 GitHub 账号硬套。

### 1.3 课程/项目资源怎么拿

- 课程页会给出 **GitLab group**、**Slurm account**（如 `dl_jobs`）、**存储路径**（如 `/work/courses/dl/team-29`）、**GPU-hours 配额**。
- 找不到时先问 TA/助教：报 nethz、课程名、需要哪个 group/account。

---

## 2. ETH GitLab 怎么用

### 2.1 首次配置 SSH（推荐）

```bash
ssh-keygen -t ed25519 -C "nethz@ethz.ch" -f ~/.ssh/id_ed25519_eth
cat ~/.ssh/id_ed25519_eth.pub
```

复制公钥 → GitLab 右上角头像 → **Preferences → SSH Keys** → 粘贴 → Add key。

测试：

```bash
ssh -T git@gitlab.ethz.ch
# Welcome to GitLab, @<nethz>!
```

`~/.ssh/config` 建议：

```sshconfig
Host gitlab.ethz.ch
  User git
  IdentityFile ~/.ssh/id_ed25519_eth
  IdentitiesOnly yes

Host gitlab.inf.ethz.ch
  User git
  IdentityFile ~/.ssh/id_ed25519_eth
  IdentitiesOnly yes
```

### 2.2 clone / push 基本流程

```bash
git clone git@gitlab.ethz.ch:<group>/<repo>.git
cd <repo>
git switch -c feat/<your-name>
# 改代码
git add -A && git commit -m "feat: ..."
git push -u origin feat/<your-name>
```

然后在 GitLab 网页开 **Merge Request**，让 owner/TA review 后 merge 到 `main`。

### 2.3 没有 SSH 时的 HTTPS

- GitLab → Preferences → **Access Tokens**，勾 `read_repository` / `write_repository`，生成 PAT。
- clone：`https://oauth2:<PAT>@gitlab.ethz.ch/<group>/<repo>.git`；不要把 PAT 写进仓库或脚本。

### 2.4 仓库约定（重要）

- **不要提交**：`ckpt/`、`*.pt`、`data/` 大文件、`results/*.jsonl` 原始日志、Drive token。
- `.gitignore` 至少包含：`ckpt/`、`*.pt`、`*.safetensors`、`__pycache__/`、`.env`、`*.log`。
- 大文件用 **Git LFS** 也要谨慎：课程 GitLab 的 LFS 配额有限，ckpt 一律放 scratch/work。
- 报告/图表可以进 Git（HTML + assets 小于几 MB 没问题）。

### 2.5 CI（可选）

仓库根放 `.gitlab-ci.yml` 即可跑 lint/test；GPU runner 一般没有，别把训练塞 CI。示例：

```yaml
stages: [test]
lint:
  stage: test
  image: python:3.12
  script:
    - pip install ruff
    - ruff check .
```

---

## 3. D-INFK 集群怎么用

### 3.1 登录

```bash
ssh <nethz>@student-cluster.inf.ethz.ch
```

建议 `~/.ssh/config`：

```sshconfig
Host eth-cluster
  HostName student-cluster.inf.ethz.ch
  User <nethz>
  IdentityFile ~/.ssh/id_ed25519_eth
```

登录后先看队列：

```bash
sinfo                 # 分区/节点
squeue -u $USER       # 自己的 job
```

### 3.2 Slurm 基本命令

```bash
sbatch job.sbatch     # 提交
squeue -u $USER       # 查看
scancel <jobid>       # 取消
sacct -j <jobid> --format=JobID,State,Elapsed,ExitCode   # 事后查
sshare -A dl_jobs     # 账户用量/份额
```

最小 sbatch：

```bash
#!/bin/bash
#SBATCH --account=dl_jobs
#SBATCH --time=04:00:00
#SBATCH --gpus=1080ti:1
#SBATCH --output=logs/%j.out
#SBATCH --error=logs/%j.err
set -u
cd /scratch/users/<nethz>/<project>
source venv/bin/activate
python train.py
```

### 3.3 配额与限制（课程集群）

- **1 个 running + 最多 2 个 queued**；第二个 running 会报 `QOSGrpJobsLimit`。
- 单 job **最长 12h**；超时会被 `CANCELLED DUE TO TIME LIMIT`。
- GPU 按卡申请：`--gpus=1080ti:1`；多卡请求常被静默降到 1 张，提交后看 `squeue`/日志确认。
- **GPU-hours 池**：课程/组共享，`sshare -A dl_jobs` 看已用/余额；跑之前算一下 `小时 × 卡数`。

### 3.4 存储

| 路径 | 大小 | 备份 | 用途 |
|---|---|---|---|
| `/home/<nethz>` | 很小（~几百 MB） | 有 | dotfiles |
| `/scratch/users/<nethz>` | 100G | **无** | 数据、ckpt、venv、临时输出 |
| `/work/courses/dl/team-XX` | 50G | 课程盘 | 团队共享、最终 ckpt |

- scratch 超配额会让 checkpoint 写入失败、进程直接挂；定期 `du -sh`。
- 训练 ckpt 每 100 步一次、每个 tag 只留最近 3 个 step；团队盘只同步 `latest.pt`。
- 重要结果再往 SwitchDrive/ETH Drive 存档。

### 3.5 环境

```bash
python3 -m venv /scratch/users/<nethz>/venvs/night
source .../bin/activate
pip install -r env/night-requirements.txt
python env/preflight.py    # 缺 torch/transformers/数据/词表 直接退出
```

- GPU 节点与登录节点的 CUDA/驱动可能不同，**在 job 里跑 preflight**，不要只在登录节点测。
- 缓存放 scratch：`export HF_HOME=/scratch/users/<nethz>/.cache/huggingface`。

---

## 4. 常见坑

1. **`QOSGrpJobsLimit`**：已经有 running job，第二个只能排队；不要重复提交。
2. **GPU 数量被降级**：请求 4 张实际 1 张；以 job 日志里的 `CUDA_VISIBLE_DEVICES` 为准。
3. **scratch 配额**：`du -sh /scratch/users/<nethz>`，超了先删 `step_*`。
4. **home 重置**：不要把 venv/ckpt 放 home。
5. **12h 上限**：长任务拆成多个 job，checkpoint 续跑。
6. **Git 里塞 ckpt**：会把仓库撑爆；用 `.gitignore` + scratch。
7. **PAT/密钥泄露**：token 只放本地 credential helper，别 commit。

---

## 5. 一份可复制的训练 recipe

```bash
# 1) 本地/登录节点准备代码
git clone git@gitlab.ethz.ch:<group>/<repo>.git
cd <repo>

# 2) 提交
sbatch run_train.sbatch
squeue -u $USER

# 3) 看日志
tail -f logs/<jobid>.out

# 4) 评测（示例）
sbatch eval_suite.sbatch

# 5) 存档
rsync -av ckpt/<tag>/latest.pt /work/courses/dl/team-XX/ckpt/<tag>/
```

`run_train.sbatch` 里记得：`preflight → MetricX/依赖服务 → 训练 → 每 100 步 ckpt → 结束前 eval`。

---

## 6. 链接

- ETH 账户：https://accounts.ethz.ch
- ETH GitLab：https://gitlab.ethz.ch
- D-INFK GitLab：https://gitlab.inf.ethz.ch
- GitLab SSH 文档：https://docs.gitlab.com/ee/user/ssh.html
- Slurm 文档：https://slurm.schedmd.com/documentation.html
- 课程集群问题：先看课程页 FAQ，再找 TA（附 `jobid`、`sacct` 输出、报错原文）。
