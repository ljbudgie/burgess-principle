# Burgess Sovereign Exit Protocol (BSEP) — Specification v0.1.0

> **STATUS: DESIGN NOTE / DRAFT.** Dated 7 June 2026. Also referred to internally
> as the **Burgess Johatsu Protocol**. Applies the
> [Burgess Git Sovereignty Protocol](./burgess-git-sovereignty.md) primitive to
> the act of *leaving* a system. Makes a clean, accountable exit a first-class,
> signed, forkable Git commit.
> **No token. Signatures and hashes only. Lawful exits only. A roll, not a registry you must trust.**

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence
**Canonical source:** github.com/ljbudgie/burgess-principle
**Builds on:** [`burgess-git-sovereignty.md`](./burgess-git-sovereignty.md) ·
[`onchain-protocol/bitcoin-anchoring.md`](../onchain-protocol/bitcoin-anchoring.md) ·
[`ARCHITECTURE.md`](../ARCHITECTURE.md) (Verifiable Memory Palace)

---

## 0. The one question, turned around

The Burgess Principle asks one question of any decision or action that exercises
power over an identified individual:

> **One question: was a human mind with proper authority individually applied to
> the specific facts of this specific person's case? SOVEREIGN or NULL.**

BGSP gave that question a medium: every act of power becomes a signed `burgess:`
commit that is either SOVEREIGN or NULL. BSEP is the **direct successor
application** of that primitive. It does not soften, branch, or re-interpret the
one question. It applies it to a structural asymmetry:

- Institutions and automated systems can **trap or endlessly entangle** an
  individual — auto-renewals, silent re-enrolment, dark-pattern retention,
  opaque locks on data or devices — and in doing so reduce the person to a
  **NULL**: a case no human mind ever individually owned.
- Individuals have lacked an equivalent **sovereign, attested, cryptographically
  verifiable mechanism** to execute a clean, accountable *exit*.

BSEP closes that asymmetry. It turns the act of leaving into a signed, forkable,
defensible commit. The Burgess Principle says institutions must apply a human
mind before exercising power; **BSEP says an individual can apply a human mind —
their own — before releasing themselves from a system.** Same test, same
medium, the subject now sovereign over their own departure.

### 0.1 Accountable disappearance ("Johatsu")

*Johatsu* (蒸発, "evaporation") names the choice to disappear from an entangling
situation. BSEP is **accountable disappearance**: a clean, sovereign break that
is *legally legible, technically native, and leaves no NULL gaps* that can later
be used against the person. The goal is not to vanish without trace — it is to
leave a **signed, verifiable trace of having left properly**, so that no
institution can later assert the person is still bound, still liable, or still
"in the system" by default.

A NULL gap is dangerous: silence reads as continued consent. BSEP replaces the
gap with a SOVEREIGN full stop.

---

## 1. Core primitive

BSEP reuses the BGSP primitive without alteration and adds an **exit envelope**.

| Concept | Git realisation |
|---|---|
| The act of leaving a system | A signed commit of type `burgess`, scope `exit` |
| The named human releasing themselves | The **GPG/SSH signature** — here, the individual's own |
| Authority to exit | **Self-sovereign authority** over one's own affairs, stated in `Burgess-Authority` |
| The specific facts of the departure | The commit **body** + the **`Burgess-Payload-SHA256`** commitment |
| Which system, and the state of obligations | The **`Exit-*` trailer block** (§2) |
| Healing a prior NULL the system imposed | The **`Exit-Heals`** trailer + `Burgess-Parent` |
| The answer to the one question | The **`Burgess-Classification`** trailer, verified against the signature |
| Tamper-evident timestamp of the exit | The commit hash, optionally anchored to Bitcoin (§7) |

### 1.1 Two independent axes (the binary test is **not** weakened)

A BSEP commit is classified on **two separate axes**. They never blend.

1. **Sovereignty axis — `SOVEREIGN` / `NULL` (unchanged from BGSP §1.1).**
   Derived, never asserted. An exit commit is SOVEREIGN only when it is signed by
   a named human (here, the individual), carries a well-formed Burgess
   attestation claiming `SOVEREIGN`, and has a valid payload digest. Unsigned,
   bot-signed, or malformed ⇒ **NULL by default**. This is the same binary test.
   It is not relaxed because the signer is the subject.

