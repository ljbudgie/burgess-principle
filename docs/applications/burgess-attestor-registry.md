# Burgess Attestor Registry — Identity & Trust-Root Design

> **STATUS: CONCEPT / DRAFT — design note, not a deployed service.**
> Dated 3 June 2026. Expands §4 of the
> [Burgess Witness concept](./burgess-witness-concept.md). Nothing here is built
> or operating; it is a rigorous, honest design for the hard part.

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685

---

## 1. The problem this solves

A [Burgess Witness](./burgess-witness-concept.md) attestation is an Ed25519
signature over a facts-hash. On its own, a signature proves only that *some key*
signed — anyone can mint a key and claim to be Dr Jones. For an attestation to
mean "**a named, accountable human stands behind this decision**," three things
must exist that a raw keypair does not provide:

1. a **binding** of the key to a real, identified holder;
2. a way to **revoke** that binding (compromise, misuse, departure);
3. a **trust root** that does both — verifiably, and without becoming the very
   kind of unaccountable power the framework exists to challenge.

That trust root is the **Burgess Attestor Registry**.

## 2. What a registered key asserts — and what it does NOT

Carried forward from the Witness concept, because it is the load-bearing honesty:

A registered key asserts: *"this key belongs to a real, identified holder (or a
named role under an accountable institution) who has accepted the attestation
terms, and whose binding the registry can revoke."*

It does **not** assert:
- that the holder is competent;
- that any given attestation reflects genuine review (the cognition gap from
  §2 of the Witness concept persists at every layer);
- that the signature is a *qualified* electronic signature in law (see §11).

The registry delivers **accountability and revocability** — liability attaches to
a named, reachable person — not proof of thought. Claimed precisely, it holds.

## 3. The registry must pass its own Burgess test

This is the spine of the design. A trust root that can **secretly** issue or
revoke keys, or backdate records, is itself exercising power over people without
individual accountability — a **NULL** by the framework's own definition. The
registry cannot be exempt from the standard it serves.

Therefore the registry is built to be **transparent and externally verifiable by
construction**:

- every issuance and revocation is written to an **append-only, signed public
  log** (a transparency log, in the spirit of Certificate Transparency);
- the log's head is periodically **anchored** via the existing
  [Burgess Claims Protocol](../../onchain-protocol/spec.md), so no entry can be
  secretly inserted, removed, or backdated;
- anyone can audit that a key was issued/active/revoked at a given time.

If the registry cannot prove its own honesty, it has no business certifying
anyone else's.

## 4. Assurance levels (mapped to the existing certification tiers)

Not every key is equal, and the registry says so plainly. Assurance maps onto
[CERTIFICATION_TIERS.md](../../CERTIFICATION_TIERS.md):

| Level | Who | Identity verification | Honest label |
|---|---|---|---|
| **L0 — Self-asserted** | Individuals, DIY/Tier 03 self-issue | None — the holder simply claims the key | "unverified / self-sovereign"; useful for personal records, not for vouching to third parties |
| **L1 — Vetted practitioner** | Tier 03 practitioners | Identity checked once; bound to a named individual | "named, identity-verified holder" |
| **L2 — Institutional** | Tier 01/02 reviewers | Issued under an institutional account; the institution vouches for and is accountable for its reviewers | "named role under an accountable institution" |

The level is part of the public record, so a verifier never mistakes a
self-asserted key for a vetted one.

## 5. The registry record (and privacy)

Per key, the **public** entry exposes only what verification needs:

```
key_id, public_key, assurance_level, role, status (active|revoked|expired),
issued_at, institution_ref (if L2), transparency_log_index
```

The binding to a real-world **name** is held by the registry as restricted
personal data and revealed only under defined process (selective disclosure,
using the same hash-then-reveal pattern as the
[on-chain protocol §5.2](../../onchain-protocol/spec.md)). This keeps reviewers'
identities out of a fully public dump while preserving accountability: the named
human can be reached through due process, not doxxed by default.

The registry is a **data controller** for that identity data and must be run on
that basis (lawful basis, retention, subject rights) — see §10.

