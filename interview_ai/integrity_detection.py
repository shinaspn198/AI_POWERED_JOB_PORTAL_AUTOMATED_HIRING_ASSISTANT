"""
Day 49 - Malpractice & Integrity Detection Engine

Purpose:
Detect cheating, unauthorized aids, and external assistance during interviews
via multimodal signal tracking, threshold rules, pattern correlation,
real-time warning escalation, and behavioral signal integration.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


# =========================================================
# 1. MALPRACTICE SIGNALS DEFINITION
# =========================================================

MALPRACTICE_SIGNALS = {
    "tab_switching_frequency": {
        "name": "Tab Switching Frequency",
        "description": "Tracks count and rate of browser tab changes or window focus shifts.",
        "unit": "events",
        "severity_weight": 0.25,
    },
    "screen_focus_loss": {
        "name": "Loss of Screen Focus",
        "description": "Measures cumulative and sustained duration spent away from interview screen.",
        "unit": "seconds",
        "severity_weight": 0.25,
    },
    "external_voice_detection": {
        "name": "External Voice Detection",
        "description": "Identifies secondary speaker voices, whispers, or acoustic overlaps.",
        "unit": "events",
        "severity_weight": 0.30,
    },
    "repeated_looking_away": {
        "name": "Repeated Looking Away",
        "description": "Tracks frequent head pose yaw/pitch deviations and off-screen gaze shifts.",
        "unit": "events",
        "severity_weight": 0.20,
    },
}


def get_malpractice_signals() -> Dict[str, Dict[str, Any]]:
    """Return all defined malpractice signals."""
    return MALPRACTICE_SIGNALS.copy()


def get_signal_names() -> List[str]:
    """Return the display names of all malpractice signals."""
    return [signal["name"] for signal in MALPRACTICE_SIGNALS.values()]


# =========================================================
# 2. DETECTION LOGIC: THRESHOLDS & PATTERNS
# =========================================================

SIGNAL_THRESHOLDS = {
    "tab_switching_frequency": {
        "warning": 2,      # >= 2 events: Warning
        "flag": 4,         # >= 4 events: Medium Flag
        "critical": 7,     # >= 7 events: Critical Flag
    },
    "screen_focus_loss": {
        "warning": 15.0,   # >= 15 seconds lost
        "flag": 45.0,      # >= 45 seconds lost
        "critical": 90.0,  # >= 90 seconds lost
    },
    "external_voice_detection": {
        "warning": 1,      # >= 1 instance: Warning
        "flag": 2,         # >= 2 instances: Medium Flag
        "critical": 4,     # >= 4 instances: Critical Flag
    },
    "repeated_looking_away": {
        "warning": 4,      # >= 4 gaze shifts: Warning
        "flag": 8,         # >= 8 gaze shifts: Medium Flag
        "critical": 14,    # >= 14 gaze shifts: Critical Flag
    },
}

SUSPICIOUS_PATTERNS = {
    "prompted_response": {
        "name": "Real-time External Prompting",
        "description": "External voice detected immediately followed by gaze diversion and answer delivery.",
        "penalty": 30,
        "risk_level": "HIGH",
    },
    "search_on_question": {
        "name": "Immediate Lookup on Question",
        "description": "Tab switch or screen focus loss occurring within 10 seconds of question delivery.",
        "penalty": 25,
        "risk_level": "HIGH",
    },
    "dual_screen_reading": {
        "name": "Secondary Screen Reading",
        "description": "Sustained off-center gaze (>5s) while answering technical questions without pause.",
        "penalty": 20,
        "risk_level": "MEDIUM",
    },
    "rapid_micro_switching": {
        "name": "Rapid Micro-Switching",
        "description": "Frequent short tab switches (<3s duration) indicating clipboard/notes lookup.",
        "penalty": 25,
        "risk_level": "HIGH",
    },
}


# =========================================================
# 3. WARNING & FLAGGING SYSTEM
# =========================================================

@dataclass
class IntegrityTelemetry:
    tab_switches: int = 0
    focus_loss_duration_sec: float = 0.0
    external_voice_events: int = 0
    looking_away_events: int = 0
    question_timestamp_sec: float = 0.0
    recent_events: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class IntegrityEvaluation:
    integrity_score: float                  # 0 to 100 (100 = completely clean)
    risk_tag: str                           # LOW, MEDIUM, HIGH, CRITICAL
    real_time_warnings: List[str]           # Candidate alerts
    recruiter_flags: List[str]              # Detailed auditor flags
    detected_patterns: List[Dict[str, Any]] # Correlated pattern matches
    behavioral_impact: Dict[str, Any]       # Adjusted confidence & impact


class IntegrityDetector:
    """Evaluates malpractice signals, flags violations, and calculates risk tags."""

    def __init__(self, thresholds: Optional[Dict] = None):
        self.thresholds = thresholds or SIGNAL_THRESHOLDS

    def evaluate_telemetry(
        self,
        telemetry: IntegrityTelemetry,
        behavioral_confidence_score: Optional[float] = None
    ) -> IntegrityEvaluation:
        score = 100.0
        warnings: List[str] = []
        flags: List[str] = []
        detected_patterns: List[Dict[str, Any]] = []

        # 1. Threshold Evaluation
        # Tab Switches
        if telemetry.tab_switches >= self.thresholds["tab_switching_frequency"]["critical"]:
            score -= 30.0
            flags.append(f"Critical: High tab switching count ({telemetry.tab_switches})")
            warnings.append("Critical: Multiple tab switches detected. This session will be flagged.")
        elif telemetry.tab_switches >= self.thresholds["tab_switching_frequency"]["flag"]:
            score -= 15.0
            flags.append(f"Warning: Multiple tab switches ({telemetry.tab_switches})")
            warnings.append("Warning: Tab switching is strictly monitored. Please return to the window.")
        elif telemetry.tab_switches >= self.thresholds["tab_switching_frequency"]["warning"]:
            score -= 5.0
            warnings.append("Please remain focused on the interview window.")

        # Focus Loss Duration
        if telemetry.focus_loss_duration_sec >= self.thresholds["screen_focus_loss"]["critical"]:
            score -= 25.0
            flags.append(f"Critical: Extended focus loss ({telemetry.focus_loss_duration_sec:.1f}s)")
            warnings.append("Critical: Extended screen focus loss detected.")
        elif telemetry.focus_loss_duration_sec >= self.thresholds["screen_focus_loss"]["flag"]:
            score -= 15.0
            flags.append(f"Warning: Significant focus loss ({telemetry.focus_loss_duration_sec:.1f}s)")
            warnings.append("Warning: Please keep the assessment screen active and visible.")
        elif telemetry.focus_loss_duration_sec >= self.thresholds["screen_focus_loss"]["warning"]:
            score -= 5.0
            warnings.append("Interview screen focus lost. Return to the assessment.")

        # External Voice
        if telemetry.external_voice_events >= self.thresholds["external_voice_detection"]["critical"]:
            score -= 35.0
            flags.append(f"Critical: Repeated external voice detected ({telemetry.external_voice_events} times)")
            warnings.append("Critical: Multiple external voice inputs detected.")
        elif telemetry.external_voice_events >= self.thresholds["external_voice_detection"]["flag"]:
            score -= 20.0
            flags.append(f"Warning: External speech detected ({telemetry.external_voice_events} times)")
            warnings.append("Warning: Background conversation detected. Ensure complete privacy.")
        elif telemetry.external_voice_events >= self.thresholds["external_voice_detection"]["warning"]:
            score -= 10.0
            warnings.append("Secondary voice activity detected. Ensure you are in a quiet room.")

        # Looking Away
        if telemetry.looking_away_events >= self.thresholds["repeated_looking_away"]["critical"]:
            score -= 20.0
            flags.append(f"Critical: Excessive gaze deviation ({telemetry.looking_away_events} times)")
            warnings.append("Critical: Persistent off-screen looking detected.")
        elif telemetry.looking_away_events >= self.thresholds["repeated_looking_away"]["flag"]:
            score -= 10.0
            flags.append(f"Warning: Repeatedly looking away from screen ({telemetry.looking_away_events} times)")
            warnings.append("Warning: Please face forward and look towards your screen.")
        elif telemetry.looking_away_events >= self.thresholds["repeated_looking_away"]["warning"]:
            score -= 5.0
            warnings.append("Please maintain eye contact with the camera.")

        # 2. Pattern Recognition Logic
        event_types = [e.get("type") for e in telemetry.recent_events]

        # Pattern: Prompted Response (voice + looking away)
        if "external_voice" in event_types and "looking_away" in event_types:
            pattern = SUSPICIOUS_PATTERNS["prompted_response"]
            score -= pattern["penalty"]
            detected_patterns.append(pattern)
            flags.append(f"Pattern Detected: {pattern['name']} - External prompting suspected")

        # Pattern: Search on Question (tab switch or focus loss right after question)
        has_quick_switch = any(
            e.get("type") in ("tab_switch", "focus_loss")
            and (e.get("timestamp", 0) - telemetry.question_timestamp_sec) < 10.0
            for e in telemetry.recent_events
        )
        if has_quick_switch:
            pattern = SUSPICIOUS_PATTERNS["search_on_question"]
            score -= pattern["penalty"]
            detected_patterns.append(pattern)
            flags.append(f"Pattern Detected: {pattern['name']} - Tab switched right after question")

        # Clamp Integrity Score between 0 and 100
        integrity_score = max(0.0, round(score, 2))

        # 3. Risk Tagging
        if integrity_score >= 85.0:
            risk_tag = "LOW_RISK"
        elif integrity_score >= 65.0:
            risk_tag = "MEDIUM_RISK"
        elif integrity_score >= 40.0:
            risk_tag = "HIGH_RISK"
        else:
            risk_tag = "CRITICAL_RISK"

        # 4. Behavioral Signal Integration
        behavioral_impact = self._integrate_behavioral_signals(
            integrity_score=integrity_score,
            risk_tag=risk_tag,
            baseline_confidence=behavioral_confidence_score
        )

        return IntegrityEvaluation(
            integrity_score=integrity_score,
            risk_tag=risk_tag,
            real_time_warnings=warnings,
            recruiter_flags=flags,
            detected_patterns=detected_patterns,
            behavioral_impact=behavioral_impact,
        )

    def _integrate_behavioral_signals(
        self,
        integrity_score: float,
        risk_tag: str,
        baseline_confidence: Optional[float]
    ) -> Dict[str, Any]:
        """
        Integrates malpractice findings with behavioral confidence metrics.
        If integrity is compromised, candidate's apparent behavioral confidence
        is penalized to prevent fraudulent high confidence scores.
        """
        if baseline_confidence is None:
            baseline_confidence = 75.0

        # Integrity discount factor: full confidence when 100, downscaled if integrity drops
        integrity_factor = integrity_score / 100.0
        adjusted_confidence = round(baseline_confidence * (0.5 + 0.5 * integrity_factor), 2)
        confidence_penalty = round(baseline_confidence - adjusted_confidence, 2)

        recommendation = "PROCEED"
        if risk_tag == "CRITICAL_RISK":
            recommendation = "DISQUALIFY_OR_MANUAL_AUDIT"
        elif risk_tag == "HIGH_RISK":
            recommendation = "FLAG_FOR_RECRUITER_REVIEW"
        elif risk_tag == "MEDIUM_RISK":
            recommendation = "PROCEED_WITH_SCRUTINY"

        return {
            "baseline_behavioral_confidence": baseline_confidence,
            "integrity_adjusted_confidence": adjusted_confidence,
            "confidence_penalty": confidence_penalty,
            "recommendation": recommendation,
        }


# =========================================================
# TEST / EXECUTION
# =========================================================

if __name__ == "__main__":
    print("=" * 65)
    print("DAY 49 - MALPRACTICE & INTEGRITY DETECTION")
    print("=" * 65)

    detector = IntegrityDetector()

    # Test Scenario 1: Clean Candidate
    clean_telemetry = IntegrityTelemetry(
        tab_switches=1,
        focus_loss_duration_sec=3.0,
        external_voice_events=0,
        looking_away_events=2,
        question_timestamp_sec=100.0,
        recent_events=[]
    )
    result_clean = detector.evaluate_telemetry(clean_telemetry, behavioral_confidence_score=85.0)

    print("\n[SCENARIO 1: CLEAN CANDIDATE]")
    print(f"Integrity Score : {result_clean.integrity_score}/100")
    print(f"Risk Tag        : {result_clean.risk_tag}")
    print(f"Warnings        : {result_clean.real_time_warnings or 'None'}")
    print(f"Recruiter Flags : {result_clean.recruiter_flags or 'None'}")
    print(f"Adjusted Conf.  : {result_clean.behavioral_impact['integrity_adjusted_confidence']}")
    print(f"Recommendation  : {result_clean.behavioral_impact['recommendation']}")

    # Test Scenario 2: Suspicious Candidate (External Prompting & Search)
    suspicious_telemetry = IntegrityTelemetry(
        tab_switches=5,
        focus_loss_duration_sec=50.0,
        external_voice_events=3,
        looking_away_events=9,
        question_timestamp_sec=200.0,
        recent_events=[
            {"type": "external_voice", "timestamp": 204.0},
            {"type": "looking_away", "timestamp": 205.0},
            {"type": "tab_switch", "timestamp": 206.0},
        ]
    )
    result_sus = detector.evaluate_telemetry(suspicious_telemetry, behavioral_confidence_score=90.0)

    print("\n[SCENARIO 2: SUSPICIOUS CANDIDATE]")
    print(f"Integrity Score : {result_sus.integrity_score}/100")
    print(f"Risk Tag        : {result_sus.risk_tag}")
    print("Real-time Alerts:")
    for w in result_sus.real_time_warnings:
        print(f" - {w}")
    print("Recruiter Flags:")
    for f in result_sus.recruiter_flags:
        print(f" - {f}")
    print(f"Adjusted Conf.  : {result_sus.behavioral_impact['integrity_adjusted_confidence']} (Down from {result_sus.behavioral_impact['baseline_behavioral_confidence']})")
    print(f"Recommendation  : {result_sus.behavioral_impact['recommendation']}")

    print("\n" + "=" * 65)
    print("DAY 49 INTEGRITY DETECTION DESIGN & IMPLEMENTATION COMPLETE")
    print("=" * 65)