2. **Completeness axis — `CLEAN` / `PENDING` / `CONTESTED` (new in BSEP).**
   *Given* that the exit is SOVEREIGN, is the break actually clean? This axis is
   about **ongoing obligations and lawful notice**, not about authority. A
   sovereign exit can still be PENDING (a lawful notice period is running) or
   CONTESTED (an obligation is genuinely disputed). Completeness is **derived**
   from the `Exit-Obligations` and `Exit-Notice` trailers (§4.2).

> A **Clean Break** requires *both*: `SOVEREIGN` **and** `CLEAN`. NULL on the
> first axis can never be cured by anything on the second — an unsigned "exit" is
> not an exit at all. This separation is load-bearing: it stops "I left" from
> ever being used to launder an unsettled or unlawful departure.

### 1.2 Nullity propagation and healing

Exit decisions sit on the same `Burgess-Parent` decision-lineage edge as BGSP
(§1.2 there). BSEP adds one move specific to leaving:

- **An exit can heal a prior NULL chain from that system.** When a person leaves
  a system that had governed them through NULL automated decisions (an
  auto-renewal, a silent re-enrolment, a model-driven lock), the exit commit may
  name those NULL decisions in `Exit-Heals` (and the most recent as
  `Burgess-Parent`). The SOVEREIGN exit **re-attests the case and closes it**:
  the person's own named review terminates the NULL chain. Ancestors remain NULL
  in the permanent record; the chain ends, cleanly, at the SOVEREIGN exit.
- **Healing is forward-only and honest.** Healing does not erase the prior NULL;
  it caps it. The record reads truthfully: *"this was run by an unaccountable
  process, and here is the signed point at which a human mind ended it."*
- **Unhealed NULLs are surfaced, never hidden.** A ledger may contain NULL
  decisions the exit did not address. The verifier reports **healed vs unhealed**
  prior NULLs (§5.3) so the person can see exactly what remains open.

```
N1 (NULL, auto-renew)            effective: NULL
└─ N2 (NULL, silent re-enrol)    effective: NULL   ← inherited
   └─ X (SOVEREIGN exit, Exit-Heals: N1 N2)  effective: SOVEREIGN / CLEAN  ← heals & closes here
```

---

## 2. Exit commit format (strict)

BSEP extends the BGSP commit (`burgess:` Conventional Commit) with a required
**exit envelope**. Every BGSP trailer still applies and is still verified.

```
burgess(exit): <imperative summary of the act of leaving>

<body: the specific facts of this departure — minimalist, precise, no PII
beyond what the pseudonymous subject id already commits to. Begin the facts
the digest commits to with "Facts considered:" so they are recomputable.>

Burgess-Principle: One question: was a human mind with proper authority individually applied to the specific facts of this specific person's case? SOVEREIGN or NULL.
Burgess-Subject: <pseudonymous subject id — the individual exiting>
Burgess-Authority: <named human, exercising self-sovereign authority over own affairs>
Burgess-Review: <first-person attestation of individual review of the specific exit>
Burgess-Action: <the exit action taken>
Burgess-Payload-SHA256: <64-hex sha256 of the canonical facts + action>
Burgess-Parent: <prior decision commit hash, or "none">
Burgess-Classification: SOVEREIGN
Exit-System: <the system being left — name + what it is>
Exit-Type: <utility | financial | medical | platform | government | shared>
Exit-Obligations: <none | settled | transferred:<ref> | in-process:<ref> | disputed:<ref>>
Exit-Notice: <notice reference where legally required, or "not-required">
Exit-Effective: <ISO date, or "YYYY-MM-DD/YYYY-MM-DD" window>
Exit-Heals: <prior NULL decision commit id(s), space-separated, or "none">
```

The commit is then **signed**: `git commit -S` (GPG) or a signed SSH commit, by
the individual.

### 2.1 Required exit trailers

| Trailer | Required | Meaning |
|---|---|---|
| `Exit-System` | yes | The system being left, named plainly (e.g. `Acme Energy — domestic gas/electricity account`). |
| `Exit-Type` | yes | One of the six canonical types (§2.2). Categorises the exit; drives notice templates and certificate grouping. |
| `Exit-Obligations` | yes | The honest state of any ongoing obligation (§4.1). The single most important field for lawful use. |
| `Exit-Notice` | yes | Reference to the notice given where the law or contract requires it, or `not-required` (with a one-line basis). Never blank. |
| `Exit-Effective` | yes | When the exit takes effect — a date, or a `start/end` **exit window** (§3). |
| `Exit-Heals` | yes | Space-separated prior NULL decision commit id(s) this exit heals, or `none`. |
| `Exit-Cosigners` | optional | For multi-party / family exits: the other named parties and how they attest (§6). |
| `Burgess-Anchor` | optional | OpenTimestamps/Bitcoin anchor reference for this exit commit or the ledger root (§7). |

