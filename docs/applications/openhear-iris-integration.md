# OpenHear × Iris Integration

**Burgess Principle framework application — hearing sovereignty**  
**Version:** v2.9.0  
**Status:** Active

---

## Overview

This document describes the OpenHear skill within Iris — the Burgess Principle's advisory engine. The integration covers two functions:

1. **Build orchestration** — guiding deaf and hard-of-hearing citizens through building their own OpenHear hearing device, stage by stage.
2. **Rights advisory** — applying EA 2010 ss.20/21 anticipatory duty and the Burgess binary test when an institution fails to accommodate an OpenHear user.

These are not separate tools. They are two modes of the same sovereignty frame: you have the right to build your own device, and you have the right to have that device accommodated.

---

## Why OpenHear + Iris

OpenHear is Lewis's open-source hearing-sovereignty platform — PCB, firmware, DSP pipeline, and BLE wristband haptics — designed to give deaf and hard-of-hearing people a device they own completely. No proprietary firmware, no NHS waiting list, no audiologist gatekeeping required.

Iris is the Burgess Principle's advisory engine, built around anticipatory duty and the binary test. The gap it was filling before this integration: a user could build an OpenHear device and then face institutional refusal to engage with it — an NHS-only policy, an employer failing to make adjustments, an audiologist declining to assess — with no framework language to push back.

The integration closes that gap. Iris can now:

- Help you build the device (engineering layer, not clinical)
- Help you understand your rights when an institution refuses to engage with it
- Apply the binary test to the institution's decision
- Connect the physical (haptic patterns on the wristband) to the legal (SOVEREIGN / AMBIGUOUS / NULL)

---

## Build Orchestration

### What Iris does

Iris guides the build through eight stages:

| Stage | What happens |
|---|---|
| **Prerequisites** | Hardware checklist, repo clone, platform confirmation |
| **Hardware assembly** | PCB orientation, actuator polarity, continuity check before power-on |
| **Firmware flash** | esptool setup, flash mode entry, chip detection, firmware write |
| **USB driver setup** | Noahlink Wireless dongle (USB ID 16F0:0003) detection on Linux / macOS / Windows; udev rules; Zadig for Windows |
| **DSP routing** | Pipeline configuration from dsp_routing.yaml; audio flow verification |
| **BLE pairing** | ESP32-S3 advertising, browser BLE scan (Chrome/Edge required), actuator acknowledge pulse |
| **Iris Bridge** | Haptic pattern mapping (SOVEREIGN / AMBIGUOUS / NULL); local-first |
| **Functional test** | 24-actuator sweep, Iris Bridge pattern verification, latency check |

At each stage, Iris asks diagnostic questions before advancing. If the user reports a problem, Iris matches the symptom against a known-issues table and returns targeted troubleshooting steps.

### What Iris does not do

Iris does not provide clinical recommendations. Gain levels, frequency response curves, equalisation profiles, and audiological calibration for a specific hearing loss profile are outside scope — always. Those are the user's sovereign domain, informed by their own audiogram and experience. If the user wants clinical input on DSP settings, the right resource is an audiologist willing to engage with a sovereign build.

This boundary is not a limitation — it is the scope. Building the device and tuning it for your hearing are two different things. Iris owns the first; you own the second.

### Hardware reference

