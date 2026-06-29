"""
CommunicationDomain — oversight assessment for institutional communications.

This domain is designed for assessing decisions about how an institution
communicates with an individual — particularly where accessibility reasonable
adjustments (RAs) are in play under EA 2010 ss.20/21.

Domain-specific metadata captures:
- The communication channel(s) used
- Whether the individual's RA was on record at the time
- Whether the channel was accessible (e.g. phone-only to a deaf person = breach)
- Applicable regulatory framework (e.g. FCA DISP, Ofcom, ICO)

A communication decision can fail the binary test AND separately breach
EA 2010 ss.20/21 through channel choice alone. These are distinct findings
and both are recorded.
"""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseDomain


# Channels that are inaccessible to a deaf person with an email-only RA.
# This list informs validation but is not exhaustive.
_INACCESSIBLE_TO_EMAIL_ONLY_RA = {"telephone", "phone", "call", "voicemail", "sms", "text"}


class CommunicationDomain(BaseDomain):
    """
    Domain for institutional communications — particularly EA 2010
    ss.20/21 accessibility and DUAA 2025 automated decision concerns.

    Additional domain_kwargs
    -----------------------
    channel : str
        The communication channel used (e.g. 'email', 'telephone',
        'letter', 'portal-only', 'app-only').
    ra_on_record : bool
        Whether a reasonable adjustment (RA) notification was on record
        at the institution at the time of the decision.
    ra_description : str, optional
        Description of the RA (e.g. 'email-only communication').
    channel_accessible : bool, optional
        Whether the channel used was accessible given the RA.
        If not provided, inferred from `channel` and `ra_description`.
    regulatory_framework : str, optional
        Applicable regulatory body / framework (e.g. 'FCA DISP 1.6',
        'Ofcom Broadcasting Code', 'ICO UK GDPR').
    automated : bool, optional
        Whether the communication was fully automated (no human author).
        Automated communications from a do-not-reply address while a
        formal complaint is active = NULL without further analysis.
    """

    @property
    def name(self) -> str:
        return "communication"

    @property
    def guidance(self) -> str:
        return (
            "Communication domain: assess both the binary test (was a named "
            "human's mind applied to the decision to send this communication?) "
            "and the accessibility of the channel (did the institution use a "
            "channel compatible with the individual's reasonable adjustment?).\n\n"
            "An automated do-not-reply email while a formal complaint is active "
            "is NULL on the binary test and may constitute a s.20/21 breach.\n\n"
            "A telephone referral to a person with an email-only RA is a s.20/21 "
            "breach regardless of the binary test outcome for the underlying decision.\n\n"
            "Process language ('we responded to your query', 'our team reviewed "
            "your message') does not satisfy the named person or specific facts "
            "elements. Ask directly: 'Please provide the full name and role of the "
            "individual who reviewed my specific case before this response was sent.'"
        )

    def validate_domain_metadata(self, metadata: dict[str, Any]) -> list[str]:
        issues = []
        channel = metadata.get("channel", "")
        ra_on_record = metadata.get("ra_on_record", None)
        ra_description = (metadata.get("ra_description") or "").lower()
        channel_accessible = metadata.get("channel_accessible", None)
        automated = metadata.get("automated", False)

        # Flag inaccessible channel where RA is on record
        if ra_on_record and channel_accessible is False:
            issues.append(
                f"Channel '{channel}' used despite RA on record — "
                "potential EA 2010 ss.20/21 breach."
            )

        # Infer accessibility if not explicitly set
        if ra_on_record and channel_accessible is None:
            channel_lower = channel.lower()
            if any(term in channel_lower for term in _INACCESSIBLE_TO_EMAIL_ONLY_RA):
                if "email" in ra_description:
                    issues.append(
                        f"Channel '{channel}' appears inaccessible given email-only RA "
                        "— inferred EA 2010 ss.20/21 concern. Set channel_accessible=False "
                        "to record this as a confirmed breach."
                    )

        # Automated communication while complaint active
        if automated:
            issues.append(
                "Communication was automated (no human author). "
                "Binary test will return NULL unless a human reviewed and "
                "authorised the specific communication before sending."
            )

        return issues

    def _build_domain_metadata(
        self,
        channel: str = "unknown",
        ra_on_record: bool = False,
        ra_description: Optional[str] = None,
        channel_accessible: Optional[bool] = None,
        regulatory_framework: Optional[str] = None,
        automated: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "domain": self.name,
            "channel": channel,
            "ra_on_record": ra_on_record,
            "automated": automated,
        }
        if ra_description:
            meta["ra_description"] = ra_description
        if channel_accessible is not None:
            meta["channel_accessible"] = channel_accessible
        if regulatory_framework:
            meta["regulatory_framework"] = regulatory_framework
        meta.update(kwargs)
        return meta
