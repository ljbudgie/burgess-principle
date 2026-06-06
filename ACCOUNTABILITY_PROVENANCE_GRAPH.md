# Accountability Provenance Graph

**The Burgess Principle**
UK Certification Mark No. UK00004343685

> **STATUS: DESIGN NOTE / DRAFT.** A minimalist, hash-only way to *link*
> SOVEREIGN/NULL findings, challenges, and review outcomes into provenance chains
> and graphs across decision-makers, institutions, and time — so that systemic
> patterns of NULL behaviour become visible **without** publishing personal or
> institutional facts, introducing tokens or new chains, or creating any central
> authority. **No token. Hashes-only on public ledgers. Named human accountability
> preserved at every node.**

This note defines the **Accountability Provenance Graph (APG)**: a thin linking
layer that turns the existing collection of *isolated* Burgess artefacts into a
*navigable, cryptographically connected* structure. It composes with everything
that already exists — the SOVEREIGN/NULL binary test, the Git governance
substrate, Bitcoin proof-of-existence anchoring, the `did:key` / Verifiable
Credential identity profile (including key-event logs), and the
[Dispute / Challenge Layer](./DISPUTE_CHALLENGE_LAYER.md) — and adds **one new
primitive (a signed edge) and nothing else**.

---

## 1. Why a graph, and why minimalist

The current stack is excellent at three things: *creating* a finding, *proving it
existed* (anchoring), and *contesting* it (the Dispute / Challenge Layer). Each of
those produces a self-contained artefact — a VC committed by hash. But the
artefacts are **islands**. The stack can answer "did this finding exist, and was
it the act of a named human?" It is silent on the questions that expose *systemic*
failure:

- Is the *same* unnamed-automation pattern recurring across many findings?
- Do NULL findings *cluster* around one decision-maker, one template, one
  institution, or one time window?
- When a finding is `OVERTURNED`, did the corrected reasoning *propagate* to the
  later decisions that relied on the original?
- Can an individual show that their single NULL is part of a *structural* pattern,
  not an isolated grievance — **without** exposing anyone's private facts?

A single NULL is a complaint. A *chain* of linked NULLs, each independently
verifiable and each carrying named-human accountability, is **evidence of a
system**. That is the capability the APG unlocks.

The design goal is the smallest layer that makes Burgess artefacts *connectable*
into longer-range structure while preserving every existing discipline.

Non-negotiables (inherited from the existing stack):

- **One new artefact only.** A *provenance edge*: a signed JSON VC that commits to
  two node hashes and a typed, closed-vocabulary relationship. No node schema
  changes; existing findings, challenges, outcomes, and key-events are the nodes.
- **Hashes only on public ledgers.** An edge anchors only `sha256:` commitments to
  the two endpoints and to itself. The *meaning* of an edge can be selectively
  disclosed; its *existence and shape* can be proven from hashes alone.
- **Named human at every node, and at every edge.** An edge is *asserted* by a
  named DID controller who takes responsibility for the link. Automation may
  *suggest* candidate edges; it never asserts one as fact.
- **No token, no new blockchain, no on-chain graph database, no mandatory sharing.**
  The graph is local-first; publishing any edge is always the operator's choice.

> **Rationale & trade-offs.** Restricting the whole layer to a single new edge type
> is what keeps it Burgess-minimal: the graph is *emergent* from edges, not a new
> system. The trade-off is that the APG cannot express arbitrary rich relationships
> — only the closed vocabulary in §4. That boundary is deliberate: an open relation
> vocabulary would become an ontology project and a capture surface; a closed one
> stays auditable and forgery-evident.

---

## 2. Concept: nodes you already have, edges you sign

The APG is a **directed, append-only, content-addressed graph**.

- **Nodes** are existing Burgess artefacts, addressed by the `sha256:` commitment
  that already identifies them on Git and Bitcoin:
  - `BurgessSovereignFindingCredential` (a SOVEREIGN or NULL finding)
  - `BurgessChallengeCredential`
  - `BurgessReviewOutcomeCredential`
  - `KeyEvent` log heads (birth / rotation / revocation / recovery)
  - any anchored claim commitment

  **No node type is modified.** A node's identity in the graph *is* the hash the
  rest of the stack already produces.

