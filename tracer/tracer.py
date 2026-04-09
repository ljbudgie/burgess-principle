# 🔍 TRACER PROTOCOL: DEFECT SCHEMA LIBRARY
#
# This library defines the specific "Facial Defects" that render a corporate
# warrant or contract Void Ab Initio under the Burgess Principle.  The tracer
# module uses these definitions to hunt for evidence of administrative taint.

"""TRACER — defect schema definitions for the Burgess Principle."""

from __future__ import annotations

from typing import TypedDict


class Defect(TypedDict):
    """Schema for a single scrutiny defect."""

    id: str
    title: str
    description: str
    axiom: str


# Each defect is a dict with an id, title, description, and axiom.
DEFECT_SCHEMA: list[Defect] = [
    {
        "id": "DEFECT_01",
        "title": "Bulk Approval Without Scrutiny",
        "description": (
            "Warrants processed in batches without individual judicial review."
        ),
        "axiom": (
            "Violates 'The Judicial Mind.' If a judge did not scrutinize the "
            "specific facts of the individual case, the resulting data is a 0 (NULL)."
        ),
    },
    {
        "id": "DEFECT_02",
        "title": "Rubber-Stamping",
        "description": (
            "Reliance on supplier affidavits without independent verification."
        ),
        "axiom": (
            "The court acts as a processing center rather than an independent "
            "judiciary, transferring corporate assumptions directly into legal mandates."
        ),
    },
    {
        "id": "DEFECT_03",
        "title": "Procedural Lies / Errors",
        "description": (
            "False safety claims (e.g., claiming a gas leak to force entry) or "
            "incomplete addresses used to expedite the warrant process."
        ),
        "axiom": (
            "Fraud vitiates all. Any procedural lie introduced at the source "
            "renders all downstream actions invalid."
        ),
    },
    {
        "id": "DEFECT_04",
        "title": "Downstream Taint Propagation",
        "description": (
            "Defects from the above categories cascading into credit agencies, "
            "billing systems, or high court enforcement records."
        ),
        "axiom": "A corrupted source (0) can only produce corrupted outputs.",
    },
]


def get_defect(defect_id: str) -> Defect | None:
    """Return the defect definition matching *defect_id*, or ``None``."""
    for defect in DEFECT_SCHEMA:
        if defect["id"] == defect_id:
            return defect
    return None


def list_defects() -> list[str]:
    """Return a list of all known defect IDs."""
    return [d["id"] for d in DEFECT_SCHEMA]
