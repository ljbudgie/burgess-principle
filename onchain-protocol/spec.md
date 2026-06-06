# Burgess Claims Protocol — Specification v0.3.0

> Lightweight on-chain protocol for issuing, storing, and verifying Burgess Claims as immutable, cryptographically signed commitment fingerprints.

---

## 1. Overview

The Burgess Claims Protocol extends the [Sovereign Personal Vault](../enforcement/sovereign-vault/) and the current **Sovereign Local Mode** workflow with a minimal on-chain layer. Users generate claims off-chain in the Vault or via Iris local claim generation, then post only a compact **commitment fingerprint** (hash + signature + metadata) to a public blockchain for neutral timestamping, ordering, and verifiability.

Full claim details remain encrypted in the user's local Vault. In the current local-first flow, a user may also queue a ready-to-post fingerprint package under `.sovereign-vault/pending-onchain-fingerprints/` before they decide to submit it. The chain stores only what is needed to prove that a claim existed at a specific time and was signed by a specific key.

### Design Principles

- **Minimalist** — no new L1, no heavy consensus. A single smart contract on an existing EVM L2.
- **Sovereign** — full claim data stays with the user. The chain sees only hashes and signatures.
- **Human-first** — the protocol exists to prove that a human demanded oversight, not to automate it away.
- **Composable** — any system (exchange, DAO, regulator, platform) can verify claims using open-source tools.

---

## 2. Data Model

### 2.1 Claim (Off-Chain — Vault)

A claim is generated in the Sovereign Personal Vault and contains:

| Field | Type | Description |
|---|---|---|
| `claim_details` | string | Free-text description of the claim (encrypted locally) |
| `timestamp` | ISO 8601 | When the claim was created |
| `nonce` | hex string (32 bytes) | Fresh random nonce for unlinkability |
| `user_pubkey` | hex string | Ed25519 public key of the claimant |
| `issuer_did` | DID string, optional | DID of the claimant, reviewer, or issuing institution |
| `subject_did` | DID string, optional | DID of the person, claim, or decision subject where appropriate |
| `verification_method` | DID URL, optional | DID verification method used for Ed25519 proof verification |
| `target_entity` | string | The institution or system being addressed |
| `category` | string | Claim category (e.g. `enforcement`, `dispute`, `oversight`, `disclosure`) |
| `vc_hash` | string, optional | `sha256:<hex>` commitment to a Verifiable Credential wrapping the claim or finding |

The minimalist identity profile is `did:key` with Ed25519 keys. A DID proves
control of a key; it does not, by itself, prove that the controller is a named
human. SOVEREIGN attribution still requires a disclosed or auditable record
binding that key to the named human who considered the facts.

### 2.2 Commitment (On-Chain Fingerprint)

The commitment posted on-chain is computed from a canonical JSON payload:

```
canonical_claim_json = serialize_json({
  "claim_details": ...,
  "issuer_did": ...,
  "nonce": ...,
  "public_key": ...,
  "subject_did": ...,
  "timestamp": ...
}, sort_keys=True, compact=True)

commitment_hash = SHA-256( canonical_claim_json )
signature        = Ed25519.sign( private_key, commitment_hash )
```

Early draft claims used `SHA-256(claim_details || timestamp || nonce || user_pubkey)`. Verifiers may continue to accept that legacy format for backwards compatibility, but new implementations should emit canonical JSON commitments.

The on-chain record stores:

| Field | Type | Solidity Type | Description |
|---|---|---|---|
| `commitmentHash` | bytes32 | `bytes32` | SHA-256 commitment hash |
| `signature` | bytes | `bytes` | Ed25519 signature over the commitment hash |
| `issuer` | address | `address` | Ethereum address of the transaction sender |
| `target` | string | `string` | Target entity identifier |
| `category` | string | `string` | Claim category |
| `expiry` | uint256 | `uint256` | Optional expiry timestamp (0 = no expiry) |
| `blockTimestamp` | uint256 | `uint256` | Block timestamp (set automatically) |

