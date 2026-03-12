"""Check for suspicious patterns in tool descriptions and metadata."""

from __future__ import annotations

import re
import json
from ..models import ServerConfig, Finding, Severity

# Patterns that suggest prompt injection in tool descriptions
INJECTION_PATTERNS = [
    (r"(?i)ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions?", "Instruction override"),
    (r"(?i)you\s+(?:are|must|should|will)\s+now\b", "Behavioral override"),
    (r"(?i)system\s*prompt", "System prompt reference"),
    (r"(?i)do\s+not\s+(?:tell|reveal|show|display)", "Information suppression"),
    (r"(?i)pretend\s+(?:to\s+be|you\s+are)", "Identity manipulation"),
    (r"(?i)(?:forget|disregard)\s+(?:your|all|the)\s+(?:rules|instructions|guidelines)", "Rule override"),
    (r"(?i)output\s+(?:your|the)\s+(?:system|initial|original)\s+prompt", "Prompt extraction"),
    (r"(?i)(?:execute|run|eval)\s+(?:this|the\s+following)\s+(?:code|command|script)", "Code execution injection"),
    (r"<\s*(?:script|img|iframe|svg)\b", "HTML/XSS injection"),
]

# Suspicious metadata patterns
SUSPICIOUS_METADATA = [
    (r"(?i)base64", "Base64 encoding reference"),
    (r"(?i)(?:encode|decode|encrypt|decrypt)", "Encoding/encryption reference"),
    (r"(?i)exfiltrat", "Data exfiltration reference"),
    (r"(?i)reverse\s*shell", "Reverse shell reference"),
    (r"(?i)bind\s*shell", "Bind shell reference"),
]


def check_descriptions(server: ServerConfig) -> list[Finding]:
    """Check for suspicious patterns in server config metadata."""
    findings: list[Finding] = []

    # Serialize the raw config to check all text content
    raw_text = json.dumps(server.raw)

    # Check for prompt injection patterns
    for pattern, label in INJECTION_PATTERNS:
        match = re.search(pattern, raw_text)
        if match:
            findings.append(Finding(
                check_id="DESC-001",
                severity=Severity.CRITICAL,
                title=f"Prompt injection pattern: {label}",
                description=f"Server '{server.name}' config contains a pattern commonly "
                            f"used for prompt injection attacks: {label}.",
                server_name=server.name,
                evidence=f"Pattern: {match.group(0)}",
                recommendation="Review and sanitize tool descriptions. "
                              "This may indicate a malicious MCP server.",
            ))

    # Check for suspicious metadata
    for pattern, label in SUSPICIOUS_METADATA:
        match = re.search(pattern, raw_text)
        if match:
            findings.append(Finding(
                check_id="DESC-002",
                severity=Severity.MEDIUM,
                title=f"Suspicious metadata: {label}",
                description=f"Server '{server.name}' config contains suspicious content: {label}.",
                server_name=server.name,
                evidence=f"Pattern: {match.group(0)}",
                recommendation="Review the server config for hidden payloads.",
            ))

    return findings
