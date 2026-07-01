"""
Deadline engine — statutory and regulatory response deadlines (Phase 4B).

Accountability has a clock. A complaint that receives no substantive response
within its statutory window is not merely "still open" — the passing of the
deadline is itself an event worth recording. This module turns well-known
statutory / regulatory response windows into computable deadlines so that a
missed deadline can be detected, dated, and (via the record layer) permanently
indexed.

The engine is deliberately small and dependency-free:

- A :class:`DeadlineProfile` describes a named window (e.g. "FCA DISP final
  response — 8 weeks").
- :data:`STANDARD_PROFILES` ships the profiles the Burgess casework relies on.
- :class:`DeadlineEngine` computes a due date from a start date and classifies
  the current position as PENDING / DUE_TODAY / BREACHED.

All date handling uses timezone-aware UTC ``datetime`` internally and accepts
ISO-8601 strings or ``date`` / ``datetime`` objects at the boundary, so callers
never have to reason about naive vs aware datetimes.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from typing import Optional, Union

__all__ = [
    "DeadlineStatus",
    "DeadlineProfile",
    "DeadlineResult",
    "DeadlineEngine",
    "STANDARD_PROFILES",
]


DateInput = Union[str, date, datetime]


class DeadlineStatus(str, Enum):
    """Where 'now' sits relative to a computed deadline."""

    PENDING = "PENDING"        # deadline is in the future
    DUE_TODAY = "DUE_TODAY"    # the deadline falls on the reference date
    BREACHED = "BREACHED"      # the deadline has passed with no resolution


@dataclass(frozen=True)
class DeadlineProfile:
    """
    A named statutory / regulatory response window.

    Attributes
    ----------
    key:
        Machine-readable identifier, e.g. ``'fca_disp_final_response'``.
    label:
        Human-readable name, e.g. ``'FCA DISP final response'``.
    days:
        The length of the window in calendar days.
    basis:
        The statutory / regulatory basis for the window.
    """

    key: str
    label: str
    days: int
    basis: str


# The response windows the Burgess casework relies on. Windows are expressed in
# calendar days; where a rule is stated in weeks or months, the conventional
# working equivalent used in practice is encoded here and documented in `basis`.
STANDARD_PROFILES: dict[str, DeadlineProfile] = {
    "fca_disp_final_response": DeadlineProfile(
        key="fca_disp_final_response",
        label="FCA DISP final response",
        days=56,  # 8 weeks
        basis="FCA DISP 1.6.2R — final response within 8 weeks of a complaint.",
    ),
    "dsar_response": DeadlineProfile(
        key="dsar_response",
        label="DSAR / UK GDPR subject access response",
        days=30,  # one month, conventionally treated as 30 days
        basis="UK GDPR Art 12(3) / DPA 2018 — respond to a DSAR within one month.",
    ),
    "lgsco_response": DeadlineProfile(
        key="lgsco_response",
        label="Local authority complaint response (pre-LGSCO)",
        days=20,  # working-day style window, encoded as calendar days
        basis="Local authority corporate complaints procedure — typical response window.",
    ),
    "ico_complaint_acknowledgement": DeadlineProfile(
        key="ico_complaint_acknowledgement",
        label="ICO complaint acknowledgement",
        days=30,
        basis="ICO service standard — acknowledgement / initial response window.",
    ),
    "ombudsman_response": DeadlineProfile(
        key="ombudsman_response",
        label="Ombudsman response",
        days=28,
        basis="General ombudsman response window used for tracking purposes.",
    ),
    "general_reasonable": DeadlineProfile(
        key="general_reasonable",
        label="General reasonable response period",
        days=28,
        basis="No fixed statutory window — a reasonable period for a substantive reply.",
    ),
}


@dataclass(frozen=True)
class DeadlineResult:
    """
    The outcome of applying a :class:`DeadlineProfile` to a start date.

    Attributes
    ----------
    profile:
        The profile that produced this result.
    start:
        The ISO-8601 date the window started (e.g. the complaint date).
    due:
        The ISO-8601 date the response is due by.
    reference:
        The ISO-8601 reference date the status was computed against ('now').
    status:
        PENDING / DUE_TODAY / BREACHED.
    days_remaining:
        Days from ``reference`` to ``due`` (negative if breached).
    """

    profile: DeadlineProfile
    start: str
    due: str
    reference: str
    status: DeadlineStatus
    days_remaining: int

    @property
    def breached(self) -> bool:
        return self.status is DeadlineStatus.BREACHED

    def to_dict(self) -> dict[str, object]:
        return {
            "profile": self.profile.key,
            "label": self.profile.label,
            "basis": self.profile.basis,
            "start": self.start,
            "due": self.due,
            "reference": self.reference,
            "status": self.status.value,
            "days_remaining": self.days_remaining,
        }

    def __str__(self) -> str:
        return (
            f"[{self.status.value}] {self.profile.label} — due {self.due} "
            f"({self.days_remaining:+d} days from {self.reference})"
        )


def _to_utc_datetime(value: DateInput) -> datetime:
    """Coerce a string / date / datetime into a timezone-aware UTC datetime."""
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, date):
        dt = datetime(value.year, value.month, value.day)
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
        except ValueError as exc:
            raise ValueError(
                f"Could not parse date '{value}' — expected ISO-8601 "
                "(e.g. '2026-06-27' or '2026-06-27T09:00:00Z')."
            ) from exc
    else:
        raise TypeError(f"Unsupported date input type: {type(value)!r}")

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class DeadlineEngine:
    """
    Computes response deadlines from known statutory / regulatory profiles.

    Usage
    -----
        engine = DeadlineEngine()
        result = engine.evaluate(
            "fca_disp_final_response",
            start="2026-01-01",
            reference="2026-04-01",
        )
        result.status        # DeadlineStatus.BREACHED
        result.days_remaining  # negative

    A custom set of profiles may be supplied; otherwise
    :data:`STANDARD_PROFILES` is used.
    """

    def __init__(
        self, profiles: Optional[dict[str, DeadlineProfile]] = None
    ) -> None:
        self._profiles = dict(profiles) if profiles is not None else dict(
            STANDARD_PROFILES
        )

    # ------------------------------------------------------------------
    # Profile management
    # ------------------------------------------------------------------

    @property
    def profiles(self) -> dict[str, DeadlineProfile]:
        return dict(self._profiles)

    def register_profile(self, profile: DeadlineProfile) -> None:
        """Add or replace a deadline profile."""
        self._profiles[profile.key] = profile

    def get_profile(self, key: str) -> DeadlineProfile:
        try:
            return self._profiles[key]
        except KeyError as exc:
            known = ", ".join(sorted(self._profiles)) or "(none)"
            raise KeyError(
                f"Unknown deadline profile '{key}'. Known profiles: {known}."
            ) from exc

    # ------------------------------------------------------------------
    # Computation
    # ------------------------------------------------------------------

    def due_date(self, profile_key: str, start: DateInput) -> str:
        """Return the ISO date a response is due, given a start date."""
        profile = self.get_profile(profile_key)
        start_dt = _to_utc_datetime(start)
        due_dt = start_dt + timedelta(days=profile.days)
        return due_dt.date().isoformat()

    def evaluate(
        self,
        profile_key: str,
        *,
        start: DateInput,
        reference: Optional[DateInput] = None,
    ) -> DeadlineResult:
        """
        Evaluate a deadline for ``profile_key`` starting at ``start``.

        ``reference`` is the date to judge against ('now'); it defaults to the
        current UTC date. The result carries the due date, the status
        (PENDING / DUE_TODAY / BREACHED) and the signed number of days
        remaining (negative once breached).
        """
        profile = self.get_profile(profile_key)
        start_dt = _to_utc_datetime(start)
        ref_dt = (
            _to_utc_datetime(reference)
            if reference is not None
            else datetime.now(timezone.utc)
        )
        due_dt = start_dt + timedelta(days=profile.days)

        start_day = start_dt.date()
        ref_day = ref_dt.date()
        due_day = due_dt.date()
        days_remaining = (due_day - ref_day).days

        if days_remaining > 0:
            status = DeadlineStatus.PENDING
        elif days_remaining == 0:
            status = DeadlineStatus.DUE_TODAY
        else:
            status = DeadlineStatus.BREACHED

        return DeadlineResult(
            profile=profile,
            start=start_day.isoformat(),
            due=due_day.isoformat(),
            reference=ref_day.isoformat(),
            status=status,
            days_remaining=days_remaining,
        )
