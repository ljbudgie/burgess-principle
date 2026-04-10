# Burgess Claims Protocol — Specification v0.1.0

> Lightweight on-chain protocol for issuing, storing, and verifying Burgess Claims as immutable, cryptographically signed commitment fingerprints.

---

## 1. Overview

The Burgess Claims Protocol extends the [Sovereign Personal Vault](../enforcement/sovereign-vault/) with a minimal on-chain layer. Users generate claims off-chain in the Vault, then post only a compact **commitment fingerprint** (hash + signature + metadata) to a public blockchain for neutral timestamping, ordering, and verifiability.

Full claim details remain encrypted in the user's local Vault. The chain stores only what is needed to prove that a claim existed at a specific time and was signed by a specific key.

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
| `target_entity` | string | The institution or system being addressed |
| `category` | string | Claim category (e.g. `enforcement`, `dispute`, `oversight`, `disclosure`) |

### 2.2 Commitment (On-Chain Fingerprint)

The commitment posted on-chain is:

```
commitment_hash = SHA-256( claim_details || timestamp || nonce || user_pubkey )
signature        = Ed25519.sign( private_key, commitment_hash )
```

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
│  2. Compute commitment_hash = SHA-256(details‖ts‖nonce‖pk) │
│  3. Sign commitment_hash with Ed25519 private key       │
│  4. Store full details encrypted locally                 │
│  5. Export compact JSON for on-chain posting             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  BLOCKCHAIN (On-Chain)                   │
│                                                         │
│  6. Call issueClaim(hash, sig, target, category, expiry) │
│  7. Contract stores fingerprint + block timestamp       │
│  8. Emits ClaimIssued event                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                 VERIFIER (Anyone)                        │
│                                                         │
│  9. Read claim from contract via getClaim(id)           │
│  10. Verify Ed25519 signature against known public key  │
│  11. Optionally: user reveals claim details off-chain   │
│  12. Verifier re-computes hash to confirm match         │
└─────────────────────────────────────────────────────────┘
```

---

## 5. Verification Flow

### 5.1 On-Chain Verification (Public)

Anyone can:
1. Call `getClaim(claimId)` to retrieve the stored fingerprint.
2. Verify that `commitmentHash` is a valid 32-byte value.
3. Verify the Ed25519 `signature` against the claimant's known public key and the `commitmentHash`.
4. Check the `blockTimestamp` for temporal ordering.

### 5.2 Off-Chain Verification (Selective Disclosure)

When the claimant chooses to reveal details:
1. Claimant provides `claim_details`, `timestamp`, `nonce`, and `user_pubkey`.
2. Verifier computes `SHA-256(claim_details || timestamp || nonce || user_pubkey)`.
3. Verifier compares with the on-chain `commitmentHash`.
4. Match → the claim existed at the recorded block time. Mismatch → tampered.

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

---

## 8. Privacy Considerations

- **No personal data on-chain.** Only hashes and signatures are stored.
- **Unlinkability.** Each commitment uses a fresh random nonce.
- **Selective disclosure.** The user controls when and to whom they reveal claim details.
- **Right to be forgotten.** Since no personal data is on-chain, GDPR right to erasure is not implicated.

---

## 9. Security Requirements

All implementations must follow the cryptographic baseline defined in [SECURITY.md](../SECURITY.md):

- **SHA-256** for commitment hashing with fresh 32-byte nonce per claim.
- **Ed25519** for claim signatures (consistent with Sovereign Vault).
- **Canonical sorted-key JSON** for deterministic serialisation of claim data before hashing.
- **Hex encoding** for all binary-to-text conversions.
- **No additional cryptographic dependencies** beyond those already approved.

---

## 10. SDK Interface (Python)

```python
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
```

---

## 11. Versioning

This specification is versioned independently from the Sovereign Vault:

| Version | Status |
|---|---|
| v0.1.0 | Draft — initial specification |

---

**Maintained under the Burgess Principle**
UK Certification Mark: UK00004343685
