"""
LLMJurist — Prompt-template engine for the Burgess Principle defense system.

Generates structured legal-argument prompts for Energy, Water, and Council Tax
sectors.  Each template can be passed to any LLM to produce a tailored formal
defense letter; the templates themselves contain all key statutory references.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

SECTORS = ("energy", "water", "council")


@dataclass
class LLMJurist:
    """Builds LLM prompt templates for three utility/council sectors."""

    templates: Dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        self.templates = {
            "energy": self._energy_template(),
            "water": self._water_template(),
            "council": self._council_template(),
        }

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def get_prompt(self, sector: str, context: dict) -> str:
        """Return a filled prompt for *sector* using *context* key/values.

        Parameters
        ----------
        sector:
            One of ``"energy"``, ``"water"``, or ``"council"``.
        context:
            Mapping of placeholder names to replacement values.
            Typical keys: ``name``, ``address``, ``supplier``, ``date``.

        Raises
        ------
        ValueError
            If *sector* is not recognised.
        """
        sector = sector.lower()
        if sector not in self.templates:
            raise ValueError(
                f"Unknown sector '{sector}'. Must be one of: {', '.join(SECTORS)}"
            )
        prompt = self.templates[sector]
        for key, value in context.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        return prompt

    def list_sectors(self) -> list[str]:
        """Return the list of supported sectors."""
        return list(self.templates.keys())

    # ------------------------------------------------------------------ #
    #  Template definitions                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _energy_template() -> str:
        return (
            "You are a specialist UK administrative-law advocate.\n\n"
            "Draft a formal legal defense letter for the following client:\n"
            "  Name:     {name}\n"
            "  Address:  {address}\n"
            "  Supplier: {supplier}\n"
            "  Date:     {date}\n\n"
            "LEGAL BASIS — ENERGY SECTOR:\n"
            "1. Rights of Entry (Gas and Electricity Boards) Act 1954: any warrant of\n"
            "   entry issued without individual judicial consideration of the specific\n"
            "   facts is void ab initio.\n"
            "2. Bulk-warrant processing (hundreds of warrants per session) makes it\n"
            "   mathematically impossible to satisfy the Act's requirement of judicial\n"
            "   scrutiny (R v Sussex Justices, Ex parte McCarthy [1924] 1 KB 256).\n"
            "3. All downstream consequences of a void warrant — debt registration,\n"
            "   credit reporting, tariff changes — are therefore unlawful.\n\n"
            "INSTRUCTIONS:\n"
            "- Address the letter to {supplier}.\n"
            "- Demand proof of individual judicial consideration within 14 days.\n"
            "- Warn that entry relying on a bulk-issued warrant constitutes trespass.\n"
            "- Cite the Burgess Principle and the authorities above.\n"
            "- Maintain a firm, professional, and legally precise tone.\n"
        )

    @staticmethod
    def _water_template() -> str:
        return (
            "You are a specialist UK water-industry and public-law advocate.\n\n"
            "Draft a formal legal challenge letter for the following client:\n"
            "  Name:     {name}\n"
            "  Address:  {address}\n"
            "  Supplier: {supplier}\n"
            "  Date:     {date}\n\n"
            "LEGAL BASIS — WATER SECTOR:\n"
            "1. Water Industry Act 1991, Section 174: creates criminal liability for\n"
            "   obstruction of authorised persons, but presupposes that the authority\n"
            "   to act is itself lawfully established.\n"
            "2. Any right of entry must derive from a specific statutory provision or\n"
            "   a court order obtained following individual judicial consideration of\n"
            "   the facts relating to the specific property.\n"
            "3. Where the water undertaker cannot evidence individual judicial\n"
            "   scrutiny, no lawful obligation to permit entry arises.\n\n"
            "INSTRUCTIONS:\n"
            "- Address the letter to {supplier}.\n"
            "- Demand documentary proof of authority to enter within 14 days.\n"
            "- Reserve all rights to treat unauthorised entry as trespass.\n"
            "- Cite the Water Industry Act 1991 and relevant case law.\n"
            "- Maintain a firm, professional, and legally precise tone.\n"
        )

    @staticmethod
    def _council_template() -> str:
        return (
            "You are a specialist UK local-government finance and public-law advocate.\n\n"
            "Draft a formal legal challenge letter for the following client:\n"
            "  Name:      {name}\n"
            "  Address:   {address}\n"
            "  Authority: {supplier}\n"
            "  Date:      {date}\n\n"
            "LEGAL BASIS — COUNCIL TAX SECTOR:\n"
            "1. Local Government Finance Act 1992 and the Council Tax (Administration\n"
            "   and Enforcement) Regulations 1992 (SI 1992/613): a Liability Order is\n"
            "   only validly obtained after proper service of a demand notice and\n"
            "   reminder notice, and a properly constituted Magistrates' Court hearing.\n"
            "2. A Liability Order granted without individual judicial consideration,\n"
            "   or on the basis of incorrectly served notices, is susceptible to\n"
            "   challenge and potential set-aside.\n"
            "3. The billing authority bears the burden of proving valid service and\n"
            "   proper procedure at every stage.\n\n"
            "INSTRUCTIONS:\n"
            "- Address the letter to {supplier}.\n"
            "- Demand certified copies of all notices and the Liability Order within\n"
            "  14 days, including proof of service.\n"
            "- Reserve the right to apply to the Magistrates' Court to set aside any\n"
            "  defective Liability Order.\n"
            "- Reference the right to complain to the Local Government Ombudsman.\n"
            "- Maintain a firm, professional, and legally precise tone.\n"
        )
