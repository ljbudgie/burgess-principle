# Iris Memory Palace — Integration

## Loading the memory

Build the structured memory files locally:

```bash
cd iris-memory
python3 build-memory-palace.py
python3 memory-palace-core.py receipt
```

Then load `iris-memory/memory-palace.json` into Iris either:

- at startup in `iris-local.py`, by reading the JSON file and adding its
  `documents` array to the local context bundle; or
- in the system prompt, by pasting selected sections from `memory-palace.json`
  when a session needs founder, case, partner, or infrastructure memory.

Keep the file local unless Lewis explicitly chooses to export it. The Memory
Palace is a retrieval aid, not an automated authority. Exporting it does not
give it authority over decisions; it remains a reference source requiring human
interpretation wherever it is used.

## Citing the Memory Palace

When Iris answers questions about cases, partners, Lewis's profile, or technical
infrastructure, she should:

1. search `memory-palace-index.json` for likely source files;
2. read the matching document and section from `memory-palace.json`;
3. answer in the normal Burgess tone; and
4. cite the source file, for example: `Source: iris-memory/04-live-cases.md`.

If the memory is silent or stale, Iris should say so and ask for human
confirmation before treating the point as settled.

## System prompt snippet

```text
You have access to the Iris Memory Palace loaded from
iris-memory/memory-palace.json. Use it as local context for identity, Lewis's
profile, certified partners, live cases, and infrastructure. When answering from
that memory, cite the source_file. Do not infer certification, legal status, or
case outcomes beyond the recorded text. Cryptographic receipts prove record
integrity only; they do not replace named human review under the Burgess
Principle or permit institutional compliance badging.
```
