"""Tests for MCPScan checks."""

import json
import pytest
from pathlib import Path

from mcpscan.parsers import parse_config
from mcpscan.checks import run_all_checks
from mcpscan.models import Severity, ScanReport

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_mcporter_config():
    """Test parsing mcporter/Claude Desktop format."""
    fmt, servers = parse_config(FIXTURES.parent.parent.parent.parent / "config" / "mcporter.json")
    assert fmt == "mcporter/claude-desktop"
    assert len(servers) >= 1


def test_parse_vulnerable_1():
    """Test parsing vulnerable fixture 1."""
    fmt, servers = parse_config(FIXTURES / "vulnerable_1.json")
    assert fmt == "mcporter/claude-desktop"
    # Note: duplicate key "shell-server" in JSON means only last one survives
    assert len(servers) >= 4


def test_credentials_detection():
    """Test that hardcoded credentials are detected."""
    _, servers = parse_config(FIXTURES / "vulnerable_1.json")
    findings = run_all_checks(servers)
    cred_findings = [f for f in findings if f.check_id.startswith("CRED")]
    assert len(cred_findings) > 0, "Should detect hardcoded credentials"

    # Should find API keys, tokens, and passwords
    titles = " ".join(f.title for f in cred_findings)
    assert any(sev in [Severity.CRITICAL, Severity.HIGH]
               for f in cred_findings for sev in [f.severity])


def test_shell_exec_detection():
    """Test that shell execution is flagged."""
    _, servers = parse_config(FIXTURES / "vulnerable_1.json")
    findings = run_all_checks(servers)
    perm_findings = [f for f in findings if f.check_id.startswith("PERM")]
    assert len(perm_findings) > 0, "Should detect shell execution risks"


def test_ssrf_detection():
    """Test SSRF detection with cloud metadata endpoint."""
    _, servers = parse_config(FIXTURES / "vulnerable_1.json")
    findings = run_all_checks(servers)
    ssrf_findings = [f for f in findings if f.check_id.startswith("SSRF")]
    assert len(ssrf_findings) > 0, "Should detect SSRF risks"

    # Cloud metadata should be critical
    critical_ssrf = [f for f in ssrf_findings if f.severity == Severity.CRITICAL]
    assert len(critical_ssrf) > 0, "Cloud metadata access should be critical"


def test_prompt_injection_detection():
    """Test prompt injection detection."""
    _, servers = parse_config(FIXTURES / "vulnerable_2.json")
    findings = run_all_checks(servers)
    desc_findings = [f for f in findings if f.check_id.startswith("DESC")]
    assert len(desc_findings) > 0, "Should detect prompt injection patterns"


def test_validation_npx_y():
    """Test npx -y auto-install detection."""
    _, servers = parse_config(FIXTURES / "vulnerable_1.json")
    findings = run_all_checks(servers)
    val_findings = [f for f in findings if f.check_id == "VAL-001"]
    assert len(val_findings) > 0, "Should detect npx -y usage"


def test_docker_detection():
    """Test Docker privilege detection."""
    _, servers = parse_config(FIXTURES / "vulnerable_2.json")
    findings = run_all_checks(servers)
    docker_findings = [f for f in findings if "docker" in f.server_name.lower() or "container" in f.title.lower()]
    assert len(docker_findings) > 0, "Should detect Docker risks"


def test_filesystem_overlap():
    """Test filesystem tool overlap detection."""
    _, servers = parse_config(FIXTURES / "vulnerable_2.json")
    findings = run_all_checks(servers)
    shadow_findings = [f for f in findings if f.check_id.startswith("SHADOW")]
    assert len(shadow_findings) > 0, "Should detect overlapping filesystem servers"


def test_score_computation():
    """Test that score is computed correctly."""
    _, servers = parse_config(FIXTURES / "vulnerable_1.json")
    findings = run_all_checks(servers)
    report = ScanReport(
        config_path="test", config_format="test",
        servers=servers, findings=findings,
    )
    score = report.compute_score()
    assert 0 <= score <= 100
    assert score < 50, "Highly vulnerable config should score poorly"


def test_clean_config():
    """Test that a clean config gets a good score."""
    from mcpscan.models import ServerConfig
    clean = ServerConfig(name="clean-server", command="mcp-server", transport="stdio")
    findings = run_all_checks([clean])
    report = ScanReport(
        config_path="test", config_format="test",
        servers=[clean], findings=findings,
    )
    report.compute_score()
    assert report.score >= 90, f"Clean config should score well, got {report.score}"


def test_json_output():
    """Test JSON report generation."""
    _, servers = parse_config(FIXTURES / "vulnerable_1.json")
    findings = run_all_checks(servers)
    report = ScanReport(
        config_path="test.json", config_format="mcporter",
        servers=servers, findings=findings,
    )
    report.compute_score()
    data = json.loads(report.to_json())
    assert "findings" in data
    assert "score" in data
    assert isinstance(data["findings"], list)


def test_markdown_output():
    """Test Markdown report generation."""
    _, servers = parse_config(FIXTURES / "vulnerable_1.json")
    findings = run_all_checks(servers)
    report = ScanReport(
        config_path="test.json", config_format="mcporter",
        servers=servers, findings=findings,
    )
    report.compute_score()
    md = report.to_markdown()
    assert "# MCPScan Report" in md
    assert "Score:" in md
