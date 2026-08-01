"""Tests for scripts/check_doc_coverage.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


_MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "check_doc_coverage.py"
)
_SPEC = importlib.util.spec_from_file_location("check_doc_coverage", _MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


@pytest.mark.parametrize(
    ("markdown", "expected"),
    [
        ("[Tier one](./CORE.md)", {"CORE.md"}),
        ("[Tier one](CORE.md)", {"CORE.md"}),
        ("[Anchored](./CORE.md#the-admission-rule)", {"CORE.md"}),
        ("[Directory](./templates/)", {"templates"}),
        ("[Angle](<./CORE.md>)", {"CORE.md"}),
        ('[Titled](./CORE.md "Core")', {"CORE.md"}),
    ],
)
def test_linked_targets_normalises_relative_links(tmp_path, monkeypatch, markdown, expected):
    (tmp_path / "DOC.md").write_text(markdown + "\n", encoding="utf-8")
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    assert _MODULE.linked_targets("DOC.md") == expected


@pytest.mark.parametrize(
    "markdown",
    [
        "[External](https://example.com/CORE.md)",
        "[Mail](mailto:someone@example.com)",
        "[Phone](tel:+441234567890)",
        "[Anchor only](#the-admission-rule)",
        "CORE.md mentioned in prose only",
        "`CORE.md` in backticks is not a link",
    ],
)
def test_linked_targets_ignores_non_relative_and_prose(tmp_path, monkeypatch, markdown):
    (tmp_path / "DOC.md").write_text(markdown + "\n", encoding="utf-8")
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    assert _MODULE.linked_targets("DOC.md") == set()


def _write_maps(root: Path, tiers: str, navigation: str) -> None:
    (root / "TIERS.md").write_text(tiers, encoding="utf-8")
    (root / "NAVIGATION.md").write_text(navigation, encoding="utf-8")


def test_main_passes_when_every_document_is_mapped(tmp_path, monkeypatch, capsys):
    _write_maps(
        tmp_path,
        "[README](./README.md) [TIERS](./TIERS.md) [NAV](./NAVIGATION.md)\n",
        "[README](./README.md) [TIERS](./TIERS.md) [NAV](./NAVIGATION.md)\n",
    )
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        _MODULE,
        "tracked_markdown",
        lambda: [Path("README.md"), Path("TIERS.md"), Path("NAVIGATION.md")],
    )

    assert _MODULE.main() == 0
    assert "Doc coverage: OK" in capsys.readouterr().out


def test_main_reports_a_document_missing_from_tiers(tmp_path, monkeypatch, capsys):
    _write_maps(
        tmp_path,
        "[TIERS](./TIERS.md) [NAV](./NAVIGATION.md)\n",
        "[README](./README.md) [TIERS](./TIERS.md) [NAV](./NAVIGATION.md)\n",
    )
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        _MODULE,
        "tracked_markdown",
        lambda: [Path("README.md"), Path("TIERS.md"), Path("NAVIGATION.md")],
    )

    assert _MODULE.main() == 1
    output = capsys.readouterr().out
    assert "README.md is not placed in a tier" in output


def test_main_reports_a_directory_missing_from_navigation(tmp_path, monkeypatch, capsys):
    _write_maps(
        tmp_path,
        "[TIERS](./TIERS.md) [NAV](./NAVIGATION.md) [templates](./templates/)\n",
        "[TIERS](./TIERS.md) [NAV](./NAVIGATION.md)\n",
    )
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        _MODULE,
        "tracked_markdown",
        lambda: [
            Path("TIERS.md"),
            Path("NAVIGATION.md"),
            Path("templates/ROUTING.md"),
        ],
    )

    assert _MODULE.main() == 1
    assert "templates/ is not indexed" in capsys.readouterr().out


def test_main_skips_exempt_directories(tmp_path, monkeypatch, capsys):
    _write_maps(
        tmp_path,
        "[TIERS](./TIERS.md) [NAV](./NAVIGATION.md)\n",
        "[TIERS](./TIERS.md) [NAV](./NAVIGATION.md)\n",
    )
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(
        _MODULE,
        "tracked_markdown",
        lambda: [
            Path("TIERS.md"),
            Path("NAVIGATION.md"),
            Path(".github/copilot-instructions.md"),
        ],
    )

    assert _MODULE.main() == 0
    assert "Doc coverage: OK" in capsys.readouterr().out


def test_repository_documents_are_all_mapped():
    """The real repository must satisfy its own coverage rule."""
    assert _MODULE.main() == 0
