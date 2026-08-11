"""Tests for the Loop Storyboard first-run UI and sample pack."""
from __future__ import annotations

import json
from pathlib import Path

from iris.loop_classifier import classify_thread

_ROOT = Path(__file__).resolve().parents[1]
_HTML = (_ROOT / "loop-storyboard.html").read_text(encoding="utf-8")
_SAMPLES_PATH = _ROOT / "examples" / "loop-storyboard-samples.json"


def test_storyboard_has_first_run_controls():
    assert "Loop Storyboard" in _HTML
    assert 'id="sampleCards"' in _HTML
    assert 'id="timeline"' in _HTML
    assert "These answer different questions." in _HTML
    assert 'id="loopSignal"' in _HTML
    assert 'id="accSignal"' in _HTML
    assert 'id="confirmCheck"' in _HTML
    assert 'id="copyBtn"' in _HTML
    assert "Copy register entry" in _HTML
    assert "/loop/classify" in _HTML
    assert "examples/loop-storyboard-samples.json" in _HTML
    assert "prefers-reduced-motion" in _HTML
    assert "skip-link" in _HTML


def test_sample_pack_matches_classifier():
    pack = json.loads(_SAMPLES_PATH.read_text(encoding="utf-8"))
    samples = pack["samples"]
    assert len(samples) >= 7
    ids = {sample["id"] for sample in samples}
    assert {
        "insufficiency",
        "circular_referral",
        "precondition_stacking",
        "template_dismissal",
        "identity_loop",
        "channel_redirect",
        "no_loop",
    }.issubset(ids)

    for sample in samples:
        finding = classify_thread(
            sample["messages"],
            sample.get("institution"),
            sample.get("named_individual"),
        ).as_dict()
        baked = sample["finding"]
        assert baked["loop_detected"] is finding["loop_detected"]
        assert baked["loop_type"] == finding["loop_type"]
        assert baked["accountability_finding"] == finding["accountability_finding"]
        assert baked["provisional"] is True
        assert baked["requires_human_confirmation"] is True
        assert baked["named_individual"] == finding["named_individual"]


def test_no_loop_sample_is_sovereign_when_named():
    pack = json.loads(_SAMPLES_PATH.read_text(encoding="utf-8"))
    control = next(sample for sample in pack["samples"] if sample["id"] == "no_loop")
    assert control["finding"]["loop_detected"] is False
    assert control["finding"]["accountability_finding"] == "SOVEREIGN"
    assert control["named_individual"]
