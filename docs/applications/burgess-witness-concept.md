# Burgess Witness — Concept & Design Note (Sovereign Attestor)

> **STATUS: CONCEPT / DRAFT — not built, not certified, not yet a product.**
> Working design note dated 3 June 2026. Nothing here should be read as a claim
> that a device exists or has been verified. It is a specification of intent and
> an honest analysis of what such a device can and cannot prove.

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685

---

## 1. What it is

**Burgess Witness** (working name; "Sovereign Attestor") is a proposed small,
open-source personal hardware device — a key-fob, wristband module, or USB-C
token — that lets a **named human reviewer cryptographically sign an
attestation** at the moment they take responsibility for a decision about an
identified person.

It is the proposed third pillar of the stack:

- **The Burgess Principle** — the testable standard, certification mark, templates, public ledger.
- **Iris** — the local, governed AI that surfaces the question, the facts summary, and the classification.
- **OpenHear** — sovereign sensory hardware (haptic, DIY, audiogram-driven).
- **Burgess Witness** — the physical + cryptographic act of a named human putting their name to a decision, in real time.

## 2. What it proves — and what it does NOT prove (read this first)

This is the single most important section. Getting it wrong would hand a critic
the whole argument in one sentence.

A signature proves: **a specific key was used, at a specific time, over a
specific facts-hash.** That is all cryptography can establish.

**It therefore does NOT prove that a human read, understood, or genuinely
considered the facts.** A person can press the button without reading a word.
Any claim that the device proves "meaningful review took place" is false and
should never be made.

**What it actually delivers is stronger and defensible: non-repudiable named
accountability.** Once a named, registered keyholder signs, they can no longer
say "the system did it" or "it was handled in line with policy." A specific
human is now personally and verifiably attached to the decision and can be held
to it. The *value is liability attachment, not proof of cognition.*

Correspondingly, the **absence** of a signature where one was requested is the
evidence of NULL — not proof that thinking failed to happen, but proof that no
named human was willing to attach their name to the decision.

This mirrors the discipline applied to [email triage](./email-triage-adm.md):
the framework is a precision instrument. Claimed precisely, it holds. Claimed as
"proof a human truly reviewed," it breaks.

## 3. The attestation record

A compact, signed object — anchored optionally via the existing
[Burgess Claims Protocol](../../onchain-protocol/spec.md):

```json
{
  "reviewer_key_id": "registered key identifier (not raw identity)",
  "reviewer_role": "e.g. Clinician / Caseworker / AI Governance Lead",
  "timestamp": "RFC3339 UTC",
  "facts_hash": "sha256 of the agreed facts summary (content kept private)",
  "decision_id": "opaque reference to the decision/interaction",
  "classification": "SOVEREIGN | NULL | AMBIGUOUS",
  "signature": "Ed25519 over the canonical payload"
}
```

Only hashes and identifiers are published; the underlying facts stay in the
individual's encrypted vault and are revealed by selective disclosure on demand.

## 4. The hard problem that is also the moat: identity & trust root

A raw signature is just "some key signed this" — anyone can mint a key and claim
to be Dr Jones. The device is worthless without a **trust root** that binds a key
to a real, accountable person and can **revoke** it.

That requirement is not a burden; it is the strategic asset. **The Burgess
Principle (via the certification mark and The Burgess Principle Ltd) is the
natural registry / certification authority for attestor keys.** The same body
that makes attestations trustworthy is the one that already owns the standard —
which means the trust layer is *also* an enforcement and revenue layer.

Open design questions (honest, unsolved):
- Key issuance and identity verification process for reviewers.
- Revocation and key-rotation handling.
- Whether the registry is centralised (simpler, a single trust point) or
  federated (more robust, more complex).

## 5. Two assurance tiers (do not conflate them)

| | DIY / Personal | Certified |
|---|---|---|
| **Build** | 3D-printed enclosure + microcontroller (+ optional ATECC608-class secure-element chip) | Audited hardware with a real secure element and attested provenance |
| **Assurance** | Low — an *accountability token*; the printed enclosure is not meaningfully tamper-proof | High — tamper-evident, key sealed in secure element |
| **For** | Individuals, sole practitioners, immediate use | Institutions, regulated reviewers |
| **Honesty** | Must be described as low-assurance; never marketed as tamper-proof | Where the "tamper-evident" language legitimately applies |

