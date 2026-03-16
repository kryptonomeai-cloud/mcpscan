# Forge Fixes — 2026-03-14

## Task 1: Restic Backup to NAS

**Status: ✅ No fix needed — backup is working fine**

**Investigation:**
- The restic backup does NOT go to the NAS at 192.168.0.18. It backs up to the **GPU server** (192.168.0.92) via an SSH-tunneled REST server.
- Script: `scripts/restic-backup.sh` — runs daily at 03:30 via launchd
- Last successful run: **2026-03-14 03:30:14** — backup, retention, and integrity check all passed
- 10 snapshots stored, no errors
- Password properly stored in Keychain (`restic-backup`)

**NAS note:** `/DATA/Backups/` doesn't exist on NAS. The actual path is `/DATA/Backup/` (singular, and currently empty). The NAS has `/DATA` on a 904GB drive (45G used). No restic repo exists on the NAS — it was never the backup target.

## Task 2: Weekly GPU Maintenance Cron

**Status: ⚠️ Self-healing — GPU is back online, will resolve on next run (Sun 03:15)**

**Job ID:** `46a7c9e0-ac59-4024-8a3b-b10ffef2f889`
**3 consecutive errors since Mar 7:**

| Date | Error | Root Cause |
|------|-------|------------|
| Mar 7 | Channel config missing | Delivery channel wasn't set to telegram |
| Mar 9 | Channel config missing | Same issue (fixed since then) |
| Mar 12 | SSH timeout | GPU server was offline/unreachable |

**Current state:** GPU server is back online (uptime 18h33m). All 5× RTX 3090 GPUs healthy at 20-21°C, Ollama active. Delivery channel is now properly configured (`telegram` → `8387589944`).

**Next scheduled run:** Sun 2026-03-15 03:15 GMT — should succeed and clear error state.

## Task 3: Credential Audit

**Status: 🔧 1 hardcoded password found and fixed**

### Finding: `scripts/unifi-vlan-setup.py`
- **Before:** UniFi controller password hardcoded as `PASSWORD = "fakmop-Tunqo1-wemcah"`
- **Fix:** Stored password in macOS Keychain (`unifi-controller` / `kryptonome`) and replaced with `security find-generic-password` subprocess call
- **Risk:** Medium — script is local-only but password was in plaintext in a git-tracked workspace

### Clean patterns found (no action needed):
- `scripts/restic-backup.sh` — already uses Keychain (`restic-backup`)
- `scripts/email-pipeline.py` — uses env var `GOG_KEYRING_PASSWORD`
- `scripts/gmail-labeller.py` — uses env var `GOG_KEYRING_PASSWORD`
- `scripts/mac-use.sh` — uses env var `GEMINI_API_KEY`
- `projects/email-classifier/` — file-based OAuth tokens (standard Google pattern)
- All cron job payloads — no hardcoded credentials found

### Recommendations:
1. Rotate the UniFi controller password (it was in git history)
2. Consider `git filter-branch` or BFG to scrub the old password from history
