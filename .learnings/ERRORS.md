# Error Log

## 2026-03-14
- **SSH hostname confusion**: `gpu-server` doesn't resolve from Mac mini; correct alias is `gpu` (192.168.0.92). Caused multiple failed status checks across sessions.
- **LoRA training crash**: Training stopped at step 600/2748 (unattended). Email-LoRA 8B also crashed — unsloth prompted for missing package in non-interactive mode (EOFError).
- **Freqtrade container disappeared**: Was running at 14:04, not found at 20:44. Restarted at 21:02.

## 2026-03-15
- No new errors detected in last 24h sessions (overnight was quiet — only paperless backup cron ran successfully).
