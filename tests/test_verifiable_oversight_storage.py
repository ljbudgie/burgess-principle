"""Tests for verifiable_oversight Phase 3 — append-only record storage.

Covers append semantics, fingerprint keying, retrieval and filtering,
persistence round-trips, the tamper-evident hash chain, and error handling.
"""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from verifiable_oversight import (
    BinaryTest,
    DecisionRecord,
    GENESIS_HASH,
    LedgerEntry,
    RecordStore,
    StorageError,
    Verdict,
    compute_entry_hash,
)


def _null_record(subject: str = "Fourth response — circular referral") -> DecisionRecord:
    return DecisionRecord.create(
        subject=subject,
        institution="EASS",
        binary_test=BinaryTest(context="No named individual across four responses."),
    )


def _sovereign_record(subject: str = "Named review confirmed") -> DecisionRecord:
    return DecisionRecord.create(
        subject=subject,
        institution="LGO",
        binary_test=BinaryTest(
            named_person="Rebecca Hunt",
            role_and_authority="Investigator with authority to differ",
            specific_facts_considered="Reviewed the specific complaint file",
            pre_decision_timing="Reviewed before the decision issued",
            authority_to_differ="Empowered to reach a different outcome",
        ),
    )


# ---------------------------------------------------------------------------
# from_dict round-trip
# ---------------------------------------------------------------------------


def test_from_dict_round_trips_and_preserves_fingerprint():
    record = _sovereign_record()
    restored = DecisionRecord.from_dict(record.to_dict())

    assert restored.record_id == record.record_id
    assert restored.fingerprint == record.fingerprint
    assert restored.verdict == record.verdict == Verdict.SOVEREIGN
    assert restored.assessment_date == record.assessment_date
    assert restored.binary_test.named_person == "Rebecca Hunt"
    # Preserved fingerprint means integrity verifies without resealing.
    assert restored.verify_integrity() is True


def test_from_dict_detects_tampered_content():
    record = _null_record()
    data = record.to_dict()
    data["subject"] = "Altered subject"  # fingerprint no longer matches
    restored = DecisionRecord.from_dict(data)
    assert restored.verify_integrity() is False


# ---------------------------------------------------------------------------
# In-memory store: append + retrieval
# ---------------------------------------------------------------------------


def test_append_returns_entry_and_updates_length():
    store = RecordStore()
    assert len(store) == 0
    assert store.head_hash == GENESIS_HASH

    record = _null_record()
    entry = store.append(record)

    assert isinstance(entry, LedgerEntry)
    assert entry.sequence == 0
    assert entry.previous_hash == GENESIS_HASH
    assert len(store) == 1
    assert store.head_hash == entry.entry_hash


def test_get_by_fingerprint_and_record_id():
    store = RecordStore()
    record = _null_record()
    store.append(record)

    assert store.get(record.fingerprint) is record
    assert store.get_by_record_id(record.record_id) is record
    assert record.fingerprint in store
    assert store.get("nonexistent") is None
    assert store.get_by_record_id("nonexistent") is None


def test_iteration_and_all_preserve_append_order():
    store = RecordStore()
    r1 = _null_record("first")
    r2 = _sovereign_record("second")
    store.append(r1)
    store.append(r2)

    assert store.all() == [r1, r2]
    assert list(store) == [r1, r2]


def test_append_rejects_unsealed_record():
    store = RecordStore()
    record = _null_record()
    record.fingerprint = None
    with pytest.raises(StorageError):
        store.append(record)


def test_append_rejects_tampered_record():
    store = RecordStore()
    record = _null_record()
    record.subject = "Altered after sealing"  # breaks integrity
    with pytest.raises(StorageError):
        store.append(record)


def test_append_rejects_duplicate_fingerprint():
    store = RecordStore()
    record = _null_record()
    store.append(record)
    with pytest.raises(StorageError):
        store.append(record)


# ---------------------------------------------------------------------------
# Filtering / tallies
# ---------------------------------------------------------------------------


