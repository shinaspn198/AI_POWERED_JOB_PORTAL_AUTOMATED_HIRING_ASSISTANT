"""
Day 58 - Advanced Features: AI Coaching, Interview Analytics & Multimodal Perception

Implements next-generation hiring intelligence:
1. Candidate AI Coaching & Personalized Growth Plan Engine
2. Enterprise Interview Pipeline Analytics Dashboard Engine
3. Multimodal Video, Emotion & Real-time Cues Perception Simulator
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


# =========================================================
# 1. CANDIDATE AI COACHING & IMPROVEMENT ENGINE
# =========================================================

@dataclass
class CandidateCoachingPlan:
    candidate_id: str
    candidate_name: str
    role: str
    strengths_observed: List[str]
    critical_skill_gaps: List[str]
    resume_improvement_suggestions: List[str]
    interview_delivery_tips: List[str]
    recommended_learning_path: List[Dict[str, str]]
    executive_encouragement: str


class CandidateAICoachingEngine:
    """Generates constructive, actionable feedback and personalized career coaching for candidates."""

    LEARNING_RESOURCES = {
        "system_design": {"topic": "Distributed System Design", "resource": "Designing Data-Intensive Applications & System Design Primer"},
        "concurrency": {"topic": "Async Programming & Concurrency", "resource": "Python AsyncIO Deep Dive & Multithreading Patterns"},
        "algorithms": {"topic": "Data Structures & Algorithmic Optimization", "resource": "LeetCode Medium/Hard Patterns & Dynamic Programming"},
        "star_method": {"topic": "Behavioral Framing (STAR Method)", "resource": "Situation-Task-Action-Result Interview Framework Masterclass"},
        "communication": {"topic": "Technical Communication & Brevity", "resource": "Executive Speaking for Engineers & Architecture Presentations"},
    }

    def generate_coaching_plan(
        self,
        candidate_id: str,
        candidate_name: str,
        role: str,
        stage_scores: Dict[str, float],
        missing_skills: Optional[List[str]] = None,
        hr_contradiction: bool = False,
        stress_level: str = "Normal",
    ) -> CandidateCoachingPlan:
        """Constructs an encouraging, actionable candidate development plan."""
        ats = stage_scores.get("ats", 70.0)
        screening = stage_scores.get("screening", 75.0)
        hr = stage_scores.get("hr", 75.0)
        tech = stage_scores.get("technical", 70.0)
        machine = stage_scores.get("machine_test", 70.0)

        strengths = []
        gaps = []
        resume_tips = []
        interview_tips = []
        learning_path = []

        # Analyze strengths & gaps
        if machine >= 85:
            strengths.append(f"Exceptional hands-on coding execution and problem-solving fluency ({machine}%).")
        elif machine < 70:
            gaps.append(f"Hands-on coding speed and test-case coverage ({machine}% on Machine Test).")
            learning_path.append(self.LEARNING_RESOURCES["algorithms"])

        if tech >= 85:
            strengths.append(f"Deep theoretical knowledge and architecture clarity ({tech}%).")
        elif tech < 70:
            gaps.append(f"System architecture fundamentals and component trade-off articulation ({tech}%).")
            learning_path.append(self.LEARNING_RESOURCES["system_design"])

        if screening >= 80:
            strengths.append("Crisp and professional verbal communication during phone screening.")
        else:
            interview_tips.append("Structure initial background overviews to under 2 minutes, highlighting impact over chronology.")

        if hr_contradiction:
            interview_tips.append("Ensure specific metrics and project dates match consistently between resume and verbal answers.")
            learning_path.append(self.LEARNING_RESOURCES["star_method"])

        if stress_level.lower() in ("high", "stressed"):
            interview_tips.append("Practice taking a 2-second pause before answering complex architectural questions to maintain composure.")

        if missing_skills:
            for skill in missing_skills[:2]:
                resume_tips.append(f"Add tangible project bullets demonstrating practical usage of '{skill}'.")

        if not resume_tips:
            resume_tips.append("Quantify business outcomes (e.g. 'Reduced latency by 40%', 'Handled 5M daily requests').")

        if not gaps:
            gaps.append("Continue deepening specialized domain knowledge to reach Senior/Staff level.")

        encouragement = (
            f"You demonstrated strong fundamentals, particularly in {strengths[0] if strengths else 'problem solving'}. "
            f"Focusing on the targeted growth areas below will significantly accelerate your interview trajectory."
        )

        return CandidateCoachingPlan(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            role=role,
            strengths_observed=strengths,
            critical_skill_gaps=gaps,
            resume_improvement_suggestions=resume_tips,
            interview_delivery_tips=interview_tips,
            recommended_learning_path=learning_path,
            executive_encouragement=encouragement,
        )


# =========================================================
# 2. INTERVIEW ANALYTICS DASHBOARD ENGINE
# =========================================================

@dataclass
class PipelineFunnelMetrics:
    total_applicants: int
    ats_screened: int
    voice_screened: int
    hr_interviewed: int
    technical_machine_tested: int
    offers_extended: int
    funnel_conversion_rates: Dict[str, float]
    average_scores_by_stage: Dict[str, float]
    role_pass_rates: Dict[str, float]


class InterviewAnalyticsDashboardEngine:
    """Calculates high-level recruitment funnel metrics and pipeline health telemetry."""

    @staticmethod
    def compute_funnel_metrics(candidates_data: List[Dict[str, Any]]) -> PipelineFunnelMetrics:
        """Aggregates applicant cohort data into recruiter analytics."""
        total = len(candidates_data)
        if total == 0:
            return PipelineFunnelMetrics(
                total_applicants=0, ats_screened=0, voice_screened=0,
                hr_interviewed=0, technical_machine_tested=0, offers_extended=0,
                funnel_conversion_rates={}, average_scores_by_stage={}, role_pass_rates={}
            )

        ats_count = sum(1 for c in candidates_data if c.get("ats_score", 0) >= 60.0)
        screening_count = sum(1 for c in candidates_data if c.get("screening_score", 0) >= 65.0)
        hr_count = sum(1 for c in candidates_data if c.get("hr_score", 0) >= 65.0)
        tech_count = sum(1 for c in candidates_data if c.get("machine_test_score", 0) >= 65.0)
        offers = sum(1 for c in candidates_data if "HIRE" in str(c.get("recommendation", "")).upper() or c.get("status") in ("shortlisted", "hired"))

        conversions = {
            "applicant_to_screening": round((screening_count / total) * 100, 2),
            "screening_to_technical": round((tech_count / max(1, screening_count)) * 100, 2),
            "technical_to_offer": round((offers / max(1, tech_count)) * 100, 2),
            "end_to_end_conversion": round((offers / total) * 100, 2),
        }

        avg_scores = {
            "ats_avg": round(sum(c.get("ats_score", 0) for c in candidates_data) / total, 1),
            "screening_avg": round(sum(c.get("screening_score", 0) for c in candidates_data) / total, 1),
            "hr_avg": round(sum(c.get("hr_score", 0) for c in candidates_data) / total, 1),
            "technical_avg": round(sum(c.get("technical_score", 0) for c in candidates_data) / total, 1),
            "machine_test_avg": round(sum(c.get("machine_test_score", 0) for c in candidates_data) / total, 1),
        }

        # Role-based pass rates
        roles: Dict[str, List[bool]] = {}
        for c in candidates_data:
            r = c.get("role", "software_engineer")
            passed = "HIRE" in str(c.get("recommendation", "")).upper() or c.get("status") in ("shortlisted", "hired")
            roles.setdefault(r, []).append(passed)

        role_pass = {
            r: round((sum(bools) / len(bools)) * 100, 1) for r, bools in roles.items()
        }

        return PipelineFunnelMetrics(
            total_applicants=total,
            ats_screened=ats_count,
            voice_screened=screening_count,
            hr_interviewed=hr_count,
            technical_machine_tested=tech_count,
            offers_extended=offers,
            funnel_conversion_rates=conversions,
            average_scores_by_stage=avg_scores,
            role_pass_rates=role_pass,
        )


# =========================================================
# 3. MULTIMODAL PERCEPTION SIMULATOR
# =========================================================

@dataclass
class MultimodalEmotionProfile:
    gaze_stability_ratio: float        # 0.0 - 1.0 (looking at screen/interviewer)
    dominant_emotion: str              # Calm, Confident, Anxious, Engaged, Distracted
    emotion_confidence: float
    prosody_pitch_jitter_pct: float
    facial_micro_expression_valence: float  # -1.0 to +1.0


class MultimodalPerceptionSimulator:
    """Simulates next-gen audio-visual emotion and gaze telemetry."""

    @staticmethod
    def analyze_audio_visual_stream(
        duration_sec: float = 60.0,
        looking_away_events: int = 0,
        hesitation_pauses: int = 2,
        sentiment_polarity: float = 0.5,
    ) -> MultimodalEmotionProfile:
        gaze_ratio = max(0.0, min(1.0, 1.0 - (looking_away_events * 0.08)))

        if looking_away_events > 4:
            dominant = "Distracted"
            conf = 0.88
        elif hesitation_pauses > 5:
            dominant = "Anxious"
            conf = 0.82
        elif sentiment_polarity > 0.4:
            dominant = "Confident"
            conf = 0.90
        else:
            dominant = "Calm"
            conf = 0.85

        pitch_jitter = round(min(5.0, 1.0 + hesitation_pauses * 0.4), 2)
        valence = round(sentiment_polarity * 0.8, 2)

        return MultimodalEmotionProfile(
            gaze_stability_ratio=round(gaze_ratio, 2),
            dominant_emotion=dominant,
            emotion_confidence=conf,
            prosody_pitch_jitter_pct=pitch_jitter,
            facial_micro_expression_valence=valence,
        )
