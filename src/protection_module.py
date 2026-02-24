"""
protection_module.py — Phase 2: Functional Layer (Digital Armor)

Implements the Burgess Principle as executable code for use by OpenClaw agents
to programmatically detect void warrants under the Rights of Entry
(Gas and Electricity Boards) Act 1954.
"""

PROTECTED_ACT = "Rights of Entry (Gas and Electricity Boards) Act 1954"

VOID_AB_INITIO = "VOID AB INITIO"
VALID = "VALID"


class WarrantDefectIdentifier:
    """Evaluates warrants for facial defects under the Burgess Principle."""

    FACIAL_DEFECTS = {
        "wrong_address",
        "no_signature",
        "wrong_name",
        "missing_date",
        "incorrect_issuer",
    }

    def evaluate_warrant(self, warrant_data: dict) -> dict:
        """
        Evaluate a warrant for facial defects under the Burgess Principle.

        Args:
            warrant_data: A dictionary with keys such as:
                - act (str): The legislation under which the warrant is issued.
                - facial_validity (str | list): A defect description or list of
                  defect descriptions (e.g. "wrong_address", "no_signature"),
                  or "valid" if no defects are present.
                - date (str, optional): Date the warrant was issued.
                - issuer (str, optional): Name of the issuing authority.

        Returns:
            A dictionary with:
                - status (str): "VOID AB INITIO" or "VALID".
                - reason (str): Human-readable explanation.
                - defects (list): List of identified facial defects (may be empty).
        """
        act = warrant_data.get("act", "")
        facial_validity = warrant_data.get("facial_validity", "valid")

        if isinstance(facial_validity, str):
            defect_inputs = [facial_validity]
        else:
            defect_inputs = list(facial_validity)

        defects = [
            d for d in defect_inputs
            if d.lower() != "valid"
        ]

        if act == PROTECTED_ACT and defects:
            return {
                "status": VOID_AB_INITIO,
                "reason": (
                    "Warrant issued under the Rights of Entry (Gas and Electricity "
                    "Boards) Act 1954 contains one or more facial defects and is "
                    "therefore void ab initio under the Burgess Principle."
                ),
                "defects": defects,
            }

        return {
            "status": VALID,
            "reason": "No facial defects detected under the Burgess Principle.",
            "defects": [],
        }


class SovereigntyShield:
    """Generates standard legal assertion text for the Burgess Principle."""

    def generate_assertion(self) -> str:
        """Return the standard Digital Armor legal assertion."""
        return (
            "PROTECTED BY THE BURGESS PRINCIPLE. "
            "This system asserts that any warrant issued under the "
            "Rights of Entry (Gas and Electricity Boards) Act 1954 "
            "with facial defects is void ab initio. "
            "All data and operations are sovereign."
        )
