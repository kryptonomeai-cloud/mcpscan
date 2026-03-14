"""MCPScan CLI — scan MCP server configs for security vulnerabilities."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .parsers import parse_config
from .checks import run_all_checks
from .models import ScanReport
from .reporter import print_report


@click.group()
@click.version_option(version=__version__, prog_name="mcpscan")
def main():
    """MCPScan — Local-first MCP security scanner.

    Scan MCP server configurations for security vulnerabilities,
    credential exposure, SSRF risks, and more.
    """
    pass


@main.command()
@click.argument("config_path", type=click.Path(exists=True))
@click.option("--format", "-f", "output_format",
              type=click.Choice(["terminal", "json", "markdown"]),
              default="terminal",
              help="Output format.")
@click.option("--report", "-r", "report_format",
              type=click.Choice(["html", "json", "sarif"]),
              default=None,
              help="Generate a report file (html=standalone HTML, json/sarif=SARIF JSON).")
@click.option("--output", "-o", "output_file",
              type=click.Path(),
              help="Write report to file (default: stdout).")
@click.option("--fail-on", "fail_severity",
              type=click.Choice(["critical", "high", "medium", "low"]),
              default=None,
              help="Exit with code 1 if findings at this severity or above.")
@click.option("--dynamic", is_flag=True, default=False,
              help="Enable dynamic checks (TCP connectivity, TLS inspection, HTTP probing).")
def scan(config_path: str, output_format: str, report_format: str | None, output_file: str | None, fail_severity: str | None, dynamic: bool):
    """Scan an MCP config file for security issues.

    CONFIG_PATH is the path to a JSON config file (Claude Desktop or mcporter format).

    Examples:

        mcpscan scan ~/.config/claude/claude_desktop_config.json

        mcpscan scan config.json --report html -o report.html

        mcpscan scan config.json --report json -o sarif.json

        mcpscan scan config.json --fail-on high
    """
    console = Console(stderr=True)

    try:
        fmt, servers = parse_config(config_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(2)

    if not servers:
        console.print("[yellow]No MCP servers found in config.[/yellow]")
        sys.exit(0)

    findings = run_all_checks(servers, dynamic=dynamic)

    report = ScanReport(
        config_path=config_path,
        config_format=fmt,
        servers=servers,
        findings=findings,
    )
    report.compute_score()

    # Handle --report flag for new report formats
    if report_format:
        if report_format == "html":
            from .reporters.html_reporter import generate_html_report
            text = generate_html_report(report)
            out_path = output_file or "mcpscan-report.html"
            Path(out_path).write_text(text)
            console.print(f"[green]HTML report written to {out_path}[/green]")
        elif report_format in ("json", "sarif"):
            from .reporters.json_reporter import generate_sarif_report
            text = generate_sarif_report(report)
            if output_file:
                Path(output_file).write_text(text)
                console.print(f"[green]SARIF report written to {output_file}[/green]")
            else:
                click.echo(text)

    # Standard output (unless --report was used and no --format explicitly set)
    elif output_format == "terminal":
        out_console = Console(file=open(output_file, "w") if output_file else None)
        print_report(report, out_console)
        if output_file:
            console.print(f"[green]Report written to {output_file}[/green]")
    elif output_format == "json":
        text = report.to_json()
        if output_file:
            Path(output_file).write_text(text)
            console.print(f"[green]JSON report written to {output_file}[/green]")
        else:
            click.echo(text)
    elif output_format == "markdown":
        text = report.to_markdown()
        if output_file:
            Path(output_file).write_text(text)
            console.print(f"[green]Markdown report written to {output_file}[/green]")
        else:
            click.echo(text)

    # Exit code based on --fail-on
    if fail_severity:
        from .models import Severity
        threshold = Severity(fail_severity)
        if any(f.severity.rank >= threshold.rank for f in findings):
            sys.exit(1)


@main.command()
@click.argument("baseline", type=click.Path(exists=True))
@click.argument("current", type=click.Path(exists=True))
@click.option("--format", "-f", "output_format",
              type=click.Choice(["terminal", "json"]),
              default="terminal",
              help="Output format.")
@click.option("--fail-on-new", is_flag=True, default=False,
              help="Exit with code 1 if new findings are present.")
def diff(baseline: str, current: str, output_format: str, fail_on_new: bool):
    """Compare two scan results to find new and resolved findings.

    Useful for PR checks: "did this change introduce new security issues?"

    Supports both mcpscan native JSON and SARIF formats.

    Examples:

        mcpscan diff baseline.json current.json

        mcpscan diff before.json after.json --fail-on-new

        mcpscan diff baseline.json current.json --format json
    """
    from .commands.diff import diff_reports

    console = Console(stderr=True)

    try:
        result = diff_reports(baseline, current)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(2)

    if output_format == "json":
        click.echo(result.to_json())
    else:
        # Terminal output
        out = Console()
        out.print()

        # Score delta
        delta = result.score_delta
        if delta > 0:
            delta_str = f"[green]+{delta}[/green]"
        elif delta < 0:
            delta_str = f"[red]{delta}[/red]"
        else:
            delta_str = "[dim]±0[/dim]"

        out.print(f"[bold]📊 MCPScan Diff Report[/bold]")
        out.print(f"  Baseline score: {result.baseline_score}/100")
        out.print(f"  Current score:  {result.current_score}/100 ({delta_str})")
        out.print()

        out.print(f"  [green]✅ Resolved:[/green] {len(result.resolved_findings)}")
        out.print(f"  [red]🆕 New:[/red]      {len(result.new_findings)}")
        out.print(f"  [dim]➖ Unchanged:[/dim] {len(result.unchanged_findings)}")
        out.print()

        if result.resolved_findings:
            out.print("[green bold]Resolved findings:[/green bold]")
            for f in result.resolved_findings:
                _print_diff_finding(out, f, prefix="  [green]✅[/green]")
            out.print()

        if result.new_findings:
            out.print("[red bold]New findings:[/red bold]")
            for f in result.new_findings:
                _print_diff_finding(out, f, prefix="  [red]🆕[/red]")
            out.print()

        if not result.new_findings and not result.resolved_findings:
            out.print("[dim]No changes between scans.[/dim]")

    if fail_on_new and result.has_new_issues:
        sys.exit(1)


def _print_diff_finding(console: Console, finding: dict, prefix: str = "  ") -> None:
    """Print a single finding from a diff result."""
    # Handle both SARIF and native formats
    if "ruleId" in finding:
        rule = finding["ruleId"]
        msg = finding.get("message", {}).get("text", "")
        sev = finding.get("properties", {}).get("severity", finding.get("level", ""))
        console.print(f"{prefix} [{rule}] {sev.upper()} — {msg}")
    else:
        rule = finding.get("check_id", "")
        title = finding.get("title", "")
        sev = finding.get("severity", "")
        console.print(f"{prefix} [{rule}] {sev.upper()} — {title}")


@main.command()
@click.option("--json", "as_json", is_flag=True, default=False,
              help="Output as JSON.")
@click.option("--scan", "auto_scan", is_flag=True, default=False,
              help="Automatically scan all discovered configs.")
@click.option("--extra", "-e", multiple=True,
              help="Additional config paths to check.")
def discover(as_json: bool, auto_scan: bool, extra: tuple[str, ...]):
    """Auto-discover MCP configuration files on the system.

    Scans well-known locations for Claude Desktop, Cursor, mcporter,
    VS Code, Windsurf, Continue.dev and more.

    Examples:

        mcpscan discover

        mcpscan discover --json

        mcpscan discover --scan

        mcpscan discover --extra ~/my-project/mcp-config.json
    """
    from .checks.discovery import discover_configs

    console = Console(stderr=True)
    configs = discover_configs(extra_paths=list(extra) if extra else None)

    if not configs:
        if as_json:
            click.echo(json.dumps({"configs": [], "total": 0}))
        else:
            console.print("[yellow]No MCP configuration files found.[/yellow]")
        return

    if as_json:
        click.echo(json.dumps({
            "configs": [c.to_dict() for c in configs],
            "total": len(configs),
        }, indent=2))
    else:
        console.print(f"\n[bold]🔍 Discovered {len(configs)} MCP configuration(s):[/bold]\n")
        for c in configs:
            status = f"[green]✓[/green] {c.server_count} server(s)" if not c.error else f"[red]✗ {c.error}[/red]"
            console.print(f"  [cyan]{c.client}[/cyan]")
            console.print(f"    Path: {c.path}")
            console.print(f"    {status}")
            console.print()

    if auto_scan:
        console.print("[bold]Running scans on discovered configs...[/bold]\n")
        for c in configs:
            if c.error or c.server_count == 0:
                continue
            console.print(f"[cyan]━━━ Scanning: {c.client} ({c.path}) ━━━[/cyan]")
            try:
                fmt, servers = parse_config(c.path)
                findings = run_all_checks(servers)
                report = ScanReport(
                    config_path=c.path,
                    config_format=fmt,
                    servers=servers,
                    findings=findings,
                )
                report.compute_score()
                print_report(report, Console())
            except Exception as e:
                console.print(f"  [red]Error scanning: {e}[/red]")
            console.print()


@main.command()
@click.argument("config_path", type=click.Path(exists=True))
def info(config_path: str):
    """Show parsed server information without running checks.

    Useful for verifying config parsing.
    """
    console = Console()

    try:
        fmt, servers = parse_config(config_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(2)

    console.print(f"[bold]Format:[/bold] {fmt}")
    console.print(f"[bold]Servers:[/bold] {len(servers)}")
    console.print()

    for s in servers:
        console.print(f"[cyan bold]{s.name}[/cyan bold]")
        console.print(f"  Transport: {s.transport}")
        if s.command:
            console.print(f"  Command: {s.command} {' '.join(s.args)}")
        if s.url:
            console.print(f"  URL: {s.url}")
        if s.env:
            console.print(f"  Env vars: {', '.join(s.env.keys())}")
        console.print()


if __name__ == "__main__":
    main()
