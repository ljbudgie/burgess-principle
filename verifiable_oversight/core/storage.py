"""
Record storage — an append-only, tamper-evident ledger for DecisionRecords (Phase 3).

A single assessment is useful. A *chain* of assessments is accountability
infrastructure: a durable, ordered log of every SOVEREIGN/NULL finding that can
be replayed, audited, and independently verified long after the conversation
that produced it.

This module provides :class:`RecordStore`, a file-backed append-only log with
three properties:

1. **Append-only** — records are only ever added, never edited or deleted
   in place. Each record is written as one line of JSON (JSON-Lines / ``.jsonl``).
2. **Keyed by fingerprint** — every record is indexed by its SHA-256
   fingerprint. The same finding cannot be appended twice, and any record can
   be retrieved by fingerprint in one lookup.
3. **Tamper-evident chain** — each entry stores the hash of the previous
   entry, forming a hash chain over the whole ledger. Altering, reordering, or
   removing any past entry breaks the chain, which :meth:`RecordStore.verify_chain`
   detects — over and above each record's own fingerprint/signature checks.

Design notes
------------
* **stdlib only.** Persistence uses ``json`` + the filesystem; the chain uses
  ``hashlib``. No third-party dependency is required to store or read records.
  (Signing individual records still uses the optional PyNaCl dependency, exactly
  as in Phase 2 — storage is agnostic to whether a record is signed.)
* **The record's own fingerprint is preserved verbatim.** Records are rehydrated
  via :meth:`DecisionRecord.from_dict`, which does *not* reseal them, so on-disk
  tampering with a record's content is caught by ``verify_integrity`` and the
  chain hash independently.
* **The chain hash is separate from the record fingerprint.** The record
  fingerprint commits to a record's content; the chain hash commits to a
  record's *position in the ledger*. Keeping them separate means signing a
  record never affects the chain, and building the chain never changes a
  record's fingerprint.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Optional, Union

from .binary_test import Verdict
from .decision_record import DecisionRecord

__all__ = [
    "CHAIN_CONTEXT",
    "GENESIS_HASH",
    "StorageError",
    "LedgerEntry",
    "RecordStore",
    "compute_entry_hash",
]

# Domain-separation prefix for the ledger hash chain. Bumping the version
# deliberately invalidates chains built under the old context, so the meaning
# of a chain hash is unambiguous and cannot be confused with a record
# fingerprint or a signing message.
CHAIN_CONTEXT = "burgess-oversight/record-ledger/v1"

# The "previous hash" of the very first entry in a ledger.
GENESIS_HASH = "0" * 64


class StorageError(RuntimeError):
    """Raised when the ledger is malformed, corrupt, or misused."""


def compute_entry_hash(
    *, sequence: int, previous_hash: str, fingerprint: str
) -> str:
    """
    Deterministically compute the chain hash for a single ledger entry.

    The hash binds an entry's position (``sequence``), the entry before it
    (``previous_hash``), and the record it carries (``fingerprint``), under a
    versioned, domain-separated context. Any change to any of these breaks the
    chain from this entry onward.
    """
    message = f"{CHAIN_CONTEXT}:{sequence}:{previous_hash}:{fingerprint}"
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class LedgerEntry:
    """
    One line of the append-only ledger: a record plus its chain metadata.

    Attributes
    ----------
    sequence:
        Zero-based position of this entry in the ledger.
    previous_hash:
        The ``entry_hash`` of the preceding entry, or ``GENESIS_HASH`` for the
        first entry.
    entry_hash:
        This entry's chain hash — see :func:`compute_entry_hash`.
    record:
        The rehydrated :class:`DecisionRecord`.
    """

    sequence: int
    previous_hash: str
    entry_hash: str
    record: DecisionRecord

    @property
    def fingerprint(self) -> Optional[str]:
        return self.record.fingerprint

    def to_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
            "record": self.record.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LedgerEntry":
        try:
            record = DecisionRecord.from_dict(data["record"])
            return cls(
                sequence=int(data["sequence"]),
                previous_hash=str(data["previous_hash"]),
                entry_hash=str(data["entry_hash"]),
                record=record,
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise StorageError(f"Malformed ledger entry: {exc}") from exc


class RecordStore:
    """
    An append-only, fingerprint-keyed, hash-chained ledger of DecisionRecords.

    Usage
    -----
        store = RecordStore("oversight-ledger.jsonl")
        entry = store.append(record)      # returns the LedgerEntry
        store.get(record.fingerprint)     # retrieve by fingerprint
        store.verify_chain()              # confirm the ledger is intact

    A ``RecordStore`` may be backed by a file (records persist across processes)
    or held purely in memory (``path=None`` — useful for tests and transient
    use). File-backed stores load any existing ledger on construction and
    verify its chain, refusing to operate on a corrupt ledger.
    """

    def __init__(self, path: Optional[Union[str, os.PathLike[str]]] = None):
        self._path: Optional[Path] = Path(path) if path is not None else None
        self._entries: list[LedgerEntry] = []
        self._by_fingerprint: dict[str, LedgerEntry] = {}
        if self._path is not None and self._path.exists():
            self._load()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def path(self) -> Optional[Path]:
        return self._path

    @property
    def head_hash(self) -> str:
        """The chain hash of the most recent entry (``GENESIS_HASH`` if empty)."""
        return self._entries[-1].entry_hash if self._entries else GENESIS_HASH

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[DecisionRecord]:
        return (entry.record for entry in self._entries)

    def __contains__(self, fingerprint: object) -> bool:
        return fingerprint in self._by_fingerprint

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def append(self, record: DecisionRecord) -> LedgerEntry:
        """
        Append a sealed DecisionRecord to the ledger.

        The record must already be sealed (have a fingerprint) and must have
        valid integrity — you cannot commit a tampered or unsealed record to
        the ledger. Appending is idempotent-safe against accidental exact
        duplicates: a fingerprint already present raises :class:`StorageError`.

        Returns the created :class:`LedgerEntry`.
        """
        if not record.fingerprint:
            raise StorageError(
                "Cannot append an unsealed record — call DecisionRecord.create() "
                "or record.seal() first."
            )
        if not record.verify_integrity():
            raise StorageError(
                "Cannot append a record whose content does not match its "
                "fingerprint (integrity check failed)."
            )
        if record.fingerprint in self._by_fingerprint:
            raise StorageError(
                f"Record with fingerprint {record.fingerprint[:12]}… is already "
                "in the ledger; the append-only ledger does not store duplicates."
            )

        sequence = len(self._entries)
        previous_hash = self.head_hash
        entry_hash = compute_entry_hash(
            sequence=sequence,
            previous_hash=previous_hash,
            fingerprint=record.fingerprint,
        )
        entry = LedgerEntry(
            sequence=sequence,
            previous_hash=previous_hash,
            entry_hash=entry_hash,
            record=record,
        )

        if self._path is not None:
            self._append_line(entry)

        self._entries.append(entry)
        self._by_fingerprint[record.fingerprint] = entry
        return entry

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def get(self, fingerprint: str) -> Optional[DecisionRecord]:
        """Return the record with this fingerprint, or ``None`` if absent."""
        entry = self._by_fingerprint.get(fingerprint)
        return entry.record if entry else None

    def get_entry(self, fingerprint: str) -> Optional[LedgerEntry]:
        """Return the ledger entry for this fingerprint, or ``None``."""
        return self._by_fingerprint.get(fingerprint)

    def get_by_record_id(self, record_id: str) -> Optional[DecisionRecord]:
        """Return the first record with this ``record_id``, or ``None``."""
        for entry in self._entries:
            if entry.record.record_id == record_id:
                return entry.record
        return None

    def all(self) -> list[DecisionRecord]:
        """Return all records in append order."""
        return [entry.record for entry in self._entries]

    def entries(self) -> list[LedgerEntry]:
        """Return all ledger entries (record + chain metadata) in append order."""
        return list(self._entries)

    def find(
        self,
        *,
        institution: Optional[str] = None,
        verdict: Optional[Union[Verdict, str]] = None,
        domain: Optional[str] = None,
    ) -> list[DecisionRecord]:
        """
        Return records matching all supplied filters (append order).

        ``verdict`` accepts either a :class:`Verdict` or its string value
        (e.g. ``"NULL"``). Omitted filters are ignored.
        """
        wanted_verdict = Verdict(verdict) if verdict is not None else None
        results: list[DecisionRecord] = []
        for entry in self._entries:
            record = entry.record
            if institution is not None and record.institution != institution:
                continue
            if wanted_verdict is not None and record.verdict != wanted_verdict:
                continue
            if domain is not None and record.domain != domain:
                continue
            results.append(record)
        return results

    def counts_by_verdict(self) -> dict[str, int]:
        """Return a ``{verdict: count}`` tally across the whole ledger."""
        tally: dict[str, int] = {v.value: 0 for v in Verdict}
        for entry in self._entries:
            tally[entry.record.verdict.value] += 1
        return tally

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verify_chain(self) -> bool:
        """
        Return True if the ledger is internally consistent and untampered.

        Checks, for every entry in order, that:

        * the sequence numbers are contiguous from zero,
        * each entry's ``previous_hash`` matches the prior entry's hash,
        * each entry's ``entry_hash`` is the correct hash of its contents, and
        * each carried record still matches its own fingerprint (integrity).

        Any failure means the ledger has been altered, reordered, or truncated.
        """
        previous_hash = GENESIS_HASH
        for index, entry in enumerate(self._entries):
            if entry.sequence != index:
                return False
            if entry.previous_hash != previous_hash:
                return False
            if not entry.record.fingerprint or not entry.record.verify_integrity():
                return False
            expected = compute_entry_hash(
                sequence=entry.sequence,
                previous_hash=entry.previous_hash,
                fingerprint=entry.record.fingerprint,
            )
            if entry.entry_hash != expected:
                return False
            previous_hash = entry.entry_hash
        return True

    # ------------------------------------------------------------------
    # Persistence internals
    # ------------------------------------------------------------------

    def _append_line(self, entry: LedgerEntry) -> None:
        assert self._path is not None
        self._path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(entry.to_dict(), ensure_ascii=False, sort_keys=True)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    def _load(self) -> None:
        assert self._path is not None
        entries: list[LedgerEntry] = []
        by_fingerprint: dict[str, LedgerEntry] = {}
        with self._path.open("r", encoding="utf-8") as handle:
            for lineno, raw in enumerate(handle, start=1):
                stripped = raw.strip()
                if not stripped:
                    continue
                try:
                    data = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise StorageError(
                        f"Corrupt ledger at {self._path} line {lineno}: {exc}"
                    ) from exc
                entry = LedgerEntry.from_dict(data)
                fp = entry.record.fingerprint
                if fp and fp in by_fingerprint:
                    raise StorageError(
                        f"Duplicate fingerprint {fp[:12]}… at {self._path} "
                        f"line {lineno}; the ledger is corrupt."
                    )
                if fp:
                    by_fingerprint[fp] = entry
                entries.append(entry)

        self._entries = entries
        self._by_fingerprint = by_fingerprint
        if not self.verify_chain():
            raise StorageError(
                f"Ledger at {self._path} failed chain verification on load — "
                "it has been altered, reordered, or truncated."
            )

    def rewrite(self, destination: Union[str, os.PathLike[str]]) -> None:
        """
        Write the current ledger to ``destination`` atomically.

        This does not mutate existing entries — it re-serialises the in-memory
        ledger to a new file (or the same path) via a temp-file-and-rename, so a
        crash mid-write cannot leave a half-written ledger. Useful for
        compaction or relocating a store; the chain is preserved exactly.
        """
        dest = Path(destination)
        dest.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=str(dest.parent), suffix=".jsonl.tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                for entry in self._entries:
                    line = json.dumps(
                        entry.to_dict(), ensure_ascii=False, sort_keys=True
                    )
                    handle.write(line + "\n")
            os.replace(tmp_name, dest)
        except BaseException:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
            raise
