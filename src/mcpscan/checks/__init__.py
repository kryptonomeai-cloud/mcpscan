"""Security checks for MCP server configurations."""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import ServerConfig, Finding

from .credentials import check_credentials
from .permissions import check_permissions
from .ssrf import check_ssrf
from .shadowing import check_shadowing
from .validation import check_validation
from .transport import check_transport
from .descriptions import check_descriptions

# All checks that operate on individual servers
SINGLE_SERVER_CHECKS = [
    check_credentials,
    check_permissions,
    check_ssrf,
    check_validation,
    check_transport,
    check_descriptions,
]

# Checks that operate across all servers
CROSS_SERVER_CHECKS = [
    check_shadowing,
]


def run_all_checks(servers: list["ServerConfig"]) -> list["Finding"]:
    """Run all checks and return findings."""
    findings: list["Finding"] = []

    # Per-server checks
    for server in servers:
        for check_fn in SINGLE_SERVER_CHECKS:
            findings.extend(check_fn(server))

    # Cross-server checks
    for check_fn in CROSS_SERVER_CHECKS:
        findings.extend(check_fn(servers))

    # Sort by severity (critical first)
    findings.sort(key=lambda f: f.severity.rank, reverse=True)
    return findings
