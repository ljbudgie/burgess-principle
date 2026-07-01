"""Tests for verifiable_oversight Phase 4C — Iris mid-conversation assessment."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from verifiable_oversight import BinaryTest, Verdict, RecordStore
from verifiable_oversight.domains import CommunicationDomain, GeneralDomain
from verifiable_oversight.integrations import (
    ConversationAssessor,
    ConversationAssessment,
    FOLLOW_UP_QUESTIONS,
    follow_up_questions_for,
)


def _sovereign_bt() -> BinaryTest:
    return BinaryTest(
        named_person="Rebecca Hunt",
        role_and_authority="Complaints Manager, authority to overturn",
        specific_facts_considered="Reviewed the specific facts of this case",
        pre_decision_timing="Reviewed before the response was sent",
        authority_to_differ="Held authority to reach a different outcome",
    )


def test_follow_up_questions_cover_all_elements():
    assert set(FOLLOW_UP_QUESTIONS) == {
        "named_person",
        "role_and_authority",
        "specific_facts_considered",
        "pre_decision_timing",
        "authority_to_differ",
    }


def test_follow_up_questions_for_empty_binary_test():
    questions = follow_up_questions_for(BinaryTest(context="nothing yet"))
    assert len(questions) == 5


def test_follow_up_questions_for_partial():
    bt = BinaryTest(named_person="Jane Doe")
    questions = follow_up_questions_for(bt)
    assert FOLLOW_UP_QUESTIONS["named_person"] not in questions
    assert len(questions) == 4


def test_mid_conversation_is_ambiguous_not_null():
    assessor = ConversationAssessor()
    step = assessor.assess(
        subject="EASS response",
        institution="EASS",
        binary_test=BinaryTest(context="Signed 'Rachel.D'."),
    )
    assert step.verdict is Verdict.AMBIGUOUS
    assert step.complete is False
    assert step.finalised is False
    assert len(step.missing_elements) == 5
    assert len(step.follow_up_questions) == 5


def test_complete_binary_test_is_sovereign_and_no_questions():
    assessor = ConversationAssessor()
    step = assessor.assess(
        subject="Named review",
        institution="LGO",
        binary_test=_sovereign_bt(),
    )
    assert step.verdict is Verdict.SOVEREIGN
    assert step.complete is True
    assert step.follow_up_questions == []


def test_finalise_produces_definitive_null():
    assessor = ConversationAssessor()
    final = assessor.finalise(
        subject="EASS response",
        institution="EASS",
        binary_test=BinaryTest(context="No name ever given."),
    )
    assert final.verdict is Verdict.NULL
    assert final.finalised is True


def test_finalise_appends_to_store():
    store = RecordStore()
    assessor = ConversationAssessor(store=store)
    final = assessor.finalise(
        subject="EASS response",
        institution="EASS",
        binary_test=BinaryTest(context="No name."),
    )
    assert len(store) == 1
    assert final.record.fingerprint in store
    assert store.verify_chain() is True


def test_record_same_record_twice_is_ignored():
    store = RecordStore()
    assessor = ConversationAssessor(store=store)
    final = assessor.finalise(
        subject="S", institution="I", binary_test=BinaryTest(context="x")
    )
    # Re-recording the identical sealed record (same fingerprint) is a no-op,
    # not a StorageError.
    assert assessor.record(final.record) is None
    assert len(store) == 1


def test_assess_does_not_write_to_store():
    store = RecordStore()
    assessor = ConversationAssessor(store=store)
    assessor.assess(subject="S", institution="I", binary_test=BinaryTest(context="x"))
    assert len(store) == 0


def test_domain_kwargs_passed_through():
    assessor = ConversationAssessor(CommunicationDomain())
    step = assessor.assess(
        subject="EASS response",
        institution="EASS",
        binary_test=BinaryTest(context="phone number given"),
        channel="telephone",
        ra_on_record=True,
        ra_description="email-only communication",
        channel_accessible=False,
    )
    assert step.record.domain == "communication"
    assert step.record.domain_metadata["channel"] == "telephone"
    assert step.record.domain_metadata.get("_validation_issues")


def test_record_without_store_returns_none():
    assessor = ConversationAssessor()
    step = assessor.assess(subject="S", institution="I",
                           binary_test=BinaryTest(context="x"))
    assert assessor.record(step.record) is None


def test_assessment_to_dict_and_str():
    assessor = ConversationAssessor()
    step = assessor.assess(subject="S", institution="I",
                           binary_test=BinaryTest(context="x"))
    d = step.to_dict()
    assert d["verdict"] == "AMBIGUOUS"
    assert "record" in d and "report" in d
    assert "in progress" in str(step)


def test_default_domain_is_general():
    assessor = ConversationAssessor()
    assert isinstance(assessor.domain, GeneralDomain)
