"""
Verifiable Human Oversight — core package.

Exports the primary public API:
    BinaryTest, Verdict, DecisionRecord, Verifier
"""

from .binary_test import BinaryTest, Verdict, BinaryTestResult
from .decision_record import DecisionRecord
from .verifier import Verifier, VerificationReport
from .signing import (
    RecordSigner,
    SigningError,
    verify_record_signature,
    signing_message,
    SIGNING_CONTEXT,
)
from .storage import (
    RecordStore,
    LedgerEntry,
    StorageError,
    compute_entry_hash,
    CHAIN_CONTEXT,
    GENESIS_HASH,
)
from .registry import Institution, InstitutionRegistry
from .deadlines import (
    DeadlineStatus,
    DeadlineProfile,
    DeadlineResult,
    DeadlineEngine,
    STANDARD_PROFILES,
)

__all__ = [
    "BinaryTest",
    "Verdict",
    "BinaryTestResult",
    "DecisionRecord",
    "Verifier",
    "VerificationReport",
    "RecordSigner",
    "SigningError",
    "verify_record_signature",
    "signing_message",
    "SIGNING_CONTEXT",
    "RecordStore",
    "LedgerEntry",
    "StorageError",
    "compute_entry_hash",
    "CHAIN_CONTEXT",
    "GENESIS_HASH",
    "Institution",
    "InstitutionRegistry",
    "DeadlineStatus",
    "DeadlineProfile",
    "DeadlineResult",
    "DeadlineEngine",
    "STANDARD_PROFILES",
]
