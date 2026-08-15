# Portable QR Accountability Receipt

**Status:** Hardened design specification (post-review)  
**UK Certification Mark:** UK00004343685  
**Schema family (target):** `openhear-qr-receipt`  
**Schema version (target):** `openhear-qr-receipt-v1.0.0`  
**Schema owner:** `github.com/ljbudgie/openhear`  
**Date:** 15 August 2026  
**Author:** Lewis James Burgess

---

## What this is

A portable, offline-verifiable accountability receipt for the Burgess Principle binary test.

It is not a marketing QR.  
It is not a URL.  
It is not a probabilistic confidence score.

It is a fact-bound, timestamped, cryptographically bound evidence artefact that answers one question only:

> Was a named human being able to apply their mind to the specific facts of this case before the action was taken?

**SOVEREIGN** — yes.  
**NULL** — no.

There is no third legal state. AMBIGUOUS may exist only as an intermediate process state before human confirmation; it is never a final finding on a confirmed receipt.

---

## Dual-signal architecture (hard boundary)

The receipt is built on two separate signals. They must never be fused into a single pipeline step.

### Signal 1 — Pattern detection (machine)
- Deterministic only.
- Output: structured facts already present in the correspondence / audit trail (who, when, what was requested, what was refused or automated, cycle counts, days consumed).
- Never claims a legal finding.
- No confidence floats. Pattern present or absent. Cycle count is integer. Days consumed is integer.
- No AI-generated summaries, paraphrases, or inferences. Extraction of structured fields only.
- Template dismissal is verified by string identity or Levenshtein ratio ≥ 0.95, not soft similarity.

### Signal 2 — Human confirmation (gated)
- Human-gated binary finding only.
- Requires named confirmation with evidence that the specific facts were reviewed.
- Confirmation gate is a hard boundary, not a “review step” inside one flow.
- AI must never issue the SOVEREIGN / NULL finding.

Treat Signal 1 and Signal 2 as separate microservices in the architecture. The confirmation gate is the legal-technical boundary that protects the certification mark.

---

## The QR is not a URL

### Minimal QR payload (only these fields)
- `receipt_id`
- `bundle_hash`
- `cert_mark` (UK00004343685)
- `timestamp`
- `signature`

No URL.  
No raw content.  
No correspondence bytes.  
No audio.  
No network requirement for verification.

Verification is performed against a local bundle (or offline registry copy) and the relevant public key. Network is optional, never required.

**Anti-pattern (rejected):** QR codes that phone home to a server for verification. That is a marketing QR, not an accountability receipt. If a design proposes `https://…` inside the QR payload, reject it. Any registry URL belongs in schema metadata only, never in the QR payload.

---

## Deterministic, not probabilistic

| Rejected | Required |
|----------|----------|
| Confidence: 0.94 | Pattern present or absent; integers only |
| AI-generated summary of correspondence | Structured field extraction only; no paraphrase |
| Probabilistic template matching | String identity or Levenshtein ≥ 0.95 |
| Soft similarity / NLP sentiment | Forbidden |

---

## Expiry and supersession (event sourcing)

- The **bundle** (underlying facts) is append-only.
- The **receipt** is a point-in-time attestation.

Fields:
- `expires_at`: ISO-8601 or null
- `superseded_by`: receipt_id or null

A receipt expires or is superseded when:
- the classification is challenged and overturned,
- new evidence emerges, or
- a SOVEREIGN exit is achieved (the loop is closed).

Model as event sourcing, not static permanent records.

---

## Boundary: no raw audio, no raw correspondence

At the receipt boundary:

```text
if any fact is raw bytes / audio / correspondence content:
    raise RawAudioRejectedError
```

The receipt contains hashes and references only. Content stays in the sovereign vault / local bundle. This aligns with OpenHear’s existing advocacy layer (`advocacy/gate.py`, `advocacy/bundle.py`): commitments travel; raw facts do not.

---

## Registry is advisory, not authoritative

- Registry function: index, verify, aggregate.
- Registry authority: none — any party can verify offline.
- Registry lock-in: none — bundles are portable; schema is open.

If `register.theburgessprinciple.com` (or any future registry) goes down, every correctly formed receipt must still verify against its local bundle and public key.

---

## Wristband / biometric witness (phased)

- Phase 1–2: human confirmation via app UI + cryptographic signature only.  
  `biometric_witness` field exists and is **null**.
- Phase 3+: optional wristband witness as biometric hardening.
- Phase 5+: wristband witness may become default for high-stakes classifications.

Do not front-load hardware dependencies. Schema remains forward-compatible; the field is present and null, not absent.

---

## Schema versioning (forward-compatible)

```json
{
  "schema": "openhear-qr-receipt-v1.0.0",
  "schema_family": "openhear-qr-receipt",
  "schema_owner": "github.com/ljbudgie/openhear"
}
```

Full semver. The owner field prevents fork/re-version attacks. Validation must enforce these fields.

---

## Alignment with existing OpenHear advocacy layer

This design extends, and does not replace:

- `advocacy/gate.py` — PersonGate, Commitment, Receipt, SOVEREIGN / NULL tags, SHA-256 commitments, facts never leave the device by default.
- `advocacy/bundle.py` — offline export bundle that carries commitment + receipt + tag + hard-coded disclaimers; never raw facts.
- Existing commitment-bundle and verifiable-oversight primitives in the Burgess Principle repo.

The QR receipt is a portable handle onto the same dual-signal, commitment-first model already enforced in OpenHear’s advocacy boundary.

---

## Required test cases (must pass before commit of implementation)

| Test | Expected result |
|------|-----------------|
| Generate receipt → tamper one character in QR → verify | TAMPERED |
| Generate receipt → wait for expiry → verify | EXPIRED |
| Generate receipt with NULL Signal 2 → verify without human confirmation | UNVERIFIED (receipt exists; not confirmed) |
| Generate receipt → challenge with new evidence → superseding receipt | Original SUPERSEDED; new receipt links back |
| Encode minimal QR → decode → verify against full bundle offline | SOVEREIGN or NULL with no network |

---

## Documentation that must ship with implementation code

Not after. With:

- `docs/QR_RECEIPT_SCHEMA.md` — human-readable schema reference
- `docs/QR_RECEIPT_INTEGRATION.md` — generate, verify, challenge
- `examples/qr_receipt_lifecycle.py` — create → confirm → verify → challenge → supersede
- `examples/qr_receipt_offline_verification.py` — no network, no registry, bundle + public key only

---

## What this is not

- Not a substitute for the binary test itself.
- Not a claim that scanning creates human review where none occurred.
- Not an automated decision system.
- Not a marketing or phone-home QR.
- Not a probabilistic or confidence-scored artefact.
- Not a third state between SOVEREIGN and NULL on a confirmed receipt.

---

## Meta rule for implementers

Every time a change would make the receipt more “user-friendly” or “feature-rich,” ask:

1. Does this compromise the binary test?
2. Does this create a third state between SOVEREIGN and NULL?
3. Does this let a machine claim what a human must confirm?

If yes to any → reject. Iterate. That is the point of the certification mark.

---

## Status

Hardened design accepted 15 August 2026 after external architectural review.  
Phase 1 implementation may proceed against OpenHear’s advocacy layer and the existing commitment / verifiable-oversight stack, subject to the constraints above.

UK Certification Mark UK00004343685  
Lewis James Burgess  
lewisjames@theburgessprinciple.com
