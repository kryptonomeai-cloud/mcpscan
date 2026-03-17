# CrowdSec Daily Status — 2026-03-16 05:00 UTC

## Machines
| Name | Status | Last Heartbeat |
|------|--------|----------------|
| localhost (Mac mini) | ✔️ | 56s ago |
| gpu-server | ✔️ | 19s ago |
| nas-zimaos | ✔️ | ⚠️ **38h 25m ago** |

## Bouncers
All 8 bouncers valid. Notable:
- `nas-fw-bouncer` & `caddy-bouncer` (185.15.59.224) last pulled ~38h ago (tracks NAS being stale)
- `gpu-firewall-bouncer@172.23.0.1` & `nas-fw-bouncer@172.23.0.1` active and current

## Alerts & Decisions
- No active alerts
- No active decisions (bans)

## CAPI
- ✔️ Connected to Central API
- Community subscription, sharing enabled, blocklist pull enabled

## Container Health
- `crowdsec` container: **healthy**

## ⚠️ Issues
- **nas-zimaos heartbeat stale (38h)** — machine may be offline or CrowdSec agent stopped
