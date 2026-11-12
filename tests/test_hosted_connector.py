"""Tests for the hosted Iris MCP connector (api/connector.py)."""

import asyncio
import importlib.util
import json
from pathlib import Path

import pytest

pytest.importorskip("mcp")
httpx = pytest.importorskip("httpx")

ROOT = Path(__file__).resolve().parent.parent
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "1"},
    },
}


def _load_connector():
    spec = importlib.util.spec_from_file_location("hosted_connector", ROOT / "api" / "connector.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _post(body, host="burgess-principle.vercel.app"):
    connector = _load_connector()

    async def run():
        transport = httpx.ASGITransport(app=connector.app)
        async with httpx.AsyncClient(transport=transport, base_url=f"https://{host}") as client:
            return await client.post(connector.MCP_PATH, json=body, headers=HEADERS)

    return asyncio.run(run())


def test_initialize_works_without_lifespan_events():
    response = _post(INIT)
    assert response.status_code == 200
    assert response.json()["result"]["serverInfo"]["name"] == "iris"


def test_lists_the_six_tools():
    response = _post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    assert response.status_code == 200
    names = {tool["name"] for tool in response.json()["result"]["tools"]}
    assert names == {
        "assess_decision",
        "classify_correspondence",
        "verify_reasoning_hash",
        "lookup_organisation",
        "register_summary",
        "certification_mark_status",
    }


def test_register_lookup_has_no_personal_columns():
    response = _post({
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {"name": "lookup_organisation", "arguments": {"name": "E.ON"}},
    })
    text = json.dumps(response.json())
    assert "Key_Reference" not in text
    assert '\\"Status\\"' not in text
    assert "@gmail" not in text.lower()


def test_unknown_host_is_rejected():
    assert _post(INIT, host="evil.example").status_code == 421
