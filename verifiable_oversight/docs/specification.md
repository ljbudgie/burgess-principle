# Verifiable Human Oversight — Specification

**Version:** 0.1.0  
**Status:** MVP / Phase 1  
**Authority:** Burgess Principle (Lewis James Burgess)  
**Legal grounding:** EA 2010 ss.6/19/20/21/27/29/136/149; DUAA 2025 s.80; Ahmed [2010] UKSC 5; Majera [2021] UKSC 46

---

## 1. The Core Question

> "Was a named human being's mind applied to the specific facts of a specific person's case before institutional power was exercised?"

This is the Burgess Binary Test. It has two possible answers: **SOVEREIGN** or **NULL**. A third state, **AMBIGUOUS**, applies when the assessor cannot determine which of those two applies because the institution has not yet provided the necessary information.

The test does not assess whether the decision was correct. A named individual who applied their mind and reached the wrong conclusion is a SOVEREIGN process that is legally challengeable on its merits. An anonymous automated system that reached the right outcome is a NULL process that is unlawful regardless of the outcome.

---

## 2. The Five Elements

All five must be satisfied for a SOVEREIGN verdict. The absence of any single element yields NULL (or AMBIGUOUS if the element's status is genuinely unknown).

| Element | What it requires | Common failure modes |
|---|---|---|
| **Named person** | The full name of the individual who made or reviewed the decision | "Our team", "the relevant department", "case handler", anonymous portal |
| **Role and authority** | Their role AND the authority to reach a different outcome | Role stated but no authority to differ; rubber-stamp reviewer |
| **Specific facts considered** | Concrete evidence that the specific facts of this person's case were considered | Templated response; bulk processing; algorithmic output without individual review |
| **Pre-decision timing** | Review took place before the decision was exercised | Post-hoc audit of automated decision; retrospective ratification |
| **Authority to differ** | The named person had practical and institutional authority to reach a different conclusion | Internal policy constrained the outcome regardless of review |

### 2.1 Process language does not satisfy any element

The following phrases, and equivalents, satisfy zero elements:

- "Reviewed by our team"
- "Subject to human oversight"
- "Considered by the relevant department"
- "Our systems have been reviewed by qualified professionals"
- "A human is always involved in our process"

A follow-up question is always required: *"Please provide the full name, job title, and the specific facts they considered before this decision was reached."*

### 2.2 The involvement / review distinction

DUAA 2025 s.80 sets the statutory floor: a decision is based solely on automated processing if there is no **meaningful human involvement** in the taking of the decision.

The Burgess standard is higher: **meaningful human review** — all five elements present.

| Level | Requirement | Source |
|---|---|---|
| Statutory floor | Meaningful human involvement | DUAA 2025 s.80 |
| Burgess standard | All five elements: named, role, specific facts, pre-decision, authority | This specification |

Involvement without review = AMBIGUOUS or NULL depending on what the institution confirms.

---

## 3. Verdicts

### SOVEREIGN
All five elements are satisfied and documented. The record is sealed with a SHA-256 fingerprint. A SOVEREIGN record does not mean the decision was correct — it means the process meets the minimum standard for accountable institutional decision-making.

### NULL
One or more elements are absent, or the institution has confirmed (by silence following a direct question, by templated response, or by admission) that no named individual reviewed the specific facts. A NULL decision is unlawful where legislation requires human review. Under Ahmed [2010] UKSC 5 and Majera [2021] UKSC 46, an unlawful act cannot found enforceable rights against an individual regardless of the label used.

### AMBIGUOUS
The element's status is genuinely unknown because the institution has not yet responded to a direct question. AMBIGUOUS is a temporary state — it becomes NULL once the institution confirms no named review occurred, or SOVEREIGN once they provide a named individual and the remaining elements.

**AMBIGUOUS is not a safe harbour for institutions.** The follow-up question must be asked and answered. Silence on a direct question is treated as NULL after a reasonable period.

---

## 4. Scoring

The score (0–5) counts the number of elements present. It is informational — any score below 5 yields NULL or AMBIGUOUS. There is no partial credit. A 4/5 score is not "nearly SOVEREIGN" — it is NULL.

---

## 5. Decision Records

Every assessment produces a `DecisionRecord` containing:

- **record_id**: UUID4 — unique identifier
- **domain**: The domain of the decision (general, communication, legal, etc.)
- **subject**: What was assessed
- **institution**: Whose decision was assessed
- **binary_test**: The five-element inputs
- **result**: Verdict, score, elements_present, missing_elements, reasoning
- **fingerprint**: SHA-256 of canonical content — tamper detection
- **signature**: Reserved for Ed25519 / PQC signing (future phase)

Records are immutable once sealed. The fingerprint allows any party to verify the record has not been altered since creation.

---

## 6. Domains

The system is domain-aware. Each domain extends the core test with:

- Domain-specific metadata fields
- Additional validation rules
- Guidance for assessors

| Domain | Status | Key additions |
|---|---|---|
| `general` | Stable | No extensions — pure binary test |
| `communication` | Stable | Channel accessibility, RA on record, automated comms detection |
| `legal` | Stable | Statutory basis, case reference, burden shift, bulk process flag |
| `banking` | Planned | FCA DISP deadlines, FSCS eligibility, automated credit decisions |
| `medical` | Planned | Clinical decision support, consent, Mental Capacity Act |

---

## 7. Cryptographic Integrity (Phase 2)

The `fingerprint` field provides content integrity — it detects if a record has been tampered with after sealing.

The `signature` field is reserved for asymmetric signing (Ed25519 or post-quantum equivalent). When wired up, a signed record provides:

- **Non-repudiation**: the assessor cannot deny creating the record
- **Third-party verifiability**: any party can verify the signature against the assessor's public key
- **Chain of custody**: records can be chained (each record references the fingerprint of the previous record in a sequence)

This is intentionally not implemented in Phase 1. The data model is designed to accept it without structural changes.

---

## 8. Legal Grounding

| Authority | Relevance |
|---|---|
| EA 2010 ss.6/19/20/21 | Disability discrimination; indirect discrimination; duty to make adjustments |
| EA 2010 s.27 | Victimisation — detriment following protected act |
| EA 2010 s.136 | Evidential burden shift in discrimination proceedings |
| EA 2010 s.149 | Public Sector Equality Duty — anticipatory, not reactive |
| DUAA 2025 s.80 | Statutory definition of automated processing; meaningful human involvement floor |
| Ahmed [2010] UKSC 5 | Unlawful act cannot found enforceable rights against individual |
| Majera [2021] UKSC 46 | Confirms Ahmed — void ab initio regardless of label |
| ZH (Tanzania) [2011] UKSC 4 | Individual circumstances must be considered, not category |
| FirstGroup v Paulley [2017] UKSC 4 | Policy compliance insufficient; individual adjustment required |
| Durant v FSA [2003] EWCA Civ 1746 | Personal data scope — decision about individual = their data |
| Guntrip v DWP [2021] EAT | Burden shift in disability discrimination — employer must explain |
| Henderson v Henderson [1843] | Relitigation bar — all grounds must be raised first time |

---

## 9. Versioning

This specification follows the Burgess Principle versioning scheme. Breaking changes to the five-element test or the verdict taxonomy require a major version increment and a new SSRN working paper.

Non-breaking additions (new domains, new metadata fields, new validation rules) are minor version increments.
