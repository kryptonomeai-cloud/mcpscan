# LoRA 7B Training Check — 2026-03-14 10:05 GMT

## Status: ✅ Training is running

### Process
- **Script:** `train-qwen7b-full.sh` (PID 453508)
- **Python process:** PID 453511, 99.4% CPU
- **Model:** Qwen/Qwen2.5-7B-Instruct (4-bit via Unsloth)
- **Output:** `/home/kryptonome/lora-output/qwen7b-v1`
- **Started:** Sat Mar 14 09:22:34 GMT 2026 (~43 min ago)

### Progress
- **Step:** 97 / 2,748 (~3.5%)
- **Speed:** ~25.8s per step (stable)
- **Elapsed:** ~42 minutes
- **Estimated remaining:** ~19.0 hours (finishes ~Sun 05:00 GMT)
- **Epochs:** 3 (14,644 packed examples, batch size 16)
- **Trainable params:** 161.5M / 7.78B (2.08%)

### GPU Usage
| GPU | Utilization | VRAM Used | VRAM Total |
|-----|------------|-----------|------------|
| 0 | 0% | 6,061 MiB | 24,576 MiB |
| **1** | **100%** | **15,849 MiB** | **24,576 MiB** |
| 2 | 0% | 14 MiB | 24,576 MiB |
| 3 | 0% | 14 MiB | 24,576 MiB |
| 4 | 0% | 32 MiB | 24,576 MiB |

Training on GPU 1 (RTX 3090). VRAM usage: 15.5 / 24 GB (64%).

### Errors
None. One non-critical warning: `regex did not match, patch may have failed` (Unsloth Zoo, cosmetic — training proceeded normally).

### Training Config
- Unsloth 2026.3.3 with FA2 (Flash Attention 2)
- BFloat16 enabled
- Gradient accumulation: 4 steps
- Packing enabled (2x faster)
- Train: 28,985 samples → Val: 1,526 samples