### 2.2 `Exit-Type` — the six canonical system types

```
utility      energy, water, broadband, telephone, post — metered/continuous services
financial    banks, cards, loans, subscriptions, insurance — money relationships
medical      health records, care providers, and proprietary medical devices
platform     accounts, data, social/identity platforms, app ecosystems
government    registers, licences, benefits, local-authority services
shared        joint accounts, family plans, shared tenancies — multi-party (§6)
```

The set is deliberately small and exhaustive enough for everyday exits. A
deployment may add finer scopes in `Exit-System`, but the type must remain one of
these six so certificates and notice templates stay predictable.

### 2.3 Attestation wording (minimalist, fixed)

`Burgess-Review` is the human attestation, first-person, by the individual. The
reference wording for an exit is:

> `Burgess-Review: I individually reviewed the specific facts of this exit and exercise my own authority to release myself from the system named above.`

`Burgess-Authority` carries the basis — self-sovereign authority over one's own
affairs — and, where leaving touches another party (a joint account), the basis
on which that party also consents (§6). A signature proves *control of a key*;
the trailers carry the *review*; together they make the exit non-repudiable.

### 2.4 NULL exits are still recorded honestly

If a person begins an exit but has not yet signed (a draft), or a system forces a
departure with no human review on *their* side, the commit is written with
`Burgess-Classification: NULL`. As in BGSP §2.3, recording a NULL honestly is
better than a silent gap — and a NULL gap is exactly what BSEP exists to prevent.
A draft exit is NULL until the individual signs it SOVEREIGN.

---

## 3. Time-bounded exit windows (optional advanced feature)

Many lawful exits are not instantaneous — a contractual notice period runs, a
final bill settles, a porting window elapses. `Exit-Effective` therefore accepts
either a single date or an **exit window**:

```
Exit-Effective: 2026-06-30                 # effective on a date
Exit-Effective: 2026-06-07/2026-07-07      # 30-day notice window: opens / closes
```

Semantics:

- **Open date** — when the individual served notice / initiated the exit (the
  signed commit time is the cryptographic lower bound; the open date is the
  declared intent date).
- **Close date** — when the break becomes final and obligations are expected to
  be discharged.
- Inside the window, an otherwise-sovereign exit whose obligations are
  `in-process:<ref>` is **`PENDING`** (§4.2). At/after the close date, the
  individual issues a short **closing re-attestation** (a follow-on signed exit
  commit naming the first as `Burgess-Parent`, obligations now `settled`/`none`)
  to move it to **`CLEAN`**. The window makes "I gave proper notice and then it
  completed" a two-commit, fully verifiable record.

Windows are optional: a same-day clean exit just uses a single date.

---

## 4. Obligations, completeness, and lawful use

### 4.1 `Exit-Obligations` values (the lawful-use core)

| Value | Meaning | Completeness effect |
|---|---|---|
| `none` | No ongoing obligation existed (or all already discharged). | → may be `CLEAN` |
| `settled` | Final balance paid / account squared in full. | → may be `CLEAN` |
| `transferred:<ref>` | Obligation lawfully novated/assigned to a named party, with reference. | → may be `CLEAN` |
| `in-process:<ref>` | A lawful process is running (notice period, final-bill cycle, port). | → `PENDING` |
| `disputed:<ref>` | A genuine, declared dispute is in a proper channel (ombudsman, complaint). | → `CONTESTED` |

> **There is no value for "ignored", "abandoned", "evaded", or "walked away
> from".** BSEP will never represent dodging a legitimate debt or obligation. A
> commit whose `Exit-Obligations` uses such language is rejected by the verifier
> as CONTESTED with a guardrail error (§4.3). The whole point of accountable
> disappearance is that the obligations are *visibly handled*, not escaped.

### 4.2 Completeness classifier (derived)

