# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it responsibly.

**Do not open a public issue.**

Instead, please email the maintainer directly or use [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) feature on this repository.

We will acknowledge your report within 72 hours and aim to provide a fix or mitigation plan within 14 days.

## Scope

This policy covers:

- The core verification logic (`verify_scrutiny.py`, `api.py`)
- The cryptographic enforcement layer (`enforcement/sovereign-vault/`)
- The tracer module (`tracer/`)
- The project website (`index.html`)
- CI/CD configuration (`.github/workflows/`)

## Security Expectations for Contributors

All contributions must follow these security principles:

1. **No hardcoded secrets** — Never commit API keys, tokens, or credentials.
2. **Input validation** — All user-facing inputs must be validated and sanitised.
3. **No dangerous patterns** — Avoid `eval()`, `innerHTML` with untrusted data, or other injection-prone patterns.
4. **Minimal dependencies** — Only add dependencies that are strictly necessary. Each new dependency increases the attack surface.
5. **Scoped changes** — Do not bundle unrelated application code (e.g., demo apps, e-commerce integrations) into PRs. Unrelated code introduces unrelated vulnerabilities.

## Supported Versions

| Version | Supported |
| ------- | --------- |
| Latest on `main` | ✅ |
| Older commits | ❌ |

Thank you for helping keep the Burgess Principle safe and trustworthy.
