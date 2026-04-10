# Integrations

Open-source tools and libraries used by the Burgess Principle framework.

Each entry is something the repository already depends on. If you're contributing code or extending the toolkit, this is a quick reference for what powers each capability.

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
| Hashing | [@noble/hashes](https://github.com/paulmillr/noble-hashes) | Audited, zero-dependency JS hashing — no native bindings required. |
| Elliptic curves | [@noble/curves](https://github.com/paulmillr/noble-curves) | Audited, zero-dependency EC signatures for signed vault receipts. |
| Legacy crypto helpers | [crypto-js](https://github.com/brix/crypto-js) | Widely adopted utility for supplementary crypto operations. |
| TypeScript compiler | [TypeScript](https://github.com/microsoft/TypeScript) | Adds type safety to the `iris-gate-person` vault library. |

## CI / CD & Hosting

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| Continuous integration | [GitHub Actions](https://github.com/features/actions) | Built into GitHub — runs pytest across Python 3.11, 3.12 and 3.13 on every push and PR. |
| Dependency updates | [Dependabot](https://github.com/dependabot) | Automated PRs for GitHub Actions version bumps. |
| Web hosting | [Vercel](https://vercel.com) | Zero-config static hosting for the landing page at `burgess-principle.vercel.app`. |

## AI Integration

| Capability | Tool | Why it's chosen |
| --- | --- | --- |
| LLM API client | [OpenAI Python SDK](https://github.com/openai/openai-python) | OpenAI-compatible client used to connect to the xAI (Grok) API in the toolkit examples. |

---

> **Contributing a new integration?** Please keep it minimal. Only add a tool if the framework genuinely depends on it. See [CONTRIBUTING.md](CONTRIBUTING.md) for tone and guidelines.
