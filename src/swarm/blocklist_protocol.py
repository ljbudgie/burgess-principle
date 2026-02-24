"""
blocklist_protocol.py — The Swarm (Federated Defense)

Defines the canonical JSON schema for a "Void Entity" (a bad actor whose
actions have been found void ab initio) and provides utilities for building,
validating, and exporting shareable threat-intelligence feeds.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

VOID_ENTITY_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://burgessprinciple.co.uk/schemas/void_entity.json",
    "title": "VoidEntity",
    "description": (
        "A legal or corporate entity whose warrant or enforcement action has "
        "been found void ab initio under the Burgess Principle."
    ),
    "type": "object",
    "required": ["entity_id", "name", "void_reason", "date_recorded"],
    "properties": {
        "entity_id": {
            "type": "string",
            "description": "Unique identifier for this void-entity record (UUID recommended).",
        },
        "name": {
            "type": "string",
            "description": "Legal name of the entity.",
        },
        "registration_number": {
            "type": "string",
            "description": "Companies House or equivalent registration number (optional).",
        },
        "void_reason": {
            "type": "string",
            "description": "Plain-English description of the defect that caused voidness.",
        },
        "warrant_reference": {
            "type": "string",
            "description": "Reference number of the defective warrant (if available).",
        },
        "date_of_void_action": {
            "type": "string",
            "format": "date",
            "description": "ISO 8601 date on which the void action occurred.",
        },
        "date_recorded": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 datetime at which this record was added to the ledger.",
        },
        "evidence_hash": {
            "type": "string",
            "description": "SHA-256 hash of the supporting notice/evidence document.",
        },
        "downstream_harms": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of downstream unlawful consequences (debt entry, credit reporting, etc.).",
        },
        "status": {
            "type": "string",
            "enum": ["active", "settled", "disputed", "withdrawn"],
            "description": "Current status of the void-entity record.",
        },
    },
    "additionalProperties": False,
}

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def make_void_entity(
    entity_id: str,
    name: str,
    void_reason: str,
    warrant_reference: str | None = None,
    date_of_void_action: str | None = None,
    evidence_hash: str | None = None,
    downstream_harms: list[str] | None = None,
    registration_number: str | None = None,
    status: str = "active",
) -> dict[str, Any]:
    """
    Construct a Void Entity record conforming to :data:`VOID_ENTITY_SCHEMA`.

    ``date_recorded`` is set automatically to the current UTC datetime.
    """
    record: dict[str, Any] = {
        "entity_id": entity_id,
        "name": name,
        "void_reason": void_reason,
        "date_recorded": datetime.now(tz=timezone.utc).isoformat(),
        "status": status,
    }
    if registration_number is not None:
        record["registration_number"] = registration_number
    if warrant_reference is not None:
        record["warrant_reference"] = warrant_reference
    if date_of_void_action is not None:
        record["date_of_void_action"] = date_of_void_action
    if evidence_hash is not None:
        record["evidence_hash"] = evidence_hash
    if downstream_harms is not None:
        record["downstream_harms"] = downstream_harms
    return record


def export_threat_intelligence(
    void_entities: list[dict[str, Any]],
    feed_version: str = "1.0",
) -> str:
    """
    Generate a shareable JSON threat-intelligence feed from a list of Void
    Entity records.

    The output is a JSON string containing metadata about the feed and the
    full list of void entities.  It can be published to a public URL or
    shared peer-to-peer so that allied systems can import the blocklist.

    Example::

        entities = [
            make_void_entity(
                entity_id="ent-001",
                name="Eon UK plc",
                void_reason="Warrant lacked proper facial description of premises.",
                warrant_reference="WAR-2024-00123",
                date_of_void_action="2024-03-15",
                downstream_harms=["credit entry", "debt registration"],
            )
        ]
        feed_json = export_threat_intelligence(entities)
        print(feed_json)
    """
    feed: dict[str, Any] = {
        "feed_id": "burgess-principle-void-entity-feed",
        "feed_version": feed_version,
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "schema_ref": VOID_ENTITY_SCHEMA["$id"],
        "total_records": len(void_entities),
        "void_entities": void_entities,
    }
    return json.dumps(feed, indent=2, ensure_ascii=False)
