#!/usr/bin/env python3
"""Burgess Git Sovereignty Protocol (BGSP) — verification and drafting helper.

See ``protocols/burgess-git-sovereignty.md`` for the full specification.

This is the reference classifier for the one Burgess question rendered as Git:

    One question: was a human mind with proper authority individually applied to
    the specific facts of this specific person's case? SOVEREIGN or NULL.

Design (deliberate, load-bearing):

* **Binary, derived, never asserted.** The ``Burgess-Classification`` trailer is a
  *claim*. This tool decides SOVEREIGN or NULL from the signature status, the
  signer identity, the attestation trailers, the payload digest, and parent
  nullity propagation. AMBIGUOUS is treated as NULL.
* **NULL by default.** Unsigned, bad-signature, or bot/CI-signed commits are NULL.
* **Local-first, stdlib only.** No third-party dependencies, no network. Portable
  enough for an iPhone shortcut or a Mac terminal. The git-backed mode shells out
  to the system ``git`` only when asked.
* **Computes, does not sign.** It drafts and verifies; a named human signs.

Two input modes:

1. **Message text / ``.commit`` files** — parse a commit message (plus an optional
   signature-status hint) and classify. Used by the example decision ledger and by
   tests, so the logic is verifiable without GPG infrastructure.
2. **Git repo** — read a real commit and its signature via ``git`` (``check`` /
   ``chain`` with refs), so ``git log --show-signature`` and this tool agree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Iterable

__all__ = [
    "SOVEREIGN",
    "NULL",
    "ONE_QUESTION",
    "REVIEW_WORDING",
    "BOT_SIGNER_PATTERNS",
    "REQUIRED_TRAILERS",
    "canonical_json_sha256",
    "payload_digest",
    "parse_commit_message",
    "BurgessCommit",
    "classify",
    "propagate_nullity",
    "draft_commit_message",
]

SOVEREIGN = "SOVEREIGN"
NULL = "NULL"

ONE_QUESTION = (
    "One question: was a human mind with proper authority individually applied "
    "to the specific facts of this specific person's case? SOVEREIGN or NULL."
)

REVIEW_WORDING = (
    "I individually reviewed the specific facts of this specific case and apply "
    "my own authority to the action above."
)

# Signer identities treated as non-human (=> NULL). Conservative by design:
# when in doubt, NULL. Deployments may extend this, never narrow it.
BOT_SIGNER_PATTERNS: tuple[str, ...] = (
    "bot",
    "[bot]",
    "noreply",
    "no-reply",
    "github-actions",
    "gitlab-ci",
    "ci@",
    "automation",
    "service-account",
    "dependabot",
    "renovate",
    "system",
    "daemon",
)

REQUIRED_TRAILERS: tuple[str, ...] = (
    "Burgess-Principle",
    "Burgess-Subject",
    "Burgess-Authority",
    "Burgess-Review",
    "Burgess-Action",
    "Burgess-Payload-SHA256",
    "Burgess-Parent",
    "Burgess-Classification",
)

# Good GPG/SSH signature statuses (git's --pretty=%G? codes):
#   G good, U good+unknown-validity, X good-but-expired, Y good-but-expired-key,
#   B bad, E cannot-check, N no-signature.
# A SOVEREIGN attestation requires a *currently valid* good signature.
GOOD_SIGNATURE_STATUSES = frozenset({"G", "U"})


def canonical_json_sha256(obj: Any) -> str:
    """SHA-256 of an object serialised as canonical sorted-key JSON.

    Matches ``iris/anchor.py`` and ``onchain-protocol/spec.md`` §2.2 so the
    payload digest is identical across the whole framework.
    """
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def payload_digest(*, subject: str, facts: str, action: str) -> str:
    """The ``Burgess-Payload-SHA256`` digest for a decision's facts + action."""
    return canonical_json_sha256({"action": action, "facts": facts, "subject": subject})


def _is_sha256_hex(value: str) -> bool:
    value = value.strip()
    if len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def is_bot_signer(signer: str | None) -> bool:
    """Whether a signer identity matches the non-human automation denylist."""
    if not signer:
        # No signer identity at all is handled as "not human" upstream via the
        # signature status; here an empty/unknown signer is treated as bot.
        return True
    low = signer.lower()
    return any(pat in low for pat in BOT_SIGNER_PATTERNS)


