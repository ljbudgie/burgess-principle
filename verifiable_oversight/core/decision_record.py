"""
Decision Record — the canonical, verifiable record of a SOVEREIGN/NULL assessment.

A DecisionRecord is the unit of accountability. It captures:
- What decision was assessed
- Who (if anyone) made it, and how
- The binary test result
- A content fingerprint (SHA-256) for integrity verification
- Optional cryptographic signature for non-repudiation

The fingerprint is always computed. The signature field is reserved
for future integration with signing infrastructure (e.g. Ed25519 via
the existing CRYPTOGRAPHIC_IDENTITY.md architecture in this repo).
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from .binary_test import BinaryTest, BinaryTestResult, Verdict


@dataclass
class DecisionRecord:
    """
    A verifiable record of a human oversight assessment.

    Attributes
    ----------
    record_id:
        UUID4 — unique identifier for this record.
    domain:
        The domain this record belongs to (e.g. 'general', 'communication',
        'legal', 'banking', 'medical'). Domains may add extra metadata fields
        via `domain_metadata`.
    subject:
        Human-readable description of the decision being assessed.
        Example: "Disability-related complaint response from DBC"
    institution:
        The institution whose decision is being assessed.
    decision_date:
        When the institution's decision was made or communicated.
    assessment_date:
        When this record was created (auto-set to UTC now).
    binary_test:
        The BinaryTest inputs used for this assessment.
    result:
        The BinaryTestResult produced by running the test.
    assessor:
        Who created this record (optional — may be the subject or
        a third-party assessor).
    domain_metadata:
        Domain-specific additional fields (free dict).
    fingerprint:
        SHA-256 of the canonical JSON representation of this record.
        Set automatically by `seal()`. Used to detect tampering.
    signature:
        Reserved for cryptographic signature (Ed25519 / PQC).
        Populate via a signing provider that holds the private key.
    notes:
        Free-text supplementary observations.
    """

    subject: str
    institution: str
    binary_test: BinaryTest
    result: BinaryTestResult

    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    domain: str = "general"
    decision_date: Optional[str] = None
    assessment_date: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    assessor: Optional[str] = None
    domain_metadata: dict[str, Any] = field(default_factory=dict)
    fingerprint: Optional[str] = None
    signature: Optional[str] = None
    notes: Optional[str] = None

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        *,
        subject: str,
        institution: str,
        binary_test: BinaryTest,
        domain: str = "general",
        decision_date: Optional[str] = None,
        assessor: Optional[str] = None,
        domain_metadata: Optional[dict[str, Any]] = None,
        notes: Optional[str] = None,
        ambiguous_if_missing: bool = False,
    ) -> "DecisionRecord":
        """
        Create and seal a DecisionRecord in one call.

        Runs the binary test, constructs the record, and computes
        the fingerprint. The returned record is ready to store or transmit.
        """
        result = binary_test.assess(ambiguous_if_missing=ambiguous_if_missing)
        record = cls(
            subject=subject,
            institution=institution,
            binary_test=binary_test,
            result=result,
            domain=domain,
            decision_date=decision_date,
            assessor=assessor,
            domain_metadata=domain_metadata or {},
            notes=notes,
        )
        record.seal()
        return record

    # ------------------------------------------------------------------
    # Integrity
    # ------------------------------------------------------------------

    def _canonical_dict(self) -> dict[str, Any]:
        """
        Deterministic dict for fingerprinting — excludes the fingerprint
        and signature fields themselves, sorts keys.
        """
        return {
            "record_id": self.record_id,
            "domain": self.domain,
            "subject": self.subject,
            "institution": self.institution,
            "decision_date": self.decision_date,
            "assessment_date": self.assessment_date,
            "assessor": self.assessor,
            "verdict": self.result.verdict.value,
            "score": self.result.score,
            "elements_present": self.result.elements_present,
            "missing_elements": self.result.missing_elements,
            "binary_test": {
                "named_person": self.binary_test.named_person,
                "role_and_authority": self.binary_test.role_and_authority,
                "specific_facts_considered": self.binary_test.specific_facts_considered,
                "pre_decision_timing": self.binary_test.pre_decision_timing,
                "authority_to_differ": self.binary_test.authority_to_differ,
                "context": self.binary_test.context,
            },
            "domain_metadata": self.domain_metadata,
            "notes": self.notes,
        }

    def seal(self) -> None:
        """Compute and store the SHA-256 fingerprint."""
        canonical = json.dumps(self._canonical_dict(), sort_keys=True, ensure_ascii=True)
        self.fingerprint = hashlib.sha256(canonical.encode()).hexdigest()

    def verify_integrity(self) -> bool:
        """
        Return True if the record's content matches its stored fingerprint.
        Returns False if the record has been tampered with or was never sealed.
        """
        if not self.fingerprint:
            return False
        canonical = json.dumps(self._canonical_dict(), sort_keys=True, ensure_ascii=True)
        expected = hashlib.sha256(canonical.encode()).hexdigest()
        return expected == self.fingerprint

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            **self._canonical_dict(),
            "fingerprint": self.fingerprint,
            "signature": self.signature,
            "reasoning": self.result.reasoning,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @property
    def verdict(self) -> Verdict:
        return self.result.verdict

    def __str__(self) -> str:
        return (
            f"DecisionRecord({self.record_id[:8]}…) "
            f"[{self.verdict.value}] "
            f"{self.institution} — {self.subject}"
        )
