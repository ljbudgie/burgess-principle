"""Tests for verifiable_oversight Phase 5 — Mental Capacity Act 2005 domain."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from verifiable_oversight import Verdict, BinaryTest
from verifiable_oversight.domains import CapacityAssessment, MedicalDomain


def _issues(record) -> list:
    return record.domain_metadata.get("_validation_issues", [])


def _complete_capacity(**overrides) -> CapacityAssessment:
    """A complete, issue-free two-stage assessment (SOVEREIGN)."""
    kwargs = dict(
        decision_in_question="Consent to fitting of hearing aids",
        time_of_assessment="2026-07-01T14:00:00Z",
        named_assessor="Priya Sharma",
        assessor_role="Consultant Audiologist",
        diagnostic_condition_identified=True,
        functional_test_applied=True,
        can_understand=True,
        can_retain=True,
        can_use_and_weigh=True,
        can_communicate=True,
        capacity_present=True,
    )
    kwargs.update(overrides)
    return CapacityAssessment(**kwargs)


# ---------------------------------------------------------------------------
# Exports
# ---------------------------------------------------------------------------

def test_capacity_exported():
    from verifiable_oversight.domains import __all__ as domain_all

    assert "CapacityAssessment" in domain_all


def test_version_is_0_5_0():
    import verifiable_oversight

    assert verifiable_oversight.__version__ == "0.5.0"


# ---------------------------------------------------------------------------
# SOVEREIGN
# ---------------------------------------------------------------------------

def test_complete_assessment_is_sovereign():
    assessment = _complete_capacity()
    assert assessment.assess() is Verdict.SOVEREIGN
    assert assessment.validation_issues() == []


# ---------------------------------------------------------------------------
# NULL
# ---------------------------------------------------------------------------

def test_empty_assessment_is_null():
    assessment = CapacityAssessment(
        decision_in_question="Discharge to residential care",
        time_of_assessment="2026-07-01T00:00:00Z",
    )
    assert assessment.assess() is Verdict.NULL


def test_phonak_autosense_automated_is_null():
    assessment = CapacityAssessment(
        decision_in_question=(
            "Adjustment of hearing aid programme for bilateral sensorineural "
            "high-frequency sloping loss, PTAs ~68-70 dB HL"
        ),
        time_of_assessment="2026-07-01T00:00:00Z",
        automated_system_used=True,
        automated_system_name="Phonak AutoSense OS 5.0",
        named_clinician_reviewed_output=False,
    )
    assert assessment.assess() is Verdict.NULL
    assert any(
        "Phonak AutoSense OS 5.0" in i and "named clinician review" in i
        for i in assessment.validation_issues()
    )


def test_automated_system_with_review_clears_that_issue():
    assessment = _complete_capacity(
        automated_system_used=True,
        automated_system_name="Phonak AutoSense OS 5.0",
        named_clinician_reviewed_output=True,
    )
    assert assessment.assess() is Verdict.SOVEREIGN
    assert not any("named clinician review" in i for i in assessment.validation_issues())


# ---------------------------------------------------------------------------
# AMBIGUOUS — partially gathered
# ---------------------------------------------------------------------------

def test_named_assessor_but_incomplete_is_ambiguous():
    assessment = CapacityAssessment(
        decision_in_question="Consent to treatment",
        time_of_assessment="2026-07-01T00:00:00Z",
        named_assessor="Dr Amara Okoye",
        assessor_role="Consultant Geriatrician",
        diagnostic_condition_identified=True,
        functional_test_applied=False,
    )
    assert assessment.assess() is Verdict.AMBIGUOUS
    assert any("functional test (s.3) not applied" in i for i in assessment.validation_issues())


# ---------------------------------------------------------------------------
# Two-stage test
# ---------------------------------------------------------------------------

def test_no_stage_recorded_flagged():
    assessment = CapacityAssessment(
        decision_in_question="Consent",
        time_of_assessment="2026-07-01T00:00:00Z",
        named_assessor="Dr Amara Okoye",
        assessor_role="Consultant",
    )
    assert any(
        "Neither stage of the MCA two-stage test" in i
        for i in assessment.validation_issues()
    )


def test_functional_element_not_assessed_flagged():
    assessment = _complete_capacity(can_use_and_weigh=None)
    issues = assessment.validation_issues()
    assert any("use and weigh" in i for i in issues)
    assert assessment.assess() is Verdict.AMBIGUOUS


# ---------------------------------------------------------------------------
# Best interests (s.4)
# ---------------------------------------------------------------------------

def test_best_interests_requires_named_decision_maker():
    assessment = _complete_capacity(
        capacity_present=False,
        best_interests_decision_required=True,
        best_interests_named_decision_maker="",
        least_restrictive_option_considered=False,
    )
    issues = assessment.validation_issues()
    assert any("no named" in i and "decision maker" in i for i in issues)
    assert any("least restrictive" in i for i in issues)
    assert assessment.assess() is Verdict.AMBIGUOUS


def test_best_interests_complete_is_sovereign():
    assessment = _complete_capacity(
        capacity_present=False,
        best_interests_decision_required=True,
        best_interests_named_decision_maker="Dr Amara Okoye",
        best_interests_decision_maker_role="Consultant Geriatrician",
        least_restrictive_option_considered=True,
    )
    assert assessment.assess() is Verdict.SOVEREIGN
    assert assessment.validation_issues() == []


# ---------------------------------------------------------------------------
# MedicalDomain integration
# ---------------------------------------------------------------------------

def test_assess_capacity_none_is_null():
    assert MedicalDomain().assess_capacity(None) is Verdict.NULL


def test_assess_capacity_delegates():
    assessment = _complete_capacity()
    assert MedicalDomain().assess_capacity(assessment) is Verdict.SOVEREIGN


def test_medical_record_folds_in_null_capacity():
    assessment = CapacityAssessment(
        decision_in_question="Hearing aid adjustment",
        time_of_assessment="2026-07-01T00:00:00Z",
        automated_system_used=True,
        automated_system_name="Phonak AutoSense OS 5.0",
        named_clinician_reviewed_output=False,
    )
    record = MedicalDomain().create_record(
        subject="Automated audiological adjustment, no named review",
        institution="Example NHS Trust",
        binary_test=BinaryTest(context="Adjusted automatically."),
        capacity_assessment=assessment,
    )
    assert record.domain_metadata["capacity_assessment_verdict"] == Verdict.NULL.value
    assert any("MCA 2005 capacity assessment is NULL" in i for i in _issues(record))


def test_medical_record_clinical_ai_without_signoff_flagged():
    record = MedicalDomain().create_record(
        subject="Clinical AI output applied",
        institution="Example NHS Trust",
        binary_test=BinaryTest(context="Applied by system."),
        clinical_ai_involved=True,
        clinical_ai_system="Phonak AutoSense OS 5.0",
        named_clinician_sign_off=False,
        mhra_registered=False,
    )
    issues = _issues(record)
    assert any("no named clinician" in i for i in issues)
    assert any("MHRA-registered" in i for i in issues)