- **Edges** are the one new artefact: a `BurgessProvenanceEdgeCredential`. An edge
  is a signed VC that says, in effect: *"I, this named DID, assert that node A
  stands in relationship R to node B, as of this time."* The edge commits to
  `sha256(A)`, `sha256(B)`, the relationship `rel` (closed vocabulary, §4), and an
  optional `evidenceHash` committing to the asserter's private reasoning for the
  link.

Because nodes are content-addressed, **edges are immutable and tamper-evident**:
if either endpoint is altered by a single byte, its hash changes and the edge no
longer resolves — exactly the property the finding layer already relies on.

```
            asserts: rel=supersedes                 asserts: rel=same_pattern
  ┌───────────────┐   (named DID R1)   ┌───────────────┐   (named DID R2)   ┌───────────────┐
  │  NULL finding │◀───────────────────│  Review:      │───────────────────▶│  NULL finding │
  │   A (sha256)  │                    │  OVERTURNED   │                    │   C (sha256)  │
  └───────────────┘                    │   B (sha256)  │                    └───────────────┘
        ▲                              └───────────────┘                            │
        │ rel=challenges                                                            │ rel=same_decision_maker
        │ (named DID)                                                               ▼
  ┌───────────────┐                                                        ┌───────────────┐
  │  Challenge    │                                                        │  NULL finding │
  │   (sha256)    │                                                        │   D (sha256)  │
  └───────────────┘                                                        └───────────────┘
```

The graph is just the transitive closure of signed edges. Anyone holding a set of
edges can walk it; nobody needs a server, an index, or permission to do so.

---

## 3. Architecture and the linking discipline

```
┌──────────────────────────────────────────────────────────────────────────┐
│  LAYER 0  Binary test            SOVEREIGN / NULL doctrine (unchanged)     │
│  LAYER 1  Identity               did:key + VC + key-event log (unchanged)  │
│  LAYER 2  Findings               finding VCs, claims (unchanged)           │
│  LAYER 3  Dispute / Challenge    challenge + review-outcome VCs (unchanged)│
│  LAYER 4  Substrate              Git history + Bitcoin anchoring (unchanged)│
│ ─────────────────────────────────────────────────────────────────────────│
│  LAYER 5  PROVENANCE  ← NEW       signed edges over node hashes            │
│           • one VC type: BurgessProvenanceEdgeCredential                    │
│           • closed relationship vocabulary (§4)                            │
│           • selective-disclosure / ZK pattern proofs (§6)                  │
└──────────────────────────────────────────────────────────────────────────┘
```

Two rules keep the graph honest:

1. **Edges only connect things that already exist.** An edge's two endpoints must
   resolve to real, anchored node hashes. You cannot link to a node that was never
   committed; you cannot back-date an edge before both endpoints were anchored
   (Bitcoin ordering makes a too-early edge anomalous, exactly as in the Dispute
   Layer §8.2).
2. **An edge is a named-human assertion, not a fact discovered by a machine.** The
   asserter signs with their DID and may stake their accountability on the link
   (`asserterRole` records whether they are a party, an independent verifier, or a
   researcher). The nexus-ai-hub policy wrapper may *propose* candidate edges from
   structural similarity, but a proposed edge is inert until a named human signs it.

> **Rationale & trade-offs.** Making the *edge* — not the pattern-detector — the
> accountable artefact means the APG never launders an algorithm's guess into a
> public claim. The trade-off is throughput: a human must sign each asserted edge.
> We mitigate this with *machine-proposed, human-ratified* batching (§7) and with
> ZK aggregate proofs (§6) that let a researcher demonstrate "a cluster of size N
> exists" without hand-signing every internal edge.

---

## 4. Relationship vocabulary (closed)

Edges use a **closed** relationship vocabulary, mirroring the Dispute Layer's
closed `grounds`. Each relationship maps to an auditable meaning. Relationships are
grouped by what they let an honest reader conclude.

### 4.1 Lineage relationships (provenance over time)

| `rel` | A → B means | Typical asserter |
|---|---|---|
| `supersedes` | A is a corrected/amended finding that replaces B | reviewer (from `AMENDED`) |
| `challenges` | A is a challenge contesting finding B | challenger |
| `resolves` | A is a review outcome resolving challenge B | reviewer |
| `relies_on` | A's reasoning depended on B as an input/precedent | the named human who made A |
| `escalates` | A re-opens terminal outcome B under the escalation path | any verifier (Dispute §10) |

