"""
Iris integration — mid-conversation assessment (Phase 4C).

Iris is the conversational assistant in this repository. During a conversation
a user describes an institutional decision a piece at a time; Iris needs to
assess what it has so far, ask the *right* next question to close the gap, and —
once enough is known — create and verify a permanent :class:`DecisionRecord`.

This module provides a runtime-agnostic :class:`ConversationAssessor` that does
exactly that. It is deliberately Python-only and free of any Iris-specific
transport, so the same logic can back the Iris UI, a CLI, or a test harness.

Two ideas make it "mid-conversation":

- **AMBIGUOUS, not NULL, while gathering.** Mid-conversation, a missing element
  usually means *Iris has not asked yet*, not that the element is confirmed
  absent. So mid-conversation assessment uses ``ambiguous_if_missing=True``:
  the verdict is AMBIGUOUS and Iris is prompted to ask the missing question,
  rather than prematurely declaring NULL.

- **Targeted follow-up questions.** For every element still missing, the
  assessor returns the precise question to ask next (see
  :data:`FOLLOW_UP_QUESTIONS`). This is the operational core of the Burgess
  method: never accept process language — ask for the named individual.

When the conversation has gathered enough (or the user confirms an element is
genuinely absent), :meth:`ConversationAssessor.finalise` produces a definitive
record (``ambiguous_if_missing=False`` — a real SOVEREIGN or NULL) and, if a
:class:`RecordStore` was supplied, appends it to the tamper-evident ledger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from ..core.binary_test import BinaryTest, Verdict
from ..core.decision_record import DecisionRecord
from ..core.storage import LedgerEntry, RecordStore
from ..core.verifier import VerificationReport, Verifier
from ..domains.base import BaseDomain
from ..domains.general import GeneralDomain


# The direct question Iris should ask to close each missing element. These are
# intentionally blunt: they ask for a named individual and specific facts, and
# they never accept process language ("our team reviewed it") as an answer.
FOLLOW_UP_QUESTIONS: dict[str, str] = {
    "named_person": (
        "Please provide the full name of the individual who made this decision. "
        "A team or department name does not answer this question."
    ),
    "role_and_authority": (
        "What is that individual's role, and did they hold the authority to reach "
        "a different outcome?"
    ),
    "specific_facts_considered": (
        "What specific facts of your case did they consider? Point to concrete "
        "evidence that your individual circumstances — not just the general "
        "category of case — were reviewed."
    ),
    "pre_decision_timing": (
        "Did that review take place before the decision was made and took effect, "
        "rather than afterwards?"
    ),
    "authority_to_differ": (
        "Did that individual have the practical authority to reach a different "
        "conclusion, or were they constrained by policy to this outcome?"
    ),
}


def follow_up_questions_for(binary_test: BinaryTest) -> list[str]:
    """Return the follow-up questions for every element still absent."""
    present = binary_test.elements_present
    return [
        FOLLOW_UP_QUESTIONS[element]
        for element, is_present in present.items()
        if not is_present
    ]


@dataclass
class ConversationAssessment:
    """
    The result of a single mid-conversation assessment.

    Attributes
    ----------
    record:
        The sealed :class:`DecisionRecord` for the current state of knowledge.
    report:
        The :class:`VerificationReport` for that record.
    follow_up_questions:
        The questions Iris should ask next to close the remaining gaps.
    missing_elements:
        Element keys still absent.
    complete:
        True when all five elements are present (no follow-up needed).
    finalised:
        True if this assessment was produced by :meth:`ConversationAssessor.finalise`
        (a definitive SOVEREIGN/NULL) rather than a mid-conversation snapshot.
    """

    record: DecisionRecord
    report: VerificationReport
    follow_up_questions: list[str] = field(default_factory=list)
    missing_elements: list[str] = field(default_factory=list)
    complete: bool = False
    finalised: bool = False

    @property
    def verdict(self) -> Verdict:
        return self.record.verdict

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "complete": self.complete,
            "finalised": self.finalised,
            "missing_elements": list(self.missing_elements),
            "follow_up_questions": list(self.follow_up_questions),
            "record": self.record.to_dict(),
            "report": self.report.to_dict(),
        }

    def __str__(self) -> str:
        state = "finalised" if self.finalised else "in progress"
        return (
            f"[{self.verdict.value}] {state} — "
            f"{len(self.missing_elements)} element(s) outstanding"
        )


class ConversationAssessor:
    """
    Create and verify oversight records mid-conversation on a user's behalf.

    Usage
    -----
        assessor = ConversationAssessor(store=RecordStore("ledger.jsonl"))

        # Mid-conversation: assess what we have, get the next question to ask.
        step = assessor.assess(
            subject="Complaint response from EASS",
            institution="EASS",
            binary_test=BinaryTest(context="Signed 'Rachel.D', no surname."),
        )
        step.verdict                 # Verdict.AMBIGUOUS (still gathering)
        step.follow_up_questions[0]  # "Please provide the full name ..."

        # When the user confirms no named individual exists, finalise it.
        final = assessor.finalise(
            subject="Complaint response from EASS",
            institution="EASS",
            binary_test=BinaryTest(context="User confirms no name was ever given."),
        )
        final.verdict     # Verdict.NULL (definitive)
        final.finalised   # True — appended to the ledger if a store was given

    Parameters
    ----------
    domain:
        The :class:`BaseDomain` to build records in. Defaults to
        :class:`GeneralDomain`.
    store:
        Optional :class:`RecordStore`. When supplied, finalised records are
        appended to the tamper-evident ledger.
    verifier:
        Optional :class:`Verifier`. A default one is created if omitted.
    """

    def __init__(
        self,
        domain: Optional[BaseDomain] = None,
        *,
        store: Optional[RecordStore] = None,
        verifier: Optional[Verifier] = None,
    ) -> None:
        self._domain: BaseDomain = domain or GeneralDomain()
        self._store = store
        self._verifier = verifier or Verifier()

    @property
    def domain(self) -> BaseDomain:
        return self._domain

    @property
    def store(self) -> Optional[RecordStore]:
        return self._store

    # ------------------------------------------------------------------
    # Assessment
    # ------------------------------------------------------------------

    def assess(
        self,
        *,
        subject: str,
        institution: str,
        binary_test: BinaryTest,
        assessor: Optional[str] = None,
        decision_date: Optional[str] = None,
        notes: Optional[str] = None,
        **domain_kwargs: Any,
    ) -> ConversationAssessment:
        """
        Assess the current state of a conversation (non-final).

        Missing elements yield AMBIGUOUS (``ambiguous_if_missing=True``), because
        mid-conversation a gap usually means Iris has not asked yet. The returned
        assessment carries the follow-up questions to ask next.
        """
        return self._build_assessment(
            subject=subject,
            institution=institution,
            binary_test=binary_test,
            assessor=assessor,
            decision_date=decision_date,
            notes=notes,
            ambiguous_if_missing=True,
            finalised=False,
            domain_kwargs=domain_kwargs,
        )

    def finalise(
        self,
        *,
        subject: str,
        institution: str,
        binary_test: BinaryTest,
        assessor: Optional[str] = None,
        decision_date: Optional[str] = None,
        notes: Optional[str] = None,
        **domain_kwargs: Any,
    ) -> ConversationAssessment:
        """
        Produce a definitive assessment and, if a store was supplied, record it.

        Missing elements now yield a real NULL (``ambiguous_if_missing=False``):
        the conversation has established that the element is genuinely absent,
        not merely unasked. If a :class:`RecordStore` was supplied, the sealed
        record is appended to the ledger. Re-recording the *same* sealed record
        (identical fingerprint) is a safe no-op rather than a ``StorageError``.
        """
        assessment = self._build_assessment(
            subject=subject,
            institution=institution,
            binary_test=binary_test,
            assessor=assessor,
            decision_date=decision_date,
            notes=notes,
            ambiguous_if_missing=False,
            finalised=True,
            domain_kwargs=domain_kwargs,
        )
        if self._store is not None:
            self.record(assessment.record)
        return assessment

    def record(self, record: DecisionRecord) -> Optional[LedgerEntry]:
        """
        Append a record to the store, ignoring exact duplicates.

        Returns the created :class:`LedgerEntry`, or ``None`` if there is no
        store or the record is already present.
        """
        if self._store is None:
            return None
        if record.fingerprint and record.fingerprint in self._store:
            return None
        return self._store.append(record)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _build_assessment(
        self,
        *,
        subject: str,
        institution: str,
        binary_test: BinaryTest,
        assessor: Optional[str],
        decision_date: Optional[str],
        notes: Optional[str],
        ambiguous_if_missing: bool,
        finalised: bool,
        domain_kwargs: dict[str, Any],
    ) -> ConversationAssessment:
        record = self._domain.create_record(
            subject=subject,
            institution=institution,
            binary_test=binary_test,
            assessor=assessor,
            decision_date=decision_date,
            notes=notes,
            ambiguous_if_missing=ambiguous_if_missing,
            **domain_kwargs,
        )
        report = self._verifier.verify(record)
        missing = list(record.result.missing_elements)
        questions = [FOLLOW_UP_QUESTIONS[m] for m in missing if m in FOLLOW_UP_QUESTIONS]
        return ConversationAssessment(
            record=record,
            report=report,
            follow_up_questions=questions,
            missing_elements=missing,
            complete=not missing,
            finalised=finalised,
        )
