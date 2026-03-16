# Port Hardening Audit — 2026-03-14

## Summary

4 ports were flagged as potentially bound to 0.0.0.0. Audit results:

| Port | Service | Bound To | Status |
|------|---------|----------|--------|
| 7070 | OpenClaw node (browser control) | 127.0.0.1 ✅ | Already secure |
| 7080 | OpenClaw node (browser control) | 127.0.0.1 ✅ | Already secure |
| 18799 | Emergency Gateway Restart (Python) | 0.0.0.0 ⚠️ | **Intentional** — LAN access needed |
| 8880 | Docker container | 127.0.0.1 ✅ | Already secure |

## Details

### Port 7070 & 7080 — OpenClaw Node Processes
- **PID:** 29305 (7070), 29317 (7080)
- **Process:** `node`
- **Binding:** `127.0.0.1` — localhost only
- **Action:** None needed. Already properly secured.

### Port 18799 — Emergency Gateway Restart Web Server ⚠️
- **PID:** 1422
- **Process:** Python (`scripts/restart-web.py`)
- **Binding:** `*` (0.0.0.0) — all interfaces
- **Purpose:** Emergency restart button accessible from phone/LAN when OpenClaw is completely dead
- **Mitigations already in place:**
  - IP-based access control: only allows `192.168.*`, `127.0.0.*`, `10.*`, `100.*` (LAN + Tailscale)
- **Action:** **Keep as-is.** This is intentionally LAN-accessible for emergency recovery scenarios. The IP allowlist provides reasonable protection. Consider adding:
  - A simple shared secret/token query param for defense-in-depth
  - Rate limiting to prevent abuse

### Port 8880 — Docker Container
- **PID:** 80273
- **Process:** `com.docker` (Docker Desktop)
- **Binding:** `127.0.0.1` — localhost only
- **Action:** None needed. Already properly secured.

## Conclusion

3 of 4 ports were already bound to 127.0.0.1. The only 0.0.0.0-bound port (18799) is intentionally exposed for LAN emergency access with IP-based ACLs. **No immediate action required.**
