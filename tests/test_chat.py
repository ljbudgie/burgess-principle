"""Tests for the Iris chat Vercel serverless function (api/chat.py).

These tests cover the BaseHTTPRequestHandler-based handler, including
request parsing, error handling, CORS, and streaming responses.
"""

import importlib.util
import io
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Module-level import helpers
# ---------------------------------------------------------------------------

# The api/ directory is not a Python package (no __init__.py) and there is
# a top-level api.py that shadows the package namespace.  We load api/chat.py
# directly using importlib so we can test it in isolation.

_CHAT_MODULE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "api", "chat.py"
)
_spec = importlib.util.spec_from_file_location("api_chat", _CHAT_MODULE_PATH)
_chat_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_chat_mod)

_load_system_prompt = _chat_mod._load_system_prompt
handler = _chat_mod.handler


# ---------------------------------------------------------------------------
# _load_system_prompt
# ---------------------------------------------------------------------------

class TestLoadSystemPrompt:
    def test_returns_string(self):
        prompt = _load_system_prompt()
        assert isinstance(prompt, str)

    def test_prompt_is_non_empty(self):
        prompt = _load_system_prompt()
        assert len(prompt.strip()) > 0

    def test_prompt_mentions_iris(self):
        prompt = _load_system_prompt()
        assert "Iris" in prompt

    def test_prompt_mentions_burgess_principle(self):
        prompt = _load_system_prompt()
        assert "Burgess Principle" in prompt


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_handler(request_data: bytes) -> handler:
    """Instantiate the handler with a fake request, suppressing __init__ side effects."""
    h = handler.__new__(handler)
    h.rfile = io.BytesIO(request_data)
    h.wfile = io.BytesIO()
    h.requestline = ""
    h.command = ""
    h.request_version = "HTTP/1.1"
    h.close_connection = True
    h.client_address = ("127.0.0.1", 12345)

    # Track response status and headers
    h._response_code = None
    h._response_headers = {}

    def fake_send_response(code, message=None):
        h._response_code = code

    def fake_send_header(keyword, value):
        h._response_headers[keyword] = value

    def fake_end_headers():
        pass

    h.send_response = fake_send_response
    h.send_header = fake_send_header
    h.end_headers = fake_end_headers

    return h


# ---------------------------------------------------------------------------
# handler.do_OPTIONS — CORS preflight
# ---------------------------------------------------------------------------

class TestDoOptions:
    def test_returns_200(self):
        h = _make_handler(b"")
        h.do_OPTIONS()
        assert h._response_code == 200

    def test_cors_allow_origin(self):
        h = _make_handler(b"")
        h.do_OPTIONS()
        assert h._response_headers.get("Access-Control-Allow-Origin") == "*"

    def test_cors_allow_methods(self):
        h = _make_handler(b"")
        h.do_OPTIONS()
        assert "POST" in h._response_headers.get("Access-Control-Allow-Methods", "")
        assert "OPTIONS" in h._response_headers.get("Access-Control-Allow-Methods", "")

    def test_cors_allow_headers(self):
        h = _make_handler(b"")
        h.do_OPTIONS()
        assert "Content-Type" in h._response_headers.get("Access-Control-Allow-Headers", "")


# ---------------------------------------------------------------------------
# handler.log_message — suppression
# ---------------------------------------------------------------------------

class TestLogMessage:
    def test_log_message_does_nothing(self, capsys):
        h = _make_handler(b"")
        h.log_message("test %s", "value")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert captured.err == ""


# ---------------------------------------------------------------------------
# handler.do_POST — error paths
# ---------------------------------------------------------------------------

class TestDoPostErrors:
    def test_missing_api_key_returns_503(self):
        body = json.dumps({"messages": [{"role": "user", "content": "hello"}]}).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("IRIS_API_KEY", None)
            h.do_POST()
        assert h._response_code == 503
        data = json.loads(h.wfile.getvalue())
        assert "error" in data
        assert "IRIS_API_KEY" in data["error"]

    def test_invalid_json_returns_400(self):
        invalid_body = b"not valid json at all"
        h = _make_handler(invalid_body)
        h.headers = {"Content-Length": str(len(invalid_body))}
        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            h.do_POST()
        assert h._response_code == 400
        data = json.loads(h.wfile.getvalue())
        assert "error" in data
        assert "Invalid JSON" in data["error"]

    def test_empty_messages_returns_400(self):
        body = json.dumps({"messages": []}).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}
        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            h.do_POST()
        assert h._response_code == 400
        data = json.loads(h.wfile.getvalue())
        assert "No messages" in data["error"]

    def test_missing_messages_key_returns_400(self):
        body = json.dumps({"data": "no messages key"}).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}
        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            h.do_POST()
        assert h._response_code == 400

    def test_zero_content_length_returns_400(self):
        h = _make_handler(b"")
        h.headers = {"Content-Length": "0"}
        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            h.do_POST()
        assert h._response_code == 400

    def test_missing_content_length_defaults_to_zero(self):
        h = _make_handler(b"")
        h.headers = {}
        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            h.do_POST()
        assert h._response_code == 400


