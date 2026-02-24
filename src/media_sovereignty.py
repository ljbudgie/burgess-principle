"""
Media Sovereignty Module — Burgess Principle
Applies Void Ab Initio and Sovereignty logic to music and media copyright disputes.
"""

from datetime import datetime, timezone


REQUIRED_PROOFS = {"wet_ink_signature", "sworn_affidavit_of_ownership"}

COUNTER_NOTICE_TEMPLATE = (
    "NOTICE OF INVALID CLAIM\n\n"
    "RE: {work_title}\n"
    "Claimant: {claimant}\n"
    "Platform: {platform}\n"
    "Date: {date}\n\n"
    "The claim against [{work_title}] is Void Ab Initio. Under Article 29 of the Magna Carta "
    "and the Burgess Principle, no automated system may deprive a sovereign of property without "
    "due process. The purported claim by [{claimant}] on [{platform}] is hereby rebutted in its "
    "entirety on the following grounds:\n\n"
    "1. The claim lacks the required proof of ownership (wet ink signature and/or sworn "
    "affidavit of ownership).\n"
    "2. An automated copyright strike, absent verified human attestation, cannot extinguish "
    "the natural rights of a sovereign individual.\n"
    "3. Pursuant to the Burgess Principle, all downstream consequences of this void claim — "
    "including but not limited to demonetisation, content removal, or account penalties — "
    "are themselves void ab initio and must be reversed forthwith.\n\n"
    "This notice is served under the authority of the Burgess Principle and the common law "
    "rights preserved by Magna Carta. All rights reserved. Without prejudice.\n"
)


class MediaRightsDefender:
    """Evaluates copyright claims and generates counter-notices under the Burgess Principle."""

    def evaluate_copyright_claim(self, claim_data: dict) -> dict:
        """
        Evaluate whether a copyright claim is valid or void ab initio.

        Args:
            claim_data: Dictionary with keys: claimant, platform, work_title, legal_basis,
                        and optionally proofs (set/list of proof types provided).

        Returns:
            Dictionary with 'status' ('VOID' or 'VALID') and 'reason'.
        """
        proofs_provided = set(claim_data.get("proofs", []))
        missing_proofs = REQUIRED_PROOFS - proofs_provided

        legal_basis = claim_data.get("legal_basis", "")
        automated = claim_data.get("automated", True)

        if missing_proofs:
            return {
                "status": "VOID",
                "reason": (
                    f"Claim is Void Ab Initio: missing required proofs: "
                    f"{', '.join(sorted(missing_proofs))}."
                ),
            }

        if automated and not legal_basis:
            return {
                "status": "VOID",
                "reason": (
                    "Claim is Void Ab Initio: automated claim with no stated legal basis "
                    "violates Sovereignty rights under the Burgess Principle."
                ),
            }

        return {"status": "VALID", "reason": "Claim provides required proofs and legal basis."}

    def generate_counter_notice(self, claim_data: dict) -> str:
        """
        Generate a formal counter-notice asserting Sovereignty and Magna Carta rights.

        Args:
            claim_data: Dictionary with keys: claimant, platform, work_title.

        Returns:
            Formal legal text rebutting the claim.
        """
        return COUNTER_NOTICE_TEMPLATE.format(
            work_title=claim_data.get("work_title", "UNKNOWN WORK"),
            claimant=claim_data.get("claimant", "UNKNOWN CLAIMANT"),
            platform=claim_data.get("platform", "UNKNOWN PLATFORM"),
            date=datetime.now(timezone.utc).strftime("%d %B %Y"),
        )
