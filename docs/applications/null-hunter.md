# NULL Hunter — local-first Burgess-Test signal scanner

**Part of:** The Burgess Principle · Iris · UK Certification Mark UK00004343685
**Module:** [`iris/null_hunter.py`](../../iris/null_hunter.py) · **Tests:** [`tests/test_null_hunter.py`](../../tests/test_null_hunter.py)

The NULL Hunter reads the text of an institutional reply — an email, a decision
letter, a portal message — and flags the language patterns associated with the
three Burgess classifications, then suggests the next Burgess step.

It is the first shippable increment toward the [Burgess Witness](./burgess-witness-concept.md)
device: it runs on-device today, has no identity or adoption dependency, and
produces the kind of classification record a future attestor would sign.

## The one rule that makes it honest

**The tool that hunts NULLs must not itself be a NULL.** An automated classifier
that quietly decided your case would be exactly the thing the framework exists to
challenge. So the NULL Hunter is **advisory only**:

- every result is marked **provisional** and carries `requires_human_confirmation = True`;
- it lists the **exact phrases** that triggered each signal, so you can check the
  reasoning rather than trust a black box;
- a human makes the classification — the scanner only surfaces signals and a
  suggested next step.

It is **local-first**: pure standard library, no network, no model download,
nothing leaves the device.

## What it looks for

| Signal | Leans | Examples it catches |
| --- | --- | --- |
| Explicit automation / no individual review | **NULL** | "processed automatically", "system-generated", "uploaded in bulk", "no individual review" |
| Process / weasel language without a named human | **AMBIGUOUS** | "subject to human oversight", "in line with our policy", "robust processes", "reviewed by the team" |
| A named person described as personally reviewing | **SOVEREIGN** | "Sarah Chen … handled your case personally", "reviewed by Jane Smith" |

Precedence is conservative: an explicit NULL admission outweighs everything; a
named reviewer *mixed with* weasel language is treated as **AMBIGUOUS** (the
named-but-unconfirmed trap), not SOVEREIGN; and if nothing is recognised the
result is **INSUFFICIENT** — meaning *ask the binary question*, don't guess.

## Usage

```bash
# Paste or pipe an institutional reply; get a provisional scan.
pbpaste | python -m iris.null_hunter
```

```python
from iris.null_hunter import scan

result = scan("Our systems are subject to human oversight.")
result.classification          # 'AMBIGUOUS' (provisional)
result.matched                 # {'ambiguous': ["'subject to human oversight'"]}
result.suggested_next_step     # routes to FOLLOW_UP_WEASEL_RESPONSE.md
result.requires_human_confirmation  # always True
```

## Limits (stated plainly)

- It matches **language**, not meaning. It can miss a cleverly-worded NULL and can
  over-flag innocent phrasing — which is exactly why the human gate is mandatory.
- A SOVEREIGN signal means the reply *claims* a named human reviewed; it is not
  proof they did. Confirm in writing who reviewed it and what they reviewed.
- It is an aid to the binary test, not a substitute for it.

*The Burgess Principle — UK Certification Mark UK00004343685 — lewisjames@theburgessprinciple.com*
