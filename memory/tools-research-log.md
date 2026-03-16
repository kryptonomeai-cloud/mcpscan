# Tools & Skills Research Log

## 2026-03-16 — Nightly Scan #2

### Summary
Web search still rate-limited (Gemini 429). ClawHub and awesome-mcp-servers raw README scanned. GitHub now has an official **MCP Registry** (github.com/mcp) with 87+ verified servers — this is new since last scan.

### New MCP Servers Found (not in last scan)

#### High Value — New Discoveries
| Server | What | Effort | Value |
|--------|------|--------|-------|
| **GitHub MCP Registry** | Official GitHub-hosted registry with 87 verified servers. Better trust signal than awesome-mcp-servers. | Low (use mcporter) | ⭐⭐⭐⭐⭐ |
| **ViperJuice/mcp-gateway** | Meta-server: 9 stable tools, auto-starts Playwright + Context7, can provision 25+ MCP servers on-demand from a manifest. Reduces tool bloat. | Medium | ⭐⭐⭐⭐ |
| **askbudi/roundtable** | Meta-MCP unifying Codex, Claude Code, Cursor, Gemini via auto-discovery | Low (npx) | ⭐⭐⭐ |
| **YangLiangwei/PersonalizationMCP** | 90+ tools for Steam, YouTube, Spotify, Reddit personal data via OAuth2 | Medium (OAuth setup) | ⭐⭐⭐ |
| **Cifero74/mcp-apple-music** | Full Apple Music integration: search, library, playlists, recommendations | Low (local) | ⭐⭐⭐ |
| **profullstack/mcp-server** | 20+ tools: SEO, document conversion, domain lookup, email validation, QR, weather, security scanning | Low (single server) | ⭐⭐⭐ |
| **whiteknightonhorse/APIbase** | 56+ tools: travel (Amadeus, Sabre), prediction markets, crypto, weather | Medium (x402) | ⭐⭐ |

#### Finance MCP — Still Sparse
- No dedicated Xero MCP server found on awesome-mcp-servers (still need custom/mcporter approach)
- **Stripe MCP** now in GitHub's official MCP Registry — useful if doing payments
- No new banking/accounting MCP servers since last scan
- ClawHub `firefly-iii` skill exists — worth evaluating if running Firefly III Docker

### ClawHub Skills Update

#### New/Notable Skills Since Last Scan
| Skill | What | Relevance |
|-------|------|-----------|
| `uptime-kuma` | Uptime Kuma integration | High — if we deploy Uptime Kuma |
| `firefly-iii` | Firefly III personal finance | Medium — alternative to Xero for personal |
| `ollama-local` | Ollama integration | Already have ollama, but skill could streamline |
| `xero` / `xero-cli` | Xero accounting | High — check if these actually work |
| `mcp-hass` | Home Assistant via MCP | Still there, relevant if HA deployed |
| `clickup-mcp` | ClickUp project management | Medium — if using ClickUp |
| `atlassian-mcp` | Jira + Confluence | Medium — if using Atlassian |
| `wordpress-mcp` | WordPress management | Low — unless managing WP sites |

#### Caution — Skip These
- Most "automation-workflows" and "productivity" skills are generic/low-quality
- `afrexai-*` skills look template-generated, not production-ready
- Agent network / marketplace skills (agenium, agentnet, etc.) — immature ecosystem

### Ecosystem Notes
- **awesome-mcp-servers** now has 863 pending PRs (up from ~850 last scan) — ecosystem still growing fast
- GitHub's official MCP Registry is the new trust anchor — 87 servers, curated
- x402 micropayment MCP servers emerging (blockrun, APIbase, satring) — pay-per-API-call trend
- Agent-to-agent MCP marketplace is a growing theme but not production-ready yet

### Action Items (Carry Forward)
1. ⚠️ **Fix Xero MCP server** — still offline, still #1 priority
2. 📊 **Deploy Uptime Kuma** — quick Docker deploy, real monitoring value
3. 🔍 **Install Anyquery** — still top recommendation, not done yet
4. 🛠️ **Install lazydocker** — still not done
5. 🆕 **Evaluate `xero` ClawHub skill** — might be easier than MCP approach
6. 🆕 **Check GitHub MCP Registry** for officially verified servers to add via mcporter
7. 🆕 **Evaluate mcp-gateway** (ViperJuice) — could simplify MCP server management