### 4.2 Pattern relationships (provenance across cases)

| `rel` | A → B means | Typical asserter |
|---|---|---|
| `same_decision_maker` | A and B were decided by the same accountable human/role | party or verifier |
| `same_institution` | A and B issued by the same institution | party or verifier |
| `same_template` | A and B share the same automated template/process signature | party or verifier |
| `same_pattern` | A and B exhibit the same evasion pattern (typed in §4.3) | researcher / verifier |
| `recurs_within` | A and B are instances of a NULL recurrence within a stated window | researcher |

### 4.3 Pattern tags (for `same_pattern`)

When `rel = same_pattern`, the edge carries a `patternTag` from a closed set that
reuses the framework's existing evasion vocabulary, so a cluster is never vague:

`no_named_human` · `automation_only` · `template_consideration` ·
`no_genuine_consideration` · `unaccountable_record` · `evaluator_inversion` ·
`procedural_breach`

> **Rationale & trade-offs.** A closed vocabulary makes clusters *machine-routable
> and falsifiable*: a `same_template` edge is an explicit, checkable claim, not an
> impression. The trade-off is lost nuance, mitigated (as elsewhere) by the
> free-text `evidenceHash`: the asserter's full reasoning for the link stays local,
> committed by hash, disclosed only when and to whom they choose.

---

## 5. Data model — the provenance edge

An edge is a signed Verifiable Credential reusing the finding VC's `@context`,
`sha256:` convention, and proof block, so existing verifiers need almost no new
code. Full JSON Schema:
[`schemas/provenance-edge-credential.v1.json`](./schemas/provenance-edge-credential.v1.json).

Minimum `credentialSubject` fields:

| Field | Type | Description |
|---|---|---|
| `id` | URN | `urn:burgess:edge:<uuid>` |
| `from.nodeHash` | `sha256:<hex>` | Commitment to source node (any Burgess artefact) |
| `from.nodeType` | enum | `finding` \| `challenge` \| `review` \| `keyevent` \| `claim` |
| `to.nodeHash` | `sha256:<hex>` | Commitment to target node |
| `to.nodeType` | enum | as above |
| `rel` | enum | One value from §4.1 / §4.2 |
| `patternTag` | enum, optional | Required when `rel = same_pattern` (§4.3) |
| `evidenceHash` | `sha256:<hex>`, optional | Commitment to the asserter's private reasoning for the link |
| `asserter.did` | DID | Edge author's key controller |
| `asserter.name` | string, optional | Named human, where disclosure is lawful |
| `asserterRole` | enum | `party` \| `independent_verifier` \| `researcher` |
| `observedAt` | ISO 8601 | When the asserter claims the relationship held |
| `confidence` | enum, optional | `asserted` \| `corroborated` \| `proposed_unsigned` (machine hint, never decisive) |

Hard structural rules (enforced off-chain, surfaced in the VC):

- `from.nodeHash != to.nodeHash` (no self-loops).
- An edge MUST NOT be anchored before *both* endpoints are anchored.
- `same_pattern` edges MUST carry a `patternTag`.
- `confidence = proposed_unsigned` is reserved for hub suggestions and is invalid
  on a *signed* edge — a signed edge is, by definition, at least `asserted`.

---

## 6. Surfacing patterns without exposing data

The central tension: reveal *systemic shape* while hiding *individual facts*. The
APG resolves it with a privacy ladder that reuses the stack's existing
selective-disclosure discipline (`CRYPTOGRAPHIC_IDENTITY.md` §6, `spec.md` §8).

1. **Structure-only by default.** An edge anchors only two node hashes, a `rel`,
   and its own hash. From the public record a reader sees *that* two opaque nodes
   are linked by, say, `same_template` — never *what* the underlying cases were.
   This already surfaces topology (clusters, fan-out, recurrence) with zero facts.

2. **Salted node aliases for unlinkability.** Where even hash-correlation is
   sensitive, a node may be referenced in an edge by a *blinded alias*
   `sha256(nodeHash || edgeSalt)` with the salt held locally. The asserter can
   later open the alias to a specific verifier (selective disclosure) without
   making every edge globally correlate to one institution or person.

