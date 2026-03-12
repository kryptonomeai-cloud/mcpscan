"""Check for missing input validation patterns."""

from __future__ import annotations

import re
from ..models import ServerConfig, Finding, Severity

# npm packages known to have had vulnerabilities
KNOWN_VULNERABLE_PACKAGES = {
    "event-stream": "Contained malicious code (crypto wallet theft)",
    "ua-parser-js": "Contained crypto-miner in compromised versions",
    "colors": "Sabotaged by maintainer",
    "faker": "Sabotaged by maintainer",
    "node-ipc": "Contained protestware",
}

# Patterns suggesting unvalidated input acceptance
DYNAMIC_EXEC_PATTERNS = [
    (r"\beval\b", "eval() — arbitrary code execution"),
    (r"\bFunction\s*\(", "Function constructor — dynamic code execution"),
    (r"child_process", "child_process — command execution"),
    (r"\bexec\b(?!utor)", "exec — command execution"),
]


def check_validation(server: ServerConfig) -> list[Finding]:
    """Check for input validation concerns."""
    findings: list[Finding] = []

    # Check for npx with -y flag (auto-install without confirmation)
    combined = f"{server.command or ''} {' '.join(server.args)}"

    if "npx" in combined:
        if "-y" in combined or "--yes" in combined:
            findings.append(Finding(
                check_id="VAL-001",
                severity=Severity.MEDIUM,
                title="Auto-install without confirmation (npx -y)",
                description=f"Server '{server.name}' uses 'npx -y' which auto-installs "
                            f"packages without confirmation. A typosquatted or compromised "
                            f"package could be installed silently.",
                server_name=server.name,
                evidence=f"Command: {combined.strip()}",
                recommendation="Pin package versions and verify package names. "
                              "Consider using 'npm install' with lockfile instead.",
            ))

        # Check for @latest tag (unpinned version)
        if "@latest" in combined:
            findings.append(Finding(
                check_id="VAL-002",
                severity=Severity.LOW,
                title="Unpinned package version (@latest)",
                description=f"Server '{server.name}' uses @latest which always pulls "
                            f"the newest version. A compromised update could be auto-installed.",
                server_name=server.name,
                evidence=f"Command: {combined.strip()}",
                recommendation="Pin to a specific version (e.g., @1.2.3) instead of @latest.",
            ))

    # Check for uvx (similar to npx for Python)
    if "uvx" in combined:
        findings.append(Finding(
            check_id="VAL-003",
            severity=Severity.LOW,
            title="Dynamic package execution (uvx)",
            description=f"Server '{server.name}' uses 'uvx' for dynamic Python package execution. "
                        f"Like npx, this downloads and runs code on-the-fly.",
            server_name=server.name,
            evidence=f"Command: {combined.strip()}",
            recommendation="Pin versions and verify package authenticity.",
        ))

    # Check for known vulnerable packages
    for pkg, reason in KNOWN_VULNERABLE_PACKAGES.items():
        if pkg in combined:
            findings.append(Finding(
                check_id="VAL-004",
                severity=Severity.HIGH,
                title=f"Known vulnerable package: {pkg}",
                description=f"Server '{server.name}' references package '{pkg}' "
                            f"which has known security issues: {reason}",
                server_name=server.name,
                evidence=f"Package: {pkg} — {reason}",
                recommendation=f"Replace {pkg} with a safe alternative.",
            ))

    # Check for missing env vars (referenced but not set)
    if server.command:
        env_refs = re.findall(r"\$\{?([A-Z_][A-Z0-9_]*)\}?", combined)
        for ref in env_refs:
            if ref not in server.env and ref not in ("HOME", "PATH", "USER", "SHELL"):
                findings.append(Finding(
                    check_id="VAL-005",
                    severity=Severity.INFO,
                    title=f"Referenced env var may be unset: ${ref}",
                    description=f"Server '{server.name}' references ${ref} but it's not "
                                f"defined in the server's env config.",
                    server_name=server.name,
                    evidence=f"Referenced: ${ref}",
                    recommendation="Ensure all required environment variables are set.",
                ))

    return findings
