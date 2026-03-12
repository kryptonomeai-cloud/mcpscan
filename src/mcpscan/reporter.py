"""Rich terminal reporter for MCPScan."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import ScanReport, Severity

SEVERITY_STYLES = {
    Severity.CRITICAL: "bold red",
    Severity.HIGH: "bold bright_red",
    Severity.MEDIUM: "bold yellow",
    Severity.LOW: "bold blue",
    Severity.INFO: "dim",
}


def print_report(report: ScanReport, console: Console | None = None) -> None:
    """Print a coloured scan report to the terminal."""
    if console is None:
        console = Console()

    # Header
    console.print()
    console.print(Panel.fit(
        f"[bold]MCPScan Report[/bold]\n"
        f"Config: [cyan]{report.config_path}[/cyan]\n"
        f"Format: {report.config_format}\n"
        f"Servers: {len(report.servers)}",
        border_style="blue",
    ))

    # Servers table
    srv_table = Table(title="Servers Scanned", show_lines=False)
    srv_table.add_column("Name", style="cyan")
    srv_table.add_column("Transport")
    srv_table.add_column("Command / URL")
    for s in report.servers:
        target = s.url or f"{s.command or ''} {' '.join(s.args)}".strip()
        if len(target) > 60:
            target = target[:57] + "..."
        srv_table.add_row(s.name, s.transport, target)
    console.print(srv_table)
    console.print()

    if not report.findings:
        console.print("[bold green]✅ No security issues found![/bold green]")
        console.print()
        _print_score(console, report)
        return

    # Findings grouped by severity
    by_severity: dict[Severity, list] = {}
    for f in report.findings:
        by_severity.setdefault(f.severity, []).append(f)

    for sev in Severity:
        items = by_severity.get(sev, [])
        if not items:
            continue

        style = SEVERITY_STYLES[sev]
        console.print(f"[{style}]{sev.emoji} {sev.value.upper()} ({len(items)})[/{style}]")
        for f in items:
            console.print(f"  [{style}][{f.check_id}][/{style}] {f.title}")
            console.print(f"    Server: [cyan]{f.server_name}[/cyan]")
            console.print(f"    {f.description}")
            if f.evidence:
                console.print(f"    [dim]Evidence: {f.evidence}[/dim]")
            if f.recommendation:
                console.print(f"    [green]→ {f.recommendation}[/green]")
            console.print()

    _print_score(console, report)


def _print_score(console: Console, report: ScanReport) -> None:
    """Print the security score."""
    score = report.score
    if score >= 70:
        color = "green"
    elif score >= 40:
        color = "yellow"
    else:
        color = "red"

    console.print(Panel.fit(
        f"[bold {color}]Score: {score}/100 ({report.score_label})[/bold {color}]",
        border_style=color,
    ))
