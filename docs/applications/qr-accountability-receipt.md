# Portable QR Accountability Receipt

**Status:** Design specification  
**UK Certification Mark:** UK00004343685  
**Date:** 15 August 2026  
**Author:** Lewis James Burgess

---

## What this is

A portable, self-contained accountability receipt for the Burgess Principle binary test.

It is not a marketing QR.  
It is not a generic “verify this certificate” link.

It is a fact-bound, timestamped evidence artefact that answers one question:

> Was a named human being able to apply their mind to the specific facts of this case before the action was taken?

**SOVEREIGN** — yes.  
**NULL** — no.  
**AMBIGUOUS** — unclear on the present record.

The QR resolves to (or embeds a pointer to) a commitment that locks those specific facts at a specific time. The same artefact can be dropped into a court bundle, FOI file, regulatory complaint, or institutional correspondence as a single exhibit.

---

## Why this is different from ordinary certificate QRs

| Ordinary certificate QR | Burgess QR accountability receipt |
|-------------------------|-----------------------------------|
| Answers “is this document authentic?” | Answers “did a named human review these specific facts?” |
| Issuer-specific | Standard-specific (the Principle itself) |
| Static verification page | Fact-bound, timestamped commitment |
| Marketing / convenience | Bundle-ready evidence format |

Most QR-on-certificate systems only prove provenance of a document.  
This one proves (or records the absence of) meaningful human involvement on the facts that matter.

---

## Core design rules

### 1. Fact-bound
The receipt is worthless without the specific facts it commits to.  
Those facts are extracted from the existing email / audit trail (who said what, when, what was requested, what was refused or automated).  
Generic branding (“we care about humans”) is not permitted.

### 2. Timestamped
The moment the facts were locked becomes part of the evidence.  
The commitment carries a clear time anchor.

### 3. AI-assisted, human-accountable
An AI may:
- extract already-existing facts from the correspondence,
- structure them,
- and propose the timestamped commitment.

An AI must never be the decision-maker on the binary finding.  
A human (the subject, or a certified practitioner) confirms SOVEREIGN / NULL / AMBIGUOUS before the receipt is finalised.  
That preserves the SOVEREIGN character of the artefact itself.

### 4. Bundle-ready
A judge, ICO case officer, MP’s office, or institutional decision-maker can open one artefact instead of reconstructing a multi-email thread.  
The receipt is designed to travel with the correspondence and to be exhibited without further reconstruction.

### 5. Compatible with existing repo primitives
This design builds on, and does not replace:
- commitment bundles (`schemas/commitment-bundle.v1.json`)
- verifiable oversight decision records
- sovereign vault / commitment-only workflow
- loop findings and memory receipts

The QR is a portable handle onto those structures, not a parallel system.

---

## Intended workflow (high level)

1. Correspondence / audit trail exists (emails, formal notices, automated replies).
2. Facts are extracted and structured (AI may assist; human confirms).
3. Binary finding is confirmed by a human.
4. Commitment is generated (hash or equivalent) binding facts + finding + timestamp.
5. QR is generated that resolves to (or embeds a pointer to) that commitment.
6. QR / receipt is attached to further correspondence or filed as an exhibit.

---

## Use cases

- Attach to letters and emails sent to councils, credit reference agencies, utilities, courts, and regulators.
- Include in court bundles and FOI / DSAR packs as a single, self-contained exhibit.
- Hand or display as a physical card when process fails in the moment.
- Generate from Iris / sovereign vault once the commitment layer is live for a given case.

---

## What this is not

- Not a substitute for the binary test itself.
- Not a claim that scanning the QR creates human review where none occurred.
- Not an automated decision system.
- Not a closed or proprietary format — the underlying commitment and finding remain human-legible and challengeable.

---

## Next implementation steps (non-blocking)

1. Define a minimal receipt schema that references or embeds an existing commitment-bundle / decision-record.
2. Specify the QR payload (URL to a receipt page, or offline-capable deep link / short payload).
3. Wire fact extraction helpers to the existing email / loop / verifiable-oversight tooling.
4. Ensure the human confirmation gate remains mandatory before any QR is finalised.
5. Document how a receipt is exhibited in a court or regulatory bundle.

---

## Status

Design accepted 15 August 2026.  
Implementation may proceed incrementally against the existing commitment and verifiable-oversight stack.

UK Certification Mark UK00004343685  
Lewis James Burgess  
lewisjames@theburgessprinciple.com
