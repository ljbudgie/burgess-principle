"""Single-source-of-truth check for the Iris system prompt.

iris/system-prompt.md is the canonical prompt. iris.html must embed it
verbatim inside `<script id="iris-system-prompt" type="text/plain">…</script>`
so that the cloud-mode static deploy and the local-mode server both surface
the same prompt without any divergent inline JS string literal.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "iris" / "system-prompt.md"
IRIS_HTML_PATH = ROOT / "iris.html"
SCRIPT_OPEN = '<script id="iris-system-prompt" type="text/plain">'
SCRIPT_CLOSE = "</script>"


def _embedded_prompt(html: str) -> str:
    start = html.index(SCRIPT_OPEN) + len(SCRIPT_OPEN)
    end = html.index(SCRIPT_CLOSE, start)
    return html[start:end]


def test_canonical_prompt_file_exists_and_is_non_trivial():
    text = PROMPT_PATH.read_text(encoding="utf-8")
    assert "Iris" in text
    assert "Burgess Principle" in text
    assert len(text.strip()) > 500


def test_iris_html_embeds_the_canonical_prompt_verbatim():
    canonical = PROMPT_PATH.read_text(encoding="utf-8")
    html = IRIS_HTML_PATH.read_text(encoding="utf-8")
    assert SCRIPT_OPEN in html, (
        "iris.html must contain <script id=\"iris-system-prompt\" type=\"text/plain\">"
        " — the cloud-mode build serves iris.html as a static file and relies on this"
        " script tag carrying the canonical prompt."
    )
    embedded = _embedded_prompt(html)
    assert embedded.strip() == canonical.strip(), (
        "iris.html's embedded #iris-system-prompt drifted from iris/system-prompt.md."
        " Re-copy the file contents into the script tag."
    )


def test_iris_html_has_no_competing_inline_prompt_literal():
    html = IRIS_HTML_PATH.read_text(encoding="utf-8")
    # The previous divergent inline literal, removed for single-source-of-truth.
    assert 'const SYSTEM_PROMPT = "You are Iris' not in html
