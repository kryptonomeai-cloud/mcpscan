# HMRC Tax Advisor Backend — Deployment Result

**Date:** 2026-03-15 18:43 UTC
**Server:** GPU server (192.168.0.92, SSH alias: `gpu`, user: kryptonome)

## Summary

| Step | Status |
|------|--------|
| bge-m3 embedding model | ⚠️ Was NOT present — pulled successfully (1.2 GB, ~10s at 118 MB/s) |
| Python venv creation | ✅ Created and all deps installed (torch 2.10.0 + CUDA, sentence-transformers 3.3.1, FastAPI, etc.) |
| tmux session `hmrc` | ✅ Running |
| Health check | ✅ Uvicorn serving, `/docs` returns 200, bge-m3 warmed up |

## Service Details

- **Port:** 8001
- **URL:** `http://192.168.0.92:8001` (bound to 127.0.0.1, so only accessible locally on GPU server or via SSH tunnel)
- **tmux session:** `hmrc`
- **Log file:** `~/hmrc-tax-advisor/backend/hmrc-api.log`
- **Qdrant:** connecting to `http://192.168.0.18:6333` (NAS)
- **Ollama:** connecting to `http://localhost:11434` (local, qwen3:32b + bge-m3 available)

## Errors

None. Clean deployment.

## Notes

- The root endpoint `/` returns 404 (no route defined there) — this is normal FastAPI behaviour
- `/docs` (Swagger UI) returns 200, confirming the app is fully loaded
- bge-m3 was warmed up on startup (log shows "✓ bge-m3 warmed up")
- sentence-transformers cross-encoder model will auto-download on first query
- Service is bound to `127.0.0.1:8001` — to access from other machines, either update `--host 0.0.0.0` in start.sh or use SSH tunnel
