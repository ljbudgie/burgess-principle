# Example Sovereign Exit Ledger (BSEP)

Illustrative `burgess(exit):` commits for the
[Burgess Sovereign Exit Protocol](../../protocols/burgess-sovereign-exit.md).
Each `.commit` file is a full exit commit message in BSEP format. Together they
are one person's **Sovereign Exit Ledger** — a signed, verifiable record of
leaving several systems cleanly and accountably.

> These are **examples**, not real signed commits. To keep them verifiable
> without GPG infrastructure (and in tests), each file begins with a stripped
> `# signature-status:` / `# signer:` / `# commit-id:` comment header that tells
> the helper the signature context a real `git log --show-signature` would
> supply. In production the signature is real and these comment lines do not
> exist.

## The two axes (the binary test is not weakened)

Every exit is classified on **two independent axes** (spec §1.1):

- **Sovereignty** — `SOVEREIGN` / `NULL`. The same binary Burgess test as BGSP:
  signed by a named human with a valid attestation, or NULL by default.
- **Completeness** — `CLEAN` / `PENDING` / `CONTESTED`. *Given* sovereignty, is
  the break actually clean? Derived from obligations + lawful notice.

A **Clean Break** needs **both**: `SOVEREIGN` and `CLEAN`.

## The commits

| File | Type | Result | What it shows |
|---|---|---|---|
| `00-null-platform-autorenew.commit` | platform | **NULL** | The prior NULL decision: an automated auto-renewal with no human review. Recorded honestly; healed later by `04`. |
| `01-exit-utility-energy.commit` | utility | **SOVEREIGN / CLEAN** | Leaving an energy supplier on a switch; final readings submitted, balance settled. |
| `02-exit-financial-bank.commit` | financial | **SOVEREIGN / CLEAN** | Closing a savings account at nil balance; no obligation. |
| `03-exit-medical-device.commit` | medical | **SOVEREIGN / CLEAN** | The canonical OpenHear transition: exit a proprietary device platform into sovereign device parameters. |
| `04-exit-platform-heal.commit` | platform | **SOVEREIGN / CLEAN** | **Heals the prior NULL** (`Exit-Heals: 00-null-platform-autorenew`): a named human ends the auto-renewal on their own terms. |
| `05-exit-government-council.commit` | government | **SOVEREIGN / PENDING** | Council-tax move-out with statutory notice served; PENDING while the final bill completes. |
| `06-exit-financial-insurance.commit` | financial | **SOVEREIGN / PENDING** | A time-bounded exit window: notice served, 30-day notice period running. |
| `07-exit-shared-family-joint.commit` | shared | **SOVEREIGN / CLEAN** | A multi-party joint-account exit; both parties attest individually (`Exit-Cosigners`). |

`CLEAN-BREAK-CERTIFICATE.md` is an example certificate **generated from** this
ledger (see below).

## Use the ledger

```bash
# Verify one exit (sovereignty + completeness):
python tools/bgsp-exit.py check examples/sovereign-exit-ledger/01-exit-utility-energy.commit

# Verify the whole ledger (oldest-first), with nullity propagation:
python tools/bgsp-exit.py verify examples/sovereign-exit-ledger/*.commit

# Show healed vs unhealed prior NULL decisions:
python tools/bgsp-exit.py heal-report examples/sovereign-exit-ledger/*.commit

# Generate notice language for a system you are leaving:
python tools/bgsp-exit.py notice examples/sovereign-exit-ledger/05-exit-government-council.commit

# Generate a Clean Break Certificate from the ledger:
python tools/bgsp-exit.py certificate examples/sovereign-exit-ledger/*.commit
```

Expected: `00` is NULL; `01`–`04` and `07` are SOVEREIGN/CLEAN; `05` and `06` are
SOVEREIGN/PENDING (lawful processes still running); the heal-report shows `00`
healed by `04`. Because the ledger still contains PENDING exits, the certificate
is **PARTIAL** — honest, not failed. When the council final bill settles and the
insurance notice window closes, a short closing re-attestation for each moves it
to CLEAN and the certificate becomes **COMPLETE**.

## Build your own

1. Keep the **facts local** (in your Verifiable Memory Palace / Sovereign Vault).
   Only the digest, attestation, and metadata go into the commit.
2. Draft an exit with `python tools/bgsp-exit.py draft …` (NULL until you sign).
3. Give any **legally required notice** and put its reference in `Exit-Notice`.
4. Set `Burgess-Classification: SOVEREIGN`, review the specific facts, and **sign**
   the commit yourself: `git commit -S -F <msg>`.
5. When obligations complete, add a closing re-attestation to reach CLEAN.

**Lawful, accountable exits only.** Obligations are *handled* (`none`, `settled`,
`transferred:<ref>`) or honestly carried as PENDING/CONTESTED — never escaped. The
helper rejects debt-dodging language (spec §4.3).

---

*The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence*
