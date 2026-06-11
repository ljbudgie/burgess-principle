# Institution Audit Taxonomy — v1.1

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
two auditors scoring the same evidence reach the same number. Score only what
is evidenced in writing. When evidence is genuinely between two anchors, take
the lower score.

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
   *Accessibility NULL*: the review question cannot even be asked.
6. **Re-scoring.** Scores move only on new written evidence. The Verification
   Protocol in [`INSTITUTIONAL_REGISTER.md`](./INSTITUTIONAL_REGISTER.md)
   defines what an institution must provide to move from NULL to SOVEREIGN;
   every change is dated via commit.

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

Changes to dimensions, weights, or bands require a major version bump and
explicit review by @ljbudgie, with existing register entries either re-scored
or clearly marked with their original taxonomy version.
