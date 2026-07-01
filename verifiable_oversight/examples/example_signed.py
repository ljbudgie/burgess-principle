"""
Example: SIGNED decision record — cryptographic non-repudiation (Phase 2)

Scenario: the same NULL finding as example_null.py, but this time the assessor
signs the sealed record with an Ed25519 key. The signature and public key travel
with the record, so anyone — a tribunal, an ombudsman, an opposing institution —
can verify OFFLINE that:

  1. the record's content still matches its fingerprint (nothing was altered), and
  2. the fingerprint was signed by the holder of the published public key.

The SHA-256 fingerprint alone proves the record has not changed. The signature
proves WHO produced it. Together they make the finding independently verifiable
without any shared secret or trusted third party.

Requires PyNaCl:  pip install PyNaCl
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import (
    BinaryTest,
    RecordSigner,
    Verifier,
    verify_record_signature,
)
from verifiable_oversight.domains import CommunicationDomain


def main() -> None:
    domain = CommunicationDomain()

    record = domain.create_record(
        subject="Fourth response — circular referral to EHRC post-whistleblowing",
        institution="EASS (Equality Advisory Support Service)",
        binary_test=BinaryTest(
            named_person=None,
            role_and_authority=None,
            specific_facts_considered=None,
            pre_decision_timing=None,
            authority_to_differ=None,
            context=(
                "Four responses across the thread. No named individual, role, or "
                "authority confirmed. No evidence the specific facts were reviewed "
                "before the response was sent."
            ),
        ),
        decision_date="2026-06-27",
        assessor="Lewis James Burgess",
        channel="email (with telephone number provided)",
        ra_on_record=True,
        ra_description="email-only communication",
        channel_accessible=False,
        regulatory_framework="EA 2010 ss.20/21; EHRC enforcement framework",
    )

    # In production the private key would be held securely (hardware token, KMS,
    # or the CRYPTOGRAPHIC_IDENTITY.md architecture). Here we generate one.
    signer = RecordSigner.generate()
    signer.sign(record)

    verifier = Verifier()
    report = verifier.verify(record)

    print("=" * 60)
    print("SIGNED DECISION RECORD")
    print("=" * 60)
    print(record)
    print()
    print("VERDICT:      ", record.verdict.value)
    print("FINGERPRINT:  ", (record.fingerprint or "")[:32] + "…")
    print("PUBLIC KEY:   ", record.public_key)
    print("SIGNATURE:    ", (record.signature or "")[:32] + "…")
    print("SIGNED AT:    ", record.signed_at)
    print()
    print("Independent signature check:", verify_record_signature(record))
    print()
    print("VERIFICATION REPORT:")
    print(report)
    print("  integrity_ok:", report.integrity_ok)
    print("  signature_ok:", report.signature_ok)
    print("  is_valid:    ", report.is_valid)
    print()

    # Demonstrate tamper-evidence: change one field after signing.
    record.subject = "Altered after signing"
    tampered = verifier.verify(record)
    print("After altering the record:")
    print("  signature verifies:", verify_record_signature(record))
    print("  report is_valid:   ", tampered.is_valid)


if __name__ == "__main__":
    main()
