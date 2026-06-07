#!/usr/bin/env python3
"""Burgess Sovereign Exit Protocol (BSEP) — drafting and verification helper.

See ``protocols/burgess-sovereign-exit.md`` for the full specification. BSEP is
the direct successor application of the Burgess Git Sovereignty Protocol (BGSP):
it applies the signed-commit SOVEREIGN / NULL primitive to the act of *leaving* a
system, turning a clean, accountable exit into a first-class Git commit.

This helper reuses ``bgsp.py`` unchanged for the **sovereignty axis**
(SOVEREIGN / NULL — the binary Burgess test, never weakened) and adds:

* the **completeness axis** (CLEAN / PENDING / CONTESTED) derived from the
  ``Exit-Obligations`` and ``Exit-Notice`` trailers;
* **lawful-use guardrails** that reject debt-dodging / escape language rather than
  laundering it into a "clean break";
* **nullity healing** reporting (healed vs unhealed prior NULL decisions);
* **notice-language** templates generated from commit data;
* a **Clean Break Certificate** generated *from* a Sovereign Exit Ledger.

Design (inherited from BGSP, deliberately):

* **Binary test not weakened.** Sovereignty is still derived from the signature,
  signer identity, attestation trailers, and payload digest. The completeness axis
  is *separate*; CLEAN can never cure NULL.
* **NULL by default.** Unsigned / bad-signature / bot-signed exits are NULL.
* **Lawful only.** Escape language in ``Exit-Obligations`` ⇒ CONTESTED + guardrail
  error. There is no representation for dodging a legitimate obligation.
* **Local-first, stdlib only.** No third-party dependencies, no network. Portable
  enough for an iPhone shortcut or a Mac terminal. Git mode shells out to ``git``
  only when asked.
* **Computes, does not sign.** It drafts and verifies; the individual signs.

Input modes mirror ``bgsp.py``: ``.commit`` message files (with an optional
stripped ``# signature-status:`` / ``# signer:`` / ``# commit-id:`` header) for
verifiable examples and tests, or real git refs with ``--git``.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


# --- import the sibling bgsp.py (repo root) regardless of CWD ----------------

def _load_bgsp():
    """Import the repo-root ``bgsp`` module without requiring installation."""
    try:  # already importable (installed, or on sys.path)
        import bgsp as _bgsp  # type: ignore

        return _bgsp
    except ModuleNotFoundError:
        pass
    root = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location("bgsp", root / "bgsp.py")
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError("could not locate bgsp.py at the repository root")
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("bgsp", module)
    spec.loader.exec_module(module)
    return module


bgsp = _load_bgsp()

SOVEREIGN = bgsp.SOVEREIGN
NULL = bgsp.NULL

# Completeness axis (independent of SOVEREIGN / NULL).
CLEAN = "CLEAN"
PENDING = "PENDING"
CONTESTED = "CONTESTED"

# The six canonical system types (spec §2.2).
EXIT_TYPES: tuple[str, ...] = (
    "utility",
    "financial",
    "medical",
    "platform",
    "government",
    "shared",
)

# Exit-specific required trailers (in addition to BGSP's REQUIRED_TRAILERS).
REQUIRED_EXIT_TRAILERS: tuple[str, ...] = (
    "Exit-System",
    "Exit-Type",
    "Exit-Obligations",
    "Exit-Notice",
    "Exit-Effective",
    "Exit-Heals",
)

# Obligation states that count as genuinely discharged (spec §4.1).
DISCHARGED_OBLIGATIONS: frozenset[str] = frozenset({"none", "settled"})

# Lawful-use guardrail: words that signal escaping rather than handling an
# obligation. Their presence in Exit-Obligations is a hard CONTESTED (spec §4.3).
# Conservative by design; a deployment may extend, never narrow, this set.
ESCAPE_LANGUAGE: tuple[str, ...] = (
    "abandon",
    "evade",
    "evading",
    "dodge",
    "dodging",
    "ignore",
    "ignored",
    "ignoring",
    "walk away",
    "walked away",
    "skip",
    "skipped",
    "default on",
    "defaulting",
    "ditch",
    "ghost",
    "disappear from",
)

REVIEW_WORDING_EXIT = (
    "I individually reviewed the specific facts of this exit and exercise my own "
    "authority to release myself from the system named above."
)

AUTHORITY_PLACEHOLDER = (
    "<named human, exercising self-sovereign authority over own affairs — "
    "REQUIRED before signing>"
)


# --- parsing ----------------------------------------------------------------

def parse_exit_commit(
    text: str,
    *,
    signature_status: str = "N",
    signer: str | None = None,
    commit_id: str | None = None,
) -> "bgsp.BurgessCommit":
    """Parse an exit commit message, reusing the BGSP parser for trailers."""
    return bgsp.parse_commit_message(
        text,
        signature_status=signature_status,
        signer=signer,
        commit_id=commit_id,
    )


def _heals(commit: "bgsp.BurgessCommit") -> list[str]:
    """The prior NULL decision ids this exit claims to heal (``Exit-Heals``)."""
    raw = (commit.trailers.get("Exit-Heals") or "").strip()
    if not raw or raw.lower() in {"none", "-", ""}:
        return []
    return [tok for tok in raw.replace(",", " ").split() if tok]


# --- completeness axis ------------------------------------------------------

@dataclass
class ExitClassification:
    """The two-axis result of classifying an exit commit, with reasons."""

    sovereignty: str  # SOVEREIGN or NULL
    completeness: str | None  # CLEAN / PENDING / CONTESTED, or None when NULL
    reasons: list[str] = field(default_factory=list)

    @property
    def is_clean_break(self) -> bool:
        return self.sovereignty == SOVEREIGN and self.completeness == CLEAN

    def label(self) -> str:
        if self.sovereignty != SOVEREIGN:
            return NULL
        return f"{SOVEREIGN} / {self.completeness}"

    def __str__(self) -> str:
        return self.label()


def _obligation_completeness(value: str, notice: str, reasons: list[str]) -> str:
    """Derive CLEAN / PENDING / CONTESTED from obligations + notice (spec §4.2)."""
    low = value.strip().lower()

    # Lawful-use guardrail first: escape language is never CLEAN.
    for word in ESCAPE_LANGUAGE:
        if word in low:
            reasons.append(
                f"GUARDRAIL: Exit-Obligations contains escape language {word!r}; "
                "BSEP never represents dodging a lawful obligation (spec §4.3) ⇒ CONTESTED"
            )
            return CONTESTED

    if low.startswith("disputed:") or low == "disputed":
        reasons.append("obligation is in a declared dispute (proper channel) ⇒ CONTESTED")
        return CONTESTED
    if low.startswith("in-process:") or low == "in-process":
        reasons.append("a lawful process is still running (notice/final-bill/port) ⇒ PENDING")
        return PENDING

    notice_blank = not notice.strip()
    if low in DISCHARGED_OBLIGATIONS or low.startswith("transferred:"):
        if notice_blank:
            reasons.append("Exit-Notice is blank; notice unproven ⇒ PENDING")
            return PENDING
        reasons.append("obligations discharged + notice referenced ⇒ CLEAN")
        return CLEAN

    reasons.append(f"unrecognised Exit-Obligations {value!r}; conservative default ⇒ PENDING")
    return PENDING


def classify_exit(
    commit: "bgsp.BurgessCommit",
    *,
    known_payload: dict[str, str] | None = None,
    parent_result: str | None = None,
) -> ExitClassification:
    """Classify an exit commit on both axes.

    Sovereignty is delegated to ``bgsp.classify`` (the binary test, unchanged).
    Completeness is derived only when the exit is SOVEREIGN; a NULL exit has no
    completeness — an unsigned "exit" is not an exit.
    """
    reasons: list[str] = []

    # Exit envelope must be well-formed (in addition to BGSP trailers).
    missing = [t for t in REQUIRED_EXIT_TRAILERS if t not in commit.trailers]
    if missing:
        reasons.append("exit envelope malformed; missing trailers: " + ", ".join(missing))

    exit_type = (commit.trailers.get("Exit-Type") or "").strip().lower()
    if exit_type and exit_type not in EXIT_TYPES:
        reasons.append(
            f"Exit-Type {exit_type!r} is not one of {', '.join(EXIT_TYPES)} (spec §2.2)"
        )

    base = bgsp.classify(commit, known_payload=known_payload, parent_result=parent_result)
    reasons = base.reasons + reasons

    if base.result != SOVEREIGN or missing:
        # NULL on the sovereignty axis (or a malformed envelope) ⇒ no clean break.
        sov = base.result if not missing else NULL
        if missing and base.result == SOVEREIGN:
            reasons.append("sovereign signature present but exit envelope incomplete ⇒ NULL exit")
        return ExitClassification(sov, None, reasons)

    completeness = _obligation_completeness(
        commit.trailers.get("Exit-Obligations", ""),
        commit.trailers.get("Exit-Notice", ""),
        reasons,
    )
    return ExitClassification(SOVEREIGN, completeness, reasons)


# --- ledger verification ----------------------------------------------------

def verify_ledger(
    commits: Iterable["bgsp.BurgessCommit"],
    *,
    known_payloads: dict[str, dict[str, str]] | None = None,
) -> list[tuple["bgsp.BurgessCommit", ExitClassification]]:
    """Classify an ordered exit ledger, propagating nullity along parents.

    ``commits`` are oldest-first. Sovereignty propagation matches BGSP: a NULL
    ancestor poisons descendants until a SOVEREIGN re-attestation heals the chain.
    """
    known_payloads = known_payloads or {}
    results: list[tuple["bgsp.BurgessCommit", ExitClassification]] = []
    by_id: dict[str, str] = {}
    prev_result: str | None = None
    for commit in commits:
        parent_result: str | None = prev_result
        if commit.parent and commit.parent in by_id:
            parent_result = by_id[commit.parent]
        payload = None
        if commit.subject and commit.subject in known_payloads:
            payload = known_payloads[commit.subject]
        result = classify_exit(commit, known_payload=payload, parent_result=parent_result)
        results.append((commit, result))
        prev_result = result.sovereignty
        if commit.commit_id:
            by_id[commit.commit_id] = result.sovereignty
    return results


@dataclass
class HealReport:
    """Healed vs unhealed prior NULL decisions across a ledger (spec §5.3)."""

    healed: dict[str, list[str]] = field(default_factory=dict)  # null_id -> healer ids
    unhealed: list[str] = field(default_factory=list)  # null ids no exit heals
    healers: dict[str, list[str]] = field(default_factory=dict)  # exit id -> healed ids

    @property
    def all_healed(self) -> bool:
        return not self.unhealed


def heal_report(
    results: list[tuple["bgsp.BurgessCommit", ExitClassification]],
) -> HealReport:
    """Build a healed/unhealed report from classified ledger results."""
    null_ids: list[str] = []
    heal_claims: dict[str, list[str]] = {}  # null_id -> [healer ids]
    healer_map: dict[str, list[str]] = {}  # healer id -> [null ids]

    for commit, result in results:
        cid = commit.commit_id or commit.summary
        if result.sovereignty == NULL:
            null_ids.append(cid)
        claimed = _heals(commit)
        # Only a SOVEREIGN exit actually heals; a NULL "healer" heals nothing.
        if claimed and result.sovereignty == SOVEREIGN:
            healer_map[cid] = claimed
            for target in claimed:
                heal_claims.setdefault(target, []).append(cid)

    healed = {nid: heal_claims[nid] for nid in null_ids if nid in heal_claims}
    unhealed = [nid for nid in null_ids if nid not in heal_claims]
    return HealReport(healed=healed, unhealed=unhealed, healers=healer_map)


# --- drafting ---------------------------------------------------------------

def draft_exit_commit_message(
    *,
    scope: str,
    subject: str,
    system: str,
    exit_type: str,
    action: str,
    facts: str,
    summary: str,
    obligations: str = "<none | settled | transferred:<ref> | in-process:<ref> | disputed:<ref>>",
    notice: str = "<notice reference where legally required, or 'not-required' with basis>",
    effective: str = "<YYYY-MM-DD or YYYY-MM-DD/YYYY-MM-DD window>",
    heals: str = "none",
    authority: str = AUTHORITY_PLACEHOLDER,
    parent: str = "none",
    classification: str = NULL,
    cosigners: str | None = None,
) -> str:
    """Build a draft ``burgess(exit):`` commit message.

    Drafts are ``NULL`` by default: no human has signed yet. The individual sets
    ``Burgess-Classification: SOVEREIGN`` and signs to make the exit sovereign.
    """
    digest = bgsp.payload_digest(subject=subject, facts=facts, action=action)
    scope_part = f"({scope})" if scope else "(exit)"
    lines = [
        f"burgess{scope_part}: {summary}",
        "",
        f"Facts considered: {facts}",
        "",
        f"Burgess-Principle: {bgsp.ONE_QUESTION}",
        f"Burgess-Subject: {subject}",
        f"Burgess-Authority: {authority}",
        f"Burgess-Review: {REVIEW_WORDING_EXIT}",
        f"Burgess-Action: {action}",
        f"Burgess-Payload-SHA256: {digest}",
        f"Burgess-Parent: {parent}",
        f"Burgess-Classification: {classification}",
        f"Exit-System: {system}",
        f"Exit-Type: {exit_type}",
        f"Exit-Obligations: {obligations}",
        f"Exit-Notice: {notice}",
        f"Exit-Effective: {effective}",
        f"Exit-Heals: {heals}",
    ]
    if cosigners:
        lines.append(f"Exit-Cosigners: {cosigners}")
    lines.append("")
    return "\n".join(lines)


# --- notice templates -------------------------------------------------------

_NOTICE_TEMPLATES: dict[str, str] = {
    "utility": (
        "To {system}\n\n"
        "Re: closure of my account (reference held privately).\n\n"
        "I am giving notice to close this account with effect from {effective}. "
        "Please take a final meter/usage reading as of that date, issue a final "
        "bill, and confirm closure in writing. Obligation status on my side: "
        "{obligations}.\n\n"
        "This notice is recorded as a signed Sovereign Exit commit; a digest of "
        "the underlying facts is available on request for verification."
    ),
    "financial": (
        "To {system}\n\n"
        "Re: closure / cancellation of my account or agreement.\n\n"
        "I am giving notice to close or cancel this account/agreement with effect "
        "from {effective}. Please confirm the final balance and closure in "
        "writing. Obligation status: {obligations}. Where a notice period "
        "applies, treat this as the start of that period.\n\n"
        "This notice is recorded as a signed Sovereign Exit commit."
    ),
    "medical": (
        "To {system}\n\n"
        "Re: transition of my care/records/device away from this provider.\n\n"
        "I am giving notice of my decision to transition away from this system "
        "with effect from {effective}, and request a safe handover and a copy of "
        "my records/parameters. Obligation status: {obligations}. Nothing in this "
        "notice waives any clinical safeguarding duty.\n\n"
        "This notice is recorded as a signed Sovereign Exit commit."
    ),
    "platform": (
        "To {system}\n\n"
        "Re: closure of my account and export/erasure of my data.\n\n"
        "I am giving notice to close my account with effect from {effective}. "
        "Please disable any auto-renewal, provide a full export of my data, and "
        "confirm erasure where I am entitled to it. Obligation status: "
        "{obligations}.\n\n"
        "This notice is recorded as a signed Sovereign Exit commit."
    ),
    "government": (
        "To {system}\n\n"
        "Re: update/removal of my registration for this service.\n\n"
        "I am giving notice to update or end my registration with effect from "
        "{effective}, in accordance with the applicable rules. Obligation status: "
        "{obligations}. Please confirm the change in writing.\n\n"
        "This notice is recorded as a signed Sovereign Exit commit."
    ),
    "shared": (
        "To {system}\n\n"
        "Re: closure/separation of a shared account or plan.\n\n"
        "The named parties are jointly giving notice to close or separate this "
        "shared arrangement with effect from {effective}. Obligation status: "
        "{obligations}. Each party attests individually; see the signed Sovereign "
        "Exit commit(s).\n\n"
        "This notice is recorded as signed Sovereign Exit commit(s)."
    ),
}


def notice_template(commit: "bgsp.BurgessCommit") -> str:
    """Generate basic notice language from an exit commit's data (spec §2)."""
    exit_type = (commit.trailers.get("Exit-Type") or "").strip().lower()
    template = _NOTICE_TEMPLATES.get(exit_type, _NOTICE_TEMPLATES["financial"])
    return template.format(
        system=commit.trailers.get("Exit-System", "<system>"),
        effective=commit.trailers.get("Exit-Effective", "<date>"),
        obligations=commit.trailers.get("Exit-Obligations", "<obligations>"),
    )


