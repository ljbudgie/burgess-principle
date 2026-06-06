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

## 10. Open questions and trade-offs

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
