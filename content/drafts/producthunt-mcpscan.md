# MCPScan — Product Hunt Listing Draft

## Tagline (60 chars max)
**Security scanner for AI agent tools — 100% local** (53 chars)

## Short Description (260 chars)
MCPScan is the first open-source security scanner for MCP (Model Context Protocol) servers. It finds SSRF, injection, auth, and permission vulnerabilities in your AI agent tooling before attackers do. Runs entirely on your machine — your configs never leave. (260 chars)

## Full Description

### 🛡️ MCPScan — Secure Your AI Agent Infrastructure

AI agents are only as secure as the tools they call. MCP servers — the protocol that connects AI models to databases, APIs, and code execution — have become critical infrastructure. Yet almost nobody is scanning them for vulnerabilities.

**MCPScan changes that.**

#### What it does:
- **10 Security Check Modules** — SSRF detection, prompt injection vectors, auth gaps, excessive permissions, transport security, and more
- **Toxic Flow Detection** — Identifies dangerous multi-tool chains where data from one tool can compromise another
- **OWASP LLM Top 10 Mapping** — Every finding maps to the industry-standard framework
- **CI/CD Ready** — JSON output for GitHub Actions, GitLab CI, or any pipeline
- **Config Format Support** — Scans `claude_desktop_config.json`, `mcp.json`, mcporter configs, and custom formats
- **100% Local** — Zero cloud dependencies. Your configs never leave your machine. No API keys, no telemetry, no accounts.

#### Why it matters:
Microsoft recently disclosed a critical SSRF vulnerability in their own Azure MCP server. If the company running one of the world's three largest cloud platforms can ship insecure MCP implementations, what's hiding in yours?

The MCP ecosystem has exploded to 8,500+ servers across registries, GitHub, and npm. Most ship with no security review, no input validation, and no authentication. MCPScan brings security tooling to this new attack surface.

#### Get started in seconds:
```
pip install mcpscan
mcpscan scan --config ~/.config/claude/claude_desktop_config.json
```

Open source. MIT licensed. Built by [MindFizz](https://mindfizz.ai).

---

## Gallery Image Descriptions

1. **Terminal scan output** — Screenshot of MCPScan running against a real config file, showing colour-coded findings (critical in red, warnings in yellow, info in blue) with OWASP LLM Top 10 references
2. **Architecture diagram** — Clean diagram showing: MCP Server configs → MCPScan → Findings report. Emphasise "100% local" with no cloud arrows
3. **Before/After comparison** — Split screen: left shows an insecure MCP config with highlighted vulnerabilities, right shows MCPScan's detection output identifying each issue
4. **CI/CD integration** — Screenshot of a GitHub Actions workflow using MCPScan as a security gate, with JSON output and pass/fail status
5. **Feature grid** — Dark-themed infographic showing the 10 check modules as icons/cards: SSRF, Injection, Auth, Permissions, Transport, Toxic Flows, Secrets, Schema, Config, OWASP mapping

---

## First Comment from Maker

Hey Product Hunt! 👋

I built MCPScan because I kept seeing the same pattern: developers wire up MCP servers to give their AI agents access to databases, APIs, and code execution — then never security-test any of it.

When Microsoft disclosed a critical SSRF in their own Azure MCP server, it confirmed what I suspected: the MCP ecosystem has a massive security gap, and traditional security tools don't understand this new attack surface.

MCPScan runs 100% locally (a security scanner that phones home would be ironic), supports the major config formats, and maps everything to OWASP LLM Top 10 so your security team speaks the same language.

It's open source, MIT licensed, and I'd love your feedback. What checks would you want to see added? What MCP servers are you running that you'd want scanned?

Star the repo, try it on your configs, and let me know what you find. 🛡️

---

## Topics
- Developer Tools
- Security
- AI
- Open Source
