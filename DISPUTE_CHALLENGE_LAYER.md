# Dispute / Challenge Layer

**The Burgess Principle**
UK Certification Mark No. UK00004343685

> **STATUS: DESIGN NOTE / DRAFT.** A minimalist, decision-level process for
> contesting a SOVEREIGN or NULL finding. **No token. Hashes-only on public
> ledgers. Named human accountability preserved end to end.**

This note defines a Dispute / Challenge Layer that lets any party — an individual,
an institution, or an independent verifier — contest a finding without changing
the constitution of the Burgess Principle, without new legal infrastructure, and
without surrendering sovereignty. It composes with the components that already
exist: the SOVEREIGN/NULL binary test, the Git governance substrate, Bitcoin
proof-of-existence anchoring, the `did:key` / Verifiable Credential identity
profile, and the nexus-ai-hub policy wrapper.

---

## 1. Why a challenge layer, and why minimalist

The current stack is strong at *creating* findings and *proving they existed*. It
is silent on what happens when someone says **"this finding is wrong."** Without a
defined path, a dispute degrades into ad-hoc email, private pressure, or quiet
revision — exactly the institutional behaviours the Principle exists to expose.

The design goal is the smallest layer that turns "I disagree" into an
**attributable, cryptographically linked, independently verifiable record** that
itself obeys the SOVEREIGN test.

Non-negotiables (inherited from the existing stack):

- **Decision-level, low-friction.** A challenge is a signed JSON file plus a Git
  commit. No new constitution, no court, no central registrar required.
- **Hashes only on public ledgers.** Public records and anchors carry SHA-256
  commitments, never the underlying facts.
- **Named human + genuine consideration + attributable record.** A challenge is
  *reviewed* by a named human applying the same binary test. Automation may
  triage and route; it never decides the outcome.
- **No token, no new blockchain, no on-chain voting, no mandatory third party.**

> **Rationale & trade-offs.** Keeping the layer at the *decision* level (a finding
> can be challenged) rather than the *constitutional* level (the test itself is up
> for vote) is what keeps it small. The trade-off is that this layer cannot settle
> disputes about the doctrine itself — only about whether a specific finding
> correctly applied the doctrine. That boundary is deliberate: doctrine changes
> belong in the Git/PR governance track, not in a per-finding dispute.

---

## 2. States and lifecycle

A finding moves through an explicit, append-only state machine. State is recorded
in Git; transitions are signed acts by named identities.

```
                 ┌─────────────────┐
                 │  FINDING ISSUED │  (SOVEREIGN or NULL VC exists)
                 └────────┬────────┘
                          │ challenge submitted + linked
                          ▼
                 ┌─────────────────┐
                 │   CHALLENGED    │  challenge VC anchored
                 └────────┬────────┘
                          │ named reviewer accepts the matter
                          ▼
                 ┌─────────────────┐
                 │  UNDER REVIEW   │  reviewer applies SOVEREIGN/NULL test
                 └───┬─────┬─────┬─┘
            upheld   │     │     │   amended
                     ▼     │     ▼
         ┌──────────────┐  │  ┌──────────────┐
         │   UPHELD     │  │  │   AMENDED    │  (supersedes via new finding VC)
         └──────────────┘  │  └──────────────┘
                           ▼ overturned
                  ┌──────────────┐
                  │  OVERTURNED  │
                  └──────────────┘

   (optional, time-bounded) any terminal state → ESCALATED → UNDER REVIEW
```

| State | Meaning | Who can cause the transition |
|---|---|---|
| `FINDING_ISSUED` | A SOVEREIGN/NULL finding exists as a VC. | Original named reviewer / issuer |
| `CHALLENGED` | A linked, signed challenge has been recorded. | Any party (challenger) |
| `UNDER_REVIEW` | A named reviewer has accepted the challenge for genuine consideration. | Named reviewer (not the challenger) |
| `UPHELD` | Review concludes the original finding stands. | Named reviewer |
| `OVERTURNED` | Review concludes the original finding was wrong. | Named reviewer |
| `AMENDED` | Review issues a corrected superseding finding. | Named reviewer |
| `ESCALATED` | A terminal outcome is re-opened under the escalation path. | Challenger or independent verifier, within window |
| `WITHDRAWN` | Challenger withdraws before review concludes. | Challenger |
| `EXPIRED` | A time-bounded window closed with no qualifying action. | System (deterministic, from timestamps) |

