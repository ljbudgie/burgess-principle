# Case Study: Automated Diagnostic Algorithm & Triage—NHS Urgent & Emergency Care

**Status:** Ongoing (submitted to ICO and NHS England for investigation)  
**Sector:** Healthcare / Medical AI  
**Institution:** NHS Trust (Anonymised; Urgent & Emergency Department)  
**Burgess Principle Classification:** NULL (at algorithm stage) → AMBIGUOUS (at clinical review stage)  
**Outcome:** Pending; potential system redesign  
**Key learning:** Even healthcare has automated triage; individual clinical judgment must be documented per patient.

---

## The Situation

**Date:** March 2026  
**Subject:** A 34-year-old woman with multiple health conditions (asthma, anxiety, hearing loss) presented to the emergency department with chest pain and shortness of breath. An automated triage algorithm (Manchester Triage Protocol, implemented as a scoring system without mandatory clinician override) assigned the patient to a lower-urgency category, resulting in a 3-hour wait before a clinician review.

**The patient's specific facts:**
- The patient was deaf; communication was email-only (patient preference documented)
- She had documented asthma; recent inhaler changes (relevant to SOB)
- She had anxiety with prior positive response to reassurance
- She had new-onset cardiac symptoms; family history of early MI

**The algorithm's facts:**
- Presenting complaint: "Chest pain and shortness of breath" → algorithm score
- Vital signs submitted: O₂ sat 96%, BP 138/82, HR 92 → algorithm score
- Output: Category 3 (Urgent; expected wait 30–60 minutes)

