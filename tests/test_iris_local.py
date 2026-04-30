"""Tests for iris-local.py — the sovereign local inference server.

These tests cover configuration loading, system prompt loading,
CLI argument parsing, and the FastAPI app endpoints.
Model loading and actual inference are mocked.
"""

import argparse
import html
import importlib.util
import json
import os
import runpy
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_MOCK_CLAIM_DATA = {"letter": "# Letter", "commitment_hash": "abc123"}
_MOCK_PROFILE_SUMMARY = {
    "name": "Alex",
    "handle": "sovereign-user",
    "preferred_signature_block": "Alex [Burgess Principle]",
    "key_fingerprint": "abc123def4567890",
    "public_key_hex": "ab" * 32,
    "profile_signature": "cd" * 64,
    "signature_mode": "classical",
    "post_quantum_algorithm": "",
    "post_quantum_public_key_hex": "",
    "signed_at": "2026-04-11T20:45:15+00:00",
    "mirror_mode_enabled": True,
    "mirror_mode_activated_at": "2026-04-11T21:00:00+00:00",
    "mirror_greeting_style": "neutral_professional",
    "mirror_custom_greeting": "",
    "mirror_reflection_scope": "vault_only",
    "mirror_greeting": "Alex — Mirror Mode active. The handshake continues on this device.",
}

