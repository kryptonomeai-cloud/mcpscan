# CrowdSec Daily Status — 2026-03-15 05:11 UTC

## Container Health: ✅ healthy

## Machines
| Name | Status | Last Heartbeat | Notes |
|------|--------|----------------|-------|
| localhost | ✔️ | 36s | OK |
| gpu-server | ✔️ | 26s | OK |
| nas-zimaos | ✔️ | ⚠️ 14h37m | Stale heartbeat — last seen 2026-03-14 14:34 UTC |

## Bouncers (8 total)
All valid. Notable:
- `caddy-bouncer@172.23.0.1` last pull 2026-03-12 — 3 days stale (non-critical, local)
- `gpu-server-fw` and `udm-se-bouncer` have no recorded pull (API-key only, pull-based)

## CAPI
- ✅ Connected to Central API
- Community subscription, sharing enabled, blocklist pull enabled

## Alerts & Decisions
- No active alerts
- No active decisions/bans

## Notes
- nas-zimaos heartbeat 14h+ stale — monitor tomorrow, may need container restart on NAS
