# Iris Integration Contract

This document defines the small, stable surface that external tools can rely on without weakening Iris's sovereignty-first model.

## Principles

- **Local-first:** integrations should prefer local files and local APIs before hosted services.
- **Advisory-only:** no integration may present AI output as a SOVEREIGN or NULL decision.
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
- `POST /claims/verify` — verify an Ed25519-signed on-chain claim receipt.

### Sovereign Local Mode
- `POST /api/chat` — local advisory chat when Iris runs via `iris-local.py`.
- `POST /api/generate-claim` — generate a local claim package and letter markdown.
- `POST /api/queue-onchain-fingerprint` — queue a compact claim fingerprint for local-first posting flows.
- `GET /api/my-profile` — read the local sovereign profile summary.
- `POST /api/my-profile/setup` — create or update the local sovereign profile summary.

### Sovereign Hub example
- `GET /api/hub/hello` — retrieve the hub public key and basic identity metadata.
- `POST /api/sovereign-sync-v2` — exchange encrypted commitment deltas with the self-hosted hub.

## Local file contracts

### Claim package
A generated claim package should be exported as structured JSON, with letter markdown separated from commitment metadata.

### Memory receipt
A memory receipt should contain the signed entry, signed root, and Merkle inclusion proof needed for selective disclosure.

### Sovereign backup bundle
A backup bundle should contain encrypted local vault state, local profile metadata, Memory Palace state, hub pairing state, and section checksums.

## Plugin-lite extension packs

Iris supports **manifest-based extension packs** loaded locally from JSON. An extension pack may add:

- template shortcuts,
- trigger presets,
- export adapters for JSON, markdown, or email packaging.

Extension packs are local configuration, not executable code. They must not add remote code loading, silent network sync, or authority-granting automation.
