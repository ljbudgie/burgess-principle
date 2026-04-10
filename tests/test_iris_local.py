"""Tests for iris-local.py — the sovereign local inference server.

These tests cover configuration loading, system prompt loading,
CLI argument parsing, and the FastAPI app endpoints.
Model loading and actual inference are mocked.
"""

import argparse
import importlib.util
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Module-level import — load iris-local.py by path (it's not a package)
# ---------------------------------------------------------------------------
_MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "iris-local.py")
_spec = importlib.util.spec_from_file_location("iris_local", _MODULE_PATH)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

load_config = _mod.load_config
load_system_prompt = _mod.load_system_prompt
parse_args = _mod.parse_args
create_app = _mod.create_app
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
        assert cfg["model_path"] == "models/model.gguf"
        assert cfg["context_size"] == 2048
        assert cfg["port"] == 8000
        assert cfg["gpu_acceleration"] is False

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

    def test_cli_overrides_config_file(self, tmp_path):
        """CLI arguments take priority over config file."""
        config_file = tmp_path / "iris-config.json"
        config_file.write_text(json.dumps({"port": 9090}))
        args = argparse.Namespace(
            model="cli-model.gguf",
            context=4096,
            port=7777,
            gpu=True,
        )
        with patch.object(_mod, "_CONFIG_PATH", config_file):
            cfg = load_config(args)
        assert cfg["model_path"] == "cli-model.gguf"
        assert cfg["context_size"] == 4096
        assert cfg["port"] == 7777
        assert cfg["gpu_acceleration"] is True

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
        args = argparse.Namespace(model=None, context=None, port=None, gpu=False)
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
        assert args.no_browser is False

    def test_all_flags(self):
        args = parse_args([
            "--model", "test.gguf",
            "--context", "4096",
            "--port", "9000",
            "--gpu",
            "--no-browser",
        ])
        assert args.model == "test.gguf"
        assert args.context == 4096
        assert args.port == 9000
        assert args.gpu is True
        assert args.no_browser is True


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
        assert api_messages[0]["content"] == self.system_prompt
        user_assistant_msgs = [m for m in api_messages if m["role"] != "system"]
        assert len(user_assistant_msgs) == 2
        assert user_assistant_msgs[0] == {"role": "user", "content": "Hello"}
        assert user_assistant_msgs[1] == {"role": "assistant", "content": "Hi there"}


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
        assert "Iris" in response.text