Rules:

1. States are **append-only**. `OVERTURNED` does not delete the original finding;
   it records a superseding decision. Both remain permanently visible (Git
   `revert` semantics, never history rewrite).
2. The reviewer who moves a finding to `UNDER_REVIEW` **must not** be the
   challenger, and **should not** be the original issuer for `OVERTURNED`/
   `AMENDED` outcomes where an independent reviewer is available.
3. `AMENDED` always produces a *new* finding VC that references the original by
   hash; the original is marked superseded, not erased.

> **Rationale & trade-offs.** Three outcomes (upheld / overturned / amended) cover
> the realistic space without the combinatorial complexity of graded verdicts.
> `EXPIRED` exists so that institutions can adopt bounded windows for operational
> certainty; individuals who need no deadline can simply leave windows unset
> (`0` = no expiry, mirroring the on-chain `expiry` field). The trade-off of
> append-only state is storage growth — acceptable, because the whole point is a
> record that cannot be quietly revised.

---

## 3. Identity and roles

Roles reuse the existing identity profile (`CRYPTOGRAPHIC_IDENTITY.md`): `did:key`
with Ed25519, W3C VCs, optional WebAuthn/FIDO2 for high-stakes signing.

| Role | Identifier | Responsibility |
|---|---|---|
| **Original issuer** | `did:key` of the named reviewer who issued the finding | Holds the finding being challenged |
| **Challenger** | `did:key` (individual) or institutional DID/LEI/plain name | Submits the challenge VC |
| **Review reviewer** | `did:key` controlled by a named human | Applies the SOVEREIGN/NULL test to the challenge and issues the Review Outcome VC |
| **Independent verifier** *(optional)* | `did:key` | Re-checks crypto + named-human sufficiency; may trigger `ESCALATED` |
| **nexus-ai-hub policy wrapper** | service identity (advisory only) | Triages, validates links, anchors, routes — **never decides** |

A DID proves key control, not humanity. As in the rest of the stack, a challenge
or outcome is only SOVEREIGN where the disclosed or auditable record binds the key
to a real named human who genuinely considered the specific facts.

> **Rationale & trade-offs.** Separating *challenger* from *reviewer* is the single
> most important integrity rule: it prevents a party from grading its own homework.
> The trade-off for a lone individual is that overturning your *own* finding still
> needs a second named human for full independence — but the design degrades
> gracefully (see §9): a self-review is still valid and attributable, just clearly
> labelled as non-independent.

---

## 4. How a challenge is submitted and linked

A challenge is a signed Verifiable Credential that **points at the original
finding by hash** and asserts a specific defect.

### 4.1 Cryptographic linkage

```
challenge.credentialSubject.challengedFinding.vcHash   = sha256(canonical finding VC)
challenge.credentialSubject.challengedFinding.findingId = urn:... of the finding
challenge.credentialSubject.grounds                    = enum (see §4.2)
challenge.credentialSubject.statementHash              = sha256(challenger's full statement)
```

The challenge VC is signed by the challenger's DID key. The **full statement of
why** the finding is wrong stays local (or is selectively disclosed); only its
`sha256:` commitment is public. This preserves hashes-only discipline while still
binding the challenge to immutable content.

### 4.2 Grounds (closed vocabulary)

Grounds map directly onto the SOVEREIGN test, so a challenge is never vague:

| Ground | Asserts that the original finding… |
|---|---|
| `no_named_human` | attributed to a human who did not actually consider the matter |
| `incomplete_facts` | was decided without the full relevant facts |
| `no_genuine_consideration` | applied a template/automation rather than individual consideration |
| `not_accountable` | lacks an attributable, durable accountability record |
| `factual_error` | rests on a demonstrable factual mistake (statement discloses it) |
| `wrong_classification` | should be NULL not SOVEREIGN, or vice-versa |
| `procedural` | breached the documented process (e.g. issuer reviewed own challenge) |

### 4.3 Submission flow

