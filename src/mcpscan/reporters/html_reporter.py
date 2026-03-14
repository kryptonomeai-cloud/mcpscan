"""Standalone HTML report generator for MCPScan."""

from __future__ import annotations

import html
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from .. import __version__

if TYPE_CHECKING:
    from ..models import ScanReport, Severity


_SEVERITY_COLORS = {
    "critical": "#ef4444",
    "high": "#f97316",
    "medium": "#eab308",
    "low": "#3b82f6",
    "info": "#6b7280",
}

_SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]


def _esc(text: str | None) -> str:
    """HTML-escape text."""
    return html.escape(str(text)) if text else ""


def generate_html_report(report: "ScanReport") -> str:
    """Generate a self-contained HTML report string."""
    from ..models import Severity

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Count by severity
    counts: dict[str, int] = {s.value: 0 for s in Severity}
    for f in report.findings:
        counts[f.severity.value] += 1

    total_findings = len(report.findings)

    # Score colour
    if report.score >= 70:
        score_color = "#22c55e"
    elif report.score >= 40:
        score_color = "#eab308"
    else:
        score_color = "#ef4444"

    # Build findings rows
    findings_rows = []
    for f in report.findings:
        sev_color = _SEVERITY_COLORS.get(f.severity.value, "#6b7280")
        findings_rows.append(f"""
        <tr>
            <td><span class="badge" style="background:{sev_color}">{_esc(f.severity.value.upper())}</span></td>
            <td class="mono">{_esc(f.check_id)}</td>
            <td>{_esc(f.title)}</td>
            <td class="mono">{_esc(f.server_name)}</td>
            <td>{_esc(f.description)}</td>
            <td>{_esc(f.evidence) if f.evidence else '<span class="dim">—</span>'}</td>
            <td>{_esc(f.recommendation) if f.recommendation else '<span class="dim">—</span>'}</td>
        </tr>""")

    findings_html = "\n".join(findings_rows) if findings_rows else """
        <tr><td colspan="7" style="text-align:center;padding:2rem;color:#22c55e">✅ No security issues found!</td></tr>"""

    # Summary cards
    summary_cards = []
    for sev_name in _SEVERITY_ORDER:
        count = counts.get(sev_name, 0)
        color = _SEVERITY_COLORS[sev_name]
        summary_cards.append(
            f'<div class="card"><div class="card-count" style="color:{color}">{count}</div>'
            f'<div class="card-label">{sev_name.upper()}</div></div>'
        )
    cards_html = "\n".join(summary_cards)

    # Servers list
    servers_rows = []
    for s in report.servers:
        target = s.url or f"{s.command or ''} {' '.join(s.args)}".strip()
        servers_rows.append(f"""
        <tr>
            <td class="mono">{_esc(s.name)}</td>
            <td>{_esc(s.transport)}</td>
            <td class="mono">{_esc(target)}</td>
        </tr>""")
    servers_html = "\n".join(servers_rows)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MCPScan Report — {_esc(report.config_path)}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a0b;color:#e4e4e7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;line-height:1.6;padding:2rem}}
.container{{max-width:1200px;margin:0 auto}}
h1{{color:#06b6d4;font-size:1.8rem;margin-bottom:.25rem}}
h2{{color:#06b6d4;font-size:1.3rem;margin:2rem 0 1rem;border-bottom:1px solid #27272a;padding-bottom:.5rem}}
.meta{{color:#71717a;font-size:.85rem;margin-bottom:2rem}}
.meta span{{margin-right:1.5rem}}
.score-box{{display:inline-flex;align-items:center;gap:1rem;background:#18181b;border:1px solid #27272a;border-radius:12px;padding:1rem 2rem;margin-bottom:2rem}}
.score-number{{font-size:2.5rem;font-weight:700}}
.score-label{{color:#a1a1aa;font-size:.9rem}}
.cards{{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:2rem}}
.card{{background:#18181b;border:1px solid #27272a;border-radius:8px;padding:1rem 1.5rem;min-width:120px;text-align:center}}
.card-count{{font-size:1.8rem;font-weight:700}}
.card-label{{color:#a1a1aa;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em}}
table{{width:100%;border-collapse:collapse;background:#18181b;border-radius:8px;overflow:hidden;margin-bottom:1rem}}
th{{background:#27272a;color:#06b6d4;text-align:left;padding:.75rem 1rem;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em}}
td{{padding:.65rem 1rem;border-bottom:1px solid #27272a;font-size:.85rem;vertical-align:top}}
tr:last-child td{{border-bottom:none}}
tr:hover td{{background:#1f1f23}}
.badge{{display:inline-block;padding:.15rem .5rem;border-radius:4px;font-size:.7rem;font-weight:600;color:#0a0a0b}}
.mono{{font-family:'SF Mono',Consolas,monospace;font-size:.8rem}}
.dim{{color:#52525b}}
footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid #27272a;color:#52525b;font-size:.75rem;text-align:center}}
@media(max-width:768px){{body{{padding:1rem}}.cards{{flex-direction:column}}table{{font-size:.75rem}}}}
</style>
</head>
<body>
<div class="container">
    <h1>🛡️ MCPScan Security Report</h1>
    <div class="meta">
        <span>📄 <strong>{_esc(report.config_path)}</strong></span>
        <span>📋 {_esc(report.config_format)}</span>
        <span>🕐 {timestamp}</span>
    </div>

    <div class="score-box">
        <div class="score-number" style="color:{score_color}">{report.score}</div>
        <div>
            <div style="font-size:1.1rem;font-weight:600">/100</div>
            <div class="score-label">{_esc(report.score_label)}</div>
        </div>
    </div>

    <h2>Summary</h2>
    <div class="cards">
        {cards_html}
        <div class="card">
            <div class="card-count" style="color:#06b6d4">{total_findings}</div>
            <div class="card-label">TOTAL</div>
        </div>
    </div>

    <h2>Servers Scanned ({len(report.servers)})</h2>
    <table>
        <thead><tr><th>Name</th><th>Transport</th><th>Command / URL</th></tr></thead>
        <tbody>{servers_html}</tbody>
    </table>

    <h2>Findings ({total_findings})</h2>
    <table>
        <thead><tr><th>Severity</th><th>Rule</th><th>Title</th><th>Server</th><th>Description</th><th>Evidence</th><th>Remediation</th></tr></thead>
        <tbody>{findings_html}</tbody>
    </table>

    <footer>
        Generated by MCPScan v{__version__} — {timestamp}<br>
        100% local scan · zero cloud dependencies
    </footer>
</div>
</body>
</html>"""