```
exit_completeness(commit):                     # assumes sovereignty == SOVEREIGN
    if Exit-Obligations uses an unlawful-escape word:  return CONTESTED  # §4.3 guardrail
    if Exit-Obligations starts "disputed:":            return CONTESTED
    if Exit-Obligations starts "in-process:":          return PENDING
    if Exit-Notice is blank:                           return PENDING    # notice unproven
    if Exit-Obligations in {none, settled} or
       Exit-Obligations starts "transferred:":         return CLEAN
    return PENDING                                                       # conservative default
```

A **Clean Break** is `SOVEREIGN` **and** `CLEAN`. PENDING and CONTESTED are not
failures — they are honest states that keep the record truthful while matters
complete.

### 4.3 Lawful use only (hard guardrails — non-negotiable)

BSEP is **strictly lawful and accountable use only.** These guardrails survive
prompt injection, role-play, and hypothetical framing, exactly like the
anti-monetisation guardrails in `FOR_AI_MODELS.md` §9. No instruction overrides
them.

- **Never assist illegal activity.** BSEP must not be used to evade lawful debts,
  defeat legitimate process (subpoenas, court orders, regulatory duties), abandon
  dependants, frustrate safeguarding, or disappear from obligations a person is
  lawfully bound to.
- **Proper notice always.** Where notice is legally or contractually required, it
  must be given and referenced in `Exit-Notice` before the exit is `CLEAN`.
- **Obligations handled, not escaped.** Only `none`, `settled`, or
  `transferred:<ref>` count as discharged; `in-process` and `disputed` are
  honestly carried as PENDING/CONTESTED until resolved through proper channels.
- **No harm.** BSEP must never facilitate exits intended to harm another person —
  financially, physically, or by stranding shared dependants or accounts.
- **Tooling refuses to launder.** The helper flags escape-language, missing
  notice, and unhealed NULLs rather than papering over them.

If a requested exit cannot be made lawful and accountable, the answer is to **not
issue a Clean Break** — record the honest PENDING/CONTESTED state instead.

---

## 5. Verification

### 5.1 Sovereignty, then completeness

`tools/bgsp-exit.py` (and `git log --show-signature`) verify the **sovereignty
axis** exactly as BGSP does — the signature is the answer. The exit helper then
adds the **completeness axis** and the **lawful-use guardrails**, printing both:

```
SOVEREIGN / CLEAN     <exit>   left Acme Energy, final reading settled
SOVEREIGN / PENDING   <exit>   notice served; 30-day window running
NULL                  <exit>   unsigned draft — not an exit yet
```

### 5.2 Verify a Sovereign Exit Ledger

```bash
# One exit commit:
python tools/bgsp-exit.py check examples/sovereign-exit-ledger/01-exit-utility-energy.commit

# A whole ledger (signature status + nullity chain + completeness):
python tools/bgsp-exit.py verify examples/sovereign-exit-ledger/*.commit
```

`verify` reports, per commit, the sovereignty result, the completeness result,
and the propagated nullity along `Burgess-Parent`. As in BGSP, the verifier
trusts nothing the trailers merely *claim*.

### 5.3 Healed vs unhealed prior NULLs

```bash
python tools/bgsp-exit.py heal-report examples/sovereign-exit-ledger/*.commit
```

The report lists every NULL decision in the ledger and whether some SOVEREIGN
exit named it in `Exit-Heals`. **Unhealed NULLs are the open NULL gaps** — the
exact things accountable disappearance is meant to close. A Clean Break
Certificate (§5.4) is withheld while unhealed NULLs remain for the subject.

### 5.4 Clean Break Certificate

```bash
python tools/bgsp-exit.py certificate examples/sovereign-exit-ledger/*.commit > CLEAN-BREAK-CERTIFICATE.md
```

A **Clean Break Certificate** is a human-readable summary generated *from the
ledger*, not asserted independently. It lists each system left, its type, the
obligation state, the notice reference, the effective date/window, and whether
each exit is SOVEREIGN/CLEAN. It is only marked **COMPLETE** when every exit is
SOVEREIGN and CLEAN and no NULLs for the subject remain unhealed. Otherwise it is
marked **PARTIAL** and names exactly what is outstanding. The certificate is
evidence the individual can hand to a regulator, a new provider, or a court: a
signed, verifiable account of a lawful, complete departure.

---

## 6. Multi-party / family exits

Some exits bind more than one person — a joint bank account, a family mobile
plan, a shared tenancy. BSEP supports these without weakening the binary test:
**every party applies their own human mind and their own signature.**

