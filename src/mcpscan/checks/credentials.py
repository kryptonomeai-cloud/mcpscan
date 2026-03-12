"""Check for hardcoded credentials and API keys in MCP configs."""

from __future__ import annotations

import re
from ..models import ServerConfig, Finding, Severity

# Patterns that indicate API keys or secrets
SECRET_PATTERNS = [
    # Generic API key patterns
    (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{16,})", "API key"),
    (r"(?i)(secret|password|passwd|pwd)\s*[:=]\s*['\"]?([^\s'\"]{8,})", "Secret/password"),
    (r"(?i)(token|auth)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{16,})", "Auth token"),
    # Specific service patterns
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI-style API key"),
    (r"sk-ak-[a-zA-Z0-9]{10,}", "Zapier-style secret key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth token"),
    (r"glpat-[a-zA-Z0-9\-_]{20,}", "GitLab personal access token"),
    (r"xox[bpsa]-[a-zA-Z0-9\-]{10,}", "Slack token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}", "Bearer token"),
]

# Environment variable names that suggest secrets
SECRET_ENV_NAMES = [
    r"(?i).*api[_-]?key.*",
    r"(?i).*secret.*",
    r"(?i).*token.*",
    r"(?i).*password.*",
    r"(?i).*passwd.*",
    r"(?i).*credential.*",
    r"(?i).*auth.*",
]


def check_credentials(server: ServerConfig) -> list[Finding]:
    """Check for hardcoded credentials in server config."""
    findings: list[Finding] = []

    # Check URL for embedded secrets
    if server.url:
        for pattern, label in SECRET_PATTERNS:
            match = re.search(pattern, server.url)
            if match:
                # Redact the key in evidence
                matched = match.group(0)
                redacted = matched[:8] + "..." + matched[-4:] if len(matched) > 16 else matched[:4] + "..."
                findings.append(Finding(
                    check_id="CRED-001",
                    severity=Severity.CRITICAL,
                    title=f"Secret exposed in URL: {label}",
                    description=f"A {label} is embedded directly in the server URL. "
                                f"This is visible in config files and version control.",
                    server_name=server.name,
                    evidence=f"URL contains: {redacted}",
                    recommendation="Use environment variables instead of embedding secrets in URLs.",
                ))
                break  # One finding per URL is enough

    # Check env vars for hardcoded secrets
    for env_name, env_value in server.env.items():
        # Check if env name suggests a secret
        is_secret_name = any(re.match(p, env_name) for p in SECRET_ENV_NAMES)

        if is_secret_name:
            # Value is hardcoded in the config (not a reference)
            if env_value and not env_value.startswith("${") and not env_value.startswith("$"):
                redacted = env_value[:4] + "..." + env_value[-4:] if len(env_value) > 12 else "***"
                findings.append(Finding(
                    check_id="CRED-002",
                    severity=Severity.HIGH,
                    title=f"Hardcoded secret in env: {env_name}",
                    description=f"The environment variable '{env_name}' contains a hardcoded secret value. "
                                f"This will be visible in config files and version control.",
                    server_name=server.name,
                    evidence=f"{env_name}={redacted}",
                    recommendation="Use a secrets manager, .env file (gitignored), or OS keychain.",
                ))

        # Also check env values against secret patterns regardless of name
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, env_value):
                if not any(f.check_id == "CRED-002" and env_name in (f.evidence or "") for f in findings):
                    findings.append(Finding(
                        check_id="CRED-003",
                        severity=Severity.HIGH,
                        title=f"Secret pattern in env value: {label}",
                        description=f"Environment variable '{env_name}' contains a value matching "
                                    f"a known secret pattern ({label}).",
                        server_name=server.name,
                        evidence=f"{env_name} matches {label} pattern",
                        recommendation="Use a secrets manager or .env file (gitignored).",
                    ))
                break

    # Check command and args for embedded secrets
    all_args = " ".join([server.command or ""] + server.args)
    for pattern, label in SECRET_PATTERNS:
        match = re.search(pattern, all_args)
        if match:
            findings.append(Finding(
                check_id="CRED-004",
                severity=Severity.HIGH,
                title=f"Secret in command args: {label}",
                description=f"The server command or arguments contain a {label}.",
                server_name=server.name,
                evidence=f"Found in command/args",
                recommendation="Pass secrets via environment variables, not command arguments.",
            ))
            break

    return findings
