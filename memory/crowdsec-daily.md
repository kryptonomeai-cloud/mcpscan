# CrowdSec Daily Status — 2026-03-17 05:00 UTC

## Container Health
- **Status:** healthy
- **Uptime:** 47 hours

## Machines
| Name | Status | Last Heartbeat |
|------|--------|----------------|
| localhost | ✔️ | 55s |
| gpu-server | ✔️ | 25s |
| nas-zimaos | ⚠️ | 62h 25m (stale) |

## Bouncers
All 7 bouncers valid. Active bouncers pulling decisions:
- nas-fw-bouncer@172.23.0.1 — last pull 05:00
- gpu-firewall-bouncer@172.23.0.1 — last pull 05:00
- ⚠️ NAS bouncers (185.15.59.224) last pulled ~62h ago (matches stale machine)
- ⚠️ caddy-bouncer@172.23.0.1 last pulled 2026-03-12

## Alerts & Decisions
- No active alerts
- No active decisions/bans

## CAPI
- Connected to community API ✔️
- Console enrolled ✔️
- Signal sharing: enabled
- Community blocklist pull: enabled

## Notes
- nas-zimaos heartbeat stale for ~62h — NAS may be offline or CrowdSec agent stopped
- caddy-bouncer@172.23.0.1 hasn't pulled in 5 days — may need investigation
