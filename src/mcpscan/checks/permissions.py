"""Check for overly permissive tool scopes."""

from __future__ import annotations

import re
from ..models import ServerConfig, Finding, Severity

# Commands that indicate shell execution capability
SHELL_EXEC_PATTERNS = [
    r"\bbash\b", r"\bsh\b", r"\bzsh\b", r"\bcmd\b",
    r"\bexec\b", r"\beval\b", r"\bspawn\b", r"\bsystem\b",
    r"\bpopen\b", r"\bsubprocess\b",
]

# Commands/names that suggest broad filesystem access
FS_ACCESS_PATTERNS = [
    r"(?i)filesystem", r"(?i)file[-_]?system", r"(?i)file[-_]?server",
    r"(?i)fs[-_]server", r"(?i)disk[-_]access",
]

# Commands/names suggesting network access
NETWORK_PATTERNS = [
    r"(?i)fetch", r"(?i)http[-_]?client", r"(?i)web[-_]?scrape",
    r"(?i)curl", r"(?i)wget", r"(?i)request",
]

# Commands that run with elevated privileges
ELEVATED_PATTERNS = [
    r"\bsudo\b", r"\bdoas\b", r"\bsu\b",
]

# Docker/container escape patterns
CONTAINER_PATTERNS = [
    r"\bdocker\b", r"\bpodman\b", r"\bcontainerd\b",
    r"\bkubectl\b", r"\bkubernetes\b",
]

# High-risk tool names
RISKY_TOOL_NAMES = {
    "docker": ("container management", Severity.MEDIUM),
    "kubernetes": ("cluster management", Severity.HIGH),
    "kubectl": ("cluster management", Severity.HIGH),
    "shell": ("shell execution", Severity.HIGH),
    "terminal": ("terminal access", Severity.HIGH),
    "exec": ("command execution", Severity.HIGH),
    "sudo": ("elevated execution", Severity.CRITICAL),
}


def check_permissions(server: ServerConfig) -> list[Finding]:
    """Check for overly permissive tool scopes."""
    findings: list[Finding] = []
    combined = " ".join([
        server.name,
        server.command or "",
        " ".join(server.args),
    ]).lower()

    # Check for shell execution
    for pattern in SHELL_EXEC_PATTERNS:
        if re.search(pattern, combined):
            findings.append(Finding(
                check_id="PERM-001",
                severity=Severity.HIGH,
                title="Shell execution capability",
                description=f"Server '{server.name}' appears to provide shell/command execution. "
                            f"This allows arbitrary command execution on the host.",
                server_name=server.name,
                evidence=f"Pattern matched: {pattern}",
                recommendation="Restrict to specific commands. Avoid generic shell access.",
            ))
            break

    # Check for broad filesystem access
    for pattern in FS_ACCESS_PATTERNS:
        if re.search(pattern, combined):
            findings.append(Finding(
                check_id="PERM-002",
                severity=Severity.MEDIUM,
                title="Broad filesystem access",
                description=f"Server '{server.name}' may provide broad filesystem access. "
                            f"Ensure it's scoped to specific directories.",
                server_name=server.name,
                evidence=f"Pattern matched: {pattern}",
                recommendation="Use allowlists and path restrictions to limit file access scope.",
            ))
            break

    # Check for elevated privileges
    for pattern in ELEVATED_PATTERNS:
        if re.search(pattern, combined):
            findings.append(Finding(
                check_id="PERM-003",
                severity=Severity.CRITICAL,
                title="Elevated privilege execution",
                description=f"Server '{server.name}' uses elevated privileges (sudo/su). "
                            f"An AI agent with sudo access is extremely dangerous.",
                server_name=server.name,
                evidence=f"Pattern matched: {pattern}",
                recommendation="Never run MCP servers with elevated privileges.",
            ))
            break

    # Check for container management
    for pattern in CONTAINER_PATTERNS:
        if re.search(pattern, combined):
            findings.append(Finding(
                check_id="PERM-004",
                severity=Severity.MEDIUM,
                title="Container management access",
                description=f"Server '{server.name}' provides container management. "
                            f"Docker access can be equivalent to root access.",
                server_name=server.name,
                evidence=f"Pattern matched: {pattern}",
                recommendation="Use rootless containers and restrict to specific operations.",
            ))
            break

    # Check known risky tool names
    for name, (desc, severity) in RISKY_TOOL_NAMES.items():
        if name in server.name.lower():
            findings.append(Finding(
                check_id="PERM-005",
                severity=severity,
                title=f"High-risk tool: {desc}",
                description=f"Server '{server.name}' provides {desc}. "
                            f"Ensure appropriate access controls are in place.",
                server_name=server.name,
                evidence=f"Server name matches risky pattern: {name}",
                recommendation=f"Review {desc} permissions and restrict to minimum required.",
            ))
            break

    return findings
