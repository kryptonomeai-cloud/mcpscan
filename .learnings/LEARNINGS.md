# Learnings Log

## 2026-03-14
- **Qwen3 thinking mode**: Always use `"think": false` in Ollama API calls for Qwen3 models — response goes to `thinking` field, `response` stays empty otherwise.
- **Ollama cold starts**: Use `keep_alive: "24h"` to avoid model swap timeouts.
- **LoRA DDP vs QLoRA**: Don't try full model replicas on multi-GPU — use QLoRA + balanced sharding.
- **Freqtrade strategy selectivity**: EMACrossOptimised is designed to trade ~1x/10 days. Zero trades in 27h is expected, not a bug. `close > ema150` blocks all entries in bear markets.
- **Work loop redundancy**: When all tasks are blocked/manual, repeated checks waste tokens. Need a skip mechanism.

## 2026-03-15
- **Self-improvement bottleneck**: 5 consecutive proposals stuck at 🔲 Proposed. The process generates ideas but has no approval flow. Low-risk items should auto-implement.

## 2026-03-16
- **iCloud Drive fragility**: bird daemon hangs can cascade — backup scripts that touch iCloud paths hang indefinitely without `timeout`. Always wrap iCloud FS ops in `timeout`.
- **Improvement proposals need user attention**: 6th consecutive unapproved proposal. Consider batching or auto-implementing lowest-risk items.

## 2026-03-17
- **iCloud cleanup failure is now a 3-day streak** (Mar 16×2, Mar 17). Pattern promoted to recurring. Timeout wrappers are non-negotiable for iCloud FS ops.
- **Improvement pipeline has zero throughput**: 8 proposals, 0 implemented. Process needs either auto-implement for low-risk items or explicit user review cadence. (4th time noted — promoted to LESSONS.md candidate)
- **iCloud cleanup failure is now 4 days**: Mar 16×2, Mar 17, Mar 18. Timeout wrappers still not applied because proposal pipeline is blocked.

## 2026-03-19
- **iCloud failures now cascading into backup cron**: Not just cleanup — the main backup cron (`775b0bef`) has 3 consecutive timeout errors. The iCloud problem is now causing data loss (no backups for 3+ days). Urgency elevated.
- **Improvement pipeline still at 0/9 throughput**: 9th proposal, 0 implemented. The meta-proposal to auto-implement low-risk items (Mar 18) is itself stuck at 🔲 Proposed.
