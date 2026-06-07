"""Tests for the Burgess Sovereign Exit Protocol helper (``tools/bgsp-exit.py``).

BSEP applies the BGSP signed-commit SOVEREIGN / NULL primitive to the act of
leaving a system. These tests cover the two-axis classification (sovereignty +
completeness), the lawful-use guardrails, nullity healing, ledger verification,
notice templates, and the Clean Break Certificate.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import bgsp

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER = REPO_ROOT / "examples" / "sovereign-exit-ledger"


def _load_bgsp_exit():
    spec = importlib.util.spec_from_file_location(
        "bgsp_exit", REPO_ROOT / "tools" / "bgsp-exit.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    import sys

    sys.modules["bgsp_exit"] = module
    spec.loader.exec_module(module)
    return module


bx = _load_bgsp_exit()


# --- helpers ----------------------------------------------------------------

def _exit_message(
    *,
    obligations: str = "settled",
    notice: str = "ref ACME-77213",
    classification: str = bgsp.SOVEREIGN,
    heals: str = "none",
    exit_type: str = "utility",
    parent: str = "none",
) -> str:
    return bx.draft_exit_commit_message(
        scope="acme",
        subject="subject:energy:1",
        system="Acme Energy — domestic account",
        exit_type=exit_type,
        action="Close energy account on switch",
        facts="switch confirmed; final readings; settled",
        summary="leave Acme Energy",
        obligations=obligations,
        notice=notice,
        effective="2026-06-30",
        heals=heals,
        parent=parent,
        classification=classification,
    )


def _signed(msg: str, signer: str = "Robin Hale") -> "bgsp.BurgessCommit":
    return bx.parse_exit_commit(msg, signature_status="G", signer=signer)


# --- drafting ---------------------------------------------------------------

def test_draft_is_null_until_signed_and_parseable():
    msg = bx.draft_exit_commit_message(
        scope="acme",
        subject="subject:energy:1",
        system="Acme Energy",
        exit_type="utility",
        action="Close account",
        facts="settled",
        summary="leave acme",
    )
    commit = bx.parse_exit_commit(msg, signature_status="N")
    assert commit.commit_type == "burgess"
    assert commit.scope == "acme"
    assert commit.classification_claim == bgsp.NULL  # NULL until a human signs
    assert bx.classify_exit(commit).sovereignty == bgsp.NULL


def test_draft_includes_all_required_exit_trailers():
    commit = bx.parse_exit_commit(_exit_message())
    for trailer in bx.REQUIRED_EXIT_TRAILERS:
        assert trailer in commit.trailers
    for trailer in bgsp.REQUIRED_TRAILERS:
        assert trailer in commit.trailers


def test_draft_default_scope_is_exit():
    msg = bx.draft_exit_commit_message(
        scope="",
        subject="s",
        system="Sys",
        exit_type="platform",
        action="a",
        facts="f",
        summary="leave",
    )
    assert msg.splitlines()[0].startswith("burgess(exit):")


def test_draft_cosigners_trailer_present_when_given():
    msg = bx.draft_exit_commit_message(
        scope="bank",
        subject="subject:joint:1",
        system="Bank — joint account",
        exit_type="shared",
        action="Close joint account",
        facts="both agree; settled",
        summary="close joint",
        cosigners="Sam Hale <sam@example.org>",
    )
    commit = bx.parse_exit_commit(msg)
    assert "Exit-Cosigners" in commit.trailers


# --- sovereignty axis (binary test, unchanged) ------------------------------

def test_unsigned_exit_is_null():
    commit = bx.parse_exit_commit(_exit_message(), signature_status="N")
    assert bx.classify_exit(commit).sovereignty == bgsp.NULL


def test_bot_signed_exit_is_null():
    commit = bx.parse_exit_commit(
        _exit_message(), signature_status="G", signer="github-actions[bot]"
    )
    assert bx.classify_exit(commit).sovereignty == bgsp.NULL


def test_good_human_signature_is_sovereign():
    result = bx.classify_exit(_signed(_exit_message()))
    assert result.sovereignty == bgsp.SOVEREIGN


def test_null_classification_claim_stays_null():
    commit = _signed(_exit_message(classification=bgsp.NULL))
    assert bx.classify_exit(commit).sovereignty == bgsp.NULL


def test_missing_exit_envelope_is_null_exit():
    # Sovereign BGSP commit but with no exit envelope is not a valid exit.
    msg = bgsp.draft_commit_message(
        scope="x",
        subject="s",
        action="a",
        facts="f",
        summary="s",
        authority="Robin Hale",
        classification=bgsp.SOVEREIGN,
    )
    commit = _signed(msg)
    result = bx.classify_exit(commit)
    assert result.sovereignty == bgsp.NULL
    assert result.completeness is None


# --- completeness axis ------------------------------------------------------

def test_settled_with_notice_is_clean():
    result = bx.classify_exit(_signed(_exit_message(obligations="settled")))
    assert result.is_clean_break
    assert result.completeness == bx.CLEAN


def test_none_obligation_with_notice_is_clean():
    result = bx.classify_exit(_signed(_exit_message(obligations="none")))
    assert result.completeness == bx.CLEAN


def test_transferred_obligation_is_clean():
    result = bx.classify_exit(
        _signed(_exit_message(obligations="transferred:novation-ref-9"))
    )
    assert result.completeness == bx.CLEAN


def test_in_process_obligation_is_pending():
    result = bx.classify_exit(
        _signed(_exit_message(obligations="in-process:30-day-notice"))
    )
    assert result.sovereignty == bgsp.SOVEREIGN
    assert result.completeness == bx.PENDING
    assert not result.is_clean_break


def test_disputed_obligation_is_contested():
    result = bx.classify_exit(
        _signed(_exit_message(obligations="disputed:ombudsman-ref-3"))
    )
    assert result.completeness == bx.CONTESTED


def test_blank_notice_downgrades_clean_to_pending():
    result = bx.classify_exit(_signed(_exit_message(obligations="settled", notice="")))
    assert result.completeness == bx.PENDING


def test_clean_break_requires_both_axes():
    # SOVEREIGN but PENDING is not a clean break.
    pending = bx.classify_exit(_signed(_exit_message(obligations="in-process:x")))
    assert not pending.is_clean_break
    # NULL can never be a clean break regardless of obligations.
    null = bx.classify_exit(bx.parse_exit_commit(_exit_message(), signature_status="N"))
    assert not null.is_clean_break


# --- lawful-use guardrails --------------------------------------------------

def test_escape_language_is_contested_guardrail():
    for word in ("abandon debt", "evade the balance", "dodge the bill", "walk away owing"):
        result = bx.classify_exit(_signed(_exit_message(obligations=word)))
        assert result.completeness == bx.CONTESTED, word
        assert any("GUARDRAIL" in r for r in result.reasons), word


def test_escape_language_never_clean():
    result = bx.classify_exit(_signed(_exit_message(obligations="ignore the loan")))
    assert not result.is_clean_break


def test_invalid_exit_type_is_flagged():
    commit = _signed(_exit_message(exit_type="random-type"))
    result = bx.classify_exit(commit)
    assert any("Exit-Type" in r for r in result.reasons)


# --- nullity healing --------------------------------------------------------

def test_heal_report_marks_healed_null():
    null_parent = bx.parse_exit_commit(
        _exit_message(classification=bgsp.NULL).replace(
            "# nothing", "# nothing"
        ),
        signature_status="N",
        commit_id="N1",
    )
    healer = bx.parse_exit_commit(
        _exit_message(heals="N1", parent="N1"),
        signature_status="G",
        signer="Robin Hale",
        commit_id="X1",
    )
    results = bx.verify_ledger([null_parent, healer])
    report = bx.heal_report(results)
    assert "N1" in report.healed
    assert report.healed["N1"] == ["X1"]
    assert report.all_healed


def test_heal_report_marks_unhealed_null():
    null_parent = bx.parse_exit_commit(
        _exit_message(classification=bgsp.NULL),
        signature_status="N",
        commit_id="N1",
    )
    other = bx.parse_exit_commit(
        _exit_message(),  # does not heal N1
        signature_status="G",
        signer="Robin Hale",
        commit_id="X1",
    )
    report = bx.heal_report(bx.verify_ledger([null_parent, other]))
    assert "N1" in report.unhealed
    assert not report.all_healed


def test_null_healer_does_not_count():
    # An unsigned commit that *claims* to heal a NULL heals nothing.
    null_parent = bx.parse_exit_commit(
        _exit_message(classification=bgsp.NULL), signature_status="N", commit_id="N1"
    )
    fake_healer = bx.parse_exit_commit(
        _exit_message(heals="N1", classification=bgsp.NULL),
        signature_status="N",
        commit_id="X1",
    )
    report = bx.heal_report(bx.verify_ledger([null_parent, fake_healer]))
    assert "N1" in report.unhealed


# --- example ledger ---------------------------------------------------------

def test_example_ledger_files_classify_as_expected():
    expected = {
        "00-null-platform-autorenew.commit": (bgsp.NULL, None),
        "01-exit-utility-energy.commit": (bgsp.SOVEREIGN, bx.CLEAN),
        "02-exit-financial-bank.commit": (bgsp.SOVEREIGN, bx.CLEAN),
        "03-exit-medical-device.commit": (bgsp.SOVEREIGN, bx.CLEAN),
        "04-exit-platform-heal.commit": (bgsp.SOVEREIGN, bx.CLEAN),
        "05-exit-government-council.commit": (bgsp.SOVEREIGN, bx.PENDING),
        "06-exit-financial-insurance.commit": (bgsp.SOVEREIGN, bx.PENDING),
        "07-exit-shared-family-joint.commit": (bgsp.SOVEREIGN, bx.CLEAN),
    }
    for name, (sov, comp) in expected.items():
        commit = bgsp._load_commit_from_file(str(LEDGER / name))
        result = bx.classify_exit(commit)
        assert result.sovereignty == sov, name
        assert result.completeness == comp, name


def test_example_ledger_payload_digests_match_facts():
    for path in sorted(LEDGER.glob("*.commit")):
        commit = bgsp._load_commit_from_file(str(path))
        facts = (
            commit.body.split("Facts considered:", 1)[-1].strip()
            if "Facts considered:" in commit.body
            else commit.body.strip()
        )
        recomputed = bgsp.payload_digest(
            subject=commit.subject or "",
            facts=facts,
            action=commit.trailers["Burgess-Action"],
        )
        assert recomputed == commit.payload_sha256, path.name


def test_example_ledger_heal_report():
    commits = [bgsp._load_commit_from_file(str(p)) for p in sorted(LEDGER.glob("*.commit"))]
    report = bx.heal_report(bx.verify_ledger(commits))
    assert "00-null-platform-autorenew" in report.healed
    assert report.healed["00-null-platform-autorenew"] == ["04-exit-platform-heal"]


# --- notice templates -------------------------------------------------------

def test_notice_template_uses_system_and_effective():
    commit = bgsp._load_commit_from_file(str(LEDGER / "01-exit-utility-energy.commit"))
    notice = bx.notice_template(commit)
    assert "Acme Energy" in notice
    assert "2026-06-30" in notice


def test_notice_template_varies_by_type():
    util = bx.notice_template(
        bgsp._load_commit_from_file(str(LEDGER / "01-exit-utility-energy.commit"))
    )
    med = bx.notice_template(
        bgsp._load_commit_from_file(str(LEDGER / "03-exit-medical-device.commit"))
    )
    assert "meter" in util.lower()
    assert "safeguarding" in med.lower() or "clinical" in med.lower()


# --- Clean Break Certificate ------------------------------------------------

def test_certificate_partial_when_pending_present():
    commits = [bgsp._load_commit_from_file(str(p)) for p in sorted(LEDGER.glob("*.commit"))]
    cert = bx.clean_break_certificate(bx.verify_ledger(commits))
    assert "PARTIAL" in cert
    assert "Healed prior NULL decisions" in cert


def test_certificate_complete_when_all_clean_and_healed():
    msgs = [
        _signed(_exit_message(obligations="settled"), signer="Robin Hale"),
    ]
    msgs[0].commit_id = "X1"
    cert = bx.clean_break_certificate(bx.verify_ledger(msgs))
    assert "COMPLETE" in cert
    assert "Status:** COMPLETE" in cert


# --- CLI --------------------------------------------------------------------

def test_cli_check_clean_returns_zero(capsys):
    rc = bx.main(["check", str(LEDGER / "01-exit-utility-energy.commit")])
    out = capsys.readouterr().out
    assert rc == 0
    assert "SOVEREIGN / CLEAN" in out


def test_cli_check_null_returns_nonzero(capsys):
    rc = bx.main(["check", str(LEDGER / "00-null-platform-autorenew.commit")])
    assert rc == 1
    assert "NULL" in capsys.readouterr().out


def test_cli_verify_ledger_reports_unhealed_or_null(capsys):
    rc = bx.main(["verify", *[str(p) for p in sorted(LEDGER.glob("*.commit"))]])
    out = capsys.readouterr().out
    # The ledger contains a NULL ancestor, so sovereignty is NULL overall.
    assert "Ledger sovereignty: NULL" in out
    assert rc == 1


def test_cli_certificate_outputs_markdown(capsys):
    rc = bx.main(["certificate", *[str(p) for p in sorted(LEDGER.glob("*.commit"))]])
    out = capsys.readouterr().out
    assert rc == 0
    assert "# Clean Break Certificate" in out


def test_cli_draft_is_null(capsys):
    rc = bx.main(
        [
            "draft",
            "--subject", "subject:energy:1",
            "--system", "Acme Energy",
            "--type", "utility",
            "--action", "Close account",
            "--facts", "settled",
            "--summary", "leave acme",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    commit = bx.parse_exit_commit(out, signature_status="N")
    assert bx.classify_exit(commit).sovereignty == bgsp.NULL
