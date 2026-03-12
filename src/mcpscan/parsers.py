"""Config file parsers for MCP server configurations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import ServerConfig


def detect_format(data: dict) -> str:
    """Detect whether config is Claude Desktop or mcporter format."""
    if "mcpServers" in data:
        return "mcporter/claude-desktop"
    if "servers" in data and isinstance(data["servers"], list):
        return "mcporter-list"
    # Claude Desktop also uses mcpServers key at top level
    return "unknown"


def parse_config(path: str | Path) -> tuple[str, list[ServerConfig]]:
    """Parse an MCP config file and return (format, servers).

    Supports:
    - Claude Desktop / mcporter format (mcpServers dict)
    - Array-of-servers format
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        data = json.load(f)

    fmt = detect_format(data)
    servers: list[ServerConfig] = []

    if fmt == "mcporter/claude-desktop":
        servers = _parse_mcpservers_dict(data["mcpServers"])
    elif fmt == "mcporter-list":
        for entry in data["servers"]:
            servers.append(_parse_server_entry(entry.get("name", "unnamed"), entry))
    else:
        # Try treating the whole thing as mcpServers dict
        if all(isinstance(v, dict) for v in data.values()):
            servers = _parse_mcpservers_dict(data)
            fmt = "claude-desktop-root"
        else:
            raise ValueError(f"Unrecognised config format in {path}")

    return fmt, servers


def _parse_mcpservers_dict(servers_dict: dict) -> list[ServerConfig]:
    """Parse the mcpServers dict format (used by Claude Desktop and mcporter)."""
    servers = []
    for name, config in servers_dict.items():
        servers.append(_parse_server_entry(name, config))
    return servers


def _parse_server_entry(name: str, config: dict) -> ServerConfig:
    """Parse a single server entry."""
    # Determine transport
    transport = "stdio"
    url = config.get("url")
    if url:
        if "sse" in url.lower() or url.endswith("/sse"):
            transport = "sse"
        elif url.startswith("http"):
            transport = "http"

    # Parse command — can be string or list
    command = config.get("command")
    args = config.get("args", [])
    if isinstance(command, list):
        args = command[1:] + args
        command = command[0]

    return ServerConfig(
        name=name,
        command=command,
        args=args if isinstance(args, list) else [args],
        url=url,
        env=config.get("env", {}),
        transport=transport,
        raw=config,
    )