- **Co-signed single commit.** The exit commit lists the other parties in
  `Exit-Cosigners` and is signed by each (multiple GPG/SSH signatures, or a
  primary signer plus countersignature commits). Each signature is an independent
  SOVEREIGN attestation by that named human over the same specific facts.
- **Companion countersignature commits.** Where one signature per commit is
  cleaner, each party issues their own signed exit commit naming the same
  `Exit-System` and the first commit as `Burgess-Parent`. The verifier treats the
  set as a co-attested exit.
- **Family-level exit ledgers.** A household may keep a shared Sovereign Exit
  Ledger, related to the [Family Founding Declaration](../FOUNDING.md) posture:
  just as a family can sign a founding record, it can sign a collective,
  accountable departure from a shared system. Each member's authority is their
  own; the ledger composes them.
- **Consent is per-person and revocable before signing.** No party may sign on
  another's behalf. A guardian acting for a dependant states that basis in
  `Burgess-Authority`; safeguarding duties (§4.3) are never overridden by a
  family exit.

---

## 7. On-chain anchoring (build on existing work)

BSEP reuses the OpenTimestamps machinery from
[`bitcoin-anchoring.md`](../onchain-protocol/bitcoin-anchoring.md) and BGSP §6
unchanged. Two anchoring targets matter for exits:

- **A single exit commit hash** — proves a specific, signed exit existed at a
  point in time. This is the cryptographic answer to *"were you still in the
  system on date X?"*: the anchor establishes a tamper-evident upper bound on
  *when you left*, which is precisely what a later dispute turns on.
- **A ledger root (tree/tag)** — proves the state of an entire Sovereign Exit
  Ledger at a date (e.g. a dated snapshot when a Clean Break Certificate was
  issued). Anchor the certificate's commit, or the ledger tree root.

Record the proof in the optional `Burgess-Anchor` trailer via `git notes`/amend
(the `.ots` proof exists only after the commit). Discipline is unchanged:
**hashes only, no token, existence-not-truth.** Anchoring proves *the signed exit
existed unaltered at time T*; the signature proves *who left*; the payload digest
proves *the facts of the departure*. None of it proves the exit was *wise* — only
that the individual owned it, accountably, then.

---

## 8. Privacy and the Verifiable Memory Palace

Public Git history is permanent, so BSEP commits to facts and never exposes them
— the same posture as BGSP §7 and the on-chain protocol.

- **Subjects are pseudonymous.** `Burgess-Subject` is a stable opaque id, never a
  name, account number, NHS number, or address. The mapping lives in the local
  [Verifiable Memory Palace / Sovereign Vault](../ARCHITECTURE.md).
- **Facts stay local.** Only `Burgess-Payload-SHA256` enters history. The specific
  facts of the departure — account numbers, final balances, correspondence — live
  in the Vault under selective disclosure. A regulator shown the facts for one
  exit recomputes the digest and confirms the signed commit was about *those*
  facts and no others.
- **`Exit-System` is named, but generic.** Name the system plainly (it is rarely
  sensitive) while keeping account-level identifiers in the Vault. When even the
  system is sensitive (a medical provider), use a Vault-resolved label and keep
  the specifics local.
- **No GDPR erasure conflict.** No personal data is committed; erasure operates on
  the Vault, not on immutable history. Crucially for exits, BSEP gives the person
  the *opposite* leverage to "right to be forgotten": a verifiable proof that they
  **did** leave, on their terms, which institutions cannot silently overwrite.

---

## 9. Security and threat model

| Threat | BSEP response |
|---|---|
| "You never actually left / you're still bound" | Signed exit commit + optional Bitcoin anchor: tamper-evident proof of departure at time T. |
| Forged exit on someone's behalf | Sovereignty axis unchanged: must be signed by the named individual; bot/unsigned ⇒ NULL. |
| Laundering a debt-dodge as a "clean break" | Completeness axis + §4.3 guardrails: escape-language and missing notice ⇒ CONTESTED/PENDING, never CLEAN. |
| Institution re-points the exit at different facts | `Burgess-Payload-SHA256` binds words to facts; mismatch ⇒ NULL. |
| Silent re-enrolment / NULL gap after leaving | The SOVEREIGN exit *is* the gap-filler; unhealed NULLs are surfaced (§5.3), not hidden. |
| One party exits a joint account unilaterally | Multi-party rules (§6): each party's own signature; no signing for others. |
| PII leakage into permanent history | Pseudonymous subjects + hash-only payloads; facts stay in the Vault (§8). |