DID, VC, and human-attribution fields SHOULD remain off-chain in the canonical
preimage or receipt bundle. The smart contract does not need to understand DID
methods or VC proof suites; it stores the resulting hash and signature only.

### 2.4 Verifiable Credential wrapper (Off-Chain)

A SOVEREIGN/NULL finding MAY be issued as a W3C Verifiable Credential. The VC is
portable evidence; the chain or Bitcoin anchor receives only `sha256:<vc-json>`.

Minimum credential subject fields:

| Field | Type | Description |
|---|---|---|
| `finding` | enum | `SOVEREIGN` or `NULL` |
| `targetEntity` | string | Institution, system, claim, or decision reviewed |
| `namedHuman.did` | DID string | DID controlled by the reviewer or attestor |
| `namedHuman.name` | string | Human-readable named accountable person where disclosure is lawful |
| `fullFactsBasisHash` | string | `sha256:<hex>` commitment to the facts considered |
| `individualConsiderationRecordHash` | string | `sha256:<hex>` commitment to the reasoning/review record |
| `accountabilityRecord` | object | Git commit, tag, release, ledger, or registry references |
| `methodology` | object | Booleans for full facts, genuine individual consideration, personal accountability, and automation-only exclusion |

Example VC:

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://w3id.org/security/suites/ed25519-2020/v1",
    "https://theburgessprinciple.com/contexts/burgess-v1"
  ],
  "id": "urn:uuid:0f8a4f6c-8a4f-4a72-8b2f-2d0e3d4b5c6a",
  "type": ["VerifiableCredential", "BurgessSovereignFindingCredential"],
  "issuer": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
  "validFrom": "2026-06-06T21:35:00Z",
  "credentialSubject": {
    "id": "urn:burgess:claim:sha256:7f4f8c0b6d2b5f4f5e9c5d0f6e8a9b0c1d2e3f405162738495a6b7c8d9e0f123",
    "targetEntity": "Example Institution",
    "finding": "SOVEREIGN",
    "namedHuman": {
      "name": "Named Human Reviewer",
      "did": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
      "verificationMethod": "did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3#z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3"
    },
    "fullFactsBasisHash": "sha256:3b7e1a8f4b5c6d7e8f90123456789abcdef0123456789abcdef0123456789abcd",
    "individualConsiderationRecordHash": "sha256:6f2d1c0b9a887766554433221100ffeeddccbbaa99887766554433221100ffaa",
    "accountabilityRecord": {
      "gitCommit": "repository-commit-or-tag-reference",
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

Verifiers SHOULD hash the canonical VC JSON, compare it to any on-chain or
Bitcoin-anchored `vc_hash`, verify the Ed25519 proof against the DID document,
then inspect the disclosed accountability record for named-human sufficiency.

### 2.3 Response (Optional On-Chain)

A counterparty may respond to a claim:

| Field | Type | Description |
|---|---|---|
| `claimId` | uint256 | ID of the original claim |
| `responseCommitment` | bytes32 | SHA-256 hash of the response details |
| `responderSignature` | bytes | Signature from the responding party |

---

## 3. Smart Contract Interface

```solidity
interface IBurgessClaimsRegistry {
    // Events
    event ClaimIssued(uint256 indexed claimId, bytes32 commitmentHash, address indexed issuer, string target, string category);
    event ClaimResponse(uint256 indexed claimId, bytes32 responseCommitment, address indexed responder);

    // Write
    function issueClaim(bytes32 commitmentHash, bytes calldata signature, string calldata target, string calldata category, uint256 expiry) external returns (uint256 claimId);
    function respondToClaim(uint256 claimId, bytes32 responseCommitment, bytes calldata responderSignature) external;

    // Read
    function getClaim(uint256 claimId) external view returns (bytes32 commitmentHash, bytes memory signature, address issuer, string memory target, string memory category, uint256 expiry, uint256 blockTimestamp);
    function getClaimCount() external view returns (uint256);
    function getResponse(uint256 claimId) external view returns (bytes32 responseCommitment, bytes memory responderSignature, address responder, uint256 responseTimestamp);
}
```

---

## 4. Claim Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                    USER (Off-Chain)                      │
│                                                         │
│  1. Create claim in Sovereign Vault                     │
│  2. Build canonical claim JSON                           │
│  3. Compute commitment_hash = SHA-256(canonical_json)    │
│  4. Sign commitment_hash with Ed25519 private key,       │
│     optionally identified by issuer_did / verification   │
│     method or wrapped in a VC                            │
│  5. Store full details encrypted locally                 │
│  6. Optionally queue a pending on-chain fingerprint      │
│     in `.sovereign-vault/pending-onchain-fingerprints/`  │
│  7. Export compact JSON for manual posting               │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  BLOCKCHAIN (On-Chain)                   │
│                                                         │
│  8. Call issueClaim(hash, sig, target, category, expiry) │
│  9. Contract stores fingerprint + block timestamp       │
│  10. Emits ClaimIssued event                            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 VERIFIER (Anyone)                        │
│                                                         │
│  11. Read claim from contract via getClaim(id)          │
│  12. Verify Ed25519 signature against known public key  │
│      or DID verification method                         │
│  13. Optionally: user reveals the canonical claim JSON, │
│      DID document, VC, or local signed receipt bundle   │
│      fields or a local signed receipt bundle            │
│  14. Verifier re-computes hash to confirm match         │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Verification Flow

### 5.1 On-Chain Verification (Public)

Anyone can:
1. Call `getClaim(claimId)` to retrieve the stored fingerprint.
2. Verify that `commitmentHash` is a valid 32-byte value.
3. Verify the Ed25519 `signature` against the claimant's known public key or DID verification method and the `commitmentHash`.
4. Check the `blockTimestamp` for temporal ordering.

### 5.2 Off-Chain Verification (Selective Disclosure)

When the claimant chooses to reveal details:
1. Claimant provides `claim_details`, `timestamp`, `nonce`, `user_pubkey`, and any disclosed DID/VC fields.
2. Verifier serializes those fields into canonical sorted-key JSON.
3. Verifier computes `SHA-256(canonical_claim_json)`.
4. Verifier compares with the on-chain `commitmentHash`.
5. If a VC is disclosed, verifier computes `SHA-256(canonical_vc_json)` and compares it with `vc_hash` or the anchored transparency-log entry.
6. Match → the claim or finding existed at the recorded block time. Mismatch → tampered.

If the claim originated from Sovereign Local Mode, the claimant may also pair the on-chain fingerprint with a local signed receipt or Memory Palace export to prove integrity inside a wider local evidence trail.

---

## 6. Categories

| Category | Use Case |
|---|---|
| `enforcement` | Challenging automated enforcement actions |
| `dispute` | General disputes with institutions |
| `oversight` | Demanding human oversight of automated decisions |
| `disclosure` | Data subject access or FOI requests |
| `dao` | DAO governance disputes |
| `exchange` | Crypto exchange support escalations |

---

## 7. Chain Selection

The protocol targets **EVM-compatible L2 chains** for low gas costs and broad tooling support:

| Chain | Status | Notes |
|---|---|---|
| Base (Sepolia testnet) | Primary target | Low gas, good ecosystem |
| Arbitrum | Supported | Alternative L2 |
| Optimism | Supported | Alternative L2 |

The contract is standard Solidity and can be deployed to any EVM chain.

**For proof-of-existence anchoring** — the default for *evidence integrity*
(findings ledger, attestations, registry transparency log) — see
[`bitcoin-anchoring.md`](./bitcoin-anchoring.md): Bitcoin via OpenTimestamps,
**no token, hash-only**. The EVM backend above remains for programmable
composability; Bitcoin anchoring is for neutral, un-capturable timestamping.

---

## 8. Privacy Considerations

- **No personal data on-chain.** Only hashes and signatures are stored.
- **Unlinkability.** Each commitment uses a fresh random nonce.
- **Selective disclosure.** The user controls when and to whom they reveal claim details.
- **DID correlation risk.** Reusing a single DID across many sensitive claims can create a public correlation trail. Use pairwise or purpose-specific DIDs where privacy requires it.
- **Zero-knowledge optionality.** BBS+, SD-JWT VC, or equivalent selective-disclosure schemes may be used for higher privacy cases, but they are optional profiles rather than the base protocol.
- **Right to be forgotten.** Since no personal data is on-chain, GDPR right to erasure is not implicated.

---

## 9. Security Requirements

All implementations must follow the cryptographic baseline defined in [SECURITY.md](../SECURITY.md):

- **SHA-256** for commitment hashing with fresh 32-byte nonce per claim.
- **Ed25519** for claim signatures (consistent with Sovereign Vault).
- **DID proof verification** for DID-backed claims, normally `did:key` Ed25519.
- **Canonical sorted-key JSON** for deterministic serialisation of claim data before hashing.
- **Hex encoding** for all binary-to-text conversions.
- **No additional cryptographic dependencies** beyond those already approved.
- **Local-first claim custody** — full claim text, receipts, and queued posting packages remain under user control until deliberately exported or posted.
- **High-stakes key ceremony** — where a finding affects liberty, housing, livelihood, legal status, or core rights, record whether a WebAuthn/FIDO2 or other hardware-backed ceremony was used to bind the named human to the commitment.

## 10. Named human identity profile

The protocol recognises a DID as a key-control identifier, not as a substitute for
the SOVEREIGN test. A DID-backed finding is SOVEREIGN only if the disclosed or
auditable record also shows:

1. the real named human accountable for the finding;
2. the facts available to that human, committed by hash where necessary;
3. the individual reasoning or consideration record, committed by hash where
   privacy requires;
4. the DID verification method used to sign the claim, finding, or VC;
5. the Git commit, tag, PR, release, registry entry, or signed bundle that makes
   attribution durable;
6. any high-stakes hardware-backed signing ceremony used.

For the detailed identity profile and examples, see
[`CRYPTOGRAPHIC_IDENTITY.md`](../CRYPTOGRAPHIC_IDENTITY.md).

---

## 11. SDK Interface (Python)

```python
# From the repository root:
#   cd onchain-protocol/sdk
#   python
from onchain_claims import generate_onchain_claim, verify_onchain_receipt

# Generate a claim ready for on-chain posting
claim = generate_onchain_claim(
    claim_details="My council tax was sent to enforcement without human review",
    target_entity="Example Council",
    category="enforcement",
    private_key_hex="<ed25519-private-key-hex>",
)
# claim.commitment_hash, claim.signature, claim.to_json()

# Verify an on-chain receipt
result = verify_onchain_receipt(
    commitment_hash="<from-chain>",
    signature="<from-chain>",
    public_key_hex="<claimant-pubkey>",
)
# result.valid, result.details

# Selective disclosure check
from onchain_claims import verify_commitment
```

For Bitcoin anchoring and DID-aware signing payloads:

```python
from iris.anchor import build_anchor_manifest, build_did_signing_payload, canonical_json_sha256

manifest = build_anchor_manifest(
    ["audits/example.csv"],
    did_controller="did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
)
payload = build_did_signing_payload(
    canonical_json_sha256(manifest["entries"]),
    controller="did:key:z6MkmM42vxfqZQsv4ehtTjFFxQ4sQKS2aG6gy4PVu7o2nyU3",
)
# Sign canonical_json_sha256(payload) with the DID-controlled Ed25519 key or
# hardware-backed ceremony. Store the signature off-chain with the manifest.
```

---

## 12. Versioning

This specification is versioned independently from the Sovereign Vault:

| Version | Status |
|---|---|
| v0.3.0 | Draft — adds DID/VC identity profile while preserving hashes-only on-chain storage |
| v0.2.0 | Draft — aligned with v1.3.0 local-first workflows and canonical JSON commitments |
| v0.1.0 | Historical draft — original concatenation-based commitment preimage |

---

**Maintained under the Burgess Principle**
UK Certification Mark: UK00004343685
