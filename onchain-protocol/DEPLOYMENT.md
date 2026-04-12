# Deployment Guide — Burgess Claims Protocol

Deploy the `BurgessClaimsRegistry` smart contract to an EVM-compatible L2 chain, then post a fingerprint generated from the current local-first Burgess workflow.

---

## Prerequisites

- [Node.js](https://nodejs.org/) ≥ 18
- [Foundry](https://book.getfoundry.sh/getting-started/installation) (recommended) **or** [Hardhat](https://hardhat.org/)
- An Ethereum wallet with testnet ETH (for gas)
- Python 3.11+ with `PyNaCl` installed (for the SDK or Sovereign Local claim generation)

---

## Option A: Deploy with Foundry (recommended)

### 1. Install Foundry

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

### 2. Compile the contract

```bash
cd onchain-protocol/contracts
forge build --contracts BurgessClaimsRegistry.sol
```

### 3. Deploy to Base Sepolia testnet

```bash
# Set your private key (EVM wallet, not Ed25519)
export PRIVATE_KEY="0x..."
export RPC_URL="https://sepolia.base.org"

forge create \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  BurgessClaimsRegistry
```

### 4. Note the deployed contract address

The output will include the contract address. Save it for SDK usage.

---

## Option B: Deploy with Hardhat

### 1. Initialise a Hardhat project

```bash
cd onchain-protocol/scripts
npm init -y
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init
```

### 2. Copy the contract

```bash
cp ../contracts/BurgessClaimsRegistry.sol contracts/
```

### 3. Create deployment script

Create `scripts/deploy.js`:

```javascript
const { ethers } = require("hardhat");

async function main() {
  const Registry = await ethers.getContractFactory("BurgessClaimsRegistry");
  const registry = await Registry.deploy();
  await registry.waitForDeployment();
  console.log("BurgessClaimsRegistry deployed to:", await registry.getAddress());
}

main().catch(console.error);
```

### 4. Deploy

```bash
npx hardhat run scripts/deploy.js --network base-sepolia
```

---

## Post-Deployment: Generate a Fingerprint Package

If you are already using Sovereign Local Mode, you can generate the claim package with `POST /api/generate-claim` and optionally queue the fingerprint locally before posting it. If you want a direct SDK flow, run the following from the repository root:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path("onchain-protocol/sdk").resolve()))

from onchain_claims import generate_onchain_claim

claim = generate_onchain_claim(
    claim_details="My case was not reviewed by a human",
    target_entity="Example Council",
    category="enforcement",
    private_key_hex="<your-ed25519-private-key-hex>",
)

print(claim.to_json())
# Post this JSON to the deployed contract's issueClaim() function
# using web3.py, ethers.js, or cast (Foundry).
```

The exported JSON is safe to keep locally or queue for later posting because it contains only the commitment fingerprint and metadata, not the full underlying claim record.

### Post with Foundry cast

```bash
cast send $CONTRACT_ADDRESS \
  "issueClaim(bytes32,bytes,string,string,uint256)" \
  $COMMITMENT_HASH \
  $SIGNATURE \
  "Example Council" \
  "enforcement" \
  0 \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY
```

---

## Supported Chains

| Chain | RPC URL | Faucet |
|---|---|---|
| Base Sepolia | `https://sepolia.base.org` | [base.org/faucet](https://www.base.org/faucet) |
| Arbitrum Sepolia | `https://sepolia-rollup.arbitrum.io/rpc` | [faucet.arbitrum.io](https://faucet.arbitrum.io/) |
| Optimism Sepolia | `https://sepolia.optimism.io` | [app.optimism.io/faucet](https://app.optimism.io/faucet) |

---

## Verify the Contract

```bash
forge verify-contract \
  --chain-id 84532 \
  --compiler-version v0.8.20 \
  $CONTRACT_ADDRESS \
  BurgessClaimsRegistry \
  --etherscan-api-key $BASESCAN_API_KEY
```

---

## Security Notes

- The contract stores only commitment hashes and signatures — **no personal data**.
- Ed25519 signature verification happens **off-chain** (EVM does not natively support Ed25519).
- The EVM wallet key (secp256k1) is used only for gas payment. Claim signatures use Ed25519 from the Sovereign Vault.
- See [SECURITY.md](../SECURITY.md) for the full cryptographic baseline.

---

**Maintained under the Burgess Principle**
UK Certification Mark: UK00004343685
