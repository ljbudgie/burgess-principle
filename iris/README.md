# Iris — AI Companion for the Burgess Principle

Iris is the conversational AI interface for the Burgess Principle, hosted at [burgess-principle.vercel.app](https://burgess-principle.vercel.app).

It helps users apply the binary test, generate personalised templates, walk through the Sovereign Personal Vault, and create or verify on-chain claims — all while keeping control and data sovereignty with the user.

---

## How It Works

Iris is a lightweight chat interface powered by:

- A static frontend (`index.html`) with a clean, modern chat UI.
- A Vercel serverless function (`api/chat.py`) that proxies requests to an OpenAI-compatible API.
- A system prompt (`iris/system-prompt.md`) that grounds every response in the Burgess Principle.

The system prompt includes the full project philosophy, binary test, template references, Vault guidance, on-chain protocol, tone, and privacy guardrails.

---

## Deployment

Iris runs in two modes — cloud and sovereign (local).

### Cloud Mode (Vercel)

Iris is deployed on [Vercel](https://vercel.com) as a serverless application.

### Environment Variables

Set these in the Vercel project settings:

| Variable | Required | Description |
|---|---|---|
| `IRIS_API_KEY` | Yes | API key for the AI model (e.g. xAI, OpenAI, Anthropic) |
| `IRIS_BASE_URL` | No | Base URL for the API (default: `https://api.x.ai/v1`) |
| `IRIS_MODEL` | No | Model name (default: `grok-3`) |

### Local Development

```bash
# Set environment variables
export IRIS_API_KEY="your-api-key"
export IRIS_BASE_URL="https://api.x.ai/v1"
export IRIS_MODEL="grok-3"

# Install dependencies
pip install openai

# Run the Vercel dev server (requires Vercel CLI)
npx vercel dev
```

### Sovereign Mode (Local)

Sovereign Mode runs Iris entirely on your own hardware using a local GGUF model — no API keys, no cloud, no telemetry. See **[SOVEREIGN_MODE.md](../SOVEREIGN_MODE.md)** for full setup instructions.

```bash
bash scripts/install-linux.sh   # or install-macos.sh / install-windows.ps1
python3 iris-local.py
```

The same `index.html` serves both modes — it auto-detects localhost and routes API calls to the local server. Configuration lives in `iris-config.json`.

---

## Local-First Architecture

Iris is **local-first by design**. Conversations remain entirely in the user's browser unless the user explicitly sends a message that requires the backend for model inference. Nothing is stored server-side by default.

```
┌──────────────────────────────────────────────────────────┐
│                     User's Browser                       │
│                                                          │
│  index.html ─── Chat UI (vanilla HTML/CSS/JS)            │
│       │                                                  │
│       ├── Conversation history (in-memory, client-side)  │
│       ├── Export conversation (local download only)       │
│       └── Clear chat (wipes in-memory state)             │
│                                                          │
│  ┌────────────────────────────────────────────────────┐   │
│  │  🛡️  All state lives here. Nothing leaves without  │   │
│  │     explicit user action (pressing Send).          │   │
│  └────────────────────────────────────────────────────┘   │
└────────────────────┬─────────────────────────────────────┘
                     │  Only when user sends a message
                     ▼
         ┌───────────────────────┐
         │   Vercel Serverless   │
         │    api/chat.py        │
         │                       │
         │  • Loads system prompt│
         │  • Forwards messages  │
         │  • Streams response   │
         │  • No storage         │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   AI Model (Grok)     │
         │   via OpenAI API      │
         └───────────────────────┘
```

### Data flow

1. Conversation history is held **in-memory in the browser only**.
2. When the user presses Send, the current message (plus conversation context) is sent to `/api/chat`.
3. The serverless function adds the system prompt and forwards to the AI model.
4. The response streams back via Server-Sent Events.
5. **No data is persisted on any server.** The serverless function is stateless.
6. Users can export their conversation locally as Markdown, or clear chat to wipe all state.

---

## Privacy

Iris keeps everything on your hardware by default — **sovereign by design**.

- **Local-first:** All conversation history stays in your browser. Nothing is stored on any server unless you explicitly send a message for model processing.
- **Minimal data transfer:** Only the current conversation context is sent to the backend. Full claim details never leave your device.
- **No server-side storage:** The serverless function is stateless — it processes and forgets.
- **User-controlled export:** You can download your conversation as a Markdown file locally. No cloud upload.
- **On-chain commitments only:** If using on-chain claims, only cryptographic fingerprints (hash + signature) are posted. No personal data touches the blockchain.
- **No tracking, no cookies, no analytics.**

---

## Example Conversations

See the [`examples/`](examples/) folder for sample interactions showing how Iris helps with:

- Applying the binary test to a real situation.
- Generating a personalised letter from a template.
- Explaining the Sovereign Personal Vault.

---

**The Burgess Principle**
UK Certification Mark: UK00004343685
[github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
