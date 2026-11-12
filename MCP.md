# Iris MCP server

Iris is available as a [Model Context Protocol](https://modelcontextprotocol.io) server. Any MCP client, including Claude Desktop and Claude Code, can call the Burgess Principle test directly.

There are two ways to use it.

## Hosted connector (no install)

Add this address to Claude as a custom connector:

```
https://burgess-principle.vercel.app/api/connector
```

In Claude, add it as a custom connector in your connector settings. In Claude Code:

```
claude mcp add --transport http iris https://burgess-principle.vercel.app/api/connector
```

The hosted connector is read-only and stateless. It needs no account or key, and it keeps nothing you send it once it has replied. It offers the same tools as the local server.

## For agent builders

Call `human_checkpoint` before any action that could affect a person. It returns PROCEED only when you declare that no identified person is affected and the description gives no sign that one is. Anything else returns STOP: refusals, charges, enforcement, credit checks, account closures, or an action you have not classified. On STOP, pass the decision to a named human, then record their review with `assess_decision`. Proceed only if that returns SOVEREIGN.

## Local server

The local server runs on your own machine over stdio. Nothing you give it leaves your machine.

### Install

```
git clone https://github.com/ljbudgie/burgess-principle.git
cd burgess-principle
pip install -e ".[mcp]"
```

### Connect

**Claude Code:**

```
claude mcp add iris -- iris-mcp
```

**Claude Desktop:** add this to `claude_desktop_config.json` and restart:

```json
{
  "mcpServers": {
    "iris": { "command": "iris-mcp" }
  }
}
```

If `iris-mcp` is not on your path, use the full path to the Python in your environment with `"args": ["-m", "iris_mcp"]`.

## Tools

| Tool | What it does |
|---|---|
| `human_checkpoint` | Call before acting. Returns PROCEED, or STOP when a named human must decide first, with what that person must confirm. |
| `assess_decision` | Classifies a decision as SOVEREIGN, NULL or AMBIGUOUS from the reviewer's name, role, whether they reviewed the specific facts, and when. |
| `classify_correspondence` | Detects delay loops in a thread: insufficiency, circular referral, precondition stacking, template dismissal, identity loops, channel redirects. |
| `verify_reasoning_hash` | Checks that recorded reasoning still matches its SHA-256 hash. |
| `lookup_organisation` | Returns an organisation's finding and score from the institutional register. |
| `register_summary` | Counts findings across the register, by sector. |
| `certification_mark_status` | States the status of UK certification mark UK00004343685. |

It also offers one resource, `iris://framework`, a short statement of the test.

## What it does not do

- It does not return named individuals. Register lookups give organisation-level fields only (institution, sector, finding, score).
- It does not certify anyone. Certification is granted under the filed regulations; see [CERTIFICATION_MARK.md](./CERTIFICATION_MARK.md).
- Its output is advisory. A named human must confirm any finding before it is relied on or published. See [DISCLAIMER.md](./DISCLAIMER.md).
