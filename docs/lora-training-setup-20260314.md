# LoRA Training Setup — GPU Server (2026-03-14)

## GPU Server Overview

| Item | Value |
|------|-------|
| Host | 192.168.0.92 (SSH alias: `gpu`) |
| User | kryptonome |
| OS | Ubuntu 24.04 |
| GPUs | 5× NVIDIA RTX 3090 (24 GB each = 120 GB total) |
| RAM | 125 GB |
| Disk (/) | 1.8 TB, 593 GB used, 1.2 TB free |
| PyTorch | 2.10.0+cu128 |
| CUDA Toolkit | 12.8 |

### GPU Status at Audit (2026-03-14 08:11 UTC)
```
GPU 0: 24576 MiB total, 6061 MiB used (ComfyUI), 15W
GPU 1: 24576 MiB total,   14 MiB used,            19W
GPU 2: 24576 MiB total,   14 MiB used,            24W
GPU 3: 24576 MiB total,   14 MiB used,            24W
GPU 4: 24576 MiB total,   32 MiB used,            21W
```

---

## Existing Training Stack

Located at `/home/kryptonome/email-lora/`

### Python Environments

| Venv | Path | Notes |
|------|------|-------|
| `venv` | `/home/kryptonome/email-lora/venv` | **Primary** — unsloth 2026.3.3, torch 2.10.0, trl 0.29.0, transformers 5.3.0 |
| `venv-70b` | `/home/kryptonome/email-lora/venv-70b` | Has torch + accelerate + deepspeed; unsloth missing; pandas corrupted |

### Key Packages (venv — working)
- `unsloth==2026.3.3` — fast QLoRA patching, Flash Attention 2 support
- `torch==2.10.0+cu128`
- `trl==0.29.0`
- `transformers==5.3.0`
- `datasets==4.6.1`
- `accelerate==1.13.0`
- `deepspeed==0.18.8` (in venv-70b)

---

## Dataset

| Item | Value |
|------|-------|
| Location | `/home/kryptonome/email-lora/data/` |
| Train | `train.jsonl` — 28,985 pairs |
| Val | `val.jsonl` — 1,526 pairs |
| Total | **30,511 pairs** |
| Format | ShareGPT-style messages with system/user/assistant roles |
| Task | Email summarisation (one concise line per email) |

Sample format:
```json
{
  "messages": [
    {"role": "system", "content": "Summarise this email in one concise line..."},
    {"role": "user",   "content": "From: Nintendo <...>\n..."},
    {"role": "assistant", "content": "Nintendo Wave 3 Booster Course Pass announced..."}
  ]
}
```

---

## Previously Trained Models

| Model | Checkpoint | Notes |
|-------|-----------|-------|
| 8B (Llama) | `models/email-lora-8b/` | Complete |
| 32B (Qwen2.5-32B-Instruct) | `models/email-lora-32b/checkpoint-500/` | Completed; adapter 256 MB |
| 70B (Llama 3.3) | `models/email-lora-70b/` | Attempted; was running ~16% through |

---

## Accelerate / FSDP Config

File: `/home/kryptonome/email-lora/accelerate_config.yaml`

```yaml
compute_environment: LOCAL_MACHINE
distributed_type: FSDP
fsdp_config:
  fsdp_auto_wrap_policy: TRANSFORMER_BASED_WRAP
  fsdp_backward_prefetch: BACKWARD_PRE
  fsdp_cpu_ram_efficient_loading: true
  fsdp_sharding_strategy: FULL_SHARD
  fsdp_state_dict_type: SHARDED_STATE_DICT
  fsdp_sync_module_states: true
  fsdp_use_orig_params: true
mixed_precision: bf16
num_processes: 5
```

---

## Recommended Training Command

### Model: Qwen/Qwen2.5-32B-Instruct (best fit for this hardware)

```bash
ssh gpu
cd ~/email-lora
source venv/bin/activate

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export WANDB_DISABLED=true
export OUTPUT_DIR="$HOME/lora-output/qwen32b-v2"
export MODEL="Qwen/Qwen2.5-32B-Instruct"
export BATCH_SIZE=2
export MAX_SEQ=1024

# Run inside tmux to survive SSH disconnect
tmux new -s lora-train
bash train-lora-v3.sh ~/email-lora/data
```

Or using the FSDP script for proper multi-GPU DDP:
```bash
accelerate launch --config_file accelerate_config.yaml train-fsdp.py \
  --model_id Qwen/Qwen2.5-32B-Instruct \
  --data_dir ~/email-lora/data \
  --output_dir ~/lora-output/qwen32b-fsdp \
  --max_seq_length 1024 \
  --per_device_train_batch_size 2 \
  --gradient_accumulation_steps 4 \
  --num_train_epochs 3 \
  --learning_rate 2e-5
```