@dataclass
class BurgessCommit:
    """A parsed ``burgess:`` commit message and its surrounding facts."""

    raw: str
    commit_type: str | None = None
    scope: str | None = None
    summary: str = ""
    body: str = ""
    trailers: dict[str, str] = field(default_factory=dict)
    # Optional context the verifier may have:
    signature_status: str = "N"  # git %G? code; default no-signature => NULL
    signer: str | None = None
    commit_id: str | None = None

    @property
    def classification_claim(self) -> str | None:
        return self.trailers.get("Burgess-Classification")

    @property
    def subject(self) -> str | None:
        return self.trailers.get("Burgess-Subject")

    @property
    def parent(self) -> str | None:
        value = self.trailers.get("Burgess-Parent")
        if value is None:
            return None
        value = value.strip()
        if value.lower() in {"", "none", "-"}:
            return None
        return value

    @property
    def payload_sha256(self) -> str | None:
        return self.trailers.get("Burgess-Payload-SHA256")


def parse_commit_message(
    text: str,
    *,
    signature_status: str = "N",
    signer: str | None = None,
    commit_id: str | None = None,
) -> BurgessCommit:
    """Parse a commit message into a :class:`BurgessCommit`.

    The message is the conventional-commit subject, an optional body, and a final
    trailer block (RFC-822-style ``Key: value`` lines). Trailers are read from the
    last contiguous block of ``Key: value`` lines, matching ``git
    interpret-trailers``.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    # Drop a trailing blank lines for clean parsing.
    while lines and lines[-1].strip() == "":
        lines.pop()

    subject_line = lines[0] if lines else ""
    commit_type = scope = None
    summary = subject_line
    if ":" in subject_line:
        head, _, rest = subject_line.partition(":")
        head = head.strip()
        type_part = head
        if "(" in head and head.endswith(")"):
            type_part, _, scope_part = head.partition("(")
            scope = scope_part[:-1].strip() or None
        commit_type = type_part.strip() or None
        summary = rest.strip()

    # Trailers: the last paragraph made entirely of "Key: value" (or continuation)
    # lines. Walk up from the end collecting such lines.
    trailers: dict[str, str] = {}
    trailer_re_key = lambda s: (  # noqa: E731 - small local helper
        ":" in s and s.split(":", 1)[0].strip() != "" and " " not in s.split(":", 1)[0].strip()
    )
    idx = len(lines)
    collected: list[str] = []
    for i in range(len(lines) - 1, 0, -1):
        line = lines[i]
        if line.strip() == "":
            idx = i + 1
            break
        if trailer_re_key(line) or (collected and (line.startswith(" ") or line.startswith("\t"))):
            collected.append(line)
            idx = i
        else:
            idx = i + 1
            break
    trailer_lines = lines[idx:]
    current_key: str | None = None
    for line in trailer_lines:
        if (line.startswith(" ") or line.startswith("\t")) and current_key:
            trailers[current_key] += "\n" + line.strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            current_key = key
            trailers[key] = value.strip()
    body_lines = lines[1:idx]
    body = "\n".join(body_lines).strip()

    return BurgessCommit(
        raw=text,
        commit_type=commit_type,
        scope=scope,
        summary=summary,
        body=body,
        trailers=trailers,
        signature_status=signature_status,
        signer=signer,
        commit_id=commit_id,
    )


@dataclass
class Classification:
    """The derived classification of a single commit, with reasons."""

    result: str  # SOVEREIGN or NULL
    reasons: list[str] = field(default_factory=list)

    @property
    def is_sovereign(self) -> bool:
        return self.result == SOVEREIGN

    def __str__(self) -> str:
        return self.result


def classify(
    commit: BurgessCommit,
    *,
    known_payload: dict[str, str] | None = None,
    parent_result: str | None = None,
) -> Classification:
    """Derive SOVEREIGN or NULL for one commit per the spec's reference classifier.

    ``known_payload`` (with ``subject``/``facts``/``action``) lets the verifier
    recompute and confirm ``Burgess-Payload-SHA256``. ``parent_result`` carries the
    effective classification of the ``Burgess-Parent`` decision for nullity
    propagation; pass it when verifying a chain.
    """
    reasons: list[str] = []

    # 1. Signature must currently verify.
    if commit.signature_status not in GOOD_SIGNATURE_STATUSES:
        reasons.append(
            f"no valid human signature (status {commit.signature_status!r}); NULL by default"
        )
        return Classification(NULL, reasons)

    # 2. Signer must be a named human, not a bot/CI/automation identity.
    if is_bot_signer(commit.signer):
        reasons.append(f"signer {commit.signer!r} is a bot/automation identity; not a human mind")
        return Classification(NULL, reasons)

    # 3. Attestation block must be well-formed.
    missing = [t for t in REQUIRED_TRAILERS if t not in commit.trailers]
    if missing:
        reasons.append("attestation block malformed; missing trailers: " + ", ".join(missing))
        return Classification(NULL, reasons)

    # 4. Claimed classification must be SOVEREIGN (AMBIGUOUS/NULL claims => NULL).
    claim = commit.classification_claim
    if claim != SOVEREIGN:
        reasons.append(f"Burgess-Classification is {claim!r}, not SOVEREIGN")
        return Classification(NULL, reasons)

    # 5. Payload digest must be a valid sha256, and recompute if facts are known.
    digest = commit.payload_sha256 or ""
    if not _is_sha256_hex(digest):
        reasons.append("Burgess-Payload-SHA256 is not a 64-hex SHA-256 digest")
        return Classification(NULL, reasons)
    if known_payload is not None:
        recomputed = payload_digest(
            subject=known_payload.get("subject", ""),
            facts=known_payload.get("facts", ""),
            action=known_payload.get("action", ""),
        )
        if recomputed != digest.strip().lower():
            reasons.append("payload digest does not match the presented facts + action")
            return Classification(NULL, reasons)
        reasons.append("payload digest verified against presented facts")

    # 6. Nullity propagation: a NULL parent poisons this commit unless it
    #    re-attests. A SOVEREIGN commit *is* a re-attestation of its own case, so
    #    a fresh SOVEREIGN attestation heals the chain from here forward. We only
    #    propagate when the parent is explicitly NULL AND this commit does not
    #    name that parent as the case it is re-attesting. By spec, any valid
    #    SOVEREIGN commit re-attests its own subject's case, so reaching this
    #    point means it heals. We still surface the inherited-nullity note.
    if parent_result == NULL:
        reasons.append("parent decision is NULL; this commit re-attests and heals the chain here")

    reasons.append("good human signature + valid attestation + payload ⇒ SOVEREIGN")
    return Classification(SOVEREIGN, reasons)


def propagate_nullity(
    commits: Iterable[BurgessCommit],
    *,
    known_payloads: dict[str, dict[str, str]] | None = None,
) -> list[tuple[BurgessCommit, Classification]]:
    """Classify an ordered decision chain, propagating nullity along parents.

    ``commits`` are given oldest-first. Each commit's effective classification is
    computed with its parent's effective result, so a NULL anywhere poisons later
    commits until a SOVEREIGN re-attestation heals the chain.
    """
    known_payloads = known_payloads or {}
    results: list[tuple[BurgessCommit, Classification]] = []
    by_id: dict[str, str] = {}
    prev_result: str | None = None
    for commit in commits:
        # Prefer an explicit parent link if we have already classified it;
        # otherwise fall back to the immediately preceding commit in the chain.
        parent_result: str | None = prev_result
        if commit.parent and commit.parent in by_id:
            parent_result = by_id[commit.parent]
        payload = None
        if commit.subject and commit.subject in known_payloads:
            payload = known_payloads[commit.subject]
        result = classify(commit, known_payload=payload, parent_result=parent_result)
        results.append((commit, result))
        prev_result = result.result
        if commit.commit_id:
            by_id[commit.commit_id] = result.result
    return results


def draft_commit_message(
    *,
    scope: str,
    subject: str,
    action: str,
    facts: str,
    summary: str,
    authority: str = "<named human, role, and basis of authority — REQUIRED before signing>",
    parent: str = "none",
    classification: str = NULL,
) -> str:
    """Build a draft ``burgess:`` commit message.

    Drafts are ``NULL`` by default: no human has signed yet. A named human sets
    ``Burgess-Classification: SOVEREIGN`` and signs the commit to make it so.
    """
    digest = payload_digest(subject=subject, facts=facts, action=action)
    scope_part = f"({scope})" if scope else ""
    return "\n".join(
        [
            f"burgess{scope_part}: {summary}",
            "",
            f"Facts considered: {facts}",
            "",
            f"Burgess-Principle: {ONE_QUESTION}",
            f"Burgess-Subject: {subject}",
            f"Burgess-Authority: {authority}",
            f"Burgess-Review: {REVIEW_WORDING}",
            f"Burgess-Action: {action}",
            f"Burgess-Payload-SHA256: {digest}",
            f"Burgess-Parent: {parent}",
            f"Burgess-Classification: {classification}",
            "",
        ]
    )


# --- Git-backed mode -------------------------------------------------------

def _git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def load_commit_from_git(ref: str) -> BurgessCommit:
    """Read a commit and its signature status from the local git repo."""
    # %G? signature status, %GS signer name, %H full hash, %B raw body.
    out = _git(["show", "-s", "--pretty=format:%G?%x1f%GS%x1f%H%x1f%B", ref])
    status, signer, commit_id, body = (out.split("\x1f", 3) + ["", "", "", ""])[:4]
    return parse_commit_message(
        body,
        signature_status=status.strip() or "N",
        signer=signer.strip() or None,
        commit_id=commit_id.strip() or None,
    )


def _load_commit_from_file(path: str) -> BurgessCommit:
    """Load a commit message from a ``.commit`` text file.

    A leading ``# signature-status: <code>`` / ``# signer: <name>`` /
    ``# commit-id: <id>`` comment block (stripped before parsing) lets example
    files and tests declare the signature context the verifier would otherwise get
    from git. Without it, the file parses as unsigned (NULL).
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    status, signer, commit_id = "N", None, None
    keep: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        low = stripped.lower()
        if low.startswith("# signature-status:"):
            status = stripped.split(":", 1)[1].strip() or "N"
        elif low.startswith("# signer:"):
            signer = stripped.split(":", 1)[1].strip() or None
        elif low.startswith("# commit-id:"):
            commit_id = stripped.split(":", 1)[1].strip() or None
        elif low.startswith("# bgsp-meta") or low == "#":
            continue
        else:
            keep.append(line)
    return parse_commit_message(
        "\n".join(keep).strip(),
        signature_status=status,
        signer=signer,
        commit_id=commit_id or path,
    )