## 6. Issuance

1. Applicant requests a key at a chosen assurance level.
2. For L1/L2, identity is verified (practitioner credentials / institutional
   account ownership). For L0, no check — the key is marked self-asserted.
3. The registry records the binding, writes an **issuance entry** to the
   transparency log, and the holder generates/stores the private key (in a
   secure element for the certified hardware tier; locally for DIY).
4. Private keys are never held by the registry. It binds and publishes; it does
   not escrow.

## 7. Revocation, rotation, and time-bound validity

- Keys can be **revoked** (compromise, misuse, a reviewer leaving a role); a
  revocation entry goes to the transparency log and a published status endpoint.
- Keys should be **short-lived and rotated** to limit blast radius.
- Crucially, an attestation is valid only if the signing key was **active at the
  attestation's anchored timestamp**. This is why anchoring matters: it proves an
  attestation predates a later revocation, so revoking a key does not retroactively
  void honestly-made attestations — nor can a revoked key be used to mint new ones.

## 8. Centralised vs federated — the honest trade-off

| | Transparent-centralised (recommended first) | Federated / web-of-trust |
|---|---|---|
| Trust model | The Burgess Principle Ltd operates one registry | Multiple issuers vouch; no single root |
| Pros | Simpler, clear accountability, clean UX, fast to ship | No single point of capture |
| Cons | Single point of failure **and** of capture | Complex, weaker UX, harder revocation |

The tension is real and worth naming: a *centralised* trust root sits uneasily
with a framework about resisting unaccountable centralised power. The resolution
is §3 — the centralised registry is acceptable **only because it is transparent,
append-only, anchored, and externally auditable**. A federation path is kept open
for later, but transparency (not decentralisation) is what does the actual work
of keeping the root honest on day one.

## 9. Neutrality & governance

The registry inherits the impartiality rules already in
[CERTIFICATION_TIERS.md](../../CERTIFICATION_TIERS.md) ("Neutral Oversight and
Impartiality"): decisions made against the published standard, conflicts of
interest recorded, external verification for the institutional tier. There is a
genuine conflict to manage — The Burgess Principle Ltd both *certifies*
organisations and would *operate the registry that vouches for their reviewers* —
and it must be declared and mitigated (external verifier / advisory reviewer), or
the registry's neutrality is compromised.

## 10. Honest limits & risks

- **Cognition gap persists.** A valid, registered signature still does not prove
  the human thought about the facts. Verification UX must never imply otherwise.
- **Registry capture / compromise.** Mitigated, not eliminated, by the
  transparency log + anchoring + external governance.
- **Coerced attestations.** A signature under duress is still a signature; out of
  scope for crypto to solve.
- **A key is not a person.** Key-sharing undermines the binding; mitigated by
  per-reviewer keys, secure elements (certified tier), and institutional
  accountability — not perfectly.
- **GDPR.** The registry processes reviewers' identity data; it is a controller
  and must operate lawfully (basis, retention, access, erasure-vs-record tension).
- **Not a qualified trust service.** This is a private accountability scheme, not
  an eIDAS qualified trust service; do not market self-issued keys as
  legally-qualified electronic signatures (see §11).

## 11. Relationship to eIDAS / qualified signatures

For legal-grade non-repudiation, the **certified institutional tier** could, in
future, build on **qualified electronic signatures / eIDAS (and UK) trust
services** rather than a bespoke scheme — inheriting established legal standing.
The DIY and L0/L1 tiers remain a private accountability layer. Being explicit
about this boundary is itself part of not overclaiming.

---

## Open questions / next steps

1. Choose the transparency-log format and anchoring cadence (ties to the Burgess Claims Protocol).
2. Define the L1 identity-verification process (what evidence, who checks).
3. Draft the registry's data-protection basis and privacy notice (controller obligations).
4. Decide the governance/neutrality split for the inherent certify-and-vouch conflict.
5. Specify key lifetimes, rotation, and the status/revocation endpoint.

*The Burgess Principle — UK Certification Mark UK00004343685 — lewisjames@theburgessprinciple.com*