def test_find_filters_by_verdict_institution_domain():
    store = RecordStore()
    null_r = _null_record()
    sov_r = _sovereign_record()
    store.append(null_r)
    store.append(sov_r)

    assert store.find(verdict=Verdict.NULL) == [null_r]
    assert store.find(verdict="SOVEREIGN") == [sov_r]
    assert store.find(institution="EASS") == [null_r]
    assert store.find(domain="general") == [null_r, sov_r]
    assert store.find(institution="EASS", verdict=Verdict.SOVEREIGN) == []


def test_counts_by_verdict():
    store = RecordStore()
    store.append(_null_record("a"))
    store.append(_null_record("b"))
    store.append(_sovereign_record("c"))

    counts = store.counts_by_verdict()
    assert counts["NULL"] == 2
    assert counts["SOVEREIGN"] == 1
    assert counts["AMBIGUOUS"] == 0


# ---------------------------------------------------------------------------
# Hash chain
# ---------------------------------------------------------------------------


def test_chain_links_entries():
    store = RecordStore()
    e0 = store.append(_null_record("a"))
    e1 = store.append(_sovereign_record("b"))

    assert e0.previous_hash == GENESIS_HASH
    assert e1.previous_hash == e0.entry_hash
    assert e1.sequence == 1
    assert store.verify_chain() is True


def test_compute_entry_hash_matches_stored_hash():
    store = RecordStore()
    entry = store.append(_null_record())
    expected = compute_entry_hash(
        sequence=entry.sequence,
        previous_hash=entry.previous_hash,
        fingerprint=entry.record.fingerprint,
    )
    assert entry.entry_hash == expected


def test_verify_chain_detects_record_tampering():
    store = RecordStore()
    store.append(_null_record())
    # Mutate the carried record after it is committed.
    store.entries()[0].record.subject = "Altered in the ledger"
    assert store.verify_chain() is False


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def test_persistence_round_trip(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    store = RecordStore(ledger)
    r1 = _null_record()
    r2 = _sovereign_record()
    store.append(r1)
    store.append(r2)

    reopened = RecordStore(ledger)
    assert len(reopened) == 2
    assert reopened.verify_chain() is True
    assert reopened.get(r1.fingerprint) is not None
    assert reopened.get(r2.fingerprint).verdict == Verdict.SOVEREIGN
    assert reopened.head_hash == store.head_hash


def test_file_is_json_lines_append_only(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    store = RecordStore(ledger)
    store.append(_null_record())
    store.append(_sovereign_record())

    lines = [ln for ln in ledger.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(lines) == 2
    for lineno, raw in enumerate(lines):
        obj = json.loads(raw)
        assert obj["sequence"] == lineno
        assert "record" in obj and "entry_hash" in obj


def test_load_rejects_corrupt_chain(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    store = RecordStore(ledger)
    store.append(_null_record())
    store.append(_sovereign_record())

    # Corrupt the first entry's record content on disk.
    lines = ledger.read_text(encoding="utf-8").splitlines()
    first = json.loads(lines[0])
    first["record"]["subject"] = "Tampered on disk"
    lines[0] = json.dumps(first)
    ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with pytest.raises(StorageError):
        RecordStore(ledger)


def test_load_rejects_malformed_json(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text("this is not json\n", encoding="utf-8")
    with pytest.raises(StorageError):
        RecordStore(ledger)


def test_rewrite_is_atomic_and_preserves_chain(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    store = RecordStore(ledger)
    store.append(_null_record())
    store.append(_sovereign_record())

    dest = tmp_path / "copy" / "ledger.jsonl"
    store.rewrite(dest)

    copy = RecordStore(dest)
    assert len(copy) == 2
    assert copy.verify_chain() is True
    assert copy.head_hash == store.head_hash


def test_empty_existing_file_loads_as_empty(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_text("\n\n", encoding="utf-8")
    store = RecordStore(ledger)
    assert len(store) == 0
    assert store.verify_chain() is True
