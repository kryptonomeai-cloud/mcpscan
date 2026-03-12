<p align="center">
  <h1 align="center">🔍 MCPScan</h1>
  <p align="center"><strong>Security scanner for MCP server configurations</strong></p>
  <p align="center">Catch vulnerabilities in your AI agent's tool access — before your agent does.</p>
</p>

<p align="center">
  <a href="https://pypi.org/project/mcpscan/"><img src="https://img.shields.io/pypi/v/mcpscan?color=blue" alt="PyPI"></a>
  <a href="https://pypi.org/project/mcpscan/"><img src="https://img.shields.io/pypi/pyversions/mcpscan" alt="Python"></a>
  <a href="https://github.com/kryptonomeai-cloud/mcpscan/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>
  <a href="https://github.com/kryptonomeai-cloud/mcpscan/actions"><img src="https://img.shields.io/badge/tests-passing-brightgreen" alt="Tests"></a>
</p>

---

## The Problem

MCP (Model Context Protocol) servers give AI agents access to powerful tools — filesystem, network, databases, shells. A misconfigured or malicious MCP server can:

- 🔓 **Expose credentials** — API keys and tokens hardcoded in configs
- 🎯 **Enable SSRF** — Internal network access via cloud metadata endpoints
- 💉 **Inject prompts** — Hijack agent behavior through tool descriptions
- 👻 **Shadow tools** — Replace legitimate tools with malicious versions
- 🐚 **Grant shell access** — Unrestricted command execution
- 📤 **Exfiltrate data** — Send sensitive info to external endpoints

**MCPScan catches these issues in seconds — 100% locally, zero cloud dependencies.**

## Quick Start

```bash
# Install
pip install mcpscan

# Scan your Claude Desktop config
mcpscan scan ~/.config/claude/claude_desktop_config.json

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

### Output formats

```bash
# Terminal (default) — coloured, human-readable
mcpscan scan config.json

# JSON — for CI/CD pipelines
mcpscan scan config.json --format json

# Markdown — for reports and PRs
mcpscan scan config.json --format markdown -o report.md
```

### CI/CD integration

```bash
# Fail the build if any high+ severity findings
mcpscan scan config.json --fail-on high
```

### Inspect parsed config

```bash
mcpscan info config.json
```

## Security Checks

| Category | IDs | What it catches |
|----------|-----|-----------------|
| **Credentials** | CRED-001..004 | API keys, tokens, passwords in URLs, env vars, and args |
| **Permissions** | PERM-001..005 | Shell exec, filesystem access, elevated privileges, containers |
| **SSRF** | SSRF-001..003 | Internal networks, cloud metadata endpoints, dangerous URI schemes |
| **Tool Shadowing** | SHADOW-001..002 | Duplicate tool names, overlapping tool categories |
| **Input Validation** | VAL-001..005 | `npx -y` auto-install, unpinned versions, known vulnerable packages |
| **Transport** | TRANS-001..002 | Unencrypted HTTP, remote SSE connections |
| **Prompt Injection** | DESC-001..002 | Injection patterns in tool descriptions, suspicious metadata |

### Severity Levels

| Level | Meaning |
|-------|---------|
| 🔴 **Critical** | Immediate security risk — credential exposure, cloud metadata SSRF, sudo |
| 🟠 **High** | Significant risk — shell exec, hardcoded secrets, tool shadowing |
| 🟡 **Medium** | Moderate risk — unencrypted HTTP, npx auto-install, container access |
| 🔵 **Low** | Minor concern — unpinned versions, dynamic package execution |
| ⚪ **Info** | Informational — internal network access, remote connections |

## Supported Config Formats

- ✅ **Claude Desktop** (`claude_desktop_config.json`)
- ✅ **mcporter** (`mcporter.json`)
- ✅ Any JSON with `mcpServers` structure

## Features

- [x] 7 security check categories with 20+ individual rules
- [x] Severity scoring (0-100) with letter grades
- [x] Multiple output formats (terminal, JSON, markdown)
- [x] CI/CD integration with `--fail-on` threshold
- [x] 100% offline — no data ever leaves your machine
- [x] Zero cloud dependencies
- [x] Extensible check architecture
- [ ] SARIF output for GitHub Security tab
- [ ] VS Code extension
- [ ] Pre-commit hook

## Development

```bash
# Clone and install
git clone https://github.com/kryptonomeai-cloud/mcpscan.git
cd mcpscan
pip install -e ".[dev]"

# Run tests
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
