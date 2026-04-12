"""Vercel serverless function for Iris chat.

Proxies user messages to an OpenAI-compatible API with the Iris
system prompt.  Streams the response back as Server-Sent Events.

This is the narrow hosted Cloud Mode relay only.  The richer
sovereignty-first `/api/*` surface lives in `iris-local.py` when Iris
is running in Sovereign Local Mode.

Required environment variable:
    IRIS_API_KEY   — API key for the AI model.

Optional environment variables:
    IRIS_BASE_URL  — API base URL (default: https://api.x.ai/v1).
    IRIS_MODEL     — Model name  (default: grok-3).
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler
from pathlib import Path


def _load_system_prompt() -> str:
    """Read the Iris system prompt from disk."""
    prompt_path = Path(__file__).resolve().parent.parent / "iris" / "system-prompt.md"
    return prompt_path.read_text(encoding="utf-8")


# Cache the system prompt at module level (cold-start optimisation).
_SYSTEM_PROMPT = _load_system_prompt()


def _get_client():
    """Lazy-create an OpenAI client so the import is only needed at runtime."""
    # openai is listed in requirements.txt and available on Vercel.
    from openai import OpenAI  # noqa: WPS433

    api_key = os.environ.get("IRIS_API_KEY", "")
    base_url = os.environ.get("IRIS_BASE_URL", "https://api.x.ai/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


class handler(BaseHTTPRequestHandler):  # noqa: N801 — Vercel requires this name
    """Handle hosted POST /api/chat requests."""

    def _send_json(self, status: int, data: dict) -> None:
        """Write a JSON response with a consistent content type."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self):  # noqa: N802 — required method name
        # ------------------------------------------------------------------
        # Guard: API key must be configured
        # ------------------------------------------------------------------
        if not os.environ.get("IRIS_API_KEY"):
            self._send_json(
                503,
                {
                    "error": (
                        "Iris is not yet configured. "
                        "The IRIS_API_KEY environment variable must be set in the Vercel project settings. "
                        "See iris/README.md for setup instructions."
                    )
                },
            )
            return

        # ------------------------------------------------------------------
        # Parse the request body
        # ------------------------------------------------------------------
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, ValueError):
            self._send_json(400, {"error": "Invalid JSON body."})
            return

        messages = body.get("messages", [])
        if not messages:
            self._send_json(400, {"error": "No messages provided."})
            return

        # ------------------------------------------------------------------
        # Build the messages array with the system prompt
        # ------------------------------------------------------------------
        model = os.environ.get("IRIS_MODEL", "grok-3")
        api_messages = [{"role": "system", "content": _SYSTEM_PROMPT}]

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ("user", "assistant") and content:
                api_messages.append({"role": role, "content": content})

        # ------------------------------------------------------------------
        # Call the AI model and stream the response via SSE
        # ------------------------------------------------------------------
        try:
            client = _get_client()
            stream = client.chat.completions.create(
                model=model,
                messages=api_messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True,
            )

            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    data = json.dumps({"content": chunk.choices[0].delta.content})
                    self.wfile.write(f"data: {data}\n\n".encode())
                    self.wfile.flush()

            self.wfile.write(b"data: [DONE]\n\n")
            self.wfile.flush()

        except Exception:  # noqa: BLE001
            self._send_json(500, {"error": "Model request failed."})

    def do_OPTIONS(self):  # noqa: N802
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):  # noqa: A002
        """Suppress default stderr logging in serverless context."""
        pass
