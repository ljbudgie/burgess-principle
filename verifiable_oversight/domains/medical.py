"""
MedicalDomain — oversight assessment for clinical and care decisions.

Phase 4D. Clinical decisions engage accountability requirements that go beyond
the general binary test:

1. **Clinical decision-support tools.** An algorithmic triage score, risk
   stratification, or diagnostic suggestion informs a decision — it does not
   make it. Where a clinical decision-support (CDS) output is treated as the
   decision, with no named clinician applying their judgment to the specific
   patient before it takes effect, the decision is NULL.

2. **Consent.** A decision affecting a patient's care generally requires the
   patient's informed consent (or a lawful alternative basis). A decision taken
   without recorded consent, where consent was required, is a distinct failure
   recorded here.

3. **Mental Capacity Act 2005.** Where capacity is in doubt, s.1–s.4 MCA 2005
   require a capacity assessment and, if the person lacks capacity, a
   best-interests determination by a named decision-maker. A decision made for a
   person who may lack capacity, without a capacity assessment and best-interests
   process, is NULL and a probable MCA breach.

This domain records these facts alongside the binary test. It never overrides
clinical judgment — it records whether a named clinician's judgment was applied
to the specific patient before the decision took effect.
"""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseDomain


class MedicalDomain(BaseDomain):
    """
    Domain for clinical / care decisions — Phase 4D.

    Additional domain_kwargs
    -----------------------
    decision_type : str, optional
        Type of decision, e.g. 'triage', 'diagnosis', 'treatment',
        'discharge', 'care_package', 'dols'.
    clinical_decision_support_used : bool, optional
        Whether a clinical decision-support / algorithmic tool informed the
        decision.
    cds_treated_as_decision : bool, optional
        Whether the CDS output was treated as the decision itself, with no named
        clinician applying judgment to the specific patient before it took effect.
    consent_required : bool, optional
        Whether the decision required the patient's informed consent.
    consent_obtained : bool, optional
        Whether informed consent (or a lawful alternative basis) was recorded.
    capacity_in_doubt : bool, optional
        Whether the patient's capacity to make this decision was in doubt.
    capacity_assessed : bool, optional
        Whether a Mental Capacity Act 2005 capacity assessment was carried out.
    best_interests_determined : bool, optional
        Whether a best-interests determination (s.4 MCA 2005) was made where the
        person was found to lack capacity.
    regulatory_framework : str, optional
        Applicable framework (e.g. 'MCA 2005', 'GMC Good Medical Practice').
    """

    @property
    def name(self) -> str:
        return "medical"

    @property
    def guidance(self) -> str:
        return (
            "Medical domain: clinical decisions require a named clinician's "
            "judgment applied to the specific patient before the decision takes "
            "effect.\n\n"
            "Clinical decision-support tools inform decisions; they do not make "
            "them. Where an algorithmic triage or risk score is treated as the "
            "decision, with no named clinician's judgment applied to this patient, "
            "the decision is NULL.\n\n"
            "Consent: a decision affecting care generally requires the patient's "
            "informed consent or a lawful alternative basis. Record whether "
            "consent was required and whether it was obtained.\n\n"
            "Mental Capacity Act 2005: where capacity is in doubt, ss.1–4 require "
            "a capacity assessment and, if the person lacks capacity, a "
            "best-interests determination by a named decision-maker. A decision "
            "made without this process, for a person who may lack capacity, is "
            "NULL and a probable MCA breach.\n\n"
            "Ask directly: 'Which named clinician applied their clinical judgment "
            "to my specific circumstances before this decision took effect?'"
        )

    def validate_domain_metadata(self, metadata: dict[str, Any]) -> list[str]:
        issues: list[str] = []

        if metadata.get("clinical_decision_support_used") and metadata.get(
            "cds_treated_as_decision"
        ):
            issues.append(
                "Clinical decision-support output was treated as the decision "
                "with no named clinician applying judgment to this patient — "
                "NULL on the binary test."
            )

        if metadata.get("consent_required"):
            consent_obtained = metadata.get("consent_obtained", None)
            if consent_obtained is False:
                issues.append(
                    "Consent was required but not recorded as obtained — a "
                    "distinct consent failure alongside the binary test."
                )

        if metadata.get("capacity_in_doubt"):
            if metadata.get("capacity_assessed") is False:
                issues.append(
                    "Capacity was in doubt but no MCA 2005 capacity assessment "
                    "(ss.1–3) was carried out — NULL and probable MCA breach."
                )
            elif metadata.get("best_interests_determined") is False:
                issues.append(
                    "Person may lack capacity but no best-interests determination "
                    "(s.4 MCA 2005) was made by a named decision-maker."
                )

        return issues

    def _build_domain_metadata(
        self,
        decision_type: Optional[str] = None,
        clinical_decision_support_used: bool = False,
        cds_treated_as_decision: bool = False,
        consent_required: bool = False,
        consent_obtained: Optional[bool] = None,
        capacity_in_doubt: bool = False,
        capacity_assessed: Optional[bool] = None,
        best_interests_determined: Optional[bool] = None,
        regulatory_framework: Optional[str] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "domain": self.name,
            "clinical_decision_support_used": clinical_decision_support_used,
            "cds_treated_as_decision": cds_treated_as_decision,
            "consent_required": consent_required,
            "capacity_in_doubt": capacity_in_doubt,
        }
        if decision_type:
            meta["decision_type"] = decision_type
        if consent_obtained is not None:
            meta["consent_obtained"] = consent_obtained
        if capacity_assessed is not None:
            meta["capacity_assessed"] = capacity_assessed
        if best_interests_determined is not None:
            meta["best_interests_determined"] = best_interests_determined
        if regulatory_framework:
            meta["regulatory_framework"] = regulatory_framework
        meta.update(kwargs)
        return meta