You cannot 3D-print a secure element. The DIY version's value is accountability
and convenience, not hardware security.

## 6. Haptic layer — the genuinely novel piece (OpenHear synergy)

The most original element, and the one only the Burgess × [OpenHear](https://github.com/ljbudgie/openhear)
intersection can produce: distinct vibration patterns signal whether an incoming
communication or interaction is trending **NULL / AMBIGUOUS / SOVEREIGN** *before
the user reads the words*. The accountability gap becomes a bodily sensation —
especially powerful for a profoundly deaf user, and a direct tie to the
neuroplasticity / frequency work. Lead with this emotionally; it is the hardest
thing to replicate.

## 7. Realistic use contexts (and one to avoid first)

Best fit — slower, repeated, document-based interactions where attaching a name
is plausible:
- medical appointments and device-fitting decisions;
- benefits / capability assessments;
- AI-governance sign-offs inside an institution (a reviewer attests before an
  automated action proceeds — the gate is then non-bypassable in hardware as
  well as software).

Avoid as the *first* scenario: **police stops.** Asking an officer mid-stop to
sign a fob is unrealistic and risks escalation. The device's encounter-recording
value for the individual still applies, but reviewer-attestation is not the right
first demand there.

## 8. Adoption — be honest about the cold start

"Institutions can't avoid demonstrating it" is only true *after* adoption. On day
one an institution simply says "we don't use your device," and non-adoption is
not yet evidence of NULL. Therefore:

- **First user is the individual.** Your own attestations and tamper-evident
  encounter records work today, with no third-party adoption required.
- Institutional leverage builds over time, anchored by the certification tiers
  and (eventually) regulatory pressure (EU AI Act / DUAA enforcement windows).

## 9. How it slots into certification

Per [CERTIFICATION_TIERS.md](../../CERTIFICATION_TIERS.md):
- **Tier 01 (Institutional)** — certified attestor devices / protocol integration
  for an institution's reviewers; ledger-anchoring services.
- **Tier 02 (Technology & Advocacy)** — platforms and claims groups integrate the
  attestation protocol; practitioner device kits.
- **Tier 03 (Practitioner)** — individual advisers issue/carry attestor tokens.

The certifiable asset is the **hardware + protocol specification itself**, governed
under the existing mark — a new enforcement and revenue layer that does not
compromise the evidence-based core.

## 10. Sequence: ship the software first

A software-only **"NULL Hunter"** classifier — running locally inside/alongside
Iris — that scans incoming institutional communications and flags
SOVEREIGN / NULL / AMBIGUOUS language, then suggests the next Burgess question,
is the pragmatic first build (**now implemented** — see
[`null-hunter.md`](./null-hunter.md) and `iris/null_hunter.py`):

- no identity or adoption problem;
- runs on-device today;
- starts generating the records the Witness device will later sign.

Then build **Burgess Witness** as the flagship, with the identity/CA layer
designed in from the start.

## 11. Open problems / risks (kept explicit, on purpose)

- **Cognition gap** — signature ≠ review (see §2).
- **Identity binding** — the unsolved 90%; needs a CA (see §4).
- **DIY security limits** — printed enclosures are not tamper-proof (see §5).
- **Coercion contexts** — see §7.
- **Privacy / data-controller status** — publishing attestations about named
  third parties engages GDPR; hash + selective disclosure, reveal on demand.
- **Legal weight** — a self-hosted record is not automatically authoritative;
  public timestamp anchoring (Burgess Claims Protocol) proves existence-at-time,
  not truth-of-content.

## 12. Out of scope / non-claims

This note does **not** claim: that a device exists; that any device is
tamper-proof; that a signature proves genuine human consideration; or that
institutions are obliged to adopt it. It documents intent and an honest design
path.

---

## Next steps (pick up from here)

1. Names / branding aligned to the restoration narrative.
2. A full technical spec (components, crypto, secure element, Iris/OpenHear integration points, 3D design).
3. Detailed commercial / tier mapping and the certified-device spec governance.
4. The identity/CA design (issuance, revocation, centralised vs federated).
5. The "NULL Hunter" software classifier as the first shippable increment.

*The Burgess Principle — UK Certification Mark UK00004343685 — lewisjames@theburgessprinciple.com*
