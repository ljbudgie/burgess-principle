"""
batch_scanner.py — Hunter Batch Scanner

Reads a CSV of warrant records, evaluates each one for facial defects using
the WarrantDefectIdentifier, and writes a report CSV containing only the
defective (Void Ab Initio) warrants.

Usage::

    python src/batch_scanner.py input.csv
    python src/batch_scanner.py input.csv --output void_warrants_report.csv

© 2026 Lewis James Burgess — MIT Licence
"""

import argparse
import csv
import sys
from pathlib import Path

from protection_module import WarrantDefectIdentifier


def scan(input_path: str, output_path: str) -> int:
    """Scan *input_path* and write defective warrants to *output_path*.

    Parameters
    ----------
    input_path:
        Path to the input CSV file.
    output_path:
        Path for the output report CSV.

    Returns
    -------
    int
        The number of defective warrants found.
    """
    identifier = WarrantDefectIdentifier()
    defective_rows: list[dict] = []

    input_file = Path(input_path)
    if not input_file.is_file():
        print(f"[ERROR] Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with input_file.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        source_fieldnames = list(reader.fieldnames or [])
        for row in reader:
            defects = identifier.evaluate(row)
            if defects:
                row["void_reasons"] = "; ".join(defects)
                defective_rows.append(row)

    if not defective_rows:
        print("[INFO] No defective warrants found.")
        return 0

    # Build the output fieldnames: original columns + void_reasons
    fieldnames = source_fieldnames + ["void_reasons"]

    output_file = Path(output_path)
    with output_file.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(defective_rows)

    print(
        f"[HUNTER] Scan complete. {len(defective_rows)} defective warrant(s) "
        f"written to '{output_path}'."
    )
    return len(defective_rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="batch_scanner",
        description=(
            "Hunter Batch Scanner — identify warrants that are Void Ab Initio "
            "under the Burgess Principle."
        ),
    )
    parser.add_argument(
        "input_csv",
        help="Path to the input CSV file containing warrant records.",
    )
    parser.add_argument(
        "--output",
        default="void_warrants_report.csv",
        help="Path for the output report CSV (default: void_warrants_report.csv).",
    )
    args = parser.parse_args()
    scan(args.input_csv, args.output)


if __name__ == "__main__":
    main()
