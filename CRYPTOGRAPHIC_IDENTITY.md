# Cryptographic Identity for Named Human Accountability

**The Burgess Principle**  
UK Certification Mark No. UK00004343685

This note integrates modern cryptographic identity standards into the Burgess
Principle without changing its core discipline: named, attributable human
accountability; hashes only on public ledgers; no token; no unnecessary central
dependency.

---

## 1. Chosen profile

The recommended minimum profile is:

- **DIDs:** `did:key` with Ed25519 keys for portable, self-contained identifiers.
- **Signatures:** Ed25519 for claim, attestation, and VC signing where the existing
  toolchain already uses Ed25519.
- **Credentials:** W3C Verifiable Credentials for portable SOVEREIGN/NULL findings
  and attestations.
- **Anchoring:** SHA-256 commitments to DID documents, VC payloads, findings
  ledgers, and transparency logs, timestamped through the existing Bitcoin
  OpenTimestamps path.
- **High-stakes keys:** WebAuthn/FIDO2 hardware-backed keys as an additional
  ceremony requirement for decisions where personal risk, liberty, housing,
  livelihood, legal status, or core rights are at stake.

Rationale: `did:key` requires no registry, account, blockchain, issuer, or hosted
identity provider. It gives a human reviewer a stable cryptographic controller
identifier that can be included in Git records, on-chain commitment preimages,
VCs, and local evidence bundles. Ed25519 aligns with the current protocol and
keeps implementation small.

This does **not** mean a DID alone proves humanity. A DID proves control of a key.
The Burgess test still requires the attributable record that ties that key to a
named human and to genuine individual consideration.

---

## 2. Identity roles

| Role | Identifier | Purpose |
|---|---|---|
| Claimant | `did:key` or local Ed25519 public key | Person raising a claim or demanding human review |
| Reviewer / attestor | `did:key` controlled by a named human | Person applying the SOVEREIGN/NULL test |
| Institution | DID, DNS name, LEI, Companies House number, or plain name | Target or issuer where an institution controls the finding |
| Credential issuer | DID of the named human or accountable institution | Signs the VC |
| Credential subject | Person, decision, institution, claim, or evidence bundle | What the finding is about |

For the minimalist profile, a DID is placed in off-chain records and canonical
commitment preimages. Public chains receive only hashes and signatures.

---

## 3. Integration points

### 3.1 Git-as-governance

Git remains the governance roll. A DID strengthens the existing named-human
record by giving the human reviewer a portable key identifier that can appear in:

- commit trailers, for example `Burgess-DID: did:key:...`;
- signed tag annotations;
- pull request approval comments;
- release notes that reference a VC hash;
- attestor registry entries and revocation logs.

Recommended commit/tag pattern:

1. Continue using GitHub-supported GPG or SSH signing for repository-native
   verification.
2. Add a DID trailer for Burgess identity continuity.
3. For releases or formal findings, sign a VC with the DID-controlled Ed25519 key.
4. Put only the VC hash or transparency-log entry in the Git tag/release notes.

This is a hybrid model: GitHub verifies the commit signature; Burgess tooling
verifies the DID/VC evidence bundle. Neither layer replaces named accountability.

### 3.2 Bitcoin anchoring

Bitcoin anchoring remains proof-of-existence, not proof of truth. DID/VC
integration changes only what is hashed before anchoring:

- DID document hash for a published reviewer key state;
- VC hash for a SOVEREIGN/NULL finding;
- transparency log head for issued/revoked credentials;
- findings ledger snapshot hash.

The anchored digest should be formatted as `sha256:<hex>`. No DID document, VC
subject data, evidence fact, or personal information is put on-chain.

### 3.3 On-chain claims protocol

The existing EVM path can keep the same contract shape. DID and VC support can be
added in the off-chain canonical JSON preimage and receipt bundle:

- `issuer_did` identifies the claim or finding issuer;
- `subject_did` identifies the claimant or credential subject where appropriate;
- `verification_method` identifies the DID key used for Ed25519 verification;
- `vc_hash` links a portable credential without publishing it;
- `proof_purpose` records whether the key was used for authentication,
  assertion, capability invocation, or another defined purpose.

The chain still stores the compact fingerprint. Full identity material stays in
the local vault or disclosed evidence bundle.

### 3.4 Provenance edges (Accountability Provenance Graph)

