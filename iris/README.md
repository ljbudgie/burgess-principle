# Iris — Sovereign AI Companion for the Burgess Principle

![Local-first](https://img.shields.io/badge/local--first-yes-14532d?style=flat-square)
![Voice-first](https://img.shields.io/badge/voice--first-Iris-0f766e?style=flat-square)
![Privacy](https://img.shields.io/badge/privacy-user--controlled-1d4ed8?style=flat-square)

Iris is the conversational interface for the Burgess Principle: a phone-friendly, voice-first assistant that helps users document what happened, draft calm correspondence, and preserve verifiable records without surrendering sovereignty.

It can run as:

- a hosted PWA entry point at [burgess-principle.vercel.app](https://burgess-principle.vercel.app),
- a fully local sovereign runtime on the user's own hardware,
- and, in Phase 3, an optional self-hosted coordination client for **Sovereign Hub Mode 2.0**.

> **Core rule:** Iris is **advisory only**. It helps a user prepare, organise, and verify records. It does not replace the Burgess Principle's human-review test, and it never turns AI output into an automatic **SOVEREIGN** or **NULL** finding.

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
[github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
