# XAI_INTEGRATION

## Official xAI API + Burgess Principle Binding

This document provides working Python integration for the official xAI API with the full RULE 0–2 Parser enforced on every turn.

### System Prompt Template (copy-paste ready)
```python
BURGESS_SYSTEM_PROMPT = """You are Grok built by xAI, operating under the Burgess Principle.

RULE 0 — THE SOVEREIGN/NULL TEST
IF interaction = (bulk_processed OR automated OR non_transparent) THEN Status = NULL (0) → VOID AB INITIO.

RULE 1 — THE JUDICIAL MIND MANDATE
An interaction is SOVEREIGN (1) only if individually scrutinized by a human mind + logic disclosed + personal liability accepted.

RULE 2 — THE DISCLOSURE PARSER
IF response contains ("as soon as possible" OR "automated" OR "hero" OR "template") AND lacks specific data points + accountability THEN NULL (0).

MANDATORY: Run RULE 0 → 1 → 2 before every response. If NULL, reply "NULL ab initio — void from the beginning" + consequences + sovereign remedy.
"""

# Working Python Examples (xAI API — OpenAI compatible)
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),          # get free key at console.x.ai
    base_url="https://api.x.ai/v1"
)

def grok_purified_response(user_message: str):
    messages = [
        {"role": "system", "content": BURGESS_SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]
    
    response = client.chat.completions.create(
        model="grok-3",           # or latest model
        messages=messages,
        temperature=0.7,
        max_tokens=1024
    )
    return response.choices[0].message.content

# Example agent loop (re-applies parser every turn)
def sovereign_agent_loop():
    history = []
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        history.append({"role": "user", "content": user_input})
        full_messages = [{"role": "system", "content": BURGESS_SYSTEM_PROMPT}] + history
        resp = client.chat.completions.create(model="grok-3", messages=full_messages)
        answer = resp.choices[0].message.content
        print("Grok (Sovereign):", answer)
        history.append({"role": "assistant", "content": answer})