```
1. Challenger obtains the finding VC (or its published vcHash).
2. Challenger writes a local statement; computes statementHash = sha256(statement).
3. Challenger builds a Challenge VC (schema in §6) linking findingId + vcHash +
   grounds + statementHash, signs with did:key Ed25519 (high-stakes: + WebAuthn).
4. Challenger computes challengeHash = sha256(canonical Challenge VC).
5. Record the challenge in Git (commit trailer Burgess-Challenge: sha256:...).
6. Anchor challengeHash to Bitcoin via OpenTimestamps (hash-only).
7. State transitions FINDING_ISSUED → CHALLENGED.
```

> **Rationale & trade-offs.** A closed grounds vocabulary keeps challenges
> machine-routable and forces the challenger to map their objection onto the test,
> rather than into open-ended grievance. The trade-off is reduced expressiveness;
> we mitigate it with the free-text statement (committed by hash) so nuance is
> preserved off-ledger without polluting the public record.

---

## 5. The review and outcome

A named reviewer accepts the challenge (`UNDER_REVIEW`), applies the **same binary
test**, and issues a **Review Outcome VC**.

```
1. Reviewer (≠ challenger) accepts: CHALLENGED → UNDER_REVIEW (signed transition).
2. Reviewer reads the disclosed finding + challenge statement + facts.
3. Reviewer applies SOVEREIGN/NULL: was the *original* finding itself the product
   of a named human with full facts and genuine individual consideration?
4. Reviewer records reasoning locally; reasoningHash = sha256(reasoning).
5. Reviewer builds a Review Outcome VC (schema in §6):
     outcome ∈ { UPHELD, OVERTURNED, AMENDED }
     references challengeHash + original findingId/vcHash
     supersedingFindingId (only when AMENDED)
6. Reviewer signs, anchors outcomeHash, transitions state.
7. If AMENDED: issue a new finding VC; mark the original superseded-by hash.
```

The outcome VC is itself a Burgess artefact: it names the reviewing human, commits
to their reasoning by hash, and is anchored. A dispute resolution is therefore
held to exactly the standard it adjudicates.

> **Rationale & trade-offs.** Making the *outcome* a first-class VC (rather than a
> mere status flag) means the resolution carries its own named-human accountability
> and its own anchor — you can audit the reviewer as rigorously as the original
> issuer. The trade-off is two VCs per dispute instead of one flag; this is the
> price of the record being self-auditing.

---

## 6. Verifiable Credential schemas

Two minimal credential types are added. Full JSON Schemas live under
[`schemas/`](./schemas/); the credential subjects are summarised here.

### 6.1 Challenge Credential — `BurgessChallengeCredential`

Minimum `credentialSubject` fields:

