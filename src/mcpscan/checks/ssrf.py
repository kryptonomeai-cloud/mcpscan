"""Check for SSRF (Server-Side Request Forgery) indicators."""

from __future__ import annotations

import re
from urllib.parse import urlparse
from ..models import ServerConfig, Finding, Severity

# Internal/private network patterns
INTERNAL_PATTERNS = [
    (r"(?:^|[/@])localhost(?:[:/]|$)", "localhost"),
    (r"(?:^|[/@])127\.0\.0\.\d+", "loopback address"),
    (r"(?:^|[/@])0\.0\.0\.0", "all-interfaces bind"),
    (r"(?:^|[/@])10\.\d+\.\d+\.\d+", "private network (10.x)"),
    (r"(?:^|[/@])172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+", "private network (172.16-31.x)"),
    (r"(?:^|[/@])192\.168\.\d+\.\d+", "private network (192.168.x)"),
    (r"(?:^|[/@])169\.254\.\d+\.\d+", "link-local / cloud metadata"),
    (r"(?:^|[/@])\[?::1\]?", "IPv6 loopback"),
    (r"(?:^|[/@])\[?fe80:", "IPv6 link-local"),
    (r"metadata\.google\.internal", "GCP metadata endpoint"),
    (r"169\.254\.169\.254", "cloud metadata endpoint"),
]

# Dangerous URL schemes
DANGEROUS_SCHEMES = ["file", "ftp", "gopher", "dict", "ldap", "tftp"]


def check_ssrf(server: ServerConfig) -> list[Finding]:
    """Check for SSRF indicators in server config."""
    findings: list[Finding] = []

    # Check server URL
    if server.url:
        findings.extend(_check_url(server.url, server.name, "server URL"))

    # Check env values for URLs
    for env_name, env_value in server.env.items():
        if re.match(r"https?://", env_value) or "://" in env_value:
            findings.extend(_check_url(env_value, server.name, f"env[{env_name}]"))

    # Check args for URLs
    for arg in server.args:
        if re.match(r"https?://", arg) or "://" in arg:
            findings.extend(_check_url(arg, server.name, f"args"))

    return findings


def _check_url(url: str, server_name: str, location: str) -> list[Finding]:
    """Check a single URL for SSRF indicators."""
    findings: list[Finding] = []

    # Check for internal network access
    for pattern, label in INTERNAL_PATTERNS:
        if re.search(pattern, url):
            # Cloud metadata is critical, internal network is medium
            if "metadata" in label or "169.254.169.254" in url:
                severity = Severity.CRITICAL
            elif "link-local" in label:
                severity = Severity.HIGH
            else:
                severity = Severity.INFO  # Internal network is often intentional

            findings.append(Finding(
                check_id="SSRF-001",
                severity=severity,
                title=f"Internal network access: {label}",
                description=f"The {location} points to a {label} address. "
                            f"If this server proxies requests, it could enable SSRF attacks.",
                server_name=server_name,
                evidence=f"{location}: {url}",
                recommendation="Ensure internal network access is intentional and rate-limited.",
            ))
            break

    # Check for dangerous URL schemes
    try:
        parsed = urlparse(url)
        if parsed.scheme.lower() in DANGEROUS_SCHEMES:
            findings.append(Finding(
                check_id="SSRF-002",
                severity=Severity.HIGH,
                title=f"Dangerous URL scheme: {parsed.scheme}",
                description=f"The {location} uses the '{parsed.scheme}' scheme, "
                            f"which may enable SSRF or local file access.",
                server_name=server_name,
                evidence=f"{location}: {url}",
                recommendation="Restrict to https:// URLs only.",
            ))
    except Exception:
        pass

    # Check for URL without HTTPS
    if url.startswith("http://") and not any(
        re.search(p, url) for p, _ in INTERNAL_PATTERNS[:4]  # Skip warning for localhost/internal
    ):
        findings.append(Finding(
            check_id="SSRF-003",
            severity=Severity.MEDIUM,
            title="Unencrypted HTTP connection",
            description=f"The {location} uses unencrypted HTTP. "
                        f"Credentials and data may be exposed in transit.",
            server_name=server_name,
            evidence=f"{location}: {url}",
            recommendation="Use HTTPS for all external connections.",
        ))

    return findings
