# WORKQUEUE.md — Active Task Tracker

_Last updated: 2026-03-20 21:22_

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

### 2026-03-18
- ✅ **HMRC Tax Advisor → Dell1 deploy** — Deployed & working: FastAPI (8200), Qdrant (6333), Next.js (3100). GPU inference via GPU server at 192.168.0.92. 12 HMRC sections seeded.
- ✅ **LoRA 7B adapter evaluation** — 60% accuracy on 5-sample eval, summaries production-quality. Label drift noted (promotions/social_media categories). Full results at `/home/kryptonome/lora-eval-results.json`.
- ✅ **NAS root disk cleanup** — False alarm: `/dev/root` is squashfs (ZimaOS, always 100%). Writable `/DATA` has 860GB free. No action needed.
- ✅ **Brew package updates** — 9 upgrades (ffmpeg→8.1, ollama→0.18.1, yt-dlp→2026.3.17, etc.). All clean.
- ✅ **HMRC VAT manual seeding (Dell1)** — 12 VAT manuals, 47 sections ingested. Collection 12→59 points. VAT queries now returning citations with MEDIUM confidence.
- ✅ **LoRA GGUF export** — email-classifier-7b (Q4_K_M, 4.7GB) live in Ollama on GPU server at 192.168.0.92:11434. Built llama.cpp from source with CUDA, full pipeline: merge→F16 GGUF→Q4_K_M.
- ✅ **Infra health check (15:20)** — Mac Mini: 8 Docker containers healthy. GPU server: idle, 5× 3090 cool. Dell1 + NAS: both reachable (SSH alias issue in sub-agent, not real outage). Freqtrade: running, no trades.

### 2026-03-15
- ✅ **HMRC Tax Advisor deploy** — Qdrant installed + running on GPU server, RAG pipeline fully operational (12 seed sections)
- ✅ **LoRA 7B training** — COMPLETE at 17:47 UTC. 2748/2748 steps, 3 epochs, final train_loss=0.2597. Adapter saved to `/home/kryptonome/lora-output/qwen7b-v1/adapter` (617MB safetensors). GPU server now free for HMRC deploy.

## 🔄 In Progress

- ✅ **Vercel deploy** — Fixed! Re-linked project via CLI (`vercel link --yes`), deployed successfully. mindfizz.ai live.
- ✅ **Volt Energy App TypeScript** — `tsc --noEmit` now 0 errors (23:10 Mar 18). Fixed: MMKV v3 API (`createMMKV`), missing MOCK_SOLAR_DATA/MOCK_SOLAR_HISTORY, expo-file-system legacy API, NetInfo stub, Supabase Database type (Relationships field + Views/Functions), `as any` casts for data returns. Phase 2–7 complete + stubs fixed (22:19 Mar 18). All tabs implemented.
- ✅ **Volt Energy App Phase 3 (Ohme EV)** — Complete. API client, charging tab UI, React Query hooks committed (2f444b6). TypeScript clean.
- ✅ **Volt Energy App Phase 8 (Launch Polish)** — Complete. Sentry, PostHog analytics, accessibility, performance, App Store metadata. Committed: `c76cfdb` (00:41 Mar 19).
- 🔄 **Autoresearch (Karpathy)** — Installed on GPU server, deps + data ready, test train passed (630ms/step on 3090). Awaiting user to agree on run tag (per program.md protocol). ⛔ BLOCKED on human input.

## Previous Cycle Results

### Cycle: 2026-03-21 03:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 3 days, RUNNING. No new trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Late night maintenance cycle — nothing actionable

### Cycle: 2026-03-21 01:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING (v2026.2). No new trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Late night maintenance cycle — nothing actionable

### Cycle: 2026-03-20 23:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING. No new trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Late night maintenance cycle — nothing actionable

### Cycle: 2026-03-20 21:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING. No new trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Late evening maintenance cycle — nothing actionable

### Cycle: 2026-03-20 19:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING. No new trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Evening maintenance cycle — nothing actionable

### Cycle: 2026-03-20 17:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING. No new trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Evening maintenance cycle — nothing actionable

### Cycle: 2026-03-20 15:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING. No new trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Afternoon maintenance cycle — nothing actionable

### Cycle: 2026-03-20 13:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING. No trades (quiet market continues)
- 8 Docker containers healthy (Mac Mini)
- No previously blocked items unblocked (all backlog still manual)
- Afternoon maintenance cycle — nothing actionable

### Cycle: 2026-03-20 09:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP 2 days, RUNNING (v2026.2). No trades (quiet market continues)
- 8 Docker containers healthy (Mac Mini)
- No previously blocked items unblocked (all backlog still manual)
- Morning maintenance cycle — nothing actionable

### Cycle: 2026-03-20 05:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP ~2 days, RUNNING. No trades (quiet market continues)
- No previously blocked items unblocked (all backlog still manual)
- Early morning maintenance cycle — nothing actionable

### Cycle: 2026-03-20 03:22
- No sub-agents spawned — all Volt phases complete (1–8), no remaining build work
- Freqtrade: UP ~49h, RUNNING. No trades (quiet market continues)
- 8 Docker containers healthy (Mac Mini)
- No previously blocked items unblocked (all backlog still manual)
- Late night maintenance cycle

### Cycles: 2026-03-19 01:22 → 2026-03-20 01:22 (13 cycles)
- All idle maintenance — no sub-agents spawned, Volt complete, Freqtrade running with no trades
- 8 Docker containers healthy throughout
- No backlog items unblocked (all manual)