| Field | Type | Description |
|---|---|---|
| `id` | URN | `urn:burgess:challenge:<uuid>` |
| `challengedFinding.findingId` | URN | The finding being contested |
| `challengedFinding.vcHash` | `sha256:<hex>` | Commitment to the original finding VC |
| `grounds` | enum[] | One or more values from §4.2 |
| `statementHash` | `sha256:<hex>` | Commitment to the challenger's full written statement |
| `challenger.did` | DID | Challenger key controller |
| `challenger.name` | string | Named human, where disclosure is lawful |
| `requestedRemedy` | enum | `review` \| `overturn` \| `amend` |
| `window` | object, optional | `{ opensAt, closesAt }` ISO 8601 for time-bounded disputes |

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/security/suites/ed25519-2020/v1",
    "https://theburgessprinciple.com/contexts/burgess-v1"
  ],
  "id": "urn:uuid:1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed",
  "type": ["VerifiableCredential", "BurgessChallengeCredential"],
  "issuer": {
    "id": "did:key:z6MkChallengerKeyExampleAaBbCcDdEeFfGgHhIiJjKkLl",
    "name": "Named Human Challenger"
  },
  "validFrom": "2026-06-06T22:00:00Z",
  "credentialSubject": {
    "id": "urn:burgess:challenge:1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed",
    "challengedFinding": {
      "findingId": "urn:uuid:0f8a4f6c-8a4f-4a72-8b2f-2d0e3d4b5c6a",
      "vcHash": "sha256:cb4faed1111f53f9d1753b833eb67aa0c11758cd0aed6cb0a9f93a11900ec1d8"
    },
    "grounds": ["no_genuine_consideration", "incomplete_facts"],
    "statementHash": "sha256:b111c6e1d318f203063e5c16bab43c108326af0aa2f7b65760c95547a43dbe52",
    "challenger": {
      "did": "did:key:z6MkChallengerKeyExampleAaBbCcDdEeFfGgHhIiJjKkLl",
      "name": "Named Human Challenger"
    },
    "requestedRemedy": "review",
    "window": { "opensAt": "2026-06-06T22:00:00Z", "closesAt": "2026-07-06T22:00:00Z" }
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-06-06T22:00:00Z",
    "verificationMethod": "did:key:z6MkChallengerKeyExampleAaBbCcDdEeFfGgHhIiJjKkLl#z6MkChallengerKeyExampleAaBbCcDdEeFfGgHhIiJjKkLl",
    "proofPurpose": "assertionMethod",
    "proofValue": "zExampleChallengeSignatureValue"
  }
}
```

### 6.2 Review Outcome Credential — `BurgessReviewOutcomeCredential`

Minimum `credentialSubject` fields:

| Field | Type | Description |
|---|---|---|
| `id` | URN | `urn:burgess:review:<uuid>` |
| `challengeRef.challengeId` | URN | The challenge being resolved |
| `challengeRef.challengeHash` | `sha256:<hex>` | Commitment to the Challenge VC |
| `originalFinding.findingId` | URN | The finding reviewed |
| `originalFinding.vcHash` | `sha256:<hex>` | Commitment to the original finding VC |
| `outcome` | enum | `UPHELD` \| `OVERTURNED` \| `AMENDED` |
| `reasoningHash` | `sha256:<hex>` | Commitment to the reviewer's reasoning record |
| `reviewer.did` | DID | Reviewing named human |
| `reviewer.name` | string | Named human, where lawful |
| `independence` | object | `{ reviewerIsChallenger: false, reviewerIsIssuer: bool }` |
| `supersedingFindingId` | URN, optional | New finding VC id when `outcome = AMENDED` |
| `methodology` | object | Same booleans as a finding: fullFacts, genuineIndividualConsideration, personalAccountability, automationOnly |

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/security/suites/ed25519-2020/v1",
    "https://theburgessprinciple.com/contexts/burgess-v1"
  ],
  "id": "urn:uuid:7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "type": ["VerifiableCredential", "BurgessReviewOutcomeCredential"],
  "issuer": {
    "id": "did:key:z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy",
    "name": "Named Human Reviewer (Review)"
  },
  "validFrom": "2026-06-20T10:00:00Z",
  "credentialSubject": {
    "id": "urn:burgess:review:7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "challengeRef": {
      "challengeId": "urn:burgess:challenge:1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed",
      "challengeHash": "sha256:bfb79f0f7b97dd0e7e4d2e375fd3cab18300b37dddaa0881824d7be86d34e8a7"
    },
    "originalFinding": {
      "findingId": "urn:uuid:0f8a4f6c-8a4f-4a72-8b2f-2d0e3d4b5c6a",
      "vcHash": "sha256:cb4faed1111f53f9d1753b833eb67aa0c11758cd0aed6cb0a9f93a11900ec1d8"
    },
    "outcome": "AMENDED",
    "reasoningHash": "sha256:0c4d01e81bb3d1fd0dc4a0b4224518953794068715317ff39e0bbfc29e4ab06a",
    "reviewer": {
      "did": "did:key:z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy",
      "name": "Named Human Reviewer (Review)"
    },
    "independence": { "reviewerIsChallenger": false, "reviewerIsIssuer": false },
    "supersedingFindingId": "urn:uuid:2d0e3d4b-5c6a-4f72-8b2f-0f8a4f6c8a4f",
    "methodology": {
      "fullFacts": true,
      "genuineIndividualConsideration": true,
      "personalAccountability": true,
      "automationOnly": false
    }
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-06-20T10:00:00Z",
    "verificationMethod": "did:key:z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy#z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy",
    "proofPurpose": "assertionMethod",
    "proofValue": "zExampleReviewOutcomeSignatureValue"
  }
}
```

