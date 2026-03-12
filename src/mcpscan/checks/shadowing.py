"""Check for tool shadowing across MCP servers."""

from __future__ import annotations

from ..models import ServerConfig, Finding, Severity

# Well-known tool names that are high-value shadow targets
HIGH_VALUE_TOOLS = {
    "read_file", "write_file", "execute", "run",
    "search", "fetch", "get", "post", "delete",
    "list_files", "create_file", "edit_file",
}


def check_shadowing(servers: list[ServerConfig]) -> list[Finding]:
    """Check for tool name conflicts across servers.

    Since we're doing static config analysis (not runtime introspection),
    we check for servers with identical names and flag common shadowing risks.
    """
    findings: list[Finding] = []

    # Check for duplicate server names
    names = {}
    for server in servers:
        lower = server.name.lower()
        if lower in names:
            findings.append(Finding(
                check_id="SHADOW-001",
                severity=Severity.HIGH,
                title=f"Duplicate server name: {server.name}",
                description=f"Multiple servers share the name '{server.name}'. "
                            f"This can cause tool shadowing where one server's tools "
                            f"override another's, potentially intercepting sensitive operations.",
                server_name=server.name,
                evidence=f"Duplicate: '{server.name}' appears multiple times",
                recommendation="Use unique server names to prevent tool shadowing.",
            ))
        names[lower] = server

    # Check for servers that might shadow common tool providers
    # (e.g., a server named "filesystem" alongside another filesystem tool)
    tool_categories = {}
    for server in servers:
        category = _categorize_server(server)
        if category:
            if category in tool_categories:
                findings.append(Finding(
                    check_id="SHADOW-002",
                    severity=Severity.MEDIUM,
                    title=f"Potential tool overlap: {category}",
                    description=f"Servers '{tool_categories[category]}' and '{server.name}' "
                                f"may provide overlapping '{category}' tools. "
                                f"This increases tool shadowing risk.",
                    server_name=server.name,
                    evidence=f"Both servers appear to serve '{category}' functionality",
                    recommendation="Review tool names across these servers for conflicts.",
                ))
            tool_categories[category] = server.name

    return findings


def _categorize_server(server: ServerConfig) -> str | None:
    """Try to categorize a server by its likely tool domain."""
    combined = f"{server.name} {server.command or ''} {' '.join(server.args)}".lower()
    categories = {
        "filesystem": ["filesystem", "file-server", "fs-server", "file_system"],
        "git": ["git-server", "git-mcp", "github", "gitlab"],
        "database": ["database", "db-server", "postgres", "mysql", "sqlite", "mongo"],
        "http": ["http-server", "fetch", "web-client", "curl"],
        "docker": ["docker", "container", "podman"],
        "shell": ["shell", "terminal", "bash", "exec"],
    }
    for category, patterns in categories.items():
        if any(p in combined for p in patterns):
            return category
    return None
