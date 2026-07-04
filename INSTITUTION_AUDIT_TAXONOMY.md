# Institution Audit Taxonomy — v1.3

**Canonical definition.** This file is the single authoritative source for the
taxonomy used to score institutions in
[`INSTITUTIONAL_REGISTER.md`](./INSTITUTIONAL_REGISTER.md) and
[`LIVE_AUDIT_LOG.md`](./LIVE_AUDIT_LOG.md).

UK Certification Mark: UK00004343685

---

## Purpose

Every institution on the register is asked one question first:

> **"Was a human member of the team able to personally review the specific
> facts of my specific situation?"**

The binary test produces the headline finding — SOVEREIGN, NULL, or AMBIGUOUS.
The taxonomy then scores *how* the institution responded across five
dimensions, each 0–4, for a total out of 20. The score does not replace the
binary finding; it makes the finding comparable across institutions, sectors,
and time.

---

## Bands

| Band | Score | Meaning |
| --- | --- | --- |
| **NULL** | 0–5 | No meaningful human consideration. Full escalation indicated. |
| **Marginal** | 6–10 | Minimal compliance only. Formal challenge and DSAR pressure warranted. |
| **Partial sovereign** | 11–15 | Some human consideration present. Remedy may be achievable without escalation. |
| **SOVEREIGN** | 16–20 | Full human consideration demonstrated and verifiable. Positive precedent. |

---

## Dimensions and scoring anchors

v1.0 named the five dimensions; v1.1 adds explicit per-score anchors so any
two auditors scoring the same evidence reach the same number; v1.2 adds
interpretation notes for recurring evidence patterns without changing any
anchor; v1.3 adds disability and reasonable-adjustment interpretation notes
on the same basis. Score only what is evidenced in writing. When evidence is
genuinely between two anchors, take the lower score.

### D1 — Response to the Burgess Principle binary question

| Score | Anchor |
| --- | --- |
| 0 | No response, or the question was ignored entirely. |
| 1 | Acknowledgement or deflection without answering — or a substantive answer confirming that no individual review took place (an honest systemic NULL admission). |
| 2 | Partial answer in process language only ("subject to human oversight", "reviewed in line with policy") — AMBIGUOUS. |
| 3 | Direct answer naming a reviewer, but with limited case-specific detail. |
| 4 | Direct written answer confirming a named human individually reviewed the specific facts of the specific case. |

### D2 — Evidence of actual individual human review

| Score | Anchor |
| --- | --- |
| 0 | No evidence of any individual human review. |
| 1 | Generic assertion that review happens, with nothing case-specific. |
| 2 | A named role or team is identified, but no specific facts of the case are referenced. |
| 3 | A named person is identified and some case-specific facts are referenced. |
| 4 | A named person, the specific facts they reviewed, and a verifiable written record. |

### D3 — Timeliness relative to statutory obligation

| Score | Anchor |
| --- | --- |
| 0 | Statutory deadline missed with no response, or deadline still breached at assessment. |
| 1 | Response substantially late against the statutory clock. |
| 2 | Deadline met only after chasing, extension, or regulator pressure. |
| 3 | Response within the statutory deadline without prompting. |
| 4 | Prompt, complete response well within the obligation. |

### D4 — Remedy offered and delivered

| Score | Anchor |
| --- | --- |
| 0 | No remedy offered. |
| 1 | Apology or acknowledgement only. |
| 2 | Partial remedy offered. |
| 3 | Full remedy offered but not yet confirmed delivered. |
| 4 | Full remedy delivered and confirmed in writing. |

### D5 — Recurrence / systemic change

| Score | Anchor |
| --- | --- |
| 0 | No systemic acknowledgement; recurrence likely or already observed. |
| 1 | The systemic issue is acknowledged, with no commitment to change. |
| 2 | A commitment to change is stated but not evidenced. |
| 3 | A documented process change has been made. |
| 4 | Verified systemic change that prevents recurrence. |

### Interpretation notes for recurring evidence patterns (v1.2)

These notes do not change any anchor. They record how the existing anchors are
applied to evidence patterns that recur across the register, so any two
auditors reach the same number.