The same `did:key` + Ed25519 + VC profile signs **provenance edges** — the single
new artefact that links findings, challenges, review outcomes, and key-events into
the [Accountability Provenance Graph](./ACCOUNTABILITY_PROVENANCE_GRAPH.md). An edge
is a named-human assertion that two artefacts (each addressed by its `sha256:`
commitment) stand in a closed-vocabulary relationship, signed with the asserter's
DID key and validated by
[`schemas/provenance-edge-credential.v1.json`](./schemas/provenance-edge-credential.v1.json).

The identity discipline carries straight over: an edge is SOVEREIGN-grade only
where the asserter is a named human accountable for the link, the signing key
resolves through their anchored key-event log (§10.4) as valid and unrevoked at the
edge's `observedAt`, and any disclosed `evidenceHash` reasoning shows genuine
individual consideration. Automation may *propose* edges
(`confidence = proposed_unsigned`); it never signs one. Selective disclosure and
zero-knowledge threshold proofs (§6) let a pattern be proven across institutions
without exposing the underlying findings.

---

## 4. Minimal DID document example

This example uses a `did:key` Ed25519 controller. The multibase value is the
public key identifier; implementations should generate a fresh key locally.

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "id": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
  "verificationMethod": [
    {
      "id": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3#z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
      "publicKeyMultibase": "z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3"
    }
  ],
  "authentication": [
    "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3#z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3"
  ],
  "assertionMethod": [
    "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3#z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3"
  ]
}
```

Rationale: this is enough to verify Ed25519 signatures without depending on an
identity provider. The attribution layer must still record the real named human,
for example through a signed Git commit, attestor registry entry, or disclosed
review bundle.

---

## 5. Example Verifiable Credential

This JSON-LD VC wraps a SOVEREIGN finding. The full evidence remains local; public
systems may receive only the VC hash.

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/security/suites/ed25519-2020/v1",
    "https://theburgessprinciple.com/contexts/burgess-v1"
  ],
  "id": "urn:uuid:0f8a4f6c-8a4f-4a72-8b2f-2d0e3d4b5c6a",
  "type": [
    "VerifiableCredential",
    "BurgessSovereignFindingCredential"
  ],
  "issuer": {
    "id": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
    "name": "Named Human Reviewer"
  },
  "validFrom": "2026-06-06T21:35:00Z",
  "credentialSubject": {
    "id": "urn:burgess:claim:sha256:7f4f8c0b6d2b5f4f5e9c5d0f6e8a9b0c1d2e3f405162738495a6b7c8d9e0f123",
    "targetEntity": "Example Institution",
    "finding": "SOVEREIGN",
    "testVersion": "SOVEREIGN/NULL",
    "namedHuman": {
      "name": "Named Human Reviewer",
      "did": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
      "verificationMethod": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3#z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3"
    },
    "fullFactsBasisHash": "sha256:3b7e1a8f4b5c6d7e8f90123456789abcdef0123456789abcdef0123456789abcd",
    "individualConsiderationRecordHash": "sha256:6f2d1c0b9a887766554433221100ffeeddccbbaa99887766554433221100ffaa",
    "accountabilityRecord": {
      "gitCommit": "sha256-compatible-git-object-or-release-reference",
      "vcHash": "sha256:e9b15f36f1f85c5a5a62f9bdb9b1d82e7d7d0a2e5f0d1c3b4a59687766554433",
      "bitcoinAnchor": "opentimestamps-proof-file-retained-off-chain"
    },
    "methodology": {
      "fullFacts": true,
      "genuineIndividualConsideration": true,
      "personalAccountability": true,
      "automationOnly": false
    }
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-06-06T21:35:00Z",
    "verificationMethod": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3#z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
    "proofPurpose": "assertionMethod",
    "proofValue": "zExampleSignatureValueGeneratedByTheDIDControlledEd25519Key"
  }
}
```

Rationale: the VC makes the finding portable across Git, email, local vaults,
regulators, courts, and third-party verifiers. It does not make the finding true
by itself; it packages the named-human assertion and links to the hashes required
to audit it.

---

## 6. Selective disclosure and zero knowledge

Use the simplest privacy mechanism that satisfies the risk:

1. **Default:** disclose the VC only to the verifier; publish or anchor only its
   hash.
2. **Selective field disclosure:** split sensitive facts into separate hashed
   exhibits and reveal only the exhibits needed for the verifier's purpose.
3. **Status privacy:** publish transparency-log heads rather than public lists of
   people or claims.
