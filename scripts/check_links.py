#!/usr/bin/env python3
"""Check relative links in the Burgess Principle repository's markdown files.

The repository routes readers between documents constantly -- a person acting on
a decision is sent from ``START_HERE.md`` to a template to a letter. A broken
link in that chain is a person who cannot ask the binary question. This checker
makes that failure a build error instead of a silent dead end.

It exists specifically to de-risk documentation reorganisation: move a file,
run this, and every stale reference is reported before the change is merged.

Scope:

* Every markdown file tracked by git (``git ls-files '*.md'``), so untracked
  scratch files and vendored trees are ignored.
* Inline links ``[text](target)``, reference definitions ``[label]: target``,
  and image links.
* Relative targets only. External URLs (``http``, ``https``, ``mailto``,
  ``tel``, ``data``) and pure in-page anchors (``#section``) are not fetched --
  this checker never touches the network.

A link is broken when the file or directory it points at does not exist on
disk. Anchor fragments are stripped before the check; anchor targets within a
file are not validated.

Run from the repo root::

    python3 scripts/check_links.py

Exits 0 when every relative link resolves, 1 otherwise.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parent.parent

# Schemes and prefixes this checker deliberately does not resolve. Nothing here
# touches the network; external URLs are somebody else's uptime problem.
EXTERNAL_PREFIXES: tuple[str, ...] = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "data:",
    "ftp://",
    "//",
)

# Inline links and images: [text](target) and ![alt](target), with an optional
# "title" after the target. Targets wrapped in <> are handled separately.
_INLINE_LINK_RE = re.compile(
    r"""!?\[[^\]]*\]\(\s*(?:<(?P<angle>[^>]*)>|(?P<bare>[^)\s]+))"""
    r"""(?:\s+["'][^"']*["'])?\s*\)""",
    re.VERBOSE,
)

# Reference definitions: [label]: target "optional title"
_REFERENCE_DEF_RE = re.compile(
    r"""^\s{0,3}\[[^\]^]+\]:\s*(?:<(?P<angle>[^>]*)>|(?P<bare>\S+))""",
    re.MULTILINE,
)

# Fenced code blocks -- links inside them are illustrative, not navigational.
_FENCED_CODE_RE = re.compile(r"^(?P<fence>```|~~~).*?^(?P=fence)", re.MULTILINE | re.DOTALL)


def tracked_markdown_files() -> list[Path]:
    """Return every markdown file tracked by git, relative to the repo root."""
    result = subprocess.run(
        ["git", "ls-files", "*.md", "*.markdown"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line.strip()]


def strip_code_blocks(text: str) -> str:
    """Blank out fenced code blocks, preserving line numbering."""

    def _blank(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    return _FENCED_CODE_RE.sub(_blank, text)


def is_external(target: str) -> bool:
    return target.startswith(EXTERNAL_PREFIXES)


def extract_targets(text: str) -> list[tuple[str, int]]:
    """Return ``(target, line_number)`` for every link target in ``text``."""
    body = strip_code_blocks(text)
    targets: list[tuple[str, int]] = []
    for pattern in (_INLINE_LINK_RE, _REFERENCE_DEF_RE):
        for match in pattern.finditer(body):
            target = match.group("angle")
            if target is None:
                target = match.group("bare")
            if target:
                line = body.count("\n", 0, match.start()) + 1
                targets.append((target.strip(), line))
    return targets


def resolve_target(source: Path, target: str) -> Path | None:
    """Resolve ``target`` as referenced from ``source``.

    Returns ``None`` when the target needs no filesystem check (external URL or
    a pure in-page anchor).
    """
    if is_external(target) or target.startswith("#") or not target:
        return None

    path_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not path_part:
        return None

    if path_part.startswith("/"):
        # Root-relative links resolve against the repo root, matching how the
        # published site serves them.
        return REPO_ROOT / path_part.lstrip("/")
    return source.parent / path_part


def check_file(path: Path, errors: list[str]) -> int:
    """Check one file. Returns the number of relative links examined."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:  # pragma: no cover - unreadable file
        errors.append(f"{path.relative_to(REPO_ROOT)}: could not read ({exc})")
        return 0

    checked = 0
    for target, line in extract_targets(text):
        resolved = resolve_target(path, target)
        if resolved is None:
            continue
        checked += 1
        if not resolved.exists():
            rel = path.relative_to(REPO_ROOT)
            errors.append(f"{rel}:{line}: broken link -> {target}")
    return checked


def main() -> int:
    errors: list[str] = []
    files = tracked_markdown_files()
    checked = sum(check_file(path, errors) for path in files)

    if errors:
        print("Link check failed:\n", file=sys.stderr)
        for err in sorted(errors):
            print(f"  - {err}", file=sys.stderr)
        print(
            f"\n{len(errors)} broken link(s) across {len(files)} markdown files.\n"
            "If you moved a document, update the references or leave a pointer "
            "file at the old path so external links keep working.",
            file=sys.stderr,
        )
        return 1

    print(f"Link check: OK ({checked} relative links across {len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
