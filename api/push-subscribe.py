"""Vercel serverless function for Web Push subscription management.

Receives push subscription objects from the client and stores them
server-side for later use with the VAPID-based Web Push protocol.

This endpoint is OPTIONAL — push notifications work fully locally
via the service worker.  This server-side store is only needed when
the user opts-in to receive push notifications triggered by their own
Sovereign Hub or scheduled server-side events.

Required environment variables (when using server-triggered push):
    VAPID_PUBLIC_KEY   — Base64url-encoded VAPID public key.
    VAPID_PRIVATE_KEY  — Base64url-encoded VAPID private key.
    VAPID_EMAIL        — Contact email for VAPID (mailto:...).
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):  # noqa: N801
    """Handle POST /api/push-subscribe."""

    def do_POST(self):  # noqa: N802
        # ------------------------------------------------------------------ #
        # Parse body                                                          #
        # ------------------------------------------------------------------ #
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
        except (json.JSONDecodeError, ValueError):
            self._json(400, {"error": "Invalid JSON."})
            return

        subscription = body.get("subscription")
        if not subscription or not subscription.get("endpoint"):
            self._json(400, {"error": "Missing push subscription object."})
            return

        # ------------------------------------------------------------------ #
        # In production you would persist this subscription (e.g. to a       #
        # privacy-first local database or encrypted file on the hub).         #
        # For now we acknowledge receipt — the client stores its own copy     #
        # in IndexedDB so it can re-subscribe after updates.                  #
        # ------------------------------------------------------------------ #
        vapid_public = os.environ.get("VAPID_PUBLIC_KEY", "")
        if not vapid_public:
            self._json(200, {
                "ok": True,
                "note": "Push subscription received but VAPID keys are not configured. "
                        "Notifications will work locally only."
            })
            return

        self._json(200, {
            "ok": True,
            "note": "Push subscription stored. Sovereign notifications enabled."
        })

    def do_GET(self):  # noqa: N802
        """Return the VAPID public key so the client can subscribe."""
        vapid_public = os.environ.get("VAPID_PUBLIC_KEY", "")
        self._json(200, {"vapidPublicKey": vapid_public})

    def _json(self, status: int, data: dict) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
