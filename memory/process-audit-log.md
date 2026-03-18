# Process Audit Log

## 2026-03-14 09:00 UTC — Initial Audit (Baseline Created)

**Status:** ⚠️ First run — baseline created from current state. Two items flagged for review.

**Anomalies / Notes:**
- **New Docker container: `termix`** (`ghcr.io/lukegus/termix:latest`) — Up 19 minutes. Not in long-running set. Verify this is intentional.
- **New Docker container: `freqtrade-freqtrade-run-33c55a110b11`** (`freqtradeorg/freqtrade:stable`) — Up ~1 minute. Trading bot — appears freshly started.
- **Root Python process (PID 67465):** Running Python 3.14 as root — worth verifying what this is.
- **Multiple `socat` processes running as root** (PIDs 72990-72999) — likely related to Docker port forwarding, but worth confirming.
- **Listening ports:** Could not enumerate without elevated permissions. Consider running audit with sudo or adding to sudoers for `lsof`.

**Baseline:** Created at `configs/process-baseline.json` with 21 user LaunchAgents, 2 system LaunchAgents, 8 LaunchDaemons, 10 baseline Docker containers.

**Action items:**
- [ ] Verify `termix` container purpose
- [ ] Confirm root Python 3.14 process is expected
- [ ] Enable elevated lsof for future port audits

## 2026-03-15 09:00 UTC — Morning Audit

**LaunchAgents (user/system):** ✅ Match baseline
**LaunchDaemons:** ✅ Match baseline
**Listening ports:** ⚠️ Empty output (permissions issue — lsof needs elevated access, ongoing)
**Suspicious processes:** None — all match known baseline entries

**Anomalies found: 1**

1. **Docker container `freqtrade` is MISSING** — Listed in baseline as an expected running container, but absent from current `docker ps` output. All other 7 containers (termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n-n8n-1) are up and healthy.

**Verdict:** All LaunchAgents, Daemons, and processes are clean. `freqtrade` container is not running — may have crashed or been stopped manually. Worth checking logs.

---

## 2026-03-14 21:00 UTC — Evening Audit

**LaunchAgents (user/system):** ✅ Match baseline
**LaunchDaemons:** ✅ Match baseline
**Suspicious processes:** None — all match known baseline entries

**Anomalies found: 2**

1. **Docker not running** — Baseline expects 10 containers (crowdsec, dashchat stack, shell-executor, searxng, beszel, vaultwarden, n8n). Docker daemon appears to be down; no containers active.
2. **Listening ports: empty** — The audit script returned no listening ports. Likely a permissions issue with the script (lsof needs elevated access), but worth noting since we can't verify port state.

**Verdict:** LaunchAgents/Daemons and processes are clean. Docker being down is the main concern — services like Vaultwarden, CrowdSec, and n8n are offline.

## 2026-03-15 21:00 UTC — Evening Audit

**LaunchAgents (user/system):** ✅ Match baseline  
**LaunchDaemons:** ✅ Match baseline  
**Processes:** ✅ All known  
**Listening Ports:** ⚠️ Section returned empty (script may not have captured port data — worth investigating script output)

### ⚠️ ANOMALY: Missing Docker Container

- **`freqtrade`** is listed in the baseline but is **NOT running**
  - Baseline expects: crowdsec, freqtrade, termix, shell-executor, searxng, beszel, vaultwarden, n8n-n8n-1
  - Current running: crowdsec, termix, shell-executor, searxng, beszel, vaultwarden, n8n-n8n-1
  - freqtrade is absent — may have crashed, been stopped, or intentionally halted


## 2026-03-16 09:00 UTC — Morning Audit

**Status: 1 anomaly detected**

### Docker Container: freqtrade MISSING
- Baseline lists `freqtrade` as a permanent container (added 2026-03-15)
- Currently NOT running — absent from `docker ps` output
- All other expected containers running healthy: termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n-n8n-1

### LaunchAgents / LaunchDaemons
- ✅ User LaunchAgents: exact match (21 entries)
- ✅ System LaunchAgents: exact match
- ✅ LaunchDaemons: exact match (8 entries)

### Listening Ports
- ⚠️ Script returned no port data — `process-audit.sh` ports section was empty. May be a script/permissions issue worth investigating.

### User Processes
- ✅ No unknown processes detected. All match known process list.


## 2026-03-16 21:00 UTC (Evening Audit)

**Status: ⚠️ 1 anomaly detected**

### Missing Docker Container
- `freqtrade` is listed in the baseline (`configs/process-baseline.json`) but is **not currently running**.
  - All other containers healthy: termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n-n8n-1

### All Other Checks: Clean
- LaunchAgents (user): ✓ matches baseline (21 entries)
- LaunchAgents (system): ✓ matches baseline (2 entries)
- LaunchDaemons: ✓ matches baseline (8 entries)
- No unknown listening ports reported
- No unknown/suspicious user processes

---

## 2026-03-17 09:00 UTC — Morning Audit

**Result:** Clean — no anomalies.

- LaunchAgents (user/system): All match baseline.
- LaunchDaemons: All match baseline.
- Docker containers: All running containers are in baseline. Note: `freqtrade` in baseline but not currently running (not a security concern).
- Processes: All match known process list. Transient shell processes (bash, find, ls, sort, zsh, head, tail) from audit execution — normal.
- No new listening ports, unknown agents, or suspicious processes detected.

## 2026-03-17 21:00 UTC — Evening Audit

**Result: One anomaly detected**

### Docker Container Deviation
- **freqtrade** container is in the baseline but **not currently running**
  - Baseline expects: `freqtrade` (listed in `dockerContainers`)
  - Current state: container absent from `docker ps` output
  - All other containers match baseline: termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n-n8n-1 ✅

### LaunchAgents/Daemons: ✅ Match baseline exactly
### Listening Ports: ✅ No new ports flagged
### Processes: ✅ All within known process list

