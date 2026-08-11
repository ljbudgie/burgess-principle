"""Local-first, advisory classifier for recurring institutional delay patterns."""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from datetime import date
from typing import Any, Sequence

__all__ = ["classify_thread", "LoopFinding", "DISCLAIMER"]

DISCLAIMER = (
    "Advisory classification only. A named human must confirm this finding before "
    "it is recorded, published, or relied upon."
)
_TYPES = (
    "insufficiency",
    "circular_referral",
    "precondition_stacking",
    "template_dismissal",
    "identity_loop",
    "channel_redirect",
)
_INDIVIDUAL = {"individual", "user", "claimant", "customer", "you"}
_INSUFFICIENT = re.compile(
    r"\b(?:not|isn't|is not|still not)\s+sufficient\b|\bprovide\s+(?:more|further|additional)\b",
    re.IGNORECASE,
)
_PRECONDITION = re.compile(r"\b(?:cannot|can't|unable to|won't)\b.{0,80}\buntil\b", re.IGNORECASE)
_IDENTITY = re.compile(
    r"\b(?:verify|verification|confirm)\b.{0,60}\b(?:identity|yourself|account)\b",
    re.IGNORECASE,
)
_CHANNEL = re.compile(r"\b(?:call|phone|telephone|visit|in person)\b", re.IGNORECASE)
_EMAIL_ONLY = re.compile(r"\b(?:email[- ]only|written[- ]only|do not (?:call|phone))\b", re.IGNORECASE)
_IDENTITY_CONFIRMED = re.compile(
    r"\b(?:identity|identification|id)\b.{0,60}\b(?:provided|confirmed|verified|supplied)\b"
    r"|\b(?:provided|confirmed|verified|supplied)\b.{0,60}\b(?:identity|identification|id)\b",
    re.IGNORECASE,
)
_TEMPLATE = re.compile(r"\b(?:all points (?:have been )?addressed|standard response)\b", re.IGNORECASE)
_REFERRAL = re.compile(r"\b(?:contact|refer(?:red)? to|speak to)\s+([A-Z][\w&' -]{1,50})", re.IGNORECASE)


@dataclass(frozen=True)
class _Message:
    date: date
    sender: str
    content_summary: str
    direction: str
    reference: str


@dataclass(frozen=True)
class LoopFinding:
    """A schema-compatible provisional finding."""

    loop_detected: bool
    loop_type: str | None
    loop_count: int
    days_consumed: int
    institution: str
    named_individual: str | None
    correspondence_refs: list[str]
    accountability_finding: str
    summary: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "loop_detected": self.loop_detected,
            "loop_type": self.loop_type,
            "loop_count": self.loop_count,
            "days_consumed": self.days_consumed,
            "institution": self.institution,
            "named_individual": self.named_individual,
            "correspondence_refs": self.correspondence_refs,
            "accountability_finding": self.accountability_finding,
            "summary": self.summary,
            "provisional": True,
            "requires_human_confirmation": True,
            "disclaimer": DISCLAIMER,
        }


def _parse_messages(messages: Sequence[dict[str, Any]]) -> list[_Message]:
    if not isinstance(messages, Sequence) or isinstance(messages, (str, bytes)) or not messages:
        raise ValueError("messages must be a non-empty array.")
    if len(messages) > 500:
        raise ValueError("messages must contain at most 500 items.")
    parsed: list[_Message] = []
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            raise ValueError(f"messages[{index}] must be an object.")
        raw_date = message.get("date")
        sender = message.get("sender")
        content = message.get("content_summary")
        if not all(isinstance(value, str) and value.strip() for value in (raw_date, sender, content)):
            raise ValueError(
                f"messages[{index}] must include non-empty date, sender, and content_summary strings."
            )
        if len(content) > 20_000:
            raise ValueError(f"messages[{index}].content_summary is too long.")
        try:
            message_date = date.fromisoformat(raw_date[:10])
        except ValueError as exc:
            raise ValueError(f"messages[{index}].date must start with an ISO-8601 date.") from exc
        direction = str(message.get("direction", "")).strip().lower()
        if direction not in {"institution", "individual"}:
            direction = "individual" if sender.strip().lower() in _INDIVIDUAL else "institution"
        reference = str(message.get("reference") or raw_date[:10]).strip()
        parsed.append(_Message(message_date, sender.strip(), content.strip(), direction, reference))
    return sorted(parsed, key=lambda message: message.date)


def _count_insufficiency(messages: list[_Message]) -> tuple[int, list[int]]:
    flagged = [index for index, message in enumerate(messages)
               if message.direction == "institution" and _INSUFFICIENT.search(message.content_summary)]
    cycles = 0
    evidence: list[int] = []
    for first, second in zip(flagged, flagged[1:]):
        if any(message.direction == "individual" for message in messages[first + 1:second]):
            cycles += 1
            evidence.extend((first, second))
    return cycles, evidence