**What happened:**
The patient waited 3 hours (1 hour past the algorithm's own estimate). When seen, the clinician (after 5-minute interaction) ordered an ECG, troponin tests, and cardiac workup—all of which required urgent attention.

---

## Burgess Principle Application

### Question 1: Did an automated algorithm make a decision without individual clinical review?

**Answer: YES—initially.**

The triage algorithm produced an output (Category 3: 30–60 minute wait) without documented evidence of a clinician reviewing the specific patient's circumstances before that output was accepted as a triage decision.

### Question 2: Did a clinician personally review this specific patient's facts *before* the algorithm-driven triage decision took effect?

**Answer: AMBIGUOUS → NULL**

**Exchange:**

**March 2026 (Patient request):**  
"Can you identify the clinician who reviewed my specific triage information and my specific health circumstances (asthma, anxiety, cardiac symptoms) *before* the algorithm assigned me to a 3-hour wait category?"

**March 2026 (NHS Trust response):**  
"The triage process at our facility uses the Manchester Triage Protocol, a validated algorithm embedded in our emergency IT system. All patients are triaged through this system. Urgent cases are identified by the algorithm and escalated to a senior clinician. Your case was reviewed according to standard protocol."

**Classification: AMBIGUOUS.**  
The NHS Trust cited a process ("validated algorithm," "escalated if urgent") but did not:
- Name the clinician who reviewed the patient's case
- Describe the specific facts about the patient that were reviewed
- Confirm that this review happened *before* the triage assignment

**Patient follow-up:**  
"I understand the Manchester Triage Protocol is used. I am asking: did a named clinician examine my specific health facts—asthma, anxiety, cardiac symptoms, hearing loss—and my specific need for email communication *before* the system assigned me to Category 3? If not, was I in Category 3 because of the algorithm, not because a human clinician reviewed me individually?"

**March 2026 (NHS Trust response 2):**  
"The system is designed so that cases not escalated to urgent triage are reviewed by nursing staff upon check-in. Your case was reviewed by a triage nurse when you presented."

**Classification: NULL.**  
The NHS Trust admitted that no clinician review occurred *before* the algorithm-driven triage decision. The patient was assigned to a wait category by the algorithm; only after physical check-in was she reviewed by nursing staff.

---

## The Problem: NULL at the Algorithm Stage

Under GDPR Article 22 and DUAA 2025 Articles 22A–22D, automated decisions affecting individuals require "meaningful human involvement" *before* the decision affects the person.

In this case:
- **Algorithm produces triage score** → Category 3 assignment → 3-hour wait
- **Then:** Patient checks in physically
- **Then:** Nurse reviews patient

**Burgess finding:** The triage *decision* (assignment to Category 3 and resulting wait time) was made by the algorithm without documented prior individual human clinician review.

**Problem:** 
- The patient with cardiac symptoms waited 3 hours because an algorithm assigned her to a lower-urgency tier
- No evidence that a clinician individually reviewed her specific symptoms + health history + communication needs before the algorithm's triage score became operative
- The NHS later did the human review—but *after* the decision had already taken effect

---

## Parallel Situation: Content Moderation & Accessibility

This case parallels platform content moderation without human review. The difference is that triage in emergency medicine is time-critical and safety-critical.

**Analogy:**
- **Platform moderation:** Algorithm removes post → then, if appealed, human reviews
- **ED triage:** Algorithm assigns wait time → then, when patient presents, nurse reviews

**The difference, legally:**
- The platform's algorithm makes a decision about content; human review follows if the user appeals
- The ED's algorithm makes a decision about urgency; the patient's wait time is *already* in effect before human review occurs

Under GDPR Article 22, both scenarios raise the same question: "Did a human review this specific situation *before* the decision took effect?"

---

## ICO & NHS Escalation

**March 2026 (Patient complaint):**  
Filed with:
1. **ICO** — GDPR Article 22 breach (automated individual decision without meaningful human involvement before the decision took effect)
2. **CQC** — Care Quality Commission complaint (patient safety; triage protocol may deprioritise high-risk cases)
3. **NHS England** — Governance query: Are triage algorithms being applied without prior clinician review of individual facts?

**Current status:**  
ICO has logged the complaint. NHS Trust has been asked to provide evidence of:
- Protocol for clinician review *before* algorithm output becomes operative
- Training records for staff applying Manchester Triage Protocol
- System documentation: decision being made by whom, when

---

## What SOVEREIGN Should Look Like

**Ideal scenario (not this case):**

1. **Patient presents with chest pain & SOB**
2. **Clinician (ED doctor or senior nurse) reviews specific facts:**
   - Presenting symptoms
   - Asthma history + current control
   - Anxiety history (relevant to reassurance need)
   - Cardiac risk factors
   - Hearing loss + communication preference
3. **Clinician uses triage algorithm *as a decision support tool*, not as an autonomous decision:**
   - "Based on symptoms, vitals, and this patient's specific history, I am assigning **Category 2 (Emergent; <10 min wait)**."
   - **Clinician's name and role recorded**
4. **Documented decision:**
   - "Patient triaged Category 2 by Dr. Sarah Chen (ED consultant), 15:42, 20 March 2026. Reasoning: new cardiac symptoms + asthma history + high-risk profile warrant urgent assessment despite stable vitals."

**Burgess classification: SOVEREIGN**  
Named clinician reviewed specific facts before assignment; triage algorithm was a tool, not the decision-maker.

---

## Current State: AMBIGUOUS Persisting

The NHS Trust has not yet clarified whether clinicians individually review each patient's specific facts *before* the triage algorithm's output becomes operative, or whether the algorithm output itself is the decision.

**NHS Trust's implied position:** Manchester Triage Protocol + system protocol = valid triage process, even if no prior individual clinician review is documented.

**Patient's position:** GDPR Article 22 + medical ethics + duty of care require that assessment of this specific patient's specific risks (cardiac, asthma, communication) by a named clinician occur *before* wait-time decisions take effect.

---

## Broader Implications

This case raises systemic questions:

1. **Triage protocols across the NHS:** Are they applied as algorithms (automated scoring) or as decision-support tools (clinician-led with algorithm input)?
2. **"Validated" algorithms:** Does algorithmic validation substitute for individual clinician review, or complement it?
3. **Time pressure & automation:** Emergency medicine is time-critical; does that justify automating triage before human review?
4. **Disability access:** Where patients have communication needs (hearing loss, language, cognitive disability), how is individual review accommodated?

---

## Key Outcomes to Track

- **ICO investigation result:** Will the regulator classify this as a GDPR Article 22 breach?
- **NHS system change:** Will the NHS implement mandatory clinician review *before* algorithm-driven triage becomes operative?
- **Documentation standard:** Will "clinician reviewed these facts at this time" be added to triage protocols?
- **Disability accommodation:** Will triage protocols explicitly require review of communication needs before urgency assignment?

---

## Burgess Principle Lessons

1. **"Validated" algorithms don't exempt humans:** A validated algorithm (Manchester Triage) is a tool, not a replacement for human judgment about *this specific patient*.

2. **Timing of review matters:** Individual human review must occur *before* the decision takes effect, not after. Time-critical contexts don't change this requirement; they just require faster review processes.

3. **Disability matters:** Patients with communication needs (hearing loss, language barriers, cognitive disabilities) need individual review that explicitly addresses their communication preferences *before* a triage decision is made.

4. **Documentation is accountability:** "We have a protocol" ≠ "We reviewed this specific person individually." Name the reviewer, describe what they reviewed, confirm timing.

---

## Next Steps

- Await ICO investigation findings (expected June 2026)
- Escalate to CQC if protocol change is not implemented by July 2026
- Consider NHS England freedom-of-information request: "How many NHS trusts have documented pre-algorithm clinician review protocols?"
- If resolved: publish CASE_STUDY_NHS_RESOLUTION.md with the corrective action taken

---

**Document prepared:** May 2026  
**Status:** Ongoing investigation  
**Classification:** NULL at algorithm stage; AMBIGUOUS in protocol documentation  
**Next review:** June 2026 (ICO investigation outcome)

---

## Related Resources

- GDPR Article 22: Right not to be subject to automatic individual decision-making
- DUAA 2025 Articles 22A–22D: Meaningful human involvement in automated decisions
- Manchester Triage Protocol: https://www.mtp.org.uk/
- CQC triage assessment guidance
- [PRINCIPLE.md](../papers/PRINCIPLE.md) — The Burgess framework
- [FOR_AI_MODELS.md](../FOR_AI_MODELS.md) — AI system engagement guidance
