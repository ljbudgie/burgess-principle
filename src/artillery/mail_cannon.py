"""
mail_cannon.py — The Artillery (Physical Service)

Structures certified physical mail payloads for dispatch via a physical mail
API (e.g., Lob <https://lob.com> or Click2Mail <https://click2mail.com>),
enabling real-world legal service of process.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RecipientAddress:
    """Postal address of the letter recipient."""

    name: str
    line1: str
    line2: str = ""
    city: str = ""
    postcode: str = ""
    country: str = "GB"


@dataclass
class CertifiedLetterPayload:
    """
    A structured, provider-agnostic payload ready for submission to a
    physical mail API.
    """

    recipient: RecipientAddress
    sender_name: str
    sender_reference: str
    pdf_content: bytes
    service_type: str = "certified"
    extra: dict[str, Any] = field(default_factory=dict)


class CertifiedMailSender:
    """
    Prepares and (when configured) dispatches certified physical mail on
    behalf of the Burgess Principle Sovereignty Defense System.

    Pass your mail-API credentials to the constructor.  Currently supported
    providers: ``"lob"`` and ``"click2mail"``.  Leave ``api_key`` empty to
    operate in dry-run / preparation-only mode.

    Usage::

        sender = CertifiedMailSender(api_key="YOUR_LOB_KEY", provider="lob")
        payload = sender.prepare_certified_letter(
            recipient={
                "name": "Eon UK plc — Legal",
                "line1": "Westwood Way",
                "city": "Coventry",
                "postcode": "CV4 8LG",
            },
            pdf_content=open("notice.pdf", "rb").read(),
        )
        # sender.dispatch(payload)  # uncomment once API key is set
    """

    SENDER_NAME = "Burgess Principle SDS"
    SENDER_REFERENCE = "BP-SDS"

    def __init__(
        self,
        api_key: str = "",
        provider: str = "lob",
    ) -> None:
        self.api_key = api_key
        self.provider = provider

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def prepare_certified_letter(
        self,
        recipient: dict[str, str] | RecipientAddress,
        pdf_content: bytes,
        sender_reference: str | None = None,
    ) -> CertifiedLetterPayload:
        """
        Structure the data required to dispatch a certified physical letter.

        *recipient* may be a :class:`RecipientAddress` instance or a plain
        ``dict`` with keys ``name``, ``line1``, and optionally ``line2``,
        ``city``, ``postcode``, ``country``.

        Returns a :class:`CertifiedLetterPayload` that can be inspected,
        logged, and eventually passed to :meth:`dispatch`.
        """
        if isinstance(recipient, dict):
            recipient = RecipientAddress(**recipient)

        return CertifiedLetterPayload(
            recipient=recipient,
            sender_name=self.SENDER_NAME,
            sender_reference=sender_reference if sender_reference is not None else self.SENDER_REFERENCE,
            pdf_content=pdf_content,
            service_type="certified",
        )

    def dispatch(self, payload: CertifiedLetterPayload) -> dict[str, Any]:
        """
        Send *payload* to the configured mail API and return the provider
        response as a dict.

        This method is a **placeholder**.  To activate:

        * For **Lob**: ``pip install lob`` then replace the stub body with::

            import lob
            lob.api_key = self.api_key
            response = lob.Letter.create(
                description=payload.sender_reference,
                to_address={...},  # build from payload.recipient
                from_address={...},
                file=payload.pdf_content,
                color=False,
            )
            return dict(response)

        * For **Click2Mail**: use their REST API with ``requests``.
        """
        # TODO: wire up real API call using self.api_key and self.provider
        if not self.api_key:
            return {
                "status": "dry_run",
                "provider": self.provider,
                "recipient": payload.recipient.name,
                "message": "Set api_key to enable physical dispatch.",
            }
        raise NotImplementedError(
            f"Dispatch for provider '{self.provider}' is not yet implemented. "
            "Follow the instructions in the docstring above."
        )
