# Security Sweep — Mac Mini — 2026-03-14

## 1. Open Ports

| Port | Process | Binding | Risk |
|---|---|---|---|
| 5000, 7000 | ControlCenter (AirPlay) | `*` (all interfaces) | ⚠️ Low — macOS system service, disable if not using AirPlay |
| 49190 | rapportd | `*` | ℹ️ Low — macOS Rapport (device communication) |
| 5111 | Python (Piper TTS) | `127.0.0.1` | ✅ Local only |
| 8111 | Python | `127.0.0.1` | ✅ Local only |
| 7070 | node | `*` | ⚠️ Check — what service is this? |
| 11434 | ollama | `127.0.0.1` | ✅ Local only |
| 8443, 80 | caddy | `*` | ⚠️ Web server exposed — ensure proper config |
| 2019 | caddy (admin) | `127.0.0.1` | ✅ Local only |
| 21 | Python (FTP?) | `*` | 🔴 **HIGH RISK** — FTP on port 21 open to all interfaces |
| 7080 | node | `*` | ⚠️ Check service identity |
| 18799 | Python | `*` | ⚠️ Unknown service — investigate |
| 7777 | lume | `*` | ⚠️ VM management exposed |
| 45876 | beszel-agent | `*` | ⚠️ Monitoring agent — should be firewalled |
| 7679 | Google Chrome | `[::1]` | ✅ Local only |
| 38222, 38224 | node | `127.0.0.1` | ✅ Local only |
| **Docker ports:** | | | |
| 8080 | CrowdSec | `*` | ℹ️ Security dashboard |
| 8888 | SearXNG | `*` | ⚠️ Search engine — ensure auth |
| 8880 | Termix | `*` | ⚠️ Terminal in browser — **ensure auth** |
| 5678 | (n8n?) | `*` | ⚠️ Automation — ensure auth |
| 5432 | PostgreSQL | `127.0.0.1` | ✅ Local only |
| 8000 | Backend service | `*` | ⚠️ Check auth |
| 8080 | Freqtrade/CrowdSec | `*` | ℹ️ Already in use |
| 3000 | Frontend | `*` | ⚠️ Check exposure |
| 6379 | Redis | `127.0.0.1` | ✅ Local only |
| 8090 | Docker service | `*` | ⚠️ Check identity |
| 9756 | Docker service | `*` | ⚠️ Check identity |
| 4321, 4322, 2222 | qemu (VM) | `127.0.0.1` | ✅ Local only |

### 🔴 Critical Findings
1. **Port 21 (FTP)** open on all interfaces — this is a major security risk. FTP transmits credentials in plaintext. Investigate and disable if not needed.
2. Multiple services bound to `*` (all interfaces) without clear authentication.

## 2. CrowdSec

**Status:** ❌ Not found on host (runs in Docker container on port 8080)
- CrowdSec is containerized — host-level `cscli` not available
- Docker container appears running based on port mapping
- **Action:** Verify CrowdSec container health: `docker exec crowdsec cscli metrics`

## 3. fail2ban

**Status:** ✅ Running
- 1 jail active: `honeypot`
- **Note:** Only honeypot jail configured — consider adding SSH jail if SSH is exposed

## 4. macOS Software Updates

**Status:** ⚠️ Could not check (sandbox limitation — `softwareupdate` not available in exec environment)
- **Action:** Run manually: `softwareupdate -l`

## 5. SSH Hardening

**Status:** ✅ Good
- `PasswordAuthentication no` — password auth is disabled ✅
- Key-based authentication only ✅

## Summary

| Check | Status | Action Needed |
|---|---|---|
| Open Ports | ⚠️ | Investigate port 21 (FTP), audit services on 7070, 7080, 18799 |
| CrowdSec | ⚠️ | Verify container health, check if host-level protection active |
| fail2ban | ✅ | Consider adding more jails (SSH, etc.) |
| macOS Updates | ❓ | Check manually |
| SSH Hardening | ✅ | Properly configured |

### Priority Actions
1. 🔴 **Investigate and likely disable port 21 (FTP)** — plaintext protocol, security risk
2. ⚠️ **Audit Termix (8880)** — browser terminal needs strong auth
3. ⚠️ **Audit unknown services** on ports 7070, 7080, 18799
4. ⚠️ **Verify CrowdSec** is actually processing and blocking threats
5. ℹ️ **Consider disabling AirPlay** receiver if not in use (ports 5000, 7000)
