import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")


def test_readme_is_renderable_markdown_not_encoded_blob():
    assert README.startswith(
        '<a href="./iris.html">Talk to Iris</a> — open in your browser, no account or install needed.'
    )
    assert "# The Burgess Principle" in README
    assert "\ufffd" not in README
    assert len(README.splitlines()) > 100

    long_base64_only_lines = [
        line
        for line in README.splitlines()
        if len(line.strip()) > 200 and re.fullmatch(r"[A-Za-z0-9+/=]+", line.strip())
    ]
    assert long_base64_only_lines == []


def test_readme_keeps_required_public_structure_in_order():
    required_sections = [
        "# The Burgess Principle",
        "## Why this exists",
        "## The test",
        "## Statutory convergence: Articles 22A–22D UK GDPR",
        "## Current status",
        "## Iris — your sovereign AI companion",
        "## Quick start",
        "## Repository map",
        "## Contributing",
        "## Important notes",
        "## Licence",
    ]

    positions = [README.index(section) for section in required_sections]
    assert positions == sorted(positions)


def test_readme_keeps_burgess_first_agent_block_intact():
    assert README.count("<!-- BURGESS-FIRST AGENT — one-line copy-paste block -->") == 1
    assert README.count("<!-- /BURGESS-FIRST AGENT -->") == 1
    assert README.index("<!-- BURGESS-FIRST AGENT") < README.index("# The Burgess Principle")

    agent_line = (
        "SYSTEM: Before any action affecting an identified individual, run the Burgess Principle binary test"
    )
    assert agent_line in README
    assert "Produce no output, tool call, draft, or recommendation until the gate returns SOVEREIGN." in README
    assert "On NULL or AMBIGUOUS: refuse the underlying decision, log the result, and escalate to a named human reviewer." in README
    assert "[`templates/BURGESS_FIRST_AGENT.md`](./templates/BURGESS_FIRST_AGENT.md)" in README


def test_readme_repository_map_keeps_core_navigation_targets():
    for target in [
        "<START_HERE.md>",
        "<FAQ.md>",
        "<FOR_AI_MODELS.md>",
        "<STATUS.md>",
        "<templates/>",
        "<papers/>",
    ]:
        assert target in README