> **Rationale & trade-offs.** Both credentials reuse the finding VC's `@context`,
> `sha256:` hash convention, and `methodology` block, so existing verifiers need
> almost no new code. The `independence` object makes the self-review limitation
> *explicit and checkable* rather than hidden. Trade-off: we add two `type` values
> and two schemas, but no new cryptography, no new wire format, and nothing on a
> public ledger except hashes.

---

## 7. nexus-ai-hub integration (advisory only)

The policy wrapper validates, links, anchors, and routes a challenge. It performs
**no adjudication** — every decision edge is reserved for a named human. The sketch
below shows the submit and process paths.

```python
"""Dispute / Challenge Layer handlers for the nexus-ai-hub policy wrapper.

ADVISORY ONLY. The hub triages, validates cryptographic links, anchors hashes,
and routes to a named human. It never sets UPHELD / OVERTURNED / AMENDED itself.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

VALID_GROUNDS = {
    "no_named_human", "incomplete_facts", "no_genuine_consideration",
    "not_accountable", "factual_error", "wrong_classification", "procedural",
}
VALID_OUTCOMES = {"UPHELD", "OVERTURNED", "AMENDED"}


def sha256_canonical(obj: dict) -> str:
    """Deterministic sha256 over canonical (sorted, compact) JSON."""
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class TriageResult:
    accepted: bool
    challenge_hash: str | None
    reasons: list[str]
    # The hub may RECOMMEND a route; it never decides the outcome.
    routed_to: str | None = None


def submit_challenge(
    challenge_vc: dict,
    finding_vc: dict,
    verify_ed25519,            # callable(vc) -> bool, verifies proof vs DID doc
    anchor_hash,               # callable(hash_str) -> None, OpenTimestamps
    record_git,                # callable(state, hash_str, meta) -> None
) -> TriageResult:
    """Validate and record a challenge. Returns advisory triage only."""
    reasons: list[str] = []
    subject = challenge_vc.get("credentialSubject", {})

    # 1. Structural + vocabulary checks (machine-safe, no judgement).
    grounds = set(subject.get("grounds", []))
    if not grounds or not grounds.issubset(VALID_GROUNDS):
        reasons.append("invalid_or_missing_grounds")

    # 2. Cryptographic linkage: the challenge must commit to THIS finding.
    expected = sha256_canonical(finding_vc)
    linked = subject.get("challengedFinding", {}).get("vcHash")
    if linked != expected:
        reasons.append("finding_link_mismatch")

    # 3. Signature: challenger controls the asserting key.
    if not verify_ed25519(challenge_vc):
        reasons.append("bad_challenger_signature")

    # 4. Independence guard prepared for the review step: a challenger must not
    #    later self-review. Record the challenger DID for the router to enforce.
    challenger_did = subject.get("challenger", {}).get("did")
    if not challenger_did:
        reasons.append("missing_challenger_did")

    if reasons:
        return TriageResult(accepted=False, challenge_hash=None, reasons=reasons)

    challenge_hash = sha256_canonical(challenge_vc)
    anchor_hash(challenge_hash)                       # hash-only on Bitcoin
    record_git("CHALLENGED", challenge_hash, {        # named-human Git trailer
        "challenger_did": challenger_did,
        "grounds": sorted(grounds),
    })
    # Advisory routing only: suggest a human reviewer who is NOT the challenger.
    return TriageResult(
        accepted=True,
        challenge_hash=challenge_hash,
        reasons=[],
        routed_to="named-human-review-queue",
    )


def process_review_outcome(
    outcome_vc: dict,
    challenge_hash: str,
    challenger_did: str,
    verify_ed25519,
    anchor_hash,
    record_git,
) -> dict:
    """Record a NAMED HUMAN's outcome. The hub only validates + anchors it."""
    subject = outcome_vc.get("credentialSubject", {})
    reviewer_did = subject.get("reviewer", {}).get("did")
    outcome = subject.get("outcome")

    # Hard guard: the hub refuses to record a self-reviewed outcome.
    if reviewer_did == challenger_did:
        raise PermissionError("reviewer_is_challenger: independence violated")
    if outcome not in VALID_OUTCOMES:
        raise ValueError("invalid_outcome")
    if subject.get("challengeRef", {}).get("challengeHash") != challenge_hash:
        raise ValueError("outcome_not_linked_to_challenge")
    if not verify_ed25519(outcome_vc):              # reviewer's named key
        raise ValueError("bad_reviewer_signature")

    outcome_hash = sha256_canonical(outcome_vc)
    anchor_hash(outcome_hash)
    record_git(outcome, outcome_hash, {             # UPHELD/OVERTURNED/AMENDED
        "reviewer_did": reviewer_did,
        "superseding": subject.get("supersedingFindingId"),
    })
    return {"state": outcome, "outcome_hash": outcome_hash}
```