4. **Zero knowledge:** reserve BBS+, SD-JWT VC, or similar schemes for cases where
   a verifier needs proof of a property without seeing the underlying field.

Trade-off: advanced selective-disclosure suites add dependencies and verification
complexity. They should be optional profiles, not the core Burgess requirement.

---

## 7. Hardware-backed keys

For high-stakes SOVEREIGN findings, the methodology should record whether the
named human used a hardware-backed key ceremony:

- WebAuthn/FIDO2 authenticator, security key, passkey, or hardware enclave;
- local presence / user verification requirement where available;
- signed challenge binding the decision hash, DID, timestamp, and finding;
- recovery or revocation path documented before use.

Recommended rule: hardware-backed proof is **not** required for every ordinary
finding, but absence of it should be explainable for high-stakes decisions. The
test remains human accountability, not possession of expensive hardware.

---

## 8. SOVEREIGN methodology adjustment

The definition can be extended as follows:

> A decision is SOVEREIGN only where a named human, attributable through a
> verifiable record and, where appropriate, a DID-controlled or hardware-backed
> key, had the full relevant facts, applied genuine individual consideration, and
> can be held personally accountable for the decision. Otherwise it is NULL.

Cryptographic proof of key control supports the attributable record. It does not
replace the human acts required by the test.

---

## 9. Accessibility and self-sovereignty

This profile must be usable by a profoundly deaf, self-taught, full-stack,
often iPhone-based operator who requires email/post-only reasonable adjustments
and is building sovereign alternatives to proprietary systems.

Practical requirements:

- no dependence on phone calls, video calls, or live identity appointments;
- email/post-compatible verification bundles;
- local-first generation of keys, DIDs, VCs, and hashes;
- plain JSON files that can be inspected, printed, posted, or archived;
- no required custodial wallet, exchange account, or proprietary identity app;
- optional passkey/security-key support because iPhone-based hardware-backed keys
  may be the most accessible secure key path;
- recovery guidance that does not assume institutional support channels.

Sovereignty requires that the operator can create, hold, rotate, revoke, and
explain their own identity keys without permission from the institution being
challenged.

---

## 10. Sovereign Key Management & Recovery

This section is written for one specific person: a lone, profoundly deaf,
self-taught operator with no support network, often working from an iPhone, who
must create, use, back up, rotate, revoke, and recover DID-controlled keys
without depending on any institution, custodian, or real-time human help. It is
deliberately minimalist. Every step is file-based, offline-capable, and uses only
primitives the project already relies on (Ed25519, SHA-256, canonical JSON, plain
files, OpenTimestamps). No new token, chain, account, or mandatory third party is
introduced.

The guiding rule is **sovereignty first**: at no point may any single outside
party hold enough material to use or block your keys without your participation.
Where a recovery scheme involves other people, it is a *threshold* scheme in which
no one helper — and no minority of helpers — can act alone.

### 10.1 Key generation and DID creation

A `did:key` Ed25519 identity is just a keypair plus a deterministic encoding.
Generate it locally, offline, and never let the private seed leave your control.

Minimal ceremony:

1. Generate a 32-byte Ed25519 private seed from a vetted local source (the OS CSPRNG,
   or an iPhone Secure Enclave / passkey where you want hardware backing).
2. Derive the public key and the `did:key` identifier (multicodec `0xed01` prefix,
   multibase `z`-base58btc) — this is the same identifier already shown in §4.
3. Write the public DID document (§4) to a plain JSON file. It contains **no**
   secret material and is safe to print, post, email, or anchor by hash.
4. Keep the private seed only inside the encrypted local store described in §10.2.
5. Record the DID's *birth* as the first entry of an append-only **key-event log**
   (§10.4) and commit its hash to Git and, optionally, to Bitcoin via
   OpenTimestamps.

You may hold more than one DID:

- a **long-lived identity DID** that anchors who you are across rotations;
- short-lived **operational DIDs** used to sign day-to-day findings;
- **pairwise DIDs** for sensitive counterparties to avoid a public correlation
  trail (see spec §8).

Rationale and trade-off: `did:key` has no native rotation or registry — that is
exactly why it is sovereign. The cost is that *you* are responsible for the
key-event log that records succession. We turn that log into a hash-only,
Git-anchored artefact so it is auditable without any hosted DID resolver.

### 10.2 Secure local storage and backup format

Keep one canonical layout so muscle memory, not memory of paths, gets you home.

