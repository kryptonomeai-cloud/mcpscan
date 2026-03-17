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