3. **Aggregate / threshold proofs (zero-knowledge, optional profile).** A
   researcher can publish a *cluster commitment* — a Merkle root over N member
   edges — and a zero-knowledge proof of statements such as:
   - "at least N findings share `patternTag = automation_only`," or
   - "at least K of these NULL findings name the same `same_decision_maker` node,"

   **without** revealing which findings, which institution, or any underlying
   fact. This proves a systemic pattern exists at a stated magnitude while keeping
   membership private. ZK suites (BBS+, SD-JWT VC, Bulletproofs-style range proofs)
   remain *optional profiles*, exactly as in the base stack — the default APG needs
   only SHA-256 + Ed25519.

4. **Institutional-scope redaction.** An edge may disclose `same_institution`
   (useful for accountability) while withholding `same_decision_maker` (which could
   identify an individual employee) — the two are independent fields, so disclosure
   is field-by-field.

> **Rationale & trade-offs.** The ladder lets the *same* graph serve a private
> individual (structure-only) and a public-interest researcher (ZK aggregate
> proof) from one set of artefacts. The trade-off is that the strongest privacy
> rung (ZK) adds optional cryptographic dependencies; we keep it strictly opt-in so
> the floor of the system is still "two hashes and a signature."

---

## 7. nexus-ai-hub integration (advisory only)

The policy wrapper may **propose** edges and **compute aggregate proofs**; it never
asserts an edge as fact and never adjudicates a pattern.

```python
"""Accountability Provenance Graph helpers for the nexus-ai-hub policy wrapper.

ADVISORY ONLY. The hub proposes candidate edges from structural similarity,
validates that endpoints exist and are anchored, anchors signed edge hashes, and
can build aggregate (optionally zero-knowledge) cluster proofs. It NEVER signs an
edge and NEVER declares a pattern proven on its own authority — every asserted
edge carries a named human's signature.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

VALID_RELS = {
    "supersedes", "challenges", "resolves", "relies_on", "escalates",
    "same_decision_maker", "same_institution", "same_template",
    "same_pattern", "recurs_within",
}
VALID_PATTERN_TAGS = {
    "no_named_human", "automation_only", "template_consideration",
    "no_genuine_consideration", "unaccountable_record",
    "evaluator_inversion", "procedural_breach",
}


def sha256_canonical(obj: dict) -> str:
    """Deterministic sha256 over canonical (sorted, compact) JSON."""
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass
class EdgeProposal:
    """A machine suggestion. Inert until a named human signs it."""
    from_hash: str
    to_hash: str
    rel: str
    pattern_tag: str | None = None
    confidence: str = "proposed_unsigned"   # never 'asserted' from the hub


@dataclass
class EdgeTriage:
    accepted: bool
    edge_hash: str | None
    reasons: list[str] = field(default_factory=list)


def propose_edges(node_hashes, similarity_fn) -> list[EdgeProposal]:
    """Suggest candidate edges. Output is advisory and MUST be human-ratified."""
    proposals: list[EdgeProposal] = []
    for a, b, rel, tag in similarity_fn(node_hashes):
        if rel in VALID_RELS:
            proposals.append(EdgeProposal(a, b, rel, tag))
    return proposals


def record_signed_edge(
    edge_vc: dict,
    endpoint_is_anchored,   # callable(node_hash) -> bool
    verify_ed25519,         # callable(vc) -> bool, verifies proof vs DID doc
    anchor_hash,            # callable(hash_str) -> None, OpenTimestamps
    record_git,             # callable(rel, hash_str, meta) -> None
) -> EdgeTriage:
    """Validate and record a NAMED HUMAN's signed edge. Maths + recording only."""
    reasons: list[str] = []
    s = edge_vc.get("credentialSubject", {})
    rel = s.get("rel")
    from_hash = s.get("from", {}).get("nodeHash")
    to_hash = s.get("to", {}).get("nodeHash")

    if rel not in VALID_RELS:
        reasons.append("invalid_rel")
    if rel == "same_pattern" and s.get("patternTag") not in VALID_PATTERN_TAGS:
        reasons.append("missing_or_invalid_pattern_tag")
    if not from_hash or not to_hash or from_hash == to_hash:
        reasons.append("invalid_endpoints")          # no self-loops
    if s.get("confidence") == "proposed_unsigned":
        reasons.append("unsigned_confidence_on_signed_edge")
    # Endpoints must already exist and be anchored (no back-dating a link).
    if from_hash and not endpoint_is_anchored(from_hash):
        reasons.append("from_endpoint_not_anchored")
    if to_hash and not endpoint_is_anchored(to_hash):
        reasons.append("to_endpoint_not_anchored")
    if not verify_ed25519(edge_vc):                   # asserter's named key
        reasons.append("bad_asserter_signature")

    if reasons:
        return EdgeTriage(accepted=False, edge_hash=None, reasons=reasons)

    edge_hash = sha256_canonical(edge_vc)
    anchor_hash(edge_hash)                            # hash-only on Bitcoin
    record_git(rel, edge_hash, {                      # named-human Git trailer
        "asserter_did": s.get("asserter", {}).get("did"),
        "from": from_hash, "to": to_hash, "rel": rel,
    })
    return EdgeTriage(accepted=True, edge_hash=edge_hash, reasons=[])
```