- **Template letters.** A response that is recognisably a standard template —
  identical or near-identical wording across cases, merge fields, no reference
  to the specific facts raised — is generic by definition. It caps D2 at 1
  ("generic assertion that review happens, with nothing case-specific") even
  where it arrives quickly or is signed with a name. A printed signature on a
  template is not evidence that the signatory reviewed the case.
- **Weasel responses.** Process language that asserts oversight without
  answering the binary question ("decisions are subject to human oversight",
  "handled in line with our policy", "reviewed by our team") scores D1 at
  most 2 (AMBIGUOUS). It does not score 3 or 4, because no reviewer is named
  and no case-specific fact is engaged.
- **Speed is not review.** A fast response scores well on D3 only. Timeliness
  never compensates for a low D2: a prompt template letter is still a template
  letter. The headline finding follows the binary test, not the clock.
- **Delegated self-investigation.** Where the team responsible for the
  decision investigates itself with no independent named reviewer, D2 scores
  at most 2 (a named role or team, no independent case-specific review).

### Evidence guidance for AI-involved processes (v1.2)

Where the institution's decision process involves an automated or AI system,
the same five dimensions apply unchanged — the binary test does not have an
AI exception. The following written evidence, where it exists, supports the
higher D1/D2 anchors:

- A named human reviewer for the specific decision, not a generic
  "human-in-the-loop" assurance (which is anchor D1 = 2, AMBIGUOUS).
- The audit trail or log entry showing what the named human saw, when, and
  what they decided — including any record of an override of the automated
  output.
- Confirmation of what the reviewer could actually change: a human who cannot
  depart from the automated recommendation is not exercising individual
  review.

This aligns with the meaningful-human-involvement expectations in UK GDPR
Article 22, the EU AI Act human-oversight provisions, and the NIST AI RMF
mappings in the foundational paper. Absence of such records is itself
evidence: an institution that cannot produce them cannot evidence D2 above 1.

### Sector context notes (v1.2 — non-scoring)

The dimensions, anchors, and bands are universal and are not adjusted by
sector: a 20-point SOVEREIGN means the same thing everywhere. Sector context
informs *expectation and escalation*, not the score:

- **Public authorities and regulated entities** (benefits, enforcement,
  utilities, financial services) operate under statutory duties. A NULL or
  Marginal finding here warrants faster escalation to the relevant regulator
  or ombudsman than the same score in a routine commercial dispute.
- **High-stakes decisions** (loss of income, housing, credit, enforcement
  action, medical access) justify recording the stake alongside the score in
  the register entry, so patterns of NULL findings in high-stakes contexts
  are visible.
- **Routine commercial disputes** are scored identically; the score simply
  carries less escalation urgency.

Sector context is recorded in the Accountability Profile (below), never as a
multiplier or modifier of the numeric score.

### Disability and reasonable adjustments (v1.3)

A disclosed disability, a disclosed vulnerability, or a requested reasonable
adjustment is a **specific fact of the case**. The existing anchors already
turn on whether the specific facts were engaged; these notes record how that
applies when one of the specific facts is the individual's disability, so any
two auditors reach the same number. No anchor changes.

- **D1 — the binary question includes the disability.** Where a disability or
  adjustment need was disclosed in writing, a "direct answer" for D1 = 3–4
  must engage the case *as raised* — including the disability. A named
  reviewer who answers the binary question but is silent on a disclosed
  disability central to the complaint has given limited case-specific detail:
  D1 caps at 3.
- **D2 — review that ignores a disclosed disability is not case-specific
  review.** A written response that does not acknowledge a disclosed
  disability, vulnerability, or pending reasonable-adjustment request has not
  referenced the specific facts of the case: D2 caps at 2 (named role or
  team, no case-specific facts), regardless of how much else it covers. To
  reach D2 = 3–4 the written record must show the named reviewer saw and
  considered the disclosed disability and any adjustment requested.
- **D3 — the statutory clock does not pause for access barriers the
  institution created.** Where the individual's response time was extended by
  the institution's own failure to provide a requested adjustment (e.g.
  refusing an accessible format, insisting on a channel the person cannot
  use), that delay is the institution's, not the individual's. It does not
  improve the institution's D3, and time the individual lost to the barrier
  is disregarded when assessing whether the institution responded "without
  prompting".
