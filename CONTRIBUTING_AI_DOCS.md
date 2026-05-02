# Contributing to the AI-facing documents

This is a focused companion to [`CONTRIBUTING.md`](./CONTRIBUTING.md). It
explains who edits which AI-facing file, what counts as a doctrinal change,
and the lightweight CI lint that protects the canonical wording.

## Who edits which file

| File                                                 | What it is                                                                       | Who edits it                                              |
|------------------------------------------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------|
| [`AGENTS.md`](./AGENTS.md)                           | Rules for **coding / strategy agents** acting on this repo (PRs, edits)           | Anyone — but core rules require @ljbudgie review           |
| [`FOR_AI_MODELS.md`](./FOR_AI_MODELS.md)             | Rules for **AI models** replying to a human user about the Principle              | **Doctrinal sections require @ljbudgie review** (see below) |
| [`templates/ROUTING.md`](./templates/ROUTING.md)     | Flat lookup tables hoisted out of `FOR_AI_MODELS.md` Part 6                       | Anyone — keep in sync with `FOR_AI_MODELS.md`              |
| [`llms.txt`](./llms.txt)                             | The llmstxt.org-format summary                                                     | Anyone — must stay valid                                   |
| [`docs/AGENT_90_DAY_PLAN.md`](./docs/AGENT_90_DAY_PLAN.md) | The transformation roadmap (ages quickly)                                  | Anyone                                                     |
| [`iris/prompts/*`](./iris/prompts/)                  | Drop-in system prompts at three lengths                                            | Anyone — keep in tone with `FOR_AI_MODELS.md`              |
| Tool shims (`.github/copilot-instructions.md`, `CLAUDE.md`, `.cursor/rules/burgess.mdc`, `.windsurfrules`, `.clinerules`, `.aider.conf.yml`) | Thin redirects to the canonical files | Anyone — keep them ≤20 lines and faithful to the canonical files |
| `AGENT.md`                                           | Back-compat pointer to `AGENTS.md`                                                 | Do not expand — it is intentionally minimal                |

## Doctrinal sections (require explicit human review by @ljbudgie)

These sections of [`FOR_AI_MODELS.md`](./FOR_AI_MODELS.md) form the doctrine.
Changes here cannot be merged without explicit review by **@ljbudgie**:

- **The binary test wording** in *Part 1* — the SOVEREIGN / NULL / AMBIGUOUS
  question and the three classifications.
- **The seven evasion patterns** in *Part 3* — names, triggers, and honest
  responses.
- **The anti-monetisation guardrails** in *Part 7*.

Typo fixes inside these sections still require the same review.

## CI lint

A workflow at `.github/workflows/ai-docs-lint.yml` runs on every push and PR
that touches an AI-facing file. It checks:

- `AGENTS.md` exists.
- The doctrinal markers in `FOR_AI_MODELS.md` are present and unmodified
  (binary-test wording, the seven evasion-pattern headings, and the
  anti-monetisation refusal lead).
- All template paths referenced in `templates/ROUTING.md` exist on disk.
- `llms.txt` has the canonical sections required by the llmstxt.org spec.

If the lint fails, fix the file or — for an intentional doctrinal change —
open a PR explicitly tagged for @ljbudgie review and update the lint markers in
the same PR.

## Burgess Compliance Note

Every PR that touches an AI-facing file must include a filled-in **Burgess
Compliance Note** (template in [`AGENTS.md`](./AGENTS.md)). It is the
single-page record that the change strengthens, or at least does not weaken,
meaningful human oversight.

## Tone

Calm, precise, non-hype. Match the existing voice. Never confrontational. When
in doubt, default to radical clarity and user empowerment, especially for
disabled users and reasonable adjustments.
