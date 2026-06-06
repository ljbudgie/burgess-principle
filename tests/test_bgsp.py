"""Tests for the Burgess Git Sovereignty Protocol helper (``bgsp.py``)."""

from __future__ import annotations

import hashlib
from pathlib import Path

import bgsp

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "examples" / "decision-ledger"


# --- payload digest --------------------------------------------------------

def test_payload_digest_is_canonical_and_deterministic():
    digest = bgsp.payload_digest(subject="s", facts="f", action="a")
    expected = hashlib.sha256(
        '{"action":"a","facts":"f","subject":"s"}'.encode("utf-8")
    ).hexdigest()
    assert digest == expected


def test_payload_digest_matches_anchor_canonicalisation():
    # Must agree with the framework-wide canonicalisation used elsewhere.
    from iris.anchor import canonical_json_sha256

    obj = {"action": "x", "facts": "y", "subject": "z"}
    assert bgsp.payload_digest(subject="z", facts="y", action="x") == canonical_json_sha256(obj)


# --- parsing ---------------------------------------------------------------

def test_parse_extracts_type_scope_and_trailers():
    msg = bgsp.draft_commit_message(
        scope="openhear",
        subject="subject:openhear:1",
        action="Approve fitting",
        facts="audiogram; consent",
        summary="approve fitting",
    )
    commit = bgsp.parse_commit_message(msg)
    assert commit.commit_type == "burgess"
    assert commit.scope == "openhear"
    assert commit.summary == "approve fitting"
    assert commit.subject == "subject:openhear:1"
    for trailer in bgsp.REQUIRED_TRAILERS:
        assert trailer in commit.trailers


def test_parse_parent_none_normalises_to_python_none():
    commit = bgsp.parse_commit_message("burgess: x\n\nBurgess-Parent: none\n")
    assert commit.parent is None
    commit2 = bgsp.parse_commit_message("burgess: x\n\nBurgess-Parent: abc123\n")
    assert commit2.parent == "abc123"


# --- classification: NULL by default ---------------------------------------

def _sovereign_message(parent: str = "none") -> str:
    return bgsp.draft_commit_message(
        scope="openhear",
        subject="subject:openhear:1",
        action="Approve fitting",
        facts="audiogram; consent",
        summary="approve fitting",
        authority="Dr A. Reviewer, audiologist",
        parent=parent,
        classification=bgsp.SOVEREIGN,
    )


def test_unsigned_commit_is_null():
    commit = bgsp.parse_commit_message(_sovereign_message(), signature_status="N")
    assert classify_result(commit) == bgsp.NULL


def test_bad_signature_is_null():
    commit = bgsp.parse_commit_message(
        _sovereign_message(), signature_status="B", signer="Dr A. Reviewer"
    )
    assert classify_result(commit) == bgsp.NULL


def test_bot_signer_is_null_even_with_good_signature():
    commit = bgsp.parse_commit_message(
        _sovereign_message(), signature_status="G", signer="github-actions[bot]"
    )
    assert classify_result(commit) == bgsp.NULL


def test_good_human_signature_is_sovereign():
    commit = bgsp.parse_commit_message(
        _sovereign_message(), signature_status="G", signer="Dr A. Reviewer"
    )
    assert classify_result(commit) == bgsp.SOVEREIGN


def test_classification_claim_null_stays_null():
    msg = bgsp.draft_commit_message(
        scope="x",
        subject="s",
        action="a",
        facts="f",
        summary="s",
        classification=bgsp.NULL,
    )
    commit = bgsp.parse_commit_message(msg, signature_status="G", signer="A Human")
    assert classify_result(commit) == bgsp.NULL


def test_missing_required_trailer_is_null():
    commit = bgsp.parse_commit_message(
        "burgess: x\n\nBurgess-Classification: SOVEREIGN\n",
        signature_status="G",
        signer="A Human",
    )
    assert classify_result(commit) == bgsp.NULL


def test_invalid_payload_digest_is_null():
    msg = _sovereign_message().replace(
        bgsp.payload_digest(subject="subject:openhear:1", facts="audiogram; consent", action="Approve fitting"),
        "not-a-real-digest",
    )
    commit = bgsp.parse_commit_message(msg, signature_status="G", signer="A Human")
    assert classify_result(commit) == bgsp.NULL


def test_payload_recompute_mismatch_is_null():
    commit = bgsp.parse_commit_message(_sovereign_message(), signature_status="G", signer="A Human")
    wrong = {"subject": "subject:openhear:1", "facts": "different facts", "action": "Approve fitting"}
    assert bgsp.classify(commit, known_payload=wrong).result == bgsp.NULL


def test_payload_recompute_match_is_sovereign():
    commit = bgsp.parse_commit_message(_sovereign_message(), signature_status="G", signer="A Human")
    right = {"subject": "subject:openhear:1", "facts": "audiogram; consent", "action": "Approve fitting"}
    assert bgsp.classify(commit, known_payload=right).result == bgsp.SOVEREIGN