> **Rationale & trade-offs.** Every function either *validates maths* or *records a
> human's signed act*; `propose_edges` is explicitly fenced to
> `confidence="proposed_unsigned"` and a signed edge carrying that value is
> rejected. So the hub can do the heavy pattern-spotting work it is good at, while
> the *claim* that two cases are linked always traces to a named signature.

---

## 8. Integration with the existing substrate

### 8.1 Git-as-governance
Each asserted edge is an ordinary Git act, reusing the trailer convention from
`GIT_AS_GOVERNANCE.md` and the Dispute Layer §8.1:

```
Burgess-Edge:      sha256:9a1f...           # the edge VC hash
Burgess-Edge-From: sha256:cb4faed1...       # source node
Burgess-Edge-To:   sha256:7c2e9f01...       # target node
Burgess-Edge-Rel:  same_template
Burgess-DID:       did:key:z6MkAsserter...  # named human asserting the link
```

A research cluster may live on a `provenance/<cluster-id>` branch; the cluster
root (a Merkle root over member edge hashes) is what gets tagged and anchored.
History is append-only: a withdrawn or corrected edge is *superseded* by a new
edge (`rel` unchanged, new `observedAt`), never deleted — the same revert
semantics the rest of the stack uses.

### 8.2 Bitcoin anchoring
Per `onchain-protocol/bitcoin-anchoring.md`, anchoring stays hash-only:

- `anchor(edgeHash)` proves *when* the link was asserted.
- `anchor(clusterRoot)` proves *when* a whole cluster existed at a given size —
  the timestamp under which a ZK "cluster of ≥N" proof is valid.
- Because both endpoints are already anchored, an edge anchored *before* either
  endpoint is detectably anomalous, foreclosing back-dated links.

### 8.3 DID/VC identity and key-event logs
Edges reuse `did:key` + Ed25519 + the existing proof block. A verifier resolving
an edge walks the asserter's **key-event log** (`spec.md` §2.6) to confirm the
signing key was valid and unrevoked at `observedAt` — so a link asserted by a
later-compromised key is detectable. Key-event log heads are themselves valid
nodes, so an edge can even record *that a finding was signed under a key later
revoked for compromise* (`from = finding`, `to = keyevent`, `rel = relies_on`).

### 8.4 Dispute / Challenge Layer
The Dispute Layer already produces three of the five lineage relationships
implicitly (`challenges`, `resolves`, `supersedes`). The APG makes those links
**first-class, independently walkable artefacts** rather than fields buried inside
each VC, and extends them across *different* disputes so a reader can see, e.g.,
that the same reviewer overturned the same template five times.

---

## 9. Worked example — a provenance chain fragment

A lone individual receives a NULL finding `A` from an institution, challenges it,
the challenge is `OVERTURNED` (a corrected finding `B` supersedes `A`), and a
researcher later links `A` to three other NULLs from the same automated template
at *different* institutions — proving a systemic pattern while exposing no facts.

