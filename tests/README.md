# Tests

This folder contains the **pytest** test suite for the Burgess Principle Python toolkit.

## What's here

| File | Purpose |
|---|---|
| `test_verify_scrutiny.py` | 51 tests covering `verify_scrutiny.py` — result types, constant-time comparison, input validation, CLI behaviour, and edge cases. |
| `test_tracer.py` | 33 tests covering the `tracer/` defect-schema library — defect lookup, listing, and error handling. |
| `test_api.py` | 6 tests covering the optional FastAPI wrapper (`api.py`) — endpoint responses, validation, and error handling. Requires `httpx`. |

## Running the tests

```bash
pip install -e ".[test]"
pytest -q
```

All 90 tests should pass. The suite runs automatically on every push and pull request via [GitHub Actions CI](../.github/workflows/ci.yml).

## Adding new tests

If you add a new feature or fix a bug, please include tests that cover the change. Follow the existing patterns in `test_verify_scrutiny.py` or `test_tracer.py` — each test function should be small, self-contained, and clearly named.