def _count_circular_referral(messages: list[_Message]) -> tuple[int, list[int]]:
    routes: list[tuple[str, int]] = []
    for index, message in enumerate(messages):
        if message.direction == "institution":
            match = _REFERRAL.search(message.content_summary)
            if match:
                routes.append((match.group(1).strip().lower(), index))
    cycles = 0
    evidence: list[int] = []
    for (first_route, first_index), (second_route, second_index), (third_route, third_index) in zip(
        routes, routes[1:], routes[2:]
    ):
        if first_route == third_route and first_route != second_route:
            cycles += 1
            evidence.extend((first_index, second_index, third_index))
    return cycles, evidence


def _count_preconditions(messages: list[_Message]) -> tuple[int, list[int]]:
    evidence = [index for index, message in enumerate(messages)
                if message.direction == "institution" and _PRECONDITION.search(message.content_summary)]
    return len(evidence), evidence


def _count_templates(messages: list[_Message]) -> tuple[int, list[int]]:
    institutional = [(index, message.content_summary) for index, message in enumerate(messages)
                     if message.direction == "institution"]
    evidence = [index for index, content in institutional if _TEMPLATE.search(content)]
    for position, (index, content) in enumerate(institutional):
        for other_index, other_content in institutional[position + 1:]:
            if difflib.SequenceMatcher(None, content.lower(), other_content.lower()).ratio() >= 0.88:
                evidence.extend((index, other_index))
    evidence = sorted(set(evidence))
    return len(evidence) // 2 if len(evidence) > 1 else 0, evidence


def _count_identity(messages: list[_Message]) -> tuple[int, list[int]]:
    identity_confirmed = False
    cycles = 0
    evidence: list[int] = []
    for index, message in enumerate(messages):
        if message.direction == "individual" and _IDENTITY_CONFIRMED.search(message.content_summary):
            identity_confirmed = True
        elif (
            identity_confirmed
            and message.direction == "institution"
            and _IDENTITY.search(message.content_summary)
        ):
            cycles += 1
            evidence.append(index)
    return cycles, evidence


def _count_channel_redirect(messages: list[_Message]) -> tuple[int, list[int]]:
    email_only_seen = False
    evidence: list[int] = []
    for index, message in enumerate(messages):
        if message.direction == "individual" and _EMAIL_ONLY.search(message.content_summary):
            email_only_seen = True
        elif email_only_seen and message.direction == "institution" and _CHANNEL.search(message.content_summary):
            evidence.append(index)
    return len(evidence), evidence


def classify_thread(
    messages: Sequence[dict[str, Any]],
    institution: str | None = None,
    named_individual: str | None = None,
) -> LoopFinding:
    """Classify a correspondence thread without sending it beyond the local process."""
    parsed = _parse_messages(messages)
    if institution is not None and not isinstance(institution, str):
        raise ValueError("institution must be a string or null.")
    if named_individual is not None and not isinstance(named_individual, str):
        raise ValueError("named_individual must be a string or null.")
    detectors = {
        "insufficiency": _count_insufficiency(parsed),
        "circular_referral": _count_circular_referral(parsed),
        "precondition_stacking": _count_preconditions(parsed),
        "template_dismissal": _count_templates(parsed),
        "identity_loop": _count_identity(parsed),
        "channel_redirect": _count_channel_redirect(parsed),
    }
    loop_type, (loop_count, evidence) = max(detectors.items(), key=lambda item: item[1][0])
    loop_detected = loop_count > 0
    refs = [parsed[index].reference for index in sorted(set(evidence))]
    named_individual = named_individual.strip() if named_individual else None
    resolved_institution = (institution or "").strip() or next(
        (message.sender for message in parsed if message.direction == "institution"), "Unspecified institution"
    )
    accountability = "SOVEREIGN" if named_individual else "NULL"
    days = (parsed[-1].date - parsed[0].date).days if loop_detected else 0
    if loop_detected:
        accountable = f"named individual {named_individual}" if named_individual else "no named individual"
        summary = (
            f"LOOP DETECTED: {resolved_institution} shows a {loop_type.replace('_', ' ')} "
            f"pattern across {loop_count} cycle(s) over {days} day(s), with {accountable} identified."
        )
    else:
        loop_type = None
        summary = f"NO LOOP: no classified delay pattern was detected in the supplied correspondence."
    return LoopFinding(
        loop_detected=loop_detected,
        loop_type=loop_type,
        loop_count=loop_count if loop_detected else 0,
        days_consumed=days,
        institution=resolved_institution,
        named_individual=named_individual,
        correspondence_refs=refs,
        accountability_finding=accountability,
        summary=summary,
    )
