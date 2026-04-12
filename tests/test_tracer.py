"""Tests for the TRACER defect schema library."""

import pytest

from tracer import (
    DEFECT_SCHEMA,
    Defect,
    TraceFinding,
    TraceReport,
    build_trace_finding,
    build_trace_report,
    get_defect,
    list_defects,
)
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
# build_trace_finding
# ---------------------------------------------------------------------------

class TestBuildTraceFinding:
    def test_returns_structured_finding_for_known_id(self):
        finding = build_trace_finding(
            "DEFECT_01",
            evidence="Batch warrant ledger",
            notes="Escalate for human review",
        )

        assert finding == {
            "defect_id": "DEFECT_01",
            "title": "Bulk Approval Without Scrutiny",
            "description": (
                "Warrants processed in batches without individual judicial review."
            ),
            "axiom": (
                "Violates 'The Judicial Mind.' If a judge did not scrutinize the "
                "specific facts of the individual case, the resulting data is a 0 (NULL)."
            ),
            "evidence": "Batch warrant ledger",
            "notes": "Escalate for human review",
        }

    def test_returns_empty_evidence_and_notes_by_default(self):
        finding = build_trace_finding("DEFECT_02")
        assert finding is not None
        assert finding["evidence"] == ""
        assert finding["notes"] == ""

    def test_returns_none_for_unknown_id(self):
        assert build_trace_finding("DEFECT_99") is None


# ---------------------------------------------------------------------------
# build_trace_report
# ---------------------------------------------------------------------------

class TestBuildTraceReport:
    def test_builds_report_for_multiple_defects(self):
        report = build_trace_report(
            ["DEFECT_01", "DEFECT_03"],
            reasoning="Two independent defects were documented.",
            evidence_by_id={
                "DEFECT_01": "Batch processing record",
                "DEFECT_03": "False gas leak claim",
            },
            notes_by_id={"DEFECT_03": "Source statement conflicts with site notes"},
            generated_at="2026-04-12T12:44:19+00:00",
        )

        assert report["generated_at"] == "2026-04-12T12:44:19+00:00"
        assert report["reasoning"] == "Two independent defects were documented."
        assert report["defect_ids"] == ["DEFECT_01", "DEFECT_03"]
        assert [finding["defect_id"] for finding in report["findings"]] == [
            "DEFECT_01",
            "DEFECT_03",
        ]
        assert report["findings"][0]["evidence"] == "Batch processing record"
        assert report["findings"][1]["notes"] == (
            "Source statement conflicts with site notes"
        )

    def test_accepts_single_defect_id_string(self):
        report = build_trace_report("DEFECT_04")
        assert report["defect_ids"] == ["DEFECT_04"]
        assert len(report["findings"]) == 1

    def test_raises_for_unknown_defect(self):
        with pytest.raises(ValueError, match="Unknown defect ID: DEFECT_99"):
            build_trace_report(["DEFECT_01", "DEFECT_99"])


# ---------------------------------------------------------------------------
# Module exports (__init__.py)
# ---------------------------------------------------------------------------

class TestModuleExports:
    def test_all_exports(self):
        assert set(tracer.__all__) == {
            "DEFECT_SCHEMA",
            "Defect",
            "TraceFinding",
            "TraceReport",
            "build_trace_finding",
            "build_trace_report",
            "get_defect",
            "list_defects",
        }

    def test_defect_type_exported(self):
        assert tracer.Defect is Defect

    def test_trace_types_exported(self):
        assert tracer.TraceFinding is TraceFinding
        assert tracer.TraceReport is TraceReport

    def test_defect_schema_exported(self):
        assert tracer.DEFECT_SCHEMA is DEFECT_SCHEMA

    def test_trace_helpers_exported(self):
        assert tracer.build_trace_finding is build_trace_finding
        assert tracer.build_trace_report is build_trace_report

    def test_get_defect_exported(self):
        assert tracer.get_defect is get_defect

    def test_list_defects_exported(self):
        assert tracer.list_defects is list_defects


# ---------------------------------------------------------------------------
# get_defect — edge cases
# ---------------------------------------------------------------------------

class TestGetDefectEdgeCases:
    def test_none_input_returns_none(self):
        # get_defect iterates and compares; None won't match any ID string
        assert get_defect(None) is None  # type: ignore[arg-type]

    def test_integer_input_returns_none(self):
        assert get_defect(1) is None  # type: ignore[arg-type]

    def test_whitespace_id_returns_none(self):
        assert get_defect("  ") is None

    def test_id_with_trailing_space_returns_none(self):
        assert get_defect("DEFECT_01 ") is None

    def test_id_with_leading_space_returns_none(self):
        assert get_defect(" DEFECT_01") is None

    def test_lowercase_full_id_returns_none(self):
        assert get_defect("defect_01") is None

    def test_get_defect_does_not_modify_schema(self):
        original_len = len(DEFECT_SCHEMA)
        get_defect("DEFECT_01")
        get_defect("DEFECT_99")
        assert len(DEFECT_SCHEMA) == original_len


# ---------------------------------------------------------------------------
# Defect TypedDict
# ---------------------------------------------------------------------------

class TestDefectTypedDict:
    def test_defect_can_be_instantiated(self):
        d: Defect = {
            "id": "TEST_01",
            "title": "Test",
            "description": "Test description",
            "axiom": "Test axiom",
        }
        assert d["id"] == "TEST_01"
        assert d["title"] == "Test"

    def test_defect_schema_items_match_type(self):
        """Every item in DEFECT_SCHEMA is a valid Defect dict."""
        for defect in DEFECT_SCHEMA:
            assert isinstance(defect["id"], str)
            assert isinstance(defect["title"], str)
            assert isinstance(defect["description"], str)
            assert isinstance(defect["axiom"], str)

    def test_trace_types_can_be_instantiated(self):
        finding: TraceFinding = {
            "defect_id": "DEFECT_01",
            "title": "Bulk Approval Without Scrutiny",
            "description": "Example",
            "axiom": "Example axiom",
            "evidence": "Example evidence",
            "notes": "Example notes",
        }
        report: TraceReport = {
            "generated_at": "2026-04-12T12:44:19+00:00",
            "reasoning": "Example reasoning",
            "defect_ids": ["DEFECT_01"],
            "findings": [finding],
        }

        assert report["findings"][0]["defect_id"] == "DEFECT_01"


# ---------------------------------------------------------------------------
# Defect axiom content
# ---------------------------------------------------------------------------

class TestDefectAxiomContent:
    def test_defect_01_axiom_mentions_judicial_mind(self):
        defect = get_defect("DEFECT_01")
        assert defect is not None
        assert "judicial mind" in defect["axiom"].lower()

    def test_defect_02_axiom_mentions_processing_center(self):
        defect = get_defect("DEFECT_02")
        assert defect is not None
        assert "processing center" in defect["axiom"].lower()

    def test_defect_03_axiom_mentions_fraud(self):
        defect = get_defect("DEFECT_03")
        assert defect is not None
        assert "fraud" in defect["axiom"].lower()

    def test_defect_04_axiom_mentions_corrupted(self):
        defect = get_defect("DEFECT_04")
        assert defect is not None
        assert "corrupted" in defect["axiom"].lower()

    def test_all_defects_have_substantive_axioms(self):
        # Axioms should be meaningful sentences, not just a few words
        min_axiom_length = 10
        for defect in DEFECT_SCHEMA:
            assert len(defect["axiom"].strip()) > min_axiom_length, (
                f"{defect['id']} axiom is too short"
            )
