"""Tests for scripts/check_links.py."""

from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest


_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_links.py"
_SPEC = importlib.util.spec_from_file_location("check_links", _MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


def _make_repo(root: Path) -> None:
    """Create a small markdown tree with a target the links can point at."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "TARGET.md").write_text("target\n", encoding="utf-8")


@pytest.mark.parametrize(
    "target",
    [
        "https://example.com/missing",
        "http://example.com/missing",
        "mailto:someone@example.com",
        "tel:+441234567890",
        "#in-page-anchor",
        "//cdn.example.com/asset.js",
    ],
)
def test_resolve_target_skips_external_and_anchor_links(tmp_path, target):
    source = tmp_path / "DOC.md"
    assert _MODULE.resolve_target(source, target) is None


def test_resolve_target_strips_anchor_and_query(tmp_path):
    source = tmp_path / "docs" / "DOC.md"
    resolved = _MODULE.resolve_target(source, "../TARGET.md#a-section")
    assert resolved == tmp_path / "docs" / ".." / "TARGET.md"

    resolved = _MODULE.resolve_target(source, "../TARGET.md?raw=1")
    assert resolved == tmp_path / "docs" / ".." / "TARGET.md"


def test_resolve_target_handles_percent_encoding(tmp_path):
    source = tmp_path / "DOC.md"
    resolved = _MODULE.resolve_target(source, "papers/My%20Paper.pdf")
    assert resolved == tmp_path / "papers" / "My Paper.pdf"


def test_resolve_target_treats_leading_slash_as_repo_root(tmp_path, monkeypatch):
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    source = tmp_path / "docs" / "DOC.md"
    assert _MODULE.resolve_target(source, "/TARGET.md") == tmp_path / "TARGET.md"


def test_extract_targets_finds_inline_reference_and_image_links():
    text = (
        "Inline [one](./A.md) and image ![alt](./B.png).\n"
        "Angle [two](<./C D.md>) and titled [three](./E.md \"Title\").\n"
        "\n"
        "[label]: ./F.md\n"
    )
    targets = [target for target, _ in _MODULE.extract_targets(text)]
    assert targets == ["./A.md", "./B.png", "./C D.md", "./E.md", "./F.md"]


def test_extract_targets_reports_line_numbers():
    text = "line one\n\n[link](./MISSING.md)\n"
    assert _MODULE.extract_targets(text) == [("./MISSING.md", 3)]


def test_extract_targets_ignores_fenced_code_blocks():
    text = (
        "Real [link](./REAL.md).\n"
        "\n"
        "```markdown\n"
        "Illustrative [link](./NOT_REAL.md)\n"
        "```\n"
        "\n"
        "~~~\n"
        "Also [ignored](./ALSO_NOT_REAL.md)\n"
        "~~~\n"
    )
    targets = [target for target, _ in _MODULE.extract_targets(text)]
    assert targets == ["./REAL.md"]


def test_strip_code_blocks_preserves_line_numbering():
    text = "a\n```\nb\nc\n```\nd [link](./X.md)\n"
    stripped = _MODULE.strip_code_blocks(text)
    assert stripped.count("\n") == text.count("\n")
    assert _MODULE.extract_targets(text) == [("./X.md", 6)]


def test_check_file_accepts_resolving_links(tmp_path, monkeypatch):
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    _make_repo(tmp_path)
    doc = tmp_path / "docs" / "DOC.md"
    doc.write_text("See [target](../TARGET.md) and [dir](../docs/).\n", encoding="utf-8")

    errors: list[str] = []
    checked = _MODULE.check_file(doc, errors)

    assert errors == []
    assert checked == 2


def test_check_file_reports_broken_link_with_path_and_line(tmp_path, monkeypatch):
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    _make_repo(tmp_path)
    doc = tmp_path / "docs" / "DOC.md"
    doc.write_text("intro\n\nSee [gone](../MISSING.md).\n", encoding="utf-8")

    errors: list[str] = []
    _MODULE.check_file(doc, errors)

    assert errors == ["docs/DOC.md:3: broken link -> ../MISSING.md"]


def test_check_file_catches_the_double_dot_regression(tmp_path, monkeypatch):
    """A one-level-deep file using ``../../`` escapes the repo. Guard it."""
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    _make_repo(tmp_path)
    doc = tmp_path / "docs" / "DOC.md"
    doc.write_text("[overshoot](../../TARGET.md)\n", encoding="utf-8")

    errors: list[str] = []
    _MODULE.check_file(doc, errors)

    assert len(errors) == 1
    assert "../../TARGET.md" in errors[0]


def test_tracked_markdown_files_lists_only_tracked_files(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "TRACKED.md").write_text("tracked\n", encoding="utf-8")
    (tmp_path / "UNTRACKED.md").write_text("untracked\n", encoding="utf-8")
    subprocess.run(["git", "add", "TRACKED.md"], cwd=tmp_path, check=True)

    original_root = _MODULE.REPO_ROOT
    _MODULE.REPO_ROOT = tmp_path
    try:
        names = [path.name for path in _MODULE.tracked_markdown_files()]
    finally:
        _MODULE.REPO_ROOT = original_root

    assert names == ["TRACKED.md"]


def test_repository_links_all_resolve():
    """The real repository must have no broken relative links."""
    assert _MODULE.main() == 0
