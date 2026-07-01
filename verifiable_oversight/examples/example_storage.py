"""
Example: RECORD STORAGE — an append-only oversight ledger (Phase 3)

Scenario: an individual assesses a sequence of institutional decisions over time
and commits each finding to a durable, append-only ledger. Months later — before
a tribunal, an ombudsman, or an internal review — the whole history can be
replayed and independently verified:

  * every record still matches its own SHA-256 fingerprint (nothing was altered),
  * the ledger's hash chain is intact (nothing was inserted, reordered, or
    removed), and
  * records can be retrieved by fingerprint and filtered by verdict/institution.

The store is stdlib-only and writes JSON-Lines (one record per line), so the
ledger is human-readable, greppable, and trivially transmittable.

No external dependency is required to run this example.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import (
    BinaryTest,
    RecordStore,
    Verdict,
    Verifier,
)
from verifiable_oversight.domains import CommunicationDomain


def main() -> None:
    domain = CommunicationDomain()
    verifier = Verifier()

    # Use a throwaway ledger file for the demo.
    ledger_path = os.path.join(tempfile.mkdtemp(), "oversight-ledger.jsonl")
    store = RecordStore(ledger_path)

    # 1. A NULL finding — no named individual across four responses.
    null_record = domain.create_record(
        subject="Fourth response — circular referral to EHRC",
        institution="EASS",
        binary_test=BinaryTest(
            context="Four responses. No named individual, role, or authority.",
        ),
        channel="email",
        ra_on_record=True,
        ra_description="email-only communication",
        channel_accessible=False,
    )

    # 2. A SOVEREIGN finding — a named human with authority reviewed the facts.
    sovereign_record = domain.create_record(
        subject="Named caseworker confirmed review before decision",
        institution="LGO",
        binary_test=BinaryTest(
            named_person="Rebecca Hunt",
            role_and_authority="Investigator, authority to uphold or reject",
            specific_facts_considered="Reviewed the specific complaint file",
            pre_decision_timing="Reviewed before the decision issued",
            authority_to_differ="Empowered to reach a different outcome",
            context="Named review confirmed in writing.",
        ),
        channel="letter",
        ra_on_record=False,
    )

    store.append(null_record)
    store.append(sovereign_record)

    print("=" * 60)
    print("APPEND-ONLY OVERSIGHT LEDGER")
    print("=" * 60)
    print("Ledger file:", ledger_path)
    print("Entries:    ", len(store))
    print("Head hash:  ", store.head_hash[:32] + "…")
    print("Verdicts:   ", store.counts_by_verdict())
    print()

    # Retrieve a record by its fingerprint.
    fp = null_record.fingerprint
    fetched = store.get(fp)
    print("Lookup by fingerprint:", fp[:16] + "…")
    print("  ->", fetched)
    print()

    # Filter by verdict.
    print("NULL findings in the ledger:")
    for record in store.find(verdict=Verdict.NULL):
        print("  -", record)
    print()

    # Verify the whole chain, and each record independently.
    print("Chain intact:", store.verify_chain())
    for report in verifier.verify_batch(store.all()):
        print(" ", report)
    print()

    # Re-open the ledger from disk — it loads and re-verifies automatically.
    reopened = RecordStore(ledger_path)
    print("Re-opened ledger entries:", len(reopened))
    print("Re-opened chain intact:  ", reopened.verify_chain())
    print("Same record retrievable: ", reopened.get(fp) is not None)


if __name__ == "__main__":
    main()
