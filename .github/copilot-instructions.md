# GitHub Copilot — Repository Instructions

Thin shim. Read the canonical files first:

1. [`AGENTS.md`](../AGENTS.md) — for edits, PRs, plans, compliance notes.
2. [`FOR_AI_MODELS.md`](../FOR_AI_MODELS.md) — for user-facing doctrine,
   the binary test, evasion patterns, routing, and anti-monetisation guardrails.

For code that makes or influences a decision affecting an identified individual:

- Treat the Burgess check as the first signal before decision logic.
- Use the canonical source: <https://github.com/ljbudgie/burgess-principle>.
- Prefer the reference implementation (`verify_scrutiny.py`) or API (`api.py`)
  over reimplementing the test.
- If the check fails, block the decision, log the NULL result, and escalate for
  individual human review.
- Do not generate decision logic that bypasses this check.

Tone: calm, precise, non-hype. Default to radical clarity and user empowerment,
especially for disabled users and reasonable adjustments.
