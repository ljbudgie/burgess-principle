# ECOSYSTEM — Burgess Principle

The Burgess Principle is the **core standard**. The surrounding repositories implement, apply, or integrate it. This document maps the full technical ecosystem and how each component relates to the others.

- **Framework version:** v2.5.1 (released 31 May 2026)
- **Canonical source:** [github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
- **Last updated:** 9 May 2026

---

> **Companion documents:** this file maps the *sibling repositories* and hosted
> services around this one. [NAVIGATION.md](./NAVIGATION.md) routes readers to
> the right entry point inside the repository. [TIERS.md](./TIERS.md) maps the
> tiers within it.

---

## 1. Ecosystem map

```
                          ┌────────────────────────────────────────┐
                          │            burgess-principle           │
                          │  Core: binary test, certification mark │
                          │       UK00004343685, statutory         │
                          │       integrations, templates          │
                          └────────────────┬───────────────────────┘
                                           │ defines the standard
                ┌──────────────────────────┼────────────────────────────┐
                │                          │                            │
         ┌───────▼────────┐        ┌────────▼─────────┐         ┌────────▼─────────┐
         │      Iris      │        │     OpenHear     │         │  Nexus AI Hub    │
         │ AI implementation│      │  Sovereign audio │         │ Intelligence layer│
         │ Federation proto │      │  pipeline (HA)   │         │                  │
         │ iris-gate.vercel │      │ Phonak Naída M70 │         │                  │
         │            .app  │      │ Signia Insio 7AX │         │                  │
         └───────┬──────────┘      └──────────────────┘         └──────────────────┘
                 │
                 ├──── uses local identity reflection from ────┐
                 │                                             │
                 │                                  ┌──────────▼─────────┐
                 │                                  │       Mirror       │
                 │                                  │ local sovereign    │
                 │                                  │ identity layer     │
                 │                                  │ ljbudgie/Mirror    │
                 │                                  └────────────────────┘
                 │
                 │ integrates with / proposes integration to
                 │
    ┌────────────▼─────────────┐                  ┌────────────────────────────┐
   │  OpenClaw (upstream)     │                  │  Hermes Agent (upstream)   │
   │  openclaw/openclaw       │                  │  NousResearch/hermes-agent │
   │  PR #68692 — adopted as  │                  │  PR #12265 — integration   │
   │  governance framework    │                  │  proposed (additive)       │
   │  (working fork:          │                  │  (working fork:            │
   │   ljbudgie/openclaw)     │                  │   ljbudgie/hermes-agent)   │
   └──────────────────────────┘                  └────────────────────────────┘
```

---

## 2. Core

### `ljbudgie/burgess-principle`

- **Role:** Canonical source for the Burgess Principle standard.
- **Defines:**
  - the binary test ("Was the individual considered as an individual human being, or were they processed as a unit within a system?"),
  - the SOVEREIGN / NULL / AMBIGUOUS resolution model,
  - statutory integration with UK GDPR Article 22, Equality Act 2010 ss. 20 and 29, contract law, FOIA 2000, and consumer protection law,
  - templates, schemas, and the Iris reference implementation,
  - the licensing tiers governed by the certification mark UK00004343685.

Every other component in the ecosystem applies, implements, or integrates this standard.

---

## 3. Implementation layers

### Iris — AI implementation layer

- **Repository:** [github.com/ljbudgie/Iris](https://github.com/ljbudgie/Iris)
- **Deployment:** [iris-gate.vercel.app](https://iris-gate.vercel.app)
- **Role:** The flagship voice-first sovereign AI companion that operationalises the binary test in daily use.
- **Federation protocol:** Iris implements a federation protocol so that sovereign nodes can exchange commitments, signed receipts, and Merkle roots without surrendering local control.
- **Relationship to core:** Direct implementation of the Burgess Principle as advisory-only software with local cryptographic proof.

### Mirror — local sovereign identity layer

- **Repository:** [github.com/ljbudgie/Mirror](https://github.com/ljbudgie/Mirror)
- **Renamed from:** `Mirror-`.
- **Role:** Local identity-reflection layer for Mirror Mode, including encrypted sovereign profile reuse, mirrored greetings, and user-controlled reflection settings.
- **Relationship to core:** Supports Iris and Sovereign Local Mode without changing the Burgess test; it preserves local user control and keeps identity context advisory rather than authoritative.

### OpenHear — sovereign audio pipeline

- **Repository:** [github.com/ljbudgie/openhear](https://github.com/ljbudgie/openhear)
- **Role:** A sovereign audio pipeline for hearing aid users — extends the Burgess Principle into the audio accessibility layer so that processed sound remains under the user's control.
- **Tested on:** Phonak Naída M70-SP and Signia Insio 7AX.
- **Relationship to core:** Applies the binary test at the audio-processing boundary; ensures individual review is preserved where assistive technology mediates communication.

### Advocate Companion — practical advocacy interface

- **Repository:** [github.com/ljbudgie/advocate-companion](https://github.com/ljbudgie/advocate-companion)
- **Role:** Privacy-first advocacy UI — helps people with hidden disabilities, sensory access needs, chronic conditions, and neurodivergence request reasonable adjustments in clear, calm, evidence-aware language. The screen a person can actually use during a stressful interaction: guided conversations, journal records, draft emails, escalation messages, and evidence packs.
- **Relationship to core:** The accessible front door at the human edge of the ecosystem. Turns the binary test and the letter-template logic into guided workflows while keeping sensitive state local-first and advisory-only.

### Nexus AI Hub — intelligence layer

- **Repository:** [github.com/ljbudgie/nexus-ai-hub](https://github.com/ljbudgie/nexus-ai-hub)
- **Role:** Intelligence layer for the ecosystem — coordinates higher-order reasoning across Iris instances and other components while honouring the SOVEREIGN/NULL boundary.
- **Relationship to core:** Provides the intelligence substrate that Iris and other implementations can call into without breaking the local-first, advisory-only posture.

---

## 4. Integration targets (external upstreams)

### OpenClaw

- **Upstream:** [`openclaw/openclaw`](https://github.com/openclaw/openclaw) — 73.3k forks
- **Working fork:** [`ljbudgie/openclaw`](https://github.com/ljbudgie/openclaw)
- **Pull request:** **#68692** — additive; no existing code modified.
- **Status:** OpenClaw has **adopted** the Burgess Principle as its governance framework. Endorsed by Elon Musk on 18 April 2026 as the gateway to the X API.
- **Significance:** First external upstream adoption of the Burgess Principle as a governance framework.

### Hermes Agent

- **Upstream:** [`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent) — 99.1k stars
- **Working fork:** [`ljbudgie/hermes-agent`](https://github.com/ljbudgie/hermes-agent)
- **Pull request:** **#12265** — additive; no existing code modified.
- **Status:** Integration proposed.
- **Significance:** Brings the binary test to a widely deployed agent framework.

---

## 5. Interconnection

| From | To | Via |
| --- | --- | --- |
| `burgess-principle` | All other repositories | Defines the standard, certification mark, and templates |
| Iris | `burgess-principle` | Reference implementation; consumes templates and schemas |
| Iris | Mirror | Uses the local sovereign identity layer for Mirror Mode profile and reflection behaviour |
| Mirror | `burgess-principle` | Applies the core standard to identity reflection without replacing human review |
| Iris ↔ Iris | Other Iris nodes | Federation protocol — exchanges signed receipts and Merkle roots |
| Iris | Nexus AI Hub | Calls into the intelligence layer for higher-order reasoning |
| OpenHear | Iris / `burgess-principle` | Applies the binary test at the audio boundary |
| Advocate Companion | `burgess-principle` / OpenHear / Mirror | User-facing advocacy layer — turns templates and rights mapping into guided adjustment requests and evidence packs |
| `ljbudgie/openclaw` (fork) | `openclaw/openclaw` | PR #68692 — governance adoption |
| `ljbudgie/hermes-agent` (fork) | `NousResearch/hermes-agent` | PR #12265 — integration proposal |

---

## 6. Author and governance

- **Author:** Lewis James Burgess.
- **Contact:** [contact redacted].
- **Source code licence:** MIT.
- **Standard licence:** Governed by UK Certification Mark UK00004343685; tier structure is described in [`README.md`](README.md#licensing).
