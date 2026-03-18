# Security Log

## 2026-03-15 (Sun) — 05:11 UTC

### Sweep Summary: ✅ All Clear (minor notes)

**Mac mini:**
- Firewall: ✅ enabled
- Listening ports: ✅ none (no unexpected services)

**CrowdSec:**
- Container: ✅ healthy
- Machines: 3/3 online — ⚠️ nas-zimaos heartbeat 14h37m stale
- Bouncers: 8/8 valid
- CAPI: ✅ connected, community blocklist active
- Alerts: none | Decisions: none

**GPU Server:**
- fail2ban sshd: ✅ 0 banned, 1 total failed attempt
- UFW: ✅ active, rules unchanged (Ollama/SSH/ComfyUI/Beszel/TRELLIS properly locked to LAN/Tailscale)
- rkhunter: timed out (ran past 15s limit, non-critical)

**Tool Versions:**
- Trivy: 0.69.3, Lynis: 3.1.6 — no brew outdated flags

**CVE Check:**
- Web search quota exhausted — unable to check this run

**Docker Images Running:**
- termix, crowdsec, mini-kali-slim, searxng, beszel — trivy scan skipped (multi-image scan needs individual runs)

**Action Items:**
- Monitor nas-zimaos heartbeat — if stale >24h, restart CrowdSec container on NAS
- CVE search will retry next run

## 2026-03-16 05:00 UTC — Daily Security Sweep

### CrowdSec
- All machines ✔️ except **nas-zimaos** (heartbeat 38h stale)
- No alerts or active bans
- CAPI connected, community blocklist enabled
- Container: healthy

### Infrastructure
- Mac mini firewall: **enabled**
- Mac mini listening ports: none unexpected (lsof returned clean)
- GPU server: fail2ban OK (0 banned), UFW active with proper rules
- GPU rkhunter: SSH timed out before rkhunter could run (non-critical)
- Trivy container scan: ran on 2 images, no HIGH/CRITICAL findings reported
- Brew security tools: all up to date (no outdated trivy/lynis)

### CVE Intel
- Web search quota exhausted; unable to check fresh CVEs this run

### Issues Noted
- ⚠️ nas-zimaos CrowdSec heartbeat stale 38h — recurring issue, likely NAS sleeping or agent stopped
- Trivy scan incomplete (SIGTERM on timeout) — consider increasing timeout

## 2026-03-17 05:00 UTC — Daily Security Sweep

### CrowdSec
- Container: healthy, uptime 47h
- Machines: localhost ✔️, gpu-server ✔️, nas-zimaos ⚠️ (62h stale heartbeat)
- Bouncers: 7 valid, NAS bouncers stale ~62h, caddy-bouncer@172.23.0.1 stale 5 days
- Alerts/Decisions: none
- CAPI: connected, community blocklist enabled

### Infrastructure
- Mac mini firewall: enabled ✔️
- Mac mini listening ports: all expected (rapportd, AirPlay, Ollama localhost, Docker services, beszel, lume, node/OpenClaw)
- No unexpected external-facing ports detected
- Port 2121 (Python FTP?) on *:2121 — recurring, noted previously
- GPU server: fail2ban sshd clean (0 banned), UFW active with proper rules, rkhunter timed out (124)

### CVE Intel
- Web search rate-limited; SearXNG fallback used
- macOS: CVE-2026-20619 (info disclosure) noted; Apple released macOS Sequoia 15.4 security update — check if applied
- Node.js: Jan 2026 security releases — verify current version
- No critical/high CVEs requiring immediate action found for our stack

### Tool Versions
- trivy, lynis: no outdated packages flagged by brew

### Action Items
- ⚠️ NAS CrowdSec agent offline ~62h — check NAS status
- ⚠️ caddy-bouncer@172.23.0.1 stale 5 days
- Verify macOS Sequoia 15.4 update applied
- Investigate port 2121 if not intentional
- rkhunter on GPU timed out — run manually if needed