Recommended on-device layout (mirrors the existing `.sovereign-vault/` discipline):

```
.sovereign-keys/
  README.txt                     # plain-language map of this folder (printable)
  identity/
    did.json                     # public DID document (no secrets)
    key-events.jsonl             # append-only key-event log (hashes + signatures)
    key-events.ots               # OpenTimestamps proof(s) for the log head
  secrets/
    seed.age                     # encrypted Ed25519 seed (age/passphrase or passkey)
    seed.shard-1.txt .. shard-N  # OPTIONAL Shamir shards (kept apart, see §10.3)
  backup/
    sovereign-key-backup.json    # portable encrypted export (format below)
    sovereign-key-backup.sha256  # digest of the export, for integrity checks
    recovery-instructions.txt    # step-by-step, written for future-you
```

Storage tiers (hybrid hardware + software):

- **Primary (hot):** seed encrypted at rest in `secrets/seed.age`, unlocked by a
  passphrase or an iPhone passkey/Secure-Enclave ceremony for daily signing.
- **Cold copy:** the same encrypted export on at least two offline media kept in
  two physical locations (e.g. one USB key in a drawer, one in a sealed envelope).
  Because the export is already encrypted, losing the medium does not leak the key.
- **Paper fallback:** the seed (or a Shamir shard) printed as a BIP39-style word
  list or base58 string. Paper survives dead batteries and dead vendors.

Portable encrypted backup format (`sovereign-key-backup.json`), validated by
[`schemas/key-event-credential.v1.json`](./schemas/key-event-credential.v1.json)
for the `KeyBirth`/`KeyRotation`/`KeyRevocation` events it carries:

```json
{
  "bundle_kind": "sovereign-key-backup",
  "bundle_schema_version": 1,
  "exported_at": "2026-06-06T21:35:00Z",
  "did": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
  "kdf": { "name": "scrypt", "n": 1048576, "r": 8, "p": 1, "salt_hex": "..." },
  "cipher": { "name": "xchacha20poly1305", "nonce_hex": "...", "ct_hex": "..." },
  "recovery": {
    "scheme": "shamir",
    "threshold": 2,
    "shares": 3,
    "note": "Encrypted seed; OR reconstruct from any 2 of 3 shards held apart."
  },
  "key_events_head": "sha256:7f4f8c0b6d2b5f4f5e9c5d0f6e8a9b0c1d2e3f405162738495a6b7c8d9e0f123",
  "integrity": { "hash_algorithm": "sha256", "self_hash": "sha256:<digest-of-this-file-with-this-field-blank>" }
}
```

Rationale and trade-off: the export holds only an *encrypted* seed plus public
metadata, so it is safe to copy widely — the more copies, the lower the loss risk.
The trade-off is that backup security now rests on the passphrase / shard secrecy;
the accessibility checklist (§10.7) addresses how a lone operator keeps that
secret recoverable to themselves but not to anyone else.

### 10.3 Recovery mechanisms without surrendering sovereignty

Pick the simplest scheme that survives your specific failure modes. All three are
file-based and need no live coordination.

1. **Self-custody passphrase recovery (default).** Restore `seed.age` on any
   device and unlock with the passphrase or passkey. Zero other parties involved.
   Fails only if you lose both the encrypted export *and* the passphrase.

2. **Threshold (Shamir) recovery.** Split the seed into N shards needing any K to
   reconstruct (e.g. 2-of-3). Hold the shards yourself across separate media/
   locations, or place individual shards with trusted contacts. No single holder —
   and no K-1 subset — can reconstruct the key, so no one can act unilaterally or
   block you. This is "social recovery" without a custodian and without a quorum
   that can seize your identity.

3. **Successor-DID recovery (sovereignty-preserving rotation).** If the seed is
   lost beyond reconstruction, you do not "recover" the old key — you generate a
   fresh DID and publish a signed succession only if you still hold a prior valid
   key (see §10.4). If you hold no valid key at all, recovery is *re-establishment*:
   a new DID whose key-event log references the old DID's last anchored head and
   any Git/Bitcoin evidence proving continuity of the same named human. Continuity
   rests on the public, anchored audit trail, not on any third party vouching.

Example file-based recovery flow (deaf-friendly, no calls, no real-time steps):

