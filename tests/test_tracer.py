"""Tests for the TRACER defect schema library."""

import pytest

from tracer import DEFECT_SCHEMA, Defect, get_defect, list_defects
import tracer


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

    def test_schema_has_exactly_four_defects(self):
        assert len(DEFECT_SCHEMA) == 4

    def test_defect_ids_are_sequential(self):
        ids = [d["id"] for d in DEFECT_SCHEMA]
        expected = [f"DEFECT_{i:02d}" for i in range(1, len(ids) + 1)]
        assert ids == expected

    def test_schema_contains_only_dicts(self):
        for defect in DEFECT_SCHEMA:
            assert isinstance(defect, dict)

    def test_defects_have_no_extra_keys(self):
        allowed_keys = {"id", "title", "description", "axiom"}
        for defect in DEFECT_SCHEMA:
            extra = set(defect.keys()) - allowed_keys
            assert not extra, (
                f"Defect {defect['id']} has unexpected keys: {extra}"
            )


# ---------------------------------------------------------------------------
# Specific defect content
# ---------------------------------------------------------------------------

class TestDefectContent:
    def test_defect_01_content(self):
        defect = get_defect("DEFECT_01")
        assert defect is not None
        assert defect["title"] == "Bulk Approval Without Scrutiny"
        assert "batch" in defect["description"].lower()

    def test_defect_02_content(self):
        defect = get_defect("DEFECT_02")
        assert defect is not None
        assert defect["title"] == "Rubber-Stamping"
        assert "affidavit" in defect["description"].lower()

    def test_defect_03_content(self):
        defect = get_defect("DEFECT_03")
        assert defect is not None
        assert defect["title"] == "Procedural Lies / Errors"
        assert "fraud" in defect["axiom"].lower()

    def test_defect_04_content(self):
        defect = get_defect("DEFECT_04")
        assert defect is not None
        assert defect["title"] == "Downstream Taint Propagation"
        assert "corrupted" in defect["axiom"].lower()


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

    def test_returns_reference_from_schema(self):
        """get_defect returns the same dict object from DEFECT_SCHEMA."""
        defect = get_defect("DEFECT_01")
        assert defect is DEFECT_SCHEMA[0]

    def test_case_sensitive_lookup(self):
        assert get_defect("defect_01") is None
        assert get_defect("Defect_01") is None

    def test_partial_id_returns_none(self):
        assert get_defect("DEFECT_") is None
        assert get_defect("DEFECT") is None

    def test_returns_none_for_numeric_suffix_only(self):
        assert get_defect("01") is None

    def test_all_four_defects_retrievable(self):
        for i in range(1, 5):
            defect_id = f"DEFECT_{i:02d}"
            defect = get_defect(defect_id)
            assert defect is not None
            assert defect["id"] == defect_id


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

    def test_preserves_schema_order(self):
        ids = list_defects()
        schema_ids = [d["id"] for d in DEFECT_SCHEMA]
        assert ids == schema_ids

    def test_returns_new_list_each_call(self):
        ids1 = list_defects()
        ids2 = list_defects()
        assert ids1 == ids2
        assert ids1 is not ids2

    def test_all_four_ids_present(self):
        ids = list_defects()
        for i in range(1, 5):
            assert f"DEFECT_{i:02d}" in ids


# ---------------------------------------------------------------------------
# Module exports (__init__.py)
# ---------------------------------------------------------------------------

class TestModuleExports:
    def test_all_exports(self):
        assert set(tracer.__all__) == {
            "DEFECT_SCHEMA", "Defect", "get_defect", "list_defects",
        }

    def test_defect_type_exported(self):
        assert tracer.Defect is Defect

    def test_defect_schema_exported(self):
        assert tracer.DEFECT_SCHEMA is DEFECT_SCHEMA

    def test_get_defect_exported(self):
        assert tracer.get_defect is get_defect

    def test_list_defects_exported(self):
        assert tracer.list_defects is list_defects
