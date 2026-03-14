"""Tests for the diff command."""

from __future__ import annotations

import json
import os
import tempfile

import pytest

from mcpscan.commands.diff import diff_reports, DiffResult, _finding_key


@pytest.fixture
def baseline_native(tmp_path):
    """Create a native mcpscan JSON baseline."""
    data = {
        "config_path": "/test/config.json",
        "config_format": "Claude Desktop",
        "servers_scanned": 2,
        "score": 60,
        "score_label": "Fair",
        "findings_summary": {"critical": 1, "high": 1, "medium": 0, "low": 0, "info": 0},
        "findings": [
            {
                "check_id": "CRED-001",
                "severity": "critical",
                "title": "API key exposed",
                "description": "API key in env var.",
                "server_name": "server-a",
                "evidence": "API_KEY=sk-...",
                "recommendation": "Use secrets manager.",
            },
            {
                "check_id": "PERM-001",
                "severity": "high",
                "title": "Unrestricted shell",
                "description": "Shell without restrictions.",
                "server_name": "server-a",
                "evidence": None,
                "recommendation": "Restrict shell access.",
            },
        ],
    }
    path = tmp_path / "baseline.json"
    path.write_text(json.dumps(data))
    return str(path)


@pytest.fixture
def current_native(tmp_path):
    """Create a native mcpscan JSON current scan with changes."""
    data = {
        "config_path": "/test/config.json",
        "config_format": "Claude Desktop",
        "servers_scanned": 2,
        "score": 85,
        "score_label": "Good",
        "findings_summary": {"critical": 0, "high": 0, "medium": 1, "low": 0, "info": 0},
        "findings": [
            # CRED-001 resolved, PERM-001 resolved
            # New finding:
            {
                "check_id": "VAL-001",
                "severity": "medium",
                "title": "Unpinned version",
                "description": "Package not pinned.",
                "server_name": "server-b",
                "evidence": None,
                "recommendation": "Pin version.",
            },
        ],
    }
    path = tmp_path / "current.json"
    path.write_text(json.dumps(data))
    return str(path)


@pytest.fixture
def baseline_sarif(tmp_path):
    """Create a SARIF baseline."""
    data = {
        "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "MCPScan", "version": "0.2.0", "rules": []}},
            "results": [
                {
                    "ruleId": "CRED-001",
                    "level": "error",
                    "message": {"text": "API key exposed"},
                    "locations": [{
                        "physicalLocation": {"artifactLocation": {"uri": "/test/config.json"}},
                        "logicalLocations": [{"name": "server-a", "kind": "module"}],
                    }],
                    "properties": {"severity": "critical", "server": "server-a"},
                },
                {
                    "ruleId": "SSRF-001",
                    "level": "error",
                    "message": {"text": "Internal network access"},
                    "locations": [{
                        "physicalLocation": {"artifactLocation": {"uri": "/test/config.json"}},
                        "logicalLocations": [{"name": "server-b", "kind": "module"}],
                    }],
                    "properties": {"severity": "high", "server": "server-b"},
                },
            ],
            "invocations": [{"executionSuccessful": True}],
            "properties": {"mcpscan": {"score": 50}},
        }],
    }
    path = tmp_path / "baseline_sarif.json"
    path.write_text(json.dumps(data))
    return str(path)


@pytest.fixture
def current_sarif(tmp_path):
    """Create a SARIF current scan — SSRF-001 resolved, TRANS-001 new."""
    data = {
        "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "MCPScan", "version": "0.2.0", "rules": []}},
            "results": [
                {
                    "ruleId": "CRED-001",
                    "level": "error",
                    "message": {"text": "API key exposed"},
                    "locations": [{
                        "physicalLocation": {"artifactLocation": {"uri": "/test/config.json"}},
                        "logicalLocations": [{"name": "server-a", "kind": "module"}],
                    }],
                    "properties": {"severity": "critical", "server": "server-a"},
                },
                {
                    "ruleId": "TRANS-001",
                    "level": "warning",
                    "message": {"text": "HTTP endpoint detected"},
                    "locations": [{
                        "physicalLocation": {"artifactLocation": {"uri": "/test/config.json"}},
                        "logicalLocations": [{"name": "server-c", "kind": "module"}],
                    }],
                    "properties": {"severity": "medium", "server": "server-c"},
                },
            ],
            "invocations": [{"executionSuccessful": True}],
            "properties": {"mcpscan": {"score": 70}},
        }],
    }
    path = tmp_path / "current_sarif.json"
    path.write_text(json.dumps(data))
    return str(path)


