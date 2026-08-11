# /loop — Institutional Delay Pattern Classifier

`/loop` classifies correspondence a person already holds for a repeatable delay
pattern. It is local-first and advisory only: Iris produces a provisional
finding, and a named human must confirm it before it is recorded or published.
It does not decide the underlying case, determine lawfulness, or replace the
Burgess SOVEREIGN / NULL / AMBIGUOUS assessment.

## First-run walkthrough

New users should open
[`loop-storyboard.html`](../../../loop-storyboard.html) before building JSON by
hand. The storyboard shows six sample delay patterns (plus a no-loop control),
a correspondence timeline with calendar days, the dual signal panel (**delay
pattern** separate from **accountability**), and a confirmation gate before
copying a draft register entry. Sample threads live in
[`examples/loop-storyboard-samples.json`](../../../examples/loop-storyboard-samples.json).
Paste-your-own and “Re-run via local `/loop/classify`” need Iris local or
another host serving the classify endpoint.

## When to use it

Use `/loop/classify` when a correspondence thread shows repetition, referral,
new conditions, template responses, identity demands, or inaccessible channel
instructions. Supply messages in date order where possible, with `date`,
`sender`, `content_summary`, optional `reference`, and `direction`
(`individual` or `institution`).

The output starts with **LOOP DETECTED** or **NO LOOP**, then identifies the
type, complete cycles, elapsed calendar days, evidence references, and the
separate SOVEREIGN / NULL accountability signal for the person or system
running the pattern. Supply `named_individual` only when a human has verified
that person's responsibility; Iris does not infer a person from an
organisation's sender name.

## The six delay patterns

| Type | Signal | Casework example |
| --- | --- | --- |
| `insufficiency` | Repeated demands for more information after the person has answered. | Darlington Borough Council correspondence seeking financial information during a 30-day enforcement hold. |
| `circular_referral` | A route sends the person back to a prior route without resolving the issue. | EHRC → EASS → EHRC correspondence with no available route. |
| `precondition_stacking` | The institution says it cannot act until another matter is complete. A human must verify whether that asserted precondition is lawful. | DBC treating a separate Council Tax Support review as a condition for considering s.13A(1)(c) discretionary relief. |
| `template_dismissal` | Identical or near-identical responses to materially different correspondence. | Ethics and Integrity Commission acknowledgements sent nine minutes apart; VWFS stating “all points addressed” while questions remained unanswered. |
| `identity_loop` | Identity verification is demanded again after the person has already provided or confirmed identity. | Experian requiring report viewing before discussing a disputed account and Notice of Correction. |
| `channel_redirect` | An institution redirects to telephone or in-person contact after an email-only or written-only adjustment is recorded. | Telephone defaulting despite an established email-only reasonable adjustment. |

## Confirmation and publication

Before publishing a finding, a named human should check the full correspondence,
the detector's references and count, dates, whether the pattern is complete,
and whether any named person actually controlled the delay. Confirmed findings
may use [`templates/LOOP_FINDING_REGISTER_ENTRY.md`](../../../templates/LOOP_FINDING_REGISTER_ENTRY.md).

The finding remains separate from the underlying decision's Burgess outcome:
for example, “LOOP DETECTED — insufficiency, 21 days; accountability: NULL”
records both the delay pattern and that no named individual was identified as
responsible for it.
