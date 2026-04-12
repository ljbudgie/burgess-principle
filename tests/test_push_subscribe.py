"""Tests for the Web Push subscription serverless handler."""

from __future__ import annotations

import importlib.util
import io
import json
import os
from pathlib import Path

from unittest.mock import patch


_MODULE_PATH = Path(__file__).resolve().parents[1] / "api" / "push-subscribe.py"
_SPEC = importlib.util.spec_from_file_location("push_subscribe", _MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)

handler = _MODULE.handler


def _make_handler(request_data: bytes) -> handler:
    instance = handler.__new__(handler)
    instance.rfile = io.BytesIO(request_data)
    instance.wfile = io.BytesIO()
    instance.requestline = ""
    instance.command = ""
    instance.request_version = "HTTP/1.1"
    instance.close_connection = True
    instance.client_address = ("127.0.0.1", 12345)
    instance._response_code = None
    instance._response_headers = {}

    def fake_send_response(code, message=None):
        instance._response_code = code

    def fake_send_header(keyword, value):
        instance._response_headers[keyword] = value

    def fake_end_headers():
        pass

    instance.send_response = fake_send_response
    instance.send_header = fake_send_header
    instance.end_headers = fake_end_headers
    return instance


class TestPushSubscribePost:
    def test_invalid_json_returns_400(self):
        request_body = b"{not-json"
        subject = _make_handler(request_body)
        subject.headers = {"Content-Length": str(len(request_body))}

        subject.do_POST()

        assert subject._response_code == 400
        assert json.loads(subject.wfile.getvalue()) == {"error": "Invalid JSON."}

    def test_missing_subscription_returns_400(self):
        request_body = json.dumps({}).encode()
        subject = _make_handler(request_body)
        subject.headers = {"Content-Length": str(len(request_body))}

        subject.do_POST()

        assert subject._response_code == 400
        assert json.loads(subject.wfile.getvalue()) == {
            "error": "Missing push subscription object."
        }

    def test_missing_subscription_endpoint_returns_400(self):
        request_body = json.dumps({"subscription": {"keys": {"auth": "token"}}}).encode()
        subject = _make_handler(request_body)
        subject.headers = {"Content-Length": str(len(request_body))}

        subject.do_POST()

        assert subject._response_code == 400
        assert json.loads(subject.wfile.getvalue()) == {
            "error": "Missing push subscription object."
        }

    def test_without_vapid_key_acknowledges_local_only_notifications(self):
        request_body = json.dumps(
            {"subscription": {"endpoint": "https://example.invalid/push/123"}}
        ).encode()
        subject = _make_handler(request_body)
        subject.headers = {"Content-Length": str(len(request_body))}

        with patch.dict(os.environ, {}, clear=True):
            subject.do_POST()

        assert subject._response_code == 200
        assert json.loads(subject.wfile.getvalue()) == {
            "ok": True,
            "note": (
                "Push subscription received but VAPID keys are not configured. "
                "Notifications will work locally only."
            ),
        }

    def test_with_vapid_key_confirms_notifications_enabled(self):
        request_body = json.dumps(
            {"subscription": {"endpoint": "https://example.invalid/push/123"}}
        ).encode()
        subject = _make_handler(request_body)
        subject.headers = {"Content-Length": str(len(request_body))}

        with patch.dict(os.environ, {"VAPID_PUBLIC_KEY": "public-key"}, clear=True):
            subject.do_POST()

        assert subject._response_code == 200
        assert json.loads(subject.wfile.getvalue()) == {
            "ok": True,
            "note": "Push subscription stored. Sovereign notifications enabled.",
        }


class TestPushSubscribeGet:
    def test_returns_empty_public_key_when_unconfigured(self):
        subject = _make_handler(b"")

        with patch.dict(os.environ, {}, clear=True):
            subject.do_GET()

        assert subject._response_code == 200
        assert json.loads(subject.wfile.getvalue()) == {"vapidPublicKey": ""}

    def test_returns_configured_public_key(self):
        subject = _make_handler(b"")

        with patch.dict(os.environ, {"VAPID_PUBLIC_KEY": "public-key"}, clear=True):
            subject.do_GET()

        assert subject._response_code == 200
        assert json.loads(subject.wfile.getvalue()) == {"vapidPublicKey": "public-key"}


def test_json_helper_sets_status_headers_and_body():
    subject = _make_handler(b"")

    subject._json(201, {"ok": True})

    assert subject._response_code == 201
    assert subject._response_headers == {"Content-Type": "application/json"}
    assert subject.wfile.getvalue() == b'{"ok": true}'
