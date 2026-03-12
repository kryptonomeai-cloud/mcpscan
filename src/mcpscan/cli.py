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
@click.option("--output", "-o", "output_file",
              type=click.Path(),
              help="Write report to file (default: stdout).")
@click.option("--fail-on", "fail_severity",
              type=click.Choice(["critical", "high", "medium", "low"]),
              default=None,
              help="Exit with code 1 if findings at this severity or above.")
def scan(config_path: str, output_format: str, output_file: str | None, fail_severity: str | None):
    """Scan an MCP config file for security issues.

    CONFIG_PATH is the path to a JSON config file (Claude Desktop or mcporter format).

    Examples:

        mcpscan scan ~/.config/claude/claude_desktop_config.json

        mcpscan scan config/mcporter.json --format json -o report.json

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

    findings = run_all_checks(servers)

    report = ScanReport(
        config_path=config_path,
        config_format=fmt,
        servers=servers,
        findings=findings,
    )
    report.compute_score()

    # Output
    if output_format == "terminal":
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
