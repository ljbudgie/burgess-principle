#!/usr/bin/env python3
"""End-to-end example: Vault → Claim → On-Chain Post (simulated).

This script demonstrates the full Burgess Claims flow:
  1. Generate an Ed25519 keypair.
  2. Create a claim with details, target, and category.
  3. Compute the commitment hash and sign it.
  4. Verify the signature (simulates on-chain verification).
  5. Verify the commitment via selective disclosure.

Run::

    pip install PyNaCl
    python onchain-protocol/examples/vault_to_chain.py
"""

import os
import sys

# Ensure the SDK is importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk"))

from nacl.signing import SigningKey

from onchain_claims import (
    generate_onchain_claim,
    verify_commitment,
    verify_onchain_receipt,
)


def main() -> None:
    # --- Step 1: Generate keypair ---
    print("=== Burgess Claims Protocol — End-to-End Example ===\n")
    sk = SigningKey.generate()
    private_key_hex = sk.encode().hex()
    public_key_hex = sk.verify_key.encode().hex()
    print(f"Public key:  {public_key_hex}")
    print(f"Private key: {private_key_hex[:16]}…(redacted)\n")

    # --- Step 2: Generate claim ---
    claim = generate_onchain_claim(
        claim_details="My council tax was sent to enforcement without any human review of the specific facts.",
        target_entity="Example Borough Council",
        category="enforcement",
        private_key_hex=private_key_hex,
    )

    print("--- Claim Generated ---")
    print(f"  Commitment hash: {claim.commitment_hash}")
    print(f"  Signature:       {claim.signature[:32]}…")
    print(f"  Target:          {claim.target_entity}")
    print(f"  Category:        {claim.category}")
    print(f"  Timestamp:       {claim.timestamp}")
    print(f"  Nonce:           {claim.nonce[:16]}…\n")

    # --- Step 3: Export compact JSON (what you'd send to the chain) ---
    print("--- Compact JSON for On-Chain Posting ---")
    print(f"  {claim.to_json()[:120]}…\n")

    # --- Step 4: Verify signature (simulates reading from chain) ---
    sig_result = verify_onchain_receipt(
        commitment_hash=claim.commitment_hash,
        signature=claim.signature,
        public_key_hex=claim.public_key,
    )
    icon = "✅" if sig_result.valid else "❌"
    print(f"--- Signature Verification ---")
    print(f"  {icon} {sig_result.details}\n")

    # --- Step 5: Selective disclosure — verifier checks commitment ---
    match = verify_commitment(
        claim_details="My council tax was sent to enforcement without any human review of the specific facts.",
        timestamp=claim.timestamp,
        nonce=claim.nonce,
        public_key_hex=claim.public_key,
        expected_hash=claim.commitment_hash,
    )
    icon = "✅" if match else "❌"
    print(f"--- Commitment Verification (Selective Disclosure) ---")
    print(f"  {icon} Commitment {'matches' if match else 'does not match'} the disclosed details.\n")

    print("=== Done. In production, step 3 would post to BurgessClaimsRegistry on an EVM L2. ===")


if __name__ == "__main__":
    main()
