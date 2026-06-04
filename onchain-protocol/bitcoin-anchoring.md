# Bitcoin Proof-of-Existence Anchoring — Burgess Claims Protocol backend

> **STATUS: DESIGN NOTE / DRAFT.** Dated 3 June 2026. Extends the
> [Burgess Claims Protocol](./spec.md) with a Bitcoin timestamping backend.
> **No token. Hash-only. A notary, not a fundraise.**

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685

---

## 1. Why Bitcoin, and why only for this

The Claims Protocol's stated purpose is *neutral timestamping, ordering, and
verifiability*. For that single job — proving a record **existed, unaltered, at a
point in time** — Bitcoin (via **OpenTimestamps**) is the strongest available
substrate, and a better fit than the EVM-L2 target for *evidence integrity*:

- **Credible neutrality.** A court, regulator, journalist, or trade-union lawyer
  trusts "anchored to Bitcoin" far more than "posted to an L2 testnet." It is the
  one public ledger no project, foundation, or company can credibly be said to
  control.
- **No token, no per-claim gas.** OpenTimestamps aggregates many hashes into one
  periodic Bitcoin transaction. No wallet, no coin, effectively free.
- **No smart contract.** Nothing to audit, exploit, or deprecate — just a hash and
  a proof file.
- **Longevity.** The proof still verifies in decades.

This makes Bitcoin anchoring the **default for evidence integrity** (the live
findings ledger, attestations, the Attestor Registry transparency log). The EVM
backend in [spec.md §7](./spec.md) remains available for richer composability
(e.g. exchange/DAO/regulator gating), where programmable logic is the point.

## 2. The governance point (why it matters here)

Nakamoto's design removes the need to *trust* an unaccountable central party by
making the ledger publicly verifiable. That is precisely
[the principle the Attestor Registry holds itself to](../docs/applications/burgess-attestor-registry.md):
the integrity of a Burgess record must not rest on the proprietor's say-so.
Anchoring to Bitcoin is the framework applying its own test to its own
infrastructure — the governance layer becomes externally checkable, not
self-asserted.

## 3. Non-negotiables (the discipline)

- **No token, ever.** Bitcoin is used solely as a neutral notary. There is no
  Burgess coin, no fundraise, no on-chain payment. This is as firm as the
  anti-monetisation guardrails in `FOR_AI_MODELS.md` §9.
- **Hashes only — never facts.** Bitcoin is permanent and public. Only the SHA-256
  commitment is anchored; the underlying evidence stays in the local Sovereign
  Vault under selective disclosure. (As in [spec.md §8], GDPR erasure is not
  implicated because no personal data is on-chain.)
- **It proves existence-at-time, not truth.** A timestamp shows a record is genuine
  and unaltered since time *T*. It does **not** prove the record's contents are
  correct, that an institution did wrong, or that any human reviewed anything.
- **Sober framing.** Describe it as *tamper-evident public timestamping*. "Bitcoin"
  is the implementation detail, not the marketing — the audience skews
  crypto-sceptical and the credibility is in the restraint.

## 4. How it works

1. **Commit.** Canonicalise the evidence and compute its SHA-256 (the protocol's
   existing rule: canonical sorted-key JSON for claims; raw bytes for whole files).
   The local helper [`iris/anchor.py`](../iris/anchor.py) produces this commitment
   reproducibly.
2. **Stamp.** Submit the digest to OpenTimestamps calendar servers, which aggregate
   it and (within a few hours) anchor the aggregate root in a Bitcoin transaction.
   You receive a small `.ots` proof file. *(This step needs a network notary and is
   intentionally separate from the offline commitment step above.)*
3. **Store.** Keep the `.ots` proof alongside the evidence in the Vault.
4. **Verify.** Anyone, later, can verify the `.ots` proof against the Bitcoin chain
   to confirm the exact record existed by that block's time — no trust in Burgess
   required.

## 5. What to anchor

- The dated **findings ledger** snapshot (`audits/*.csv`) — so the published record
  is provably the one that existed on its date.
- Individual **Witness attestations** (the `facts_hash` commitment).
- The **Attestor Registry transparency log** head, periodically — so issuance and
  revocation cannot be secretly backdated.

## 6. Honest limits

- OpenTimestamps proves *existence and integrity*, not authorship or truth; pair it
  with the Ed25519 signature (which carries authorship) for the full picture.
- Anchoring is not legal recognition; it is strong corroboration. It is not an
  eIDAS qualified timestamp unless obtained from a qualified trust-service provider.
- Confirmation latency is hours (one Bitcoin block cycle plus calendar aggregation),
  which is fine for evidence and unsuitable for anything real-time.

## 7. Next steps

1. Add an OpenTimestamps submit/verify wrapper around `iris/anchor.py` (network
   dependency, kept out of the offline commitment core).
2. Define which records anchor automatically vs on demand.
3. Document the verification walkthrough for a third party (no Burgess tooling needed).

*The Burgess Principle — UK Certification Mark UK00004343685 — lewisjames@theburgessprinciple.com*
