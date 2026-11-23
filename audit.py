#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def fail(errors, message):
    errors.append(message)


def main():
    errors = []
    required = {
        "id", "category", "app", "description", "app_description", "auth",
        "access", "access_detail", "surface", "mcp", "verdict", "blocker",
        "evidence", "auth_evidence", "access_evidence", "api_evidence",
        "confidence", "last_checked",
    }

    with (ROOT / "research.json").open(encoding="utf-8") as f:
        rows = json.load(f)
    if len(rows) != 100:
        fail(errors, f"Expected 100 rows, found {len(rows)}")
    if len({r["app"] for r in rows}) != 100:
        fail(errors, "Duplicate app names found")

    for row in rows:
        missing = required - row.keys()
        if missing:
            fail(errors, f"{row.get('app', row.get('id'))}: missing {sorted(missing)}")
        if not str(row.get("evidence", "")).startswith("http"):
            fail(errors, f"{row.get('app')}: evidence URL missing")
        if not str(row.get("last_checked", "")).startswith("2026-"):
            fail(errors, f"{row.get('app')}: last_checked missing")

    with (ROOT / "verification.csv").open(newline="", encoding="utf-8") as f:
        checks = list(csv.DictReader(f))
    if len(checks) != 30:
        fail(errors, f"Expected 30 verification rows, found {len(checks)}")
    hits = sum(row["first_pass"] == "Hit" for row in checks)
    misses = sum(row["first_pass"] == "Miss" for row in checks)
    if hits + misses != len(checks):
        fail(errors, "Verification first_pass labels are not Hit/Miss")

    with (ROOT / "agent_run.json").open(encoding="utf-8") as f:
        agent = json.load(f)
    if agent.get("status") not in {"skipped_no_api_key", "sdk_initialized", "sdk_initialization_failed", "sdk_unavailable"}:
        fail(errors, "Unexpected agent_run status")

    report = {
        "status": "passed" if not errors else "failed",
        "app_rows": len(rows),
        "unique_apps": len({r["app"] for r in rows}),
        "verification_rows": len(checks),
        "first_pass_hits": hits,
        "first_pass_misses": misses,
        "agent_status": agent.get("status"),
        "errors": errors,
    }
    (ROOT / "audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
