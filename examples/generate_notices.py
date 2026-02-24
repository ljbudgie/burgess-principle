"""
Example: Generate void-warrant notices using the Enforcer module.

Usage:
    python examples/generate_notices.py
    python examples/generate_notices.py path/to/void_warrants_report.csv
"""

import os
import sys

# Allow running from the repo root without installing the package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.enforcer_module import LegalNoticeGenerator

DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "warrants_sample.csv")


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
    output_dir = "notices"

    print(f"Loading warrants from: {csv_path}")
    generator = LegalNoticeGenerator(output_dir=output_dir)
    paths = generator.generate_from_csv(csv_path)

    print(f"Generated {len(paths)} notice(s):")
    for path in paths:
        print(f"  {path}")


if __name__ == "__main__":
    main()
