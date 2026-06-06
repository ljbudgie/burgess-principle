# Example decision ledger (BGSP)

Illustrative `burgess:` commits for the
[Burgess Git Sovereignty Protocol](../../protocols/burgess-git-sovereignty.md).
Each `.commit` file is a full commit message in BGSP format. They demonstrate the
binary test rendered as Git: **SOVEREIGN or NULL**.

> These are **examples**, not real signed commits. To keep them verifiable without
> GPG infrastructure (and in tests), each file begins with a stripped
> `# signature-status:` / `# signer:` / `# commit-id:` comment header that tells
> `bgsp.py` the signature context a real `git log --show-signature` would supply.
> In production the signature is real and these comment lines do not exist.

| File | Classification | What it shows |
|---|---|---|
| `01-null-automated-credit.commit` | **NULL** | An automated institutional decision with no named human and no signature. NULL by default — and recorded honestly rather than hidden. |
| `02-sovereign-openhear-fitting.commit` | **SOVEREIGN** | A medical / OpenHear device fitting individually reviewed and signed by a named, registered clinician. |
| `03-sovereign-institutional-reattestation.commit` | **SOVEREIGN** | An institutional action that **forks the NULL decision** (`Burgess-Parent: 01-null-automated-credit`), applies sovereign review, and heals the chain. |

## Verify them

```bash
# One commit:
python bgsp.py check examples/decision-ledger/02-sovereign-openhear-fitting.commit

# A decision chain, with nullity propagation (oldest-first):
python bgsp.py chain \
  examples/decision-ledger/01-null-automated-credit.commit \
  examples/decision-ledger/03-sovereign-institutional-reattestation.commit
```

Expected: `01` is NULL, `02` is SOVEREIGN, and in the chain `03` is SOVEREIGN
(it re-attests) while the chain as a whole reports NULL because it still contains
the original NULL ancestor — exactly the trace `git bisect` would give you.

## The remedy in miniature

`03` is "fork the decision" made concrete: an affected person's case was decided
by a NULL automated process (`01`); a named officer with proper authority then
individually reviewed the specific facts and signed a SOVEREIGN re-attestation.
The signed fork is independently verifiable evidence that sovereign review
happened — by whom, when, and over which facts.

---

*The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence*