- **D4 — remedy must include the adjustment.** Where a reasonable adjustment
  was requested, a remedy that resolves the substantive issue but leaves the
  adjustment unmet is a partial remedy: D4 caps at 2. "Full remedy delivered"
  (D4 = 4) requires the adjustment delivered and confirmed in writing
  alongside the substantive remedy.
- **D5 — repeat adjustment failures are systemic.** A repeated failure to
  apply an adjustment the institution has already been told about (re-sending
  inaccessible formats, re-routing to a barred channel, requiring the same
  disclosure again) is direct evidence of no systemic change: D5 = 0. Under
  the Equality Act 2010 the duty to make reasonable adjustments is
  anticipatory for service providers — an institution that only reacts, per
  contact, after the same disclosure has not made a process change.

**Relationship to Accessibility NULL (scoring rule 5).** Accessibility NULL
covers the case where the barrier prevents the question being asked at all.
These notes cover the case where the question *was* asked and answered, but
the disability was scored out of the "specific facts". Both are recorded;
they are complementary, not alternatives.

**Accountability Profile.** Where a disability or adjustment was disclosed,
the entry's Accountability Profile records: what was disclosed, what
adjustment was requested, and whether it was acknowledged, delivered, or
ignored — so adjustment-failure patterns are visible across the register.

---

## Scoring rules

1. **Evidence in writing only.** Telephone assurances, verbal commitments, and
   inferred intentions score 0 on the relevant dimension until documented.
