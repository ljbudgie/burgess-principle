#!/usr/bin/env python3
"""Iris Local — sovereign inference server.

Runs Iris entirely on the user's own hardware using llama-cpp-python.
No data leaves the device. No cloud dependency. No telemetry.

Usage:
    python iris-local.py
    python iris-local.py --model models/mistral-7b-instruct.gguf
    python iris-local.py --port 9000 --gpu
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
import webbrowser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from iris.claim_builder import auto_generate_claim, queue_onchain_fingerprint
from iris.sovereign_profile import (
    load_personal_profile_summary,
    setup_personal_profile,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("iris-local")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent
_CONFIG_PATH = _ROOT / "iris-config.json"
_SYSTEM_PROMPT_PATH = _ROOT / "iris" / "system-prompt.md"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def load_config(cli_overrides: argparse.Namespace | None = None) -> dict:
    """Merge iris-config.json defaults with CLI overrides."""
    defaults = {
        "model_path": "models/model.gguf",
        "context_size": 2048,
        "port": 8000,
        "gpu_acceleration": False,
    }

    if _CONFIG_PATH.exists():
        try:
            with open(_CONFIG_PATH, encoding="utf-8") as f:
                file_cfg = json.load(f)
            defaults.update(file_cfg)
        except (json.JSONDecodeError, OSError) as exc:
            log.warning("Could not read %s: %s — using defaults.", _CONFIG_PATH, exc)

    if cli_overrides is not None:
        if cli_overrides.model:
            defaults["model_path"] = cli_overrides.model
        if cli_overrides.context:
            defaults["context_size"] = cli_overrides.context
        if cli_overrides.port:
            defaults["port"] = cli_overrides.port
        if cli_overrides.gpu:
            defaults["gpu_acceleration"] = True

    return defaults


def load_system_prompt() -> str:
    """Read the Iris system prompt from disk."""
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------
_llm = None  # module-level handle, set once


def load_model(cfg: dict):
    """Load the GGUF model via llama-cpp-python."""
    global _llm  # noqa: PLW0603

    model_path = Path(cfg["model_path"])
    if not model_path.is_absolute():
        model_path = _ROOT / model_path

    if not model_path.exists():
        log.error(
            "Model file not found: %s\n"
            "Download a GGUF model and place it at the configured path.\n"
            "See SOVEREIGN_MODE.md for instructions.",
            model_path,
        )
        sys.exit(1)

    log.info("Loading model: %s", model_path)

    from llama_cpp import Llama  # noqa: WPS433

    n_gpu_layers = -1 if cfg.get("gpu_acceleration") else 0
    _llm = Llama(
        model_path=str(model_path),
        n_ctx=cfg.get("context_size", 2048),
        n_gpu_layers=n_gpu_layers,
        verbose=False,
    )
    log.info("Model loaded successfully.")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------


def create_app(system_prompt: str, personal_profile: dict | None = None) -> FastAPI:
    """Build the FastAPI app that serves the local chat API."""
    app = FastAPI(title="Iris Local", docs_url=None, redoc_url=None)
    app.state.personal_profile = personal_profile

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    # Serve static files (index.html and assets) from project root
    # Mount after API routes so /api/chat takes priority
    @app.post("/api/chat")
    async def chat(request: Request):
        """Local inference endpoint — mirrors the Vercel API contract."""
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON body."}, status_code=400)

        messages = body.get("messages", [])
        if not messages:
            return JSONResponse(
                {"error": "No messages provided."}, status_code=400
            )

        # Build message list with system prompt
        api_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role in ("user", "assistant") and content:
                api_messages.append({"role": role, "content": content})

        try:
            stream = _llm.create_chat_completion(
                messages=api_messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True,
            )

            def generate():
                for chunk in stream:
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    token = delta.get("content")
                    if token:
                        yield f"data: {json.dumps({'content': token})}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(
                generate(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                },
            )
        except Exception:
            return JSONResponse(
                {"error": "Model inference failed. Check the server logs for details."},
                status_code=500,
            )

    @app.post("/api/generate-claim")
    async def generate_claim(request: Request):
        """Generate a sovereign local claim package from a user query and profile."""
        try:
            body = await request.json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JSONResponse({"error": "Invalid JSON body."}, status_code=400)

        query = body.get("query")
        profile = body.get("profile")
        if not isinstance(query, str) or not query.strip():
            return JSONResponse(
                {"error": "query must be a non-empty string."}, status_code=400
            )
        if not isinstance(profile, dict):
            return JSONResponse({"error": "profile must be an object."}, status_code=400)

        try:
            claim = auto_generate_claim(query, profile)
        except ValueError as exc:
            error = (
                "profile must include vault_passphrase."
                if "vault_passphrase" in str(exc)
                else "Invalid claim generation request."
            )
            return JSONResponse({"error": error}, status_code=400)
        except OSError:
            log.exception("Claim generation failed for local query due to an I/O error.")
            return JSONResponse(
                {"error": "Claim generation failed. Check the server logs for details."},
                status_code=500,
            )
        except RuntimeError:
            log.exception("Claim generation failed for local query due to a runtime error.")
            return JSONResponse(
                {"error": "Claim generation failed. Check the server logs for details."},
                status_code=500,
            )

        return JSONResponse(
            {
                "claim": claim,
                "letter_markdown": claim["letter"],
            }
        )

    @app.post("/api/queue-onchain-fingerprint")
    async def queue_onchain_claim_fingerprint(request: Request):
        """Queue a minimal fingerprint package for privacy-first background posting."""
        try:
            body = await request.json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JSONResponse({"error": "Invalid JSON body."}, status_code=400)

        fingerprint = body.get("fingerprint")
        if not isinstance(fingerprint, dict):
            return JSONResponse(
                {"error": "fingerprint must be an object."},
                status_code=400,
            )

        try:
            queued = queue_onchain_fingerprint(fingerprint)
        except ValueError:
            return JSONResponse(
                {"error": "fingerprint must include commitment_hash, signature, and public_key"},
                status_code=400,
            )
        except OSError:
            log.exception("Fingerprint queueing failed due to an I/O error.")
            return JSONResponse(
                {"error": "Fingerprint queueing failed. Check the server logs for details."},
                status_code=500,
            )

        return JSONResponse({"queued_fingerprint": queued}, status_code=202)

    @app.get("/api/my-profile")
    async def get_my_profile():
        """Return the auto-loaded public sovereign profile summary."""
        return JSONResponse({"profile": app.state.personal_profile})

    @app.post("/api/my-profile/setup")
    async def setup_my_profile(request: Request):
        """Create or load the sovereign personal profile stored in the local vault."""
        try:
            body = await request.json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JSONResponse({"error": "Invalid JSON body."}, status_code=400)

        vault_passphrase = str(body.get("vault_passphrase", "")).strip()
        if not vault_passphrase:
            return JSONResponse(
                {"error": "vault_passphrase must be a non-empty string."},
                status_code=400,
            )

        existing_profile = load_personal_profile_summary()
        name = str(body.get("name", "")).strip()
        if existing_profile is None and not name:
            return JSONResponse(
                {"error": "name must be a non-empty string when creating a new profile."},
                status_code=400,
            )

        try:
            result = setup_personal_profile(
                vault_passphrase=vault_passphrase,
                name=name or None,
                handle=str(body.get("handle", "ljbudgie")).strip() or "ljbudgie",
                preferred_signature_block=str(body.get("preferred_signature_block", "")).strip() or None,
                private_key_hex=str(body.get("private_key_hex", "")).strip() or None,
            )
        except FileNotFoundError:
            return JSONResponse({"error": "No local personal profile exists yet."}, status_code=404)
        except ValueError as exc:
            return JSONResponse({"error": str(exc)}, status_code=400)
        except OSError:
            log.exception("Personal profile setup failed due to an I/O error.")
            return JSONResponse(
                {"error": "Personal profile setup failed. Check the server logs for details."},
                status_code=500,
            )

        app.state.personal_profile = result["profile"]
        return JSONResponse(result)

    # Serve index.html at root
    @app.get("/")
    async def serve_index():
        index_path = _ROOT / "index.html"
        content = index_path.read_bytes()
        return StreamingResponse(
            iter([content]),
            media_type="text/html",
        )

    # Serve static assets from the project root (banner.png, robots.txt, etc.)
    app.mount("/", StaticFiles(directory=str(_ROOT)), name="static")

    return app


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Iris Local — sovereign AI inference for the Burgess Principle",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to a GGUF model file (overrides iris-config.json)",
    )
    parser.add_argument(
        "--context",
        type=int,
        default=None,
        help="Context window size in tokens (default: 2048)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port for the local server (default: 8000)",
    )
    parser.add_argument(
        "--gpu",
        action="store_true",
        default=False,
        help="Enable GPU acceleration (requires compatible llama-cpp-python build)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        default=False,
        help="Don't open the browser automatically",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Load config, load model, start server."""
    args = parse_args(argv)
    cfg = load_config(args)

    # Load system prompt
    if not _SYSTEM_PROMPT_PATH.exists():
        log.error("System prompt not found: %s", _SYSTEM_PROMPT_PATH)
        sys.exit(1)

    system_prompt = load_system_prompt()
    log.info("System prompt loaded (%d chars).", len(system_prompt))

    # Load model
    load_model(cfg)

    # Create app
    personal_profile = load_personal_profile_summary()
    if personal_profile:
        log.info(
            "Loaded sovereign profile for %s (%s).",
            personal_profile["name"],
            personal_profile["key_fingerprint"],
        )
    else:
        log.info("No sovereign personal profile found yet. Use Setup My Identity to create one.")

    app = create_app(system_prompt, personal_profile=personal_profile)

    port = cfg["port"]

    # Open browser after a short delay
    if not args.no_browser:

        def _open_browser():
            webbrowser.open(f"http://localhost:{port}")

        threading.Timer(1.5, _open_browser).start()

    log.info("Starting Iris Local on http://localhost:%d", port)
    log.info("Press Ctrl+C to stop.")

    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


if __name__ == "__main__":
    main()
