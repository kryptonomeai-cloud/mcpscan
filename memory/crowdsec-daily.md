# CrowdSec Daily Status — 2026-03-22

## Machines
| Name | Status | Last Heartbeat |
|------|--------|----------------|
| localhost (Mac mini) | ✔️ | 8s ago |
| gpu-server | ✔️ | 37s ago |
| nas-zimaos | ⚠️ | **182h27m ago (~7.6 days)** |

## Bouncers
All 7 bouncers valid. Active ones pulling regularly:
- nas-fw-bouncer@172.23.0.1 — last pull 05:02
- gpu-firewall-bouncer@172.23.0.1 — last pull 05:02
- NAS-based bouncers (185.15.59.224) — last pull Mar 14 (stale, matches NAS offline)

## Alerts & Decisions
- No active alerts
- No active decisions (bans)

## CAPI
- Connected, community subscription
- Signal sharing: enabled
- Blocklist pull: enabled

## Container Health
- crowdsec container: **healthy**

## ⚠️ Issues
- **nas-zimaos machine heartbeat stale (7+ days)** — NAS may be offline or CrowdSec agent stopped
- NAS-based bouncers also stale (last pull Mar 14)