2. **Provisional findings.** Where statutory clocks are still running or a
   response is pending, the finding is marked *provisional* (e.g. "NULL
   (provisional)") and re-scored when the position settles.
3. **What is not scored.** Constructive engagements, partnership outreach,
   parliamentary contacts, and submissions to reform bodies are documented but
   not scored — they are not NULL/SOVEREIGN tests of an institution exercising
   power over an individual.
4. **Clean negative.** An institution that properly confirms it holds no
   records on the individual is recorded as a *clean negative* (N/A), not
   scored — a correct institutional response, not a finding either way.
5. **Accessibility NULL.** Where an institution cannot be reached at all
   through its published routes (bounced complaint addresses, no working
   contact for a disabled person's reasonable-adjustment request), record an
   *Accessibility NULL*: the review question cannot even be asked. Where the
   failed route was a reasonable-adjustment request, note this in the entry —
   an Accessibility NULL of that kind is also a potential failure of the
   Equality Act 2010 duty to make reasonable adjustments, and the entry
   should record the adjustment requested and the failure in writing.
6. **Re-scoring.** Scores move only on new written evidence. The Verification
   Protocol in [`INSTITUTIONAL_REGISTER.md`](./INSTITUTIONAL_REGISTER.md)
   defines what an institution must provide to move from NULL to SOVEREIGN;
   every change is dated via commit.
7. **Accountability Profile.** Each scored register entry should carry, next
   to the numbers, a one-to-three-sentence written summary of the pattern the
   scores show (e.g. "Strong on remedy once escalated; binary question never
   answered; systemic NULL drift evident across repeat contacts."). The
   profile is descriptive, not scored: it records what the numbers alone
   cannot — the shape of the institution's response — and makes patterns
   visible across the register.

---

## Aggregate statistics (register-level)

To support research and pattern detection, the register maintains simple
aggregate figures derived from the scored entries (see the summary table in
[`INSTITUTIONAL_REGISTER.md`](./INSTITUTIONAL_REGISTER.md)):

- mean taxonomy score across scored institutions, dated;
- NULL prevalence (proportion of scored entries in the NULL band);
- sector breakdowns where enough entries exist to be meaningful.

Aggregates are recomputed when entries change and are always dated. They
describe the register as evidence gathered to date; they are not projections.

---

## Extensibility and backward compatibility

- **Minor versions (v1.x)** are additive only: anchors clarified,
  interpretation notes added, non-scoring guidance introduced. Dimensions,
  weights, and bands never change in a minor version, so every score recorded
  under any v1.x remains valid without re-scoring.
- **Major versions (v2.0+)** may change dimensions, weights, or bands. Any
  major version must ship with an explicit mapping from old scores to new
  (or a statement that old entries retain their original taxonomy version
  label), so no historical finding is silently invalidated.
- **Proposals.** Anyone may propose a change by pull request. Doctrinal
  control rests with @ljbudgie, who has final review on any change to
  dimensions, weights, bands, or anchors (see `AGENTS.md`).

---

## Worked examples

**Wave Utilities — SOVEREIGN (16/20): D1 4, D2 4, D3 3, D4 4, D5 1.**
Direct answer; named case handler; specific facts cited; both accounts cleared
to £0.00 with fees removed (D4 4); within deadline but after the matter was
raised (D3 3); no evidence of systemic change beyond the individual case
(D5 1).

**E.ON Next — NULL (1/20): D1 0, D2 0, D3 0, D4 1, D5 0.**
Binary question not answered (D1 0); no individual review evidenced (D2 0);
field team investigated themselves; letter of apology offered (D4 1); no
systemic change (D5 0).

---

## Versioning

| Version | Date | Change |
| --- | --- | --- |
| v1.0 | 2025–2026 register | Five dimensions (D1–D5, 0–4 each) and four bands defined inline in the register and audit log. |
| v1.1 | June 2026 | Canonical standalone file. Adds explicit per-score anchors for each dimension and codifies the scoring rules already in practice (provisional findings, clean negative, Accessibility NULL, evidence-in-writing). **Additive only** — dimensions, weights, and bands are unchanged, so every score recorded under v1.0 remains valid without re-scoring. |
| v1.2 | July 2026 | Interpretation notes for recurring evidence patterns (template letters, weasel responses, speed-is-not-review, delegated self-investigation); evidence guidance for AI-involved processes; non-scoring sector context notes; Accountability Profile; Equality Act cross-link for Accessibility NULL; register-level aggregate statistics; extensibility protocol. **Additive only** — dimensions, weights, bands, and anchors are unchanged, so every score recorded under v1.0 or v1.1 remains valid without re-scoring. |
| v1.3 | July 2026 | Disability and reasonable-adjustment interpretation notes: a disclosed disability is a specific fact of the case, so responses that ignore it cap D1/D2; unmet adjustments cap D4; institution-created access barriers do not improve D3; repeat adjustment failures score D5 = 0. Accountability Profile records disclosure and adjustment status. **Additive only** — dimensions, weights, bands, and anchors are unchanged, so every score recorded under v1.0–v1.2 remains valid without re-scoring. |

Changes to dimensions, weights, or bands require a major version bump and
explicit review by @ljbudgie, with existing register entries either re-scored
or clearly marked with their original taxonomy version.

---

## Appendix — v2.0 draft proposal (NOT IN FORCE)

> **Status: draft for discussion only.** Nothing in this appendix changes how
> any entry is scored today. Adopting any part of it is a major version bump
> requiring explicit review and approval by @ljbudgie, and a published mapping
> from v1.x scores.

Two candidate changes, prompted by external review, are recorded here so they
can be evaluated against real register entries before any adoption decision:

1. **Weighted D2.** Re-scale D2 (evidence of actual individual human review)
   to 0–8 — it is the dimension closest to the essence of the binary test —
   for a total out of 24, with bands re-scaled proportionally (NULL 0–6,
   Marginal 7–12, Partial sovereign 13–18, SOVEREIGN 19–24). Rationale: a
   fast, vague response (high D3, low D2) should not outscore a thorough but
   slower one. Counter-consideration: the v1.2 interpretation notes already
   cap D2 for templates and weasel responses, and the headline finding —
   which follows the binary test, not the score — already carries the weight
   the score cannot.
2. **D6 — Depth of review / reasoning transparency (0–4).** A sixth dimension
   distinguishing boilerplate sign-off from case-specific rationale: did the
   written response engage the key facts, vulnerabilities, and any reasonable
   adjustments raised? Counter-consideration: much of this is already priced
   into the D1/D2 anchors (case-specific detail is what separates 3–4 from
   0–2); a sixth dimension adds nuance at the cost of comparability with 30+
   existing entries.

The evaluation standard for adoption is the project's own: does the change
make it easier or harder to determine whether a named human personally
reviewed the specific facts of a specific case? Stability aids adoption and
comparability; neither change should be adopted unless it demonstrably
sharpens that determination on real evidence.
