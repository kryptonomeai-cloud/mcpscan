# LoRA Training Status — 2026-03-14

## GPU Server
- **Host:** 192.168.0.92 (SSH alias `gpu`, user `kryptonome`)
- **Hardware:** 5× NVIDIA RTX 3090 (24GB each), 125GB RAM
- **Software:** CUDA 13.1, Driver 590.48.01, PyTorch 2.10.0+cu128, Unsloth 2026.3.3
- **Stack:** Unsloth + trl 0.29.0 + peft 0.18.1 (NOT Axolotl — Unsloth is better for this)
- **Venv:** `/home/kryptonome/email-lora/venv/`

## What Happened (March 8 crash)
The **DDP multi-GPU training** (`train-qwen-ddp.py`) crashed with **CUDA OOM** on March 8 at 01:36.

**Root cause:** The DDP script tried to load **Qwen3-32B** (not Qwen2.5-32B!) with `torchrun --nproc_per_node=5`, which loads a **full copy** of the model on each GPU. Each 3090 has 24GB — not enough for a 32B model per rank.

**Key error:** `torch.OutOfMemoryError: Tried to allocate 17.43 GiB. GPU 0 has a total capacity of 23.56 GiB of which 1.16 GiB is free`

The correct approach (which already exists in `train-qwen32b-test.sh`) uses **Unsloth + QLoRA + device_map="balanced"**, which shards the quantized model across GPUs without DDP.

## Dataset
- **Location:** `/home/kryptonome/email-lora/data/`
- **Train:** 28,985 examples (124MB `train.jsonl`)
- **Val:** 1,526 examples (6.6MB `val.jsonl`)
- **Format:** Chat messages (system + user + assistant), email summarisation task
- **Note:** `/home/jarvis/email-classifier/data/lora-dataset/` does NOT exist on the GPU server

## Current GPU State (as of 09:12 UTC)
- All 5 GPUs idle (0% utilization), cool (20°C)
- GPU 0 has 6GB used: ComfyUI (256MB) + a `python app.py` process (5.8GB, PID 30735 — started March 13)
- GPUs 1–4 free (14MB each from Xorg)
- No training processes running

## Test Results

### Qwen2.5-32B-Instruct (QLoRA, 5 GPUs)
- ✅ Model loaded successfully via `device_map="balanced"`
- ✅ Training started (0.41% params trained = 134M/32.9B)
- Config: batch=2, grad_accum=4, seq_len=1024, r=16
- 21,521 packed examples
- Timed out before completing step timing (needs longer run)
- **Script:** `/home/kryptonome/train-qwen32b-test.sh` (fixed — now exports env vars)

### Qwen2.5-7B-Instruct (QLoRA, single GPU)
- ✅ Model loaded on GPU 1, training confirmed working
- **~26.5 seconds/step** (batch=4, grad_accum=4, seq_len=2048, r=64)
- 2.08% params trained = 161M/7.8B
- 14,644 packed examples
- **Estimated time for 3 epochs: ~20 hours** (~2,747 steps × 26.5s)
- **Script:** `/home/kryptonome/train-qwen7b.sh` (test) / `/home/kryptonome/train-qwen7b-full.sh` (full)

## Scripts on Server

| Script | Purpose |
|--------|---------|
| `train-qwen32b-test.sh` | Unsloth QLoRA 32B, multi-GPU balanced, quick test |
| `train-qwen7b.sh` | Unsloth QLoRA 7B, single GPU, quick test (N steps) |
| `train-qwen7b-full.sh` | Unsloth QLoRA 7B, 3 epochs, eval + checkpoints |
| `train-qwen-ddp.py` | ❌ DDP script — BROKEN (OOM), do not use |

## To Start Full Training

```bash
ssh gpu
nohup bash /home/kryptonome/train-qwen7b-full.sh > ~/lora-qwen7b-training.log 2>&1 &
tail -f ~/lora-qwen7b-training.log
```

Output will be saved to `/home/kryptonome/lora-output/qwen7b-v1/adapter/`

## Recommendations
1. **Start with 7B** — runs on single GPU, ~20h for 3 epochs, good baseline
2. **32B later** — works with device_map="balanced" across all 5 GPUs, but much slower per step
3. **Kill PID 30735** if you need GPU 0 memory (`ssh gpu "kill 30735"`)
4. **Monitor:** `ssh gpu "tail -f ~/lora-qwen7b-training.log"` or `ssh gpu "nvidia-smi"`
