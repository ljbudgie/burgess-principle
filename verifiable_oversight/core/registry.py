"""
Institution registry — a lookup of the bodies whose decisions are assessed (Phase 4B).

The same institution recurs across many interactions, under many spellings
("DBC", "Durham County Council", "Durham CC"). An :class:`InstitutionRegistry`
gives each institution one canonical entry that records:

- its canonical name and any aliases,
- its sector / type (e.g. local_authority, bank, regulator, ombudsman),
- the regulatory framework it answers to,
- whether a reasonable adjustment (RA) is on record with it, and its description,
- the default statutory response deadline profile that applies to it.

This lets the rest of the system resolve a free-text institution name to a
canonical record, and pair an institution with the right deadline profile from
:mod:`verifiable_oversight.core.deadlines`.

Registry lookup is case-insensitive and alias-aware, but never fuzzy: an
unknown name resolves to ``None`` rather than guessing, because misattributing
an accountability finding to the wrong body is worse than not resolving it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator, Optional

__all__ = [
    "Institution",
    "InstitutionRegistry",
]


def _normalise(name: str) -> str:
    """Case- and whitespace-insensitive key for name/alias lookup."""
    return " ".join(name.strip().lower().split())


@dataclass(frozen=True)
class Institution:
    """
    A canonical record of an institution whose decisions are assessed.

    Attributes
    ----------
    name:
        The canonical institution name.
    sector:
        Sector / type, e.g. 'local_authority', 'bank', 'regulator',
        'ombudsman', 'healthcare', 'enforcement'.
    aliases:
        Alternative names / abbreviations that resolve to this institution.
    regulatory_framework:
        The framework the institution answers to (e.g. 'FCA DISP', 'LGSCO').
    ra_on_record:
        Whether a reasonable adjustment is on record with this institution.
    ra_description:
        Description of the RA (e.g. 'email-only communication').
    deadline_profile:
        The default deadline profile key (see
        :data:`verifiable_oversight.core.deadlines.STANDARD_PROFILES`).
    notes:
        Free-text notes.
    """

    name: str
    sector: str = "unknown"
    aliases: tuple[str, ...] = field(default_factory=tuple)
    regulatory_framework: Optional[str] = None
    ra_on_record: bool = False
    ra_description: Optional[str] = None
    deadline_profile: Optional[str] = None
    notes: Optional[str] = None

    def all_names(self) -> tuple[str, ...]:
        """The canonical name plus every alias."""
        return (self.name, *self.aliases)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "sector": self.sector,
            "aliases": list(self.aliases),
            "regulatory_framework": self.regulatory_framework,
            "ra_on_record": self.ra_on_record,
            "ra_description": self.ra_description,
            "deadline_profile": self.deadline_profile,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Institution":
        return cls(
            name=data["name"],
            sector=data.get("sector", "unknown"),
            aliases=tuple(data.get("aliases") or ()),
            regulatory_framework=data.get("regulatory_framework"),
            ra_on_record=bool(data.get("ra_on_record", False)),
            ra_description=data.get("ra_description"),
            deadline_profile=data.get("deadline_profile"),
            notes=data.get("notes"),
        )


class InstitutionRegistry:
    """
    A case-insensitive, alias-aware registry of institutions.

    Usage
    -----
        registry = InstitutionRegistry()
        registry.register(Institution(
            name="Durham County Council",
            sector="local_authority",
            aliases=("DBC", "Durham CC"),
            deadline_profile="lgsco_response",
            ra_on_record=True,
            ra_description="email-only communication",
        ))
        registry.resolve("dbc")            # -> the Institution
        registry.resolve("unknown body")  # -> None
    """

    def __init__(self, institutions: Optional[list[Institution]] = None) -> None:
        self._by_name: dict[str, Institution] = {}
        self._index: dict[str, Institution] = {}
        for inst in institutions or []:
            self.register(inst)

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, institution: Institution, *, replace: bool = False) -> None:
        """
        Register an institution.

        Raises ``ValueError`` if the canonical name or any alias already maps to
        a *different* institution, unless ``replace=True``. Registering the same
        institution again (identical canonical name) with ``replace=True``
        overwrites the previous entry and its aliases.
        """
        canonical_key = _normalise(institution.name)

        if not replace:
            for key in map(_normalise, institution.all_names()):
                existing = self._index.get(key)
                if existing is not None and _normalise(existing.name) != canonical_key:
                    raise ValueError(
                        f"Name/alias '{key}' already registered to "
                        f"'{existing.name}'. Use replace=True to override."
                    )
        else:
            # Drop any prior entry (and its aliases) for this canonical name.
            prior = self._by_name.get(canonical_key)
            if prior is not None:
                for key in map(_normalise, prior.all_names()):
                    self._index.pop(key, None)

        self._by_name[canonical_key] = institution
        for key in map(_normalise, institution.all_names()):
            self._index[key] = institution

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def resolve(self, name: str) -> Optional[Institution]:
        """Resolve a free-text name or alias to an Institution, or ``None``."""
        return self._index.get(_normalise(name))

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and _normalise(name) in self._index

    def __len__(self) -> int:
        return len(self._by_name)

    def __iter__(self) -> Iterator[Institution]:
        return iter(self._by_name.values())

    def all(self) -> list[Institution]:
        """Return all registered institutions (registration order not guaranteed)."""
        return list(self._by_name.values())

    def by_sector(self, sector: str) -> list[Institution]:
        """Return all institutions in a given sector."""
        target = sector.strip().lower()
        return [i for i in self._by_name.values() if i.sector.lower() == target]

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_list(self) -> list[dict[str, Any]]:
        return [i.to_dict() for i in self._by_name.values()]

    @classmethod
    def from_list(cls, data: list[dict[str, Any]]) -> "InstitutionRegistry":
        return cls([Institution.from_dict(d) for d in data])
