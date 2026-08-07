"""
BankingDomain — oversight assessment for banking and financial-services decisions.

Phase 4D. Financial-services decisions carry two distinct accountability
hazards that this domain makes explicit:

1. **Solely automated credit / account decisions.** A decision to refuse credit,
   close an account, or freeze funds that is made with no meaningful human
   involvement engages UK GDPR Art 22 / DUAA 2025 s.80. On the binary test such
   a decision is NULL unless a named human reviewed the specific facts before the
   decision took effect — an appeals process *after* the automated refusal is
   involvement, not review that could have changed the outcome.

2. **FCA DISP complaint-handling deadlines.** A firm must issue a final response
   within the DISP window (8 weeks). A complaint that passes that deadline without
   a substantive, named response is both a DISP breach and, typically, NULL.

This domain records the automated-decision facts and the DISP deadline position
alongside the binary test. It pairs naturally with
:class:`verifiable_oversight.core.deadlines.DeadlineEngine` (profile
``'fca_disp_final_response'``) to compute the deadline itself.
"""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseDomain


# Decision types where a solely-automated outcome is especially serious.
_HIGH_STAKES_AUTOMATED = {
    "credit_refusal",
    "account_closure",
    "funds_freeze",
    "loan_decision",
    "overdraft_withdrawal",
    "mortgage_decision",
    "mortgage_forbearance",
    "insurance_underwriting",
    "insurance_claim",
    "insurance_non_renewal",
}


class BankingDomain(BaseDomain):
    """
    Domain for banking / financial-services decisions — Phase 4D.

    Additional domain_kwargs
    -----------------------
    decision_type : str, optional
        Type of decision, e.g. 'credit_refusal', 'account_closure',
        'funds_freeze', 'loan_decision', 'mortgage_decision',
        'mortgage_forbearance', 'insurance_underwriting',
        'insurance_claim', 'insurance_non_renewal', 'complaint_response'.
    automated_credit_decision : bool, optional
        Whether the decision was made solely by automated means (no meaningful
        human involvement). Engages UK GDPR Art 22 / DUAA 2025 s.80.
    human_review_available : bool, optional
        Whether a human review / appeal was offered. Note: a review offered
        *after* an automated decision does not, by itself, satisfy the binary
        test's pre-decision timing element.
    disp_stage : str, optional
        DISP handling stage, e.g. 'acknowledgement', 'final_response',
        'referred_to_fos'.
    complaint_date : str, optional
        ISO date the complaint was made — the start of the DISP window.
    final_response_issued : bool, optional
        Whether a DISP final response has been issued.
    disp_deadline_breached : bool, optional
        Whether the DISP final-response deadline has passed without a final
        response. Compute with DeadlineEngine('fca_disp_final_response').
    regulatory_framework : str, optional
        Applicable framework (defaults conceptually to 'FCA DISP').
    """

    @property
    def name(self) -> str:
        return "banking"

    @property
    def guidance(self) -> str:
        return (
            "Banking domain: financial decisions engage two distinct standards.\n\n"
            "First, the binary test. A solely automated credit refusal, account "
            "closure, funds freeze, mortgage underwriting decision, or insurance "
            "claim / underwriting / non-renewal outcome is NULL unless a named "
            "human reviewed the specific facts before the decision took effect. "
            "An appeal offered after the automated refusal is involvement, not "
            "review — it could not have changed the original decision.\n\n"
            "Second, UK GDPR Art 22 / DUAA 2025 s.80. A significant, solely "
            "automated decision about a person requires a lawful basis and the "
            "right to obtain human intervention. Record whether the decision was "
            "automated and whether human review was genuinely available before "
            "the decision.\n\n"
            "Third, FCA DISP deadlines. A firm must issue a final response within "
            "8 weeks (DISP 1.6). A complaint past that deadline without a named, "
            "substantive final response is a DISP breach and typically NULL.\n\n"
            "Ask directly: 'Was this decision made solely by automated means, and "
            "if so, who is the named individual who reviewed my specific "
            "circumstances before it took effect?'"
        )

    def validate_domain_metadata(self, metadata: dict[str, Any]) -> list[str]:
        issues: list[str] = []

        automated = metadata.get("automated_credit_decision", False)
        decision_type = metadata.get("decision_type", "")
        human_review_available = metadata.get("human_review_available", None)

        if automated:
            issues.append(
                "Decision was solely automated — engages UK GDPR Art 22 / "
                "DUAA 2025 s.80. Binary test returns NULL unless a named human "
                "reviewed the specific facts before the decision took effect."
            )
            if decision_type in _HIGH_STAKES_AUTOMATED:
                issues.append(
                    f"High-stakes automated decision ('{decision_type}') — a "
                    "significant solely-automated decision requires a lawful basis "
                    "and a genuine right to human intervention."
                )
            if human_review_available is False:
                issues.append(
                    "No human review was available for an automated decision — "
                    "confirmed absence of the Art 22 / DUAA 2025 s.80 safeguard."
                )

        if metadata.get("disp_deadline_breached"):
            issues.append(
                "FCA DISP final-response deadline breached (8 weeks, DISP 1.6) "
                "without a final response — regulatory breach recorded alongside "
                "the binary test outcome."
            )

        return issues

    def _build_domain_metadata(
        self,
        decision_type: Optional[str] = None,
        automated_credit_decision: bool = False,
        human_review_available: Optional[bool] = None,
        disp_stage: Optional[str] = None,
        complaint_date: Optional[str] = None,
        final_response_issued: Optional[bool] = None,
        disp_deadline_breached: bool = False,
        regulatory_framework: Optional[str] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "domain": self.name,
            "automated_credit_decision": automated_credit_decision,
            "disp_deadline_breached": disp_deadline_breached,
        }
        if decision_type:
            meta["decision_type"] = decision_type
        if human_review_available is not None:
            meta["human_review_available"] = human_review_available
        if disp_stage:
            meta["disp_stage"] = disp_stage
        if complaint_date:
            meta["complaint_date"] = complaint_date
        if final_response_issued is not None:
            meta["final_response_issued"] = final_response_issued
        if regulatory_framework:
            meta["regulatory_framework"] = regulatory_framework
        meta.update(kwargs)
        return meta
