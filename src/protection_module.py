"""
protection_module.py — Warrant Defect Identifier

Implements the Burgess Principle logic tree for identifying facial defects
in warrants issued under the Rights of Entry (Gas and Electricity Boards)
Act 1954.  A warrant that fails any check is Void Ab Initio.

© 2026 Lewis James Burgess — MIT Licence
"""

REQUIRED_ACT = "Rights of Entry (Gas and Electricity Boards) Act 1954"

# Columns that must be present and non-empty for a warrant to be facially valid
REQUIRED_FIELDS = ["warrant_id", "act", "issuing_court", "issue_date", "subject_address"]


class WarrantDefectIdentifier:
    """Evaluate a single warrant record for facial defects.

    Usage::

        identifier = WarrantDefectIdentifier()
        defects = identifier.evaluate(row)   # row is a dict
        if defects:
            print("Void Ab Initio:", defects)
    """

    def evaluate(self, row: dict) -> list[str]:
        """Return a list of defect reasons for *row*, or an empty list if valid.

        Parameters
        ----------
        row:
            A dictionary representing one warrant, typically read from a CSV row.

        Returns
        -------
        list[str]
            Human-readable defect descriptions.  An empty list means no defects
            were found and the warrant appears facially valid.
        """
        defects: list[str] = []

        # 1. Missing mandatory fields
        for field in REQUIRED_FIELDS:
            if not row.get(field, "").strip():
                defects.append(f"Missing mandatory field: '{field}'")

        # 2. Wrong or absent enabling Act
        act = row.get("act", "").strip()
        if act and act != REQUIRED_ACT:
            defects.append(
                f"Incorrect enabling Act cited ('{act}'). "
                f"Must be '{REQUIRED_ACT}'."
            )

        # 3. Explicit facial_validity flag supplied in data
        facial_validity = row.get("facial_validity", "").strip().lower()
        if facial_validity in ("false", "no", "0", "invalid", "defective"):
            defects.append("Warrant flagged as facially invalid in source data.")

        # 4. Issuing authority blank (belt-and-braces beyond field check above)
        issuing_court = row.get("issuing_court", "").strip()
        if issuing_court and issuing_court.lower() in ("none", "unknown", "n/a"):
            defects.append("Issuing court is unknown or unspecified.")

        # 5. Protected-characteristics flag present but no reasonable adjustment recorded
        protected = row.get("protected_characteristics", "").strip().lower()
        adjustment = row.get("reasonable_adjustment", "").strip().lower()
        if protected in ("yes", "true", "1") and adjustment in ("", "none", "no", "n/a"):
            defects.append(
                "Protected characteristics recorded but no reasonable adjustment noted "
                "(potential Equality Act 2010 / CRPD breach)."
            )

        return defects