# ---------------------------------------------------------------------------
# handler.do_POST — successful streaming
# ---------------------------------------------------------------------------

class TestDoPostSuccess:
    def _make_mock_stream(self, chunks):
        """Create a mock streaming response from OpenAI."""
        mock_chunks = []
        for text in chunks:
            chunk = MagicMock()
            choice = MagicMock()
            choice.delta.content = text
            chunk.choices = [choice]
            mock_chunks.append(chunk)
        return mock_chunks

    def test_successful_stream(self):
        body = json.dumps({
            "messages": [{"role": "user", "content": "Hello"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        mock_stream = self._make_mock_stream(["Hello", " world"])
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_stream

        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        assert h._response_code == 200
        assert h._response_headers.get("Content-Type") == "text/event-stream"

        output = h.wfile.getvalue().decode()
        assert "Hello" in output
        assert "world" in output
        assert "data: [DONE]" in output

    def test_stream_with_empty_delta(self):
        """Chunks with no content should be skipped."""
        body = json.dumps({
            "messages": [{"role": "user", "content": "test"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        empty_chunk = MagicMock()
        empty_choice = MagicMock()
        empty_choice.delta.content = None
        empty_chunk.choices = [empty_choice]

        content_chunk = MagicMock()
        content_choice = MagicMock()
        content_choice.delta.content = "response"
        content_chunk.choices = [content_choice]

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = [empty_chunk, content_chunk]

        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        assert h._response_code == 200
        output = h.wfile.getvalue().decode()
        assert "response" in output
        assert "data: [DONE]" in output

    def test_stream_with_no_choices(self):
        """Chunks with empty choices list should be skipped."""
        body = json.dumps({
            "messages": [{"role": "user", "content": "test"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        no_choices_chunk = MagicMock()
        no_choices_chunk.choices = []

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = [no_choices_chunk]

        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        assert h._response_code == 200
        output = h.wfile.getvalue().decode()
        assert "data: [DONE]" in output

    def test_model_failure_returns_500(self):
        body = json.dumps({
            "messages": [{"role": "user", "content": "hello"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = RuntimeError("API down")

        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        assert h._response_code == 500
        data = json.loads(h.wfile.getvalue())
        assert "error" in data
        assert "API down" in data["error"]

    def test_messages_filtering(self):
        """Only user and assistant messages with content are forwarded."""
        body = json.dumps({
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "system", "content": "ignored"},
                {"role": "assistant", "content": "Hi there"},
                {"role": "user", "content": ""},
                {"role": "tool", "content": "ignored"},
            ]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = []

        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        call_kwargs = mock_client.chat.completions.create.call_args
        api_messages = call_kwargs.kwargs.get("messages") or call_kwargs[1].get("messages")
        assert api_messages[0]["role"] == "system"
        user_assistant_msgs = [m for m in api_messages if m["role"] != "system"]
        assert len(user_assistant_msgs) == 2
        assert user_assistant_msgs[0] == {"role": "user", "content": "Hello"}
        assert user_assistant_msgs[1] == {"role": "assistant", "content": "Hi there"}

    def test_default_model_used(self):
        """When IRIS_MODEL is not set, 'grok-3' is used."""
        body = json.dumps({
            "messages": [{"role": "user", "content": "hi"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = []

        with patch.dict(os.environ, {"IRIS_API_KEY": "test-key"}, clear=True):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        call_kwargs = mock_client.chat.completions.create.call_args
        assert call_kwargs.kwargs.get("model") == "grok-3"

    def test_custom_model_used(self):
        """IRIS_MODEL env var overrides the default model."""
        body = json.dumps({
            "messages": [{"role": "user", "content": "hi"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = []

        with patch.dict(os.environ, {"IRIS_API_KEY": "key", "IRIS_MODEL": "custom-model"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        call_kwargs = mock_client.chat.completions.create.call_args
        assert call_kwargs.kwargs.get("model") == "custom-model"

    def test_stream_cache_control_headers(self):
        """Successful stream sets Cache-Control and Connection headers."""
        body = json.dumps({
            "messages": [{"role": "user", "content": "hi"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = []

        with patch.dict(os.environ, {"IRIS_API_KEY": "key"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        assert h._response_headers.get("Cache-Control") == "no-cache"
        assert h._response_headers.get("Connection") == "keep-alive"

    def test_sse_format(self):
        """Verify SSE data lines are properly formatted."""
        body = json.dumps({
            "messages": [{"role": "user", "content": "hi"}]
        }).encode()
        h = _make_handler(body)
        h.headers = {"Content-Length": str(len(body))}

        mock_stream = self._make_mock_stream(["test-data"])
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_stream

        with patch.dict(os.environ, {"IRIS_API_KEY": "key"}):
            with patch.object(_chat_mod, "_get_client", return_value=mock_client):
                h.do_POST()

        output = h.wfile.getvalue().decode()
        lines = output.strip().split("\n\n")
        # Each SSE data line should start with "data: "
        for line in lines:
            assert line.startswith("data: ")