### Next Scan Focus
- Retry web searches (Gemini quota resets daily)
- Deep-dive into GitHub MCP Registry for finance/accounting servers
- Check for new brew formulas (couldn't search this time)
- Evaluate GPU-specific tools for the 5x3090 server

---

## 2026-03-15 — Initial Scan

### Current Setup Inventory
- **MCP Servers (mcporter):** paperless, neural-memory, zapier, docker, propertydata, xero (OFFLINE), semgrep
- **ClawHub Skills:** web-monitor (1.0.0)
- **Brew tools:** ~150+ packages including ollama, restic, semgrep, trivy, lynis, peekaboo, sag, ffmpeg, ripgrep, tmux, gh, tesseract, qemu, ansible, caddy, bitwarden-cli, memo, remindctl, imsg, summarize, gogcli, goplaces, yt-dlp

### ⚠️ Issues Found
- **Xero MCP server is OFFLINE** — needs investigation. If this is the accounting integration, it should be kept healthy.

---

### ClawHub Skills Worth Investigating

#### High Priority
| Skill | Why | Notes |
|-------|-----|-------|
| `firefly-iii` | Self-hosted personal finance tracker, Docker-native | Would complement Paperless-NGX for financial document management |
| `home-assistant` | Smart home control if HA is running | MCP server also available (`mcp-hass`) |
| `system-resource-monitor` | Monitor Mac mini + GPU server resources | Could feed into heartbeat checks |
| `ping-monitor` | Uptime monitoring for services | Docker containers, external sites |
| `cloudflare-dns` | DNS management if using Cloudflare | Automation of DNS records |
| `openclaw-backup` | Automated OpenClaw workspace backups | Already have restic but this is OpenClaw-specific |
| `docker-diag` | Docker diagnostics beyond docker-essentials | Container debugging |

#### Medium Priority
| Skill | Why |
|-------|-----|
| `beancount-skill` | Plain-text accounting (alternative to Xero for personal) |
| `automation-workflows` | Generic workflow automation |
| `domain-checker` | Quick domain availability checks |

#### Lower Priority / Niche
- `x-post-automation` — already have xurl skill
- `ollama-local` — already have ollama installed via brew
- `security-auditor` / `security-scanner` — already have trivy + lynis

---

### MCP Servers Worth Investigating (via mcporter)

#### High Value
| Server | What | Effort | Value |
|--------|------|--------|-------|
| **Anyquery** (`julien040/anyquery`) | Query 40+ apps via SQL — Go binary, local-first | Low (single binary) | ⭐⭐⭐⭐⭐ |
| **Forage** (`isaac-levine/forage`) | Self-improving tool discovery, auto-installs MCP servers | Medium | ⭐⭐⭐⭐ |
| **MindsDB** (`mindsdb/mindsdb`) | Unified data across platforms + databases | Medium (Docker) | ⭐⭐⭐⭐ |
| **PipedreamHQ** | 2,500 API integrations, 8,000+ prebuilt tools | Low (cloud) | ⭐⭐⭐⭐ |
| **Home Assistant MCP** (`mcp-hass`) | Smart home control via MCP | Low (if HA exists) | ⭐⭐⭐ |
| **Cortex** (`gzoonet/cortex`) | Local knowledge graph from project files | Medium | ⭐⭐⭐ |

#### Medium Value
| Server | What | Notes |
|--------|------|-------|
| **RAD Security** | K8s/cloud security insights | Only if running K8s |
| **Notion MCP** | If using Notion | Official server available |
| **Imagen3 MCP** | Google Imagen image generation | Needs API key |

#### Already Have / Skip
- Docker MCP — already configured
- Paperless MCP — already configured
- Semgrep MCP — already configured

---

### Brew / CLI Tools to Consider

Already well-equipped. Notable gaps:
| Tool | What | Install |
|------|------|---------|
| `dust` | Disk usage analyzer (better than du) | `brew install dust` |
| `procs` | Modern ps replacement | `brew install procs` |
| `bandwhich` | Network bandwidth monitor per-process | `brew install bandwhich` |
| `btop` | Resource monitor (better than htop) | `brew install btop` |
| `age` | Simple file encryption | `brew install age` |
| `glow` | Render markdown in terminal | `brew install glow` |
| `lazydocker` | Docker TUI management | `brew install lazydocker` |
| `atuin` | Shell history sync + search | `brew install atuin` |

---

### Docker Containers to Consider
| Container | What | Priority |
|-----------|------|----------|
| **Firefly III** | Personal finance manager | Medium — if not using Xero for personal |
| **Uptime Kuma** | Service uptime monitoring with alerts | High — simple, effective |
| **Grafana + Prometheus** | Metrics/dashboards for GPU server | Medium — if not already running |
| **Portainer** | Docker management UI | Low — nice to have |
| **Actual Budget** | Privacy-focused budgeting | Low — alternative to Firefly |

---

### Recommendations (Ranked by Impact)

1. **🔧 Fix Xero MCP server** — it's offline, needs immediate attention
2. **📊 Install Uptime Kuma** (Docker) — monitor all services, get alerts when things go down
3. **🔍 Install Anyquery** — query 40+ apps via SQL through MCP, massive capability boost
4. **🛠️ Install lazydocker** — quick Docker management from terminal
5. **💾 Install btop** — better resource monitoring for both machines
6. **🔗 Evaluate Pipedream MCP** — 2,500+ API integrations could replace many custom setups
7. **📝 Consider Firefly III** — if personal finance tracking needed beyond Xero

---

### Notes
- Web search was rate-limited (Gemini 429) during this scan — searches will be retried next run
- ClawHub has many skills but quality varies; stick to verified/trusted publishers
- MCP ecosystem is growing rapidly — 850+ PRs pending on awesome-mcp-servers repo
- Next scan should focus on: finance MCP servers, N8N integrations, GPU server tooling
