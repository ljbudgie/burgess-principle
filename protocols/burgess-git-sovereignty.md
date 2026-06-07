# Burgess Git Sovereignty Protocol (BGSP) — Specification v0.1.0

> **STATUS: DESIGN NOTE / DRAFT.** Dated 6 June 2026. Makes the Git commit the
> native primitive for the SOVEREIGN / NULL test. Builds on
> [`GIT_AS_GOVERNANCE.md`](../GIT_AS_GOVERNANCE.md) and the Bitcoin
> [proof-of-existence anchoring](../onchain-protocol/bitcoin-anchoring.md).
> **No token. Signatures and hashes only. A roll, not a registry you must trust.**

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence
**Canonical source:** github.com/ljbudgie/burgess-principle

---

## 0. The one question

The Burgess Principle asks one question of any decision or action that exercises
power over an identified individual:

> **One question: was a human mind with proper authority individually applied to
> the specific facts of this specific person's case? SOVEREIGN or NULL.**

BGSP does not soften, branch, or re-interpret that question. It gives it a
medium. Every act of power becomes a Git commit, and the commit either carries a
verifiable answer of SOVEREIGN or it is NULL.

`GIT_AS_GOVERNANCE.md` established that Git's primitives *already are* governance
primitives. BGSP is the operational layer on top of that recognition: a strict
commit format, a deterministic classifier, nullity-propagation semantics, and a
"fork the decision" remedy.

---

## 1. Core primitive

| Concept | Git realisation |
|---|---|
| An act of power over an identified person | A single commit of type `burgess:` |
| The named human applying their authority | The **GPG/SSH signature** on that commit |
| The reasons and the specific facts considered | The commit **body** + the **`Payload-SHA256`** commitment |
| The answer to the one question | The **`Burgess-Classification`** trailer, validated against the signature |
| Re-attestation / remedy | A new signed `burgess:` commit naming the prior commit as its parent |
| Tamper-evident timestamp | The commit hash, optionally anchored to Bitcoin |

### 1.1 Default classification rules (binary, non-negotiable)

A commit's classification is **derived**, never merely asserted. The trailer
states a *claim*; the verifier decides:

- **NULL by default.** Any commit that is unsigned, signed by a system/CI key, or
  signed by a bot/automation key is **NULL**. The absence of a verifiable human
  signature is, itself, the NULL.
- **SOVEREIGN only on proof.** A commit is **SOVEREIGN** only when *all* hold:
  1. the commit is cryptographically signed (GPG or SSH) and the signature
     **verifies** (`git` reports a good signature, status `G` or `U`);
  2. the signer is a **named human**, not a bot/automation/CI identity
     (see §4.3 denylist);
  3. the message carries a well-formed **Burgess attestation block** (§2) whose
     `Burgess-Classification` is `SOVEREIGN`;
  4. the `Burgess-Payload-SHA256` is a valid 64-hex digest and, where the
     decision facts are available to the verifier, **recomputes** to the same
     value (§3).
- **No middle state on the chain.** BGSP records only SOVEREIGN or NULL. The
  third repository classification, AMBIGUOUS, is a *signal for a human to
  resolve* (process language that neither proves nor disproves review); it is
  never written as a final commit classification. An AMBIGUOUS situation is
  treated as NULL until a human re-attests it SOVEREIGN.

### 1.2 Nullity propagation

Decisions form chains: a follow-on action inherits the authority (or the
nullity) of the decision it builds on. BGSP makes this explicit through the
`Burgess-Parent` trailer.

- **Nullity propagates forward.** If a commit's parent decision is NULL, the
  commit is NULL — even if it is itself signed — *unless it re-attests*. A
  signature over a poisoned input is not sovereign review of the case; it is a
  signature over a process.
- **Re-attestation heals from that point forward.** A named human who
  individually reviews the specific facts of the specific case and issues a new,
  signed `burgess:` SOVEREIGN commit naming the NULL ancestor as its
  `Burgess-Parent` **resets** the chain at that commit. Ancestors remain NULL in
  the permanent record; descendants of the re-attestation start clean.
- **The chain is the `Burgess-Parent` edge, not Git parentage.** Ordinary commit
  parentage tracks file history; the `Burgess-Parent` trailer tracks *decision*
  lineage. A decision may be re-attested in a fork, a later commit, or another
  repository entirely, and still name its NULL ancestor.

