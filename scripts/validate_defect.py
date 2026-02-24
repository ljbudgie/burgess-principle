#!/usr/bin/env python3
"""Validate an OpenClaw defect report JSON file against the required schema fields."""

import json
import sys

REQUIRED_FIELDS = [
    "defect_id",
    "reporter",
    "target_system",
    "description",
    "severity",
    "date_logged",
]

VALID_SEVERITIES = {"Critical", "High", "Medium", "Low", "Void Ab Initio"}


def validate(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {filepath}: {e}")
        sys.exit(1)

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        print(f"ERROR: Missing required fields: {', '.join(missing)}")
        sys.exit(1)

    severity = data.get("severity")
    if severity is not None and severity not in VALID_SEVERITIES:
        print(
            f"ERROR: Invalid severity '{severity}'. "
            f"Must be one of: {', '.join(sorted(VALID_SEVERITIES))}"
        )
        sys.exit(1)

    print(f"OK: {filepath} is a valid OpenClaw defect report.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_defect.py <path-to-defect-json>")
        sys.exit(1)
    validate(sys.argv[1])
