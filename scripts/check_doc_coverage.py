#!/usr/bin/env python3
"""Check that every root document is placed in TIERS.md and indexed in NAVIGATION.md.

``TIERS.md`` and ``NAVIGATION.md`` are only useful if they are complete. A file
that appears in neither is a file a contributor cannot place and a reader cannot
find -- which is how the repository accumulated an unmapped root in the first
place. This checker turns both documents from snapshots into invariants: add a
root document without mapping it and the build fails.

What is checked:

* Every markdown file tracked by git at the repository root is linked from
  ``TIERS.md`` (in a tier table or the "Outside the tiers" table).
* Every markdown file tracked by git at the repository root is linked from the
  ``NAVIGATION.md`` index.
* Every top-level directory that holds tracked markdown is linked from
  ``TIERS.md`` and from ``NAVIGATION.md``.

A "link" is any relative markdown link to that path -- ``[text](./FILE.md)`` or
``[text](FILE.md)``. Mentioning a filename in prose does not count, because a
reader cannot click prose.

Run from the repo root::

    python3 scripts/check_doc_coverage.py

Exits 0 when coverage is complete, 1 otherwise.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

TIERS = "TIERS.md"
NAVIGATION = "NAVIGATION.md"

# Directories that hold no reader-facing documentation and are therefore not
# expected to appear on either map.
EXEMPT_DIRECTORIES: frozenset[str] = frozenset({".github", ".cursor"})

# Link targets, with or without a leading "./", and with any anchor stripped.
_LINK_TARGET_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)>\s]+)>?(?:\s+[\"'][^\"']*[\"'])?\s*\)")


def tracked_markdown() -> list[Path]:
    """Return every markdown file tracked by git, as repo-relative paths."""
    result = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [Path(line) for line in result.stdout.splitlines() if line]


def linked_targets(document: str) -> set[str]:
    """Return the normalised relative link targets found in ``document``."""
    text = (REPO_ROOT / document).read_text(encoding="utf-8")
    targets: set[str] = set()
    for match in _LINK_TARGET_RE.finditer(text):
        target = match.group(1).split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "tel:")):
            continue
        target = target.removeprefix("./").rstrip("/")
        if target:
            targets.add(target)
    return targets


def main() -> int:
    for document in (TIERS, NAVIGATION):
        if not (REPO_ROOT / document).is_file():
            print(f"Doc coverage: {document} is missing at the repo root")
            return 1

    markdown = tracked_markdown()
    root_documents = sorted(str(path) for path in markdown if len(path.parts) == 1)
    documented_directories = sorted(
        {
            path.parts[0]
            for path in markdown
            if len(path.parts) > 1 and path.parts[0] not in EXEMPT_DIRECTORIES
        }
    )

    tiers_links = linked_targets(TIERS)
    navigation_links = linked_targets(NAVIGATION)

    errors: list[str] = []
    for document in root_documents:
        if document not in tiers_links:
            errors.append(
                f"{document} is not placed in a tier -- add it to a table in {TIERS}"
            )
        if document not in navigation_links:
            errors.append(
                f"{document} is not indexed -- add it to the appendix in {NAVIGATION}"
            )
    for directory in documented_directories:
        if directory not in tiers_links:
            errors.append(
                f"{directory}/ is not placed in a tier -- add it to a table in {TIERS}"
            )
        if directory not in navigation_links:
            errors.append(
                f"{directory}/ is not indexed -- add it to the appendix in {NAVIGATION}"
            )

    if errors:
        print("Doc coverage: FAILED")
        for error in errors:
            print(f"  - {error}")
        print(
            "\nEvery root document belongs somewhere. If it is not Core, "
            f"Toolkit, or Extensions, add it to 'Outside the tiers' in {TIERS}."
        )
        return 1

    print(
        f"Doc coverage: OK ({len(root_documents)} root documents, "
        f"{len(documented_directories)} directories mapped)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
