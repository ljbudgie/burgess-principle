# Tests

This folder contains the **pytest** test suite for the Burgess Principle Python toolkit.

## Coverage areas

The suite covers the core Python modules and scripts, including:

- `verify_scrutiny.py`
- `tracer/`
- `api.py`
- `api/chat.py`
- `iris/claim_builder.py`
- `iris/sovereign_profile.py`
- `iris-local.py`
- `setup-wizard.py`
- `onchain-protocol/sdk/onchain_claims.py`
- static PWA integration checks

## Running the tests

```bash
pip install -e ".[test,api,onchain]"
python -m pytest tests/
```

The suite runs automatically on every push and pull request via [GitHub Actions CI](../.github/workflows/ci.yml).

## Adding new tests

If you add a new feature or fix a bug, include tests that cover the change. Keep tests small, isolated, and clearly named, and prefer loading path-based scripts with `importlib.util` when the target is not an importable package.
