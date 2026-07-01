"""
Example: Banking + Medical domains (Phase 4D)

Two decisions:
  1. A solely automated credit refusal by a bank, with no human review — NULL,
     engaging UK GDPR Art 22 / DUAA 2025 s.80, past its FCA DISP deadline.
  2. A hospital discharge decision for a patient whose capacity is in doubt,
     with no capacity assessment — NULL, probable Mental Capacity Act breach.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import BinaryTest, DeadlineEngine, Verifier
from verifiable_oversight.domains import BankingDomain, MedicalDomain


def _print(title, record):
    print("=" * 60)
    print(title)
    print("=" * 60)
    print("VERDICT:", record.verdict.value, f"({record.result.score}/5)")
    print("DOMAIN METADATA:")
    for k, v in record.domain_metadata.items():
        if k == "_validation_issues":
            continue
        print(f"  {k}: {v}")
    print("FINDINGS:")
    for issue in record.domain_metadata.get("_validation_issues", []) or ["  None"]:
        print(f"  ⚠ {issue}")
    print()


def main() -> None:
    verifier = Verifier()
    engine = DeadlineEngine()

    # 1. Banking — automated credit refusal, past DISP deadline.
    disp = engine.evaluate(
        "fca_disp_final_response", start="2026-03-01", reference="2026-07-01"
    )
    banking = BankingDomain().create_record(
        subject="Automated credit refusal, no human review",
        institution="Example Bank plc",
        binary_test=BinaryTest(
            context="Application declined by an automated scoring system. No "
            "named individual reviewed the specific circumstances.",
        ),
        assessor="Lewis James Burgess",
        decision_type="credit_refusal",
        automated_credit_decision=True,
        human_review_available=False,
        disp_stage="final_response",
        complaint_date="2026-03-01",
        final_response_issued=False,
        disp_deadline_breached=disp.breached,
        regulatory_framework="FCA DISP; UK GDPR Art 22; DUAA 2025 s.80",
    )
    _print("BANKING — automated credit refusal", banking)
    print("  DISP deadline:", disp)
    print()
    print(verifier.verify(banking))
    print()

    # 2. Medical — discharge, capacity in doubt, no assessment.
    medical = MedicalDomain().create_record(
        subject="Discharge decision, capacity in doubt",
        institution="Example NHS Trust",
        binary_test=BinaryTest(
            context="Patient discharged following an automated risk score. "
            "Capacity was in doubt; no assessment recorded.",
        ),
        assessor="Lewis James Burgess",
        decision_type="discharge",
        clinical_decision_support_used=True,
        cds_treated_as_decision=True,
        consent_required=True,
        consent_obtained=False,
        capacity_in_doubt=True,
        capacity_assessed=False,
        regulatory_framework="MCA 2005 ss.1–4",
    )
    _print("MEDICAL — discharge, capacity in doubt", medical)
    print(verifier.verify(medical))


if __name__ == "__main__":
    main()
