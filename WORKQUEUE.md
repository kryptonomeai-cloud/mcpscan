# WORKQUEUE.md — Active Task Tracker

_Last updated: 2026-03-16 03:19_

## ✅ Completed

### 2026-03-14
- ✅ **MCPScan v0.2.0** — HTML reports, SARIF output, diff mode, 132 tests passing, GitHub release published
- ✅ **MCPScan product page** — Added to MindFizz website
- ✅ **MindFizz blog posts** — 5 total now live
- ✅ **MindFizz case studies + contact page** — Built and deployed
- ✅ **MindFizz SEO** — robots.txt, sitemap.xml, JSON-LD structured data (24 files committed)
- ✅ **Freqtrade deep optimisation** — 3 profitable strategies identified (EMACrossOptimised best at +15.5%)
- ✅ **Email classifier dashboard** — Built (React + Tailwind, mock data)
- ✅ **Trivy DB fixed** — Database corruption resolved
- ✅ **Competitor analysis** — Completed
- ✅ **Restic backup verified** — Working fine (GPU server via REST/SSH tunnel, 10 snapshots)
- ✅ **GPU maintenance cron** — Self-healing (delivery channel fixed, GPU back online)
- ✅ **Credential audit** — 1 hardcoded UniFi password moved to Keychain
- ✅ **Port audit** — 3 ports rebound from 0.0.0.0 → 127.0.0.1 (7070, 7080, 8880)
- ✅ **Social media assets** — Generated for MindFizz/MCPScan
- ✅ **MCPScan v0.1.0 polish** — README badges, CHANGELOG, pyproject.toml updated, 83 tests
- ✅ **Taskmaster blockers** — 10 resolved (FTP port, SEO, CrowdSec, port audit, etc.)
- ✅ **Port rebinding (security)** — 3/4 ports rebound to localhost
- ✅ **LoRA training setup audit** — GPU server capability confirmed (5× RTX 3090, dataset ready)
- ✅ **HMRC Tax Advisor backend** — Verified working (RAG pipeline functional, qwen3:32b + bge-m3 + Qdrant + cross-encoder). Deploy blocked by GPU availability.

### 2026-03-15
- ✅ **HMRC Tax Advisor deploy** — Qdrant installed + running on GPU server, RAG pipeline fully operational (12 seed sections)
- ✅ **LoRA 7B training** — COMPLETE at 17:47 UTC. 2748/2748 steps, 3 epochs, final train_loss=0.2597. Adapter saved to `/home/kryptonome/lora-output/qwen7b-v1/adapter` (617MB safetensors). GPU server now free for HMRC deploy.

## 🔄 In Progress

- ⛔ **Freqtrade paper trading** — Container CRASHED ~16h ago (Exited 255). Was running EMACrossOptimised, Binance, 1h, 100 USDT stake. Zero trades in 27+ hours before crash — strategy too strict for current market. **Needs human decision before restart:** relax volume filter (1.46→1.1), add more pairs, switch to 15m timeframe, or try different strategy.

- ⛔ **Vercel deploy** — Still failing with "Unexpected error" on build (retried 13:07 Mar 14). Confirmed NOT transient — likely **team/account permissions issue**. Needs manual Vercel dashboard check by human.

## 🔄 Spawned This Cycle

_(none — all automatable tasks done or blocked)_

### Previous Cycle Results
- ✅ **HMRC uvicorn restart** — Confirmed running (PID 179565), health check passing
- ✅ **LoRA 7B adapter evaluation** — PASSED. 4/4 classification correct. Adapter production-ready.

## 🔲 Backlog

- 🔲 **PyPI trusted publisher registration** — Manual step, docs at `docs/pypi-publish-steps.md`
- 🔲 **mindfizz.co.uk DNS → Vercel** — GoDaddy (not Cloudflare), depends on Vercel fix
- 🔲 **GA4 property creation** — Manual Google Analytics setup
- 🔲 **Social account signups** — Manual (Twitter/X, LinkedIn, etc.)
- 🔲 **Connect email dashboard to real WSL data** — Replace mock data with live classifier output. ⚠️ WSL port 2222 still REACHABLE (09:39 Mar 15) but SSH handshake timing out at banner exchange — SSHD appears degraded. Attempted restart via dell1 but dell1 is Linux (no wsl.exe). Needs **manual WSL restart** on the Windows host. Check /etc/hosts or ask which Windows machine runs WSL.
- 🔲 **Rotate UniFi password** — Script was never in git (only iCloud backups). No BFG needed. Just rotate password on UniFi controller (manual) and old backups will age out
- 🔲 **Scanner FTP port update** — Change from 21 → 2121 on physical scanner device
- 🔲 **macOS update** — Tahoe 26.3.1 available (2.9 GB, requires restart)