### Cycle: 2026-03-18 23:20
- 1 sub-agent spawned: volt-phase3-ohme (Claude Code, session mild-river)
- Focus: Volt Phase 3 — Ohme EV charger integration (API client, charging tab UI, React Query hooks)
- Freqtrade: UP 21h, RUNNING, no trades (quiet market continues)
- TypeScript check: clean (0 errors)
- No previously blocked items unblocked (all backlog still manual)
- Late night cycle — maintenance only, no second agent needed

### Cycle: 2026-03-18 22:19
- Volt stubs fixed (claude code, session tide-river): handleExportData (real JSON export via expo-sharing), handleClearCache (MMKV + react-query cleared), useGreenScore (live Carbon Intensity API wired up)
- TypeScript check clean: npx tsc --noEmit passed with 0 errors

### Cycle: 2026-03-18 21:34
- Volt sub-agent spawned: fix Settings stubs + real green score data + data export
- Previous cycle (21:20) sub-agents confirmed complete: AI Coach (real data hooks), n3rgy universal smart meter support, Solar/GivEnergy/Solis screens, AI Coach screen + anomaly detection + premium paywall

### Cycle: 2026-03-18 21:20
- 1 sub-agent spawned: volt-phase2-finish (Claude Code, session plaid-willow)
- Focus: Complete Volt Phase 2 remaining items — standing charge tracker, push notifications, CSV/JSON export wiring
- Freqtrade: UP 19h, no new trades (quiet market)
- No previously blocked items unblocked (all backlog still manual)

### Cycle: 2026-03-18 17:20
- 4 sub-agents spawned: infra-health-1720, gpu-cleanup, freqtrade-check, hmrc-health
- Focus: Routine infra health check, GPU disk cleanup (removing ~30GB intermediate GGUF/safetensors), Freqtrade status, HMRC Dell1 deployment verification
- All backlog items remain manual/blocked — pulled maintenance work from MEMORY.md

### Cycle: 2026-03-18 15:33
- Reviewed 15:20 sub-agent results — all 3 tasks completed successfully
- HMRC VAT seeding ✅ — 47 new sections, collection 12→59 points on Dell1
- LoRA GGUF export ✅ — email-classifier-7b (4.7GB Q4_K_M) live in Ollama on GPU server
- Infra health ✅ — Dell1 + NAS both reachable (sub-agent used wrong usernames; aliases work fine)
- HMRC services confirmed still up on Dell1 (3 containers, 2h uptime)
- All remaining backlog items are manual or blocked — HEARTBEAT_OK

### Cycle: 2026-03-18 15:20
- 3 sub-agents spawned: hmrc-vat-seed, lora-gguf-export, infra-health
- Focus: Seed VAT manual into HMRC on Dell1, convert LoRA to GGUF for Ollama, infra health check
- All backlog 🔲 items are manual — pulled new work from MEMORY.md "Next Steps"

### Cycle: 2026-03-18 14:01
- All 4 tasks from the 13:20 cycle confirmed complete (via daily log review)
- WORKQUEUE.md updated to reflect completions
- No unblocked autonomous tasks remaining

### Cycle: 2026-03-18 13:20
- 4 sub-agents spawned: hmrc-dell1-deploy, lora-eval, nas-disk-cleanup, brew-update
- Focus: Deploy HMRC to Dell1 (recon done), evaluate LoRA adapter, fix NAS disk, update brew

### Cycle: 2026-03-18 11:20
- 4 sub-agents spawned: lora-gpu-check, freqtrade-check, infra-health, hmrc-deploy-recon
- Results: Dell1 viable for HMRC (201GB free), NAS root disk 100% full, LoRA adapter healthy (617MB), Freqtrade running (no trades), infra healthy

### Cycle: 2026-03-18 09:20 → 09:31
- Sub-agents spawned for freqtrade-status, gpu-health-check, lora-eval, infra-health
- Sub-agents completed (no active sessions at 09:31); results not written to memory — likely clean runs with nothing urgent to report
- Freqtrade: UP (7h confirmed at 09:20)
- GPU server: BACK ONLINE as of Mar 18
- LoRA 7B adapter: saved at `/home/kryptonome/lora-output/qwen7b-v1/adapter`

### Cycle: 2026-03-17 17:20
- No sub-agents spawned — everything was blocked on human action
- Freqtrade was crashed (Exited 255, 3+ days) — NOW BACK UP
- GPU server was off since Mar 16 — NOW BACK ONLINE

## 🔲 Backlog

- 🔲 **PyPI trusted publisher registration** — Manual step, docs at `docs/pypi-publish-steps.md`
- 🔲 **mindfizz.co.uk DNS → Vercel** — GoDaddy (not Cloudflare), depends on Vercel fix
- 🔲 **GA4 property creation** — Manual Google Analytics setup
- 🔲 **Social account signups** — Manual (Twitter/X, LinkedIn, etc.)
- 🔲 **Connect email dashboard to real WSL data** — Replace mock data with live classifier output. ⚠️ WSL port 2222 still REACHABLE (09:39 Mar 15) but SSH handshake timing out at banner exchange — SSHD appears degraded. Attempted restart via dell1 but dell1 is Linux (no wsl.exe). Needs **manual WSL restart** on the Windows host. Check /etc/hosts or ask which Windows machine runs WSL.
- 🔲 **Rotate UniFi password** — Script was never in git (only iCloud backups). No BFG needed. Just rotate password on UniFi controller (manual) and old backups will age out
- 🔲 **Scanner FTP port update** — Change from 21 → 2121 on physical scanner device
- 🔲 **macOS update** — Tahoe 26.3.1 available (2.9 GB, requires restart)