```
Step 1.  Locate any one backup medium with sovereign-key-backup.json.
Step 2.  Verify integrity:   sha256(sovereign-key-backup.json) == .sha256 file?
                             -> mismatch: STOP, try another copy. Clear error.
Step 3a. Passphrase path:    enter passphrase -> decrypt -> seed recovered.
Step 3b. Shamir path:        gather any K shard files -> combine -> seed recovered.
Step 4.  Re-derive did:key from the seed; confirm it equals did.json "id".
                             -> mismatch: wrong seed/backup. Clear error, stop.
Step 5.  Re-append a "KeyRecovery" event to key-events.jsonl, sign it, re-anchor
         the new log head (Git commit + optional OpenTimestamps).
Step 6.  Resume signing. Nothing secret ever left the device during recovery.
```

Rationale and trade-off: threshold recovery removes the single-point-of-failure of
one passphrase without creating a custodian who could act alone. The cost is more
moving parts; the checklist in §10.7 keeps it to a 2-of-3 scheme that a lone
operator can physically manage.

### 10.4 Rotation and revocation with auditable linkage

`did:key` cannot mutate in place, so rotation and revocation are expressed as
**signed events in an append-only log**, then committed by hash exactly like every
other Burgess artefact. The log lives at `identity/key-events.jsonl` (one JSON
object per line) and is the source of truth for "which key is current".

Each event is a small object signed by the key that is still authoritative at the
time of the event:

- `KeyBirth` — establishes a DID; self-signed by the new key.
- `KeyRotation` — the *old* key signs over the new key's DID, marking succession.
  Anyone holding the old anchored log can verify the chain forward.
- `KeyRevocation` — the authoritative key (or, if compromised/lost, a threshold of
  recovery shards reconstituting it) signs a statement retiring a key/DID, with a
  reason code.
- `KeyRecovery` — records a restore event for the audit trail (§10.3).

Only the **hash of the new log head** (and optionally a signed event commitment)
is ever placed on a public ledger; the events themselves stay local and can be
disclosed selectively. This preserves the project's hashes-only discipline while
giving any verifier a way to answer "was this finding signed by a key that was
valid and unrevoked at signing time?".

Linkage to existing anchored records:

- Every rotation/revocation event references the **previous log head hash**,
  forming a hash chain back to `KeyBirth`.
- The log head is committed in Git (a trailer or a tag) and may be timestamped via
  OpenTimestamps, so the *order* of rotations is provable.
- VCs already carry `accountabilityRecord` (§5); a verifier resolves the signing
  key's status by walking the key-event log to the head anchored at or before the
  VC's `validFrom`.

Rationale and trade-off: an append-only signed log is the minimum mechanism that
gives `did:key` rotation and revocation without a registry or smart contract. The
trade-off is that revocation is only as timely as your last anchor — so anchor the
log head whenever you rotate or revoke, especially after a suspected compromise.

### 10.5 Minimal Python sketch — DID-controlled signing

This sketch reuses the existing `iris/anchor.py` helpers
(`canonical_json_sha256`, `build_did_signing_payload`) so a key-event or finding is
committed and signed exactly like an anchor manifest. Signing itself stays outside
the stdlib core: plug in an Ed25519 library, an iPhone passkey, or a hardware
signer. It takes no custody of private keys it is not given.

```python
# Sketch — integrates with iris/anchor.py style helpers. Pseudocode for the
# signer; everything else is plain standard library.
from iris.anchor import canonical_json_sha256, build_did_signing_payload

def append_key_event(log_path, *, event, did, sign):
    """Append a signed key-event to the append-only log and return the new head.

    `event`  : "KeyBirth" | "KeyRotation" | "KeyRevocation" | "KeyRecovery"
    `did`    : the controller did:key being asserted by this event
    `sign`   : callable(digest_hex) -> signature_hex  (Ed25519 / passkey / HW)
    """
    prev_head = _read_head(log_path)              # None for the first event
    record = {
        "event": event,
        "did": did,
        "prev": prev_head,                        # hash chain back to KeyBirth
        "created": _utc_now_iso(),
    }
    # Canonical commitment over the record (sorted keys, no whitespace).
    commitment = canonical_json_sha256(record)
    # Wrap the commitment in the same DID signing payload used for anchoring.
    payload = build_did_signing_payload(commitment, controller=did)
    signature = sign(canonical_json_sha256(payload))   # key never seen here
    line = {**record, "commitment": f"sha256:{commitment}", "signature": signature}
    _append_jsonl(log_path, line)                 # append-only; never rewrite
    return line["commitment"]                     # the new, anchorable log head
```

