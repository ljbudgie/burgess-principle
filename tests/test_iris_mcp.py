"""Tests for the Iris MCP server."""

import asyncio
import hashlib

import pytest

pytest.importorskip("mcp")

import iris_mcp  # noqa: E402


def test_tools_are_registered():
    names = {tool.name for tool in asyncio.run(iris_mcp.mcp.list_tools())}
    assert names == {
        "assess_decision",
        "classify_correspondence",
        "verify_reasoning_hash",
        "lookup_organisation",
        "register_summary",
        "certification_mark_status",
    }


def test_assess_decision_sovereign_and_null():
    ok = iris_mcp.assess_decision(
        reviewer_name="Alice Example",
        reviewer_role="Appeals officer",
        specific_facts_reviewed=True,
        review_timing="before_action",
    )
    assert ok["status"] == "SOVEREIGN"
    assert "advisory" in ok
    assert iris_mcp.assess_decision()["status"] == "AMBIGUOUS"
    refused = iris_mcp.assess_decision(
        reviewer_name="Team", reviewer_role="Collections", specific_facts_reviewed=False
    )
    assert refused["status"] == "NULL"


def test_verify_reasoning_hash():
    text = "The officer reviewed the tenancy file on 3 March."
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert iris_mcp.verify_reasoning_hash(text, digest)["status"] == "SOVEREIGN"
    assert iris_mcp.verify_reasoning_hash(text, "0" * 64)["status"] == "NULL"


def test_lookup_returns_organisation_fields_only():
    result = iris_mcp.lookup_organisation("E.ON")
    assert result["match_count"] >= 1
    for row in result["matches"]:
        assert set(row) == set(iris_mcp.PUBLIC_REGISTER_FIELDS)
        assert row["Finding"].upper() != "REMOVED"


def test_lookup_rejects_short_queries():
    assert iris_mcp.lookup_organisation("e")["matches"] == []


def test_register_summary_counts_add_up():
    summary = iris_mcp.register_summary()
    assert sum(summary["totals"].values()) == summary["organisations"]


def test_mark_is_registered_not_pending():
    facts = iris_mcp.certification_mark_status()
    assert facts["status"] == "registered"
    assert facts["registered_date"] == "2026-10-09"


def test_classify_correspondence_runs():
    result = iris_mcp.classify_correspondence(
        [
            {"date": "2026-10-01", "sender": "Me", "direction": "individual",
             "content_summary": "Please reply by email."},
            {"date": "2026-10-05", "sender": "Council", "direction": "institution",
             "content_summary": "Please call us on our helpline."},
        ],
        institution="Council",
    )
    assert "loop_detected" in result
    assert "advisory" in result
