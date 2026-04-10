"""Lightweight FastAPI wrapper for the Burgess Principle Binary Test.

Start the server::

    uvicorn api:app --reload

Then POST to ``/verify``::

    curl -X POST http://127.0.0.1:8000/verify \
         -H "Content-Type: application/json" \
         -d '{"reasoning_text": "...", "provided_hash": "..."}'

Requires the ``api`` optional dependency group::

    pip install -e ".[api]"
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from verify_scrutiny import verify_instrument

app = FastAPI(
    title="Burgess Principle Binary Test",
    description="SOVEREIGN / NULL verification API.",
    version="0.1.0",
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


# ---------------------------------------------------------------------------
# Endpoint
# ---------------------------------------------------------------------------

@app.post("/verify", response_model=VerifyResponse)
def verify(payload: VerifyRequest) -> VerifyResponse:
    """Run the Burgess Principle Binary Test and return a structured result."""
    result = verify_instrument(payload.reasoning_text, payload.provided_hash)
    data = result.to_dict()
    return VerifyResponse(**data)