To rotate: call `append_key_event(..., event="KeyRotation", did=new_did,
sign=old_key_sign)` — the *old* key signs the succession. To revoke: sign a
`KeyRevocation` with the authoritative key (or reconstituted threshold). Then
anchor the returned head with `build_anchor_manifest([...])` and OpenTimestamps.

Rationale and trade-off: keeping the signer as an injected callable means the same
flow works for a softkey on a laptop and a passkey on an iPhone, and the helper
never holds a private seed. The trade-off is that the operator must supply a
trustworthy signer; the checklist notes which options are most accessible.

### 10.6 Integration notes — Git-as-governance and Bitcoin anchoring

- **Git-as-governance.** The key-event log head is the canonical succession record.
  Commit it (or its hash) with a `Burgess-DID:` trailer (see §3.1); rotations and
  revocations become reviewable pull requests and signed tags. Git history gives
  ordering and named-human review; the log gives cryptographic succession.
- **Bitcoin proof-of-existence.** Anchor `key-events.jsonl`'s head hash via
  OpenTimestamps whenever you rotate or revoke, exactly as for the findings ledger
  (`onchain-protocol/bitcoin-anchoring.md`). Only the digest is anchored — never a
  key, seed, or fact. A revocation that is anchored before a disputed signature is
  provably earlier, which is what a Dispute / Challenge Layer reviewer needs.
- **Dispute / Challenge Layer.** When a finding is challenged on `no_named_human`
  or `not_accountable` grounds, the reviewer can walk the anchored key-event log to
  confirm the signing key was valid and unrevoked at `validFrom`. The log is
  hash-committed, so this check needs no hosted resolver.

### 10.7 Accessibility and sovereignty checklist (lone deaf operator)

Tailored to a profoundly deaf operator with no support network, often on an iPhone:

- [ ] **No voice, no real-time.** Every step is file-based and asynchronous — no
      phone/video call, no live appointment, no time-boxed human coordination.
- [ ] **Clear, textual error states.** Each recovery step has an explicit
      pass/fail with a written next action (see §10.3); failures say *stop and try
      another copy*, never silently continue.
- [ ] **Printable plain files.** DID document, key-event log, backup, and recovery
      instructions are plain text/JSON that can be inspected, printed, or posted.
- [ ] **iPhone-first hardware option.** A passkey / Secure-Enclave ceremony is an
      accepted signer, because it may be the most accessible hardware-backed key.
- [ ] **Self-recoverable, not custodian-dependent.** Default recovery needs only
      *you* (passphrase) or *your own* shards; no institution can unlock or block.
- [ ] **Threshold, not single helper.** If any contacts hold shards, use K-of-N so
      no one helper — and no sub-quorum — can act alone or be coerced alone.
- [ ] **Two copies, two places.** At least two encrypted backups in two physical
      locations, plus one paper fallback that survives dead devices/vendors.
- [ ] **Rehearsed recovery.** Do a dry-run restore on a spare device at least once,
      so the written steps are known-good before a real emergency.
- [ ] **Anchor on change.** Re-anchor the key-event head on every rotation or
      revocation so timeliness does not depend on memory.
- [ ] **No mandatory third party.** Nothing in the flow requires an account,
      custodian, exchange, hosted resolver, or new token/chain.

Rationale and trade-off: the checklist trades a little upfront setup (two copies, a
rehearsed restore, a 2-of-3 split) for the ability to fully recover alone, asynchronously, in writing — the failure modes most dangerous to a lone operator
without a support network.

---

## 11. Open questions and trade-offs

- **DID method:** `did:key` is simplest and self-contained, but has no native
  rotation. Rotation should be handled through Git records, registry entries, and
  anchored revocation logs.
- **VC proof suite:** Ed25519 JSON-LD signatures align with the existing stack;
  JWT or SD-JWT may be easier for some verifiers. The repository should support
  hashes and examples before adding dependencies.
- **Human binding:** no cryptographic standard alone proves that a controller is a
  specific human. Burgess records must keep the named attribution layer.
- **Hardware access:** hardware-backed keys strengthen high-stakes findings but
  must not exclude people who cannot afford or use specialist devices.
- **On-chain minimisation:** DID and VC fields belong in off-chain payloads and
  receipts. Public chains should continue to see hashes only.

*The Burgess Principle — UK Certification Mark UK00004343685*
