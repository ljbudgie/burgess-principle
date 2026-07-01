"""Tests for verifiable_oversight Phase 4B — institution registry + deadline engine."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from verifiable_oversight import (
    Institution,
    InstitutionRegistry,
    DeadlineEngine,
    DeadlineProfile,
    DeadlineStatus,
    STANDARD_PROFILES,
)


# ---------------------------------------------------------------------------
# Institution registry
# ---------------------------------------------------------------------------

def _registry() -> InstitutionRegistry:
    return InstitutionRegistry([
        Institution(
            name="Durham County Council",
            sector="local_authority",
            aliases=("DBC", "Durham CC"),
            deadline_profile="lgsco_response",
            ra_on_record=True,
            ra_description="email-only communication",
        ),
        Institution(name="Example Bank plc", sector="bank", aliases=("ExBank",)),
    ])


def test_resolve_by_canonical_name():
    assert _registry().resolve("Durham County Council").sector == "local_authority"


def test_resolve_is_case_insensitive():
    assert _registry().resolve("durham county council") is not None


def test_resolve_by_alias():
    r = _registry()
    assert r.resolve("DBC").name == "Durham County Council"
    assert r.resolve("dbc").name == "Durham County Council"


def test_resolve_unknown_returns_none_not_guess():
    assert _registry().resolve("Some Other Council") is None


def test_contains_and_len():
    r = _registry()
    assert "DBC" in r
    assert "nope" not in r
    assert len(r) == 2


def test_by_sector():
    banks = _registry().by_sector("bank")
    assert [i.name for i in banks] == ["Example Bank plc"]


def test_duplicate_alias_raises():
    r = _registry()
    with pytest.raises(ValueError):
        r.register(Institution(name="Other", aliases=("DBC",)))


def test_replace_overwrites_and_clears_old_aliases():
    r = _registry()
    r.register(
        Institution(name="Durham County Council", sector="local_authority",
                    aliases=("DCC",)),
        replace=True,
    )
    assert r.resolve("DCC") is not None
    # Old alias no longer resolves after replace.
    assert r.resolve("DBC") is None


def test_registry_roundtrip_serialisation():
    r = _registry()
    restored = InstitutionRegistry.from_list(r.to_list())
    assert restored.resolve("DBC").name == "Durham County Council"
    assert len(restored) == len(r)


def test_all_names_includes_aliases():
    inst = Institution(name="X", aliases=("Y", "Z"))
    assert inst.all_names() == ("X", "Y", "Z")


# ---------------------------------------------------------------------------
# Deadline engine
# ---------------------------------------------------------------------------

def test_standard_profiles_present():
    assert "fca_disp_final_response" in STANDARD_PROFILES
    assert STANDARD_PROFILES["fca_disp_final_response"].days == 56


def test_due_date_computed():
    engine = DeadlineEngine()
    assert engine.due_date("dsar_response", "2026-06-01") == "2026-07-01"


def test_breached_when_past_due():
    engine = DeadlineEngine()
    result = engine.evaluate(
        "fca_disp_final_response", start="2026-01-01", reference="2026-04-01"
    )
    assert result.status is DeadlineStatus.BREACHED
    assert result.breached is True
    assert result.days_remaining < 0


def test_pending_when_before_due():
    engine = DeadlineEngine()
    result = engine.evaluate(
        "dsar_response", start="2026-06-01", reference="2026-06-15"
    )
    assert result.status is DeadlineStatus.PENDING
    assert result.days_remaining == 16


def test_due_today_boundary():
    engine = DeadlineEngine()
    result = engine.evaluate(
        "dsar_response", start="2026-06-01", reference="2026-07-01"
    )
    assert result.status is DeadlineStatus.DUE_TODAY
    assert result.days_remaining == 0


def test_evaluate_accepts_datetime_strings_with_z():
    engine = DeadlineEngine()
    result = engine.evaluate(
        "dsar_response",
        start="2026-06-01T09:00:00Z",
        reference="2026-06-10T09:00:00Z",
    )
    assert result.status is DeadlineStatus.PENDING


def test_unknown_profile_raises():
    engine = DeadlineEngine()
    with pytest.raises(KeyError):
        engine.evaluate("no_such_profile", start="2026-01-01")


def test_bad_date_raises_valueerror():
    engine = DeadlineEngine()
    with pytest.raises(ValueError):
        engine.evaluate("dsar_response", start="not-a-date")


def test_register_custom_profile():
    engine = DeadlineEngine()
    engine.register_profile(
        DeadlineProfile(key="custom", label="Custom", days=10, basis="test")
    )
    assert engine.due_date("custom", "2026-01-01") == "2026-01-11"


def test_result_to_dict_roundtrip_fields():
    engine = DeadlineEngine()
    result = engine.evaluate(
        "dsar_response", start="2026-06-01", reference="2026-06-15"
    )
    d = result.to_dict()
    assert d["profile"] == "dsar_response"
    assert d["status"] == "PENDING"
    assert d["days_remaining"] == 16


def test_default_reference_is_now(monkeypatch):
    # With no reference, a long-past start is breached against 'now'.
    engine = DeadlineEngine()
    result = engine.evaluate("dsar_response", start="2000-01-01")
    assert result.status is DeadlineStatus.BREACHED
