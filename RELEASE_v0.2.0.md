# 🔍 MCPScan v0.2.0

**Local-first security scanner for MCP server configurations.**

## What's New

### 📄 HTML Reports (`--report html`)
Beautiful standalone HTML reports with dark theme, executive summary, severity cards, and detailed findings table with evidence and remediation. Zero dependencies — share as a single file.

### 📋 SARIF JSON Export (`--report json`)
GitHub Code Scanning compatible SARIF v2.1.0 output. Upload directly to GitHub Advanced Security for native integration.

### 🔀 Diff Mode (`mcpscan diff`)
Compare two scan results to identify new, resolved, and unchanged findings. Supports `--fail-on-new` flag as a PR gate — exit code 1 if new issues appear. Shows score delta between scans.

### 🧪 132 Tests
Expanded test suite covering all check modules, reporters, and diff logic.

## All Features

- 🛡️ **10 security check modules** with 40+ individual rules
- 🔎 **Auto-discovery** across 6 MCP clients (Claude Desktop, Cursor, VS Code, Windsurf, Continue.dev, mcporter)
- 📊 **Severity scoring** (0–100) with letter grades
- 🔌 **CI/CD ready** — `--fail-on` threshold + JSON/SARIF output
- 📄 **HTML reports** — dark-themed, self-contained
- 🔀 **Diff mode** — track changes between scans
- 🔒 **100% local** — zero cloud dependencies, your secrets never leave your machine

## Install / Upgrade

```bash
pip install --upgrade mcpscan
```

---

Built by [Fyzi Security](https://fyzi.co.uk) · Securing the AI tool chain
