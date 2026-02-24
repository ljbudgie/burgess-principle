"""
credit_tracer.py — Tracer Protocol (Forensics)
Part of The Burgess Principle toolkit.

Traces "contaminated credit" chains from a single email address back to the
original sin: a void warrant issued under the Rights of Entry (Gas and
Electricity Boards) Act 1954.

Contamination Chain:
  Email -> Address -> Void Warrant -> CCJ/Default -> Credit Score Impact

DISCLAIMER: Live data requires external API credentials.
  - Identity/address resolution: FullContact, Clearbit, or equivalent OSINT API.
  - CCJ / default lookups: Registry Trust, credit-bureau APIs, or equivalent.
Set the relevant environment variables (see placeholder methods) before
calling the live data paths.  Without keys the module returns mock/placeholder
data so that the forensic chain can still be exercised end-to-end.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Optional: import WarrantDefectIdentifier if it lives in the same package.
# If the module does not yet exist the tracer degrades gracefully.
# ---------------------------------------------------------------------------
try:
    from .warrant_defect_identifier import WarrantDefectIdentifier  # type: ignore
    _WARRANT_CHECKER_AVAILABLE = True
except ImportError:
    _WARRANT_CHECKER_AVAILABLE = False


# ---------------------------------------------------------------------------
# Known void warrants — local reference database.
# In production this would be loaded from a file or external store.
# ---------------------------------------------------------------------------
KNOWN_VOID_WARRANTS: list[dict[str, Any]] = [
    {
        "warrant_id": "DEMO-001",
        "address": "1 Example Street, London, EC1A 1BB",
        "issuing_court": "Westminster Magistrates",
        "issue_date": "2023-06-15",
        "defect": "Warrant granted without valid application under s.2 of the Rights of Entry (Gas and Electricity Boards) Act 1954",
        "status": "VOID_AB_INITIO",
    },
]


class CreditContaminationTracer:
    """
    Forensic framework that traces the downstream credit-contamination chain
    originating from a defective warrant.

    Usage::

        tracer = CreditContaminationTracer()
        report = tracer.trace_by_email("someone@example.com")
        print(json.dumps(report, indent=2))
    """

    def __init__(
        self,
        fullcontact_api_key: Optional[str] = None,
        clearbit_api_key: Optional[str] = None,
        ccj_api_key: Optional[str] = None,
    ) -> None:
        """
        Parameters
        ----------
        fullcontact_api_key:
            API key for FullContact identity resolution.
            Falls back to the ``FULLCONTACT_API_KEY`` environment variable.
        clearbit_api_key:
            API key for Clearbit identity resolution.
            Falls back to the ``CLEARBIT_API_KEY`` environment variable.
        ccj_api_key:
            API key for Registry Trust / CCJ lookup.
            Falls back to the ``CCJ_API_KEY`` environment variable.
        """
        self._fullcontact_key = fullcontact_api_key or os.environ.get("FULLCONTACT_API_KEY")
        self._clearbit_key = clearbit_api_key or os.environ.get("CLEARBIT_API_KEY")
        self._ccj_key = ccj_api_key or os.environ.get("CCJ_API_KEY")

    # ------------------------------------------------------------------
    # Public entry-point
    # ------------------------------------------------------------------

    def trace_by_email(self, email: str) -> dict[str, Any]:
        """
        Orchestrate the full contamination-chain investigation for *email*.

        Returns a structured report dict (JSON-serialisable) showing:
          Email -> Address -> Void Warrant -> CCJ/Default -> Credit Score Impact

        Parameters
        ----------
        email:
            The email address to investigate.
        """
        if not self._is_valid_email(email):
            return self._error_report(email, "Invalid email address format.")

        report: dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "tracer_version": "1.0.0",
            "contamination_chain": {},
            "summary": "",
            "disclaimer": (
                "This report is for forensic/investigative use only. "
                "Live data requires external API credentials. "
                "Placeholder data is returned when no API keys are configured."
            ),
        }

        chain: dict[str, Any] = report["contamination_chain"]

        # Step 1 — Identity Resolution
        chain["email"] = email
        address = self.resolve_address_from_email(email)
        chain["resolved_address"] = address

        # Step 2 — Warrant Linkage
        void_warrant = self._check_void_warrant(address)
        chain["void_warrant"] = void_warrant

        # Step 3 — Credit Damage Assessment
        ccj_data = self.check_ccj_registry(address)
        chain["ccj_defaults"] = ccj_data

        # Step 4 — Credit Score Impact summary
        chain["credit_score_impact"] = self._assess_credit_impact(void_warrant, ccj_data)

        # Human-readable summary
        report["summary"] = self._build_summary(chain)

        return report

    # ------------------------------------------------------------------
    # Step 1 — Identity Resolution (placeholder)
    # ------------------------------------------------------------------

    def resolve_address_from_email(self, email: str) -> Optional[str]:
        """
        Resolve a physical address from an email address.

        **Placeholder implementation.**
        In a live deployment this method calls an OSINT identity API such as
        FullContact (https://www.fullcontact.com/) or Clearbit
        (https://clearbit.com/).  Set ``FULLCONTACT_API_KEY`` or
        ``CLEARBIT_API_KEY`` in your environment (or pass them to the
        constructor) to enable live resolution.

        Without valid API keys this method returns ``None`` so that the rest
        of the chain can still be exercised with a manually supplied address.

        Parameters
        ----------
        email:
            The email address to resolve.

        Returns
        -------
        str or None
            The resolved postal address, or ``None`` if resolution fails.
        """
        if self._fullcontact_key:
            # TODO: Replace with real FullContact v3 Person Enrich call.
            # import requests
            # resp = requests.post(
            #     "https://api.fullcontact.com/v3/person.enrich",
            #     headers={"Authorization": f"Bearer {self._fullcontact_key}"},
            #     json={"email": email},
            # )
            # data = resp.json()
            # return data.get("details", {}).get("locations", [{}])[0].get("formatted")
            pass  # pragma: no cover

        if self._clearbit_key:
            # TODO: Replace with real Clearbit Person API call.
            # import requests
            # resp = requests.get(
            #     "https://person.clearbit.com/v2/people/find",
            #     params={"email": email},
            #     auth=(self._clearbit_key, ""),
            # )
            # data = resp.json()
            # return data.get("location")
            pass  # pragma: no cover

        # No API keys configured — return None (caller may supply address manually).
        return None

    # ------------------------------------------------------------------
    # Step 2 — Warrant Linkage (internal helper)
    # ------------------------------------------------------------------

    def _check_void_warrant(self, address: Optional[str]) -> Optional[dict[str, Any]]:
        """
        Check whether *address* matches any known void warrant.

        Integrates with ``WarrantDefectIdentifier`` when available; otherwise
        consults the module-level ``KNOWN_VOID_WARRANTS`` list.
        """
        if not address:
            return None

        normalised = address.strip().lower()

        if _WARRANT_CHECKER_AVAILABLE:
            # Delegate to the dedicated identifier if present.
            checker = WarrantDefectIdentifier()  # type: ignore[name-defined]
            result = checker.check_address(address)
            if result and result.get("is_void"):
                return result

        # Fallback: scan local database.
        for warrant in KNOWN_VOID_WARRANTS:
            if warrant["address"].strip().lower() == normalised:
                return warrant

        return None

    # ------------------------------------------------------------------
    # Step 3 — CCJ / Default check (placeholder)
    # ------------------------------------------------------------------

    def check_ccj_registry(self, address: Optional[str]) -> dict[str, Any]:
        """
        Check for County Court Judgments (CCJs) or defaults linked to *address*.

        **Placeholder implementation.**
        In a live deployment this method queries Registry Trust
        (https://www.registrytrust.org.uk/) or a credit-bureau API.
        Set ``CCJ_API_KEY`` in your environment (or pass it to the constructor)
        to enable live lookups.

        Without a valid API key this method returns a placeholder result
        indicating that a real check is required.

        Parameters
        ----------
        address:
            The postal address to query.

        Returns
        -------
        dict
            A dict containing ``found`` (bool), ``entries`` (list), and
            ``note`` (str).
        """
        if not address:
            return {
                "found": False,
                "entries": [],
                "note": "No address supplied; CCJ lookup skipped.",
            }

        if self._ccj_key:
            # TODO: Replace with real Registry Trust or credit-bureau API call.
            # import requests
            # resp = requests.get(
            #     "https://api.registrytrust.org.uk/v1/search",
            #     headers={"Authorization": f"Bearer {self._ccj_key}"},
            #     params={"address": address},
            # )
            # data = resp.json()
            # return {
            #     "found": bool(data.get("results")),
            #     "entries": data.get("results", []),
            #     "note": "Live data from Registry Trust.",
            # }
            pass  # pragma: no cover

        # found=None intentionally signals "check not performed" (distinct from
        # found=False which means "checked and nothing found").
        return {
            "found": None,
            "entries": [],
            "note": (
                "CCJ_API_KEY not configured. "
                "Provide a Registry Trust or credit-bureau API key for live data."
            ),
        }

    # ------------------------------------------------------------------
    # Step 4 — Credit Score Impact assessment (internal helper)
    # ------------------------------------------------------------------

    def _assess_credit_impact(
        self,
        void_warrant: Optional[dict[str, Any]],
        ccj_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Produce a structured credit-impact summary from available evidence."""
        if void_warrant is None and not ccj_data.get("found"):
            return {
                "level": "UNKNOWN",
                "reason": "Insufficient data to assess credit impact.",
            }

        reasons: list[str] = []
        level = "LOW"

        if void_warrant:
            reasons.append(
                f"Void warrant detected ({void_warrant.get('warrant_id', 'N/A')}). "
                "All downstream entries originating from this warrant are tainted."
            )
            level = "HIGH"

        if ccj_data.get("found"):
            entry_count = len(ccj_data.get("entries", []))
            reasons.append(
                f"{entry_count} CCJ/default record(s) found linked to this address."
            )
            level = "HIGH"
        elif ccj_data.get("found") is None:
            reasons.append("CCJ check pending — API key required for live data.")

        return {
            "level": level,
            "reasons": reasons,
        }

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Basic email format check (not full RFC 5322 compliance).
        Rejects obviously malformed values while keeping the dependency footprint
        minimal.  For stricter validation consider the ``email-validator`` package.
        """
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        return bool(re.match(pattern, email))

    @staticmethod
    def _build_summary(chain: dict[str, Any]) -> str:
        """Render a plain-text summary of the contamination chain."""
        lines = [
            "=== CONTAMINATION CHAIN SUMMARY ===",
            f"  Email              : {chain.get('email', 'N/A')}",
            f"  Resolved Address   : {chain.get('resolved_address') or 'Not resolved (supply manually)'}",
        ]

        warrant = chain.get("void_warrant")
        if warrant:
            lines.append(f"  Void Warrant       : {warrant.get('warrant_id')} — {warrant.get('defect', '')}")
        else:
            lines.append("  Void Warrant       : None found in local database")

        ccj = chain.get("ccj_defaults", {})
        if ccj.get("found"):
            lines.append(f"  CCJ/Defaults       : {len(ccj.get('entries', []))} record(s) found")
        else:
            lines.append(f"  CCJ/Defaults       : {ccj.get('note', 'N/A')}")

        impact = chain.get("credit_score_impact", {})
        lines.append(f"  Credit Impact      : {impact.get('level', 'UNKNOWN')}")
        for reason in impact.get("reasons", []):
            lines.append(f"                       → {reason}")

        lines.append("====================================")
        return "\n".join(lines)

    @staticmethod
    def _error_report(email: str, message: str) -> dict[str, Any]:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "error": message,
            "email": email,
            "contamination_chain": {},
            "summary": f"ERROR: {message}",
        }

    # ------------------------------------------------------------------
    # Convenience: allow supplying the address manually
    # ------------------------------------------------------------------

    def trace_by_address(self, email: str, address: str) -> dict[str, Any]:
        """
        Run the contamination-chain trace using a manually supplied *address*
        instead of attempting automatic email resolution.

        Useful when OSINT API keys are not available.

        Parameters
        ----------
        email:
            The email address associated with the subject (for the report).
        address:
            The known postal address to investigate.
        """
        report: dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "tracer_version": "1.0.0",
            "contamination_chain": {},
            "summary": "",
            "disclaimer": (
                "This report is for forensic/investigative use only. "
                "Address was supplied manually."
            ),
        }

        chain: dict[str, Any] = report["contamination_chain"]
        chain["email"] = email
        chain["resolved_address"] = address
        chain["address_source"] = "manual"

        void_warrant = self._check_void_warrant(address)
        chain["void_warrant"] = void_warrant

        ccj_data = self.check_ccj_registry(address)
        chain["ccj_defaults"] = ccj_data

        chain["credit_score_impact"] = self._assess_credit_impact(void_warrant, ccj_data)
        report["summary"] = self._build_summary(chain)

        return report
