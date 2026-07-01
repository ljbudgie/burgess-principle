"""
EmailDomain — oversight assessment for a sovereign, email-only application.

Phase 4A. Where :class:`CommunicationDomain` assesses *any* channel choice,
the email domain models the specific accountability object the Burgess Principle
was built for: an **email-only** exchange between an individual and an
institution, where every message is either **inbound** (an institutional
response, assessed on receipt) or **outbound** (the individual's communication,
which itself creates a record).

The design constraint is the feature. If the process works for a profoundly
deaf person with a broken phone and a Mac, it works for everyone who has ever
been routed away from help by an inaccessible process. The following
requirements are therefore treated as **non-negotiable** and each is recorded
as a distinct EA 2010 ss.20/21 finding when breached:

- Email is the only interface — **no portal redirect**.
- **No telephone requirement.**
- **No CAPTCHA.**
- **No app-only verification.**
- A **named individual** is required for every significant response.
- The **reasonable adjustment (RA) is confirmed and recorded before the first
  substantive exchange.**

An inbound response can fail the binary test (no named mind applied) AND
separately breach the accessibility requirements above. These are distinct
findings and all of them are recorded.
"""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseDomain


# Message directions.
_INBOUND = "inbound"      # institution -> individual (assessed on receipt)
_OUTBOUND = "outbound"    # individual -> institution (creates a record)
_DIRECTIONS = {_INBOUND, _OUTBOUND}

# Non-negotiable accessibility barriers. Each maps a metadata flag to the
# breach description recorded when the flag is True on an inbound response.
_ACCESSIBILITY_BARRIERS = {
    "portal_redirect": (
        "Inbound response redirected the individual to a portal — email is the "
        "only agreed interface. No portal redirect: EA 2010 ss.20/21 breach."
    ),
    "telephone_required": (
        "Inbound response required a telephone call — no telephone requirement "
        "is permitted for an email-only RA. EA 2010 ss.20/21 breach."
    ),
    "captcha_required": (
        "Inbound response required a CAPTCHA — no CAPTCHA is permitted. "
        "EA 2010 ss.20/21 breach."
    ),
    "app_only_verification": (
        "Inbound response required app-only verification — no app-only "
        "verification is permitted. EA 2010 ss.20/21 breach."
    ),
}


