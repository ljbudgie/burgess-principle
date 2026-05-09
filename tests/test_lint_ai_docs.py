"""Tests for scripts/lint_ai_docs.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path


_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "lint_ai_docs.py"
_SPEC = importlib.util.spec_from_file_location("lint_ai_docs", _MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


def _write_valid_ai_docs_tree(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("agent instructions\n", encoding="utf-8")
    (root / "FOR_AI_MODELS.md").write_text(
        "\n".join(_MODULE.DOCTRINAL_MARKERS_FOR_AI_MODELS),
        encoding="utf-8",
    )
    (root / "llms.txt").write_text(
        "# The Burgess Principle\n\n## Getting Started\n\n## Optional\n",
        encoding="utf-8",
    )
    templates = root / "templates"
    templates.mkdir()
    (templates / "ROUTING.md").write_text(
        "Use `CONFIRM_HUMAN_REVIEW.md`, `FOR_AI_MODELS.md`, "
        "`SECTOR_ENERGY.md`, `litigation/WARRANT_DEFECT_IDENTIFIER.md`, "
        "and `papers/PAPER_1.md`.\n",
        encoding="utf-8",
    )
    (templates / "CONFIRM_HUMAN_REVIEW.md").write_text("template\n", encoding="utf-8")
    (root / "litigation").mkdir()
    (root / "litigation" / "WARRANT_DEFECT_IDENTIFIER.md").write_text(
        "litigation\n",
        encoding="utf-8",
    )
    (root / "papers").mkdir()
    (root / "papers" / "PAPER_1.md").write_text("paper\n", encoding="utf-8")


def test_normalise_doctrinal_text_collapses_markdown_wrapping_and_quotes():
    wrapped = """
    > **“Was a human member of the team able to personally review the specific
    > facts of my specific situation?”**
    It’s reviewed.
    """

    assert _MODULE.normalise_doctrinal_text(wrapped) == (
        '"Was a human member of the team able to personally review the specific '
        'facts of my specific situation?" It\'s reviewed.'
    )


def test_lint_for_ai_models_accepts_normalised_binary_test(monkeypatch, tmp_path):
    _write_valid_ai_docs_tree(tmp_path)
    text = (tmp_path / "FOR_AI_MODELS.md").read_text(encoding="utf-8")
    text = text.replace(
        '"Was a human member of the team able to personally review the specific facts of my specific situation?"',
        "> **“Was a human member of the team able to personally review the specific\n"
        "> facts of my specific situation?”**",
    )
    (tmp_path / "FOR_AI_MODELS.md").write_text(text, encoding="utf-8")
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    errors: list[str] = []

    _MODULE.lint_for_ai_models(errors)

    assert errors == []


def test_lint_for_ai_models_reports_each_missing_doctrinal_marker(monkeypatch, tmp_path):
    _write_valid_ai_docs_tree(tmp_path)
    (tmp_path / "FOR_AI_MODELS.md").write_text("### 1 — The Binary Test (core doctrine)\n", encoding="utf-8")
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    errors: list[str] = []

    _MODULE.lint_for_ai_models(errors)

    assert any("doctrinal marker" in error for error in errors)
    assert any("Evaluator Inversion" in error for error in errors)
    assert any("Anti-monetisation guardrails" in error for error in errors)


def test_lint_routing_paths_skips_non_template_and_sector_references(monkeypatch, tmp_path):
    _write_valid_ai_docs_tree(tmp_path)
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    errors: list[str] = []

    _MODULE.lint_routing_paths(errors)

    assert errors == []


def test_lint_routing_paths_reports_missing_template_litigation_and_paper(monkeypatch, tmp_path):
    _write_valid_ai_docs_tree(tmp_path)
    (tmp_path / "templates" / "ROUTING.md").write_text(
        "Use `MISSING_TEMPLATE.md`, `litigation/MISSING_FILE.md`, "
        "and `papers/MISSING_PAPER.md`.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    errors: list[str] = []

    _MODULE.lint_routing_paths(errors)

    assert "templates/ROUTING.md references missing template: templates/MISSING_TEMPLATE.md" in errors
    assert "templates/ROUTING.md references missing litigation file: litigation/MISSING_FILE.md" in errors
    assert "templates/ROUTING.md references missing paper: papers/MISSING_PAPER.md" in errors


def test_lint_llms_txt_reports_missing_required_sections(monkeypatch, tmp_path):
    _write_valid_ai_docs_tree(tmp_path)
    (tmp_path / "llms.txt").write_text("# The Burgess Principle\n", encoding="utf-8")
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)
    errors: list[str] = []

    _MODULE.lint_llms_txt(errors)

    assert "llms.txt is missing the required section heading: '## Getting Started'" in errors
    assert "llms.txt is missing the required section heading: '## Optional'" in errors


def test_main_returns_success_for_valid_tree(monkeypatch, tmp_path, capsys):
    _write_valid_ai_docs_tree(tmp_path)
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)

    assert _MODULE.main() == 0

    assert capsys.readouterr().out == "AI docs lint: OK\n"


def test_main_returns_failure_and_guidance_for_invalid_tree(monkeypatch, tmp_path, capsys):
    _write_valid_ai_docs_tree(tmp_path)
    (tmp_path / "AGENTS.md").unlink()
    monkeypatch.setattr(_MODULE, "REPO_ROOT", tmp_path)

    assert _MODULE.main() == 1

    error = capsys.readouterr().err
    assert "AI docs lint failed:" in error
    assert "AGENTS.md is missing at the repo root" in error
    assert "tag @ljbudgie for review" in error
