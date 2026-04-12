# 🔍 TRACER PROTOCOL: DEFECT SCHEMA LIBRARY
#
# This library defines the specific "Facial Defects" that render a corporate
# warrant or contract Void Ab Initio under the Burgess Principle.  The tracer
# module uses these definitions to hunt for evidence of administrative taint.

"""TRACER — defect schema definitions for the Burgess Principle."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime, timezone
from typing import TypedDict


class Defect(TypedDict):
    """Schema for a single scrutiny defect."""

    id: str
    title: str
    description: str
    axiom: str


class TraceFinding(TypedDict):
    """Audit-ready finding derived from a known scrutiny defect."""

    defect_id: str
    title: str
    description: str
    axiom: str
    evidence: str
    notes: str


class TraceReport(TypedDict):
    """Structured trace output that can feed later Burgess review steps."""

    generated_at: str
    reasoning: str
    defect_ids: list[str]
    findings: list[TraceFinding]


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


def build_trace_finding(
    defect_id: str,
    *,
    evidence: str = "",
    notes: str = "",
) -> TraceFinding | None:
    """Return an audit-ready finding for *defect_id*, or ``None``."""
    defect = get_defect(defect_id)
    if defect is None:
        return None

    return {
        "defect_id": defect["id"],
        "title": defect["title"],
        "description": defect["description"],
        "axiom": defect["axiom"],
        "evidence": evidence,
        "notes": notes,
    }


def build_trace_report(
    defect_ids: Iterable[str] | str,
    *,
    reasoning: str = "",
    evidence_by_id: Mapping[str, str] | None = None,
    notes_by_id: Mapping[str, str] | None = None,
    generated_at: str | None = None,
) -> TraceReport:
    """Build a structured report for the supplied defect IDs."""
    if isinstance(defect_ids, str):
        normalized_ids = [defect_ids]
    else:
        normalized_ids = list(defect_ids)

    evidence_lookup = evidence_by_id or {}
    notes_lookup = notes_by_id or {}
    findings: list[TraceFinding] = []

    for defect_id in normalized_ids:
        finding = build_trace_finding(
            defect_id,
            evidence=evidence_lookup.get(defect_id, ""),
            notes=notes_lookup.get(defect_id, ""),
        )
        if finding is None:
            raise ValueError(f"Unknown defect ID: {defect_id}")
        findings.append(finding)

    timestamp = generated_at or datetime.now(timezone.utc).isoformat()

    return {
        "generated_at": timestamp,
        "reasoning": reasoning,
        "defect_ids": [finding["defect_id"] for finding in findings],
        "findings": findings,
    }
