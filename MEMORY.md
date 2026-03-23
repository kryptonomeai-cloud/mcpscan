# MEMORY.md — Long-Term Memory

_Curated knowledge. Updated: 2026-03-22 (memory maintenance review)._

---

## Infrastructure

### MiniClaw (Mac mini)
- macOS Tahoe 26.3.1, ARM64
- Runs OpenClaw gateway, Docker services, cron jobs (26 total, 20 enabled, 6 disabled MOSS agents)
- Restic backup → GPU server via REST (SSH tunnel), NOT NAS. 10 snapshots retained.
- CrowdSec v1.7.6 (Docker-only), healthy, 8 bouncers valid
- Ports hardened: 7070/7080/8880 rebound to 127.0.0.1; 18799 left open (phone LAN access, IP whitelist)
- **NordVPN installed** (LaunchDaemon: `com.nordvpn.macos.helper.plist`, added to baseline Mar 21)
- **New LaunchAgents**: ComfyUI MCP Server, OpenMOSS server (added to baseline Mar 22)
- macOS background security update pending ("25D771280a", 208MB, requires restart)

### GPU Server (192.168.0.92)
- 5× RTX 3090 (120 GB VRAM total), 125 GB RAM, 1.2 TB free disk
- **SSH alias: `gpu`** (not `gpu-server` — hostname doesn't resolve)
- Ollama active, Qwen 32B model cached (62 GB)
- Training stack: unsloth 2026.3.3, torch 2.10.0+cu128
- **Always use tmux** for training — SSH timeout kills processes
- FSDP DDP recommended over unsloth balanced mode (~5-7s/step vs 46s/step)
- GPU 0 runs ComfyUI venv process
- SSH publickey auth intermittently fails — has resolved itself multiple times
- **HMRC Tax Advisor backend deployed** (port 8001, tmux session `hmrc`, bound to 127.0.0.1)

### NAS (nas-zimaos) — ⚠️ Offline
- CrowdSec agent offline since ~Mar 14 (8+ days stale as of Mar 22)
- NAS-side bouncers last pulled Mar 14
- **Needs investigation** — possibly sleeping or agent stopped

### Paperless
- Backup: ~1.4 MB daily export to iCloud (working, verified Mar 22)
- iCloud cleanup of old backups may lag due to sync issues
- Scanner FTP port moved from 21 → 2121 (scanner device still needs updating)

---

## Projects

### MCPScan (v0.2.0) — ✅ Released
- **Repo:** GitHub, under Fyzi Security
- Static security scanner for MCP server configs
- 10 check modules, 40+ rules, 6 config formats supported
- v0.2.0: HTML reports, SARIF output, diff mode, 132 tests passing
- v0.1.0: 83 tests, README polished, CHANGELOG created
- GitHub release published; PyPI publish needs trusted publisher setup (OIDC workflow ready)
- Product page live on MindFizz website
- **Next:** PyPI trusted publisher registration (manual, docs at `docs/pypi-publish-steps.md`)

### Freqtrade — 🔄 Paper Trading (Zero Trades — Awaiting Decision)
- **3 profitable strategies** from deep optimisation (500-epoch hyperopt):
  - **EMACrossOptimised** ⭐ — +1.64% (6mo), 94% win rate (16/17 trades), 0.12% max drawdown
  - **BearShortOptimised** — +2.75% (3mo), 30-36% win rate, futures shorting
  - **MomentumOptimised** — +1.45% (6mo), 37-39% win rate
  - Failed: MeanReversion (-5.51%), DCA (-9.21%)
- Paper trading: EMACrossOptimised, $1000 dry-run, BTC/ETH/SOL 1h, FreqUI at localhost:8081
- **⚠️ Zero trades in 27+ hours** — not a bug, strategy is very conservative by design:
  - EMA7/44 crossover happens ~1x per 2-4 weeks per pair
  - `close > ema150` filter blocks ALL signals in bear market (likely blocking 100% of entries now)
  - Volume spike filter (1.46×) eliminates many valid crossovers
  - Only 17 trades in 6 months of backtesting = ~1 trade per 10 days
  - ROI target of 49.1% means trades take forever to close even if they open
- **Options:** Relax `ema150` filter, lower volume multiplier, add more pairs/shorter timeframe, or switch strategy
- **Next:** Human decision needed

### MindFizz Website — 🔄 Deploy Blocked
- Built with Next.js, deployed via Vercel
- **Pages:** Homepage, MCPScan product page, case studies, contact page
- **Blog:** 5 posts live
- **SEO:** robots.txt, sitemap.xml, JSON-LD structured data (24 files committed + pushed)
- **Blocked:** Vercel team permissions error (needs manual dashboard fix)
- **Next:** mindfizz.co.uk DNS (GoDaddy → Vercel), GA4 property, social account signups

### HMRC Tax Advisor — ✅ Deployed to GPU Server
- **Backend:** GPU server port 8001 (tmux session `hmrc`, bound to 127.0.0.1 — needs SSH tunnel or `--host 0.0.0.0` for remote access)
- **Frontend:** localhost:3000 (Mac mini)
- **Fix:** Qwen3:32b is a thinking model — added `"think": False` to all Ollama `/api/generate` calls
- Also: `keep_alive: "24h"`, timeouts increased to 300s
- bge-m3 embedding model pulled on GPU server (1.2 GB), Qdrant on NAS (192.168.0.18:6333)
- Test results: VAT threshold → HIGH confidence (5 citations, ~60s), Self assessment → HIGH confidence (5 citations, 87s)

### Email Classifier Dashboard — 🔄 Needs Real Data
- React + Tailwind dashboard built with mock data
- Docs at `docs/email-dashboard-20260314.md`
- **Next:** Connect to real WSL classifier output

### LoRA Training — ✅ Complete
- **Dataset:** 30,511 email→summary pairs (14,644 used for training)
- **Completed runs:** Qwen 7B (3 epochs, 2,748 steps, ~26-30s/step), Qwen 32B (checkpoint-500)
- Output: `~/lora-output/qwen7b-v1/` on GPU server
- Previous attempts: 70B partially done, 8B crashed (GGUF conversion EOFError)
- Axolotl failed (torch version mismatch — needs 2.8.0, server has 2.10.0)
- **Lesson:** DDP tries full model per GPU → OOM. Use QLoRA + device_map="balanced" instead
- Docs at `docs/lora-training-setup-20260314.md`

---

## Security

- Credential audit: 1 hardcoded UniFi password found, moved to Keychain. Need to rotate + BFG scrub.
- Port audit: 3 ports rebound to localhost. MongoDB/MySQL/Telnet/RDP on 0.0.0.0 flagged (higher priority).
- FTP port 21 → 2121 (non-privileged)

---

## Lessons Learned

- **Qwen3 thinking mode:** Always use `"think": false` in Ollama API calls for Qwen3 models — output goes to `thinking` field, `response` stays empty
- **Ollama model swapping:** Pre-warm with `keep_alive: "24h"` to avoid cold-start timeouts
- **LoRA multi-GPU:** Don't try full model replicas (DDP) on multi-GPU — use QLoRA + balanced sharding
- **Vercel deploys:** Local `next build` success ≠ Vercel deploy success; team permissions can silently block
- **Backtesting ≠ live:** Hyperopt-optimised strategies can be too selective for real-time trading (EMACrossOptimised: 17 trades in 6 months, 0 in 27+ hours live)
- **Trend filters in bear markets:** `close > ema150` type filters will block 100% of entries when market is bearish — consider making these conditional or removable
- **CrowdSec NAS heartbeat:** If stale >24h, likely NAS sleeping or agent stopped — recurring issue since Mar 14

## System Health (as of Mar 22)

- MiniClaw overall healthy: 697GB free, FileVault on, SIP enabled, firewall on
- Docker: 8 containers running (freqtrade, termix, crowdsec, shell-executor, searxng, beszel, vaultwarden, n8n)
- Ollama: 4 models loaded (bge-m3, qwen3.5:27b, nomic-embed-text, qwen3:32b)
- OpenClaw: v2026.3.13 — confirmed current (npm latest = 2026.3.13, GitHub tag `-1` is recovery tag only)
- Brew: 14 outdated packages (non-critical: ca-certificates, caddy, cmake, deno, ollama, semgrep, uv, etc.)
- GPU maintenance cron job still failing — ansible playbook directory doesn't exist, needs setup or disable
- NAS CrowdSec agent offline 8+ days — needs investigation
- Node.js security releases scheduled Mar 24 — monitor and patch v25.x
- Port 2121 (Python FTP?) recurring on Mac mini — verify if intentional

## Operational Notes

- Vercel deploys blocked by team auth issue — `vercel project ls` shows no projects despite linked team. Manual dashboard fix needed.
- Scanner device needs FTP port updated from 21 → 2121
- UniFi password needs rotation + BFG git history scrub
- rkhunter on GPU server consistently times out — consider manual run or increased timeout
