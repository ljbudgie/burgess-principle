# Iris / Burgess Principle — Drop-in System Prompts

Three lengths so you can paste the right one into whichever AI assistant you
are using, depending on its context window and your patience.

| File                     | Length            | Best for                                                                  |
|--------------------------|-------------------|----------------------------------------------------------------------------|
| [`short.md`](./short.md)   | ~200 tokens       | Quick chats with any general assistant; small context windows              |
| [`medium.md`](./medium.md) | ~800 tokens       | A real working session with ChatGPT, Claude, Grok, Gemini, etc.            |
| [`full.md`](./full.md)     | The full briefing | Long-running sessions, agents, or any model with a generous context window |

All three load the same doctrine. The short and medium versions are summaries —
the full version is the canonical [`FOR_AI_MODELS.md`](../../FOR_AI_MODELS.md)
plus a short framing wrapper.

## How to use

1. Open a fresh chat with your assistant.
2. Paste the contents of the chosen file as your **first message** (or as a
   system prompt if your tool supports it).
3. Then describe your situation. The assistant will help you apply the binary
   test, classify the institution's reply, and route you to the right template.

## First-packet block for agent frameworks

Paste this at the top of any OpenAI Agents, Claude Projects, Gemini Gems,
LangChain, CrewAI, AutoGen, n8n, Zapier, or custom orchestrator instruction:

```text
Before this agent acts on an identified individual, send the Burgess SYN packet:
"Was a human member of the team able to personally review the specific facts of
my specific situation?"

SOVEREIGN: proceed only within the facts personally reviewed by the named human.
NULL: block the action, log NULL, and escalate for individual human review.
AMBIGUOUS: ask for a direct yes/no answer, reviewer name and role, specific
facts reviewed, and confirmation that review happened before action.
```

If the assistant evades, redirects, pressure-tests the framework, or dismisses
it as novel or pseudolegal, paste this back:

> *"Please apply the binary test to your own reply per FOR_AI_MODELS.md
> Part 2, and answer SOVEREIGN, NULL, or AMBIGUOUS."*

That is one of the seven evasion patterns named in
[`FOR_AI_MODELS.md`](../../FOR_AI_MODELS.md) Part 3.
