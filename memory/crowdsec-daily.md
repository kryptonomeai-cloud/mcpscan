# CrowdSec Daily Status — 2026-03-21

## Machines
| Name | Status | Last Heartbeat |
|------|--------|----------------|
| localhost | ✔️ | 55s |
| gpu-server | ✔️ | 24s |
| nas-zimaos | ⚠️ | 158h (stale since ~Mar 14) |

## Bouncers
All 8 bouncers valid. gpu-firewall-bouncer and nas-fw-bouncer@172.23.0.1 pulling fresh. NAS-side bouncers last pulled Mar 14.

## Alerts & Decisions
- No active alerts
- No active decisions (bans)

## CAPI
- Connected, community subscription
- Signal sharing: enabled
- Community blocklist pull: enabled
- Console blocklist pull: enabled

## Container Health
- CrowdSec container: **healthy**
- All containers up (freqtrade, termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n)
