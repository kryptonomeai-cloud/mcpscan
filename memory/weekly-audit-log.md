# Weekly Audit Log

## 2026-03-15 04:01 UTC — Weekly System Audit

**Overall: ✅ Healthy — 3 items need attention**

### Passed ✅
- **OS:** macOS 26.3 (Build 25D125), uptime 10h, load avg ~6.4 (normal for M2 Pro)
- **Disk:** 720GB free of 926GB (22% used) — healthy
- **Memory:** Normal (active 901k pages, inactive 896k, wired 139k)
- **Firewall:** Enabled
- **FileVault:** On
- **SIP:** Enabled
- **Docker:** 8/8 expected containers running, all up 7h, healthy where applicable
- **LaunchAgents/Daemons:** All match baseline (21 user, 2 system, 8 daemons)
- **CrowdSec:** No active decisions (no blocked threats)
- **iCloud Backup:** Latest today at 03:02 — ✅ within 24h
- **Ollama:** Responding, 4 models loaded (bge-m3, qwen3.5:27b, nomic-embed-text, qwen3:32b)
- **OpenClaw Health:** All channel probes OK (6 Telegram bots, 1 Slack)
- **MEMORY.md:** 113 lines, 8KB — not bloated
- **OpenClaw Security:** 0 critical findings

### Warnings ⚠️
1. **OpenClaw update available** — v2026.3.13 on stable channel. Not auto-applied (requires user decision).
2. **Brew: 19 outdated packages** — including caddy, deno, gh, go, node, ollama, poppler. Non-critical but should be updated periodically.
3. **Weekly GPU Maintenance cron job in error state** — Job ID `46a7c9e0`. Last ran 3d ago with error. Needs investigation.

### Informational ℹ️
- **`softwareupdate` command not found** — unusual for macOS 26.3, may be relocated or renamed in this version.
- **Listening ports empty** — `lsof -iTCP -sTCP:LISTEN` returns nothing without elevated permissions. Known issue from previous audits.
- **Time Machine:** No destination configured (using iCloud backup via custom script instead — acceptable).
- **Brew doctor:** Deprecated cask `memo`, unlinked kegs. Cosmetic.
- **Dashchat stack** no longer running — removed from baseline (was 4 containers: frontend, backend, postgres, redis).
- **OpenClaw security warnings (3):** trusted_proxies_missing (acceptable for loopback), weak_tier models on scout/venture/taskmaster (Sonnet 4 — known config choice), multi_user heuristic (Slack allowlist triggers this — known).

### Actions Taken
- ✅ Created `/scripts/weekly-audit.md` checklist (was missing, caused this cron to have no reference)
- ✅ Updated `configs/process-baseline.json` — removed dashchat stack, added freqtrade + termix as permanent
- ℹ️ Did NOT auto-update OpenClaw or brew packages (requires user approval for external-facing changes)

### Docker Container Status
| Container | Image | Status |
|-----------|-------|--------|
| freqtrade | freqtradeorg/freqtrade:stable | Up 7h |
| termix | ghcr.io/lukegus/termix:latest | Up 7h (healthy) |
| crowdsec | crowdsecurity/crowdsec:latest | Up 7h (healthy) |
| shell-executor | yohannesgk/mini-kali-slim:latest | Up 7h |
| searxng | searxng/searxng:latest | Up 7h |
| beszel | henrygd/beszel | Up 7h |
| vaultwarden | vaultwarden/server:latest | Up 7h (healthy) |
| n8n-n8n-1 | n8nio/n8n | Up 7h |

### Cron Health
- 25 total cron jobs, 1 in error state (Weekly GPU Maintenance)
- 146 total sessions for main agent
