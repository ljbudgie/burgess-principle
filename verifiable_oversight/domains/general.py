"""
GeneralDomain — the baseline domain with no additional metadata requirements.

Use this when no more specific domain applies, or when building a
cross-domain assessment. All five binary test elements apply with
no domain-specific extensions.
"""

from __future__ import annotations

from .base import BaseDomain


class GeneralDomain(BaseDomain):
    """
    General-purpose domain. No domain-specific metadata or validation.

    Suitable for:
    - Initial assessments before a domain is determined
    - Cross-domain comparative analysis
    - Test and demonstration purposes
    """

    @property
    def name(self) -> str:
        return "general"

    @property
    def guidance(self) -> str:
        return (
            "General domain: apply the five-element binary test without "
            "domain-specific extensions. All five elements are required for "
            "SOVEREIGN. A single missing element yields NULL.\n\n"
            "Process language — 'reviewed by our team', 'subject to human "
            "oversight', 'considered by the relevant department' — does not "
            "satisfy any element. A follow-up question is always required."
        )