# --- Clean Break Certificate ------------------------------------------------

def clean_break_certificate(
    results: list[tuple["bgsp.BurgessCommit", ExitClassification]],
    *,
    subject: str | None = None,
) -> str:
    """Render a Clean Break Certificate from classified ledger results (spec §5.4).

    The certificate is COMPLETE only when every exit is SOVEREIGN/CLEAN and no
    NULLs remain unhealed; otherwise PARTIAL, naming what is outstanding.
    """
    report = heal_report(results)
    exits = [
        (c, r)
        for c, r in results
        if (c.commit_type == "burgess" and (c.trailers.get("Exit-System")))
    ]
    sovereign_exits = [(c, r) for c, r in exits if r.sovereignty == SOVEREIGN]
    clean = all(r.is_clean_break for _, r in sovereign_exits) and bool(sovereign_exits)
    # COMPLETE when every sovereign exit is clean and no prior NULL gap is left
    # unhealed. A NULL decision that has been healed (e.g. the prior auto-renewal)
    # does not block completeness — it is reported in the healed section instead.
    complete = clean and report.all_healed

    subjects = sorted({c.subject for c, _ in exits if c.subject})
    subject_line = subject or (", ".join(subjects) if subjects else "<subject>")

    out: list[str] = []
    out.append("# Clean Break Certificate")
    out.append("")
    out.append("> Generated from a signed Sovereign Exit Ledger (BSEP). This")
    out.append("> certificate asserts nothing on its own — every line is derived")
    out.append("> from signed commits and is independently verifiable with")
    out.append("> `python tools/bgsp-exit.py verify <ledger>`.")
    out.append("")
    out.append(f"**Subject:** `{subject_line}`")
    out.append(f"**Status:** {'COMPLETE' if complete else 'PARTIAL'}")
    out.append(f"**Exits recorded:** {len(exits)}  ·  **Sovereign/Clean:** "
               f"{sum(1 for _, r in exits if r.is_clean_break)}")
    out.append("")
    out.append("| System | Type | Result | Obligations | Notice | Effective |")
    out.append("|---|---|---|---|---|---|")
    for commit, result in exits:
        out.append(
            "| {system} | {type} | {result} | {obl} | {notice} | {eff} |".format(
                system=commit.trailers.get("Exit-System", ""),
                type=commit.trailers.get("Exit-Type", ""),
                result=result.label(),
                obl=commit.trailers.get("Exit-Obligations", ""),
                notice=commit.trailers.get("Exit-Notice", ""),
                eff=commit.trailers.get("Exit-Effective", ""),
            )
        )
    out.append("")

    if report.healed:
        out.append("**Healed prior NULL decisions:**")
        for null_id, healers in report.healed.items():
            out.append(f"- `{null_id}` healed by {', '.join(f'`{h}`' for h in healers)}")
        out.append("")
    if report.unhealed:
        out.append("**Outstanding (unhealed) NULL decisions:**")
        for null_id in report.unhealed:
            out.append(f"- `{null_id}` — no sovereign exit has healed this NULL gap")
        out.append("")
    outstanding = [
        commit.trailers.get("Exit-System", commit.commit_id or "")
        for commit, result in sovereign_exits
        if not result.is_clean_break
    ]
    if outstanding:
        out.append("**Outstanding exits (sovereign but not yet Clean):**")
        for item in outstanding:
            out.append(f"- {item}")
        out.append("")

    if complete:
        out.append("This certifies a lawful, sovereign, and complete departure "
                   "from the systems listed above. The break is clean.")
    else:
        out.append("This is a PARTIAL certificate: the departure is recorded "
                   "honestly but is not yet complete. The items above remain open.")
    out.append("")
    out.append("---")
    out.append("")
    out.append("*The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence*")
    out.append("")
    return "\n".join(out)


