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
        Ed25519 signature (hex) over the fingerprint, produced by a
        RecordSigner. Populated by `verifiable_oversight.core.signing`.
        Lives outside the canonical fingerprint, so signing never changes
        the fingerprint and unsigned records are unaffected.
    public_key:
        Ed25519 public key (hex) corresponding to `signature`. Published so
        third parties can verify the signature independently and offline.
    signed_at:
        UTC ISO-8601 timestamp of when the signature was applied.
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
    public_key: Optional[str] = None
    signed_at: Optional[str] = None
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DecisionRecord":
        """
        Reconstruct a DecisionRecord from its ``to_dict()`` representation.

        This is the inverse of :meth:`to_dict` and is used by the storage
        layer to rehydrate persisted records. The stored fingerprint and
        signature fields are restored **verbatim** — the record is *not*
        resealed — so that :meth:`verify_integrity` and signature checks
        remain meaningful: if the persisted content was altered on disk,
        integrity verification will fail rather than silently pass.

        Parameters
        ----------
        data:
            A mapping produced by :meth:`to_dict` (or a compatible JSON
            object). Missing optional keys default to ``None`` / empty.
        """
        bt = data.get("binary_test") or {}
        binary_test = BinaryTest(
            named_person=bt.get("named_person"),
            role_and_authority=bt.get("role_and_authority"),
            specific_facts_considered=bt.get("specific_facts_considered"),
            pre_decision_timing=bt.get("pre_decision_timing"),
            authority_to_differ=bt.get("authority_to_differ"),
            context=bt.get("context"),
        )
        result = BinaryTestResult(
            verdict=Verdict(data["verdict"]),
            score=data["score"],
            elements_present=dict(data.get("elements_present") or {}),
            missing_elements=list(data.get("missing_elements") or []),
            reasoning=data.get("reasoning", ""),
        )
        record = cls(
            subject=data["subject"],
            institution=data["institution"],
            binary_test=binary_test,
            result=result,
            record_id=data.get("record_id", str(uuid.uuid4())),
            domain=data.get("domain", "general"),
            decision_date=data.get("decision_date"),
            assessor=data.get("assessor"),
            domain_metadata=dict(data.get("domain_metadata") or {}),
            fingerprint=data.get("fingerprint"),
            signature=data.get("signature"),
            public_key=data.get("public_key"),
            signed_at=data.get("signed_at"),
            notes=data.get("notes"),
        )
        # Restore the original assessment timestamp rather than "now".
        if data.get("assessment_date"):
            record.assessment_date = data["assessment_date"]
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
            "public_key": self.public_key,
            "signed_at": self.signed_at,
            "reasoning": self.result.reasoning,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @property
    def verdict(self) -> Verdict:
        return self.result.verdict

    @property
    def is_signed(self) -> bool:
        """True if the record carries both a signature and a public key."""
        return bool(self.signature and self.public_key)

    def __str__(self) -> str:
        return (
            f"DecisionRecord({self.record_id[:8]}…) "
            f"[{self.verdict.value}] "
            f"{self.institution} — {self.subject}"
        )
