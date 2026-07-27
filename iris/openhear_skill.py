"""
OpenHear skill for Iris — build orchestration + rights advisory.

Two modes, one sovereignty frame.

**Mode 1: Build Orchestration**
    Iris guides a deaf or hard-of-hearing citizen through building their own
    OpenHear device — hardware assembly, firmware, DSP pipeline, BLE pairing.
    Step-by-step, diagnostic, conversational. The build is treated as a
    sovereign act: you own this device, you control it, no gatekeeping required.

    Orchestration covers: hardware checklist, driver/USB setup, firmware flash,
    DSP routing and connectivity. It does NOT cover clinical tuning (gain,
    frequency response for a specific hearing loss profile) — that is the user's
    own sovereign domain, with signposting to audiologist support if wanted.

**Mode 2: Rights Advisory**
    Iris applies EA 2010 ss.20/21 anticipatory duty and the binary test to
    situations where an institution has failed to account for an OpenHear user —
    treating NHS-prescribed devices as the only valid category, refusing to
    accommodate a sovereign build, or making decisions about a user's hearing
    needs without named individual review of their specific facts.

    The anticipatory duty runs ahead of any request: an institution must already
    have considered how to accommodate someone using a non-NHS device before
    that person walks through the door.

Design principles (shared with null_hunter and decline_compliance, load-bearing):

* **Advisory only throughout.** ``requires_human_confirmation = True`` on all
  rights findings. No clinical advice — gain settings, frequency response, and
  audiological calibration are out of scope and explicitly signed away from.
* **Build orchestration is technical, not medical.** Routing audio through a
  DSP pipeline and confirming BLE pairing is engineering, not audiology.
* **Local-first.** Pure standard library. No network calls from this module.
* **Transparent.** Every recommendation states its basis.
* **The user owns the device.** Every output reinforces sovereignty, not
  dependence.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__all__ = [
    "BuildStage",
    "BuildSession",
    "BuildOrchestrator",
    "RightsAdvisor",
    "RightsSignal",
    "OpenHearSkill",
    "assess_context",
]

# ---------------------------------------------------------------------------
# Hardware constants (Noahlink Wireless dongle — confirmed against hardware)
# ---------------------------------------------------------------------------

NOAHLINK_VID = 0x16F0
NOAHLINK_PID = 0x0003
NOAHLINK_USB_ID = f"{NOAHLINK_VID:04X}:{NOAHLINK_PID:04X}"  # "16F0:0003"

OPENHEAR_HARDWARE = {
    "mcu": "ESP32-S3",
    "haptic_actuators": 24,
    "actuator_type": "LRA (Linear Resonant Actuator)",
    "pcb": "4-layer, 65×30mm, ENIG finish",
    "form_factor": "wristband",
    "dongle_vid": NOAHLINK_VID,
    "dongle_pid": NOAHLINK_PID,
    "dongle_usb_id": NOAHLINK_USB_ID,
    "connectivity": "BLE (Bluetooth Low Energy) + USB (dongle)",
    "pipeline": "sovereign audio DSP → haptic transduction (sound-to-wrist vibration)",
}

OPENHEAR_REPO = "https://github.com/ljbudgie/openhear"

# ---------------------------------------------------------------------------
# Build stage model
# ---------------------------------------------------------------------------

class BuildStage(str, Enum):
    """Ordered stages of an OpenHear build."""
    PREREQUISITES    = "prerequisites"
    HARDWARE         = "hardware_assembly"
    FIRMWARE         = "firmware_flash"
    USB_DRIVER       = "usb_driver_setup"
    DSP_ROUTING      = "dsp_routing"
    BLE_PAIRING      = "ble_pairing"
    IRIS_BRIDGE      = "iris_bridge"
    FUNCTIONAL_TEST  = "functional_test"
    COMPLETE         = "complete"

_STAGE_ORDER = list(BuildStage)

_STAGE_GUIDANCE: dict[BuildStage, dict] = {
    BuildStage.PREREQUISITES: {
        "title": "Prerequisites — what you need before you start",
        "description": (
            "Before assembling hardware, confirm you have:\n"
            "  • ESP32-S3 development board (or OpenHear PCB from PCBWay)\n"
            f"  • Noahlink Wireless USB dongle (USB ID {NOAHLINK_USB_ID})\n"
            "  • 24× LRA haptic actuators (confirm LRA, not ERM)\n"
            "  • USB-C cable (data-capable, not charge-only)\n"
            "  • Computer running Linux, macOS, or Windows with Python 3.11+\n"
            "  • Git installed\n\n"
            f"Clone the OpenHear repo: git clone {OPENHEAR_REPO}"
        ),
        "questions": [
            "Do you have all the hardware listed above?",
            "Have you cloned the OpenHear repo?",
            "What operating system are you building on?",
        ],
    },
    BuildStage.HARDWARE: {
        "title": "Hardware assembly — PCB and actuators",
        "description": (
            "Attach the 24 LRA actuators to the PCB in the wristband layout.\n"
            "The PCB is 4-layer, 65×30mm — handle with care around the edges.\n"
            "  • Solder or use the connector footprints — check the OpenHear repo\n"
            "    for the specific layout diagram for your PCB revision.\n"
            "  • Confirm each actuator is oriented correctly (polarity matters for LRA).\n"
            "  • Do not power on yet — complete the wiring check first."
        ),
        "questions": [
            "Which PCB revision do you have?",
            "Are all 24 actuators attached and oriented?",
            "Have you done a continuity check before first power-on?",
        ],
    },
    BuildStage.FIRMWARE: {
        "title": "Firmware — flashing the ESP32-S3",
        "description": (
            "Flash the OpenHear firmware to your ESP32-S3:\n"
            "  1. Connect ESP32-S3 via USB-C in flash mode (hold BOOT, press RESET,\n"
            "     release RESET, release BOOT).\n"
            "  2. Install esptool: pip install esptool\n"
            "  3. From the OpenHear repo: python -m esptool flash_id\n"
            "     (confirm the chip is detected before flashing)\n"
            "  4. Follow the firmware/README.md in the OpenHear repo for your\n"
            "     specific firmware version.\n\n"
            "⚠ If esptool does not detect the chip, check your USB cable is\n"
            "  data-capable and try a different port."
        ),
        "questions": [
            "Is the ESP32-S3 detected by esptool (flash_id)?",
            "Which firmware version are you flashing?",
            "Did the flash complete without errors?",
        ],
    },
    BuildStage.USB_DRIVER: {
        "title": "USB driver — Noahlink Wireless dongle",
        "description": (
            f"The Noahlink Wireless dongle (USB ID {NOAHLINK_USB_ID}) must be\n"
            "recognised by your OS before the DSP pipeline can use it.\n\n"
            "Linux:\n"
            "  lsusb | grep 16F0\n"
            "  If absent: check dmesg | tail -20 after plugging in.\n"
            "  You may need a udev rule:\n"
            '  echo \'SUBSYSTEM=="usb", ATTR{idVendor}=="16f0", '
            'ATTR{idProduct}=="0003", MODE="0666"\' \\\n'
            "  | sudo tee /etc/udev/rules.d/99-openhear.rules\n"
            "  sudo udevadm control --reload-rules\n\n"
            "macOS:\n"
            "  system_profiler SPUSBDataType | grep -A5 '16F0'\n"
            "  (Usually works without a driver — confirm in System Information.)\n\n"
            "Windows:\n"
            "  Device Manager → check for Unknown Device under USB controllers.\n"
            "  Install via Zadig (libusb driver) if not auto-detected."
        ),
        "questions": [
            "What OS are you on?",
            "Is the dongle detected (lsusb / System Information / Device Manager)?",
            "Any error messages when plugging in?",
        ],
    },
    BuildStage.DSP_ROUTING: {
        "title": "DSP pipeline — audio routing (technical, not clinical)",
        "description": (
            "Configure the OpenHear DSP routing layer.\n\n"
            "This step sets up HOW audio moves through the pipeline:\n"
            "  • Input source → DSP engine → haptic actuator mapping\n"
            "  • Channel routing (L/R separation)\n"
            "  • Latency buffering\n\n"
            "⚠ SCOPE BOUNDARY — what Iris does NOT cover here:\n"
            "  Gain levels, frequency response curves, equalisation profiles,\n"
            "  and audiological calibration for your specific hearing loss are\n"
            "  outside Iris's scope. Those are yours to determine — from your\n"
            "  own audiogram, your own experience, and if you choose, with an\n"
            "  audiologist who will engage with your sovereign build.\n\n"
            "  The OpenHear repo contains example DSP configurations. Start\n"
            "  with the default routing profile and adjust from there.\n\n"
            "Follow: firmware/config/dsp_routing.yaml in the OpenHear repo."
        ),
        "questions": [
            "Have you reviewed the default DSP routing config in the repo?",
            "Is audio flowing from input to the haptic layer in the logs?",
            "Any routing errors in the console?",
        ],
    },
    BuildStage.BLE_PAIRING: {
        "title": "BLE pairing — wristband to host",
        "description": (
            "Pair the ESP32-S3 wristband to your host device via BLE.\n\n"
            "  1. Power on the wristband — the ESP32-S3 will advertise.\n"
            "  2. On the host: open the OpenHear web interface (BLE Web API).\n"
            "  3. Click 'Connect' — the browser will show available BLE devices.\n"
            "  4. Select 'OpenHear' from the list and pair.\n"
            "  5. Confirm the wristband acknowledges (actuator pulse on successful pair).\n\n"
            "BLE Web API requires Chrome or Edge (80+). Safari and Firefox do not\n"
            "currently support Web Bluetooth.\n\n"
            "If the device does not appear: confirm ESP32-S3 firmware is running\n"
            "(check serial output at 115200 baud), and ensure you are within ~10m."
        ),
        "questions": [
            "Is the wristband advertising (visible in browser BLE scan)?",
            "Did pairing complete — do you see the actuator acknowledge pulse?",
            "What browser are you using?",
        ],
    },
    BuildStage.IRIS_BRIDGE: {
        "title": "Iris Bridge — haptic feedback from Burgess classifications",
        "description": (
            "The Iris Bridge maps Burgess Principle classification outcomes to\n"
            "haptic patterns on your wristband. This is local-first — no cloud.\n\n"
            "Pattern mapping:\n"
            "  SOVEREIGN  → steady triple pulse (confident, clear)\n"
            "  AMBIGUOUS  → double pulse with pause (uncertain, wait)\n"
            "  NULL       → long single hold (alert, act)\n\n"
            "To activate: in the OpenHear web interface, enable 'Iris Bridge'\n"
            "from the settings panel. The bridge listens on localhost via the\n"
            "BLE Web API — no data leaves your device.\n\n"
            "This is the physical expression of the binary test: when Iris\n"
            "classifies an institutional response, you feel it."
        ),
        "questions": [
            "Is the Iris Bridge enabled in the web interface?",
            "Are you getting haptic feedback on test classifications?",
            "Do the patterns match the SOVEREIGN/AMBIGUOUS/NULL mapping above?",
        ],
    },
    BuildStage.FUNCTIONAL_TEST: {
        "title": "Functional test — end-to-end verification",
        "description": (
            "Run a full end-to-end test before using OpenHear in the real world.\n\n"
            "  1. Play a known audio source through the DSP pipeline.\n"
            "  2. Confirm haptic actuation across all 24 LRAs (use the test\n"
            "     pattern in the OpenHear repo: firmware/test/actuator_sweep.py).\n"
            "  3. Trigger a test Iris classification and confirm the Bridge\n"
            "     pattern fires correctly on the wristband.\n"
            "  4. Check latency — the haptic response should feel near-instant.\n\n"
            "Log the test output. This is your build record — the evidence that\n"
            "your device works, timestamped, on your machine."
        ),
        "questions": [
            "Did all 24 actuators fire in the sweep test?",
            "Is latency acceptable?",
            "Did the Iris Bridge patterns fire correctly?",
        ],
    },
    BuildStage.COMPLETE: {
        "title": "Build complete — your device, your sovereignty",
        "description": (
            "You have built your own hearing device.\n\n"
            "This is the sovereignty principle made physical. No audiologist\n"
            "gatekeeping required. No NHS waiting list. No proprietary firmware\n"
            "you cannot inspect. You own this — the hardware, the firmware,\n"
            "the pipeline, the data.\n\n"
            "What happens next is yours:\n"
            "  • Tune the DSP from your own experience and audiogram.\n"
            "  • Seek an audiologist who will engage with your build if you want\n"
            "    clinical input — and if they refuse, Iris can help you understand\n"
            "    what the anticipatory duty requires of them.\n"
            "  • Contribute back to the OpenHear repo.\n"
            "  • Tell Iris about any institution that fails to accommodate your\n"
            "    sovereign device — we will apply the binary test together."
        ),
        "questions": [],
    },
}


# ---------------------------------------------------------------------------
# Build orchestrator
# ---------------------------------------------------------------------------

@dataclass
class BuildSession:
    """Tracks where a user is in an OpenHear build."""
    current_stage: BuildStage = BuildStage.PREREQUISITES
    completed_stages: list[BuildStage] = field(default_factory=list)
    os_platform: Optional[str] = None
    pcb_revision: Optional[str] = None
    notes: list[str] = field(default_factory=list)

    def advance(self) -> bool:
        """Move to the next stage. Returns False if already complete."""
        idx = _STAGE_ORDER.index(self.current_stage)
        if idx + 1 >= len(_STAGE_ORDER):
            return False
        self.completed_stages.append(self.current_stage)
        self.current_stage = _STAGE_ORDER[idx + 1]
        return True

    @property
    def progress(self) -> str:
        total = len(_STAGE_ORDER) - 1  # COMPLETE is the end state
        done = len(self.completed_stages)
        return f"{done}/{total} stages complete"


class BuildOrchestrator:
    """
    Guides a user through building an OpenHear device, stage by stage.

    This is a conversational orchestrator, not an IDE. It asks diagnostic
    questions, provides the right guidance for the current stage, and advances
    when the user confirms readiness. It does not execute commands on the user's
    machine — it provides them for the user to run.

    Clinical tuning (gain, frequency response, EQ for specific hearing loss)
    is explicitly out of scope. The orchestrator handles the engineering layer
    only. See CLINICAL_SCOPE_BOUNDARY below.
    """

    CLINICAL_SCOPE_BOUNDARY = (
        "⚠ SCOPE BOUNDARY\n"
        "Iris can help you build OpenHear and get it working technically.\n"
        "Gain levels, frequency response curves, and audiological calibration\n"
        "for your specific hearing profile are yours to determine — from your\n"
        "own audiogram and experience. If you want clinical input on those\n"
        "settings, an audiologist who will engage with your sovereign build\n"
        "is the right resource. If they refuse, come back to Iris and we will\n"
        "apply the binary test and anticipatory duty together."
    )

    def guide(self, session: BuildSession) -> "BuildGuidance":
        """Return the guidance for the current build stage."""
        stage = session.current_stage
        info = _STAGE_GUIDANCE[stage]
        return BuildGuidance(
            stage=stage,
            title=info["title"],
            description=info["description"],
            questions=info["questions"],
            progress=session.progress,
            hardware_ref=OPENHEAR_HARDWARE,
            repo=OPENHEAR_REPO,
        )

    def diagnose(self, session: BuildSession, symptom: str) -> "DiagnosticResult":
        """
        Match a user-reported symptom to known issues for the current stage.
        Returns targeted troubleshooting steps.
        """
        symptom_lower = symptom.lower()
        stage = session.current_stage
        issues = _KNOWN_ISSUES.get(stage, [])
        matched = [i for i in issues if any(kw in symptom_lower for kw in i["keywords"])]
        if not matched:
            return DiagnosticResult(
                matched=False,
                steps=["Check the OpenHear repo issues tab for similar reports."],
                repo=OPENHEAR_REPO,
            )
        return DiagnosticResult(
            matched=True,
            steps=[step for issue in matched for step in issue["steps"]],
            repo=OPENHEAR_REPO,
        )


@dataclass
class BuildGuidance:
    stage: BuildStage
    title: str
    description: str
    questions: list[str]
    progress: str
    hardware_ref: dict
    repo: str

    def __str__(self) -> str:
        lines = [
            f"[OpenHear Build — {self.progress}]",
            f"Stage: {self.title}",
            "",
            self.description,
        ]
        if self.questions:
            lines += ["", "Before advancing, confirm:"]
            for q in self.questions:
                lines.append(f"  • {q}")
        return "\n".join(lines)


@dataclass
class DiagnosticResult:
    matched: bool
    steps: list[str]
    repo: str

    def __str__(self) -> str:
        if not self.matched:
            return (
                f"No known issue matched. Check {self.repo}/issues for similar reports.\n"
                "Describe the exact error message or behaviour and Iris will try again."
            )
        return "Troubleshooting steps:\n" + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(self.steps))


_KNOWN_ISSUES: dict[BuildStage, list[dict]] = {
    BuildStage.USB_DRIVER: [
        {
            "keywords": ["not detected", "not found", "lsusb", "no device", "unknown device"],
            "steps": [
                f"Confirm the dongle USB ID is {NOAHLINK_USB_ID} — run: lsusb | grep 16F0",
                "Check dmesg | tail -20 immediately after plugging in for error messages.",
                "Try a different USB port and a different cable (data-capable, not charge-only).",
                "On Linux: add the udev rule in the driver guidance above and reload rules.",
                "On Windows: use Zadig to install the libusb driver for the dongle.",
            ],
        },
        {
            "keywords": ["permission", "access denied", "cannot open"],
            "steps": [
                "Add yourself to the dialout/plugdev group: sudo usermod -aG plugdev $USER",
                "Log out and back in for the group change to take effect.",
                "Confirm the udev rule has MODE=\"0666\".",
            ],
        },
    ],
    BuildStage.FIRMWARE: [
        {
            "keywords": ["not detected", "esptool", "no chip", "failed to connect"],
            "steps": [
                "Confirm the ESP32-S3 is in flash mode: hold BOOT, press RESET, release RESET, release BOOT.",
                "Use a data-capable USB-C cable — many cables are charge-only.",
                "Try a different USB port.",
                "Check: python -m esptool chip_id — if it times out, repeat flash mode entry.",
            ],
        },
        {
            "keywords": ["wrong chip", "unsupported chip"],
            "steps": [
                "Confirm your board is ESP32-S3 (not ESP32, ESP32-S2, or ESP32-C3).",
                "Check the chip marking on the module — ESP32-S3-WROOM or ESP32-S3-MINI.",
            ],
        },
    ],
    BuildStage.BLE_PAIRING: [
        {
            "keywords": ["not visible", "not found", "not showing", "no device"],
            "steps": [
                "Confirm the ESP32-S3 firmware is running — check serial output at 115200 baud.",
                "Ensure you are within ~10 metres of the device.",
                "Use Chrome or Edge — BLE Web API is not supported in Safari or Firefox.",
                "On Android: grant location permission to the browser (required for BLE scan).",
                "Try restarting the ESP32-S3 (press RESET) and re-scanning.",
            ],
        },
        {
            "keywords": ["paired", "connected", "no haptic", "no feedback"],
            "steps": [
                "Confirm the firmware version supports haptic feedback (check OpenHear repo tags).",
                "Run the actuator sweep test: firmware/test/actuator_sweep.py",
                "Check wiring continuity between the PCB and actuators.",
            ],
        },
    ],
    BuildStage.DSP_ROUTING: [
        {
            "keywords": ["no audio", "no sound", "silent", "nothing"],
            "steps": [
                "Check the input source is selected in dsp_routing.yaml.",
                "Confirm the Noahlink dongle is detected before starting the DSP engine.",
                "Check the DSP engine log for routing errors.",
                "Try the default configuration first before any custom changes.",
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# Rights advisory
# ---------------------------------------------------------------------------

_RIGHTS_TRIGGER_PATTERNS = [
    (re.compile(r"(won.t|won't|refuse|refuse[ds]?|not accept|not support|don.t support|can.t use)\b.{0,40}\b(openhear|device|my own|sovereign|open.source|non.nhs|not nhs|self.built|built)", re.I), "institution_refusal"),
    (re.compile(r"(nhs only|nhs.approved|approved device|certified device|prescribed device)", re.I), "nhs_gatekeeping"),
    (re.compile(r"(audiologist|audiology).{0,40}(refuse|won.t|can.t|won't|isn.t supported)", re.I), "audiologist_refusal"),
    (re.compile(r"(workplace|employer|school|college|university|hospital).{0,40}(hearing|device|openhear|accommodation)", re.I), "workplace_accommodation"),
    (re.compile(r"(discriminat|equality act|reasonable adjustment|adjust)", re.I), "rights_query"),
]


@dataclass
class RightsSignal:
    """A rights-relevant pattern detected in user input."""
    signal_type: str
    confidence: str  # "HIGH", "MEDIUM", "LOW"
    advisory: str
    binary_test_triggered: bool
    requires_human_confirmation: bool = True
    clinical_scope_note: Optional[str] = None


class RightsAdvisor:
    """
    Advisory layer — EA 2010 anticipatory duty and binary test for OpenHear contexts.

    This class detects when a user's description of an institutional response
    suggests a potential EA 2010 breach, and provides advisory framing.

    All findings carry ``requires_human_confirmation = True``. This is a
    heuristic aid, not a legal verdict.
    """

    ANTICIPATORY_DUTY_NOTE = (
        "Under EA 2010 ss.20/21, the anticipatory duty runs AHEAD of any request.\n"
        "An institution must already have considered how to accommodate someone\n"
        "using a non-NHS hearing device before you walk through the door — not\n"
        "wait until you ask, and not impose an NHS-only requirement without\n"
        "individual consideration of your specific situation.\n\n"
        "'We only support NHS-approved devices' is a provision, criterion, or\n"
        "practice (PCP). If it puts deaf or hard-of-hearing people who use\n"
        "sovereign builds at a particular disadvantage, that is prima facie s.19\n"
        "indirect discrimination — unless it can be objectively justified."
    )

    def assess(self, user_input: str) -> list[RightsSignal]:
        """Detect rights-relevant patterns and return advisory signals."""
        signals = []
        for pattern, signal_type in _RIGHTS_TRIGGER_PATTERNS:
            if pattern.search(user_input):
                signals.append(self._build_signal(signal_type))
        return signals

    def _build_signal(self, signal_type: str) -> RightsSignal:
        if signal_type == "institution_refusal":
            return RightsSignal(
                signal_type=signal_type,
                confidence="HIGH",
                advisory=(
                    "An institution refusing to accommodate your OpenHear device\n"
                    "may be applying a provision, criterion, or practice (PCP)\n"
                    "that puts you at a particular disadvantage — EA 2010 s.19.\n\n"
                    + self.ANTICIPATORY_DUTY_NOTE + "\n\n"
                    "Binary test triggered: did a named individual apply their\n"
                    "mind to the specific facts of your situation — your device,\n"
                    "your hearing profile, your access need — before refusing?\n"
                    "If not, that is a NULL finding and a starting point for\n"
                    "escalation under EA 2010 and DUAA 2025 Arts. 22A–22D."
                ),
                binary_test_triggered=True,
            )
        elif signal_type == "nhs_gatekeeping":
            return RightsSignal(
                signal_type=signal_type,
                confidence="HIGH",
                advisory=(
                    "'NHS-approved devices only' is a PCP. Applied without\n"
                    "individual assessment of your specific circumstances, it\n"
                    "is prima facie indirect discrimination under EA 2010 s.19.\n\n"
                    + self.ANTICIPATORY_DUTY_NOTE + "\n\n"
                    "Ask in writing: 'Please provide the name and role of the\n"
                    "person who considered the specific facts of my hearing\n"
                    "situation before applying this policy to me.' Apply the\n"
                    "binary test to the response."
                ),
                binary_test_triggered=True,
            )
        elif signal_type == "audiologist_refusal":
            return RightsSignal(
                signal_type=signal_type,
                confidence="MEDIUM",
                advisory=(
                    "An audiologist refusing to engage with your OpenHear build\n"
                    "may be applying a blanket policy rather than considering\n"
                    "your specific situation. That triggers both the anticipatory\n"
                    "duty (did they already consider non-standard devices?) and\n"
                    "the binary test (did a named person apply their mind to\n"
                    "your specific facts?).\n\n"
                    "Note: clinical recommendations (what settings to use for\n"
                    "your hearing loss) remain the audiologist's domain. The\n"
                    "question here is whether they ENGAGED — not what they said."
                ),
                binary_test_triggered=True,
                clinical_scope_note=(
                    "Iris cannot advise on the clinical content of an audiologist's\n"
                    "assessment. The rights question (did they engage?) is separate\n"
                    "from the clinical question (what did they recommend?)."
                ),
            )
        elif signal_type == "workplace_accommodation":
            return RightsSignal(
                signal_type=signal_type,
                confidence="MEDIUM",
                advisory=(
                    "Workplace, educational, and healthcare settings have\n"
                    "anticipatory duties under EA 2010 ss.20/21 to accommodate\n"
                    "disabled people's communication needs — including non-standard\n"
                    "hearing devices. A failure to make reasonable adjustments for\n"
                    "an OpenHear user is the same legal question as any other\n"
                    "hearing accommodation failure.\n\n"
                    "Apply the binary test: did a named individual consider the\n"
                    "specific facts of your situation before the accommodation\n"
                    "decision was made? If not — NULL."
                ),
                binary_test_triggered=True,
            )
        else:  # rights_query
            return RightsSignal(
                signal_type=signal_type,
                confidence="LOW",
                advisory=(
                    "You have rights around hearing device accommodation under\n"
                    "EA 2010 ss.20/21. Tell Iris more about the specific situation\n"
                    "— what institution, what decision, what they said — and Iris\n"
                    "will apply the binary test and anticipatory duty framing."
                ),
                binary_test_triggered=False,
            )


# ---------------------------------------------------------------------------
# Top-level skill entry point
# ---------------------------------------------------------------------------

@dataclass
class SkillResult:
    """Combined result from the OpenHear skill."""
    mode: str  # "build" | "rights" | "both" | "none"
    build_guidance: Optional[BuildGuidance] = None
    diagnostic: Optional[DiagnosticResult] = None
    rights_signals: list[RightsSignal] = field(default_factory=list)
    requires_human_confirmation: bool = False
    clinical_scope_note: Optional[str] = None


_BUILD_TRIGGER = re.compile(
    r"\b(build|assemble|flash|firmware|esp32|actuator|lra|pcb|noahlink|openhear|dongle|ble|pair|haptic|dsp)\b",
    re.I,
)

_RIGHTS_TRIGGER = re.compile(
    r"\b(rights?|discriminat|adjust|nhs|refuse|accept|employer|workplace|audiolog|accommodation|equality act|binary test|sovereign|null|ambiguous)\b",
    re.I,
)


class OpenHearSkill:
    """
    Top-level OpenHear skill — routes to build orchestration, rights advisory,
    or both based on the user's input.

    Usage::

        skill = OpenHearSkill()
        session = BuildSession()
        result = skill.assess("The dongle isn't being detected by lsusb", session)
        print(result.diagnostic)
    """

    def __init__(self) -> None:
        self._orchestrator = BuildOrchestrator()
        self._advisor = RightsAdvisor()

    def assess(self, user_input: str, build_session: Optional[BuildSession] = None) -> SkillResult:
        """
        Assess user input and return the appropriate OpenHear skill response.

        Parameters
        ----------
        user_input:
            The user's message or description.
        build_session:
            An existing BuildSession if a build is in progress.
            Pass None for a first contact or rights-only query.
        """
        is_build = bool(_BUILD_TRIGGER.search(user_input))
        is_rights = bool(_RIGHTS_TRIGGER.search(user_input))

        rights_signals = self._advisor.assess(user_input)
        has_rights = bool(rights_signals)
        has_clinical = any(s.clinical_scope_note for s in rights_signals)

        mode = "none"
        guidance = None
        diagnostic = None

        if is_build and build_session:
            mode = "build" if not has_rights else "both"
            # Check if this is a symptom/problem description
            problem_words = re.compile(r"\b(not|no|can.t|won.t|failed|error|broken|stuck|help)\b", re.I)
            if problem_words.search(user_input):
                diagnostic = self._orchestrator.diagnose(build_session, user_input)
            guidance = self._orchestrator.guide(build_session)
        elif is_build and not build_session:
            mode = "build" if not has_rights else "both"
            build_session = BuildSession()
            guidance = self._orchestrator.guide(build_session)
        elif has_rights:
            mode = "rights"

        clinical_note = BuildOrchestrator.CLINICAL_SCOPE_BOUNDARY if has_clinical else None

        return SkillResult(
            mode=mode,
            build_guidance=guidance,
            diagnostic=diagnostic,
            rights_signals=rights_signals,
            requires_human_confirmation=has_rights,
            clinical_scope_note=clinical_note,
        )


def assess_context(user_input: str, build_session: Optional[BuildSession] = None) -> SkillResult:
    """Module-level convenience function."""
    return OpenHearSkill().assess(user_input, build_session)
