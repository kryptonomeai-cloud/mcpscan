<p align="center">
  <h1 align="center">🔍 MCPScan</h1>
  <p align="center"><strong>Security scanner for MCP server configurations</strong></p>
  <p align="center">Catch vulnerabilities in your AI agent's tool access — before your agent does.</p>
</p>

<p align="center">
  <a href="https://pypi.org/project/mcpscan/"><img src="https://img.shields.io/pypi/v/mcpscan?color=blue" alt="PyPI"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white" alt="Python 3.10+"></a>
  <a href="https://github.com/kryptonomeai-cloud/mcpscan/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License: MIT"></a>
  <a href="https://github.com/kryptonomeai-cloud/mcpscan/actions"><img src="https://img.shields.io/badge/tests-132%20passed-brightgreen" alt="Tests: 132 passed"></a>
  <a href="#privacy"><img src="https://img.shields.io/badge/runs-100%25%20locally-purple" alt="100% Local"></a>
</p>

---

## 🆕 What's New in v0.2.0

- **📄 HTML Reports** (`--report html`) — Beautiful standalone HTML reports with dark theme, executive summary, severity cards, and detailed findings. Zero dependencies — share as a single file.
- **📋 SARIF JSON Export** (`--report json`) — GitHub Code Scanning compatible SARIF v2.1.0 output. Upload directly to GitHub Advanced Security.
- **🔀 Diff Mode** (`mcpscan diff baseline.json current.json`) — Compare two scans to track new/resolved findings. Use `--fail-on-new` as a PR gate.
- **🧪 132 tests** — Comprehensive test coverage across all modules.

> See the full [CHANGELOG](CHANGELOG.md) for details.

---

## The Problem

MCP (Model Context Protocol) servers give AI agents access to powerful tools — filesystem, network, databases, shells. A misconfigured or malicious MCP server can:

- 🔓 **Expose credentials** — API keys and tokens hardcoded in configs
- 🎯 **Enable SSRF** — Internal network access via cloud metadata endpoints
- 💉 **Inject prompts** — Hijack agent behavior through tool descriptions
- 👻 **Shadow tools** — Replace legitimate tools with malicious versions
- 🐚 **Grant shell access** — Unrestricted command execution
- ☠️ **Create toxic flows** — Chain data sources to external sinks for exfiltration
- 📤 **Exfiltrate data** — Send sensitive info to external endpoints

**MCPScan catches these issues in seconds — 100% locally, zero cloud dependencies.**

## Quick Start

```bash
# Install
pip install mcpscan

# Scan your Claude Desktop config
mcpscan scan ~/.config/claude/claude_desktop_config.json

# Auto-discover and scan all MCP configs on your system
mcpscan discover

# Scan any MCP config
mcpscan scan config/mcporter.json
```

## Installation

### From PyPI (recommended)

```bash
pip install mcpscan
```

### From source

```bash
git clone https://github.com/kryptonomeai-cloud/mcpscan.git
cd mcpscan
pip install -e .
```

### With dev dependencies

```bash
pip install -e ".[dev]"
```

## Usage

### Basic scan

```bash
$ mcpscan scan config.json

╭─────────────────────────────╮
│ MCPScan Report              │
│ Config: config.json         │
│ Format: claude_desktop      │
│ Servers: 6                  │
╰─────────────────────────────╯

🔴 CRITICAL (1)
  [CRED-001] Secret exposed in URL: Zapier-style secret key
    Server: zapier
    → Use environment variables instead of embedding secrets in URLs.

🟠 HIGH (2)
  [CRED-002] Hardcoded secret in env: PAPERLESS_API_KEY
    Server: paperless
    → Use a secrets manager or .env file (gitignored).

  [PERM-001] Unrestricted shell access
    Server: terminal
    → Limit allowed commands or use a sandboxed environment.

╭──────────────────────────╮
│ Score: 42/100 (Poor)     │
╰──────────────────────────╯
```

### HTML report

