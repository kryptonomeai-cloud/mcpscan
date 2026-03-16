# Learnings Log

## 2026-03-14
- **Qwen3 thinking mode**: Always use `"think": false` in Ollama API calls for Qwen3 models — response goes to `thinking` field, `response` stays empty otherwise.
- **Ollama cold starts**: Use `keep_alive: "24h"` to avoid model swap timeouts.
- **LoRA DDP vs QLoRA**: Don't try full model replicas on multi-GPU — use QLoRA + balanced sharding.
- **Freqtrade strategy selectivity**: EMACrossOptimised is designed to trade ~1x/10 days. Zero trades in 27h is expected, not a bug. `close > ema150` blocks all entries in bear markets.
- **Work loop redundancy**: When all tasks are blocked/manual, repeated checks waste tokens. Need a skip mechanism.

## 2026-03-15
- **Self-improvement bottleneck**: 5 consecutive proposals stuck at 🔲 Proposed. The process generates ideas but has no approval flow. Low-risk items should auto-implement.