# --- Git / file loading (mirrors bgsp.py) -----------------------------------

def _load_commit(ref_or_path: str, *, use_git: bool) -> "bgsp.BurgessCommit":
    if use_git:
        return bgsp.load_commit_from_git(ref_or_path)
    return bgsp._load_commit_from_file(ref_or_path)


# --- CLI --------------------------------------------------------------------

def _print_exit(commit: "bgsp.BurgessCommit", result: ExitClassification) -> None:
    ident = commit.commit_id or "(commit)"
    print(f"{result.label()}\t{ident}\t{commit.summary}")
    for reason in result.reasons:
        print(f"    - {reason}")


def _cmd_check(args: argparse.Namespace) -> int:
    commit = _load_commit(args.ref, use_git=args.git)
    result = classify_exit(commit)
    _print_exit(commit, result)
    return 0 if result.is_clean_break else 1


def _cmd_verify(args: argparse.Namespace) -> int:
    commits = [_load_commit(ref, use_git=args.git) for ref in args.refs]
    results = verify_ledger(commits)
    clean = True
    for commit, result in results:
        _print_exit(commit, result)
        if not (result.sovereignty == SOVEREIGN):
            clean = False
    report = heal_report(results)
    print("\nLedger sovereignty:", SOVEREIGN if clean else NULL)
    if report.unhealed:
        print("Unhealed NULL gaps:", ", ".join(report.unhealed))
    return 0 if clean and report.all_healed else 1


