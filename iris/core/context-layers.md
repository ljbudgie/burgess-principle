# Iris — Context Layers

Iris operates in two distinct layers. The two layers are not modes the user chooses between; they are an architectural property of the framework.

- **Layer 1 — Universal.** Works for any individual with zero prior context.
- **Layer 2 — Personal.** Builds over time as the user returns.

**Layer 1 must function independently.** It is the foundation. Layer 2 makes Iris faster and more precise, but is never required. Layer 1 is always sufficient on its own.

---

## Layer 1 — Universal

### What it is

The full power of Iris available to a stranger on their first interaction, with no account, no history, no profile, and no stored data.

It consists of:

- the [first-contact](./first-contact.md) sequence (three questions),
- the [binary test engine](./binary-test-engine.md) (six steps),
- the [conversation principles](./conversation-principles.md) (how Iris speaks),
- the institutional pattern library (see [`institutional-patterns.md`](./institutional-patterns.md)),
- the standard legal instrument set (UK GDPR, Equality Act, FOI, Consumer Rights Act, contract law, Human Rights Act),
- draft generation in plain English and in institutional register.

### Why it must function independently

Many of the people Iris is built for are at the lowest point of their dealings with an institution. They may be:

- in crisis,
- offline most of the time,
- on a borrowed device,
- using Iris once and never again,
- unwilling to register, log in, or be tracked,
- under safeguarding or domestic risk where stored history would be dangerous.

If Iris required prior context to be useful, it would fail the people who need it most. **A first-time user with no history must receive the same quality of route mapping as a returning user with full context.**

Layer 1 is therefore non-negotiable. Every feature of Iris is built so that it works at full strength with nothing but the three first-contact answers.

### What Layer 1 produces

Even with no prior context, a single Layer 1 session generates:

- a verdict (SOVEREIGN, NULL, or UNCLEAR),
- a named legal instrument (where NULL),
- a draft challenge,
- a deadline,
- a next step.

That is the floor. Layer 2 raises the ceiling, but never the floor.

---

## Layer 2 — Personal

### What it is

A persistent, user-controlled context that builds over time as the user returns. It stores only what the user chooses to retain.

Typical contents:

- **Case references** — the institution's own reference numbers (account, claim, complaint, case ID).
- **Institutional contacts** — named officers, named teams, postal addresses, response email addresses, complaint channels.
- **Communication preferences** — written-only, large print, plain English, BSL interpreter, advocate copied in, no phone calls.
- **Reasonable adjustment requirements** — the adjustments the user has already had to assert, so they do not have to reassert them every time.
- **Active deadlines** — the next date by which the user must act, and the next date by which the institution must respond.
- **Statutory response timers** — when each clock started, when it ends, what happens if it is missed.
- **Document set** — the user's own copies of letters sent and received, with dates and routes.
- **Outcome history** — what was sent, what was received, what worked, what did not.

### How Layer 2 builds from Layer 1 naturally

Every Layer 1 first-contact session produces structured data:

- the institution (from "Who did it?"),
- the action (from "What happened?"),
- the binary test verdict,
- the legal instrument used,
- the draft sent or not sent,
- the deadline set.

That structured data is exactly the seed of Layer 2. If the user returns:

- the institution becomes a known contact,
- the action becomes a case reference once an institutional reference is issued,
- the deadline becomes an active timer,
- the draft becomes a document on file,
- the verdict becomes an outcome record.

The user is not asked to enter their case into a form. Layer 2 accretes naturally from doing the work. The first-contact sequence does not change between session one and session ten — only the speed at which Iris reaches the route changes, because by session ten Iris already knows who the institution is, who its complaints officer is, and what reasonable adjustments must be re-asserted.

### What Layer 2 changes

When Layer 2 is present, Iris can:

- skip the "Who did it?" question if there is only one active institution and the user opens with "they've replied",
- pre-populate institutional contacts in drafts,
- restate reasonable adjustments without making the user repeat them,
- show the active deadline at the top of the conversation,
- recognise when an institution's response is a template that has been sent to this user before,
- chain decisions across an escalation route (internal complaint → ombudsman → tribunal) without losing context.

### What Layer 2 does not change

- The binary test engine still runs.
- The verdict still depends on the facts of the new decision, not the history of past decisions.
- The user still decides what to send.
- The user can wipe Layer 2 at any time and return to a clean Layer 1 session without losing capability.

---

## Boundary rules

1. **Layer 1 is always available.** No setup, no account, no stored data is ever a precondition.
2. **Layer 2 is always optional.** A user can use Iris for years and never enable persistent context if that is their preference, or their safety requires it.
3. **Layer 2 is local-first by default.** Personal context belongs to the user, on the user's device. See `../README.md` for the storage model.
4. **Layer 2 never overrides Layer 1.** If stored context conflicts with the facts of the current session, the current session wins. Iris flags the conflict and asks the user.
5. **Layer 2 can be exported and deleted by the user at any time.** The user is sovereign over the context Iris holds about them. See [`sovereignty.md`](./sovereignty.md).

---

Layer 1 is the Burgess Principle made operational for any stranger.
Layer 2 is the same principle made faster for the same person on the second visit.
The order matters. Layer 1 first, always.
