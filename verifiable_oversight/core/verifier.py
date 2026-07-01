"""
Verifier — validates DecisionRecord integrity and produces human-readable reports.

The Verifier does three things:
1. Checks that a DecisionRecord's fingerprint matches its content (tamper detection).
2. Validates that a SOVEREIGN record genuinely satisfies all five elements.
3. Generates a structured report suitable for logging, display, or transmission.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional

from .binary_test import Verdict
from .decision_record import DecisionRecord
from .signing import SigningError, verify_record_signature


@dataclass
class VerificationReport:
    record_id: str
    verdict: Verdict
    integrity_ok: bool
    elements_valid: bool
    issues: list[str]
    summary: str
    signature_ok: Optional[bool] = None

    @property
    def is_valid(self) -> bool:
        return self.integrity_ok and self.elements_valid and not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "verdict": self.verdict.value,
            "integrity_ok": self.integrity_ok,
            "elements_valid": self.elements_valid,
            "signature_ok": self.signature_ok,
            "is_valid": self.is_valid,
            "issues": self.issues,
            "summary": self.summary,
        }

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        return f"[{status}] {self.record_id[:8]}… — {self.summary}"


class Verifier:
    """
    Verifies DecisionRecord instances for integrity and logical consistency.

    Usage
    -----
        verifier = Verifier()
        report = verifier.verify(record)
        print(report)
    """

    def verify(self, record: DecisionRecord) -> VerificationReport:
        """Run all verification checks and return a VerificationReport."""
        issues: list[str] = []

        # 1. Fingerprint integrity
        integrity_ok = record.verify_integrity()
        if not integrity_ok:
            if record.fingerprint is None:
                issues.append("Record has not been sealed (no fingerprint).")
            else:
                issues.append(
                    "Fingerprint mismatch — record content has changed since sealing."
                )

        # 2. SOVEREIGN records must have all five elements populated
        elements_valid = True
        if record.verdict == Verdict.SOVEREIGN:
            test = record.binary_test
            if not test.named_person or not test.named_person.strip():
                issues.append("SOVEREIGN verdict requires a named person.")
                elements_valid = False
            if not test.role_and_authority or not test.role_and_authority.strip():
                issues.append("SOVEREIGN verdict requires role and authority to be documented.")
                elements_valid = False
            if not test.specific_facts_considered or not test.specific_facts_considered.strip():
                issues.append("SOVEREIGN verdict requires specific facts to be documented.")
                elements_valid = False
            if not test.pre_decision_timing or not test.pre_decision_timing.strip():
                issues.append("SOVEREIGN verdict requires pre-decision timing confirmation.")
                elements_valid = False
            if not test.authority_to_differ or not test.authority_to_differ.strip():
                issues.append("SOVEREIGN verdict requires authority to differ to be confirmed.")
                elements_valid = False

        # 3. Score consistency
        declared_score = record.result.score
        computed_score = record.binary_test.score
        if declared_score != computed_score:
            issues.append(
                f"Score inconsistency: record declares {declared_score}/5 "
                f"but binary test computes {computed_score}/5."
            )
            elements_valid = False

        # 4. NULL records should have at least one missing element
        if record.verdict == Verdict.NULL and not record.result.missing_elements:
            issues.append("NULL verdict declared but no missing elements recorded.")
            elements_valid = False

        # 5. Signature (optional). Unsigned records remain valid — signing is an
        #    additional guarantee, not a requirement. A signed record whose
        #    signature does not verify is a hard failure.
        signature_ok: Optional[bool] = None
        if record.is_signed:
            try:
                signature_ok = verify_record_signature(record)
            except SigningError as exc:
                signature_ok = False
                issues.append(f"Signature could not be verified: {exc}")
            else:
                if not signature_ok:
                    issues.append(
                        "Signature verification failed — the record is signed but "
                        "the signature does not match its content or public key."
                    )

        summary = self._build_summary(record, issues)
        return VerificationReport(
            record_id=record.record_id,
            verdict=record.verdict,
            integrity_ok=integrity_ok,
            elements_valid=elements_valid,
            issues=issues,
            summary=summary,
            signature_ok=signature_ok,
        )

    def verify_batch(self, records: list[DecisionRecord]) -> list[VerificationReport]:
        return [self.verify(r) for r in records]

    def report_json(self, record: DecisionRecord, indent: int = 2) -> str:
        return json.dumps(self.verify(record).to_dict(), indent=indent)

    def _build_summary(self, record: DecisionRecord, issues: list[str]) -> str:
        if not issues:
            return (
                f"{record.verdict.value} — {record.institution} — "
                f"integrity confirmed, all checks passed."
            )
        return (
            f"{record.verdict.value} — {record.institution} — "
            f"{len(issues)} issue(s): {'; '.join(issues[:2])}"
            + (" …" if len(issues) > 2 else "")
        )
