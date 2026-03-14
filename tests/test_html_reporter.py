"""Tests for HTML report generation."""

from __future__ import annotations

import pytest

from mcpscan.models import Finding, ScanReport, ServerConfig, Severity
from mcpscan.reporters.html_reporter import generate_html_report


def _make_report(findings: list[Finding] | None = None, score: int = 75) -> ScanReport:
    """Create a test report."""
    servers = [
        ServerConfig(name="test-server", command="node", args=["server.js"], transport="stdio"),
        ServerConfig(name="remote-api", url="https://api.example.com/mcp", transport="sse"),
    ]
    if findings is None:
        findings = [
            Finding(
                check_id="CRED-001",
                severity=Severity.CRITICAL,
                title="API key exposed",
                description="API key found in environment variable.",
                server_name="test-server",
                evidence="API_KEY=sk-proj-abc123...",
                recommendation="Use a secrets manager.",
            ),
            Finding(
                check_id="PERM-001",
                severity=Severity.HIGH,
                title="Unrestricted shell",
                description="Shell execution without restrictions.",
                server_name="test-server",
            ),
            Finding(
                check_id="VAL-001",
                severity=Severity.MEDIUM,
                title="Unpinned version",
                description="Package version is not pinned.",
                server_name="test-server",
                recommendation="Pin to a specific version.",
            ),
            Finding(
                check_id="TRANS-001",
                severity=Severity.LOW,
                title="HTTP endpoint",
                description="Unencrypted HTTP connection.",
                server_name="remote-api",
            ),
        ]
    report = ScanReport(
        config_path="/test/config.json",
        config_format="Claude Desktop",
        servers=servers,
        findings=findings,
        score=score,
    )
    return report


class TestHtmlReporter:
    def test_generates_valid_html(self):
        report = _make_report()
        html = generate_html_report(report)
        assert html.startswith("<!DOCTYPE html>")
        assert "</html>" in html

    def test_contains_config_path(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "/test/config.json" in html

    def test_contains_score(self):
        report = _make_report(score=75)
        html = generate_html_report(report)
        assert ">75<" in html

    def test_contains_severity_counts(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "CRITICAL" in html
        assert "HIGH" in html
        assert "MEDIUM" in html
        assert "LOW" in html

    def test_contains_finding_details(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "CRED-001" in html
        assert "API key exposed" in html
        assert "Use a secrets manager." in html

    def test_contains_server_info(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "test-server" in html
        assert "remote-api" in html

    def test_contains_dark_theme_colors(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "#0a0a0b" in html
        assert "#06b6d4" in html

    def test_self_contained_css(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "<style>" in html
        # No external CSS links
        assert '<link rel="stylesheet"' not in html

    def test_contains_version(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "MCPScan v0.2.0" in html or "MCPScan v" in html

    def test_contains_timestamp(self):
        report = _make_report()
        html = generate_html_report(report)
        assert "UTC" in html

    def test_empty_findings(self):
        report = _make_report(findings=[], score=100)
        html = generate_html_report(report)
        assert "No security issues found" in html

    def test_html_escaping(self):
        """Ensure special characters are escaped."""
        findings = [
            Finding(
                check_id="TEST-001",
                severity=Severity.HIGH,
                title='XSS <script>alert("test")</script>',
                description="Description with <b>HTML</b>",
                server_name="server&name",
                evidence='key="value"',
            ),
        ]
        report = _make_report(findings=findings)
        html = generate_html_report(report)
        assert "<script>alert" not in html
        assert "&lt;script&gt;" in html
        assert "server&amp;name" in html

    def test_score_colors(self):
        # High score = green
        report_good = _make_report(score=85)
        html_good = generate_html_report(report_good)
        assert "#22c55e" in html_good

        # Medium score = yellow
        report_mid = _make_report(score=50)
        html_mid = generate_html_report(report_mid)
        assert "#eab308" in html_mid

        # Low score = red
        report_bad = _make_report(score=20)
        html_bad = generate_html_report(report_bad)
        assert "#ef4444" in html_bad

    def test_evidence_and_recommendation_optional(self):
        findings = [
            Finding(
                check_id="TEST-001",
                severity=Severity.INFO,
                title="Info finding",
                description="Just info",
                server_name="srv",
            ),
        ]
        report = _make_report(findings=findings)
        html = generate_html_report(report)
        assert "INFO" in html
        assert "—" in html  # em-dash for missing fields