```bash
$ mcpscan scan config.json --report html -o report.html

# Generates a self-contained HTML file with:
# • Executive summary with overall risk score
# • Severity count cards (critical/high/medium/low/info)
# • Servers overview table
# • Detailed findings with evidence and remediation
# • Dark theme (#0a0a0b) with cyan accents — looks great
```

### SARIF export (GitHub Security)

```bash
# Generate SARIF for GitHub Code Scanning
$ mcpscan scan config.json --report json -o results.sarif

# Upload to GitHub (in CI):
# gh api repos/{owner}/{repo}/code-scanning/sarifs \
#   --field sarif=@results.sarif
```

### Diff mode — track changes between scans

```bash
# Save a baseline
$ mcpscan scan config.json --format json -o baseline.json

# Later, scan again and compare
$ mcpscan scan config.json --format json -o current.json
$ mcpscan diff baseline.json current.json

  ✅ Resolved: [CRED-001] Secret exposed in URL (zapier)
  🆕 New:      [PERM-003] Container escape vector (docker)
  Score: 42 → 58 (+16)

# Use as a PR gate — fail if new issues appear
$ mcpscan diff baseline.json current.json --fail-on-new
```

### Auto-discover configs

```bash
# Find and scan all MCP configs on your system
$ mcpscan discover

Found 3 MCP configurations:
  ✅ Claude Desktop — ~/.config/claude/claude_desktop_config.json (4 servers)
  ✅ mcporter — ~/.openclaw/config/mcporter.json (6 servers)
  ❌ Cursor — not found

# Scan all discovered configs at once
$ mcpscan discover --scan
```

### Output formats

```bash
# Terminal (default) — coloured, human-readable
mcpscan scan config.json

# JSON — for CI/CD pipelines
mcpscan scan config.json --format json

# Markdown — for reports and PRs
mcpscan scan config.json --format markdown -o report.md
```

### Dynamic checks (connectivity)

```bash
# Include live connectivity & TLS checks
mcpscan scan config.json --dynamic
```

### CI/CD integration

```bash
# Fail the build if any high+ severity findings
mcpscan scan config.json --fail-on high

# JSON output for machine parsing
mcpscan scan config.json --format json --fail-on medium
```

### Inspect parsed config

```bash
mcpscan info config.json
```

## Security Check Modules

MCPScan includes **10 security check modules** with **40+ individual rules**:

| # | Module | IDs | Rules | What it catches |
|---|--------|-----|-------|-----------------|
| 1 | **Credentials** | `CRED-001..004` | 4 | API keys, tokens, passwords in URLs, env vars, and command args |
| 2 | **Permissions** | `PERM-001..005` | 5 | Shell exec, filesystem access, elevated privileges, Docker/container escape |
| 3 | **SSRF** | `SSRF-001..003` | 3 | Internal networks, cloud metadata endpoints (AWS/GCP/Azure), dangerous URI schemes |
| 4 | **Tool Shadowing** | `SHADOW-001..002` | 2 | Duplicate tool names across servers, overlapping tool categories |
| 5 | **Input Validation** | `VAL-001..005` | 5 | `npx -y` auto-install, unpinned versions, known vulnerable packages |
| 6 | **Transport** | `TRANS-001..002` | 2 | Unencrypted HTTP endpoints, remote SSE connections without TLS |
| 7 | **Descriptions** | `DESC-001..002` | 2 | Suspicious metadata patterns, injection vectors in tool descriptions |
| 8 | **Prompt Injection** | `INJECT-001..005` | 5 | System prompt override attempts, hidden instructions, role-play attacks |
| 9 | **Connectivity** | `CONN-001..013` | 13 | Live TCP reachability, TLS certificate validation, expiry checks (dynamic) |
| 10 | **Toxic Flows** | `TOXIC-001..002` | 2 | Data source → external sink chains, exfiltration paths between servers |

> Modules 1–8 are **static** (analyse config only). Module 9 is **dynamic** (requires `--dynamic` flag). Module 10 is a **cross-server** analysis.