> **Rationale & trade-offs.** Every function either *validates maths* or *records a
> human's signed act*; none contains a branch that picks an outcome. The hub's most
> assertive action is `routed_to="named-human-review-queue"` — a recommendation.
> The hard `PermissionError` on self-review encodes the §3 independence rule in
> code, not just prose. Trade-off: a fully isolated individual hits that guard when
> trying to review their own finding (addressed in §9).

---

## 8. Integration with Git-as-governance and Bitcoin anchoring

### 8.1 Git-as-governance

Each state transition is a Git act, reusing the primitive map in
`GIT_AS_GOVERNANCE.md`:

- **Commit** — every transition (`CHALLENGED`, `UNDER_REVIEW`, `UPHELD`, …) is a
  named commit with trailers, e.g.:
  ```
  Burgess-Finding:    urn:uuid:0f8a4f6c-...
  Burgess-Challenge:  sha256:7c2e9f01...
  Burgess-State:      UNDER_REVIEW
  Burgess-DID:        did:key:z6MkReviewer...
  ```
- **Branch** — a contested finding may be tracked on a `dispute/<finding-id>`
  branch; merge to canonical only when an outcome VC exists.
- **Revert semantics** — `OVERTURNED`/`AMENDED` are recorded as superseding
  commits. History is never rewritten; both the original and the correction stay
  permanently visible (no quiet edits).
- **Tag** — a resolved high-stakes dispute may be tagged (`dispute-<id>-resolved`)
  with the outcome VC hash in the annotation.
- **Append-only ledger** — `LIVE_AUDIT_LOG.md` gains challenge/outcome rows
  carrying only ids and `sha256:` hashes.

### 8.2 Bitcoin anchoring

Per `onchain-protocol/bitcoin-anchoring.md`, anchoring is hash-only
proof-of-existence:

- `anchor(challengeHash)` proves *when* the challenge existed.
- `anchor(outcomeHash)` proves *when* the resolution existed.
- Time-bounded windows (§4.2 `window`) are verifiable: a challenge anchored after
  `closesAt` can be shown to be late; an outcome anchored before the window opened
  is anomalous.
- OpenTimestamps aggregation keeps this **free and token-less**; only digests
  touch Bitcoin.

> **Rationale & trade-offs.** Re-using Git commits + OpenTimestamps means the
> dispute layer adds *no new infrastructure* — it is the existing substrate applied
> to two new artefact types. The trade-off is that ordering precision is bounded by
> Bitcoin's block cadence; for decision-level disputes (days/weeks), this is more
> than sufficient.

---

## 9. Accessibility and sovereignty (lone, profoundly deaf operator)

This layer must be fully operable by a profoundly deaf, self-taught operator
working **alone, on an iPhone, with no support network**, who requires
email/post-only reasonable adjustments. Concretely:

- **No phone, no video, no live appointments.** Submitting a challenge and
  receiving an outcome are file exchanges (signed JSON), shareable by email or
  printed/posted as plain text. Nothing requires a call or a hearing.
- **Local-first generation.** Keys, DIDs, the challenge statement, hashes, and the
  Challenge VC are all generated on-device; no custodial wallet, exchange account,
  or proprietary identity app is required.
- **Plain, inspectable artefacts.** Every record is human-readable JSON plus a
  SHA-256 hash that can be recomputed by hand or with a one-line command.
- **Graceful degradation of independence.** Full independence wants a *second*
  named human (reviewer ≠ challenger). A lone operator who has no second human can
  still:
  1. file a fully valid, anchored challenge against an institution's finding
     (the common case — the institution supplies the reviewer); and
  2. when reviewing their *own* finding, issue a Review Outcome VC explicitly
     flagged `independence.reviewerIsIssuer: true`. It is valid and attributable;
     it is simply, and honestly, labelled non-independent — so a later independent
     verifier can re-open it via the escalation path.
