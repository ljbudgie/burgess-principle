#!/usr/bin/env python3
"""Generate VAPID key pair for Web Push notifications.

Usage:
    python scripts/generate-vapid-keys.py

Outputs base64url-encoded keys suitable for .env / Vercel environment
variables.  Uses the Web Crypto-compatible P-256 (prime256v1) curve.

Dependencies:
    pip install cryptography   (or use PyNaCl — but P-256 is standard for VAPID)
"""

from __future__ import annotations

import base64
import sys

try:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import (
        Encoding,
        NoEncryption,
        PublicFormat,
        PrivateFormat,
    )
except ImportError:
    print(
        "Error: 'cryptography' package is required.\n"
        "Install with:  pip install cryptography",
        file=sys.stderr,
    )
    sys.exit(1)


def _b64url(data: bytes) -> str:
    """Encode bytes to unpadded base64url."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def main() -> None:
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Raw 32-byte private scalar
    private_numbers = private_key.private_numbers()
    private_bytes = private_numbers.private_value.to_bytes(32, byteorder="big")

    # Uncompressed 65-byte public point (0x04 || x || y)
    public_bytes = private_key.public_key().public_bytes(
        Encoding.X962, PublicFormat.UncompressedPoint
    )

    print("Add these to your .env or Vercel environment variables:\n")
    print(f"VAPID_PUBLIC_KEY={_b64url(public_bytes)}")
    print(f"VAPID_PRIVATE_KEY={_b64url(private_bytes)}")
    print(f'VAPID_EMAIL=mailto:your-contact@example.com')
    print(
        "\nThe VAPID_PUBLIC_KEY also goes into your client-side code "
        "(it is safe to embed in the HTML)."
    )


if __name__ == "__main__":
    main()
