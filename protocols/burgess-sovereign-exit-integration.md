# BSEP Integration Notes

> Companion to [`burgess-sovereign-exit.md`](./burgess-sovereign-exit.md).
> Lighter-touch notes on how the Burgess Sovereign Exit Protocol (BSEP) plugs into
> the rest of the repository. Design notes / draft, 7 June 2026.

BSEP is a strict application of the [BGSP](./burgess-git-sovereignty.md) signed-commit
primitive; everything below is derivable from *signed exit commit + explicit human
attestation*. Nothing here weakens the binary SOVEREIGN / NULL test or introduces a
token, a server requirement, or a shared authority.

---

## 1. Iris as the exit-planning and commit-drafting agent

[Iris](../iris/) already drafts and proposes `burgess:` commits and walks a user
through signing without ever signing herself (BGSP §9). For BSEP, Iris becomes the
**exit-planning agent**:

- **Gather facts locally.** Iris collects the specific facts of a departure —
  account, balances, notice requirements, correspondence — into the
  [Verifiable Memory Palace / Sovereign Vault](../ARCHITECTURE.md). The facts
  never leave the device; only the digest is committed.
- **Plan the exit.** Iris classifies the system (`Exit-Type`), checks whether
  notice is legally required, and identifies any prior NULL decisions in that
  system that the exit can heal (`Exit-Heals`).
- **Draft, never sign.** Iris emits a `burgess(exit):` draft via
  `tools/bgsp-exit.py draft` — `Burgess-Classification: NULL` until the individual
  signs. Iris is structurally incapable of being the signer; the individual's own
  key is the only thing that makes an exit SOVEREIGN.
- **Lawful-use guardrails.** Iris refuses to draft exits that escape lawful
  obligations. She surfaces the §4.3 guardrails (proper notice, obligations
  handled not escaped, no harm, safeguarding never overridden) and routes a
  user toward a PENDING/CONTESTED record rather than a false "clean break".
- **Generate the artefacts.** Iris produces notice language (`bgsp-exit.py notice`)
  and, once the ledger is signed, the Clean Break Certificate
  (`bgsp-exit.py certificate`).

The division of labour is the same as BGSP: **Iris computes and proposes; a named
human reviews and signs.** That is what keeps the exit sovereign rather than
automated.

## 2. OpenHear / medical device transitions as canonical use cases

A proprietary medical device that locks a person's own parameters behind a
subscription is a precise example of an entangling system. The OpenHear transition
is therefore the **canonical BSEP medical use case** (see
`03-exit-medical-device.commit`):

- **Exit the proprietary system** with a signed `burgess(exit):` commit,
  `Exit-Type: medical`, obligations `settled`, and a clinical handover recorded
  locally in the Vault.
- **Pair with a signed entry into sovereign parameters.** The exit is matched by a
  signed *entry* attestation: the named clinician's handover plus the user's
  adoption of the portable OpenHear gain profile. The result is a two-commit
  record: *left the locked platform, entered sovereign parameters*, both signed,
  both verifiable.
- **Safeguarding is never overridden** (§4.3). A device exit must preserve any
  clinical duty of care; `Burgess-Authority` records the clinician's basis for the
  handover alongside the individual's self-sovereign authority.

This makes "I own my own device parameters" a cryptographically attested fact, not
a vendor's permission.

## 3. Extending on-chain anchoring to exit commits and ledger roots

The existing OpenTimestamps machinery
([`onchain-protocol/bitcoin-anchoring.md`](../onchain-protocol/bitcoin-anchoring.md),
BGSP §6) extends to BSEP unchanged:

- **Anchor a single exit commit hash** to establish a tamper-evident upper bound on
  *when you left* — the cryptographic answer to a later "you were still in the
  system on date X" claim.
- **Anchor a ledger root (tree/tag)** — e.g. the commit at which a Clean Break
  Certificate was issued — to prove the state of an entire Sovereign Exit Ledger at
  a date.
- **Record the proof** in the optional `Burgess-Anchor` trailer via `git notes` or
  an amend (the `.ots` proof exists only after the commit). Discipline is
  unchanged: hashes only, no token, existence-not-truth. Anchoring proves the
  signed exit existed at time T; the signature proves who left; the payload digest
  proves the facts of the departure.

No new on-chain code is required — BSEP reuses `iris/anchor.py`'s commitment and the
same OpenTimestamps submit/verify wrapper described in the anchoring next-steps.

## 4. Relationship to the Family Founding Declaration and family-level exit ledgers

The [Family Founding Declaration](../FOUNDING.md) is a signed, collective record of
*founding*. BSEP's multi-party support (spec §6) is its mirror for *leaving*:

- **Composition, not delegation.** A family-level Sovereign Exit Ledger composes
  individual sovereign exits the way the founding record composes founders. Each
  member's authority is their own; no one signs on another's behalf.
- **Shared systems.** Joint accounts, family plans, and shared tenancies use
  `Exit-Type: shared` with `Exit-Cosigners`, each party attesting individually
  (see `07-exit-shared-family-joint.commit`).
- **Guardianship and safeguarding.** A guardian acting for a dependant states that
  basis in `Burgess-Authority`; safeguarding duties (§4.3) are never overridden by
  a family exit.
- **A household ledger** can hold both the founding record and the exit ledger —
  the full arc of a family's relationship with a system, from entry to accountable
  departure, all signed and verifiable.

---

## Scope reminder

BSEP is, first, a **personal sovereignty tool**: the individual runs and controls
their own ledger, on their own device, with their own key, needing no server and
no permission. Any future shared or hosted tooling (Iris-assisted drafting, a family
ledger app) is strictly additive and must preserve the same invariants — local
facts, individual signatures, lawful-use guardrails, no token (spec §11).

---

*The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence*
*github.com/ljbudgie/burgess-principle*