### Severity Levels

| Level | Meaning |
|-------|---------|
| 🔴 **Critical** | Immediate security risk — credential exposure, cloud metadata SSRF, sudo |
| 🟠 **High** | Significant risk — shell exec, hardcoded secrets, tool shadowing |
| 🟡 **Medium** | Moderate risk — unencrypted HTTP, npx auto-install, container access |
| 🔵 **Low** | Minor concern — unpinned versions, dynamic package execution |
| ⚪ **Info** | Informational — internal network access, remote connections |

## MCPScan vs Cloud Scanners

| | MCPScan | Cloud-based scanners |
|---|---------|---------------------|
| **Data privacy** | ✅ 100% local — secrets never leave your machine | ❌ Configs uploaded to third-party servers |
| **Speed** | ✅ Scans in <1 second | ⏳ Network round-trip + queue |
| **Offline** | ✅ Works without internet | ❌ Requires connectivity |
| **Cost** | ✅ Free & open source | 💰 Often paid/freemium |
| **CI/CD** | ✅ `pip install` + one command | 🔧 API keys, webhooks, config |
| **Auditability** | ✅ Read every line of source | ❌ Black box |
| **MCP-specific** | ✅ Purpose-built for MCP configs | ⚠️ Generic or adapted scanners |

**Your MCP configs contain API keys, tokens, and infrastructure details. Why send them to the cloud?**

## Supported Config Formats

- ✅ **Claude Desktop** (`claude_desktop_config.json`)
- ✅ **Cursor** (`.cursor/mcp.json`)
- ✅ **VS Code** (`.vscode/mcp.json`)
- ✅ **Windsurf** (`.windsurf/mcp.json`)
- ✅ **Continue.dev** (`.continue/config.json`)
- ✅ **mcporter** (`mcporter.json`)
- ✅ Any JSON with `mcpServers` structure

### Auto-Discovery

MCPScan can automatically find MCP configs on your system across all supported clients. Run `mcpscan discover` to scan well-known locations for macOS, Linux, and Windows.

## Features

- [x] 10 security check modules with 40+ individual rules
- [x] Auto-discovery of MCP configs across 6 popular clients
- [x] Severity scoring (0-100) with letter grades
- [x] Static + dynamic (live connectivity/TLS) analysis
- [x] Cross-server analysis (toxic flows, tool shadowing)
- [x] Multiple output formats (terminal, JSON, markdown)
- [x] CI/CD integration with `--fail-on` threshold
- [x] HTML reports — dark-themed, self-contained, shareable
- [x] SARIF JSON export — GitHub Code Scanning compatible
- [x] Diff mode — track new/resolved findings between scans
- [x] 100% offline — no data ever leaves your machine
- [x] Zero cloud dependencies
- [x] Extensible check architecture
- [ ] VS Code extension
- [ ] Pre-commit hook

## Development

```bash
# Clone and install
git clone https://github.com/kryptonomeai-cloud/mcpscan.git
cd mcpscan
pip install -e ".[dev]"

# Run tests (132 tests)
pytest tests/ -v

# Run against test fixtures
mcpscan scan tests/fixtures/vulnerable_1.json
mcpscan scan tests/fixtures/vulnerable_2.json
```

## Privacy

MCPScan is **100% local**:

- ✅ Runs entirely on your machine
- ✅ Never sends data to any external service
- ✅ Zero cloud dependencies
- ✅ Works fully offline

Your MCP configs may contain secrets — MCPScan never transmits them anywhere.

## Contributing

Contributions welcome! Here's how:

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/new-check`)
3. Add tests for new checks
4. Run `pytest tests/ -v` to verify
5. Submit a PR

### Adding a new security check

1. Create a new file in `src/mcpscan/checks/`
2. Implement the check function following existing patterns
3. Register it in `src/mcpscan/checks/__init__.py`
4. Add test fixtures and test cases

## License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built by <a href="https://fyzi.co.uk">Fyzi Security</a> · Securing the AI tool chain
</p>