def classify_result(commit: bgsp.BurgessCommit) -> str:
    return bgsp.classify(commit).result


# --- nullity propagation ---------------------------------------------------

def test_nullity_propagates_to_unattested_child():
    null_parent = bgsp.parse_commit_message(
        _sovereign_message().replace("SOVEREIGN", "NULL"),
        signature_status="N",
    )
    # Child is itself signed but does NOT re-attest (its claim is NULL too here).
    child = bgsp.parse_commit_message(
        _sovereign_message().replace("Burgess-Classification: SOVEREIGN", "Burgess-Classification: NULL"),
        signature_status="G",
        signer="A Human",
    )
    results = bgsp.propagate_nullity([null_parent, child])
    assert results[0][1].result == bgsp.NULL
    assert results[1][1].result == bgsp.NULL


def test_sovereign_reattestation_heals_chain():
    null_parent = bgsp.parse_commit_message(
        "burgess: auto\n\nBurgess-Classification: NULL\n", signature_status="N"
    )
    healer = bgsp.parse_commit_message(
        _sovereign_message(), signature_status="G", signer="A Human"
    )
    results = bgsp.propagate_nullity([null_parent, healer])
    assert results[0][1].result == bgsp.NULL
    assert results[1][1].result == bgsp.SOVEREIGN


# --- example decision ledger -----------------------------------------------

def test_example_ledger_null_commit():
    commit = bgsp._load_commit_from_file(str(LEDGER / "01-null-automated-credit.commit"))
    assert bgsp.classify(commit).result == bgsp.NULL


def test_example_ledger_openhear_is_sovereign():
    commit = bgsp._load_commit_from_file(str(LEDGER / "02-sovereign-openhear-fitting.commit"))
    assert bgsp.classify(commit).result == bgsp.SOVEREIGN


def test_example_ledger_institutional_reattestation_is_sovereign():
    commit = bgsp._load_commit_from_file(str(LEDGER / "03-sovereign-institutional-reattestation.commit"))
    assert bgsp.classify(commit).result == bgsp.SOVEREIGN


def test_example_ledger_payload_digests_match_facts():
    # Every example commit's committed digest must recompute from its own
    # stated "Facts considered" + Burgess-Action.
    for name in (
        "01-null-automated-credit.commit",
        "02-sovereign-openhear-fitting.commit",
        "03-sovereign-institutional-reattestation.commit",
    ):
        commit = bgsp._load_commit_from_file(str(LEDGER / name))
        facts = commit.body.split("Facts considered:", 1)[-1].strip() if "Facts considered:" in commit.body else commit.body.strip()
        recomputed = bgsp.payload_digest(
            subject=commit.subject or "",
            facts=facts,
            action=commit.trailers["Burgess-Action"],
        )
        assert recomputed == commit.payload_sha256, name


# --- CLI -------------------------------------------------------------------

def test_cli_check_returns_nonzero_for_null(capsys):
    rc = bgsp.main(["check", str(LEDGER / "01-null-automated-credit.commit")])
    assert rc == 1
    assert "NULL" in capsys.readouterr().out


def test_cli_check_returns_zero_for_sovereign(capsys):
    rc = bgsp.main(["check", str(LEDGER / "02-sovereign-openhear-fitting.commit")])
    assert rc == 0
    assert "SOVEREIGN" in capsys.readouterr().out


def test_cli_draft_is_null_and_parseable(capsys):
    rc = bgsp.main(
        [
            "draft",
            "--scope", "openhear",
            "--subject", "subject:openhear:1",
            "--action", "Approve fitting",
            "--facts", "audiogram; consent",
            "--summary", "approve fitting",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    commit = bgsp.parse_commit_message(out, signature_status="N")
    assert commit.classification_claim == bgsp.NULL  # draft is NULL until signed
    assert bgsp.classify(commit).result == bgsp.NULL


def test_git_backed_unsigned_commit_is_null(tmp_path):
    import subprocess

    def git(*args):
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    git("init", "-q")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test Human")
    git("config", "commit.gpgsign", "false")
    msg = _sovereign_message()
    git("commit", "--allow-empty", "-q", "-m", msg)
    cwd = Path.cwd()
    try:
        import os

        os.chdir(tmp_path)
        commit = bgsp.load_commit_from_git("HEAD")
    finally:
        os.chdir(cwd)
    # Unsigned => NULL regardless of a SOVEREIGN claim in the trailers.
    assert commit.signature_status in {"N", "E", "B"}
    assert bgsp.classify(commit).result == bgsp.NULL


def test_cli_digest_matches_helper(capsys):
    rc = bgsp.main(
        ["digest", "--subject", "s", "--action", "a", "--facts", "f"]
    )
    assert rc == 0
    out = capsys.readouterr().out.strip()
    assert out == bgsp.payload_digest(subject="s", facts="f", action="a")
