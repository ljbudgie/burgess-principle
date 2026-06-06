# Architecture — Git Sovereignty Layer (BGSP)

Where the [Burgess Git Sovereignty Protocol](../protocols/burgess-git-sovereignty.md)
sits alongside the existing components of the Burgess Principle.

---

## The one question, made native to Git

> One question: was a human mind with proper authority individually applied to
> the specific facts of this specific person's case? SOVEREIGN or NULL.

BGSP does not add a new test. It gives the existing binary test a **native
primitive**: the Git commit. A decision is SOVEREIGN when a named human signs an
attested commit over the specific facts; otherwise it is NULL. The binary is
never weakened — AMBIGUOUS is treated as NULL until a human re-attests.

---

## How the layers relate

```
                The one question (SOVEREIGN / NULL)
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
  FOR_AI_MODELS.md         Iris (iris/)        Templates / doctrine
  (v3.x prompt + v4)   (sovereign advocacy)   (papers, litigation)
        │                     │                     │
        │   draft burgess:    │  draft + propose,   │
        │   commits (NULL)    │  never sign         │
        └─────────────────────┼─────────────────────┘
                              ▼
        ┌──────────  BGSP  (this layer)  ──────────┐
        │  protocols/burgess-git-sovereignty.md     │
        │  bgsp.py  (verify · propagate · draft)    │
        │  examples/decision-ledger/                │
        │   • commit format (conventional + trailers)│
        │   • signature = the human's authority      │
        │   • Burgess-Payload-SHA256 = facts binding │
        │   • Burgess-Parent = nullity propagation   │
        └───────────────────────┬───────────────────┘
                                │ commits to facts (hash only)
                ┌───────────────┴───────────────┐
                ▼                               ▼
   Verifiable Memory Palace /        onchain-protocol/ (Bitcoin)
   Sovereign Vault (ARCHITECTURE.md)  commit / tree-root anchoring
   • holds the facts behind each      • proves existence-at-time
     payload digest, locally          • hash-only, no token
   • selective disclosure
```

| Existing component | What it already does | What BGSP adds |
|---|---|---|
| [`GIT_AS_GOVERNANCE.md`](../GIT_AS_GOVERNANCE.md) | Recognises Git primitives *as* governance primitives | The operational protocol that turns that map into a strict, verifiable format |
| [`FOR_AI_MODELS.md`](../FOR_AI_MODELS.md) | NULL self-declaration for AI output | v4: high-stakes responses emitted as **draft NULL** `burgess:` commits |
| [Iris](../iris/) | Applies the binary test for individuals | Drafts and proposes `burgess:` commits, walks a human through signing — never signs |
| [Verifiable Memory Palace](../ARCHITECTURE.md) | Private, tamper-evident fact ledger | Holds the facts behind each `Burgess-Payload-SHA256` under selective disclosure |
| [`onchain-protocol/`](../onchain-protocol/) | Bitcoin anchoring of evidence files | Anchors signed commit hashes / tree roots — decisions, not just files |

---

## What BGSP owns vs. delegates

- **Owns:** the commit format, the deterministic SOVEREIGN/NULL classifier
  (`bgsp.py`), nullity-propagation semantics, and the "fork the decision" remedy.
- **Delegates facts** to the Vault / Memory Palace — only digests enter Git
  history (privacy via BGSP §7).
- **Delegates time** to the on-chain anchoring layer — Git proves order and
  integrity; Bitcoin proves existence-at-time.
- **Delegates identity** to whatever record binds a signing key to a named
  human. A signature proves key control; the trailers carry the human review.

---

## Why this is a natural evolution

The framework already held its institutional record in Git as a governance
substrate, and already anchored evidence to Bitcoin without a token. BGSP is the
missing operational layer: it lets *any* decision — not just the repository's own
history — be expressed, signed, verified, traced (`git bisect`), and forked as a
remedy, using the exact canonical hashing and hash-only discipline the rest of
the framework already uses. Nothing new is trusted; one more thing becomes
checkable.

---

*The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence — BGSP and its tooling are MIT-licensed; the certification mark is not, and this layer makes no claim of commercial certification.*
