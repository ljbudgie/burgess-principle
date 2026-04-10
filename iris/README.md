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

---

## Architecture

```
index.html          →  Chat UI (vanilla HTML/CSS/JS)
api/chat.py         →  Vercel serverless function (Python)
iris/system-prompt.md →  System prompt (loaded at runtime)
```

The frontend sends user messages to `/api/chat`, which:
1. Loads the system prompt from `iris/system-prompt.md`.
2. Sends the conversation to the configured AI model.
3. Streams the response back to the frontend via Server-Sent Events.

---

## Privacy

- Iris helps create sovereign claims. Your full facts remain in your local Vault.
- On-chain posts contain only cryptographic commitments.
- No persistent user data storage without explicit consent.
- Conversation history exists only in the browser session and is not stored server-side.

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
