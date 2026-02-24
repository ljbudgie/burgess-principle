"""
trace_example.py — Tracer Protocol demonstration
Part of The Burgess Principle toolkit.

Demonstrates how to use CreditContaminationTracer with:
  1. Automatic email-to-address resolution (requires API keys).
  2. Manual address supply (no API keys needed).

Run from the repository root:
    python examples/trace_example.py
"""

import json
import sys
import os

# Allow running from the repo root without installing the package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from credit_tracer import CreditContaminationTracer, KNOWN_VOID_WARRANTS

# ---------------------------------------------------------------------------
# Example 1 — Email-only trace (no API keys configured → address not resolved)
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("EXAMPLE 1: Email-only trace (placeholder — no API keys)")
print("=" * 60)

tracer = CreditContaminationTracer()
report = tracer.trace_by_email("subject@example.com")
print(report["summary"])
print("\nFull report (JSON):")
print(json.dumps(report, indent=2))

# ---------------------------------------------------------------------------
# Example 2 — Manual address supply (email resolution failed or unavailable)
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("EXAMPLE 2: Manual address supply")
print("=" * 60)

# Use the first address from the demo database so the warrant linkage fires.
demo_address = KNOWN_VOID_WARRANTS[0]["address"]

report2 = tracer.trace_by_address(
    email="subject@example.com",
    address=demo_address,
)
print(report2["summary"])
print("\nFull report (JSON):")
print(json.dumps(report2, indent=2))

# ---------------------------------------------------------------------------
# Example 3 — Manual address that has no matching warrant
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("EXAMPLE 3: Address with no matching void warrant")
print("=" * 60)

report3 = tracer.trace_by_address(
    email="clean@example.com",
    address="99 Clean Road, Manchester, M1 1AA",
)
print(report3["summary"])

# ---------------------------------------------------------------------------
# Example 4 — With API keys (illustrative; keys shown as placeholders)
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("EXAMPLE 4: With API keys (keys are illustrative placeholders)")
print("=" * 60)

# WARNING: Never commit real API credentials to source control.
# Use environment variables or a secrets manager instead:
#   export FULLCONTACT_API_KEY=your_key_here
#   export CLEARBIT_API_KEY=your_key_here
#   export CCJ_API_KEY=your_key_here
tracer_live = CreditContaminationTracer(
    fullcontact_api_key="YOUR_FULLCONTACT_API_KEY_HERE",
    clearbit_api_key="YOUR_CLEARBIT_API_KEY_HERE",
    ccj_api_key="YOUR_CCJ_API_KEY_HERE",
)
# In a real run with valid keys the resolve_address_from_email call would
# return a real address and check_ccj_registry would return live data.
print("Tracer instantiated with API key slots. Replace placeholder strings")
print("with real credentials to enable live OSINT and CCJ lookups.")
print(
    "\nTo run a live trace:\n"
    "  report = tracer_live.trace_by_email('real.subject@domain.com')\n"
    "  print(json.dumps(report, indent=2))"
)