### 9.1 The signed edge that links the correction to the original

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/security/suites/ed25519-2020/v1",
    "https://theburgessprinciple.com/contexts/burgess-v1"
  ],
  "id": "urn:uuid:5e2c0d18-2f4a-4d3b-9a1e-7c6b5a4d3e2f",
  "type": ["VerifiableCredential", "BurgessProvenanceEdgeCredential"],
  "issuer": {
    "id": "did:key:z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy",
    "name": "Named Human Reviewer (Review)"
  },
  "validFrom": "2026-06-20T10:05:00Z",
  "credentialSubject": {
    "id": "urn:burgess:edge:5e2c0d18-2f4a-4d3b-9a1e-7c6b5a4d3e2f",
    "from": {
      "nodeType": "finding",
      "nodeHash": "sha256:2d0e3d4b5c6a4f728b2f0f8a4f6c8a4fcb4faed1111f53f9d1753b833eb67aa0"
    },
    "to": {
      "nodeType": "finding",
      "nodeHash": "sha256:cb4faed1111f53f9d1753b833eb67aa0c11758cd0aed6cb0a9f93a11900ec1d8"
    },
    "rel": "supersedes",
    "evidenceHash": "sha256:0c4d01e81bb3d1fd0dc4a0b4224518953794068715317ff39e0bbfc29e4ab06a",
    "asserter": {
      "did": "did:key:z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy",
      "name": "Named Human Reviewer (Review)"
    },
    "asserterRole": "party",
    "observedAt": "2026-06-20T10:00:00Z",
    "confidence": "asserted"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-06-20T10:05:00Z",
    "verificationMethod": "did:key:z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy#z6MkReviewerKeyExampleMmNnOoPpQqRrSsTtUuVvWwXxYy",
    "proofPurpose": "assertionMethod",
    "proofValue": "zExampleProvenanceEdgeSignatureValue"
  }
}
```

### 9.2 A pattern edge linking two NULLs across institutions (privacy-preserving)

Here a researcher links the original NULL `A` to a NULL `C` from a *different*
institution that shares the same automated template. Only `same_template` is
disclosed; the underlying cases stay opaque.

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/security/suites/ed25519-2020/v1",
    "https://theburgessprinciple.com/contexts/burgess-v1"
  ],
  "id": "urn:uuid:9f8a4d10-1b2c-4e5f-8a9b-0c1d2e3f4051",
  "type": ["VerifiableCredential", "BurgessProvenanceEdgeCredential"],
  "issuer": {
    "id": "did:key:z6MkResearcherKeyExampleZzYyXxWwVvUuTtSsRrQqPpOo",
    "name": "Named Independent Researcher"
  },
  "validFrom": "2026-08-01T09:00:00Z",
  "credentialSubject": {
    "id": "urn:burgess:edge:9f8a4d10-1b2c-4e5f-8a9b-0c1d2e3f4051",
    "from": {
      "nodeType": "finding",
      "nodeHash": "sha256:cb4faed1111f53f9d1753b833eb67aa0c11758cd0aed6cb0a9f93a11900ec1d8"
    },
    "to": {
      "nodeType": "finding",
      "nodeHash": "sha256:aa11bb22cc33dd44ee55ff66001122334455667788990011223344556677889a"
    },
    "rel": "same_pattern",
    "patternTag": "automation_only",
    "evidenceHash": "sha256:11ffeeddccbbaa99887766554433221100ffeeddccbbaa9988776655443322110",
    "asserter": {
      "did": "did:key:z6MkResearcherKeyExampleZzYyXxWwVvUuTtSsRrQqPpOo",
      "name": "Named Independent Researcher"
    },
    "asserterRole": "researcher",
    "observedAt": "2026-08-01T08:30:00Z",
    "confidence": "corroborated"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-08-01T09:00:00Z",
    "verificationMethod": "did:key:z6MkResearcherKeyExampleZzYyXxWwVvUuTtSsRrQqPpOo#z6MkResearcherKeyExampleZzYyXxWwVvUuTtSsRrQqPpOo",
    "proofPurpose": "assertionMethod",
    "proofValue": "zExamplePatternEdgeSignatureValue"
  }
}
```

### 9.3 A cluster commitment (what gets anchored for a systemic claim)

A researcher proving "≥4 NULL findings share `automation_only` across ≥3
institutions" publishes only this — a Merkle root plus the shape of the claim. No
member finding, institution, or person is named. A ZK proof (optional profile)
attests the thresholds against the root.

