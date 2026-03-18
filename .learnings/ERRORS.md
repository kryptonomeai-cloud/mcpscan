# Error Log

## 2026-03-14
- **SSH hostname confusion**: `gpu-server` doesn't resolve from Mac mini; correct alias is `gpu` (192.168.0.92). Caused multiple failed status checks across sessions.
- **LoRA training crash**: Training stopped at step 600/2748 (unattended). Email-LoRA 8B also crashed — unsloth prompted for missing package in non-interactive mode (EOFError).
- **Freqtrade container disappeared**: Was running at 14:04, not found at 20:44. Restarted at 21:02.

## 2026-03-15
- No new errors detected in last 24h sessions (overnight was quiet — only paperless backup cron ran successfully).

## 2026-03-16
- **iCloud Drive hang** (03:19): bird daemon became unresponsive during backup symlink/stats phase. Restarting bird didn't fully recover. Backup cleanup at 04:00 skipped — `find`/`ls` hung on iCloud path. May need reboot to resolve.
- **macOS update still pending**: CLI `softwareupdate --install` failed (sudo auth in non-interactive context). Needs manual System Settings install.

## 2026-03-17
- **iCloud backup cleanup failed again** (04:00): 3rd consecutive day. `find -mtime +7` on iCloud path hung. Backup export itself succeeded but stale files accumulating.
