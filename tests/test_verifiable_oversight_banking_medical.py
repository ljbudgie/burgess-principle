"""Tests for verifiable_oversight Phase 4D — banking + medical domains."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from verifiable_oversight import BinaryTest, Verdict
from verifiable_oversight.domains import BankingDomain, MedicalDomain


def _issues(record) -> list:
    return record.domain_metadata.get("_validation_issues", [])


def _sovereign_bt() -> BinaryTest:
    return BinaryTest(
        named_person="Rebecca Hunt",
        role_and_authority="Underwriter, authority to approve",
        specific_facts_considered="Reviewed the applicant's specific file",
        pre_decision_timing="Reviewed before the decision took effect",
        authority_to_differ="Held authority to reach a different outcome",
    )


# ---------------------------------------------------------------------------
# Banking
# ---------------------------------------------------------------------------

def test_banking_name_and_export():
    from verifiable_oversight.domains import __all__ as domain_all

    assert BankingDomain().name == "banking"
    assert "BankingDomain" in domain_all


def test_banking_automated_decision_flagged():
    record = BankingDomain().create_record(
        subject="Automated credit refusal",
        institution="Example Bank plc",
        binary_test=BinaryTest(context="Declined by scoring system."),
        automated_credit_decision=True,
    )
    assert any("solely automated" in i for i in _issues(record))
    assert record.verdict is Verdict.NULL


def test_banking_high_stakes_automated_extra_flag():
    record = BankingDomain().create_record(
        subject="Automated account closure",
        institution="Example Bank plc",
        binary_test=BinaryTest(context="Closed automatically."),
        automated_credit_decision=True,
        decision_type="account_closure",
        human_review_available=False,
    )
    issues = _issues(record)
    assert any("High-stakes automated decision" in i for i in issues)
    assert any("No human review was available" in i for i in issues)


def test_banking_mortgage_and_insurance_high_stakes():
    for decision_type in (
        "mortgage_decision",
        "mortgage_forbearance",
        "insurance_underwriting",
        "insurance_claim",
        "insurance_non_renewal",
    ):
        record = BankingDomain().create_record(
            subject=f"Automated {decision_type}",
            institution="Example Financial Firm plc",
            binary_test=BinaryTest(context="Scored automatically."),
            automated_credit_decision=True,
            decision_type=decision_type,
            human_review_available=False,
        )
        issues = _issues(record)
        assert any("High-stakes automated decision" in i for i in issues), decision_type
        assert record.verdict is Verdict.NULL


def test_banking_disp_deadline_breach_flagged():
    record = BankingDomain().create_record(
        subject="Complaint past DISP deadline",
        institution="Example Bank plc",
        binary_test=_sovereign_bt(),
        disp_deadline_breached=True,
    )
    assert any("DISP final-response deadline breached" in i for i in _issues(record))


def test_banking_clean_manual_decision_no_issues():
    record = BankingDomain().create_record(
        subject="Manual underwriting decision",
        institution="Example Bank plc",
        binary_test=_sovereign_bt(),
        automated_credit_decision=False,
        disp_deadline_breached=False,
    )
    assert _issues(record) == []
    assert record.verdict is Verdict.SOVEREIGN


def test_banking_metadata_defaults_recorded():
    record = BankingDomain().create_record(
        subject="X",
        institution="Y",
        binary_test=BinaryTest(context="z"),
    )
    md = record.domain_metadata
    assert md["automated_credit_decision"] is False
    assert md["disp_deadline_breached"] is False


# ---------------------------------------------------------------------------
# Medical
# ---------------------------------------------------------------------------

def test_medical_name_and_export():
    from verifiable_oversight.domains import __all__ as domain_all

    assert MedicalDomain().name == "medical"
    assert "MedicalDomain" in domain_all


def test_medical_cds_treated_as_decision_flagged():
    record = MedicalDomain().create_record(
        subject="Triage by score",
        institution="Example NHS Trust",
        binary_test=BinaryTest(context="Algorithmic triage."),
        clinical_decision_support_used=True,
        cds_treated_as_decision=True,
    )
    assert any("decision-support output was treated as the decision" in i
               for i in _issues(record))


def test_medical_cds_used_but_not_as_decision_ok():
    record = MedicalDomain().create_record(
        subject="Triage informed by score",
        institution="Example NHS Trust",
        binary_test=_sovereign_bt(),
        clinical_decision_support_used=True,
        cds_treated_as_decision=False,
    )
    assert not any("decision-support output was treated" in i
                   for i in _issues(record))


def test_medical_consent_required_but_not_obtained_flagged():
    record = MedicalDomain().create_record(
        subject="Treatment without consent",
        institution="Example NHS Trust",
        binary_test=_sovereign_bt(),
        consent_required=True,
        consent_obtained=False,
    )
    assert any("Consent was required but not recorded" in i for i in _issues(record))


def test_medical_capacity_in_doubt_no_assessment_flagged():
    record = MedicalDomain().create_record(
        subject="Discharge, capacity in doubt",
        institution="Example NHS Trust",
        binary_test=BinaryTest(context="No assessment."),
        capacity_in_doubt=True,
        capacity_assessed=False,
    )
    assert any("no MCA 2005 capacity assessment" in i for i in _issues(record))


def test_medical_capacity_assessed_but_no_best_interests_flagged():
    record = MedicalDomain().create_record(
        subject="Lacks capacity, no best interests",
        institution="Example NHS Trust",
        binary_test=_sovereign_bt(),
        capacity_in_doubt=True,
        capacity_assessed=True,
        best_interests_determined=False,
    )
    assert any("best-interests determination" in i for i in _issues(record))


def test_medical_clean_decision_no_issues():
    record = MedicalDomain().create_record(
        subject="Consented treatment, capacity clear",
        institution="Example NHS Trust",
        binary_test=_sovereign_bt(),
        consent_required=True,
        consent_obtained=True,
        capacity_in_doubt=False,
    )
    assert _issues(record) == []
    assert record.verdict is Verdict.SOVEREIGN
