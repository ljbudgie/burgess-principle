# Iris — AI Companion for the Burgess Principle

Iris is the conversational AI interface for the Burgess Principle, hosted at [burgess-principle.vercel.app](https://burgess-principle.vercel.app).

It helps users apply the binary test, generate personalised templates, walk through the Sovereign Personal Vault, create or verify on-chain claims, and optionally enable Mirror Mode in Sovereign Local Mode — all while keeping control and data sovereignty with the user.

Iris now includes a guided onboarding flow for new users, persistent user profiles, Mirror Mode-aware local identity setup, digital-handshake framing, intelligent template matching, and handling for ambiguous institutional responses.

---

## How It Works

Iris is part of a two-view single-page site powered by:

- A **landing page** with project overview, binary test visualisation, template showcase, and case study cards.
- A **chat interface** (`index.html`) with Markdown rendering and a clean, modern design.
- A Vercel serverless function (`api/chat.py`) that proxies requests to an OpenAI-compatible API.
- A system prompt (`iris/system-prompt.md`) that grounds every response in the Burgess Principle.

The landing page introduces visitors to the framework. The "Talk to Iris" CTA switches to the chat view, where Iris responses are rendered as rich Markdown (headings, bold, code blocks, tables, lists, links).

---

## Key Capabilities

### Onboarding Flow

When Iris detects a new user (no profile in `iris-config.json`), it begins a gentle six-step onboarding:

1. Introduces itself and explains that everything stays private on the user's device.
2. Asks the user's name and preferred form of address.
3. Asks about communication needs (e.g. plain language, no jargon).
4. Invites the user to describe their situation in their own words.
5. Saves the profile to `iris-config.json`.
6. Confirms the profile has been saved.

On subsequent sessions, Iris silently loads the profile and uses it without repeating the onboarding.

### Mirror Mode

In Sovereign Local Mode, users can create an encrypted personal sovereign profile, then enable **Mirror Mode** so the interface restores a local mirrored greeting and hardware-linked identity summary on startup.

Mirror Mode currently provides:

- Local identity setup with name, handle, preferred signature block, and Ed25519-backed public profile summary.
- A mirrored greeting in the welcome screen when the local profile is active, framed as a continuation of the digital handshake.
- Reuse of the local identity layer across claim/profile workflows without sending it to a cloud service.

Mirror Mode remains optional and local-only.

### Intelligent Template Matching

Iris matches the right template to the user's situation instead of presenting the full list:

| Situation described | Template suggested |
|---|---|
| Bailiffs or forced entry | Bailiff Threat |
| Automated decision, algorithm, or system | Article 22 Challenge |
| Disability or access needs ignored | Equality Act Adjustments |
| Wants to see what data is held | DSAR |
| Challenging a public body | FOI |
| Crypto exchange freeze, withdrawal hold, or source-of-funds review | Crypto Exchange Account Restriction |
| Wants to reference a hash, signature, receipt, or on-chain claim | Cryptographic Proof and On-Chain Notice |
| Wants maximum privacy with minimal disclosure | Commitment-Only Placeholder or Vault-first guidance |
| Everything else | Request for Human Review (default) |

### Handling Ambiguous Responses

Institutions don't always give clear answers. Iris helps users assess ambiguity:

- Identifies evasion patterns — templated language, redirection, non-answers.
- Asks whether a named individual confirmed personal review of the specific facts.
- Records unclear findings as **NULL (provisional)** and recommends a follow-up letter.
- Never records SOVEREIGN unless confirmed by a named individual.

### Template Discovery

Iris now mirrors the streamlined templates folder documentation:

- [`templates/README.md`](../templates/README.md) is the main template index.
- [`templates/COMMON_SCENARIOS.md`](../templates/COMMON_SCENARIOS.md) is the fast routing guide.
- Crypto and on-chain flows always stay **Vault first, commitments second**.

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

Iris's first duty is privacy — **sovereign by design**.

- **Local-first:** All conversation history stays in your browser. Nothing is stored on any server unless you explicitly send a message for model processing.
- **User profiles stay local:** The `iris-config.json` profile is stored on the user's device and never uploaded.
- **Vault before chain:** Iris always recommends the Sovereign Personal Vault before any on-chain action. Full claim details stay encrypted on the user's device.
- **Minimal data transfer:** Only the current conversation context is sent to the backend. Full claim details never leave your device.
- **No server-side storage:** The serverless function is stateless — it processes and forgets.
- **User-controlled export:** You can download your conversation as a Markdown file locally. No cloud upload.
- **On-chain commitments only:** If using on-chain claims, only cryptographic fingerprints (hash + signature) are posted. No personal data touches the blockchain.
- **No tracking, no cookies, no analytics.**

---

## Example Conversations

See the [`examples/`](examples/) folder for sample interactions showing how Iris helps with:

- Walking a new user through onboarding (`onboarding.md`).
- Applying the binary test to a real situation (`greeting.md`).
- Explaining the Sovereign Personal Vault (`vault-guidance.md`).

---

**The Burgess Principle**
UK Certification Mark: UK00004343685
[github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
