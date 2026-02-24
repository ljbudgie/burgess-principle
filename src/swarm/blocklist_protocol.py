"""
BlocklistProtocol — Tracks organisations ("bad actors") by sector for the
Burgess Principle defense system.

Records are kept in memory (and optionally persisted to a JSON file) and are
grouped by sector: Energy, Water, and Council.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

SECTORS = ("energy", "water", "council")


@dataclass
class BadActorRecord:
    """A single entry in the blocklist."""

    name: str
    sector: str
    reason: str
    added: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "sector": self.sector,
            "reason": self.reason,
            "added": self.added,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BadActorRecord":
        return cls(
            name=data["name"],
            sector=data["sector"],
            reason=data["reason"],
            added=data.get("added", ""),
        )


class BlocklistProtocol:
    """Maintains a registry of bad actors grouped by sector.

    Parameters
    ----------
    persist_path:
        Optional filesystem path for JSON persistence.  If supplied the
        blocklist is loaded on construction and saved after every mutation.
    """

    def __init__(self, persist_path: Optional[str] = None) -> None:
        self._persist_path = persist_path
        self._records: Dict[str, List[BadActorRecord]] = {s: [] for s in SECTORS}
        if persist_path and os.path.isfile(persist_path):
            self._load(persist_path)

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def add(self, name: str, sector: str, reason: str) -> BadActorRecord:
        """Add an organisation to the blocklist.

        Parameters
        ----------
        name:   Organisation name.
        sector: One of ``"energy"``, ``"water"``, or ``"council"``.
        reason: Short description of the alleged violation.

        Raises
        ------
        ValueError
            If *sector* is not recognised.
        """
        sector = sector.lower()
        self._validate_sector(sector)
        record = BadActorRecord(name=name, sector=sector, reason=reason)
        self._records[sector].append(record)
        self._save()
        return record

    def remove(self, name: str, sector: str) -> bool:
        """Remove an organisation from the blocklist.

        Returns ``True`` if an entry was removed, ``False`` otherwise.
        """
        sector = sector.lower()
        self._validate_sector(sector)
        before = len(self._records[sector])
        self._records[sector] = [
            r for r in self._records[sector] if r.name.lower() != name.lower()
        ]
        removed = len(self._records[sector]) < before
        if removed:
            self._save()
        return removed

    def get_by_sector(self, sector: str) -> List[BadActorRecord]:
        """Return all records for a given sector."""
        sector = sector.lower()
        self._validate_sector(sector)
        return list(self._records[sector])

    def get_all(self) -> Dict[str, List[BadActorRecord]]:
        """Return a copy of the full blocklist, keyed by sector."""
        return {s: list(records) for s, records in self._records.items()}

    def is_blocked(self, name: str, sector: Optional[str] = None) -> bool:
        """Return ``True`` if *name* appears in the blocklist.

        If *sector* is given, only that sector is searched; otherwise all
        sectors are checked.
        """
        sectors = [sector.lower()] if sector else list(SECTORS)
        for s in sectors:
            if any(r.name.lower() == name.lower() for r in self._records[s]):
                return True
        return False

    def summary(self) -> Dict[str, int]:
        """Return the count of blocked organisations per sector."""
        return {s: len(records) for s, records in self._records.items()}

    # ------------------------------------------------------------------ #
    #  Persistence helpers                                                 #
    # ------------------------------------------------------------------ #

    def _save(self) -> None:
        if not self._persist_path:
            return
        data = {
            sector: [r.to_dict() for r in records]
            for sector, records in self._records.items()
        }
        with open(self._persist_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    def _load(self, path: str) -> None:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        for sector in SECTORS:
            if sector in data:
                self._records[sector] = [
                    BadActorRecord.from_dict(item) for item in data[sector]
                ]

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _validate_sector(sector: str) -> None:
        if sector not in SECTORS:
            raise ValueError(
                f"Unknown sector '{sector}'. Must be one of: {', '.join(SECTORS)}"
            )
