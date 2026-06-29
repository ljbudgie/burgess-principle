"""
BaseDomain — abstract base class for all domain implementations.

A domain wraps the core binary test to provide:
- Domain-specific metadata fields
- Domain-specific validation rules (beyond the five core elements)
- Guidance text tailored to the domain context
- A factory method that produces a sealed DecisionRecord in one call

To add a new domain, subclass BaseDomain and override:
- `name` (class attribute)
- `validate_domain_metadata` (optional additional checks)
- `guidance` (human-readable guidance for assessors in this domain)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..core.binary_test import BinaryTest
from ..core.decision_record import DecisionRecord


class BaseDomain(ABC):
    """Abstract base for domain-specific oversight assessors."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Machine-readable domain name, e.g. 'communication'."""
        ...

    @property
    @abstractmethod
    def guidance(self) -> str:
        """
        Human-readable guidance for assessors operating in this domain.
        Returned as part of the DecisionRecord's domain_metadata.
        """
        ...

    def validate_domain_metadata(self, metadata: dict[str, Any]) -> list[str]:
        """
        Domain-specific validation of metadata fields.
        Return a list of issue strings; empty list = valid.
        Override in subclasses to add domain-specific checks.
        """
        return []

    def create_record(
        self,
        *,
        subject: str,
        institution: str,
        binary_test: BinaryTest,
        decision_date: Optional[str] = None,
        assessor: Optional[str] = None,
        notes: Optional[str] = None,
        ambiguous_if_missing: bool = False,
        **domain_kwargs: Any,
    ) -> DecisionRecord:
        """
        Create a sealed DecisionRecord for this domain.

        domain_kwargs are domain-specific metadata fields.
        Each subclass documents the supported kwargs.
        """
        domain_metadata = self._build_domain_metadata(**domain_kwargs)
        issues = self.validate_domain_metadata(domain_metadata)
        if issues:
            # Surface validation issues as metadata rather than raising,
            # so the record is still created and the issues are preserved.
            domain_metadata["_validation_issues"] = issues

        return DecisionRecord.create(
            subject=subject,
            institution=institution,
            binary_test=binary_test,
            domain=self.name,
            decision_date=decision_date,
            assessor=assessor,
            domain_metadata=domain_metadata,
            notes=notes,
            ambiguous_if_missing=ambiguous_if_missing,
        )

    def _build_domain_metadata(self, **kwargs: Any) -> dict[str, Any]:
        """Merge domain kwargs with standard domain metadata."""
        return {"domain": self.name, **kwargs}
