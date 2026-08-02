# Iris Integration Contract

**v2.0 — August 2026**

This contract implements the Burgess Principle (UK Certification Mark
**UK00004343685**, Classes 41, 42, 45 — accepted by the UK IPO on 21 July 2026;
publication, opposition period, and registration pending; see
[`CERTIFICATION_MARK.md`](./CERTIFICATION_MARK.md) for the authoritative status).

This document defines the small, stable surface that external tools can rely on without weakening Iris's sovereignty-first model.

## Principles

- **Local-first:** integrations should prefer local files and local APIs before hosted services.
- **Advisory-only:** no integration may autonomously issue a SOVEREIGN or NULL classification. All classifications require named human attribution before becoming a certified finding.
- **Digest-first:** integrations should move commitments, receipts, and summaries before raw facts.
- **Versioned contracts:** file formats and extension packs should declare explicit schema versions.

## Versioned schemas

The following schemas are published in [`/schemas`](./schemas):

- `claim-package.v1.json`
- `memory-receipt.v1.json`
- `profile-export.v1.json`
- `commitment-bundle.v1.json`
- `sovereign-backup-bundle.v1.json`
- `extension-pack-manifest.v1.json`

## Supported local/API endpoints

### Core verification
- `POST /verify` — verify Burgess reasoning text against a SHA-256 digest.
- `POST /scrutiny/assess` — run the pre-decision Burgess gate before a system acts on an identified individual; returns SOVEREIGN, NULL, or AMBIGUOUS with the required next action.
- `POST /claims/verify` — verify an Ed25519-signed on-chain claim receipt.

### Certification verification
- `GET /certify/verify` — verify whether a named organisation holds a current
  Burgess Principle certification, and return its tier and certified scope.
  **Status: reserved — specified here, not yet implemented.** Until it ships,
  the authoritative sources are
  [`INSTITUTIONAL_REGISTER.md`](./INSTITUTIONAL_REGISTER.md) and the live
  certification page at <https://certify.theburgessprinciple.com>. A response
  must never be read as confirming that any specific decision was SOVEREIGN —
  certification records evidenced practice, not individual outcomes.

### Governance gate in production
`POST /scrutiny/assess` is the governance gate used by the OpenHear
commercial-open-source (COSS) enterprise layer for patient configuration
accountability in NHS deployments. The gate is advisory to the deploying
organisation: it surfaces the classification and the required next action, and a
named human remains accountable for the configuration change that follows. See
[`OPENHEAR_LICENSING_FRAMEWORK.md`](./OPENHEAR_LICENSING_FRAMEWORK.md) for the
licensing model that governs that layer.

### Hosted Cloud Mode helpers
- `POST /api/chat` — stateless hosted chat relay for the Vercel PWA entry point.
- `GET /api/push-subscribe` — retrieve the hosted VAPID public key when optional server-triggered push is configured.
- `POST /api/push-subscribe` — acknowledge an optional hosted push subscription for server-triggered notifications.

Hosted `/api/*` routes are intentionally narrow. Richer claim-building, profile, and queueing routes remain local-first and are exposed by `iris-local.py`.

### Sovereign Local Mode
- `POST /api/chat` — local advisory chat when Iris runs via `iris-local.py`.
- `POST /api/generate-claim` — generate a local claim package and letter markdown.
- `POST /api/queue-onchain-fingerprint` — queue a compact claim fingerprint for local-first posting flows.
- `GET /api/my-profile` — read the local sovereign profile summary.
- `POST /api/my-profile/setup` — create or update the local sovereign profile summary.

### Sovereign Hub example
- `GET /api/hub/hello` — retrieve the hub public key and basic identity metadata.
- `POST /api/sovereign-sync-v2` — exchange encrypted commitment deltas with the self-hosted hub.

## Regulatory alignment

The integration surface is designed to help a deploying organisation evidence
compliance with the following provisions. It is a technical aid, not legal
advice, and it does not by itself satisfy any statutory duty.

| Provision | What it requires | What this contract provides |
| --- | --- | --- |
| **UK GDPR Arts 22A–22D** (inserted by Data (Use and Access) Act 2025 s.80) | Safeguards for significant decisions based on solely automated processing — information, representations, human intervention, contest | `POST /scrutiny/assess` run before the system acts, producing a classification and the required next action, with named human attribution |
| **DPA 2018 ss.50A–50D** (law enforcement processing limb, inserted by DUAA 2025 s.80) | Equivalent safeguards for adverse-effect law enforcement decisions | Same gate, applied at the pre-decision boundary |
| **EU AI Act Art 14** (human oversight of high-risk AI systems) | Effective oversight by natural persons with the competence, authority, and means to intervene | Advisory-only classification plus the requirement that a named human attributes the finding before it is certified |
| **Equality Act 2010 s.20** (reasonable adjustments) | Anticipatory adjustment for disabled people | Accessible, local-first routes and the individual-review requirement at the point of configuration |

Detailed mappings: [`ADM_HUMAN_REVIEW.md`](./ADM_HUMAN_REVIEW.md),
[`EU-AI-ACT-MAPPING.md`](./EU-AI-ACT-MAPPING.md), and
[`LEGAL_MAPPING.md`](./LEGAL_MAPPING.md).

## Local file contracts

### Claim package
A generated claim package should be exported as structured JSON, with letter markdown separated from commitment metadata.

### Memory receipt
A memory receipt should contain the signed entry, signed root, leaf position metadata, and Merkle inclusion proof needed for selective disclosure.

### Sovereign backup bundle
A backup bundle should contain encrypted local vault state, local profile metadata, Memory Palace state, hub pairing state, and section checksums.

## Plugin-lite extension packs

Iris supports **manifest-based extension packs** loaded locally from JSON. An extension pack may add:

- template shortcuts,
- trigger presets,
- export adapters for JSON, markdown, or email packaging.

Extension packs are local configuration, not executable code. They must not add remote code loading, silent network sync, or authority-granting automation.
