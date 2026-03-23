# Weekly Audit Log

## 2026-03-22 04:03 UTC — Weekly System Audit

**Overall: ✅ Healthy — 2 minor items noted**

### Passed ✅
- **OS:** macOS 26.3.1 (Build 25D2128), uptime 6d 22h, load avg 1.43/1.33/1.25
- **Disk:** 697GB free of 926GB (2% used) — excellent
- **Memory:** Normal (active 860k pages, inactive 849k, wired 137k, 0 swapouts)
- **Firewall:** Enabled
- **FileVault:** On
- **SIP:** Enabled
- **Docker:** 8/8 expected containers running, all up 4-6 days, healthy where applicable
- **LaunchAgents/Daemons:** 23 user (2 new: ComfyUI MCP Server, OpenMOSS), 2 system, 9 daemons (1 new: NordVPN helper) — all accounted for
- **CrowdSec:** Healthy, no active decisions
- **Ollama:** Responding on :11434, 4 models (bge-m3, qwen3.5:27b, nomic-embed-text, qwen3:32b)
- **OpenClaw Health:** All channel probes OK (Telegram + Slack)
- **Cron Jobs:** 26 total, 20 enabled, 6 disabled (MOSS agents). All enabled jobs in OK state, 0 consecutive errors.
- **Sessions:** 161 main agent sessions (stable from last week's 146)
- **MEMORY.md:** 130 lines — within limits

### Warnings ⚠️
1. **OpenClaw update available** — v2026.3.13 on stable. Current version not auto-updated. User should decide when to apply.
2. **macOS background security update pending** — "macOS Background Security Improvement (a)-25D771280a" requires restart. 208MB.

### Informational ℹ️
- **Brew:** 14 outdated packages (ca-certificates, caddy, cmake, deno, harfbuzz, libnghttp2, mlx-c, ollama, qemu, semgrep, simdjson, uv). Non-critical.
- **Brew doctor:** Deprecated cask `memo` (cosmetic). Fixed: linked certifi + memo kegs, added /opt/homebrew/sbin to PATH.
- **Time Machine:** Not configured (using restic + iCloud backups — acceptable)
- **Security audit:** 1 critical (hooks.allowed_agent_ids_unrestricted — known/accepted config), 4 warnings (trusted_proxies, weak_tier models on sub-agents, multi_user heuristic, probe scope) — all known from previous audits.
- **New LaunchAgents since last audit:** com.comfyui.mcp-server.plist, com.openmoss.server.plist — intentional additions
- **New LaunchDaemon:** com.nordvpn.macos.helper.plist — NordVPN installation

### Actions Taken
- ✅ Linked unlinked brew kegs (certifi, memo)
- ✅ Added /opt/homebrew/sbin to ~/.zshrc PATH
- ✅ Updated process-baseline.json with 3 new LaunchAgent/Daemon entries

### Docker Container Status
| Container | Status |
|-----------|--------|
| freqtrade | Up 4 days |
| termix | Up 6 days (healthy) |
| crowdsec | Up 6 days (healthy) |
| shell-executor | Up 6 days |
| searxng | Up 6 days |
| beszel | Up 6 days |
| vaultwarden | Up 6 days (healthy) |
| n8n-n8n-1 | Up 6 days |

---

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
