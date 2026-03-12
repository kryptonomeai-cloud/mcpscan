"""Check transport security of MCP servers."""

from __future__ import annotations

from ..models import ServerConfig, Finding, Severity


def check_transport(server: ServerConfig) -> list[Finding]:
    """Check transport-level security."""
    findings: list[Finding] = []

    if server.transport == "sse" and server.url:
        # SSE over HTTP (not HTTPS) to external host
        if server.url.startswith("http://") and not _is_local(server.url):
            findings.append(Finding(
                check_id="TRANS-001",
                severity=Severity.HIGH,
                title="SSE transport over unencrypted HTTP",
                description=f"Server '{server.name}' uses SSE over HTTP to a remote host. "
                            f"All tool calls and responses are transmitted in cleartext.",
                server_name=server.name,
                evidence=f"URL: {server.url}",
                recommendation="Use HTTPS (wss:// or https://) for SSE connections.",
            ))

        # SSE to external service (data leaves the machine)
        if not _is_local(server.url):
            findings.append(Finding(
                check_id="TRANS-002",
                severity=Severity.INFO,
                title="Remote SSE connection",
                description=f"Server '{server.name}' connects to a remote SSE endpoint. "
                            f"All tool interactions are sent to an external server.",
                server_name=server.name,
                evidence=f"URL: {server.url}",
                recommendation="Review the privacy policy of the remote service. "
                              "Consider if local alternatives exist.",
            ))

    return findings


def _is_local(url: str) -> bool:
    """Check if URL points to a local address."""
    local_patterns = ["localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]"]
    return any(p in url for p in local_patterns)
