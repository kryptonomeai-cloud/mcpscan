# Changelog

All notable changes to MCPScan will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-14

### Added

- **HTML Report Generator** (`--report html`) — Standalone self-contained HTML report with dark theme (#0a0a0b background, #06b6d4 cyan accents). Features executive summary with overall risk score, severity count cards (critical/high/medium/low/info), servers table, and detailed findings table with evidence and remediation columns. All CSS inlined for zero-dependency sharing.
- **SARIF JSON Export** (`--report json` / `--report sarif`) — GitHub Code Scanning compatible SARIF v2.1.0 output. Machine-readable format for CI/CD pipelines, can be uploaded directly to GitHub Advanced Security. Includes rule definitions, severity mappings, and full finding details.
- **Diff Mode** (`mcpscan diff <baseline.json> <current.json>`) — Compare two scan results to identify new, resolved, and unchanged findings. Supports both native mcpscan JSON and SARIF formats. Includes `--fail-on-new` flag for PR gate checks (exit code 1 if new issues found). Shows score delta between scans.

### Changed

- CLI `scan` command now accepts `--report` / `-r` flag for report generation alongside existing `--format` flag.
- Added `reporters/` package with `html_reporter.py` and `json_reporter.py`.
- Added `commands/` package with `diff.py`.

## [0.1.0] - 2026-03-14

### Added

#### Security Check Modules (10)

1. **Credentials** (`CRED-001..004`) — Detects API keys, tokens, and passwords exposed in URLs, environment variables, and command-line arguments.
2. **Permissions** (`PERM-001..005`) — Flags unrestricted shell execution, broad filesystem access, elevated privileges (sudo/root), Docker/container escape vectors, and dangerous process spawning.
3. **SSRF** (`SSRF-001..003`) — Identifies internal network access (RFC 1918), cloud metadata endpoint exposure (AWS/GCP/Azure IMDSv1), and dangerous URI schemes (`file://`, `gopher://`).
4. **Tool Shadowing** (`SHADOW-001..002`) — Detects duplicate tool names across servers and overlapping tool categories that could be exploited.
5. **Input Validation** (`VAL-001..005`) — Catches `npx -y` auto-install patterns, unpinned package versions, known vulnerable packages, dynamic code evaluation, and unsafe deserialization.
6. **Transport** (`TRANS-001..002`) — Warns on unencrypted HTTP endpoints and remote SSE connections without TLS.
7. **Descriptions** (`DESC-001..002`) — Scans tool descriptions for suspicious metadata patterns and embedded injection vectors.
8. **Prompt Injection** (`INJECT-001..005`) — Detects system prompt override attempts, hidden instructions, role-play attacks, instruction delimiter abuse, and encoded payload obfuscation.
9. **Connectivity** (`CONN-001..013`) — Dynamic checks: live TCP reachability, HTTP HEAD probes, TLS certificate validation, certificate expiry warnings, and connection failure reporting.
10. **Toxic Flows** (`TOXIC-001..002`) — Cross-server analysis identifying data source → external sink chains and potential exfiltration paths.

#### Core Features

- CLI with `scan`, `discover`, and `info` commands
- Auto-discovery of MCP configs across 6 clients (Claude Desktop, Cursor, VS Code, Windsurf, Continue.dev, mcporter)
- Support for macOS, Linux, and Windows config paths
- Severity scoring (0-100) with letter grades (A+ through F)
- Three output formats: terminal (rich), JSON, and Markdown
- CI/CD integration via `--fail-on` severity threshold
- Static analysis (default) + dynamic connectivity checks (`--dynamic` flag)
- Cross-server analysis for tool shadowing and toxic data flows
- 100% local execution — zero cloud dependencies, zero data exfiltration

#### Testing

- 83 unit tests across 5 test files covering all check modules
- Test fixtures with realistic vulnerable configurations

[0.1.0]: https://github.com/kryptonomeai-cloud/mcpscan/releases/tag/v0.1.0
