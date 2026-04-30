"""Iris helper modules."""

from .claim_builder import auto_generate_claim

# Single source of truth for the Iris assistant version.
# Surfaced by iris-local.py (banner, /api/version) and the PWA footer.
# Keep in sync with the [project].version field in pyproject.toml.
__version__ = "1.3.0"

__all__ = ["auto_generate_claim", "__version__"]