class EmailDomain(BaseDomain):
    """
    Domain for a sovereign email-only application — Phase 4A.

    Additional domain_kwargs
    -----------------------
    direction : str
        ``'inbound'`` (an institutional response received and assessed) or
        ``'outbound'`` (the individual's own communication, which creates a
        record). Any other value is recorded as a validation issue.
    ra_on_record : bool
        Whether a reasonable adjustment (RA) notification was on record at the
        institution at the time of the message.
    ra_description : str, optional
        Description of the RA (defaults conceptually to 'email-only communication').
    ra_confirmed_before_first_substantive_exchange : bool, optional
        Whether the RA was confirmed and recorded *before* the first substantive
        exchange. Required for the first substantive exchange.
    first_substantive_exchange : bool, optional
        Whether this message is the first substantive exchange in the thread.
        When True, the RA must already have been confirmed and recorded.
    significant_response : bool, optional
        (Inbound only) Whether this response is significant. Every significant
        response requires a named individual.
    named_individual_provided : bool, optional
        (Inbound only) Whether a named individual was provided in the response.
        If not given, inferred from the binary test's named_person element.
    portal_redirect : bool, optional
        (Inbound) The response redirected the individual to a portal.
    telephone_required : bool, optional
        (Inbound) The response required a telephone call.
    captcha_required : bool, optional
        (Inbound) The response required a CAPTCHA.
    app_only_verification : bool, optional
        (Inbound) The response required app-only verification.
    thread_reference : str, optional
        A stable reference for the email thread / conversation.
    message_id : str, optional
        The RFC 5322 Message-ID (or equivalent) of the assessed message.
    regulatory_framework : str, optional
        Applicable regulatory body / framework.
    """

    @property
    def name(self) -> str:
        return "email"

    @property
    def guidance(self) -> str:
        return (
            "Email domain: model an email-only exchange. Each outbound message "
            "(individual -> institution) creates a record; each inbound message "
            "(institution -> individual) is assessed on receipt against both the "
            "binary test and the non-negotiable accessibility requirements.\n\n"
            "The accessibility requirements are absolute for an email-only RA: no "
            "portal redirect, no telephone requirement, no CAPTCHA, no app-only "
            "verification. A response that imposes any of these is an EA 2010 "
            "ss.20/21 breach regardless of the binary test outcome.\n\n"
            "Every significant inbound response requires a named individual. A "
            "significant response signed only by a team, a department, or a "
            "do-not-reply address is NULL on the binary test and fails the named "
            "individual requirement.\n\n"
            "The reasonable adjustment must be confirmed and recorded before the "
            "first substantive exchange. If the first substantive exchange proceeds "
            "without a confirmed, recorded RA, that is a distinct procedural failure "
            "recorded here.\n\n"
            "Process language ('we responded to your query', 'our team reviewed "
            "your message') does not satisfy the named person or specific facts "
            "elements. Ask directly: 'Please provide the full name and role of the "
            "individual who reviewed my specific case before this response was sent.'"
        )

    def validate_domain_metadata(self, metadata: dict[str, Any]) -> list[str]:
        issues: list[str] = []

        direction = metadata.get("direction")
        if direction not in _DIRECTIONS:
            issues.append(
                f"Unknown message direction '{direction}' — expected "
                f"'{_INBOUND}' or '{_OUTBOUND}'."
            )

        ra_on_record = metadata.get("ra_on_record", False)
        first_exchange = metadata.get("first_substantive_exchange", False)
        ra_confirmed = metadata.get(
            "ra_confirmed_before_first_substantive_exchange", None
        )

        # RA must be confirmed and recorded before the first substantive exchange.
        if first_exchange and ra_confirmed is not True:
            issues.append(
                "First substantive exchange proceeded without the RA confirmed "
                "and recorded beforehand — the RA must be confirmed and recorded "
                "before the first substantive exchange."
            )

        # Accessibility barriers apply to inbound institutional responses.
        if direction == _INBOUND:
            for flag, description in _ACCESSIBILITY_BARRIERS.items():
                if metadata.get(flag):
                    issues.append(description)

            # Named individual required for every significant response.
            if metadata.get("significant_response"):
                named_present = metadata.get("named_individual_provided", None)
                if named_present is None:
                    named_present = metadata.get("_named_person_present", None)
                if named_present is False:
                    issues.append(
                        "Significant inbound response provided no named individual "
                        "— every significant response requires a named individual."
                    )

        return issues

    def _build_domain_metadata(
        self,
        direction: str = "outbound",
        ra_on_record: bool = False,
        ra_description: Optional[str] = None,
        ra_confirmed_before_first_substantive_exchange: Optional[bool] = None,
        first_substantive_exchange: bool = False,
        significant_response: bool = False,
        named_individual_provided: Optional[bool] = None,
        portal_redirect: bool = False,
        telephone_required: bool = False,
        captcha_required: bool = False,
        app_only_verification: bool = False,
        thread_reference: Optional[str] = None,
        message_id: Optional[str] = None,
        regulatory_framework: Optional[str] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        meta: dict[str, Any] = {
            "domain": self.name,
            "direction": direction,
            "ra_on_record": ra_on_record,
            "first_substantive_exchange": first_substantive_exchange,
            "significant_response": significant_response,
            # The four non-negotiable accessibility barriers, always recorded
            # so their absence (False) is as evidential as their presence.
            "portal_redirect": portal_redirect,
            "telephone_required": telephone_required,
            "captcha_required": captcha_required,
            "app_only_verification": app_only_verification,
        }
        if ra_description:
            meta["ra_description"] = ra_description
        if ra_confirmed_before_first_substantive_exchange is not None:
            meta["ra_confirmed_before_first_substantive_exchange"] = (
                ra_confirmed_before_first_substantive_exchange
            )
        if named_individual_provided is not None:
            meta["named_individual_provided"] = named_individual_provided
        if thread_reference:
            meta["thread_reference"] = thread_reference
        if message_id:
            meta["message_id"] = message_id
        if regulatory_framework:
            meta["regulatory_framework"] = regulatory_framework
        meta.update(kwargs)
        return meta