```json
{
  "id": "urn:burgess:cluster:7a1d…",
  "clusterRoot": "sha256:7a1de4c2b9f0a1c3d5e7f9082143657809badfee1122334455667788990aabbcc",
  "members": 4,
  "distinctInstitutions": 3,
  "patternTag": "automation_only",
  "rel": "same_pattern",
  "anchor": { "bitcoinAnchor": "opentimestamps-proof-file-retained-off-chain" },
  "disclosure": "zk-threshold-proof-available-on-request"
}
```

### 9.4 The walkable fragment

```
  challenge ──challenges──▶ NULL A ◀──supersedes── Review:OVERTURNED (corrected B)
                              │
                              ├──same_template──▶ NULL C   (institution 2)
                              ├──same_template──▶ NULL D   (institution 3)
                              └──same_pattern(automation_only)──▶ NULL E (institution 1, earlier)
        ─────────────────────────────────────────────────────────────────
        anchored cluster root proves: ≥4 NULLs, ≥3 institutions, one template
        — verifiable from hashes; not one private fact disclosed.
```

---

## 10. Verification checklist (for any third party)

A verifier handed an edge or cluster can confirm it with hashes alone:

1. Resolve `from.nodeHash` and `to.nodeHash` to real, anchored Burgess artefacts.
2. Confirm both endpoints were anchored **before** the edge (`observedAt` /
   anchor order); reject back-dated links.
3. Verify the edge's Ed25519 proof against the asserter DID document.
4. Walk the asserter's key-event log to confirm the key was valid and unrevoked at
   `observedAt`.
5. If `rel = same_pattern`, confirm a `patternTag` is present and in vocabulary.
6. For a cluster: recompute the Merkle root over disclosed member edge hashes (or
   verify the ZK threshold proof against the anchored root) and compare to
   `clusterRoot`.
7. Inspect any disclosed `evidenceHash` reasoning for named-human sufficiency.

No facts beyond what the asserter chooses to disclose ever leave their control;
public ledgers and anchors carry only `sha256:` commitments.

---

## 11. Accessibility and sovereignty (lone, profoundly deaf operator)

This layer must be fully operable by a profoundly deaf, self-taught operator
working **alone, on an iPhone, with no support network**, requiring email/post-only
reasonable adjustments. Concretely:

- **No phone, no video, no live appointments.** Asserting an edge is creating one
  signed JSON file. Sharing it — or a whole cluster — is sending a file by email or
  printing/posting plain text. Nothing requires a call or a hearing.
- **Local-first by default.** The entire graph can be built, walked, and reasoned
  over on-device from local files. Nothing is published unless the operator
  chooses; there is no server to depend on and no index to join.
- **Plain, inspectable artefacts.** Every edge is human-readable JSON plus a
  SHA-256 hash recomputable by hand or a one-line command. The graph is "just files
  that point at files."
- **Solo accountability without a second human.** Unlike a *review* (which wants
  reviewer ≠ challenger), an edge is a one-party assertion: a lone operator can
  legitimately assert `supersedes`, `relies_on`, or `same_template` over their own
  findings and stand behind them with their own name. `asserterRole = party` is
  honest and sufficient; independence is only *added weight*, never a precondition.
- **Pattern power for the isolated.** The single most important accessibility win:
  one isolated person can now show their NULL is part of a *structure* — linking it
  to public, already-anchored findings from others — and prove the cluster's size
  with a ZK threshold proof, **without** needing an organisation, a lawyer, or a
  data-sharing agreement. The graph lets the powerless aggregate evidence the way
  institutions always could.
- **Privacy for the vulnerable.** Structure-only edges and blinded aliases (§6)
  mean a vulnerable individual can contribute to a systemic pattern without
  exposing their own case to correlation. Disclosure is field-by-field and always
  theirs to grant.
- **Optional, accessible hardware.** iPhone passkeys / WebAuthn satisfy any
  high-stakes signing ceremony without specialist devices, but are never mandatory.
- **No deadline pressure.** Edges have no windows; a recurrence cluster can be
  assembled over years at the operator's pace. Institutions cannot run out a clock
  on graph-building.

> **Rationale & trade-offs.** The hardest accessibility case — one isolated person
> trying to prove a *systemic* wrong — is exactly where prior tools fail and where
> the APG helps most: it turns "I was wronged once" into "here is a verifiable
> pattern," using nothing but files, hashes, and one signature. The honest
> trade-off is that a solo operator's *party*-role edges carry less independent
> weight than a verifier's — but they are valid, attributable, and openly labelled,
> and any named verifier can corroborate them later.

