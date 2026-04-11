"""Lightweight FastAPI wrapper for the Burgess Principle Binary Test.

Start the server::

    uvicorn api:app --reload

Then POST to ``/verify``::

    curl -X POST http://127.0.0.1:8000/verify \
         -H "Content-Type: application/json" \
         -d '{"reasoning_text": "...", "provided_hash": "..."}'

Or POST to ``/claims/verify`` to verify an on-chain claim receipt::

    curl -X POST http://127.0.0.1:8000/claims/verify \
         -H "Content-Type: application/json" \
         -d '{"commitment_hash": "...", "signature": "...", "public_key_hex": "..."}'

Requires the ``api`` optional dependency group::

    pip install -e ".[api]"
"""

from __future__ import annotations

import sys
import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

from verify_scrutiny import verify_instrument

app = FastAPI(
    title="Burgess Principle Binary Test",
    description="SOVEREIGN / NULL verification API with optional on-chain claims support.",
    version="1.1.1",
)


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class VerifyRequest(BaseModel):
    """Payload for the /verify endpoint."""

    reasoning_text: str = Field(
        ..., min_length=1, description="The reasoning text to verify."
    )
    provided_hash: str = Field(
        ...,
        min_length=64,
        max_length=64,
        pattern=r"^[0-9a-fA-F]{64}$",
        description="The expected SHA-256 hex-digest (Sovereign Hash).",
    )


class VerifyResponse(BaseModel):
    """Structured result returned by the /verify endpoint."""

    status: str
    code: int
    description: str


class ClaimVerifyRequest(BaseModel):
    """Payload for the /claims/verify endpoint."""

    commitment_hash: str = Field(
        ...,
        min_length=64,
        max_length=64,
        pattern=r"^[0-9a-fA-F]{64}$",
        description="The SHA-256 commitment hash (64 hex characters).",
    )
    signature: str = Field(
        ...,
        min_length=128,
        max_length=128,
        pattern=r"^[0-9a-fA-F]{128}$",
        description="The Ed25519 signature (128 hex characters / 64 bytes).",
    )
    public_key_hex: str = Field(
        ...,
        min_length=64,
        max_length=64,
        pattern=r"^[0-9a-fA-F]{64}$",
        description="The claimant's Ed25519 public key (64 hex characters).",
    )


class ClaimVerifyResponse(BaseModel):
    """Structured result returned by the /claims/verify endpoint."""

    valid: bool
    commitment_hash: str
    public_key: str
    details: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/verify", response_model=VerifyResponse)
def verify(payload: VerifyRequest) -> VerifyResponse:
    """Run the Burgess Principle Binary Test and return a structured result."""
    result = verify_instrument(payload.reasoning_text, payload.provided_hash)
    data = result.to_dict()
    return VerifyResponse(**data)


@app.post("/claims/verify", response_model=ClaimVerifyResponse)
def verify_claim(payload: ClaimVerifyRequest) -> ClaimVerifyResponse:
    """Verify an on-chain Burgess Claim receipt (Ed25519 signature check).

    This endpoint checks that the Ed25519 signature over the commitment
    hash is valid for the given public key.  It does **not** interact with
    any blockchain — it performs the same cryptographic verification that
    would be done off-chain after reading the claim from a contract.
    """
    # Lazy import to keep PyNaCl optional.
    sdk_path = os.path.join(os.path.dirname(__file__), "onchain-protocol", "sdk")
    if sdk_path not in sys.path:
        sys.path.insert(0, sdk_path)

    from onchain_claims import verify_onchain_receipt

    result = verify_onchain_receipt(
        commitment_hash=payload.commitment_hash,
        signature=payload.signature,
        public_key_hex=payload.public_key_hex,
    )
    return ClaimVerifyResponse(
        valid=result.valid,
        commitment_hash=result.commitment_hash,
        public_key=result.public_key,
        details=result.details,
    )