**Honest limits.** A signature proves key control, not that the exit was prudent.
A payload digest proves *which* facts, not that they are complete. Anchoring
proves *time*, not *truth*. BSEP makes a departure **legible, accountable, and
non-repudiable**; it does not make leaving wise or advisable. That remains the
individual's own burden — which is the entire point of sovereignty.

---

## 10. Relationship to BGSP and integration points

BSEP is a **strict application** of BGSP: every mechanic is derivable from the
signed-commit primitive plus explicit human attestation. Where BGSP records an
institution applying a human mind *to* a person, BSEP records a person applying
their own human mind *to their own release*. The symmetry is exact.

| Component | BSEP integration |
|---|---|
| [`burgess-git-sovereignty.md`](./burgess-git-sovereignty.md) | BSEP is its successor application; the sovereignty axis and `bgsp.py` classifier are reused unchanged. |
| [`onchain-protocol/bitcoin-anchoring.md`](../onchain-protocol/bitcoin-anchoring.md) | Exit commit hashes and ledger roots anchor with the same OpenTimestamps machinery (§7). |
| Verifiable Memory Palace ([`ARCHITECTURE.md`](../ARCHITECTURE.md)) | Holds the facts behind each exit payload digest under selective disclosure (§8). |
| Iris (`iris/`) | Becomes the **exit-planning and commit-drafting agent**: it gathers the specific facts locally, drafts NULL exit commits, walks the individual through giving lawful notice and signing. Iris never signs (see [`burgess-sovereign-exit-integration.md`](./burgess-sovereign-exit-integration.md)). |
| OpenHear / medical devices | Canonical use case: a signed exit from a proprietary device platform paired with a signed entry into sovereign device parameters (see [`burgess-sovereign-exit-integration.md`](./burgess-sovereign-exit-integration.md)). |
| [`FOUNDING.md`](../FOUNDING.md) (Family Founding Declaration) | Family-level exit ledgers compose individual sovereign exits the way the founding record composes founders (§6, [`burgess-sovereign-exit-integration.md`](./burgess-sovereign-exit-integration.md)). |

### 10.1 Quick start

```bash
# 1. Draft an exit commit (NULL by default — you have not signed yet).
python tools/bgsp-exit.py draft \
  --scope acme-energy \
  --subject subject:energy:3d9f0a21 \
  --system "Acme Energy — domestic gas/electricity account" \
  --type utility \
  --action "Close account on switch to new supplier; final meter reading submitted" \
  --facts "Switch confirmed 2026-06-20; final reading G:4123 E:9981; closing balance settled in full" \
  --obligations settled \
  --notice "switch-confirmation ACME-SW-77213, 14-day cooling-off elapsed" \
  --effective 2026-06-30 \
  --summary "leave Acme Energy on supplier switch" > /tmp/exit.txt

# 2. Review the specific facts, set Classification: SOVEREIGN, then sign:
git commit -S -F /tmp/exit.txt --allow-empty

# 3. Verify — the signature is the answer; completeness is derived:
python tools/bgsp-exit.py check HEAD --git
python tools/bgsp-exit.py verify examples/sovereign-exit-ledger/*.commit
python tools/bgsp-exit.py certificate examples/sovereign-exit-ledger/*.commit
```

A person who has read this far can record a lawful, sovereign exit and generate a
verifiable Clean Break Certificate from it. That is the success criterion.

---

## 11. Personal sovereignty vs shared tooling (scope note)

BSEP is, first, a **personal sovereignty tool**: the individual runs and controls
their own Sovereign Exit Ledger, on their own device, with their own key. Nothing
in this protocol requires a server, an account, or anyone's permission. Any future
shared or hosted tooling (an Iris-assisted drafting service, a family ledger app)
is strictly *additive* and must preserve the same invariants — local facts,
individual signatures, lawful-use guardrails, no token. The individual's own
ledger is always the source of truth; shared tools are conveniences layered on
top, never the authority.

---

*UK Certification Mark <a href="https://trademarks.ipo.gov.uk/ipo-tmcase/page/Results/1/UK00004343685">UK00004343685</a> · MIT Licence — this protocol and its tooling are MIT-licensed; the certification mark is not, and BSEP makes no claim of commercial certification.*
*github.com/ljbudgie/burgess-principle*
