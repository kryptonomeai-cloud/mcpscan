"""SARIF JSON report generator for MCPScan (GitHub Code Scanning compatible)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from .. import __version__

if TYPE_CHECKING:
    from ..models import ScanReport

_SEVERITY_TO_SARIF_LEVEL = {
    "critical": "error",
    "high": "error",
    "medium": "warning",
    "low": "note",
    "info": "note",
}

_SEVERITY_TO_SARIF_RANK = {
    "critical": 9.5,
    "high": 8.0,
    "medium": 5.0,
    "low": 3.0,
    "info": 1.0,
}


def generate_sarif_report(report: "ScanReport") -> str:
    """Generate a SARIF 2.1.0 JSON report string.

    Follows the SARIF spec used by GitHub Code Scanning:
    https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning
    """
    # Collect unique rules
    rules_map: dict[str, dict] = {}
    for f in report.findings:
        if f.check_id not in rules_map:
            rules_map[f.check_id] = {
                "id": f.check_id,
                "shortDescription": {"text": f.title},
                "fullDescription": {"text": f.description},
                "defaultConfiguration": {
                    "level": _SEVERITY_TO_SARIF_LEVEL.get(f.severity.value, "note"),
                },
                "properties": {
                    "security-severity": str(_SEVERITY_TO_SARIF_RANK.get(f.severity.value, 1.0)),
                    "tags": ["security", "mcp"],
                },
            }
            if f.recommendation:
                rules_map[f.check_id]["help"] = {
                    "text": f.recommendation,
                    "markdown": f"**Recommendation:** {f.recommendation}",
                }

    # Build results
    results = []
    for f in report.findings:
        result = {
            "ruleId": f.check_id,
            "level": _SEVERITY_TO_SARIF_LEVEL.get(f.severity.value, "note"),
            "message": {
                "text": f"{f.title}: {f.description}",
            },
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": report.config_path,
                            "uriBaseId": "%SRCROOT%",
                        },
                    },
                    "logicalLocations": [
                        {
                            "name": f.server_name,
                            "kind": "module",
                        }
                    ],
                }
            ],
            "properties": {
                "severity": f.severity.value,
                "server": f.server_name,
            },
        }
        if f.evidence:
            result["properties"]["evidence"] = f.evidence
        results.append(result)

    sarif = {
        "$schema": "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "MCPScan",
                        "version": __version__,
                        "informationUri": "https://github.com/kryptonomeai-cloud/mcpscan",
                        "rules": list(rules_map.values()),
                    }
                },
                "results": results,
                "invocations": [
                    {
                        "executionSuccessful": True,
                        "endTimeUtc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    }
                ],
                "properties": {
                    "mcpscan": {
                        "configPath": report.config_path,
                        "configFormat": report.config_format,
                        "serversScanned": len(report.servers),
                        "score": report.score,
                        "scoreLabel": report.score_label,
                    }
                },
            }
        ],
    }

    return json.dumps(sarif, indent=2)