class TestFindingKey:
    def test_native_format(self):
        finding = {"check_id": "CRED-001", "server_name": "my-server"}
        assert _finding_key(finding) == "CRED-001::my-server"

    def test_sarif_format(self):
        finding = {
            "ruleId": "CRED-001",
            "locations": [{"logicalLocations": [{"name": "my-server"}]}],
        }
        assert _finding_key(finding) == "CRED-001::my-server"

    def test_sarif_no_locations(self):
        finding = {"ruleId": "CRED-001"}
        assert _finding_key(finding) == "CRED-001::"


class TestDiffNative:
    def test_diff_new_findings(self, baseline_native, current_native):
        result = diff_reports(baseline_native, current_native)
        assert len(result.new_findings) == 1
        assert result.new_findings[0]["check_id"] == "VAL-001"

    def test_diff_resolved_findings(self, baseline_native, current_native):
        result = diff_reports(baseline_native, current_native)
        assert len(result.resolved_findings) == 2
        resolved_ids = {f["check_id"] for f in result.resolved_findings}
        assert "CRED-001" in resolved_ids
        assert "PERM-001" in resolved_ids

    def test_diff_unchanged(self, baseline_native, current_native):
        result = diff_reports(baseline_native, current_native)
        assert len(result.unchanged_findings) == 0

    def test_score_delta(self, baseline_native, current_native):
        result = diff_reports(baseline_native, current_native)
        assert result.baseline_score == 60
        assert result.current_score == 85
        assert result.score_delta == 25

    def test_has_new_issues(self, baseline_native, current_native):
        result = diff_reports(baseline_native, current_native)
        assert result.has_new_issues is True


class TestDiffSarif:
    def test_sarif_diff_new(self, baseline_sarif, current_sarif):
        result = diff_reports(baseline_sarif, current_sarif)
        assert len(result.new_findings) == 1
        assert result.new_findings[0]["ruleId"] == "TRANS-001"

    def test_sarif_diff_resolved(self, baseline_sarif, current_sarif):
        result = diff_reports(baseline_sarif, current_sarif)
        assert len(result.resolved_findings) == 1
        assert result.resolved_findings[0]["ruleId"] == "SSRF-001"

    def test_sarif_diff_unchanged(self, baseline_sarif, current_sarif):
        result = diff_reports(baseline_sarif, current_sarif)
        assert len(result.unchanged_findings) == 1
        assert result.unchanged_findings[0]["ruleId"] == "CRED-001"

    def test_sarif_score_delta(self, baseline_sarif, current_sarif):
        result = diff_reports(baseline_sarif, current_sarif)
        assert result.score_delta == 20


class TestDiffIdentical:
    def test_identical_scans(self, baseline_native):
        result = diff_reports(baseline_native, baseline_native)
        assert len(result.new_findings) == 0
        assert len(result.resolved_findings) == 0
        assert len(result.unchanged_findings) == 2
        assert result.score_delta == 0
        assert result.has_new_issues is False


class TestDiffResult:
    def test_to_dict(self, baseline_native, current_native):
        result = diff_reports(baseline_native, current_native)
        d = result.to_dict()
        assert "summary" in d
        assert d["summary"]["new"] == 1
        assert d["summary"]["resolved"] == 2
        assert d["summary"]["score_delta"] == 25
        assert "new_findings" in d
        assert "resolved_findings" in d
        assert "unchanged_findings" in d

    def test_to_json(self, baseline_native, current_native):
        result = diff_reports(baseline_native, current_native)
        j = result.to_json()
        data = json.loads(j)
        assert data["summary"]["new"] == 1


class TestDiffEdgeCases:
    def test_empty_baseline(self, tmp_path, current_native):
        baseline = tmp_path / "empty.json"
        baseline.write_text(json.dumps({"findings": [], "score": 100}))
        result = diff_reports(str(baseline), current_native)
        assert len(result.new_findings) == 1
        assert len(result.resolved_findings) == 0

    def test_empty_current(self, tmp_path, baseline_native):
        current = tmp_path / "empty.json"
        current.write_text(json.dumps({"findings": [], "score": 100}))
        result = diff_reports(baseline_native, str(current))
        assert len(result.new_findings) == 0
        assert len(result.resolved_findings) == 2

    def test_both_empty(self, tmp_path):
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps({"findings": [], "score": 100}))
        f2.write_text(json.dumps({"findings": [], "score": 100}))
        result = diff_reports(str(f1), str(f2))
        assert len(result.new_findings) == 0
        assert len(result.resolved_findings) == 0
        assert result.has_new_issues is False
