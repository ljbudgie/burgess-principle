"""Hosted Iris MCP server: a remote connector anyone can add to Claude.

Served by Vercel at https://burgess-principle.vercel.app/api/connector using the
MCP streamable HTTP transport. It exposes the same six tools as the local
server in ``iris_mcp.py``.

The endpoint is stateless and read-only. Each request is answered on its own;
nothing a caller sends is stored by this code. Register lookups return
organisation-level fields only, exactly as in the local server.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mcp.server.transport_security import TransportSecuritySettings  # noqa: E402

from iris_mcp import mcp as iris  # noqa: E402

MCP_PATH = "/api/connector"

# Requests arrive through public Vercel domains, so the localhost-only
# DNS-rebinding guard is replaced with an explicit list of allowed hosts.
ALLOWED_HOSTS = [
    "burgess-principle.vercel.app",
    "*.vercel.app",
    "localhost:*",
    "127.0.0.1:*",
]


def _build_app():
    return iris.streamable_http_app(
        streamable_http_path=MCP_PATH,
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=ALLOWED_HOSTS,
            allowed_origins=[],
        ),
    )


async def app(scope, receive, send):
    """ASGI entry point for Vercel.

    Serverless hosts do not reliably send ASGI lifespan events, and the MCP
    session manager must be running before a request is handled. In stateless
    mode each request stands alone, so build the app and run its lifespan
    around every request.
    """
    if scope["type"] == "lifespan":
        message = await receive()
        while message["type"] != "lifespan.shutdown":
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            message = await receive()
        await send({"type": "lifespan.shutdown.complete"})
        return
    starlette_app = _build_app()
    async with starlette_app.router.lifespan_context(starlette_app):
        await starlette_app(scope, receive, send)
