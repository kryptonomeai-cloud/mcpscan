# 🔍 MCPScan v0.1.0 — Initial Release

**Local-first security scanner for MCP server configurations.**

Catch credential leaks, SSRF vectors, prompt injection, tool shadowing, and toxic data flows in your AI agent's MCP configs — in seconds, 100% offline.

## Highlights

- 🛡️ **10 security check modules** with 40+ individual rules
- 🔎 **Auto-discovery** across 6 MCP clients (Claude Desktop, Cursor, VS Code, Windsurf, Continue.dev, mcporter)
- 📊 **Severity scoring** (0–100) with letter grades
- 🔌 **CI/CD ready** — `--fail-on` threshold + JSON output
- 🔒 **100% local** — zero cloud dependencies, your secrets never leave your machine

## Check Modules

| Module | Rules | Catches |
|--------|-------|---------|
| Credentials | 4 | API keys, tokens, passwords in URLs/env/args |
| Permissions | 5 | Shell exec, filesystem access, sudo, container escape |
| SSRF | 3 | Internal nets, cloud metadata (AWS/GCP/Azure), dangerous URIs |
| Tool Shadowing | 2 | Duplicate tool names, overlapping categories |
| Input Validation | 5 | `npx -y`, unpinned versions, vulnerable packages |
| Transport | 2 | Unencrypted HTTP, remote SSE without TLS |
| Descriptions | 2 | Suspicious metadata, injection in tool descriptions |
| Prompt Injection | 5 | System prompt overrides, hidden instructions, role-play attacks |
| Connectivity | 13 | Live TCP/TLS checks, cert expiry (dynamic mode) |
| Toxic Flows | 2 | Data source → external sink exfiltration paths |

## Install

```bash
pip install mcpscan
```

## Quick Start

```bash
# Scan a config
mcpscan scan ~/.config/claude/claude_desktop_config.json

# Auto-discover all configs
mcpscan discover

# CI/CD — fail on high+ findings
mcpscan scan config.json --fail-on high --format json
```

## Testing

83 tests passing across all modules.

---

Built by [Fyzi Security](https://fyzi.co.uk) · Securing the AI tool chain
