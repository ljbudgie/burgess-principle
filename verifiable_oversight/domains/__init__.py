"""
Domain implementations for Verifiable Human Oversight.

Each domain extends the core binary test with domain-specific
metadata, validation, and guidance. Import the domain you need:

    from verifiable_oversight.domains.communication import CommunicationDomain
    from verifiable_oversight.domains.legal import LegalDomain
"""

from .base import BaseDomain
from .general import GeneralDomain
from .communication import CommunicationDomain
from .legal import LegalDomain

__all__ = ["BaseDomain", "GeneralDomain", "CommunicationDomain", "LegalDomain"]
