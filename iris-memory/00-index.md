# Iris Memory Palace — Index

**Version:** 0.1.0  
**Last updated:** 2026-05-07

## Overview

The Iris Memory Palace is a local-first knowledge base for the Iris sovereign AI
agent. It gathers the current identity, founder profile, partner structure, live
case context, and technical infrastructure into one verifiable memory surface.

It is not a substitute for human judgment. It exists to help Iris retrieve the
right record, cite the source, and preserve the Burgess Principle requirement for
individual human scrutiny.

## Table of contents

| File | Description | Last updated |
|---|---|---|
| `01-identity.md` | Iris's role, tone, operating principles, and protected governance question. | 2026-05-07 |
| `02-lewis-profile.md` | Founder profile, communication preferences, family founders, and 90-day goals. | 2026-05-07 |
| `03-partners.md` | Certified practitioner structure, licensing boundaries, and anti-monetisation guardrails. | 2026-05-07 |
| `04-live-cases.md` | Current energy, local government, enforcement, consumer, FOI, and regulatory fronts. | 2026-05-07 |
| `05-infrastructure.md` | Repository, Iris stack, Phase 3 Memory Palace architecture, on-chain protocol, and statutory context. | 2026-05-07 |

## How to query this memory

Use prompts that ask Iris to answer from the Memory Palace first, then name the
source file it relied on.

Example prompts:

- "Iris, using the Memory Palace, summarise the current live energy cases and cite the source file."
- "Iris, what are Lewis's communication preferences? Answer from memory and name the source."
- "Iris, list the current certified partners and explain the anti-monetisation boundary."
- "Iris, what does the Phase 3 Memory Palace architecture require for verifiable receipts?"
- "Iris, before drafting this letter, check whether any Memory Palace case context is relevant."

## Integrity note

The generated `memory-palace.json` records the full Markdown content and a
SHA-256 hash for each source file. The core Memory Palace then signs each memory
entry with Ed25519 and calculates a Merkle root so later readers can detect
tampering. Cryptography proves record integrity; it does not prove legal truth
or replace named human review.
