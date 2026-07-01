"""
Integrations for Verifiable Human Oversight.

These modules adapt the core engine to specific runtimes. The first is Iris —
the conversational assistant in this repository — via a runtime-agnostic
:class:`~verifiable_oversight.integrations.iris.ConversationAssessor` that any
conversational agent can call to create and verify records mid-conversation.
"""

from .iris import (
    ConversationAssessor,
    ConversationAssessment,
    FOLLOW_UP_QUESTIONS,
    follow_up_questions_for,
)

__all__ = [
    "ConversationAssessor",
    "ConversationAssessment",
    "FOLLOW_UP_QUESTIONS",
    "follow_up_questions_for",
]