# ---------------------------------------------------------------------------
# Module-level import — load iris-local.py by path (it's not a package)
# ---------------------------------------------------------------------------
_MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "iris-local.py")
_spec = importlib.util.spec_from_file_location("iris_local", _MODULE_PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

load_config = _mod.load_config
load_system_prompt = _mod.load_system_prompt
load_model = _mod.load_model
parse_args = _mod.parse_args
create_app = _mod.create_app
build_runtime_system_prompt = _mod.build_runtime_system_prompt
main = _mod.main
_ROOT = _mod._ROOT
_CONFIG_PATH = _mod._CONFIG_PATH
_SYSTEM_PROMPT_PATH = _mod._SYSTEM_PROMPT_PATH


# ---------------------------------------------------------------------------
# load_system_prompt
# ---------------------------------------------------------------------------
class TestLoadSystemPrompt:
    def test_returns_string(self):
        prompt = load_system_prompt()
        assert isinstance(prompt, str)

    def test_prompt_is_non_empty(self):
        prompt = load_system_prompt()
        assert len(prompt.strip()) > 0

    def test_prompt_mentions_iris(self):
        prompt = load_system_prompt()
        assert "Iris" in prompt

    def test_prompt_mentions_burgess_principle(self):
        prompt = load_system_prompt()
        assert "Burgess Principle" in prompt


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------
class TestLoadConfig:
    def test_defaults_without_config_file(self, tmp_path):
        """When iris-config.json doesn't exist, defaults are used."""
        with patch.object(_mod, "_CONFIG_PATH", tmp_path / "nonexistent.json"):
            cfg = load_config()
        assert cfg["model_path"] == "models/phi-3-mini-4k-instruct-q4.gguf"
        assert cfg["context_size"] == 2048
        assert cfg["port"] == 8000
        assert cfg["gpu_acceleration"] is False
        assert cfg["easy_mode"] is True
        assert cfg["mirror_greeting_style"] == "neutral_professional"
        assert cfg["mirror_reflection_scope"] == "vault_only"
        assert cfg["post_quantum"] is False

    def test_reads_config_file(self, tmp_path):
        """Values from iris-config.json override defaults."""
        config_file = tmp_path / "iris-config.json"
        config_file.write_text(json.dumps({
            "model_path": "custom/model.gguf",
            "port": 9090,
        }))
        with patch.object(_mod, "_CONFIG_PATH", config_file):
            cfg = load_config()
        assert cfg["model_path"] == "custom/model.gguf"
        assert cfg["port"] == 9090
        # Defaults preserved for unset values
        assert cfg["context_size"] == 2048
        assert cfg["gpu_acceleration"] is False
        assert cfg["easy_mode"] is True

    def test_nested_user_profile_defaults_are_preserved(self, tmp_path):
        config_file = tmp_path / "iris-config.json"
        config_file.write_text(
            json.dumps(
                {
                    "user_profile": {
                        "preferred_name": "Alex",
                        "communication_needs": "Email only",
                    }
                }
            )
        )
        with patch.object(_mod, "_CONFIG_PATH", config_file):
            cfg = load_config()
        assert cfg["user_profile"]["preferred_name"] == "Alex"
        assert cfg["user_profile"]["communication_needs"] == "Email only"

    def test_cli_overrides_config_file(self, tmp_path):
        """CLI arguments take priority over config file."""
        config_file = tmp_path / "iris-config.json"
        config_file.write_text(json.dumps({"port": 9090}))
        args = argparse.Namespace(
            model="cli-model.gguf",
            context=4096,
            port=7777,
            gpu=True,
            post_quantum=True,
        )
        with patch.object(_mod, "_CONFIG_PATH", config_file):
            cfg = load_config(args)
        assert cfg["model_path"] == "cli-model.gguf"
        assert cfg["context_size"] == 4096
        assert cfg["port"] == 7777
        assert cfg["gpu_acceleration"] is True
        assert cfg["post_quantum"] is True

    def test_invalid_json_uses_defaults(self, tmp_path):
        """Malformed config file falls back to defaults."""
        config_file = tmp_path / "iris-config.json"
        config_file.write_text("not valid json {{{")
        with patch.object(_mod, "_CONFIG_PATH", config_file):
            cfg = load_config()
        assert cfg["port"] == 8000

    def test_cli_none_values_do_not_override(self, tmp_path):
        """CLI args set to None don't override config file values."""
        config_file = tmp_path / "iris-config.json"
        config_file.write_text(json.dumps({"port": 5555}))
        args = argparse.Namespace(model=None, context=None, port=None, gpu=False, post_quantum=False)
        with patch.object(_mod, "_CONFIG_PATH", config_file):
            cfg = load_config(args)
        assert cfg["port"] == 5555


# ---------------------------------------------------------------------------
# parse_args
# ---------------------------------------------------------------------------
class TestParseArgs:
    def test_defaults(self):
        args = parse_args([])
        assert args.model is None
        assert args.context is None
        assert args.port is None
        assert args.gpu is False
        assert args.post_quantum is False
        assert args.no_browser is False

    def test_all_flags(self):
        args = parse_args([
            "--model", "test.gguf",
            "--context", "4096",
            "--port", "9000",
            "--gpu",
            "--post-quantum",
            "--no-browser",
        ])
        assert args.model == "test.gguf"
        assert args.context == 4096
        assert args.port == 9000
        assert args.gpu is True
        assert args.post_quantum is True
        assert args.no_browser is True


class TestBuildRuntimeSystemPrompt:
    def test_includes_local_runtime_context(self):
        prompt = build_runtime_system_prompt(
            "Base prompt",
            {"easy_mode": True, "mirror_reflection_scope": "vault_only"},
            _MOCK_PROFILE_SUMMARY,
        )

        assert "Local Runtime Context" in prompt
        assert "Easy Mode is on" in prompt
        assert "Mirror greeting style: Neutral & Professional" in prompt
        assert "Current config: easy_mode=true, mirror_greeting_style=neutral_professional, mirror_reflection_scope=vault_only." in prompt
        assert "Active local profile: Alex." in prompt

    def test_includes_saved_local_user_profile_context(self):
        prompt = build_runtime_system_prompt(
            "Base prompt",
            {
                "easy_mode": True,
                "user_profile": {
                    "preferred_name": "Alex",
                    "communication_needs": "Email only, plain language",
                    "location": "London",
                    "active_cases": ["Trading 212 DSAR", "Home Office FOI"],
                    "key_context": "Deaf user requesting calm written replies.",
                    "last_updated": "2026-04-11",
                },
            },
            _MOCK_PROFILE_SUMMARY,
        )

        assert "Saved Local User Profile" in prompt
        assert "Preferred name: Alex." in prompt
        assert "Communication needs: Email only, plain language." in prompt
        assert "Active cases: Trading 212 DSAR, Home Office FOI." in prompt


# ---------------------------------------------------------------------------
# FastAPI app — endpoint tests
# ---------------------------------------------------------------------------
class TestChatEndpoint:
    """Test the /api/chat endpoint with a mocked LLM."""

    @pytest.fixture(autouse=True)
    def _setup_app(self):
        """Create a test app with a mocked LLM."""
        self.system_prompt = "You are a test assistant."
        self.app = create_app(self.system_prompt)

        # Mock the global _llm
        self.mock_llm = MagicMock()
        _mod._llm = self.mock_llm

        # Import TestClient lazily (requires httpx)
        try:
            from starlette.testclient import TestClient
            self.client = TestClient(self.app)
            self.has_client = True
        except ImportError:
            self.has_client = False

        yield

        _mod._llm = None

    def test_invalid_json(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post(
            "/api/chat",
            content=b"not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
        assert "Invalid JSON" in response.json()["error"]

    def test_empty_messages(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post("/api/chat", json={"messages": []})
        assert response.status_code == 400
        assert "No messages" in response.json()["error"]

    def test_missing_messages_key(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post("/api/chat", json={"data": "hello"})
        assert response.status_code == 400

    def test_successful_stream(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")

        self.mock_llm.create_chat_completion.return_value = iter([
            {"choices": [{"delta": {"content": "Hello"}}]},
            {"choices": [{"delta": {"content": " world"}}]},
        ])

        response = self.client.post(
            "/api/chat",
            json={"messages": [{"role": "user", "content": "Hi"}]},
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        text = response.text
        assert "Hello" in text
        assert "world" in text
        assert "[DONE]" in text

    def test_stream_skips_empty_deltas(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")

        self.mock_llm.create_chat_completion.return_value = iter([
            {"choices": [{"delta": {}}]},
            {"choices": [{"delta": {"content": "response"}}]},
        ])

        response = self.client.post(
            "/api/chat",
            json={"messages": [{"role": "user", "content": "test"}]},
        )
        assert response.status_code == 200
        assert "response" in response.text
        assert "[DONE]" in response.text

    def test_model_failure_returns_500(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")

        self.mock_llm.create_chat_completion.side_effect = RuntimeError("OOM")

        response = self.client.post(
            "/api/chat",
            json={"messages": [{"role": "user", "content": "hi"}]},
        )
        assert response.status_code == 500
        assert "inference failed" in response.json()["error"]

    def test_messages_filtering(self):
        """Only user and assistant messages with content are forwarded."""
        if not self.has_client:
            pytest.skip("starlette.testclient not available")

        self.mock_llm.create_chat_completion.return_value = iter([
            {"choices": [{"delta": {"content": "ok"}}]},
        ])

        self.client.post(
            "/api/chat",
            json={
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "system", "content": "ignored"},
                    {"role": "assistant", "content": "Hi there"},
                    {"role": "user", "content": ""},
                    {"role": "tool", "content": "ignored"},
                ]
            },
        )

        call_kwargs = self.mock_llm.create_chat_completion.call_args
        api_messages = call_kwargs.kwargs["messages"]
        assert api_messages[0]["role"] == "system"
        assert self.system_prompt in api_messages[0]["content"]
        assert "Local Runtime Context" in api_messages[0]["content"]
        user_assistant_msgs = [m for m in api_messages if m["role"] != "system"]
        assert len(user_assistant_msgs) == 2
        assert user_assistant_msgs[0] == {"role": "user", "content": "Hello"}
        assert user_assistant_msgs[1] == {"role": "assistant", "content": "Hi there"}


class TestGenerateClaimEndpoint:
    """Test the /api/generate-claim endpoint."""

    @pytest.fixture(autouse=True)
    def _setup_app(self):
        app = create_app("test prompt")
        try:
            from starlette.testclient import TestClient
            self.client = TestClient(app)
            self.has_client = True
        except ImportError:
            self.has_client = False
        yield

    def test_invalid_json(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post(
            "/api/generate-claim",
            content=b"not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
        assert "Invalid JSON" in response.json()["error"]

    def test_requires_non_empty_query(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post(
            "/api/generate-claim",
            json={"query": "   ", "profile": {}},
        )
        assert response.status_code == 400
        assert "non-empty string" in response.json()["error"]

    def test_requires_profile_object(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post(
            "/api/generate-claim",
            json={"query": "Need a letter", "profile": []},
        )
        assert response.status_code == 400
        assert "object" in response.json()["error"]

    def test_successful_response_returns_claim_and_markdown(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "auto_generate_claim", return_value=_MOCK_CLAIM_DATA) as mock_auto:
            response = self.client.post(
                "/api/generate-claim",
                json={"query": "Need a letter", "profile": {"vault_passphrase": "secret"}},
            )
        assert response.status_code == 200
        assert response.json() == {
            "claim": _MOCK_CLAIM_DATA,
            "letter_markdown": "# Letter",
        }
        mock_auto.assert_called_once_with(
            "Need a letter",
            {"vault_passphrase": "secret"},
            post_quantum=False,
        )

    def test_runtime_post_quantum_config_enables_hybrid_claims(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        app = create_app("test prompt", runtime_config={"post_quantum": True})
        from starlette.testclient import TestClient

        client = TestClient(app)
        with patch.object(_mod, "auto_generate_claim", return_value=_MOCK_CLAIM_DATA) as mock_auto:
            response = client.post(
                "/api/generate-claim",
                json={"query": "Need a letter", "profile": {"vault_passphrase": "secret"}},
            )

        assert response.status_code == 200
        mock_auto.assert_called_once_with(
            "Need a letter",
            {"vault_passphrase": "secret"},
            post_quantum=True,
        )

    def test_value_error_returns_400(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(
            _mod,
            "auto_generate_claim",
            side_effect=ValueError("profile must include vault_passphrase"),
        ):
            response = self.client.post(
                "/api/generate-claim",
                json={"query": "Need a letter", "profile": {}},
            )
        assert response.status_code == 400
        assert "vault_passphrase" in response.json()["error"]

    def test_other_value_error_returns_generic_400(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(
            _mod,
            "auto_generate_claim",
            side_effect=ValueError("bad profile data"),
        ):
            response = self.client.post(
                "/api/generate-claim",
                json={"query": "Need a letter", "profile": {}},
            )
        assert response.status_code == 400
        assert response.json()["error"] == "Invalid claim generation request."

    def test_unexpected_failure_returns_500(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(
            _mod,
            "auto_generate_claim",
            side_effect=RuntimeError("boom"),
        ):
            response = self.client.post(
                "/api/generate-claim",
                json={"query": "Need a letter", "profile": {}},
            )
        assert response.status_code == 500
        assert "Claim generation failed" in response.json()["error"]

    def test_io_failure_returns_500(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(
            _mod,
            "auto_generate_claim",
            side_effect=OSError("disk full"),
        ):
            response = self.client.post(
                "/api/generate-claim",
                json={"query": "Need a letter", "profile": {}},
            )
        assert response.status_code == 500
        assert "Claim generation failed" in response.json()["error"]


class TestQueueOnchainFingerprintEndpoint:
    @pytest.fixture(autouse=True)
    def _setup_app(self):
        app = create_app("test prompt")
        try:
            from starlette.testclient import TestClient
            self.client = TestClient(app)
            self.has_client = True
        except ImportError:
            self.has_client = False
        yield

    def test_requires_object_payload(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post("/api/queue-onchain-fingerprint", json={"fingerprint": []})
        assert response.status_code == 400
        assert response.json()["error"] == "fingerprint must be an object."

    def test_invalid_json_returns_400(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post(
            "/api/queue-onchain-fingerprint",
            content=b"not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
        assert response.json()["error"] == "Invalid JSON body."

    def test_returns_accepted_with_queue_metadata(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(
            _mod,
            "queue_onchain_fingerprint",
            return_value={"queue_id": "queued-1", "path": "/tmp/queued-1.json"},
        ) as mock_queue:
            response = self.client.post(
                "/api/queue-onchain-fingerprint",
                json={"fingerprint": {"commitment_hash": "0xproof", "signature": "0xsig", "public_key": "ab" * 32}},
            )
        assert response.status_code == 202
        assert response.json() == {
            "queued_fingerprint": {"queue_id": "queued-1", "path": "/tmp/queued-1.json"}
        }
        mock_queue.assert_called_once()

    def test_value_error_returns_400(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(
            _mod,
            "queue_onchain_fingerprint",
            side_effect=ValueError("fingerprint must include commitment_hash, signature, and public_key"),
        ):
            response = self.client.post("/api/queue-onchain-fingerprint", json={"fingerprint": {}})
        assert response.status_code == 400
        assert "commitment_hash" in response.json()["error"]

    def test_os_error_returns_500(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(
            _mod,
            "queue_onchain_fingerprint",
            side_effect=OSError(),
        ):
            response = self.client.post(
                "/api/queue-onchain-fingerprint",
                json={
                    "fingerprint": {
                        "commitment_hash": "0xproof",
                        "signature": "0xsig",
                        "public_key": "ab" * 32,
                    }
                },
            )
        assert response.status_code == 500
        assert "Fingerprint queueing failed" in response.json()["error"]


class TestMyProfileEndpoint:
    @pytest.fixture(autouse=True)
    def _setup_app(self):
        app = create_app("test prompt", personal_profile=None)
        try:
            from starlette.testclient import TestClient
            self.client = TestClient(app)
            self.has_client = True
        except ImportError:
            self.has_client = False
        yield

    def test_get_returns_loaded_summary(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        app = create_app("test prompt", personal_profile=_MOCK_PROFILE_SUMMARY)
        from starlette.testclient import TestClient

        response = TestClient(app).get("/api/my-profile")
        assert response.status_code == 200
        assert response.json() == {"profile": _MOCK_PROFILE_SUMMARY}

    def test_setup_requires_passphrase(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post("/api/my-profile/setup", json={"name": "Alex"})
        assert response.status_code == 400
        assert "vault_passphrase" in response.json()["error"]

    def test_setup_requires_name_for_first_profile(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "load_personal_profile_summary", return_value=None):
            response = self.client.post(
                "/api/my-profile/setup",
                json={"vault_passphrase": "secret"},
            )
        assert response.status_code == 400
        assert "name must be a non-empty string" in response.json()["error"]

    def test_setup_returns_profile_summary(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "load_personal_profile_summary", return_value=None), patch.object(
            _mod,
            "setup_personal_profile",
            return_value={
                "created": True,
                "stored_path": "/tmp/personal-profile.json",
                "profile": _MOCK_PROFILE_SUMMARY,
            },
        ) as mock_setup:
            response = self.client.post(
                "/api/my-profile/setup",
                json={"name": "Alex", "vault_passphrase": "secret"},
            )
        assert response.status_code == 200
        assert response.json()["created"] is True
        assert response.json()["profile"] == _MOCK_PROFILE_SUMMARY
        mock_setup.assert_called_once()
        assert mock_setup.call_args.kwargs["mirror_mode_enabled"] is None

    def test_setup_passes_mirror_mode_flag(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "load_personal_profile_summary", return_value=_MOCK_PROFILE_SUMMARY), patch.object(
            _mod,
            "setup_personal_profile",
            return_value={
                "created": False,
                "stored_path": "/tmp/personal-profile.json",
                "profile": _MOCK_PROFILE_SUMMARY,
            },
        ) as mock_setup:
            response = self.client.post(
                "/api/my-profile/setup",
                json={"vault_passphrase": "secret", "mirror_mode_enabled": True},
            )
        assert response.status_code == 200
        assert mock_setup.call_args.kwargs["mirror_mode_enabled"] is True
        assert mock_setup.call_args.kwargs["mirror_greeting_style"] is None

    def test_setup_passes_extended_mirror_preferences(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "load_personal_profile_summary", return_value=_MOCK_PROFILE_SUMMARY), patch.object(
            _mod,
            "setup_personal_profile",
            return_value={
                "created": False,
                "stored_path": "/tmp/personal-profile.json",
                "profile": _MOCK_PROFILE_SUMMARY,
            },
        ) as mock_setup:
            response = self.client.post(
                "/api/my-profile/setup",
                json={
                    "vault_passphrase": "secret",
                    "mirror_mode_enabled": True,
                    "mirror_greeting_style": "warm_personal",
                    "mirror_custom_greeting": "Welcome back, Alex.",
                    "mirror_reflection_scope": "all_documents",
                },
            )
        assert response.status_code == 200
        assert mock_setup.call_args.kwargs["mirror_greeting_style"] == "warm_personal"
        assert mock_setup.call_args.kwargs["mirror_custom_greeting"] == "Welcome back, Alex."
        assert mock_setup.call_args.kwargs["mirror_reflection_scope"] == "all_documents"

    def test_setup_rejects_invalid_json(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        response = self.client.post(
            "/api/my-profile/setup",
            content=b"not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 400
        assert response.json()["error"] == "Invalid JSON body."

    def test_setup_returns_404_when_existing_profile_disappears(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "load_personal_profile_summary", return_value=_MOCK_PROFILE_SUMMARY), patch.object(
            _mod,
            "setup_personal_profile",
            side_effect=FileNotFoundError,
        ):
            response = self.client.post(
                "/api/my-profile/setup",
                json={"vault_passphrase": "secret"},
            )
        assert response.status_code == 404
        assert response.json()["error"] == "No local personal profile exists yet."

    def test_setup_returns_generic_400_for_invalid_profile_request(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "load_personal_profile_summary", return_value=None), patch.object(
            _mod,
            "setup_personal_profile",
            side_effect=ValueError("bad profile"),
        ):
            response = self.client.post(
                "/api/my-profile/setup",
                json={"name": "Alex", "vault_passphrase": "secret"},
            )
        assert response.status_code == 400
        assert response.json()["error"] == "Invalid personal profile request."

    def test_setup_returns_500_for_io_errors(self):
        if not self.has_client:
            pytest.skip("starlette.testclient not available")
        with patch.object(_mod, "load_personal_profile_summary", return_value=None), patch.object(
            _mod,
            "setup_personal_profile",
            side_effect=OSError("disk full"),
        ):
            response = self.client.post(
                "/api/my-profile/setup",
                json={"name": "Alex", "vault_passphrase": "secret"},
            )
        assert response.status_code == 500
        assert response.json()["error"] == "Personal profile setup failed. Check the server logs for details."


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------
class TestIndexPage:
    def test_serves_index_html(self):
        app = create_app("test prompt")
        try:
            from starlette.testclient import TestClient
            client = TestClient(app)
        except ImportError:
            pytest.skip("starlette.testclient not available")

        response = client.get("/")
        assert response.status_code == 200
        unescaped = html.unescape(response.text)
        assert "Iris" in unescaped
        assert "Save to Sovereign Vault" in unescaped
        assert "Generate Commitment & Sign" in unescaped
        assert "Copy Final Letter" in unescaped
        assert "+ New Claim" in unescaped
        assert "Setup My Identity" in unescaped
        assert "Claim profile & phone settings" in unescaped
        assert "Enable Mirror Mode" in unescaped
        assert "Mirror greeting style" in unescaped
        assert "Include in all generated documents" in unescaped
        assert "voiceStatus" in response.text
        assert "manifest.json" in response.text
        assert "service-worker.js" in response.text
        assert "/api/generate-claim" in unescaped
        assert "/api/my-profile" in unescaped


# ---------------------------------------------------------------------------
# load_model
# ---------------------------------------------------------------------------
class TestLoadModel:
    """Tests for the load_model function."""

    def test_missing_model_file_exits(self, tmp_path):
        """load_model exits with code 1 when the model file does not exist."""
        cfg = {"model_path": str(tmp_path / "nonexistent.gguf")}
        with pytest.raises(SystemExit) as exc_info:
            load_model(cfg)
        assert exc_info.value.code == 1

    def test_relative_path_resolved_against_root(self, tmp_path):
        """A relative model_path is resolved relative to _ROOT."""
        model_file = _ROOT / "models" / "fake.gguf"
        cfg = {"model_path": "models/fake.gguf"}
        # Model file won't exist under _ROOT, so this should exit
        with pytest.raises(SystemExit) as exc_info:
            load_model(cfg)
        assert exc_info.value.code == 1

    def test_absolute_path_used_directly(self, tmp_path):
        """An absolute model_path is used as-is without prepending _ROOT."""
        abs_path = tmp_path / "model.gguf"
        cfg = {"model_path": str(abs_path)}
        # File doesn't exist, so it should exit
        with pytest.raises(SystemExit) as exc_info:
            load_model(cfg)
        assert exc_info.value.code == 1

    def test_successful_load_with_gpu(self, tmp_path):
        """Successful model loading with GPU acceleration enabled."""
        model_file = tmp_path / "model.gguf"
        model_file.write_bytes(b"fake model data")

        mock_llama_cls = MagicMock()
        mock_llama_instance = MagicMock()
        mock_llama_cls.return_value = mock_llama_instance

        cfg = {
            "model_path": str(model_file),
            "context_size": 4096,
            "gpu_acceleration": True,
        }
        with patch.dict("sys.modules", {"llama_cpp": MagicMock(Llama=mock_llama_cls)}):
            load_model(cfg)

        mock_llama_cls.assert_called_once_with(
            model_path=str(model_file),
            n_ctx=4096,
            n_gpu_layers=-1,
            verbose=False,
        )
        assert _mod._llm is mock_llama_instance

    def test_successful_load_without_gpu(self, tmp_path):
        """Successful model loading with GPU acceleration disabled."""
        model_file = tmp_path / "model.gguf"
        model_file.write_bytes(b"fake model data")

        mock_llama_cls = MagicMock()
        mock_llama_instance = MagicMock()
        mock_llama_cls.return_value = mock_llama_instance

        cfg = {
            "model_path": str(model_file),
            "context_size": 2048,
            "gpu_acceleration": False,
        }
        with patch.dict("sys.modules", {"llama_cpp": MagicMock(Llama=mock_llama_cls)}):
            load_model(cfg)

        mock_llama_cls.assert_called_once_with(
            model_path=str(model_file),
            n_ctx=2048,
            n_gpu_layers=0,
            verbose=False,
        )

    def test_default_context_size(self, tmp_path):
        """When context_size is missing from config, default 2048 is used."""
        model_file = tmp_path / "model.gguf"
        model_file.write_bytes(b"fake model data")

        mock_llama_cls = MagicMock()
        cfg = {"model_path": str(model_file)}
        with patch.dict("sys.modules", {"llama_cpp": MagicMock(Llama=mock_llama_cls)}):
            load_model(cfg)

        call_kwargs = mock_llama_cls.call_args
        assert call_kwargs.kwargs["n_ctx"] == 2048


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
class TestMain:
    """Tests for the main() orchestration function."""

    def test_missing_system_prompt_exits(self, tmp_path):
        """main exits with code 1 when the system prompt file is missing."""
        with patch.object(_mod, "_SYSTEM_PROMPT_PATH", tmp_path / "missing.md"):
            with pytest.raises(SystemExit) as exc_info:
                main(["--no-browser"])
            assert exc_info.value.code == 1

    def test_missing_post_quantum_provider_exits_cleanly(self):
        with patch.object(_mod, "print_sovereign_banner", side_effect=ImportError("missing PQ provider")):
            with pytest.raises(SystemExit) as exc_info:
                main(["--no-browser"])
        assert exc_info.value.code == 1

    def test_main_calls_uvicorn_run(self, tmp_path):
        """main orchestrates config → prompt → model → app → uvicorn.run."""
        mock_uvicorn_run = MagicMock()
        mock_load_model = MagicMock()

        with patch.object(_mod, "load_model", mock_load_model), \
             patch.object(_mod, "uvicorn") as mock_uvicorn:
            mock_uvicorn.run = mock_uvicorn_run
            main(["--no-browser", "--port", "9999"])

        mock_load_model.assert_called_once()
        mock_uvicorn_run.assert_called_once()
        call_kwargs = mock_uvicorn_run.call_args
        assert call_kwargs.kwargs["port"] == 9999
        assert call_kwargs.kwargs["host"] == "127.0.0.1"

    def test_browser_opens_when_not_suppressed(self):
        """Without --no-browser, a browser timer is scheduled."""
        mock_timer = MagicMock()
        mock_load_model = MagicMock()

        with patch.object(_mod, "load_model", mock_load_model), \
             patch.object(_mod, "uvicorn") as mock_uvicorn, \
             patch.object(_mod, "threading") as mock_threading:
            mock_uvicorn.run = MagicMock()
            mock_threading.Timer.return_value = mock_timer
            main([])

        mock_threading.Timer.assert_called_once()
        assert mock_threading.Timer.call_args[0][0] == 1.5
        mock_timer.start.assert_called_once()

    def test_browser_timer_callback_opens_local_url(self):
        """The scheduled callback opens the configured localhost URL."""
        mock_load_model = MagicMock()

        with patch.object(_mod, "load_model", mock_load_model), \
             patch.object(_mod, "uvicorn") as mock_uvicorn, \
             patch.object(_mod, "threading") as mock_threading, \
             patch.object(_mod, "webbrowser") as mock_webbrowser:
            mock_uvicorn.run = MagicMock()
            main(["--port", "8123"])
            _, open_browser = mock_threading.Timer.call_args[0]
            open_browser()

        mock_webbrowser.open.assert_called_once_with("http://localhost:8123")

    def test_no_browser_flag_skips_browser(self):
        """With --no-browser, no browser timer is scheduled."""
        mock_load_model = MagicMock()

        with patch.object(_mod, "load_model", mock_load_model), \
             patch.object(_mod, "uvicorn") as mock_uvicorn, \
             patch.object(_mod, "threading") as mock_threading:
            mock_uvicorn.run = MagicMock()
            main(["--no-browser"])

        mock_threading.Timer.assert_not_called()

    def test_main_passes_loaded_personal_profile_to_app(self):
        mock_load_model = MagicMock()
        mock_app = MagicMock()

        with patch.object(_mod, "load_model", mock_load_model), \
             patch.object(_mod, "load_personal_profile_summary", return_value=_MOCK_PROFILE_SUMMARY), \
             patch.object(_mod, "create_app", return_value=mock_app) as mock_create_app, \
             patch.object(_mod, "uvicorn") as mock_uvicorn:
            mock_uvicorn.run = MagicMock()
            main(["--no-browser"])

        mock_create_app.assert_called_once()
        assert mock_create_app.call_args.args[0] == load_system_prompt()
        assert mock_create_app.call_args.kwargs["personal_profile"] == _MOCK_PROFILE_SUMMARY
        assert mock_create_app.call_args.kwargs["runtime_config"]["easy_mode"] is True

    def test_module_main_guard_runs_main(self, monkeypatch, tmp_path):
        script_path = Path(__file__).resolve().parents[1] / "iris-local.py"
        model_path = tmp_path / "model.gguf"
        model_path.write_bytes(b"fake model data")
        mock_uvicorn = MagicMock()
        mock_llama_cls = MagicMock()

        monkeypatch.setattr(
            sys,
            "argv",
            ["iris-local.py", "--no-browser", "--model", str(model_path)],
        )

        with patch.dict(
            sys.modules,
            {
                "uvicorn": MagicMock(run=mock_uvicorn.run),
                "llama_cpp": MagicMock(Llama=mock_llama_cls),
            },
        ):
            runpy.run_path(str(script_path), run_name="__main__")

        mock_uvicorn.run.assert_called_once()


# ---------------------------------------------------------------------------
# /api/version + CLI flags + prompt injection (Step 6 + 7)
# ---------------------------------------------------------------------------
class TestVersionEndpoint:
    def test_returns_iris_version(self):
        from starlette.testclient import TestClient
        app = create_app("test prompt")
        response = TestClient(app).get("/api/version")
        assert response.status_code == 200
        body = response.json()
        from iris import __version__ as IRIS_VERSION
        assert body == {"version": IRIS_VERSION}


class TestCorsTightening:
    def test_default_cors_is_loopback_only(self):
        from starlette.testclient import TestClient
        app = create_app(
            "test prompt",
            runtime_config={"port": 8000, "cors_allow_all": False},
        )
        client = TestClient(app)
        # Allowed loopback origin: middleware echoes Access-Control-Allow-Origin.
        response = client.options(
            "/api/chat",
            headers={
                "Origin": "http://localhost:8000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://localhost:8000"

        # Disallowed origin: middleware does not echo it.
        response_blocked = client.options(
            "/api/chat",
            headers={
                "Origin": "https://evil.example.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        assert response_blocked.headers.get("access-control-allow-origin") != "https://evil.example.com"

    def test_cors_allow_all_opt_in(self):
        from starlette.testclient import TestClient
        app = create_app(
            "test prompt",
            runtime_config={"port": 8000, "cors_allow_all": True},
        )
        response = TestClient(app).options(
            "/api/chat",
            headers={
                "Origin": "https://lan-tablet.local",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "content-type",
            },
        )
        assert response.status_code == 200
        # Wildcard surfaces some way (either "*" or echoed origin).
        allow = response.headers.get("access-control-allow-origin")
        assert allow in {"*", "https://lan-tablet.local"}


class TestCliNewFlags:
    def test_host_flag(self):
        args = parse_args(["--host", "0.0.0.0"])
        assert args.host == "0.0.0.0"
        cfg = load_config(args)
        assert cfg["host"] == "0.0.0.0"

    def test_default_host_is_loopback(self):
        args = parse_args([])
        cfg = load_config(args)
        assert cfg["host"] == "127.0.0.1"

    def test_cors_allow_all_flag(self):
        args = parse_args(["--cors-allow-all"])
        cfg = load_config(args)
        assert cfg["cors_allow_all"] is True

    def test_config_flag_uses_alternative_path(self, tmp_path):
        alt = tmp_path / "alt-config.json"
        alt.write_text(json.dumps({"port": 9876, "host": "192.0.2.1"}))
        args = parse_args(["--config", str(alt)])
        cfg = load_config(args)
        assert cfg["port"] == 9876
        assert cfg["host"] == "192.0.2.1"


class TestPromptInjection:
    def test_inject_replaces_script_tag_content(self):
        canonical = "CANONICAL PROMPT TEXT"
        html = (
            '<html><body>'
            '<script id="iris-system-prompt" type="text/plain">__IRIS_SYSTEM_PROMPT__</script>'
            '<p>after</p></body></html>'
        )
        out = _mod._inject_system_prompt(html, canonical)
        assert canonical in out
        assert "__IRIS_SYSTEM_PROMPT__" not in out
        assert "<p>after</p>" in out

    def test_inject_is_noop_without_script_tag(self):
        html = "<html><body>no prompt tag</body></html>"
        assert _mod._inject_system_prompt(html, "X") == html

    def test_iris_html_route_serves_canonical_prompt(self, tmp_path):
        from starlette.testclient import TestClient
        canonical = "CANONICAL_FROM_TEST"
        app = create_app(canonical)
        response = TestClient(app).get("/iris.html")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        body = response.text
        # The canonical prompt is injected into the embedded script tag.
        assert canonical in body
        # The placeholder/old prompt is no longer in the served body.
        assert "__IRIS_SYSTEM_PROMPT__" not in body


class TestChatErrorSanitisation:
    def test_500_message_does_not_leak_exception_text(self):
        """A failing inference call must return a generic, safe error message."""
        from starlette.testclient import TestClient
        app = create_app("test prompt")
        mock_llm = MagicMock()
        # Use a sensitive-looking message to confirm it's not leaked.
        mock_llm.create_chat_completion.side_effect = RuntimeError(
            "secret-trace: /home/user/model.gguf failed at offset 0xDEADBEEF"
        )
        _mod._llm = mock_llm
        try:
            client = TestClient(app, raise_server_exceptions=False)
            response = client.post(
                "/api/chat",
                json={"messages": [{"role": "user", "content": "hi"}]},
            )
            assert response.status_code == 500
            body = response.json()
            assert "secret-trace" not in body["error"]
            assert "0xDEADBEEF" not in body["error"]
            assert "Model inference failed" in body["error"]
        finally:
            _mod._llm = None
