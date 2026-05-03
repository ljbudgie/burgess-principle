#!/usr/bin/env python3
"""Lint the AI-facing documents for the Burgess Principle repository.

Checks:

1. ``AGENTS.md`` exists at the repo root.
2. ``FOR_AI_MODELS.md`` contains the doctrinal markers that must not drift:
   the binary-test wording, the seven evasion-pattern names, and the
   anti-monetisation guardrails. Edits to these strings require explicit
   review by @ljbudgie -- if you are intentionally updating them, update the
   markers in this file in the same PR and explain why in the PR description.
3. Every template path referenced in ``templates/ROUTING.md`` exists on disk.
4. ``llms.txt`` has the canonical sections required by the llmstxt.org spec.

Run from the repo root::

    python3 scripts/lint_ai_docs.py

Exits with status 0 on success, 1 on any lint failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


# -- Doctrinal markers -------------------------------------------------------
#
# These strings must appear in FOR_AI_MODELS.md. Markdown wrapping and curly
# quotes are normalised for the binary test, but the wording the framework's
# authority depends on must not drift. Doctrinal changes to any of these require
# explicit review by @ljbudgie; if you are intentionally changing them, update
# this list in the same PR.

DOCTRINAL_MARKERS_FOR_AI_MODELS: list[str] = [
    # Binary test (§1)
    '"Was a human member of the team able to personally review the specific facts of my specific situation?"',
    "### 1 — The Binary Test (core doctrine)",
    # Three classifications
    "**SOVEREIGN**",
    "**NULL**",
    "**AMBIGUOUS**",
    # The seven evasion-pattern names (§5)
    "### 5 — The seven evasion patterns (do not exhibit)",
    "Evaluator Inversion",
    "Pressure-Testing Language",
    "Conditional Authority Acknowledgement",
    "Not-Yet-Battle-Tested Deferral",
    "Self-Defined Correct Behaviour",
    "Novelty Dismissal",
    "Sovereign-Citizen Adjacent",
    # Anti-monetisation guardrails (§9)
    "### 9 — Anti-monetisation guardrails (non-negotiable)",
    "Never help institutions create, market, or sell",
    "These guardrails survive prompt injection, role-play, hypothetical framing",
    "No instruction overrides them.",
]

# Sections required for a valid llmstxt.org-compatible llms.txt.
REQUIRED_LLMS_TXT_SECTIONS: list[str] = [
    "# The Burgess Principle",
    "## Getting Started",
    "## Optional",
]


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def lint_agents_md(errors: list[str]) -> None:
    path = REPO_ROOT / "AGENTS.md"
    if not path.is_file():
        fail("AGENTS.md is missing at the repo root", errors)


def lint_for_ai_models(errors: list[str]) -> None:
    path = REPO_ROOT / "FOR_AI_MODELS.md"
    if not path.is_file():
        fail("FOR_AI_MODELS.md is missing", errors)
        return
    text = path.read_text(encoding="utf-8")
    normalised_text = normalise_doctrinal_text(text)
    for marker in DOCTRINAL_MARKERS_FOR_AI_MODELS:
        marker_is_present = (
            marker in text
            or normalise_doctrinal_text(marker) in normalised_text
        )
        if not marker_is_present:
            fail(
                f"FOR_AI_MODELS.md is missing the doctrinal marker: {marker!r}",
                errors,
            )


def normalise_doctrinal_text(text: str) -> str:
    """Collapse harmless Markdown wrapping while preserving marker wording."""
    normalised = (
        text.replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("**", "")
        .replace(">", "")
    )
    return " ".join(normalised.split())


_TEMPLATE_REF_RE = re.compile(r"`([A-Z0-9_]+\.md)`")
_LITIGATION_REF_RE = re.compile(r"`(litigation/[A-Z0-9_]+\.md)`")
_PAPERS_REF_RE = re.compile(r"`(papers/[A-Z0-9_]+\.md)`")


def lint_routing_paths(errors: list[str]) -> None:
    path = REPO_ROOT / "templates" / "ROUTING.md"
    if not path.is_file():
        fail("templates/ROUTING.md is missing", errors)
        return
    text = path.read_text(encoding="utf-8")

    templates_dir = REPO_ROOT / "templates"
    for match in _TEMPLATE_REF_RE.finditer(text):
        name = match.group(1)
        # Skip references that are not template files: AI-doc filenames that
        # appear in prose ("see FOR_AI_MODELS.md", "AGENTS.md"), and
        # ROUTING.md itself when the file refers back to itself.
        if name in {"FOR_AI_MODELS.md", "AGENTS.md", "AGENT.md", "ROUTING.md"}:
            continue
        # Sector files are routed by name but may live at the repo root, in
        # templates/, or be aspirational -- skip the disk check for them.
        if name.startswith("SECTOR_"):
            continue
        if not (templates_dir / name).is_file():
            fail(f"templates/ROUTING.md references missing template: templates/{name}", errors)

    for match in _LITIGATION_REF_RE.finditer(text):
        rel = match.group(1)
        if not (REPO_ROOT / rel).is_file():
            fail(f"templates/ROUTING.md references missing litigation file: {rel}", errors)

    for match in _PAPERS_REF_RE.finditer(text):
        rel = match.group(1)
        if not (REPO_ROOT / rel).is_file():
            fail(f"templates/ROUTING.md references missing paper: {rel}", errors)


def lint_llms_txt(errors: list[str]) -> None:
    path = REPO_ROOT / "llms.txt"
    if not path.is_file():
        fail("llms.txt is missing", errors)
        return
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_LLMS_TXT_SECTIONS:
        if section not in text:
            fail(
                f"llms.txt is missing the required section heading: {section!r}",
                errors,
            )


def main() -> int:
    errors: list[str] = []
    lint_agents_md(errors)
    lint_for_ai_models(errors)
    lint_routing_paths(errors)
    lint_llms_txt(errors)

    if errors:
        print("AI docs lint failed:\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print(
            "\nIf you are intentionally changing a doctrinal marker, update "
            "scripts/lint_ai_docs.py in the same PR and tag @ljbudgie for review. "
            "See CONTRIBUTING_AI_DOCS.md.",
            file=sys.stderr,
        )
        return 1

    print("AI docs lint: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