def _load_commit(ref_or_path: str, *, use_git: bool) -> BurgessCommit:
    if use_git:
        return load_commit_from_git(ref_or_path)
    return _load_commit_from_file(ref_or_path)


# --- CLI -------------------------------------------------------------------

def _print_classification(commit: BurgessCommit, result: Classification) -> None:
    ident = commit.commit_id or "(commit)"
    print(f"{result.result}\t{ident}\t{commit.summary}")
    for reason in result.reasons:
        print(f"    - {reason}")


def _cmd_check(args: argparse.Namespace) -> int:
    commit = _load_commit(args.ref, use_git=args.git)
    result = classify(commit)
    _print_classification(commit, result)
    return 0 if result.is_sovereign else 1


def _cmd_chain(args: argparse.Namespace) -> int:
    commits = [_load_commit(ref, use_git=args.git) for ref in args.refs]
    results = propagate_nullity(commits)
    sovereign = True
    for commit, result in results:
        _print_classification(commit, result)
        if not result.is_sovereign:
            sovereign = False
    print("\nChain result:", SOVEREIGN if sovereign else NULL)
    return 0 if sovereign else 1


def _cmd_draft(args: argparse.Namespace) -> int:
    msg = draft_commit_message(
        scope=args.scope,
        subject=args.subject,
        action=args.action,
        facts=args.facts,
        summary=args.summary,
        parent=args.parent,
    )
    sys.stdout.write(msg)
    return 0


