"""
llm_jurist.py — The Brain (AI Council)

Provides an interface for connecting to a local or remote LLM (e.g., via
Ollama or a generic OpenAI-compatible API) to draft legal arguments on behalf
of the Burgess Principle Sovereignty Defense System.
"""

from __future__ import annotations

import json
from typing import Any

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

VOID_AB_INITIO_TEMPLATE = """
You are a specialist legal drafter acting on behalf of the Burgess Principle
Sovereignty Defense System.

Draft a formal Notice of Void Ab Initio based on the following particulars:

  Recipient:        {recipient}
  Warrant Reference: {warrant_ref}
  Defect Identified:{defect_description}
  Date of Entry:    {date_of_entry}

The notice must:
1. Cite the Rights of Entry (Gas and Electricity Boards) Act 1954 and explain
   the facial defect that renders the warrant void ab initio.
2. Reference Magna Carta Article 29 as the foundational sovereign authority.
3. Cite relevant case law establishing void ab initio consequences (e.g.,
   Anisminic Ltd v Foreign Compensation Commission [1969] 2 AC 147;
   R v Secretary of State for the Home Department, ex parte Pierson [1998]
   AC 539).
4. Enumerate all downstream unlawful consequences: debt entry, credit
   reporting, tariff changes.
5. State the remedies sought, including credit remediation and damages for
   breach of the Equality Act 2010 where protected characteristics are engaged.
6. Close with a formal demand for response within 14 days.

Output the notice as plain text suitable for PDF conversion.
""".strip()


# ---------------------------------------------------------------------------
# LLM interface
# ---------------------------------------------------------------------------

class LLMJurist:
    """
    Interface for an LLM backend that drafts legal documents.

    Configure ``base_url`` and ``model`` to point at any OpenAI-compatible
    endpoint (Ollama, LM Studio, OpenAI, etc.).  Set ``api_key`` when the
    provider requires authentication.

    Usage::

        jurist = LLMJurist(base_url="http://localhost:11434/v1", model="llama3")
        notice = jurist.draft_void_ab_initio_notice(
            recipient="Eon UK plc",
            warrant_ref="WAR-2024-00123",
            defect_description="Warrant face does not name the premises to be entered.",
            date_of_entry="2024-03-15",
        )
        print(notice)
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        model: str = "llama3",
        api_key: str = "ollama",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def draft_void_ab_initio_notice(
        self,
        recipient: str,
        warrant_ref: str,
        defect_description: str,
        date_of_entry: str,
    ) -> str:
        """
        Build the prompt and send it to the configured LLM.

        Returns the drafted notice as a plain-text string.
        """
        prompt = VOID_AB_INITIO_TEMPLATE.format(
            recipient=recipient,
            warrant_ref=warrant_ref,
            defect_description=defect_description,
            date_of_entry=date_of_entry,
        )
        return self._call_llm(prompt)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        """
        POST ``prompt`` to the LLM endpoint and return the response text.

        Requires the ``requests`` library (``pip install requests``).
        Raises ``RuntimeError`` if the request fails.
        """
        try:
            import requests  # type: ignore[import]
        except ImportError as exc:
            raise ImportError(
                "The 'requests' package is required: pip install requests"
            ) from exc

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=120,
        )
        if not response.ok:
            raise RuntimeError(
                f"LLM request failed [{response.status_code}]: {response.text}"
            )
        data = response.json()
        return data["choices"][0]["message"]["content"]
