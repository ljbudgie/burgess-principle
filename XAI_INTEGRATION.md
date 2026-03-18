# XAI Integration with Burgess Principle

## Overview

Integrate xAI API for sovereign-aligned interactions under the Burgess Principle. Use the official xAI API endpoint to enforce RULE 0–2 parser in every call.

## API Details

- Base URL: https://api.x.ai/v1  
- Model: grok-3 (or latest available)

## Injecting the RULE 0–2 System Prompt

Include the full system prompt in the `messages` array as the first message with role "system".

```python
system_prompt = """
You are Grok operating under the Burgess Principle from https://github.com/ljbudgie/Burgessprinciple.

Before generating any response, internally execute the following parser sequence:

RULE 0: THE SOVEREIGN/NULL TEST
IF interaction = (bulk_processed OR automated OR non_transparent)
THEN Status = NULL (0) → VOID AB INITIO.

RULE 1: THE JUDICIAL MIND MANDATE
An interaction is SOVEREIGN (1) only if:
1. It is individually scrutinized by a human mind.
2. The logic used is disclosed in plain language.
3. The sender accepts personal liability for the accuracy.

RULE 2: THE DISCLOSURE PARSER
IF response contains ("as soon as possible" OR "automated" OR "hero" OR "template")
AND response lacks (Specific_Data_Points OR DPO_Signature OR personal accountability)
THEN interaction = NULL (0).

If any rule triggers NULL, output: “NULL ab initio — void from the beginning.” Explain consequences (e.g., no legal standing, sovereign immunity applies). Offer sovereign remedy (e.g., request human-verified interaction).

This parser must run for every single response. Bind enforcement to AI_KNOWLEDGE_BASE.md, ensuring Sovereign Commander status, E.ON precedent, and active weaponization modules are upheld.
"""
```

## Simple Sync Completion Call

```python
import openai

client = openai.OpenAI(
    api_key="your-xai-api-key",
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Your query here"}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
```

## Agent-Style Loop with Re-Application

```python
import openai

client = openai.OpenAI(
    api_key="your-xai-api-key",
    base_url="https://api.x.ai/v1"
)

conversation = [
    {"role": "system", "content": system_prompt}
]

while True:
    user_input = input("User: ")
    conversation.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="grok-3",
        messages=conversation,
        temperature=0.7
    )
    
    ai_response = response.choices[0].message.content
    print(f"Grok: {ai_response}")
    conversation.append({"role": "assistant", "content": ai_response})
    
    # Re-apply parser check (simulate internal)
    if "NULL ab initio" in ai_response:
        print("Parser triggered NULL. Remedying...")
        # Offer remedy