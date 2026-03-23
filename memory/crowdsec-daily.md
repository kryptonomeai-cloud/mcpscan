# CrowdSec Daily Status — 2026-03-23 05:00 UTC

## Machines
| Name | IP | Status | Last Heartbeat |
|------|-----|--------|----------------|
| localhost | 127.0.0.1 | ✔️ | 58s ago |
| gpu-server | 172.23.0.1 | ✔️ | 27s ago |
| nas-zimaos | 185.15.59.224 | ⚠️ | **206h stale** |

## Bouncers
All 8 bouncers valid. Notable:
- `nas-fw-bouncer@172.23.0.1` — last pull 05:00:09Z ✔️
- `gpu-firewall-bouncer@172.23.0.1` — last pull 05:00:08Z ✔️
- `caddy-bouncer@172.23.0.1` — last pull 2026-03-12 ⚠️ (11 days stale)
- NAS bouncers (185.15.59.224) — last pull 2026-03-14 ⚠️ (stale with machine)

## Alerts & Decisions
- No active alerts
- No active decisions (bans)

## CAPI
- Status: **Connected** (community)
- Signal sharing: enabled
- Blocklist pull: enabled

## Container Health
- `crowdsec` container: **healthy**

## Notes
- nas-zimaos machine offline for ~8.5 days — NAS likely powered down or network issue. Known pattern.
- caddy-bouncer on 172.23.0.1 hasn't pulled in 11 days — may need investigation if caddy is still running.
