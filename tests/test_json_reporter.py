"""Tests for SARIF JSON report generation."""

from __future__ import annotations

import json

import pytest

from mcpscan.models import Finding, ScanReport, ServerConfig, Severity
from mcpscan.reporters.json_reporter import generate_sarif_report


def _make_report(findings: list[Finding] | None = None, score: int = 75) -> ScanReport:
    """Create a test report."""
    servers = [
        ServerConfig(name="test-server", command="node", args=["server.js"], transport="stdio"),
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
        ]
    report = ScanReport(
        config_path="/test/config.json",
        config_format="Claude Desktop",
        servers=servers,
        findings=findings,
        score=score,
    )
    return report


class TestSarifReporter:
    def test_valid_json(self):
        report = _make_report()
        result = generate_sarif_report(report)
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_sarif_schema(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        assert data["version"] == "2.1.0"
        assert "$schema" in data
        assert "oasis-open.org" in data["$schema"]

    def test_has_runs(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        assert "runs" in data
        assert len(data["runs"]) == 1

    def test_tool_driver(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        driver = data["runs"][0]["tool"]["driver"]
        assert driver["name"] == "MCPScan"
        assert "version" in driver
        assert "rules" in driver

    def test_rules_from_findings(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        rules = data["runs"][0]["tool"]["driver"]["rules"]
        rule_ids = [r["id"] for r in rules]
        assert "CRED-001" in rule_ids
        assert "PERM-001" in rule_ids
        assert "VAL-001" in rule_ids

    def test_results_count(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        results = data["runs"][0]["results"]
        assert len(results) == 3

    def test_result_structure(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        result = data["runs"][0]["results"][0]
        assert "ruleId" in result
        assert "level" in result
        assert "message" in result
        assert "locations" in result

    def test_severity_mapping(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        results = data["runs"][0]["results"]
        # Critical -> error
        cred = next(r for r in results if r["ruleId"] == "CRED-001")
        assert cred["level"] == "error"
        # Medium -> warning
        val = next(r for r in results if r["ruleId"] == "VAL-001")
        assert val["level"] == "warning"

    def test_location_includes_config_path(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        result = data["runs"][0]["results"][0]
        artifact = result["locations"][0]["physicalLocation"]["artifactLocation"]
        assert artifact["uri"] == "/test/config.json"

    def test_location_includes_server_name(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        result = data["runs"][0]["results"][0]
        logical = result["locations"][0]["logicalLocations"]
        assert logical[0]["name"] == "test-server"

    def test_evidence_in_properties(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        cred = next(r for r in data["runs"][0]["results"] if r["ruleId"] == "CRED-001")
        assert cred["properties"]["evidence"] == "API_KEY=sk-proj-abc123..."

    def test_recommendation_in_rule_help(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        rules = data["runs"][0]["tool"]["driver"]["rules"]
        cred_rule = next(r for r in rules if r["id"] == "CRED-001")
        assert "help" in cred_rule
        assert "secrets manager" in cred_rule["help"]["text"]

    def test_invocations(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        invocations = data["runs"][0]["invocations"]
        assert len(invocations) == 1
        assert invocations[0]["executionSuccessful"] is True

    def test_mcpscan_properties(self):
        report = _make_report(score=75)
        data = json.loads(generate_sarif_report(report))
        props = data["runs"][0]["properties"]["mcpscan"]
        assert props["score"] == 75
        assert props["configPath"] == "/test/config.json"
        assert props["serversScanned"] == 1

    def test_empty_findings(self):
        report = _make_report(findings=[], score=100)
        data = json.loads(generate_sarif_report(report))
        assert data["runs"][0]["results"] == []
        assert data["runs"][0]["tool"]["driver"]["rules"] == []

    def test_deduplicated_rules(self):
        """Same check_id from multiple servers should produce one rule."""
        findings = [
            Finding(check_id="CRED-001", severity=Severity.CRITICAL,
                    title="API key exposed", description="Key found.",
                    server_name="server-a"),
            Finding(check_id="CRED-001", severity=Severity.CRITICAL,
                    title="API key exposed", description="Key found.",
                    server_name="server-b"),
        ]
        report = _make_report(findings=findings)
        data = json.loads(generate_sarif_report(report))
        rules = data["runs"][0]["tool"]["driver"]["rules"]
        assert len(rules) == 1
        assert len(data["runs"][0]["results"]) == 2

    def test_security_severity_property(self):
        report = _make_report()
        data = json.loads(generate_sarif_report(report))
        rules = data["runs"][0]["tool"]["driver"]["rules"]
        cred_rule = next(r for r in rules if r["id"] == "CRED-001")
        assert "security-severity" in cred_rule["properties"]
        assert float(cred_rule["properties"]["security-severity"]) == 9.5