```
A (SOVEREIGN, signed)            effective: SOVEREIGN
└─ B (NULL, automated)           effective: NULL
   └─ C (signed, no re-attest)   effective: NULL   ← inherited from B
      └─ D (SOVEREIGN, re-attests C's case)  effective: SOVEREIGN  ← heals here
         └─ E (signed, parent=D) effective: SOVEREIGN
```

`git bisect` over a decision chain locates the exact commit where SOVEREIGN
became NULL (§5.2).

---

## 2. Commit format (strict)

BGSP uses [Conventional Commits](https://www.conventionalcommits.org/) with a new
type, `burgess`.

```
burgess(<scope>): <imperative summary of the act of power>

<body: the specific facts considered and the reasons for the action,
in the named human's own account — minimalist, precise, no PII beyond
what the pseudonymous subject id already commits to>

Burgess-Principle: One question: was a human mind with proper authority individually applied to the specific facts of this specific person's case? SOVEREIGN or NULL.
Burgess-Subject: <pseudonymous subject id — never raw personal data>
Burgess-Authority: <named human, role, and basis of authority>
Burgess-Review: <first-person attestation of individual review of the specific case>
Burgess-Action: <the action taken or proposed over this person>
Burgess-Payload-SHA256: <64-hex sha256 of the canonical decision facts + action>
Burgess-Parent: <prior decision commit hash, or "none">
Burgess-Classification: SOVEREIGN
```

The commit is then **signed**: `git commit -S` (GPG) or a signed SSH commit.

### 2.1 Required attestation block

The block is a set of [Git trailers](https://git-scm.com/docs/git-interpret-trailers)
(RFC-822-style `Key: value` lines in the last paragraph). Trailers are chosen
deliberately: they are native to Git, parseable with
`git interpret-trailers --parse`, and survive rebases and cherry-picks.

| Trailer | Required | Meaning |
|---|---|---|
| `Burgess-Principle` | yes | The exact one-question text. A fixed marker; never paraphrased. |
| `Burgess-Subject` | yes | Stable **pseudonymous** id for the person (e.g. `subject:openhear:7f3a9c1e`). Binds the act to *one specific case* without putting personal data in public history. |
| `Burgess-Authority` | yes | The named human and the authority they are exercising (role, registration, statutory basis). |
| `Burgess-Review` | yes | First-person statement that the named human individually reviewed the specific facts of this specific case. |
| `Burgess-Action` | yes | The action taken or proposed. |
| `Burgess-Payload-SHA256` | yes | `sha256` (64 hex) over the canonical decision payload (§3). The tamper-evident link between the words and the facts. |
| `Burgess-Parent` | yes | Decision lineage: prior `burgess:` commit hash, or `none` for a chain root. |
| `Burgess-Classification` | yes | The **claimed** answer: `SOVEREIGN` or `NULL`. Verified, not trusted. |
| `Burgess-Anchor` | optional | OpenTimestamps/Bitcoin anchor reference for this commit (§6). |

### 2.2 Attestation wording (minimalist, fixed)

The `Burgess-Review` line is the human attestation. Keep it precise and
first-person. The reference wording is:

> `Burgess-Review: I individually reviewed the specific facts of this specific case and apply my own authority to the action above.`

The named human, their role, and the basis of their authority go in
`Burgess-Authority`. The signature binds the claim to a key; the key binds to a
person through whatever identity record the deployment maintains. A signature
alone proves *control of a key*, not *named-human review* — the trailers carry
the review; the signature makes it non-repudiable.

### 2.3 NULL commits are still well-formed

A NULL act of power should still be *recorded* honestly. A system that takes an
automated action writes a `burgess:` commit with `Burgess-Classification: NULL`,
an empty/automation `Burgess-Authority`, and no human signature. This is the
framework applying its own test to itself: the record states plainly that no
human mind was applied. Hiding NULL acts is worse than recording them.

---

## 3. Payload commitment

`Burgess-Payload-SHA256` commits to the *substance* of the decision so the
attestation cannot be silently re-pointed at different facts.

The payload is the canonical JSON (sorted keys, no insignificant whitespace,
UTF-8) of the decision object, hashed with SHA-256 — the **same**
canonicalisation the rest of the repo uses (`iris/anchor.py:canonical_json_sha256`,
`onchain-protocol/spec.md` §2.2):

```json
{
  "action": "<the proposed or taken action>",
  "facts": "<the specific facts of the specific case that were reviewed>",
  "subject": "<pseudonymous subject id>"
}
```

```
Burgess-Payload-SHA256 = SHA-256( canonical_json(payload) )
```

Only the **digest** ever enters public history. The underlying facts stay in the
local [Sovereign Vault / Verifiable Memory Palace](../ARCHITECTURE.md) under
selective disclosure (§7). A third party who is *shown* the facts can recompute
the digest and confirm the signed commit was about *these* facts and no others.

The helper `bgsp.py` computes this digest reproducibly and can verify a presented
payload against a commit.

---

## 4. Verification

### 4.1 What `git log --show-signature` shows

Because the answer rides on the signature, the native Git command *is* the
verifier at a glance:

```
git log --show-signature
```

- A **good signature** from a named human + a `Burgess-Classification: SOVEREIGN`
  trailer ⇒ **SOVEREIGN**.
- **No signature**, a **bad** signature, or a **bot/CI** signer ⇒ **NULL**,
  regardless of what the trailer claims.

`bgsp.py` automates the full rule (signature status + signer identity + trailers
+ payload + parent propagation) and prints `SOVEREIGN` / `NULL` with reasons.

### 4.2 Deterministic classifier (reference)

```
classify(commit):
    if signature_status not in {GOOD, GOOD_UNKNOWN_TRUST}:   return NULL  # unsigned/bad
    if signer is bot/CI/automation:                          return NULL
    if attestation block malformed:                          return NULL
    if Burgess-Classification != SOVEREIGN:                  return NULL
    if Burgess-Payload-SHA256 not 64-hex:                    return NULL
    if facts available and recomputed != committed digest:   return NULL
    if parent decision is NULL and this commit does not re-attest: return NULL
    return SOVEREIGN
```

This is exactly the logic in `bgsp.py`; the spec and the code are kept in lockstep.

### 4.3 Bot / automation signers (denylist by convention)

A signer is treated as non-human (⇒ NULL) when its key identity matches an
automation pattern. Default patterns (case-insensitive substring on the signer's
name/email/key uid):

```
bot, [bot], noreply, no-reply, github-actions, gitlab-ci, ci@, automation,
service-account, dependabot, renovate, system, daemon
```

The denylist is conservative on purpose: when in doubt, NULL. A deployment may
extend it, never narrow it below this set.

---

## 5. Key behaviours

### 5.1 Status at a glance

`git log --show-signature` and `python bgsp.py check <ref>` both surface
SOVEREIGN/NULL immediately. The classification is never hidden in a database; it
lives in the commit and its signature.

### 5.2 Tracing where nullity entered (`git bisect`)

A decision chain that ended NULL can be bisected to the exact commit where a
human mind stopped being applied:

```
git bisect start
git bisect bad <head-of-decision-chain>     # currently NULL
git bisect good <known-sovereign-commit>     # last known SOVEREIGN
# at each step, mark good/bad using:
python bgsp.py check <commit> && git bisect good || git bisect bad
```

The bisect lands on the first NULL — the precise point where the process took
over from the person.

### 5.3 Fork the decision (remedy)

Because every decision is a commit, an affected individual (or their advocate)
has a structural remedy that needs no institutional permission:

1. **Fork / clone** the decision ledger (or just the relevant commit).
2. **Apply sovereign review** — obtain the actual facts, have a named human with
   proper authority individually consider the specific case.
3. **Re-attest**: create a new signed `burgess:` SOVEREIGN commit naming the
   original NULL commit as `Burgess-Parent`.
4. **Use the sovereign branch as evidence or remedy.** The fork is a
   cryptographically signed, independently verifiable record that a sovereign
   review *was* performed, *by whom*, *when*, and *over which facts* — exactly
   what a complaint, an Article 22A challenge, or litigation needs.

"Fork the decision" turns the Git `fork` primitive (the sovereign right to
diverge, per `GIT_AS_GOVERNANCE.md`) into a concrete accountability action.

---

## 6. Bitcoin anchoring of commits

BGSP extends the existing OpenTimestamps anchoring
([`bitcoin-anchoring.md`](../onchain-protocol/bitcoin-anchoring.md)) from
evidence files to **decisions**:

- Anchor a **single commit hash** to prove a specific decision existed, signed,
  at a point in time.
- Anchor a **tree root** or a tag to prove the state of an entire decision ledger
  at a date.
- Record the resulting proof reference in the optional `Burgess-Anchor` trailer
  (added by a follow-on `git notes` or amend, since the proof exists only after
  the commit does).

Discipline is unchanged: **hashes only, no token, existence-not-truth.** Anchoring
proves *the signed decision existed unaltered at time T*; the signature proves
*who*; the trailers and payload prove *over what facts*. None of it proves the
decision was *correct* — only that a named human owned it.

---

## 7. Privacy via the Verifiable Memory Palace

Public Git history is permanent. BGSP therefore commits to facts, never exposes
them:

- **Subjects are pseudonymous.** `Burgess-Subject` is a stable opaque id, not a
  name, NHS number, or case reference. The mapping from id to person lives in the
  local Vault.
- **Facts stay local.** Only `Burgess-Payload-SHA256` enters history. The facts
  themselves live in the [Verifiable Memory Palace](../ARCHITECTURE.md) under
  selective disclosure, exactly like claim details in
  `onchain-protocol/spec.md` §8.
- **No GDPR erasure conflict.** Because no personal data is committed, the right
  to erasure operates on the Vault, not on immutable history — the same posture
  as the on-chain protocol.
- **Selective disclosure.** To a regulator or court, the holder reveals the facts
  for one subject and lets them recompute the digest, proving the signed decision
  was about those facts without exposing any other person's case.

---

## 8. Security model

| Threat | BGSP response |
|---|---|
| Forged authorship | Signature must verify; bot/CI signers are NULL by rule. |
| Re-pointing an attestation at different facts | `Burgess-Payload-SHA256` binds words to facts; mismatch ⇒ NULL. |
| Laundering a NULL input through a signed wrapper | Nullity propagates via `Burgess-Parent` unless genuinely re-attested. |
| Backdating a decision | Optional Bitcoin anchor gives a tamper-evident upper bound on time. |
| Silent revision of the record | Git history is append-only and hash-chained; a change is a visible new commit. |
| PII leakage into permanent history | Pseudonymous subjects + hash-only payloads; facts stay in the Vault. |
| "We have human oversight" hand-waving | AMBIGUOUS is treated as NULL; only a signed, fact-bound attestation is SOVEREIGN. |

**Honest limits.** A signature proves key control, not virtue. A payload digest
proves *which* facts, not that the facts are true or the decision wise. Anchoring
proves time, not correctness. BGSP makes accountability *legible and
non-repudiable*; it does not make decisions good. That remains the named human's
burden — which is the entire point.

---

## 9. Integration points

| Existing component | BGSP integration |
|---|---|
| `GIT_AS_GOVERNANCE.md` | BGSP is the operational protocol for the primitive map it describes. |
| `FOR_AI_MODELS.md` (v4) | High-stakes AI responses can be emitted as **draft** `burgess:` commits, explicitly `Burgess-Classification: NULL` until a human signs. |
| Iris (`iris/`) | Iris drafts and proposes `burgess:` commits and walks a user through signing; Iris itself is never the signer. |
| `onchain-protocol/` | Commit/tree-root anchoring extends evidence anchoring. |
| Verifiable Memory Palace (`ARCHITECTURE.md`) | Holds the facts behind each payload digest under selective disclosure. |
| `git-sovereignty/ARCHITECTURE.md` | How this layer sits alongside the others. |
| [`burgess-sovereign-exit.md`](./burgess-sovereign-exit.md) | **Successor application (BSEP):** applies this signed-commit primitive to the act of *leaving* a system — an individual's sovereign, accountable exit. |

---

## 10. Quick start

```bash
# 1. Draft a burgess commit message (NULL by default — no human has signed yet)
python bgsp.py draft \
  --scope openhear \
  --subject subject:openhear:7f3a9c1e \
  --action "Approve OpenHear left-ear fitting at prescribed gain profile" \
  --facts "Audiogram 2026-05-30; left moderate SNHL; patient consents; no contraindication" \
  --summary "approve left-ear OpenHear fitting" > /tmp/msg.txt

# 2. A named human reviews the specific case, sets Classification: SOVEREIGN,
#    then signs the commit:
git commit -S -F /tmp/msg.txt --allow-empty

# 3. Verify — the signature is the answer:
git log --show-signature -1
python bgsp.py check HEAD

# 4. Trace nullity across a chain of decision files or commits:
python bgsp.py chain examples/decision-ledger/*.commit
```

A new contributor who has read this far can create a SOVEREIGN decision and
verify one. That is the success criterion.

---

*UK Certification Mark <a href="https://trademarks.ipo.gov.uk/ipo-tmcase/page/Results/1/UK00004343685">UK00004343685</a> · MIT Licence — this protocol and its tooling are MIT-licensed; the certification mark is not, and BGSP makes no claim of commercial certification.*
*github.com/ljbudgie/burgess-principle*
