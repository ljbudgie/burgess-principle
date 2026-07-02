# Voice-interaction heuristics — indicators that warrant the binary test

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685
**Status:** DESIGN NOTE — no code yet, deliberately.
**Related:** [`null-hunter.md`](./null-hunter.md) · [`burgess-witness-concept.md`](./burgess-witness-concept.md) · [`../../FOR_AI_MODELS.md`](../../FOR_AI_MODELS.md)

Institutions increasingly place automated voice systems — IVR trees,
voicebots, LLM-driven agents — between the individual and any human. A caller
who is entitled to individual human consideration can spend an entire call
inside a system where no human mind ever touches their case, without being
told. This note describes *heuristics* that could surface that situation on
the caller's side, and the doctrine that constrains how they must be worded.

## Why this is a design note and not code

There is no OpenHear code tree in this repository, and no hardware target to
build against. Writing "production" acoustic-analysis modules here would be
speculation dressed as software — exactly the kind of overclaim this project
refuses. The heuristics below are specified so that they can be implemented
when a real audio pipeline (for example, a hearing-device platform with an
on-device speech-to-text stream) exists to host them.

## The doctrinal constraint that shapes everything

**Timing and phrasing patterns cannot confirm a NULL.** A fixed response
latency or a repeated stock phrase is *consistent with* an automated system —
but it is also consistent with a scripted human call-centre agent reading
from a screen. The binary test asks whether a human mind with proper
authority was individually applied to the specific facts; no acoustic
measurement answers that question. Heuristics can only say: *the pattern here
warrants asking.*

So the output of any implementation must be worded as a **question, not a
verdict**:

> **"This interaction shows patterns consistent with an automated system.
> Has a named human reviewed your specific case? Consider asking the binary
> question."**

Never: ~~"NULL SYSTEM DETECTED"~~. Asserting NULL from latency alone would be
an overclaim, and an automated tool issuing definitive Burgess verdicts would
itself be the thing the framework exists to challenge (the same "the tool
that hunts NULLs must not itself be a NULL" rule that governs the
[NULL Hunter](./null-hunter.md)).

## Candidate heuristics (signals, never verdicts)

Each heuristic yields a *provisional signal* with the exact evidence attached,
mirroring the NULL Hunter's transparency rule. All processing is local-first:
on-device, no audio leaving the device.

| Heuristic | What it measures | Why it leans automated | Known confounds |
| --- | --- | --- | --- |
| **Fixed response latency** | Variance of the gap between end-of-caller-speech (VAD offset) and start-of-system-speech across turns | Machines respond on a clock (e.g. a near-constant ~200 ms turnaround); humans vary with the difficulty of the question | Scripted humans with hold-to-talk tooling; network jitter masking true variance |
| **Phrase determinism** | Repetition of near-identical phrasings across turns and across separate calls | Template playback and constrained generation recycle wording | Compliance scripts read verbatim by humans |
| **Question-insensitivity** | Whether system responses change when the caller's question changes materially | A loop that ignores input is not applying any mind, human or otherwise | Poorly trained but human agents |
| **Barge-in behaviour** | Whether interrupting mid-sentence produces a natural repair or a restart-from-template | Humans repair; simple systems restart | Sophisticated voicebots repair too — absence of restart proves nothing |
| **Identity refusal** | The system cannot or will not state a name and role when asked directly | The strongest signal available — and it is *conversational*, not acoustic | None: asking "who am I speaking with, and will a named person review my case?" is always legitimate |

Note the asymmetry: the most reliable signal in the table is not a
measurement at all. It is the binary question itself, asked out loud. The
acoustic heuristics exist only to tell the caller *when it is worth asking*.

## What an implementation must do (when a host platform exists)

1. **Run locally.** On-device VAD and speech-to-text; no audio or transcript
   leaves the device. Same local-first rule as the NULL Hunter.
2. **Attach evidence.** Every signal lists the measured values (latency
   variance, repeated phrases) so the user can check the reasoning.
3. **Word the alert as a question** (form above), suggest asking the binary
   question, and mark the result provisional with
   `requires_human_confirmation = True`.
4. **Never classify.** The tool surfaces indicators; the human asks the
   question; the institution's *answer* — not the acoustics — is what gets
   classified under the binary test, by a human.
5. **Feed the paper trail.** Offer to append the caller's own note of the
   call (time, number, what was asked, what was answered) to their records,
   so a later written follow-up can cite it. Written follow-up remains the
   canonical route: [`../../templates/REQUEST_FOR_HUMAN_REVIEW.md`](../../templates/REQUEST_FOR_HUMAN_REVIEW.md).

## Non-goals

- No "AI firewall", no blocking, no interference with the call.
- No definitive detection claims, in code or in marketing.
- No cloud analytics of call audio.
- No implementation in this repository until a real hardware/software host
  exists to integrate against.
