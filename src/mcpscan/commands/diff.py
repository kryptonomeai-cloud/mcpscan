"""Diff command — compare two MCPScan JSON/SARIF scan results."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DiffResult:
    """Result of comparing two scan reports."""
    new_findings: list[dict]
    resolved_findings: list[dict]
    unchanged_findings: list[dict]
    baseline_score: int
    current_score: int

    @property
    def score_delta(self) -> int:
        return self.current_score - self.baseline_score

    @property
    def has_new_issues(self) -> bool:
        return len(self.new_findings) > 0

    def to_dict(self) -> dict:
        return {
            "summary": {
                "new": len(self.new_findings),
                "resolved": len(self.resolved_findings),
                "unchanged": len(self.unchanged_findings),
                "baseline_score": self.baseline_score,
                "current_score": self.current_score,
                "score_delta": self.score_delta,
            },
            "new_findings": self.new_findings,
            "resolved_findings": self.resolved_findings,
            "unchanged_findings": self.unchanged_findings,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def _finding_key(finding: dict) -> str:
    """Generate a unique key for a finding to enable comparison."""
    # For SARIF format
    if "ruleId" in finding:
        server = ""
        locations = finding.get("locations", [])
        if locations:
            logical = locations[0].get("logicalLocations", [])
            if logical:
                server = logical[0].get("name", "")
        return f"{finding['ruleId']}::{server}"
    # For mcpscan native JSON format
    return f"{finding.get('check_id', '')}::{finding.get('server_name', '')}"


def _extract_findings_and_score(data: dict) -> tuple[list[dict], int]:
    """Extract findings list and score from either SARIF or native JSON format."""
    # SARIF format
    if "$schema" in data and "runs" in data:
        runs = data.get("runs", [])
        if not runs:
            return [], 100
        run = runs[0]
        results = run.get("results", [])
        score = run.get("properties", {}).get("mcpscan", {}).get("score", 100)
        return results, score

    # Native mcpscan JSON format
    findings = data.get("findings", [])
    score = data.get("score", 100)
    return findings, score


def diff_reports(baseline_path: str, current_path: str) -> DiffResult:
    """Compare two scan result files and return the diff.

    Supports both mcpscan native JSON and SARIF formats.
    """
    baseline_data = json.loads(Path(baseline_path).read_text())
    current_data = json.loads(Path(current_path).read_text())

    baseline_findings, baseline_score = _extract_findings_and_score(baseline_data)
    current_findings, current_score = _extract_findings_and_score(current_data)

    baseline_keys = {_finding_key(f): f for f in baseline_findings}
    current_keys = {_finding_key(f): f for f in current_findings}

    baseline_set = set(baseline_keys.keys())
    current_set = set(current_keys.keys())

    new = [current_keys[k] for k in sorted(current_set - baseline_set)]
    resolved = [baseline_keys[k] for k in sorted(baseline_set - current_set)]
    unchanged = [current_keys[k] for k in sorted(current_set & baseline_set)]

    return DiffResult(
        new_findings=new,
        resolved_findings=resolved,
        unchanged_findings=unchanged,
        baseline_score=baseline_score,
        current_score=current_score,
    )
