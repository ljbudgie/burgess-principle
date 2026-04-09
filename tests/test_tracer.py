"""Tests for the TRACER defect schema library."""

import pytest

from tracer import DEFECT_SCHEMA, get_defect, list_defects


# ---------------------------------------------------------------------------
# Schema integrity
# ---------------------------------------------------------------------------

class TestDefectSchema:
    def test_schema_is_non_empty(self):
        assert len(DEFECT_SCHEMA) > 0

    def test_all_defects_have_required_keys(self):
        required_keys = {"id", "title", "description", "axiom"}
        for defect in DEFECT_SCHEMA:
            assert required_keys.issubset(defect.keys()), (
                f"Defect {defect.get('id', '???')} is missing keys: "
                f"{required_keys - defect.keys()}"
            )

    def test_defect_ids_are_unique(self):
        ids = [d["id"] for d in DEFECT_SCHEMA]
        assert len(ids) == len(set(ids)), "Duplicate defect IDs found"

    def test_defect_ids_follow_naming_convention(self):
        for defect in DEFECT_SCHEMA:
            assert defect["id"].startswith("DEFECT_"), (
                f"ID {defect['id']} does not start with 'DEFECT_'"
            )

    def test_all_values_are_non_empty_strings(self):
        for defect in DEFECT_SCHEMA:
            for key in ("id", "title", "description", "axiom"):
                assert isinstance(defect[key], str), (
                    f"{defect['id']}.{key} is not a string"
                )
                assert defect[key].strip(), (
                    f"{defect['id']}.{key} is empty"
                )


# ---------------------------------------------------------------------------
# get_defect
# ---------------------------------------------------------------------------

class TestGetDefect:
    def test_returns_matching_defect(self):
        defect = get_defect("DEFECT_01")
        assert defect is not None
        assert defect["id"] == "DEFECT_01"
        assert defect["title"] == "Bulk Approval Without Scrutiny"

    def test_returns_none_for_unknown_id(self):
        assert get_defect("DEFECT_99") is None

    def test_returns_none_for_empty_string(self):
        assert get_defect("") is None

    def test_each_known_defect_is_retrievable(self):
        for defect_id in list_defects():
            assert get_defect(defect_id) is not None


# ---------------------------------------------------------------------------
# list_defects
# ---------------------------------------------------------------------------

class TestListDefects:
    def test_returns_list_of_strings(self):
        ids = list_defects()
        assert isinstance(ids, list)
        assert all(isinstance(i, str) for i in ids)

    def test_count_matches_schema(self):
        assert len(list_defects()) == len(DEFECT_SCHEMA)

    def test_known_defects_present(self):
        ids = list_defects()
        assert "DEFECT_01" in ids
        assert "DEFECT_04" in ids
