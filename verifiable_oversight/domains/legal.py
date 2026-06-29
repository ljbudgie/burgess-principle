"""
LegalDomain — oversight assessment for legal proceedings and enforcement decisions.

This domain captures the specific requirements for decisions made in legal
or quasi-legal contexts: court orders, enforcement actions, ombudsman findings,
regulator decisions, and formal complaint responses.

The legal domain adds:
- Statutory / procedural basis for the decision
- Case reference tracking
- Whether the burden of proof has been shifted (e.g. s.136 EA 2010)
- Whether the decision is susceptible to judicial review / appeal
- Applicable case law anchors

A decision that cannot produce its statutory basis on request is AMBIGUOUS
at minimum; a decision that proceeds without one is NULL.
"""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseDomain


class LegalDomain(BaseDomain):
    """
    Domain for legal proceedings, enforcement decisions, and formal complaints.

    Additional domain_kwargs
    -----------------------
    statutory_basis : str, optional
        The statutory provision(s) under which the decision was made.
        Example: 'EA 2010 s.149 PSED', 'Council Tax (Administration and
        Enforcement) Regulations 1992'.
    case_reference : str, optional
        The case/complaint/reference number.
    burden_shifted : bool, optional
        Whether the evidential burden has been formally shifted to the
        respondent (e.g. via s.136 EA 2010 letter).
    decision_type : str, optional
        Type of decision: 'enforcement', 'complaint_response', 'ombudsman',
        'court_order', 'regulator', 'tribunal'.
    case_law_anchors : list[str], optional
        Case law relied upon in the decision or challenge.
        Example: ['ZH (Tanzania) [2011] UKSC 4', 'FirstGroup v Paulley [2017] UKSC 4']
    appeal_route : str, optional
        Available appeal or review route.
    bulk_process : bool, optional
        Whether the decision was made as part of a bulk process (e.g.
        bulk liability orders). Bulk processing creates a strong presumption
        of NULL — individual consideration is structurally impossible at scale.
    """

    @property
    def name(self) -> str:
        return "legal"

    @property
    def guidance(self) -> str:
        return (
            "Legal domain: decisions in legal contexts carry heightened accountability "
            "requirements. A named individual must be identified — not just a team, "
            "department, or automated system.\n\n"
            "Bulk processes (bulk liability orders, templated enforcement letters, "
            "automated court applications) create a structural presumption of NULL: "
            "individual consideration is impossible when 2,857 orders are granted in "
            "a single session. The institution must demonstrate the specific exception.\n\n"
            "Where the evidential burden has been shifted (s.136 EA 2010, or equivalent), "
            "the institution must produce a named individual and demonstrate specific "
            "consideration. Silence or a generic response following a burden-shift letter "
            "is a confirmed NULL.\n\n"
            "Case law anchors — Bracking, Nzolameso, Ahmed, Guntrip — are signposts "
            "to the applicable standard. An institution that receives a letter citing "
            "these authorities and responds without engaging them has not applied "
            "a named mind to the specific facts."
        )

    def validate_domain_metadata(self, metadata: dict[str, Any]) -> list[str]:
        issues = []

        if metadata.get("bulk_process"):
            issues.append(
                "Decision was part of a bulk process — strong presumption of NULL. "
                "Individual consideration must be demonstrated explicitly to rebut."
            )

        burden_shifted = metadata.get("burden_shifted", False)
        named_person = metadata.get("_named_person_present", None)
        if burden_shifted and named_person is False:
            issues.append(
                "Evidential burden has been shifted (s.136 EA 2010 or equivalent) "
                "but no named individual has been provided — confirmed NULL."
            )

        return issues

    def _build_domain_metadata(
        self,
        statutory_basis: Optional[str] = None,
        case_reference: Optional[str] = None,
        burden_shifted: bool = False,
        decision_type: Optional[str] = None,
        case_law_anchors: Optional[list[str]] = None,
        appeal_route: Optional[str] = None,
        bulk_process: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "domain": self.name,
            "burden_shifted": burden_shifted,
            "bulk_process": bulk_process,
        }
        if statutory_basis:
            meta["statutory_basis"] = statutory_basis
        if case_reference:
            meta["case_reference"] = case_reference
        if decision_type:
            meta["decision_type"] = decision_type
        if case_law_anchors:
            meta["case_law_anchors"] = case_law_anchors
        if appeal_route:
            meta["appeal_route"] = appeal_route
        meta.update(kwargs)
        return meta
