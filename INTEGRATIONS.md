# Integrations

Open-source tools and libraries used by the Burgess Principle framework.

Each entry is something the repository already depends on. If you're contributing code or extending the toolkit, this is a quick reference for what powers each capability.

For the stable local/API surface and versioned file contracts, see [`INTEGRATION_CONTRACT.md`](INTEGRATION_CONTRACT.md).

---

## Python Toolkit

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| Hash verification | [hashlib + hmac](https://docs.python.org/3/library/hashlib.html) (stdlib) | Zero-dependency, constant-time SHA-256 comparison for the SOVEREIGN / NULL binary test. |
| REST API | [FastAPI](https://github.com/fastapi/fastapi) | Lightweight async framework with automatic OpenAPI docs — ideal for a single `/verify` endpoint. |
| ASGI server | [Uvicorn](https://github.com/encode/uvicorn) | Fast, production-ready ASGI server that pairs natively with FastAPI. |
| Testing | [pytest](https://github.com/pytest-dev/pytest) | Simple, expressive test runner used across the 90-test suite. |
| Build system | [setuptools](https://github.com/pypa/setuptools) | Standard Python packaging — keeps `pyproject.toml` configuration minimal. |

## Cryptographic Vault (TypeScript)

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| Hashing & KDF | [@noble/hashes](https://github.com/paulmillr/noble-hashes) | Audited, zero-dependency JS hashing and PBKDF2 key derivation — no native bindings required. |
| Elliptic curves | [@noble/curves](https://github.com/paulmillr/noble-curves) | Audited, zero-dependency EC signatures for signed vault receipts. |
| Authenticated encryption | [Node.js crypto](https://nodejs.org/api/crypto.html) (built-in) | AES-256-GCM via the standard library — no third-party dependency needed. |
| TypeScript compiler | [TypeScript](https://github.com/microsoft/TypeScript) | Adds type safety to the Sovereign Personal Vault library. |

## On-Chain Claims Protocol (Python)

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| Ed25519 signing | [PyNaCl](https://github.com/pyca/pynacl) | Audited Python binding to libsodium — Ed25519 key generation, signing, and verification for on-chain claim receipts. |

## Smart Contracts (Solidity)

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| On-chain registry | [Solidity ^0.8.20](https://github.com/ethereum/solidity) | Industry-standard smart contract language for EVM L2 deployment (Base, Arbitrum, Optimism). |
| Build & deploy | [Foundry](https://github.com/foundry-rs/foundry) (recommended) | Fast, minimal toolchain for compiling and deploying Solidity contracts. |

## CI / CD & Hosting

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| Continuous integration | [GitHub Actions](https://github.com/features/actions) | Built into GitHub — runs pytest across Python 3.11, 3.12 and 3.13 on every push and PR. |
| Dependency updates | [Dependabot](https://github.com/dependabot) | Automated PRs for GitHub Actions version bumps. |
| Web hosting | [Vercel](https://vercel.com) | Zero-config hosting for the Iris chat interface and serverless API at `burgess-principle.vercel.app`. |

## Iris — Conversational AI Interface

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| Chat API (cloud) | [OpenAI Python SDK](https://github.com/openai/openai-python) | OpenAI-compatible client used to connect to xAI (Grok), OpenAI, or Anthropic APIs via a single interface. |
| Chat API (local) | [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) | Runs GGUF models locally for Sovereign Mode — zero cloud dependency, full privacy. |
| Serverless runtime | [Vercel Python Runtime](https://vercel.com/docs/functions/runtimes/python) | Lightweight serverless function that serves the Iris chat endpoint without additional infrastructure. |
| Local server | [FastAPI](https://github.com/fastapi/fastapi) + [Uvicorn](https://github.com/encode/uvicorn) | Powers the Sovereign Mode local HTTP server (`iris-local.py`). |
| Streaming | Server-Sent Events (SSE) | Native browser support for real-time streaming — no WebSocket overhead or additional dependencies. |

## AI Integration

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| LLM API client | [OpenAI Python SDK](https://github.com/openai/openai-python) | OpenAI-compatible client used to connect to the xAI (Grok) API in the toolkit examples. |

---

## Verifying On-Chain Burgess Claims

External systems — AI assistants, exchanges, DAOs, regulators — can verify on-chain Burgess Claims using the open-source SDK or by reading the smart contract directly.

| Step | Method | What it proves |
| --- | --- | --- |
| Signature verification | `verify_onchain_receipt(commitment_hash, signature, public_key_hex)` | The claim was signed by the stated Ed25519 key. |
| Commitment verification | `verify_commitment(claim_details, timestamp, nonce, public_key_hex, expected_hash)` | The disclosed facts match the on-chain fingerprint (selective disclosure). |
| Temporal ordering | Read `blockTimestamp` from `getClaim(claimId)` on the smart contract | The claim existed at that block time. |

No personal data is stored on-chain. Verifiers only ever see hashes, signatures, and metadata — full claim details stay encrypted in the user's local Vault unless they choose to disclose.

See [onchain-protocol/spec.md](onchain-protocol/spec.md) for the full protocol specification and [onchain-protocol/examples/vault_to_chain.py](onchain-protocol/examples/vault_to_chain.py) for a working example.

---

> **Contributing a new integration?** Please keep it minimal. Only add a tool if the framework genuinely depends on it. See [CONTRIBUTING.md](CONTRIBUTING.md) for tone and guidelines.
