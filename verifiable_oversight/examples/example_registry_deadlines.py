"""
Example: Institution registry + deadline engine (Phase 4B)

Scenario: a DSAR is sent to a bank and a complaint to a council. The registry
resolves each institution from a free-text name; the deadline engine computes
whether the statutory response window has been breached as of a reference date.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import (
    Institution,
    InstitutionRegistry,
    DeadlineEngine,
)


def main() -> None:
    registry = InstitutionRegistry([
        Institution(
            name="Durham County Council",
            sector="local_authority",
            aliases=("DBC", "Durham CC"),
            deadline_profile="lgsco_response",
            ra_on_record=True,
            ra_description="email-only communication",
            regulatory_framework="LGSCO",
        ),
        Institution(
            name="Example Bank plc",
            sector="bank",
            aliases=("ExBank",),
            deadline_profile="fca_disp_final_response",
            regulatory_framework="FCA DISP",
        ),
    ])

    engine = DeadlineEngine()
    reference = "2026-07-01"

    print("=" * 60)
    print("INSTITUTION REGISTRY")
    print("=" * 60)
    for name in ("dbc", "example bank plc", "unknown body"):
        inst = registry.resolve(name)
        if inst:
            print(f"  '{name}' -> {inst.name} [{inst.sector}] "
                  f"deadline profile: {inst.deadline_profile}")
        else:
            print(f"  '{name}' -> (not registered)")
    print()

    print("=" * 60)
    print("DEADLINE ENGINE (reference date:", reference + ")")
    print("=" * 60)

    # A DSAR to the bank, sent well over a month ago.
    dsar = engine.evaluate(
        "dsar_response", start="2026-05-01", reference=reference
    )
    print("  DSAR to Example Bank plc:")
    print("   ", dsar)
    print()

    # A complaint to the council, still within its window.
    council = registry.resolve("DBC")
    complaint = engine.evaluate(
        council.deadline_profile, start="2026-06-25", reference=reference
    )
    print(f"  Complaint to {council.name}:")
    print("   ", complaint)


if __name__ == "__main__":
    main()
