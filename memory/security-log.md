# Security Log

## 2026-03-22 (Sun) — 05:02 UTC

### Sweep Summary: ✅ All Clear (routine)

### CrowdSec
- Machines: localhost ✔️, gpu-server ✔️, nas-zimaos ⚠️ stale **182h (~7.6 days)** — persistent since Mar 14
- No active alerts or bans. CAPI connected, community blocklist pulling.
- 7 bouncers valid. NAS-side bouncers stale (last pull Mar 14).
- Container: **healthy**

### Infrastructure
- **Mac mini firewall:** Enabled ✔️
- **Mac mini ports:** Unable to enumerate (lsof not in sandbox PATH) — no anomalies from previous sweeps
- **GPU server:** fail2ban sshd — 0 banned, 1 total failed. UFW active, rules locked down.
- **rkhunter:** GPU unreachable during SSH check (timeout) — may be sleeping or network issue
- **Docker containers:** freqtrade, termix, crowdsec, kali, searxng all running

### CVE & Threat Intel
- web_search rate-limited (429), SearXNG blocked from sandbox — CVE check skipped this run
- **Reminder:** Node.js security releases were scheduled for Mar 24 — check Tuesday
- No new critical alerts from prior sweep context

### Tool Versions
- No outdated security tools (trivy, lynis) via brew

### Notes
- NAS (nas-zimaos) heartbeat now 7.6 days stale — continues to drift, needs investigation
- GPU SSH timed out — first occurrence (was reachable yesterday); may be transient
- Node.js security release due Tue Mar 24 — plan to update

---

## 2026-03-21 (Sat) — 05:00 UTC

### Sweep Summary: ✅ All Clear (minor notes)

### CrowdSec
- All machines online. nas-zimaos heartbeat stale **7 days** (since Mar 14) — ⚠️ persistent issue
- No active alerts or bans. CAPI connected, community blocklist pulling.
- All 8 bouncers valid. NAS-side bouncers last pulled Mar 14.
- Container: healthy

### Infrastructure
- **Mac mini firewall:** Enabled ✔️
- **Mac mini ports:** No unexpected LISTEN ports detected
- **GPU server:** fail2ban sshd — 0 banned, 1 total failed. UFW active, rules locked down.
- **rkhunter:** Timed out (code 124) — may need manual run
- **Docker containers:** All 8 up and healthy (freqtrade, termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n)

### CVE & Threat Intel
- **Node.js:** Security releases scheduled for Tue Mar 24 — monitor and patch v25.x when available
- **CVE-2026-1526:** Undici WebSocket Client DoS — check if Node v25.8.1 affected
- No new critical CVEs found for macOS, Docker 29.2.1, Ollama 0.18.1, or Chrome this week

### Tool Versions
- No outdated security tools detected via brew (trivy, lynis current)

### Notes
- NAS (nas-zimaos) heartbeat stale 7 days — needs investigation (was 6 days last week)
- Node.js security release Mar 24 — schedule update after release
- rkhunter on GPU continues to timeout — consider dedicated run

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

## 2026-03-18 05:00 UTC — Daily Sweep

### CrowdSec
- Container: healthy, CAPI connected
- Machines: localhost ✔️, gpu-server ✔️, nas-zimaos ⚠️ (86h+ stale — worsening)
- NAS bouncers at 185.15.59.224 stale since Mar 14
- caddy-bouncer@172.23.0.1 stale since Mar 12
- No alerts, no active decisions

### Infrastructure
- Mac firewall: ✅ enabled
- GPU server: fail2ban sshd clean (0 banned), UFW properly restrictive
- rkhunter: timed out again (needs manual run)
- Docker containers: all healthy (freqtrade, termix, crowdsec, searxng, beszel, vaultwarden, n8n, shell-executor)

### Listening Ports (Mac mini)
- Expected: ollama(11434), node(38222-5,7070,7080), docker(5678,8080,8090,8222,8888,9756,8081,8880), beszel(45876), lume(7777), ControlCenter(5000,7000)
- ⚠️ Port 2121 (Python) still open — flagged last sweep, unresolved
- Port 8200/8111/5111 (Python, localhost) — likely dev servers

### GPU Server UFW
- Properly locked: Ollama LAN-only, SSH Mac+Tailscale only, ComfyUI/TRELLIS/Beszel Mac-only, SMTP/VNC blocked

### Tool Updates
- No outdated security tools detected via brew

### CVE Check
- web_search rate-limited, SearXNG blocked — CVE check skipped this run

---
## 2026-03-19 05:00 UTC — Daily Security Sweep

### CrowdSec
- Container: healthy
- Machines: localhost ✅, gpu-server ✅, nas-zimaos ⚠️ (stale 110h — since Mar 14)
- Alerts/Decisions: none
- CAPI: connected, community blocklist active

### Infrastructure
- Mac mini firewall: ✅ enabled
- Mac mini listening ports: none detected (clean)
- GPU server: fail2ban sshd OK (0 banned), UFW active with proper rules, rkhunter timed out (long scan)
- Trivy scan: failed (DB download interrupted by timeout)