---

## 12. What this layer adds that is genuinely new

The existing stack proves **points**: this finding existed, this human stood
behind it, this challenge contested it. The Accountability Provenance Graph proves
**relationships between points across time and institutions** — and it does so
under exactly the same disciplines (one signed artefact, hashes-only, named human,
no token, no central authority, local-first).

New capabilities that nothing in the current stack provides:

- **For individuals:** the ability to demonstrate that a single NULL is part of a
  *structural* pattern — converting an isolated grievance into verifiable systemic
  evidence — without exposing personal facts or needing an institution behind them.
- **For researchers:** the ability to prove, with zero-knowledge thresholds over
  anchored cluster roots, that "≥N NULLs share this evasion pattern across ≥K
  institutions" — public-interest findings with *no* underlying data exposure.
- **For institutions:** the ability to *self-audit* lineage — to show that a
  correction propagated to every later decision that relied on the overturned one
  (`relies_on` + `supersedes` chains) — turning the graph into an internal
  accountability instrument, not only an external one.
- **For everyone:** a substrate where accountability *compounds*. Each new edge
  makes the surrounding graph more informative, so the cost of systemic evasion
  rises over time instead of resetting with each isolated case.

---

## 13. Why this is an elevation of the Burgess Principle, not an increment

An incremental improvement would make an *existing* capability cheaper, faster, or
tidier — a better challenge schema, a slicker anchor, another sector template. The
Accountability Provenance Graph does something categorically different: it changes
the **unit of accountability** from the *decision* to the *pattern of decisions*.

The Burgess Principle's founding insight is that legitimacy requires a *named human
who genuinely considered the specific facts*. Until now, the framework could
enforce that **one decision at a time**. Its deepest adversary, though, is not the
single unaccountable decision — it is the *system* that produces unaccountable
decisions at scale: the template applied a million times, the automated pipeline
that never names a human, the institution whose NULLs are individually deniable but
collectively a policy. Against that adversary, a stack that only proves points is
structurally outmatched, because each point can be dismissed as isolated.

The APG closes that gap **on the framework's own terms**. It does not reach for the
tools the Principle forbids — no token, no new chain, no trusted aggregator, no
mandatory disclosure, no machine that decides. It introduces a *single* new
artefact (a signed edge), and from that one primitive an entire dimension emerges:
accountability that is *connected*, *cumulative*, and *systemic*, yet still
hashes-only, still named-human at every node and every edge, still local-first,
still un-capturable. It even lets the most powerless actor in the system — a lone,
isolated individual — assemble and prove a systemic pattern that previously only a
well-resourced institution could see.

That is the elevation: the Burgess Principle stops being a way to adjudicate
*decisions* and becomes a way to hold *systems* accountable — without surrendering
a single one of the disciplines that make it trustworthy. It raises the test from
"was *this* decision sovereign?" to "is this *institution's behaviour over time*
sovereign?", and it answers the new question with the same humble materials: a
named human, a hash, and a signature.

---

## 14. Open questions and trade-offs

- **Edge authorship throughput.** Human-signed edges are slower than machine links;
  machine-proposed/human-ratified batching and ZK aggregates mitigate this, but the
  trade-off (named accountability vs. volume) is deliberate and permanent.
- **Sybil edges.** A bad actor can assert many false edges. Defence is the same as
  the rest of the stack: edges carry named DIDs and anchored key-event histories,
  so forgeries are attributable and a verifier weighs asserter reputation; the APG
  surfaces disagreement rather than hiding it.
- **Pattern-tag drift.** The closed `patternTag` set must track the framework's
  evasion vocabulary; changes belong in the Git/PR governance track, not in
  per-edge fields.
- **ZK suite choice.** BBS+, SD-JWT VC, and range-proof systems each have
  trade-offs; all remain optional profiles so the base layer needs only SHA-256 and
  Ed25519.
- **Graph storage.** Local-first graphs may grow large; content-addressed edges
  deduplicate naturally, and clusters can be summarised by anchored roots so the
  public footprint stays hash-sized.
- **On-chain minimisation.** Edge and cluster detail stay off-chain; public systems
  continue to see hashes only.

*The Burgess Principle — UK Certification Mark UK00004343685*