| Component | Specification |
|---|---|
| MCU | ESP32-S3 |
| Haptic actuators | 24× LRA (Linear Resonant Actuator) |
| PCB | 4-layer, 65×30mm, ENIG finish |
| Form factor | Wristband |
| Dongle | Noahlink Wireless — USB VID 0x16F0, PID 0x0003 (confirmed against hardware) |
| Connectivity | BLE (Bluetooth Low Energy) + USB (dongle) |
| OpenHear repo | [github.com/ljbudgie/openhear](https://github.com/ljbudgie/openhear) |

---

## Rights Advisory

### Anticipatory duty — EA 2010 ss.20/21

The anticipatory duty runs ahead of any request. An institution must already have considered how to accommodate someone using a non-NHS hearing device before that person walks through the door — not wait until they ask, not impose an NHS-only requirement without individual consideration.

This applies to:

- NHS trusts and clinical settings
- Employers and workplaces
- Educational institutions
- Financial services (where hearing accommodation is relevant)
- Any other service provider within EA 2010 Part 3

### Indirect discrimination — EA 2010 s.19

"NHS-approved devices only" (or any equivalent policy) is a provision, criterion, or practice (PCP). Applied without individual assessment of the specific person's circumstances, it puts deaf and hard-of-hearing people who use sovereign builds at a particular disadvantage. That is prima facie s.19 indirect discrimination unless it can be objectively justified.

The justification threshold is not trivially met by "that's our policy." The institution must show the PCP is a proportionate means of achieving a legitimate aim, assessed against the individual's actual situation.

### Binary test — applied to hearing device contexts

When an institution refuses to accommodate an OpenHear device, the binary test applies in the same way as any other institutional decision:

> Was a named human being's mind applied to the specific facts of this person's case — their device, their hearing profile, their access need — before the institution exercised its power?

The five elements:
1. Named person
2. Role and authority
3. Specific facts considered (including the user's actual device, not a generic "non-NHS device" category)
4. Pre-decision timing
5. Authority to differ from the policy

If any of these are absent: **NULL**. A NULL finding on a hearing accommodation decision is a starting point for escalation under EA 2010 and, for AI-mediated decisions, DUAA 2025 Arts. 22A–22D.

### EA 2010 s.27 — victimisation

If the user has previously raised a complaint about hearing accommodation and subsequently experiences worse treatment from the same institution, s.27 victimisation is a potential Stage 3 issue in addition to the underlying adjustment failure.

The burden shift under EA 2010 s.136 applies: if a detriment follows a protected act (the complaint), the respondent must explain why the detriment is not connected to the protected act.

### Standard question to ask in writing

> "Please provide the name and role of the person who considered the specific facts of my hearing situation — including my device — before applying this policy to me, and confirm when that review took place."

Apply the binary test to the response. If the institution cannot answer, or responds with process language rather than a named individual, that is NULL or AMBIGUOUS.

---

## Iris Bridge — haptic sovereignty

The Iris Bridge is the physical connection between the advisory layer and the wristband. When Iris classifies an institutional response, the user feels it:

| Classification | Haptic pattern | Meaning |
|---|---|---|
| **SOVEREIGN** | Steady triple pulse | Named human reviewed your specific facts — the institution's position has a basis |
| **AMBIGUOUS** | Double pulse with pause | Process language without confirmed individual review — seek clarification |
| **NULL** | Long single hold | No named human applied their mind — your rights are engaged |

The bridge is local-first. No data leaves the device. The BLE Web API connection is between the browser and the wristband; no cloud relay is involved.

---

## Advisory constraints

All outputs from the OpenHear Iris skill carry the following constraints:

- **Advisory only.** `requires_human_confirmation = True` on all rights findings. Iris identifies patterns and frames the legal question — it does not issue legal verdicts. Rights findings should be confirmed with a solicitor or qualified caseworker before formal escalation.
- **No clinical advice.** Gain settings, frequency response, and audiological calibration are always out of scope. Iris does not hold itself out as a clinical tool.
- **Local-first.** Pure standard library. No network calls from the skill module.
- **Transparent basis.** Every advisory output states the statutory basis for the framing.

---

## Module reference

**Source:** [`iris/openhear_skill.py`](../../iris/openhear_skill.py)  
**Prompt context:** [`iris/prompts/openhear.md`](../../iris/prompts/openhear.md)  
**Noahlink VID/PID:** confirmed against hardware — 0x16F0 / 0x0003  
**OpenHear repo:** [github.com/ljbudgie/openhear](https://github.com/ljbudgie/openhear)

### Classes

| Class | Purpose |
|---|---|
| `BuildOrchestrator` | Stage-by-stage build guidance; diagnostic matching |
| `BuildSession` | Tracks current stage, completed stages, platform, PCB revision |
| `RightsAdvisor` | EA 2010 / binary test pattern matching and advisory framing |
| `OpenHearSkill` | Top-level entry point — routes to build, rights, or both |
| `RightsSignal` | A detected rights-relevant pattern with confidence and advisory text |
| `BuildGuidance` | Structured guidance for the current build stage |
| `DiagnosticResult` | Matched troubleshooting steps for a reported symptom |

### Module-level function

```python
from iris.openhear_skill import assess_context, BuildSession

# First contact — no session yet
result = assess_context("The Noahlink dongle isn't being detected by lsusb")

# Build in progress
session = BuildSession()
result = assess_context("I'm getting a permission denied error on the USB port", session)
print(result.diagnostic)

# Rights query
result = assess_context("My employer says they only support NHS-approved hearing devices")
for signal in result.rights_signals:
    print(signal.advisory)
```

---

*The Burgess Principle — UK Certification Mark UK00004343685*  
*lewisjames@theburgessprinciple.com · theburgessprinciple.com*  
*OpenHear — [github.com/ljbudgie/openhear](https://github.com/ljbudgie/openhear)*