def _cmd_heal_report(args: argparse.Namespace) -> int:
    commits = [_load_commit(ref, use_git=args.git) for ref in args.refs]
    results = verify_ledger(commits)
    report = heal_report(results)
    if not (report.healed or report.unhealed):
        print("No prior NULL decisions found in this ledger.")
        return 0
    if report.healed:
        print("Healed prior NULL decisions:")
        for null_id, healers in report.healed.items():
            print(f"  HEALED   {null_id}  <-  {', '.join(healers)}")
    if report.unhealed:
        print("Unhealed prior NULL decisions (open gaps):")
        for null_id in report.unhealed:
            print(f"  UNHEALED {null_id}")
    return 0 if report.all_healed else 1


def _cmd_notice(args: argparse.Namespace) -> int:
    commit = _load_commit(args.ref, use_git=args.git)
    print(notice_template(commit))
    return 0


def _cmd_certificate(args: argparse.Namespace) -> int:
    commits = [_load_commit(ref, use_git=args.git) for ref in args.refs]
    results = verify_ledger(commits)
    sys.stdout.write(clean_break_certificate(results, subject=args.subject))
    return 0


def _cmd_draft(args: argparse.Namespace) -> int:
    msg = draft_exit_commit_message(
        scope=args.scope,
        subject=args.subject,
        system=args.system,
        exit_type=args.type,
        action=args.action,
        facts=args.facts,
        summary=args.summary,
        obligations=args.obligations,
        notice=args.notice,
        effective=args.effective,
        heals=args.heals,
        parent=args.parent,
        cosigners=args.cosigners,
    )
    sys.stdout.write(msg)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bgsp-exit",
        description="Burgess Sovereign Exit Protocol — draft and verify burgess(exit): commits.",
    )
    parser.add_argument(
        "--git",
        action="store_true",
        help="treat refs as git revisions and read signatures via git (default: read .commit files)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="classify one exit (SOVEREIGN/NULL + CLEAN/PENDING/CONTESTED)")
    p_check.add_argument("ref", help="a .commit file path, or a git ref with --git")
    p_check.set_defaults(func=_cmd_check)

    p_verify = sub.add_parser("verify", help="verify a Sovereign Exit Ledger (oldest-first)")
    p_verify.add_argument("refs", nargs="+", help="ordered .commit files or git refs")
    p_verify.set_defaults(func=_cmd_verify)

    p_heal = sub.add_parser("heal-report", help="show healed vs unhealed prior NULL decisions")
    p_heal.add_argument("refs", nargs="+", help="ordered .commit files or git refs")
    p_heal.set_defaults(func=_cmd_heal_report)

    p_notice = sub.add_parser("notice", help="generate notice language from an exit commit")
    p_notice.add_argument("ref", help="a .commit file path, or a git ref with --git")
    p_notice.set_defaults(func=_cmd_notice)

    p_cert = sub.add_parser("certificate", help="generate a Clean Break Certificate from a ledger")
    p_cert.add_argument("refs", nargs="+", help="ordered .commit files or git refs")
    p_cert.add_argument("--subject", default=None, help="override the certificate subject line")
    p_cert.set_defaults(func=_cmd_certificate)

    p_draft = sub.add_parser("draft", help="generate a draft burgess(exit): commit (NULL until signed)")
    p_draft.add_argument("--scope", default="exit")
    p_draft.add_argument("--subject", required=True)
    p_draft.add_argument("--system", required=True)
    p_draft.add_argument("--type", required=True, choices=EXIT_TYPES)
    p_draft.add_argument("--action", required=True)
    p_draft.add_argument("--facts", required=True)
    p_draft.add_argument("--summary", required=True)
    p_draft.add_argument("--obligations", default="settled")
    p_draft.add_argument("--notice", default="not-required (no notice period applies)")
    p_draft.add_argument("--effective", default="<YYYY-MM-DD>")
    p_draft.add_argument("--heals", default="none")
    p_draft.add_argument("--parent", default="none")
    p_draft.add_argument("--cosigners", default=None)
    p_draft.set_defaults(func=_cmd_draft)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
