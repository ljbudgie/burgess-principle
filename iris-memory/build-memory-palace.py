#!/usr/bin/env python3
"""Build the Iris Memory Palace JSON files from the five source Markdown files."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VERSION = "0.1.0"
SOURCE_FILES = [
    "01-identity.md",
    "02-lewis-profile.md",
    "03-partners.md",
    "04-live-cases.md",
    "05-infrastructure.md",
]
STOPWORDS = {
    "about",
    "after",
    "all",
    "and",
    "are",
    "before",
    "from",
    "into",
    "only",
    "that",
    "the",
    "this",
    "under",
    "with",
    "your",
}


def sha256_hex(text: str) -> str:
    """Return the SHA-256 digest of UTF-8 Markdown content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_title(content: str, fallback: str) -> str:
    """Use the first H1 as the document title."""
    for line in content.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def split_sections(content: str) -> list[dict[str, str]]:
    """Split Markdown into heading-led sections while preserving full text."""
    sections: list[dict[str, str]] = []
    current_title = "Preamble"
    current_lines: list[str] = []

    for line in content.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            if current_lines:
                sections.append(
                    {"title": current_title, "content": "\n".join(current_lines).strip()}
                )
            current_title = re.sub(r"^#{1,6}\s+", "", line).strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections.append({"title": current_title, "content": "\n".join(current_lines).strip()})

    return sections


def keywords_for(title: str, content: str) -> list[str]:
    """Create a small deterministic keyword list for lightweight search."""
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", f"{title} {content}".lower())
    ranked: dict[str, int] = {}
    for word in words:
        normalized = word.strip("'-")
        if normalized and normalized not in STOPWORDS:
            ranked[normalized] = ranked.get(normalized, 0) + 1

    return [
        word
        for word, _count in sorted(ranked.items(), key=lambda item: (-item[1], item[0]))[:24]
    ]


def build_memory_palace(base_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Read the five canonical Memory Palace Markdown files."""
    documents: list[dict[str, Any]] = []
    index: list[dict[str, Any]] = []
    file_hashes: dict[str, str] = {}

    for filename in SOURCE_FILES:
        path = base_dir / filename
        content = path.read_text(encoding="utf-8")
        title = extract_title(content, filename)
        digest = sha256_hex(content)
        sections = split_sections(content)
        file_hashes[filename] = digest

        documents.append(
            {
                "source_file": filename,
                "title": title,
                "sha256": digest,
                "sections": sections,
                "content": content,
            }
        )
        index.append(
            {
                "title": title,
                "keywords": keywords_for(title, content),
                "source_file": filename,
            }
        )

    palace = {
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "file_hashes": file_hashes,
        "documents": documents,
    }
    return palace, index


def main() -> int:
    base_dir = Path(__file__).resolve().parent
    palace, index = build_memory_palace(base_dir)

    palace_path = base_dir / "memory-palace.json"
    index_path = base_dir / "memory-palace-index.json"
    palace_path.write_text(json.dumps(palace, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("Iris Memory Palace build complete.")
    print(f"- Version: {palace['version']}")
    print(f"- Source files: {len(palace['documents'])}")
    print(f"- Output: {palace_path.name}")
    print(f"- Search index: {index_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