def _cmd_digest(args: argparse.Namespace) -> int:
    print(payload_digest(subject=args.subject, facts=args.facts, action=args.action))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bgsp",
        description="Burgess Git Sovereignty Protocol — verify and draft burgess: commits.",
    )
    parser.add_argument(
        "--git",
        action="store_true",
        help="treat refs as git revisions and read signatures via git (default: read .commit files)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="classify one commit as SOVEREIGN or NULL")
    p_check.add_argument("ref", help="a .commit file path, or a git ref with --git")
    p_check.set_defaults(func=_cmd_check)

    p_chain = sub.add_parser("chain", help="classify a decision chain with nullity propagation")
    p_chain.add_argument("refs", nargs="+", help="ordered (oldest-first) .commit files or git refs")
    p_chain.set_defaults(func=_cmd_chain)

    p_draft = sub.add_parser("draft", help="generate a draft burgess: commit message (NULL until signed)")
    p_draft.add_argument("--scope", default="")
    p_draft.add_argument("--subject", required=True)
    p_draft.add_argument("--action", required=True)
    p_draft.add_argument("--facts", required=True)
    p_draft.add_argument("--summary", required=True)
    p_draft.add_argument("--parent", default="none")
    p_draft.set_defaults(func=_cmd_draft)

    p_digest = sub.add_parser("digest", help="compute the Burgess-Payload-SHA256 for facts + action")
    p_digest.add_argument("--subject", required=True)
    p_digest.add_argument("--action", required=True)
    p_digest.add_argument("--facts", required=True)
    p_digest.set_defaults(func=_cmd_digest)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