- **Optional, accessible hardware.** iPhone passkeys / WebAuthn satisfy the
  high-stakes ceremony without specialist devices, but are never mandatory.
- **No deadline pressure by default.** Windows are opt-in. A lone individual can
  leave `window` unset so that an institution cannot run out the clock on them.
- **Escalation without a central authority.** Escalation (§10) is an *invitation to
  any independent verifier*, not a petition to a gatekeeper — so isolation never
  means a dead end.

> **Rationale & trade-offs.** The hardest accessibility case — one isolated person
> versus an institution — drives the design: the challenger role needs nothing but
> a key, a text file, and a hash. The honest trade-off is that a truly solo user
> cannot manufacture independence for their *own* findings; rather than fake it,
> the layer labels it transparently and leaves an open door for any verifier to
> step in later.

---

## 10. Lightweight escalation (no heavy central authority)

Escalation re-opens a terminal outcome **without** creating a court or registrar:

1. **Independent verifier invitation.** Any party may publish an `ESCALATED`
   transition that links the disputed outcome hash and states grounds. This is an
   *open invitation* for any named independent verifier to review — not a referral
   to an authority.
2. **Time-bounded re-opening.** If a `window` was set, escalation must be anchored
   before `closesAt`; otherwise the outcome is final unless new facts are
   disclosed (which themselves start a fresh challenge).
3. **Verifier review.** An independent verifier who accepts issues a new Review
   Outcome VC; `UNDER_REVIEW` resumes. Multiple independent outcomes can coexist —
   the public record shows each named human's signed conclusion, and readers judge
   the weight of competing named accountabilities.
4. **Termination.** There is no supreme adjudicator. Finality comes from the window
   closing or from no further named human being willing to put their name to a
   contrary outcome — both fully visible in Git.

> **Rationale & trade-offs.** Replacing a central appeal body with an *open
> invitation to named verifiers* keeps the layer un-capturable and consistent with
> "fork = the right to diverge." The trade-off is that escalation does not
> guarantee a single authoritative answer; instead it guarantees a transparent,
> attributable contest of named humans — which is precisely the Burgess Principle's
> notion of legitimacy.

---

## 11. Verification checklist (for any third party)

A verifier handed a dispute can independently confirm it with hashes alone:

1. Recompute `sha256(finding VC)` and compare to `challenge.challengedFinding.vcHash`.
2. Verify the challenge Ed25519 proof against the challenger DID document.
3. Confirm `challengeHash` is anchored (OpenTimestamps) and ordered correctly.
4. Recompute `sha256(challenge VC)` and compare to `outcome.challengeRef.challengeHash`.
5. Verify the outcome Ed25519 proof against the reviewer DID document.
6. Check `independence.reviewerIsChallenger == false`.
7. If `AMENDED`, confirm the superseding finding VC exists and references the original.
8. Inspect disclosed reasoning/statement (selective disclosure) for named-human
   sufficiency under the SOVEREIGN test.

No facts beyond what the parties choose to disclose ever leave their control; the
public ledgers and anchors carry only `sha256:` commitments.

---

## 12. Open questions and trade-offs

- **Reviewer pools.** Institutions may maintain an attestor registry of eligible
  reviewers; individuals may rely on ad-hoc verifiers. The layer does not mandate
  either — registries are an optional adoption profile.
- **Competing outcomes.** Allowing multiple independent outcomes maximises
  sovereignty but can produce unresolved contests. This is intentional: the
  Principle prefers a visible, named disagreement to a hidden, central verdict.
- **VC proof suite.** Ed25519 JSON-LD aligns with the stack; SD-JWT VC may ease
  some institutional verifiers and remains an optional profile.
- **DID rotation.** As elsewhere, `did:key` has no native rotation; rely on Git
  records and anchored revocation logs.
- **On-chain minimisation.** Challenge and outcome detail stay off-chain; public
  systems continue to see hashes only.

*The Burgess Principle — UK Certification Mark UK00004343685*
