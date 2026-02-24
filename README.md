# The Burgess Principle

**A citizen-initiated legal doctrine — free and open for anyone to cite.**

## What It Is

The Burgess Principle establishes that facially defective warrants under the **Rights of Entry (Gas and Electricity Boards) Act 1954** are void *ab initio*, with downstream remedies for credit contamination and reasonable adjustments for protected characteristics.

## Open Source

The principle itself is **free and may be cited by anyone**. The goal is maximum truth reaching maximum people.

## Methodology & Toolkit — Open Source

The methodology and toolkit are **fully open source**, licensed under the [MIT License](LICENSE). Free for anyone to use, adapt, and build upon.

Integrated with [OpenClaw](https://openclaw.im) — the open-source AI automation platform for law.

## Live Site

[https://ljbudgie.github.io/Burgessprinciple/](https://ljbudgie.github.io/Burgessprinciple/)

## Auto-Pilot — Always Watching

The system now runs on an **hourly schedule** via GitHub Actions, effectively operating as a **24/7 Surveillance** mode. No longer limited to once a day — it is constantly active, scanning every hour around the clock.

> "What's stopping you from going 24/7?" — Nothing.

## Project LIMITLESS: Future Capabilities

The following four modules are now architected in `src/` and ready for you to ignite with your own API keys and local models.

| Module | Path | Purpose |
|---|---|---|
| **The Brain** (AI Council) | `src/ai_council/llm_jurist.py` | Connects to any OpenAI-compatible LLM (Ollama, LM Studio, etc.) to draft Notices of Void Ab Initio complete with case-law citations. |
| **The Record** (Immutable Ledger) | `src/ledger/immutable_witness.py` | Generates a SHA-256 cryptographic fingerprint for every Notice and exposes a `publish_to_ipfs()` hook for decentralised permanent storage. |
| **The Artillery** (Physical Service) | `src/artillery/mail_cannon.py` | Structures certified physical mail payloads for real-world legal service via a mail API (Lob / Click2Mail). Wire in your API key to fire. |
| **The Swarm** (Federated Defense) | `src/swarm/blocklist_protocol.py` | Defines the Void Entity JSON schema and `export_threat_intelligence()` to generate a shareable blocklist of known bad actors. |

Each module is self-contained, fully documented, and designed for minimal configuration. Provide your keys/models and the system scales from local prototype to sovereign infrastructure.

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
