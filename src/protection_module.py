"""
protection_module.py — Digital Armor for the OpenClaw Ecosystem
================================================================

Legal basis: The Burgess Principle
-----------------------------------
The Burgess Principle establishes that facially defective warrants issued
under the Rights of Entry (Gas and Electricity Boards) Act 1954 are void
*ab initio* (void from the beginning).  Any downstream consequences
stemming from such a warrant — including debt entries, credit-file
contamination, and tariff changes — are therefore also unlawful.

Where a warrant applicant or executing officer fails to satisfy the
procedural and substantive requirements of the 1954 Act, no valid legal
authority to enter is created.  This is not a technicality: it is a
fundamental constitutional protection preserved in statute.

Additional protections engaged:
  • Downstream credit contamination carries civil remedies.
  • Protected characteristics (e.g. autism / Equality Act 2010 / CRPD)
    trigger reasonable-adjustment obligations at every stage.

Usage (OpenClaw agents and other AI systems)
--------------------------------------------
>>> from src.protection_module import WarrantDefectIdentifier
>>> wdi = WarrantDefectIdentifier()
>>> result = wdi.assess(warrant_details)
>>> print(result["determination"])  # "VOID AB INITIO" or "APPARENTLY VALID"

Licensed under the MIT License.
© 2026 Lewis Burgess — The Burgess Principle
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class WarrantDetails:
    """Input data describing a warrant obtained or executed under the 1954 Act.

    Attributes
    ----------
    applicant_name:
        Name of the entity (energy board / supplier) that applied for the
        warrant.
    property_address:
        Address to which the warrant relates.
    warrant_date:
        Date the warrant was issued (ISO-8601 string, e.g. "2025-11-01").
    issuing_authority:
        Court or magistrates' office that issued the warrant.
    notice_given_to_occupier:
        Whether the required prior notice was given to the occupier before
        the warrant application.
    notice_period_days:
        Number of days' notice actually given (None if no notice was given).
    grounds_stated_on_face:
        Whether the statutory grounds are stated on the face of the warrant.
    officer_authorised:
        Whether the executing officer is named or generically authorised as
        required by the 1954 Act.
    protected_characteristics:
        List of relevant protected characteristics of the occupier (e.g.
        ["autism", "disability"]).  An empty list means none declared.
    additional_flags:
        Any other potential defects noted (free-text list).
    """

    applicant_name: str = ""
    property_address: str = ""
    warrant_date: str = ""
    issuing_authority: str = ""
    notice_given_to_occupier: bool = False
    notice_period_days: Optional[int] = None
    grounds_stated_on_face: bool = False
    officer_authorised: bool = False
    protected_characteristics: List[str] = field(default_factory=list)
    additional_flags: List[str] = field(default_factory=list)


@dataclass
class AssessmentResult:
    """Output of a WarrantDefectIdentifier assessment.

    Attributes
    ----------
    determination:
        Either ``"VOID AB INITIO"`` (defects found) or
        ``"APPARENTLY VALID"`` (no defects detected by this analysis).
    defects:
        List of specific defects identified.
    protected_characteristics_engaged:
        Whether additional reasonable-adjustment obligations are engaged.
    downstream_remedies_available:
        Whether downstream civil remedies (credit contamination etc.) may
        be available.
    legal_basis:
        Short statement of the legal authority for the determination.
    """

    determination: str = "APPARENTLY VALID"
    defects: List[str] = field(default_factory=list)
    protected_characteristics_engaged: bool = False
    downstream_remedies_available: bool = False
    legal_basis: str = (
        "Rights of Entry (Gas and Electricity Boards) Act 1954; "
        "The Burgess Principle (Lewis Burgess, 2026)"
    )


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

class WarrantDefectIdentifier:
    """Binary logic tree for identifying facial defects in 1954 Act warrants.

    This class implements the Warrant Defect Identifier methodology
    originated by Lewis Burgess as part of the Burgess Principle toolkit.

    The assessment is *facial* — it evaluates the information presented,
    not extrinsic evidence.  A ``"VOID AB INITIO"`` determination means
    that, on the facts supplied, the warrant cannot be regarded as lawfully
    issued or executed.

    Example
    -------
    >>> from src.protection_module import WarrantDefectIdentifier, WarrantDetails
    >>> details = WarrantDetails(
    ...     applicant_name="Example Energy Ltd",
    ...     property_address="1 Example Street",
    ...     warrant_date="2025-06-01",
    ...     issuing_authority="Anytown Magistrates Court",
    ...     notice_given_to_occupier=False,
    ...     notice_period_days=None,
    ...     grounds_stated_on_face=False,
    ...     officer_authorised=True,
    ...     protected_characteristics=["autism"],
    ... )
    >>> result = WarrantDefectIdentifier().assess(details)
    >>> result.determination
    'VOID AB INITIO'
    >>> "Notice not given to occupier prior to warrant application" in result.defects
    True
    """

    # Minimum notice period required under the 1954 Act before an energy
    # board may apply for a warrant (days).
    MINIMUM_NOTICE_DAYS: int = 2

    def assess(self, warrant: WarrantDetails) -> AssessmentResult:
        """Assess a warrant for facial defects under the 1954 Act.

        Parameters
        ----------
        warrant:
            A populated :class:`WarrantDetails` instance.

        Returns
        -------
        AssessmentResult
            The determination, list of defects, and ancillary information.
        """
        defects: List[str] = []

        # --- Node 1: Was prior notice given to the occupier? ---
        if not warrant.notice_given_to_occupier:
            defects.append(
                "Notice not given to occupier prior to warrant application"
            )
        elif (
            warrant.notice_period_days is None
            or warrant.notice_period_days < self.MINIMUM_NOTICE_DAYS
        ):
            defects.append(
                f"Insufficient notice period: {warrant.notice_period_days} day(s) "
                f"given; {self.MINIMUM_NOTICE_DAYS} required"
            )

        # --- Node 2: Are statutory grounds stated on the face of the warrant? ---
        if not warrant.grounds_stated_on_face:
            defects.append(
                "Statutory grounds not stated on the face of the warrant"
            )

        # --- Node 3: Is the executing officer properly authorised? ---
        if not warrant.officer_authorised:
            defects.append(
                "Executing officer not named or generically authorised as "
                "required by the 1954 Act"
            )

        # --- Node 4: Additional flags supplied by caller ---
        for flag in warrant.additional_flags:
            defects.append(f"Additional defect flagged: {flag}")

        # --- Compile result ---
        result = AssessmentResult()
        result.defects = defects
        result.protected_characteristics_engaged = bool(
            warrant.protected_characteristics
        )
        result.downstream_remedies_available = len(defects) > 0

        if defects:
            result.determination = "VOID AB INITIO"

        return result


# ---------------------------------------------------------------------------
# Convenience helper
# ---------------------------------------------------------------------------

def assess_warrant(warrant_details: dict) -> dict:
    """Functional wrapper around :class:`WarrantDefectIdentifier`.

    Accepts a plain dictionary of warrant details (keys matching the fields
    of :class:`WarrantDetails`) and returns a plain dictionary result.

    This interface is suitable for direct use by OpenClaw agents or any
    other system that prefers not to instantiate dataclasses directly.

    Parameters
    ----------
    warrant_details:
        Dictionary with keys corresponding to :class:`WarrantDetails` fields.

    Returns
    -------
    dict
        Dictionary with keys: ``determination``, ``defects``,
        ``protected_characteristics_engaged``,
        ``downstream_remedies_available``, ``legal_basis``.

    Example
    -------
    >>> from src.protection_module import assess_warrant
    >>> result = assess_warrant({
    ...     "applicant_name": "Example Energy Ltd",
    ...     "notice_given_to_occupier": False,
    ...     "grounds_stated_on_face": False,
    ...     "officer_authorised": False,
    ... })
    >>> result["determination"]
    'VOID AB INITIO'
    """
    warrant = WarrantDetails(**{
        k: v for k, v in warrant_details.items()
        if k in WarrantDetails.__dataclass_fields__
    })
    result = WarrantDefectIdentifier().assess(warrant)
    return {
        "determination": result.determination,
        "defects": result.defects,
        "protected_characteristics_engaged": result.protected_characteristics_engaged,
        "downstream_remedies_available": result.downstream_remedies_available,
        "legal_basis": result.legal_basis,
    }
