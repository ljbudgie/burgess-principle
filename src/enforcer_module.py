"""
Enforcer Module — Burgess Principle Automated Legal Defence Suite
Generates "Notice of Void Ab Initio" letters for defective warrants.
"""

import csv
import os

NOTICE_TEMPLATE = (
    "NOTICE OF VOID WARRANT AB INITIO\n\n"
    "To {court_issuer}.\n\n"
    "Take notice that Warrant {warrant_id} issued on {date} is void ab initio "
    "due to {defect}. Under the Burgess Principle, all entry is trespass. "
    "Immediate remedy required."
)


class LegalNoticeGenerator:
    """Generates formal legal notices for defective warrants."""

    def __init__(self, output_dir="notices"):
        self.output_dir = output_dir

    def generate_from_list(self, warrants):
        """Generate notices from a list of warrant dicts.

        Each dict must contain: warrant_id, date, defect, court_issuer.
        Returns a list of paths to the generated notice files.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        paths = []
        for warrant in warrants:
            path = self._write_notice(warrant)
            paths.append(path)
        return paths

    def generate_from_csv(self, csv_path):
        """Generate notices from a CSV file.

        The CSV must have columns: warrant_id, date, defect, court_issuer.
        Returns a list of paths to the generated notice files.
        """
        try:
            with open(csv_path, newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                warrants = list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"Warrant CSV not found: {csv_path}")
        except PermissionError:
            raise PermissionError(f"Permission denied reading CSV: {csv_path}")
        except csv.Error as exc:
            raise ValueError(f"Malformed CSV file '{csv_path}': {exc}") from exc
        return self.generate_from_list(warrants)

    def _write_notice(self, warrant):
        required_fields = ("warrant_id", "date", "defect", "court_issuer")
        missing = [f for f in required_fields if not warrant.get(f)]
        if missing:
            raise ValueError(
                f"Warrant entry is missing required field(s): {', '.join(missing)}. "
                f"Entry: {warrant}"
            )
        notice_text = NOTICE_TEMPLATE.format(
            court_issuer=warrant["court_issuer"],
            warrant_id=warrant["warrant_id"],
            date=warrant["date"],
            defect=warrant["defect"],
        )
        filename = f"Notice_Warrant_{warrant['warrant_id']}.txt"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(notice_text)
        return filepath