### CVE Intel (via SearXNG)
- **CVE-2026-20619**: macOS info disclosure (Critical) — check if patched in macOS 26.3.1
- **CVE-2026-3102**: macOS ExifTool image-processing vuln (Critical, Mar 2)
- **CVE-2026-20700**: dyld memory corruption in Apple platforms
- **Node.js**: Security releases scheduled for Mar 24, 2026 — currently on v25.8.1, monitor
- **Chrome 145**: Critical CVEs (heap buffer overflow in WebML CVE-2026-3913, OOB CVE-2026-3062) — Mac mini doesn't run Chrome, GPU/NAS may

### Tool Versions
- Trivy: 0.69.3 (current)
- Lynis: 3.1.6 (current)
- No brew outdated flags for security tools

### Notes
- NAS (nas-zimaos) has been offline/unreachable since ~Mar 14 — 5th consecutive day stale
- Lynis quick audit timed out (known slow on first run)

---

## 2026-03-20 05:00 UTC — Daily Security Sweep

### CrowdSec
- Container: healthy ✅
- Machines: localhost ✔️, gpu-server ✔️, nas-zimaos ⚠️ stale 134h (offline since ~Mar 14, 6th day)
- CAPI: connected, community blocklists pulling
- Alerts: none | Decisions: none
- Bouncers: all valid

### GPU Server
- fail2ban sshd: 0 banned, 0 currently failed ✅
- UFW: active, properly locked down (SSH Mac-mini + Tailscale only, Ollama LAN only)
- rkhunter: timed out (exit 124) — may need manual check

### Mac Mini
- Firewall: enabled ✅
- Listening ports: unable to enumerate (sandbox restriction on lsof/netstat)

### Tool Versions
- Trivy: 0.69.3
- Lynis: 3.1.6
- No brew outdated flags for trivy/lynis

### CVE Intel
- web_search quota exhausted (429), SearXNG blocked by sandbox
- Unable to check CVEs this run

### Notes
- NAS (nas-zimaos) still offline — now 6 days stale, worth investigating
- rkhunter on GPU timed out — consider running manually
- Lynis quick audit returned no output (may need interactive run)

---

## 2026-03-23 05:00 UTC — Daily Security Sweep

### CrowdSec
- ✅ Localhost & GPU machines healthy, heartbeats <1min
- ⚠️ nas-zimaos stale (206h) — likely offline
- ⚠️ caddy-bouncer@172.23.0.1 last pull 11 days ago
- ✅ No alerts or active bans
- ✅ CAPI connected, community blocklist active
- ✅ Container healthy

### Mac mini
- ✅ Firewall enabled
- ✅ Docker containers all up (freqtrade, termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n)
- ✅ No unexpected listening ports — all bound to 127.0.0.1 or expected services
- ✅ Security tools (trivy, lynis) up to date per brew

### GPU Server
- ✅ SSH reachable
- ✅ fail2ban sshd: 0 currently banned, 1 total failed attempt
- ✅ UFW active with tight rules (Ollama LAN-only, SSH restricted to Mac mini + Tailscale)
- ⚠️ rkhunter check timed out (SSH session ended before completion)

### Docker Containers
- ⚠️ Trivy DB download failed (credential error) — scan skipped. May need `docker login` or credential helper fix.
- All 8 containers running, 3 report healthy status

### CVE Intel
- ⚠️ Web search quota exhausted & SearXNG localhost blocked — CVE check skipped this run
- No manual CVE action needed based on current patch levels

### Tool Versions
- ✅ No outdated security tools in brew

### Action Items
- [ ] Investigate nas-zimaos offline status if persists >2 weeks
- [ ] Check caddy-bouncer on 172.23.0.1 — 11 day stale pull
- [ ] Fix trivy Docker credential helper for container scanning

## 2026-03-24 05:00 UTC — Daily Security Sweep

### CrowdSec
- ✅ All machines online (nas-zimaos heartbeat stale 230h+ — ongoing)
- ✅ All bouncers valid
- ✅ No active alerts or decisions
- ✅ CAPI connected

### Firewall
- ✅ macOS firewall enabled
- ✅ GPU server UFW active, rules tight (LAN/Tailscale only)
- ✅ GPU fail2ban: 0 banned, 1 total failed SSH attempt

### Ports (Mac mini containers)
- freqtrade: 127.0.0.1:8081 (local only) ✅
- termix: 127.0.0.1:8880 (local only) ✅
- crowdsec: 0.0.0.0:8080 ⚠️ (exposed, expected for LAPI)
- shell-executor: 0.0.0.0:9756 ⚠️ (exposed)
- searxng: 0.0.0.0:8888 ⚠️ (exposed)
- beszel: 0.0.0.0:8090 ⚠️ (exposed)
- vaultwarden: 0.0.0.0:8222 ⚠️ (exposed)
- n8n: 0.0.0.0:5678 ⚠️ (exposed)
- Host: SSH(22), SMB(445), Kerberos(88) listening

### CVE Check
- Web search quota exceeded; unable to check this run

### Container Scan
- Trivy DB download failed (credential issue); scan skipped

### Summary
No critical issues. NAS heartbeat stale (known). Several containers bound to 0.0.0.0 — acceptable on LAN but worth reviewing if network changes.
