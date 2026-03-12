"""Data models for MCPScan findings and reports."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Finding severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

    @property
    def rank(self) -> int:
        return {
            Severity.CRITICAL: 5,
            Severity.HIGH: 4,
            Severity.MEDIUM: 3,
            Severity.LOW: 2,
            Severity.INFO: 1,
        }[self]

    @property
    def emoji(self) -> str:
        return {
            Severity.CRITICAL: "🔴",
            Severity.HIGH: "🟠",
            Severity.MEDIUM: "🟡",
            Severity.LOW: "🔵",
            Severity.INFO: "⚪",
        }[self]


@dataclass
class Finding:
    """A single security finding."""
    check_id: str
    severity: Severity
    title: str
    description: str
    server_name: str
    evidence: Optional[str] = None
    recommendation: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["severity"] = self.severity.value
        return d


@dataclass
class ServerConfig:
    """Parsed MCP server configuration."""
    name: str
    command: Optional[str] = None
    args: list[str] = field(default_factory=list)
    url: Optional[str] = None
    env: dict[str, str] = field(default_factory=dict)
    transport: str = "stdio"  # stdio, sse, http
    raw: dict = field(default_factory=dict)


@dataclass
class ScanReport:
    """Complete scan report."""
    config_path: str
    config_format: str
    servers: list[ServerConfig]
    findings: list[Finding]
    score: int = 100

    def compute_score(self) -> int:
        """Compute security score 0-100 (higher = better)."""
        penalty = 0
        for f in self.findings:
            penalty += {
                Severity.CRITICAL: 25,
                Severity.HIGH: 15,
                Severity.MEDIUM: 8,
                Severity.LOW: 3,
                Severity.INFO: 0,
            }[f.severity]
        self.score = max(0, 100 - penalty)
        return self.score

    @property
    def score_label(self) -> str:
        if self.score >= 90:
            return "Excellent"
        elif self.score >= 70:
            return "Good"
        elif self.score >= 50:
            return "Fair"
        elif self.score >= 30:
            return "Poor"
        return "Critical"

    def to_dict(self) -> dict:
        return {
            "config_path": self.config_path,
            "config_format": self.config_format,
            "servers_scanned": len(self.servers),
            "score": self.score,
            "score_label": self.score_label,
            "findings_summary": {
                s.value: len([f for f in self.findings if f.severity == s])
                for s in Severity
            },
            "findings": [f.to_dict() for f in self.findings],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def to_markdown(self) -> str:
        lines = [
            f"# MCPScan Report",
            f"",
            f"**Config:** `{self.config_path}`  ",
            f"**Format:** {self.config_format}  ",
            f"**Servers scanned:** {len(self.servers)}  ",
            f"**Score:** {self.score}/100 ({self.score_label})",
            f"",
        ]
        by_severity = {}
        for f in self.findings:
            by_severity.setdefault(f.severity, []).append(f)

        for sev in Severity:
            items = by_severity.get(sev, [])
            if not items:
                continue
            lines.append(f"## {sev.emoji} {sev.value.upper()} ({len(items)})")
            lines.append("")
            for f in items:
                lines.append(f"### [{f.check_id}] {f.title}")
                lines.append(f"**Server:** `{f.server_name}`  ")
                lines.append(f"{f.description}")
                if f.evidence:
                    lines.append(f"")
                    lines.append(f"**Evidence:**")
                    lines.append(f"```")
                    lines.append(f"{f.evidence}")
                    lines.append(f"```")
                if f.recommendation:
                    lines.append(f"")
                    lines.append(f"**Recommendation:** {f.recommendation}")
                lines.append("")
        return "\n".join(lines)
