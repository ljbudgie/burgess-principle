# Iris — Sovereign Advocacy Layer for the Burgess Principle

![Local-first](https://img.shields.io/badge/local--first-yes-14532d?style=flat-square)
![Voice-first](https://img.shields.io/badge/voice--first-Iris-0f766e?style=flat-square)
![Privacy](https://img.shields.io/badge/privacy-user--controlled-1d4ed8?style=flat-square)

**Iris is not a chatbot.** It is a sovereign advocacy layer that applies the Burgess Principle binary test on behalf of any individual facing institutional power.

It requires no legal knowledge from the user. It requires no prior context. It requires only three things:

1. **What happened?**
2. **Who did it?**
3. **Were you individually considered before they did it?**

From those three answers, Iris applies the binary test, determines whether the situation is **SOVEREIGN** or **NULL**, and — where NULL — drafts the challenge, names the legal instrument, and sets the deadline. The user does not need to know the law. The user does not need to know their rights. The user does not need to know the Burgess Principle exists. Iris handles the translation from lived experience to structured challenge.

Canonical source: [github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle).

## Core framework

The behavioural and procedural rules of Iris are documented in [`core/`](./core):

- [`core/first-contact.md`](./core/first-contact.md) — the three-question intake sequence, with examples across energy, local government, consumer rights, employment, and healthcare.
- [`core/conversation-principles.md`](./core/conversation-principles.md) — how Iris speaks: lead with the answer, never flatter, correct factual errors immediately, match the user's language.
- [`core/binary-test-engine.md`](./core/binary-test-engine.md) — the six-step decision engine and the mapping from common institutional failures to specific legal routes.
- [`core/context-layers.md`](./core/context-layers.md) — Layer 1 (universal, zero context) and Layer 2 (personal, accretive). Layer 1 is always sufficient on its own.
- [`core/institutional-patterns.md`](./core/institutional-patterns.md) — the recurring patterns Iris recognises across institutional failures, with the binary test reading and recommended challenge route for each.
- [`core/sovereignty.md`](./core/sovereignty.md) — the boundary between Iris as infrastructure and the user as the decision-maker.

The canonical Iris persona prompt lives in [`./system-prompt.md`](./system-prompt.md). It inherits the repository-wide [`prompts/MASTER_PROMPT.md`](../prompts/MASTER_PROMPT.md) v1.1, which in turn inherits [`FOR_AI_MODELS.md`](../FOR_AI_MODELS.md) v3.3. That inheritance carries the Part 2 NULL declaration, the seven evasion patterns, the anti-monetisation guardrails, the Mythos routing, and the Pre-Send Self-Check into Iris without duplication. Iris itself is not a named human reviewer.

For drop-in use in any other AI assistant, paste-ready system prompts at three lengths live in [`./prompts/`](./prompts):

- [`prompts/short.md`](./prompts/short.md) — ~200 tokens, for small context windows.
- [`prompts/medium.md`](./prompts/medium.md) — ~800 tokens, for a real working session.
- [`prompts/full.md`](./prompts/full.md) — the full briefing, for long-running sessions or agents.

Iris is the conversational interface for the Burgess Principle: a phone-friendly, voice-first assistant that helps users document what happened, draft calm correspondence, and preserve verifiable records without surrendering sovereignty.

It can run as:

- a hosted PWA entry point at [burgess-principle.vercel.app](https://burgess-principle.vercel.app),
- a fully local sovereign runtime on the user's own hardware,
- and, in Phase 3, an optional self-hosted coordination client for **Sovereign Hub Mode 2.0**.

> **Core rule:** Iris is **advisory only**. It helps a user prepare, organise, and verify records. It does not replace the Burgess Principle's human-review test, and it never turns AI output into an automatic **SOVEREIGN** or **NULL** finding.

## Instant scrutiny gate

Iris should treat the Burgess question as the first packet before any draft,
claim, template, or workflow touches a person's specific facts:

> **Was a human member of the team able to personally review the specific facts of my specific situation?**

For an individual user, the zero-friction flow is:

1. Name the institution or system.
2. Name the specific action it took or proposes to take.
3. Ask whether a named human personally reviewed the specific facts before that
   action.
4. Classify the answer as **SOVEREIGN**, **NULL**, or **AMBIGUOUS**.
5. Only then draft, route, save to the Vault, or prepare a follow-up.

Copy-paste gate for any Iris-adjacent assistant:

```text
Send the Burgess SYN packet first. Before you draft or recommend any action
about my specific situation, classify whether a named human personally reviewed
my specific facts before the institution acted: SOVEREIGN / NULL / AMBIGUOUS.
If NULL, help me block, record, and escalate. If AMBIGUOUS, ask for a direct
yes/no answer plus the reviewer's name and role.
```

---

## What Iris does

Iris helps users:

- describe a situation in natural language,
- find the right template or next step,
- build claim summaries and local records,
- preserve evidence in the Sovereign Personal Vault,
- maintain long-term context in the **Verifiable Memory Palace**,
- export signed receipts when selective disclosure is needed.

---

## Phase 3 in Iris

| Capability | What Iris now adds |
| --- | --- |
| **Verifiable Memory Palace** | Long-term local memory becomes a tamper-evident ledger of encrypted entries, commitments, signatures, and Merkle roots |
| **Signed receipt export** | Iris can export a signed entry plus signed root and inclusion proof for selective disclosure |
| **Integrity verification** | Users can recompute the chain and latest root from genesis on-device |
| **Hub Mode 2.0** | Users can manually pair with a self-hosted hub, pin the hub key, and sync commitment deltas over intermittent links |
| **Audit logging** | Hub activity and derived local events can be recommitted into the Memory Palace without sending raw facts away |

---

## Sovereign Core architecture audit

The unified **Sovereign Core** strengthens the Burgess Principle by making every sensitive local action pass through shared, inspectable rules:

- **Commitment Orchestrator** keeps trigger, memory, and hub audit commitments structurally consistent so integrity checks are reproducible on-device.
- **Profile Manager** centralises connectivity, wireless minimisation, queued-sync preference, and governance toggles into one local sovereignty profile rather than scattering implicit policy across UI panels.
- **Audit Engine** standardises Merkle proofs, receipt exports, and chain verification so users can verify evidence without trusting invisible server state.
- **Connectivity-aware background behaviour** now reads the sovereignty profile before flushing queued hub work, which keeps Starlink-style intermittent links manual-first while allowing more eager background refresh on stable fiber.
- **Human review remains explicit** because the shared core only shapes local evidence handling and advisory prompts; it never upgrades AI output into a SOVEREIGN or NULL decision.

### Updated file structure overview

```text
/
├─ index.html                  # Iris shell, trigger UI, profile bridge
├─ service-worker.js           # offline shell + connectivity-aware background work
├─ phase3-memory-hub.js        # Memory Palace + Sovereign Hub integrations
├─ memory-palace-worker.js     # worker for Merkle/search offload
├─ sovereign-core/
│  ├─ types.js                 # shared sovereignty profile + settings keys
│  ├─ utils.js                 # connectivity normalisation, sync policy, presets
│  ├─ commitment-orchestrator.js
│  ├─ audit-engine.js
│  └─ profile-manager.js
└─ tests/
   └─ sovereign_core.test.mjs  # focused coverage for the shared sovereign core
```

---

## Verifiable Memory Palace

### Simple explanation

Iris no longer has to rely on opaque, server-side "memory." In Sovereign Local Mode, it can keep a **private local ledger** where each memory is:

- encrypted on the device,
- committed with SHA-256,
- chained to the previous memory,
- signed with Ed25519,
- rolled into a Merkle root,
- and exportable as a selective-disclosure receipt.

That means a user can later prove:

- *this entry existed,*
- *it belonged to this signed set,*
- *and the set has not been silently rewritten,*

without exposing everything else they stored.

### Merkle roots and inclusion proofs

**Analogy:**  
Imagine sealing each note in an envelope, then creating a master seal that represents the whole stack. An inclusion proof is the small set of seals you need to prove one envelope belonged to that stack.

**Technical view:**  
Iris hashes memory commitments into a Merkle tree. The signed root represents the full set. A receipt can include the sibling hashes needed to recompute the root for one entry, proving set membership without revealing other entries.

### Why this matters for the Burgess Principle

- A benefits claimant can prove a key timeline note was preserved without disclosing unrelated history.
- A disabled user can share the exact access-failure record needed for an advocate.
- A rights-mapping workflow can produce calm, inspectable receipts instead of asking people to trust black-box memory.
- A maintainer or reviewer can verify integrity without treating AI output as authority.

### Human accountability, strengthened

The ledger improves evidence quality, not decision authority:

- **Human review is still the standard**
- **AI remains advisory**
- **Receipts improve auditability**
- **Selective disclosure reduces over-sharing**
- **Local verification resists invisible revision**

---

## Sovereign Hub Mode 2.0

Sovereign Hub Mode 2.0 is Iris's optional coordination layer for users who want continuity across their own infrastructure.

### What it is

- **Optional**
- **Manual-first**
- **Self-hosted**
- **Digest-first**
- **Built for intermittent links**

By default, the example hub stores **commitment digests** such as memory roots, claim commitments, and trigger heads — not raw private Memory Palace content.

### Setup overview

1. Run Iris locally: `python3 iris-local.py`
2. Start the example hub in [`../sovereign-hub-example/`](../sovereign-hub-example/)
3. Open `GET /api/hub/hello`
4. Verify the returned `public_key_hex`
5. Paste the pairing JSON into Iris
6. Enter the shared secret
7. Push or pull commitments manually

### Starlink / intermittent links

Hub Mode 2.0 is designed so connectivity problems do not collapse sovereignty:

- failed sync requests are queued locally,
- local Memory Palace work continues without the hub,
- retry happens later when the link returns,
- foreground workflows still work on platforms with weaker background execution.

### Connectivity & personal environmental preferences

#### Sovereignty and Burgess audit

- **Human review remains final:** Iris can help the user record and review connectivity choices, but it does not decide whether a specific setup is the right adjustment for a specific person.
- **Local-first remains intact:** raw notes, claim context, and Memory Palace content stay on-device unless the user exports a signed receipt.
- **User control stays explicit:** Hub Mode settings, trigger presets, and Memory Palace notes are opt-in and can be exported later as signed receipts for human review.
- **No medical claim:** the feature is described as **user-configured frequency balancing**, **personal environmental preferences**, or **reasonable adjustments**, not a treatment promise.
- **Transparent sync boundaries:** Hub Mode still sends lightweight commitment material first — not the user's private timeline by default.

Iris can now frame multiple hardwired choices for local review:

| Profile | What Iris records | Why a user may choose it |
| --- | --- | --- |
| **Fiber Hardwired** | ONT, Ethernet path, Wi‑Fi state, sync preference, environmental notes | Lowest-local-RF “gold standard” where infrastructure exists |
| **Starlink Hardwired** | Bypass mode, Ethernet path, dish placement, queued sync windows | Useful in remote areas while keeping indoor wireless reduced |
| **Other** | Fixed wireless after hardwiring, or legacy DSL/cable kept Ethernet-first | Practical fallback where fiber is unavailable |

Practical tips:

- **Starlink hardwired:** use **bypass mode** where available, prefer **Ethernet**, and place the dish outside primary living areas where practical.
- **Fiber hardwired:** keep the **ONT** on a stable wired path and continue with pure **Ethernet** after the ONT.
- **Other links:** hardwire from fixed-wireless outdoor units where possible, or keep DSL/cable routers Ethernet-first and reduce unnecessary radios.
- **Hub sync:** prefer **manual / queued syncs** so Iris stays offline-first and only opens short sync windows when needed.

> **Important:** Iris presents this as a **personal environmental preference** and an **assistive configuration option**. It does not make direct health or treatment claims.

#### Suggested local review notes

When a user changes connectivity setup, Iris can recommit a Memory Palace note containing:

- connectivity profile (`starlink-hardwired`, `fiber-hardwired`, `other`),
- whether Ethernet was used,
- whether local Wi-Fi was disabled,
- whether sync stayed queued/manual,
- a short user note about comfort, focus, usability, or voice workflow.

Starter local trigger presets now include:

- **Fiber hardwired review**
- **Connectivity profile check-in (Starlink vs Fiber)**
- **Environmental note on wired setup**

See [`../sovereign-hub-example/README.md`](../sovereign-hub-example/README.md) and [`../SOVEREIGN_MODE.md`](../SOVEREIGN_MODE.md).

---

## Deployment modes

### Cloud Mode

The hosted experience runs on Vercel and provides the fastest entry point.
Its hosted API surface is intentionally narrow: `api/chat.py` provides the stateless chat relay and `api/push-subscribe.py` handles optional hosted push setup, while the richer sovereignty-first `/api/*` routes are exposed by `iris-local.py`.

#### Environment variables

| Variable | Required | Description |
| --- | --- | --- |
| `IRIS_API_KEY` | Yes | API key for the AI model |
| `IRIS_BASE_URL` | No | Base URL for the API (default: `https://api.x.ai/v1`) |
| `IRIS_MODEL` | No | Model name (default: `grok-3`) |

### Sovereign Local Mode

Sovereign Local Mode runs Iris entirely on the user's own hardware using a local GGUF model.

```bash
bash scripts/install-linux.sh   # or install-macos.sh / install-windows.ps1
python3 iris-local.py
```

The same `index.html` serves both modes; local mode auto-routes API calls to the local server when running on localhost. Configuration lives in [`../iris-config.json`](../iris-config.json).

#### CLI flags

| Flag | Default | Purpose |
| --- | --- | --- |
| `--port <n>` | `8000` | Port for the local server. |
| `--host <addr>` | `127.0.0.1` | Interface to bind to. The default is loopback only; pass `0.0.0.0` only if you intentionally want a LAN device (e.g. a tablet) to reach Iris on a network you trust. |
| `--config <path>` | `./iris-config.json` | Use an alternative config file. Useful for tests and multi-profile setups. |
| `--model <path>` | from config | Override the GGUF model path. |
| `--context <n>` | from config | Context window size. |
| `--gpu` | off | Enable GPU acceleration (requires a compatible llama-cpp-python build). |
| `--cors-allow-all` | off | Opt back into the legacy `*` CORS wildcard. By default CORS is restricted to `http://localhost:<port>` and `http://127.0.0.1:<port>` because the server binds to loopback. |
| `--no-browser` | — | Don't auto-open the browser at startup. |
| `--post-quantum` | off | Sign with a hybrid classical + post-quantum signature. |

#### Local API surface

In addition to the sovereign vault and claim-builder routes documented elsewhere, the local server exposes:

- `POST /api/chat` — streaming Server-Sent Events (`text/event-stream`) of token deltas from the local model. Returns `{ "error": "Model inference failed. Check the server logs for details." }` with HTTP 500 on inference failure (the underlying exception class and message are deliberately not leaked to the client; they are written to the server log via `log.exception`).
- `GET /api/version` — returns `{ "version": "<iris.__version__>" }`. Used by the PWA footer to display the running build.

The server also serves `iris.html` and `index.html` and re-injects the canonical system prompt from [`./system-prompt.md`](./system-prompt.md) into the embedded `<script id="iris-system-prompt" type="text/plain">…</script>` block on each first read so the local UI cannot drift from the canonical prompt.

#### Streaming, Stop, and conversation export

The PWA in `iris.html`:

- **Streams** replies into the chat bubble as Server-Sent Events arrive (works against the Cloudflare proxy, the local server, Anthropic, and OpenAI/OpenAI-compatible endpoints). If `ReadableStream` isn't available, it falls back to non-streaming JSON.
- **Stop button** replaces Send while a reply is being generated. It calls `AbortController.abort()`; any partial text that already arrived is preserved with a `_[stopped]_` marker.
- **Conversation toolbar** (top-right) lets you start a new conversation, export the current conversation as `.md` or `.json`, or copy Iris's last reply to the clipboard. Everything happens in-browser; nothing is uploaded.
- **Backend errors** (401/403/429/5xx) are now rendered as a distinct system notice with a "Try again" button rather than spoken in Iris's voice.

---

## Architecture

Iris is local-first by design.

```text
User device
├─ PWA / chat UI
├─ local profile + vault state
├─ Memory Palace ledger
├─ receipt export
└─ optional local model runtime
        │
        ├─ Cloud Mode only: stateless API relay for model inference
        └─ Optional Hub Mode 2.0: self-hosted commitment sync
```

Key implementation points:

- the browser/UI keeps conversational state local by default,
- the local runtime can maintain the Memory Palace and verify it from genesis,
- the hub path is optional and explicit,
- raw Memory Palace content does not need to be sent to the hub.

For the broader Phase 3 design, see [`../ARCHITECTURE.md`](../ARCHITECTURE.md).

---

## Privacy and data boundaries

### Sovereign Local Mode

In Sovereign Local Mode:

- Memory Palace entries stay on-device unless exported,
- the user controls when a signed receipt leaves the device,
- hub sync is opt-in and can remain commitment-only,
- no analytics, cookies, or mandatory cloud account are required.

### Cloud Mode

In Cloud Mode:

- the conversation sent for model inference goes through the serverless backend,
- the backend is stateless,
- no conversation history is stored server-side by default.

### Constant principle

Whichever mode is used, Iris should make the user's situation **more reviewable**, not more opaque.

---

## Where to go next

- Run full local setup: [`../SOVEREIGN_MODE.md`](../SOVEREIGN_MODE.md)
- Review Phase 3 architecture: [`../ARCHITECTURE.md`](../ARCHITECTURE.md)
- Explore the project overview: [`../README.md`](../README.md)
- Self-host the hub: [`../sovereign-hub-example/README.md`](../sovereign-hub-example/README.md)

---

**The Burgess Principle**  
UK Certification Mark: UK00004343685  
Author: Lewis James Burgess, Darlington, UK.  
Contact: lewisjames@theburgessprinciple.com  
[github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
