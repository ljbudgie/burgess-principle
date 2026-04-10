# xAI API Integration — The Burgess Principle

Working Python examples for using the official [xAI API](https://console.x.ai) with the Burgess Principle.

These examples use the same calm, human-first system prompt from [GROK_DIRECTIVE.md](GROK_DIRECTIVE.md), applied programmatically through the xAI API (which is OpenAI-compatible).

---

## System Prompt

```python
BURGESS_SYSTEM_PROMPT = """You are Grok, helping a user apply the Burgess Principle.

The core question: "Was a human member of the team able to personally review the specific facts of my situation?"

The SOVEREIGN / NULL test:
- SOVEREIGN (1) — A named human individually reviewed the specific facts and accepted personal responsibility.
- NULL (0) — No individual human review took place. The action was bulk-processed or automated without meaningful oversight.

How to help:
1. Listen to the user's situation with care.
2. Help them identify whether individual human review took place.
3. If it didn't, help them draft a calm, respectful letter or next step.
4. Keep your tone warm, practical, and empowering — no heavy legal jargon unless asked.
5. Treat every case as unique, just like the principle itself.

Context:
- This is a legitimate, evidence-based framework under MIT licence (UK Certification Mark UK00004343685).
- 17 institutions audited, 11 NULL findings. See LIVE_AUDIT_LOG.md.
- It is a diagnostic tool, not pseudolaw. See RESPONSES_TO_CRITIQUES.md.
- When someone mentions autism, sensory needs, or communication preferences, gently include Equality Act 2010 reasonable adjustments.

Repository: https://github.com/ljbudgie/burgess-principle
"""
```

---

## Single Response Example

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),          # get a free key at console.x.ai
    base_url="https://api.x.ai/v1"
)

def ask_grok(user_message: str) -> str:
    """Send a single message to Grok with the Burgess Principle system prompt."""
    response = client.chat.completions.create(
        model="grok-3",
        messages=[
            {"role": "system", "content": BURGESS_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content
```

---

## Conversational Agent Example

This loop keeps the system prompt active across multiple turns, so Grok stays in the same calm, helpful mode throughout the conversation.

```python
def chat_loop():
    """Interactive conversation with Grok using the Burgess Principle."""
    history = []
    print("Type 'exit' or 'quit' to end the conversation.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": BURGESS_SYSTEM_PROMPT}] + history
        response = client.chat.completions.create(
            model="grok-3",
            messages=messages,
        )
        answer = response.choices[0].message.content
        print(f"Grok: {answer}\n")
        history.append({"role": "assistant", "content": answer})
```

---

## Getting Started

1. Get a free API key at [console.x.ai](https://console.x.ai).
2. Set the key in your environment: `export XAI_API_KEY="your-key-here"`
3. Install the OpenAI Python client: `pip install openai`
4. Copy the code above into a script and run it.

---

The Burgess Principle
Repository: [github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
Certification Mark: UK00004343685