### LoRA Config (used in v3 script)
```python
r=16
lora_alpha=32
lora_dropout=0.05 (set to 0 for unsloth speed boost)
target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]
use_gradient_checkpointing="unsloth"
load_in_4bit=True
```

---

## Performance Benchmarks

### Test Run (2026-03-14) — Unsloth balanced mode, 5 GPUs

| Metric | Value |
|--------|-------|
| Model | Qwen/Qwen2.5-32B-Instruct |
| Mode | Unsloth `device_map="balanced"` (model parallelism) |
| Packed examples | 21,521 |
| Step 1 (JIT warmup) | 68.2s |
| Step 2+ (steady state) | ~46s/step |
| Trainable params | 134,217,728 / 32.9B (0.41%) |
| GPU memory (post-load) | ~14-16 GB/GPU (4-bit sharded) |

**⚠️ Unsloth balanced mode = model parallelism, NOT data parallelism.**  
Each step processes the same amount of data regardless of GPU count.  
3 epochs × ~2,690 steps × 46s/step = **~103 hours** — **NOT RECOMMENDED** for full training.

### Prior Training (2026-03-08) — FSDP DDP mode, 5 GPUs

| Metric | Value |
|--------|-------|
| Model | Qwen/Qwen2.5-32B-Instruct |
| Mode | FSDP FULL_SHARD (data parallelism) |
| seq_len | 512 |
| Step rate | ~4.65–6.71s/step |
| Total steps | ~4,980 (3 epochs) |
| Estimated total time | **~8–10 hours** |
| Checkpoint-500 | ✅ Saved (256 MB adapter) |

**FSDP is the correct approach for multi-GPU training on this server.**

### Estimated Training Time — Qwen 32B, seq_len=1024, FSDP

| Config | Steps/epoch | s/step | Total (3 epochs) |
|--------|------------|--------|------------------|
| FSDP, bs=2/GPU, grad_accum=4 | ~725 | ~8s | **~5–6 hours** |
| FSDP, bs=1/GPU, grad_accum=8 | ~1,450 | ~5s | **~6–7 hours** |

---

## Axolotl Installation Attempt

**Status: ❌ Not working on this environment**

Axolotl 0.15.0 requires `torch==2.8.0`, but the server has `torch==2.10.0`. Installing without deps (`--no-deps`) leaves too many missing dependencies (colorama, fire, posthog, trackio, etc.) and the `venv-70b` pandas install is also corrupted.

**Config file created** at `/home/kryptonome/axolotl-email-qwen32b.yml` for reference if Axolotl is installed properly later (requires fresh venv + matching torch version).

**Recommendation:** Use the existing **unsloth + TRL + FSDP** stack. It's already proven (32B checkpoint exists), properly configured for 5-GPU FSDP, and runs at ~5–7s/step.

---

## Axolotl Config (reference — not currently usable)

File: `/home/kryptonome/axolotl-email-qwen32b.yml`

```yaml
base_model: Qwen/Qwen2.5-32B-Instruct
load_in_4bit: true
adapter: qlora
lora_r: 16
lora_alpha: 32
datasets:
  - path: /home/kryptonome/email-lora/data/train.jsonl
    type: sharegpt
output_dir: /home/kryptonome/lora-output/qwen32b-axolotl
sequence_len: 1024
micro_batch_size: 2
gradient_accumulation_steps: 4
num_epochs: 3
optimizer: adamw_bnb_8bit
bf16: auto
fsdp:
  - full_shard
  - auto_wrap
fsdp_config:
  fsdp_transformer_layer_cls_to_wrap: Qwen2DecoderLayer
```

---

## Next Steps

1. **Launch full training** using `train-lora-v3.sh` or `train-fsdp.py` inside a `tmux` session
2. **Important:** Always use `tmux` — SSH connections timeout and kill training
3. Monitor with: `ssh gpu "nvidia-smi dmon -s pucvmet -d 5"`
4. After training completes, merge with `merge_and_export.py` for GGUF/Ollama deployment
5. If Axolotl is needed: create fresh venv with `torch==2.8.0` and `pip install axolotl[deepspeed]`

---

## Scripts Available on Server

| Script | Purpose |
|--------|---------|
| `train-lora-v3.sh` | Unsloth + balanced mode (single node, sequential) |
| `train-fsdp.py` | **Recommended** — proper FSDP DDP across 5 GPUs |
| `train-qwen-ddp.py` | DDP variant |
| `train_deepspeed.py` | DeepSpeed variant |
| `merge_and_export.py` | Merge LoRA → full model → GGUF |
| `train-qwen32b-test.sh` | 10-step benchmark script (uploaded 2026-03-14) |
