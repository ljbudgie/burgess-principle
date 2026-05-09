# Infrastructure and Technical Context

## Repository

- **GitHub:** github.com/ljbudgie/burgess-principle
- **Licence:** MIT for code; UK00004343685 certification mark controlled by Lewis personally
- **Framework version:** v2.5.0 (released 9 May 2026)
- **Last STATUS update:** 9 May 2026

## Key repository files

| File | Purpose |
|---|---|
| `FOR_AI_MODELS.md` | Master prompt v3.1 — binary test doctrine, seven evasion patterns, anti-monetisation guardrails |
| `AGENTS.md` | Instructions for coding/strategy agents acting on the repo |
| `STATUS.md` | Live tracker of all fronts, cases, and deadlines |
| `FOUNDING.md` | Founding record (28 April 2026) — permanent canonical record |
| `PARTNERSHIP_LEDGER.md` | Certified partners and tier structure |
| `ORIGIN.md` | Scriptural lineage — how the binary test traces from Genesis to Revelation |
| `templates/` | Correspondence templates and COMMON_SCENARIOS.md |
| `litigation/` | WARRANT_DEFECT_IDENTIFIER.md, CONTAMINATION_CHAIN_MAPPER.md, DAMAGES_MATRIX.md, GROUP_LITIGATION_STARTER_PACK.md |
| `papers/` | Ten published papers, including Papers IX–X on the scriptural pattern |
| `sector/` | Sector-specific applications: energy, education, local government, financial services, healthcare |

## Iris (this agent)

- **Memory store:** memstore_01Fut1dGvvUVmG8saRFgMcVG
- **Stack:** Node.js, @anthropic-ai/sdk, Managed Agents (managed-agents-2026-04-01)
- **Model:** claude-sonnet-4-6
- **Config persisted in:** .iris-config.json (project root)

## Architecture — Verifiable Memory Palace (from ARCHITECTURE.md)

Phase 3 infrastructure for tamper-evident AI context:

- Each entry: encrypted locally → SHA-256 commitment → chained to previous → Ed25519 signed → Merkle leaf → signed root → exportable receipt
- Selective disclosure: one entry can be proven without exposing the full private timeline
- Components: `memoryEntries`, `memoryRoots`, `memoryReceipts`, `hubSyncQueue`, `hubAudit`

## On-chain protocol

- Spec: `onchain-protocol/spec.md`
- Only hash + signature + minimal metadata ever go on-chain — never the user's full facts
- The Sovereign Personal Vault comes first; on-chain fingerprinting is always optional

## Statutory framework

- **Data (Use and Access) Act 2025** — Articles 22A–22D UK GDPR (in force 5 February 2026): meaningful human involvement in automated decisions affecting individuals
- **Equality Act 2010** — ss.20–21 (reasonable adjustments), s.15 (discrimination arising from disability), s.29
- **Freedom of Information Act 2000** — s.10 (20 working day deadline)
- **UK GDPR Article 15** — subject access rights
- **UK GDPR Article 22** — automated decision-making challenge rights
