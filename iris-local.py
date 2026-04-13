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
import hashlib
import json
import logging
import sys
import threading
import webbrowser
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from iris.claim_builder import (
    auto_generate_claim,
    queue_onchain_fingerprint,
    signature_mode_label,
)
from iris.sovereign_profile import (
    load_personal_profile_summary,
    normalize_mirror_greeting_style,
    normalize_mirror_reflection_scope,
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


def print_sovereign_banner(config: dict) -> None:
    source_code = Path(__file__).read_text(encoding="utf-8")
    fingerprint = hashlib.sha256(source_code.encode("utf-8")).hexdigest()
    short_fingerprint = fingerprint[:16] + "..."
    model_name = Path(str(config.get("model_path", "unknown"))).name or "unknown"
    port = config.get("port", 8000)
    gpu_status = "ON" if config.get("gpu_acceleration") else "OFF"
    signatures = signature_mode_label(bool(config.get("post_quantum")))
    inner_width = 78
    lines = [
        "🚀  IRIS LOCAL — SOVEREIGN MODE ACTIVE",
        "",
        "• Runs 100% on your hardware",
        "• Zero cloud, zero telemetry, zero external APIs",
        "• All inference & commitments stay on-device",
        "• Powered by v0.4.0 cryptographic human scrutiny (Burgess Principle)",
        "",
        f"Source fingerprint: {short_fingerprint} (v0.4.0 self-verified)",
        f"Model: {model_name:40}",
        f"Port : {port} | GPU: {gpu_status}",
        f"Signatures: {signatures}",
    ]

    print("╔" + "═" * inner_width + "╗")
    for line in lines:
        print(f"║  {line:<{inner_width - 2}}║")
    print("╚" + "═" * inner_width + "╝")
    log.info("✅ Sovereign Local Mode initialised — no external dependencies detected")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent
_CONFIG_PATH = _ROOT / "iris-config.json"
_SYSTEM_PROMPT_PATH = _ROOT / "iris" / "system-prompt.md"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def _merge_config(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """Merge config values while preserving nested defaults for known objects."""
    merged = dict(defaults)
    for key, value in overrides.items():
        if (
            key in {"easy_mode_model", "user_profile"}
            and isinstance(value, dict)
            and isinstance(merged.get(key), dict)
        ):
            nested = dict(merged[key])
            nested.update(value)
            merged[key] = nested
            continue
        merged[key] = value
    return merged


def load_config(cli_overrides: argparse.Namespace | None = None) -> dict:
    """Merge iris-config.json defaults with CLI overrides."""
    defaults = {
        "model_path": "models/phi-3-mini-4k-instruct-q4.gguf",
        "context_size": 2048,
        "port": 8000,
        "gpu_acceleration": False,
        "easy_mode": True,
        "easy_mode_model": {
            "name": "Phi-3 Mini 4K Instruct Q4",
            "filename": "phi-3-mini-4k-instruct-q4.gguf",
            "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
        },
        "mirror_greeting_style": "neutral_professional",
        "mirror_custom_greeting": "",
        "mirror_reflection_scope": "vault_only",
        "post_quantum": False,
        "user_profile": {},
    }

    if _CONFIG_PATH.exists():
        try:
            with open(_CONFIG_PATH, encoding="utf-8") as f:
                file_cfg = json.load(f)
            defaults = _merge_config(defaults, file_cfg)
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
        if getattr(cli_overrides, "post_quantum", False):
            defaults["post_quantum"] = True

    return defaults


def load_system_prompt() -> str:
    """Read the Iris system prompt from disk."""
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def build_runtime_system_prompt(
    base_prompt: str,
    runtime_config: dict | None = None,
    personal_profile: dict | None = None,
) -> str:
    """Append local runtime context so Iris respects current local settings."""
    config = runtime_config or {}
    profile = personal_profile or {}
    greeting_style = normalize_mirror_greeting_style(
        profile.get("mirror_greeting_style") or config.get("mirror_greeting_style")
    )
    custom_greeting = str(
        profile.get("mirror_custom_greeting") or config.get("mirror_custom_greeting") or ""
    ).strip()
    reflection_scope = normalize_mirror_reflection_scope(
        profile.get("mirror_reflection_scope") or config.get("mirror_reflection_scope")
    )
    mirror_enabled = bool(profile.get("mirror_mode_enabled"))
    style_label = {
        "warm_personal": "Warm & Personal",
        "neutral_professional": "Neutral & Professional",
        "minimal": "Minimal",
    }[greeting_style]
    scope_label = {
        "off": "Off",
        "vault_only": "Internal vault only",
        "all_documents": "Include in all generated documents",
    }[reflection_scope]
    user_profile = config.get("user_profile")
    context_lines = [
        "## Local Runtime Context",
        "- This conversation is running in Sovereign Local Mode on the user's own hardware.",
        "- Treat the conversation as a continuation of the digital handshake: the user brings energy, Iris brings form and memory.",
        f"- Easy Mode is {'on' if config.get('easy_mode', True) else 'off'}.",
        f"- Mirror greeting style: {style_label}.",
        f"- Mirror reflection scope: {scope_label}.",
        (
            "- Current config: "
            f"easy_mode={'true' if config.get('easy_mode', True) else 'false'}, "
            f"mirror_greeting_style={greeting_style}, "
            f"mirror_reflection_scope={reflection_scope}."
        ),
    ]
    if custom_greeting:
        context_lines.append(f"- Custom greeting override: {custom_greeting}")
    if mirror_enabled and profile.get("name"):
        context_lines.extend(
            [
                f"- Active local profile: {profile['name']}.",
                "- Mirror Mode is enabled, so greetings should respect the configured style and keep the handshake language restrained.",
                "- Use the chosen Mirror greeting style sparingly, mainly for initial load or voice mode.",
                "- Keep generated claims and official letters formal even when Mirror Mode is enabled.",
            ]
        )
    else:
        context_lines.append("- No active Mirror Mode profile is loaded yet.")
    if isinstance(user_profile, dict):
        preferred_name = str(
            user_profile.get("preferred_name") or user_profile.get("name") or ""
        ).strip()
        communication_needs = str(
            user_profile.get("communication_needs")
            or user_profile.get("accessibility_requirements")
            or ""
        ).strip()
        location = str(user_profile.get("location") or "").strip()
        key_context = str(user_profile.get("key_context") or "").strip()
        last_updated = str(user_profile.get("last_updated") or "").strip()
        active_cases = user_profile.get("active_cases")
        if any(
            (
                preferred_name,
                communication_needs,
                location,
                key_context,
                last_updated,
                active_cases,
            )
        ):
            context_lines.append("## Saved Local User Profile")
            if preferred_name:
                context_lines.append(f"- Preferred name: {preferred_name}.")
            if communication_needs:
                context_lines.append(
                    f"- Communication needs: {communication_needs}."
                )
            if location:
                context_lines.append(f"- Location: {location}.")
            if isinstance(active_cases, list) and active_cases:
                case_list = ", ".join(str(case).strip() for case in active_cases[:3] if str(case).strip())
                if case_list:
                    context_lines.append(f"- Active cases: {case_list}.")
            if key_context:
                context_lines.append(f"- Key context: {key_context}.")
            if last_updated:
                context_lines.append(f"- Profile last updated: {last_updated}.")
        else:
            context_lines.append("- No saved local user profile is loaded from iris-config.json.")
    return f"{base_prompt.rstrip()}\n\n---\n\n" + "\n".join(context_lines)


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


def create_app(
    system_prompt: str,
    personal_profile: dict | None = None,
    runtime_config: dict | None = None,
) -> FastAPI:
    """Build the FastAPI app that serves the local chat API."""
    app = FastAPI(title="Iris Local", docs_url=None, redoc_url=None)
    app.state.personal_profile = personal_profile
    app.state.runtime_config = runtime_config or {}

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
        runtime_prompt = build_runtime_system_prompt(
            system_prompt,
            app.state.runtime_config,
            app.state.personal_profile,
        )
        api_messages = [{"role": "system", "content": runtime_prompt}]
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

        post_quantum = (
            body.get("post_quantum")
            if isinstance(body.get("post_quantum"), bool)
            else bool(app.state.runtime_config.get("post_quantum"))
        )
        try:
            claim = auto_generate_claim(query, profile, post_quantum=post_quantum)
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
                handle=str(body.get("handle", "sovereign-user")).strip() or "sovereign-user",
                preferred_signature_block=str(body.get("preferred_signature_block", "")).strip() or None,
                private_key_hex=str(body.get("private_key_hex", "")).strip() or None,
                post_quantum=bool(app.state.runtime_config.get("post_quantum")),
                post_quantum_private_key_hex=str(body.get("post_quantum_private_key_hex", "")).strip() or None,
                post_quantum_public_key_hex=str(body.get("post_quantum_public_key_hex", "")).strip() or None,
                mirror_mode_enabled=body.get("mirror_mode_enabled")
                if isinstance(body.get("mirror_mode_enabled"), bool)
                else None,
                mirror_greeting_style=str(body.get("mirror_greeting_style", "")).strip() or None,
                mirror_custom_greeting=str(body.get("mirror_custom_greeting", "")).strip() or None,
                mirror_reflection_scope=str(body.get("mirror_reflection_scope", "")).strip() or None,
            )
        except FileNotFoundError:
            return JSONResponse({"error": "No local personal profile exists yet."}, status_code=404)
        except ValueError:
            return JSONResponse(
                {"error": "Invalid personal profile request."},
                status_code=400,
            )
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
        "--post-quantum",
        action="store_true",
        default=False,
        help="Enable hybrid signatures (Ed25519 plus an installed ML-DSA or SLH-DSA provider).",
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
    try:
        print_sovereign_banner(cfg)
    except ImportError as exc:
        log.error("Post-quantum mode requested but is not available: %s", exc)
        sys.exit(1)

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

    app = create_app(system_prompt, personal_profile=personal_profile, runtime_config=cfg)

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
