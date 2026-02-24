"""
Batch Scanner — The Burgess Principle "Hunter" System
Scans warrant CSV data for defects under the
Rights of Entry (Gas and Electricity Boards) Act 1954
and outputs a void-warrant "Kill List" report.
"""

import csv
import sys
import os
from datetime import datetime, timezone

REQUIRED_FIELDS = [
    "warrant_id",
    "issuing_authority",
    "issue_date",
    "property_address",
    "utility_type",
    "statutory_basis",
    "officer_name",
    "signature_present",
    "date_on_warrant",
]

VALID_STATUTORY_BASIS = "Rights of Entry (Gas and Electricity Boards) Act 1954"
VALID_COURTS = {"Magistrates Court"}

OUTPUT_FILE = "void_warrants_report.csv"


def check_defects(row):
    """Return a list of defect descriptions for a single warrant row."""
    defects = []

    # Defect 1: Missing or blank signature
    if row.get("signature_present", "").strip().lower() != "yes":
        defects.append("Missing or invalid signature")

    # Defect 2: Date absent from warrant face
    if not row.get("date_on_warrant", "").strip():
        defects.append("Date absent from warrant face")

    # Defect 3: Wrong issuing court (must be Magistrates Court under the 1954 Act)
    court = row.get("issuing_authority", "").strip()
    if court not in VALID_COURTS:
        defects.append(f"Invalid issuing authority: '{court}' (must be Magistrates Court)")

    # Defect 4: Incorrect or missing statutory basis
    basis = row.get("statutory_basis", "").strip()
    if basis != VALID_STATUTORY_BASIS:
        defects.append(f"Incorrect statutory basis: '{basis}'")

    # Defect 5: Missing mandatory fields
    for field in ["warrant_id", "property_address", "officer_name"]:
        if not row.get(field, "").strip():
            defects.append(f"Missing mandatory field: '{field}'")

    return defects


def scan(input_path):
    """Scan warrants CSV and return list of void warrant records."""
    void_warrants = []

    with open(input_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            defects = check_defects(row)
            if defects:
                void_warrants.append(
                    {
                        "warrant_id": row.get("warrant_id", "").strip(),
                        "property_address": row.get("property_address", "").strip(),
                        "issue_date": row.get("issue_date", "").strip(),
                        "issuing_authority": row.get("issuing_authority", "").strip(),
                        "utility_type": row.get("utility_type", "").strip(),
                        "officer_name": row.get("officer_name", "").strip(),
                        "defects": "; ".join(defects),
                        "status": "VOID AB INITIO",
                    }
                )

    return void_warrants


def write_report(void_warrants, output_path):
    """Write void warrants to CSV report."""
    fieldnames = [
        "warrant_id",
        "property_address",
        "issue_date",
        "issuing_authority",
        "utility_type",
        "officer_name",
        "defects",
        "status",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(void_warrants)


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_scanner.py <input_warrants.csv>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print(f"Error: input file not found: {input_path}")
        sys.exit(1)

    print(f"[{datetime.now(timezone.utc).isoformat()}] Hunter Scanner starting...")
    print(f"Input : {input_path}")

    void_warrants = scan(input_path)

    write_report(void_warrants, OUTPUT_FILE)

    print(f"Output: {OUTPUT_FILE}")
    print(f"Total void warrants identified: {len(void_warrants)}")
    if void_warrants:
        print("\n--- Kill List ---")
        for w in void_warrants:
            print(f"  {w['warrant_id']} | {w['property_address']} | {w['defects']}")
    print(f"[{datetime.now(timezone.utc).isoformat()}] Scan complete.")


if __name__ == "__main__":
    main()
