"""Iris MCP server: the Burgess Principle as tools any MCP client can call.

Runs locally over stdio. Nothing is sent anywhere; every tool works on the
input it is given and on files in this repository.

Install and run::

    pip install -e ".[mcp]"
    iris-mcp

See MCP.md for client configuration.

Privacy: the register lookup returns organisation-level findings only
(institution, sector, finding, score). It never returns the free-text
status or reference columns, which can contain named officers and case
details.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

try:  # MCP Python SDK 2.x
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # MCP Python SDK 1.x
    from mcp.server.fastmcp import FastMCP as _Server

from verify_scrutiny import assess_scrutiny, verify_instrument
from iris.loop_classifier import classify_thread

REPO_ROOT = Path(__file__).resolve().parent
REGISTER_PATH = REPO_ROOT / "institutional_register.csv"
PUBLIC_REGISTER_FIELDS = ("Institution", "Sector", "Finding", "Score")

MARK_FACTS = {
    "mark": "UK00004343685",
    "word": "THE BURGESS PRINCIPLE",
    "type": "UK certification mark",
    "classes": [41, 42, 45],
    "status": "registered",
    "registered_date": "2026-10-09",
    "effective_date": "2026-02-22",
    "certifies": (
        "A named human reviewed the specific facts before the decision was made."
    ),
    "source": "https://github.com/ljbudgie/burgess-principle/blob/main/CERTIFICATION_MARK.md",
    "note": (
        "Holding the mark is a matter of the filed regulations and a granted "
        "licence. This tool states the mark's status; it does not certify anyone."
    ),
}

ADVISORY = (
    "Iris output is advisory. It is not legal advice and not a certification. "
    "A named human must confirm any finding before it is relied on or published."
)

mcp = _Server(
    "iris",
    instructions=(
        "Iris applies the Burgess Principle binary test: a decision is SOVEREIGN "
        "only when a named human with authority personally reviewed the specific "
        "facts before it was made; otherwise it is NULL. NULL is the starting "
        "point for a named review, not a finding that the decision is void. "
        + ADVISORY
    ),
)


def _load_register() -> list[dict[str, str]]:
    with REGISTER_PATH.open(newline="", encoding="utf-8") as handle:
        rows = [
            {field: (row.get(field) or "").strip() for field in PUBLIC_REGISTER_FIELDS}
            for row in csv.DictReader(handle)
        ]
    return [row for row in rows if row["Finding"].upper() != "REMOVED"]


@mcp.tool()
def assess_decision(
    reviewer_name: str | None = None,
    reviewer_role: str | None = None,
    specific_facts_reviewed: bool | None = None,
    review_timing: str | None = None,
    review_notes: str | None = None,
) -> dict[str, Any]:
    """Classify a decision as SOVEREIGN, NULL or AMBIGUOUS under the Burgess Principle.

    Give what the decision-maker's own records show. SOVEREIGN requires a
    named reviewer, their role, confirmation that they reviewed the specific
    facts, and review_timing "before_action". Evidence that review did not
    happen returns NULL; missing evidence returns AMBIGUOUS. Each result
    includes the action needed next.
    """
    try:
        result = assess_scrutiny(
            reviewer_name=reviewer_name,
            reviewer_role=reviewer_role,
            specific_facts_reviewed=specific_facts_reviewed,
            review_timing=review_timing,
            review_notes=review_notes,
        ).to_dict()
    except (TypeError, ValueError) as exc:
        return {"error": str(exc), "advisory": ADVISORY}
    result["advisory"] = ADVISORY
    return result


@mcp.tool()
def classify_correspondence(
    messages: list[dict[str, str]],
    institution: str | None = None,
    named_individual: str | None = None,
) -> dict[str, Any]:
    """Detect institutional delay loops in a correspondence thread.

    Each message needs "date" (YYYY-MM-DD), "sender" and "content_summary";
    optional "direction" ("individual" or "institution") and "reference".
    Detects insufficiency, circular referral, precondition stacking, template
    dismissal, identity loops and channel redirects. The result is
    provisional and must be confirmed by a named human.
    """
    try:
        finding = classify_thread(messages, institution, named_individual).as_dict()
    except ValueError as exc:
        return {"error": str(exc), "advisory": ADVISORY}
    finding["advisory"] = ADVISORY
    return finding


@mcp.tool()
def verify_reasoning_hash(reasoning_text: str, provided_hash: str) -> dict[str, Any]:
    """Check that a decision's recorded reasoning matches its SHA-256 hash.

    Use this to confirm that reasoning text has not changed since it was
    sealed. Returns SOVEREIGN when the hash matches, NULL when it does not.
    """
    result = verify_instrument(reasoning_text, provided_hash).to_dict()
    result["advisory"] = ADVISORY
    return result


@mcp.tool()
def lookup_organisation(name: str) -> dict[str, Any]:
    """Look up an organisation's findings on the Burgess institutional register.

    Matches by case-insensitive substring. Returns organisation-level fields
    only: institution, sector, finding as recorded (for example SOVEREIGN,
    NULL, AMBIGUOUS or PENDING) and score. Removed entries are excluded.
    Individual officers are never returned.
    """
    query = name.strip().lower()
    if len(query) < 3:
        return {"error": "Use at least 3 characters.", "matches": []}
    matches = [row for row in _load_register() if query in row["Institution"].lower()]
    return {
        "query": name,
        "match_count": len(matches),
        "matches": matches[:20],
        "note": (
            "Findings record whether a named human review was evidenced in the "
            "correspondence logged. They are not findings of wrongdoing."
        ),
    }


@mcp.tool()
def register_summary() -> dict[str, Any]:
    """Return counts of each recorded finding across the register, in total and by sector."""
    rows = _load_register()
    by_sector: dict[str, dict[str, int]] = {}
    for row in rows:
        sector = by_sector.setdefault(row["Sector"] or "Unspecified", {})
        sector[row["Finding"]] = sector.get(row["Finding"], 0) + 1
    totals: dict[str, int] = {}
    for row in rows:
        totals[row["Finding"]] = totals.get(row["Finding"], 0) + 1
    return {"organisations": len(rows), "totals": totals, "by_sector": by_sector}


# Actions that, on their own, show a decision bears on an identified person.
# A match always routes the action to a named human, whatever the caller declared.
_PERSON_AFFECTING = re.compile(
    r"\b("
    r"refus\w*|declin\w*|den(?:y|ies|ied|ial)|reject\w*|"
    r"charg\w*|fine[sd]?|penalt\w*|surcharge\w*|"
    r"enforc\w*|bailiff\w*|warrant\w*|summons\w*|liability orders?|"
    r"disconnect\w*|cut off|terminat\w*|cancel\w*|suspend\w*|evict\w*|"
    r"debt\w*|arrears|default\w*|collect\w* (?:(?:the|their|this|that|a|an|his|her|its|my|your) )?(?:debt|payment|balance)|"
    r"credit (?:check|search|report)\w*|identity (?:check|verification)|"
    r"sanction\w*|ban(?:s|ned)?|block\w* (?:(?:the|their|this|that|a|an|his|her|its|my|your) )?(?:account|access|user)|close\w* (?:(?:the|their|this|that|a|an|his|her|its|my|your) )?(?:account|case)|"
    r"dismiss\w*|deduct\w*|recover\w*|repossess\w*|"
    r"refer\w* to (?:police|enforcement|collections?)|report\w* to (?:police|credit)|"
    r"benefit\w*|eligib\w*|appeal\w*|complaint\w*|"
    r"(?:customer|client|tenant|patient|applicant|claimant|resident|employee|account holder)s?"
    r")\b",
    re.IGNORECASE,
)

_REVIEWER_MUST_CONFIRM = [
    "reviewer_name: the named human who will decide",
    "reviewer_role: their role and authority to decide",
    "specific_facts_reviewed: true, once they have personally reviewed this person's specific facts",
    "review_timing: \"before_action\"",
]


@mcp.tool()
def human_checkpoint(
    action: str,
    affects_identified_person: bool | None = None,
) -> dict[str, Any]:
    """Call BEFORE taking an action. Says whether a named human must decide first.

    Describe the action in plain words, for example "refuse the refund on
    order 1234" or "send the weekly newsletter". Set affects_identified_person
    to true or false if you know.

    Returns PROCEED only when you declare that no identified person is
    affected and the description contains nothing that suggests otherwise.
    Returns STOP when a person is affected, when the description suggests one
    may be, or when you have not said. On STOP, pause and pass the decision to
    a named human; once they have reviewed it, record their details with
    assess_decision. Doubt is always resolved in favour of asking a human.
    """
    text = (action or "").strip()
    if not text:
        return {
            "decision": "STOP",
            "reason": "No action was described, so it cannot be cleared.",
            "required_before_action": _REVIEWER_MUST_CONFIRM,
            "advisory": ADVISORY,
        }

    triggers = sorted({m.group(0).lower() for m in _PERSON_AFFECTING.finditer(text)})

    if affects_identified_person is False and not triggers:
        return {
            "decision": "PROCEED",
            "reason": "Declared not to affect an identified person, and nothing in the description suggests otherwise.",
            "triggers": [],
            "advisory": ADVISORY,
        }

    if affects_identified_person is True:
        reason = "Declared to affect an identified person."
    elif affects_identified_person is False:
        reason = (
            "Declared not to affect an identified person, but the description "
            "suggests it may. Treated as affecting a person."
        )
    elif triggers:
        reason = "The description suggests this action affects an identified person."
    else:
        reason = (
            "It was not stated whether this action affects an identified person. "
            "Call again with affects_identified_person set, or pass it to a named human."
        )

    return {
        "decision": "STOP",
        "reason": reason,
        "triggers": triggers,
        "required_before_action": _REVIEWER_MUST_CONFIRM,
        "next_step": (
            "Pause this action and pass it to a named human with authority. "
            "After they have reviewed the specific facts, call assess_decision "
            "with their details. Proceed only if it returns SOVEREIGN."
        ),
        "advisory": ADVISORY,
    }


@mcp.tool()
def certification_mark_status() -> dict[str, Any]:
    """State the registration status of the Burgess Principle certification mark."""
    return dict(MARK_FACTS)


@mcp.resource("iris://framework")
def framework() -> str:
    """The Burgess Principle binary test, in brief."""
    return (
        "The Burgess Principle asks one question of any decision about a person: "
        "did a named human with authority personally review the specific facts "
        "before the decision was made? Yes, evidenced: SOVEREIGN. Not evidenced: "
        "NULL. A signature is not enough; meeting a deadline is not enough; "
        "'I do not recall' is not a no. NULL is the starting point for a named "
        "review, not a finding that the decision is void.\n\n" + ADVISORY
    )


def main() -> None:
    """Run the Iris MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
