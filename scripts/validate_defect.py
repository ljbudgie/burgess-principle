import json
import sys

REQUIRED_FIELDS = [
    "defect_id",
    "reporter",
    "target_system",
    "severity",
    "description",
    "date_logged",
]


def validate_defect(file_path):
    """Load a JSON defect file and verify all required fields are present.

    Prints a success message to stdout when valid.
    Prints an error message and exits with code 1 on missing fields,
    malformed JSON, or a missing file.
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Malformed JSON in {file_path}: {e}")
        sys.exit(1)

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        print(f"ERROR: Missing required fields in {file_path}: {', '.join(missing)}")
        sys.exit(1)

    print(f"SUCCESS: {file_path} is a valid OpenClaw defect report.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_defect.py <path_to_defect_json>")
        sys.exit(1)
    validate_defect(sys.argv[1])
