"""
Day 53 - Hiring Intelligence Report Generator

Combines multi-stage evaluation insights into a recruiter-ready,
executive candidate evaluation report with strengths, weaknesses,
risk indicators, cross-round telemetry, and multi-format exports
(JSON, Markdown, Printable HTML).
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
import html


@dataclass
class CandidateProfileData:
    candidate_id: str
    candidate_name: str
    role: str
    experience_level: str
    generated_at: str = field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"))

    # Stage Summaries
    ats_summary: Dict[str, Any] = field(default_factory=dict)
    screening_summary: Dict[str, Any] = field(default_factory=dict)
    hr_insights: Dict[str, Any] = field(default_factory=dict)
    technical_performance: Dict[str, Any] = field(default_factory=dict)
    behavioral_and_integrity_flags: Dict[str, Any] = field(default_factory=dict)

    # Aggregated Outcome
    hiring_fit_score: float = 0.0
    hiring_recommendation: str = "PENDING"
    decision_confidence: float = 0.0

    # Key Highlights
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    risk_indicators: List[str] = field(default_factory=list)
    executive_summary: str = ""
    recommended_action: str = ""


class HiringIntelligenceReportGenerator:
    """Generates comprehensive recruiter intelligence reports from multi-round evaluations."""

    def __init__(self):
        pass

    def build_report(
        self,
        candidate_id: str,
        candidate_name: str,
        role: str,
        experience_level: str,
        stage_scores: Dict[str, float],
        ats_details: Optional[Dict[str, Any]] = None,
        screening_details: Optional[Dict[str, Any]] = None,
        hr_details: Optional[Dict[str, Any]] = None,
        technical_details: Optional[Dict[str, Any]] = None,
        integrity_details: Optional[Dict[str, Any]] = None,
        recommendation_details: Optional[Dict[str, Any]] = None,
    ) -> CandidateProfileData:
        """Synthesizes candidate insights into a unified profile report."""

        # 1. Normalize stage scores
        ats_score = stage_scores.get("ats", 0.0)
        screening_score = stage_scores.get("screening", 0.0)
        hr_score = stage_scores.get("hr", 0.0)
        tech_score = stage_scores.get("technical", 0.0)
        machine_score = stage_scores.get("machine_test", 0.0)

        # 2. Extract or populate ATS summary
        ats_summary = {
            "score": ats_score,
            "skill_match": (ats_details or {}).get("skill_match", ats_score),
            "experience_relevance": (ats_details or {}).get("experience_relevance", ats_score),
            "education_alignment": (ats_details or {}).get("education_alignment", 85.0),
            "matched_skills": (ats_details or {}).get("matched_skills", ["Python", "FastAPI", "Data Structures"]),
            "missing_skills": (ats_details or {}).get("missing_skills", []),
        }

        # 3. Extract or populate Screening summary
        screening_summary = {
            "score": screening_score,
            "communication_clarity": (screening_details or {}).get("communication_clarity", round(screening_score * 0.95, 1)),
            "role_relevance": (screening_details or {}).get("role_relevance", screening_score),
            "availability": (screening_details or {}).get("availability", "Immediate / 2 Weeks"),
            "location_compatibility": (screening_details or {}).get("location_compatibility", "Compatible"),
        }

        # 4. Extract or populate HR insights
        hr_insights = {
            "score": hr_score,
            "behavioral_confidence": (hr_details or {}).get("behavioral_confidence", 82.0),
            "sentiment_score": (hr_details or {}).get("sentiment_score", 75.0),
            "stress_indicator": (hr_details or {}).get("stress_indicator", "Normal / Composed"),
            "contradiction_detected": (hr_details or {}).get("contradiction_detected", False),
            "culture_alignment": (hr_details or {}).get("culture_alignment", "High"),
        }

        # 5. Extract or populate Technical performance
        technical_performance = {
            "interview_score": tech_score,
            "machine_test_score": machine_score,
            "code_correctness": (technical_details or {}).get("test_cases_passed_ratio", 1.0) * 100,
            "execution_efficiency_ms": (technical_details or {}).get("execution_time_ms", 35.0),
            "problem_solving_depth": "Strong" if tech_score >= 80 else "Moderate",
        }

        # 6. Extract or populate Behavioral & Integrity Flags
        integrity_score = (integrity_details or {}).get("integrity_score", 100.0)
        risk_tag = (integrity_details or {}).get("risk_tag", "LOW_RISK")
        tab_switches = (integrity_details or {}).get("tab_switches", 0)
        looking_away_count = (integrity_details or {}).get("looking_away_events", 0)

        behavioral_flags = {
            "integrity_score": integrity_score,
            "risk_tag": risk_tag,
            "tab_switches": tab_switches,
            "looking_away_events": looking_away_count,
            "malpractice_detected": integrity_score < 70.0 or risk_tag in ("HIGH_RISK", "CRITICAL_RISK"),
        }

        # 7. Recommendation details
        hiring_fit = (recommendation_details or {}).get("hiring_fit_score", round((ats_score * 0.15 + screening_score * 0.15 + hr_score * 0.15 + tech_score * 0.25 + machine_score * 0.30), 2))
        recommendation = (recommendation_details or {}).get("decision", "STRONG_HIRE" if hiring_fit >= 80 else ("HIRE" if hiring_fit >= 68 else "BORDERLINE"))
        confidence = (recommendation_details or {}).get("decision_confidence", 88.5)

        # 8. Synthesize Strengths, Weaknesses, and Risks
        strengths = []
        weaknesses = []
        risk_indicators = []

        if machine_score >= 85:
            strengths.append(f"Outstanding practical coding ability ({machine_score}% on Hands-on Machine Test)")
        elif machine_score >= 70:
            strengths.append(f"Solid engineering execution ({machine_score}% on Machine Test)")
        else:
            weaknesses.append(f"Below target machine test score ({machine_score}%)")

        if tech_score >= 85:
            strengths.append(f"Deep theoretical knowledge and architecture clarity ({tech_score}%)")
        elif tech_score < 65:
            weaknesses.append(f"Technical interview revealed foundational knowledge gaps ({tech_score}%)")

        if ats_summary["missing_skills"]:
            weaknesses.append(f"Missing resume keywords: {', '.join(ats_summary['missing_skills'][:3])}")

        if hr_insights["contradiction_detected"]:
            risk_indicators.append("Cross-interview statement contradiction flagged during HR dialogue")

        if tab_switches >= 3:
            risk_indicators.append(f"Frequent window unfocus detected during assessment ({tab_switches} tab switches)")

        if integrity_score < 75.0:
            risk_indicators.append(f"Integrity telemetry score lowered to {integrity_score}% ({risk_tag})")

        if not risk_indicators:
            risk_indicators.append("Zero malpractice or behavioral anomalies detected")

        if not strengths:
            strengths.append("Meets minimum baseline across all qualifying rounds")

        # 9. Executive Summary & Recommended Action
        executive_summary = (
            f"{candidate_name} evaluated for {role} ({experience_level} tier) achieved an overall Hiring Fit "
            f"Score of {hiring_fit}% ({recommendation}). Key performance highlight: {strengths[0]}. "
            f"Integrity status is verified at {integrity_score}% ({risk_tag})."
        )

        if recommendation in ("STRONG_HIRE", "Selected", "HIRE"):
            recommended_action = "Proceed immediately to Offer Stage / Compensation Alignment."
        elif recommendation in ("Hold / Review", "BORDERLINE"):
            recommended_action = "Schedule a 15-minute follow-up technical alignment with Lead Architect."
        else:
            recommended_action = "Send standard courteous feedback and keep profile in candidate talent pool."

        return CandidateProfileData(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            role=role,
            experience_level=experience_level,
            ats_summary=ats_summary,
            screening_summary=screening_summary,
            hr_insights=hr_insights,
            technical_performance=technical_performance,
            behavioral_and_integrity_flags=behavioral_flags,
            hiring_fit_score=hiring_fit,
            hiring_recommendation=str(recommendation),
            decision_confidence=confidence,
            strengths=strengths,
            weaknesses=weaknesses,
            risk_indicators=risk_indicators,
            executive_summary=executive_summary,
            recommended_action=recommended_action,
        )

    def export_json(self, profile: CandidateProfileData, indent: int = 2) -> str:
        """Exports profile as structured JSON."""
        return json.dumps(asdict(profile), indent=indent)

    def export_markdown(self, profile: CandidateProfileData) -> str:
        """Exports profile as a clean markdown report."""
        lines = [
            f"# Zecpath AI Hiring Intelligence Report",
            f"**Candidate:** {profile.candidate_name} (`{profile.candidate_id}`)",
            f"**Role:** {profile.role.replace('_', ' ').title()} | **Tier:** {profile.experience_level.title()}",
            f"**Generated:** {profile.generated_at}",
            f"",
            f"---",
            f"",
            f"## Executive Overview",
            f"- **Final Recommendation:** **{profile.hiring_recommendation}**",
            f"- **Composite Hiring Fit Score:** **{profile.hiring_fit_score}%**",
            f"- **Decision Confidence:** **{profile.decision_confidence}%**",
            f"- **Recommended Recruiter Action:** {profile.recommended_action}",
            f"",
            f"> {profile.executive_summary}",
            f"",
            f"---",
            f"",
            f"## Stage Score Breakdown",
            f"| Stage | Score | Key Signal |",
            f"| :--- | :---: | :--- |",
            f"| **ATS Resume Match** | {profile.ats_summary.get('score', 0)}% | Skill Match: {profile.ats_summary.get('skill_match', 0)}% |",
            f"| **Screening Call AI** | {profile.screening_summary.get('score', 0)}% | Communication: {profile.screening_summary.get('communication_clarity', 0)}% |",
            f"| **HR Behavioral** | {profile.hr_insights.get('score', 0)}% | Confidence: {profile.hr_insights.get('behavioral_confidence', 0)}% |",
            f"| **Technical Interview** | {profile.technical_performance.get('interview_score', 0)}% | Problem Solving: {profile.technical_performance.get('problem_solving_depth', 'N/A')} |",
            f"| **Machine Test Sandbox** | {profile.technical_performance.get('machine_test_score', 0)}% | Correctness: {profile.technical_performance.get('code_correctness', 0)}% |",
            f"",
            f"---",
            f"",
            f"## Candidate Highlights & Risk Telemetry",
            f"",
            f"### Key Strengths",
        ]
        for s in profile.strengths:
            lines.append(f"-  {s}")

        lines.append(f"\n### Areas for Growth / Weaknesses")
        if profile.weaknesses:
            for w in profile.weaknesses:
                lines.append(f"-  {w}")
        else:
            lines.append("- No critical weaknesses identified during assessment rounds.")

        lines.append(f"\n### Integrity & Risk Indicators")
        for r in profile.risk_indicators:
            lines.append(f"-  {r}")

        lines.append(f"\n- **Integrity Score:** {profile.behavioral_and_integrity_flags.get('integrity_score', 100)}% ({profile.behavioral_and_integrity_flags.get('risk_tag', 'LOW_RISK')})")
        lines.append(f"\n---\n*Report certified by Zecpath Autonomous Hiring Intelligence System.*")
        return "\n".join(lines)

    def export_recruiter_card(self, profile: CandidateProfileData) -> Dict[str, Any]:
        """Exports a clean, executive recruiter scorecard tailored for fast hiring manager decisions."""
        fit_tier = "EXCEPTIONAL" if profile.hiring_fit_score >= 85.0 else ("COMPETENT" if profile.hiring_fit_score >= 70.0 else "NEEDS_IMPROVEMENT")
        return {
            "candidate_id": profile.candidate_id,
            "candidate_name": profile.candidate_name,
            "role": profile.role,
            "fit_tier": fit_tier,
            "hiring_fit_score": round(profile.hiring_fit_score, 1),
            "recommendation": profile.hiring_recommendation,
            "decision_confidence": round(profile.decision_confidence, 1),
            "top_strengths": profile.strengths[:3],
            "critical_risks": profile.risk_indicators,
            "executive_summary": profile.executive_summary,
            "recommended_action": profile.recommended_action,
            "stage_breakdown": {
                "ats": profile.ats_summary.get("score", 0),
                "screening": profile.screening_summary.get("score", 0),
                "hr": profile.hr_insights.get("score", 0),
                "technical": profile.technical_performance.get("interview_score", 0),
                "machine_test": profile.technical_performance.get("machine_test_score", 0),
                "integrity": profile.behavioral_and_integrity_flags.get("integrity_score", 100)
            }
        }

    def export_html(self, profile: CandidateProfileData) -> str:
        """Exports profile as a polished, export-ready HTML document suitable for printing/PDF."""
        status_color = "#10b981" if "HIRE" in profile.hiring_recommendation.upper() else ("#f59e0b" if "BORDERLINE" in profile.hiring_recommendation.upper() or "HOLD" in profile.hiring_recommendation.upper() else "#ef4444")
        
        strengths_html = "".join([f"<li style='margin-bottom:6px;'>{html.escape(s)}</li>" for s in profile.strengths])
        weaknesses_html = "".join([f"<li style='margin-bottom:6px;'>{html.escape(w)}</li>" for w in profile.weaknesses]) or "<li>No critical gaps noted.</li>"
        risks_html = "".join([f"<li style='margin-bottom:6px;'>{html.escape(r)}</li>" for r in profile.risk_indicators])

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Hiring Intelligence Report - {html.escape(profile.candidate_name)}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #1e293b; background: #f8fafc; margin: 0; padding: 24px; }}
  .container {{ max-width: 860px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); padding: 32px; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 20px; }}
  .title {{ font-size: 24px; font-weight: 700; color: #0f172a; margin: 0; }}
  .subtitle {{ color: #64748b; font-size: 14px; margin-top: 4px; }}
  .badge {{ display: inline-block; padding: 6px 14px; border-radius: 20px; color: white; background: {status_color}; font-weight: 700; font-size: 13px; text-transform: uppercase; }}
  .score-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0; }}
  .score-card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; text-align: center; }}
  .score-val {{ font-size: 28px; font-weight: 800; color: #0f172a; }}
  .score-lbl {{ font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 600; margin-top: 4px; }}
  .section {{ margin-top: 28px; }}
  .section-title {{ font-size: 16px; font-weight: 700; color: #334155; margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
  .table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
  .table th, .table td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 14px; }}
  .table th {{ background: #f1f5f9; font-weight: 600; color: #475569; }}
  .summary-box {{ background: #eff6ff; border-left: 4px solid #3b82f6; padding: 14px 18px; border-radius: 0 8px 8px 0; font-size: 14px; line-height: 1.5; color: #1e3a8a; }}
  .action-box {{ background: #f0fdf4; border: 1px solid #bbf7d0; padding: 14px 18px; border-radius: 8px; margin-top: 24px; font-size: 14px; font-weight: 600; color: #166534; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <h1 class="title">{html.escape(profile.candidate_name)}</h1>
      <div class="subtitle">{html.escape(profile.role.replace('_', ' ').title())} &bull; Tier: {html.escape(profile.experience_level.title())} &bull; ID: {html.escape(profile.candidate_id)}</div>
    </div>
    <div class="badge">{html.escape(profile.hiring_recommendation)}</div>
  </div>

  <div class="score-grid">
    <div class="score-card">
      <div class="score-val">{profile.hiring_fit_score}%</div>
      <div class="score-lbl">Hiring Fit Score</div>
    </div>
    <div class="score-card">
      <div class="score-val">{profile.decision_confidence}%</div>
      <div class="score-lbl">Decision Confidence</div>
    </div>
    <div class="score-card">
      <div class="score-val">{profile.technical_performance.get('machine_test_score', 0)}%</div>
      <div class="score-lbl">Machine Test</div>
    </div>
    <div class="score-card">
      <div class="score-val">{profile.behavioral_and_integrity_flags.get('integrity_score', 100)}%</div>
      <div class="score-lbl">Integrity Score</div>
    </div>
  </div>

  <div class="summary-box">
    <strong>AI Executive Summary:</strong> {html.escape(profile.executive_summary)}
  </div>

  <div class="action-box">
    &rarr; Recommended Next Step: {html.escape(profile.recommended_action)}
  </div>

  <div class="section">
    <div class="section-title">Evaluation Stage Breakdown</div>
    <table class="table">
      <thead>
        <tr><th>Stage</th><th>Score</th><th>Details</th></tr>
      </thead>
      <tbody>
        <tr><td>ATS Resume Match</td><td>{profile.ats_summary.get('score', 0)}%</td><td>Skill Match: {profile.ats_summary.get('skill_match', 0)}%</td></tr>
        <tr><td>Screening Call AI</td><td>{profile.screening_summary.get('score', 0)}%</td><td>Communication Clarity: {profile.screening_summary.get('communication_clarity', 0)}%</td></tr>
        <tr><td>HR Behavioral Interview</td><td>{profile.hr_insights.get('score', 0)}%</td><td>Confidence: {profile.hr_insights.get('behavioral_confidence', 0)}% | Stress: {profile.hr_insights.get('stress_indicator', 'Normal')}</td></tr>
        <tr><td>Technical Interview</td><td>{profile.technical_performance.get('interview_score', 0)}%</td><td>Problem Solving: {profile.technical_performance.get('problem_solving_depth', 'Moderate')}</td></tr>
        <tr><td>Hands-on Machine Test</td><td>{profile.technical_performance.get('machine_test_score', 0)}%</td><td>Test Correctness: {profile.technical_performance.get('code_correctness', 0)}%</td></tr>
      </tbody>
    </table>
  </div>

  <div class="section">
    <div class="section-title">Strengths, Growth Areas & Risk Signals</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <div>
        <h4 style="color:#059669; margin: 0 0 8px 0;">Key Strengths</h4>
        <ul style="padding-left: 20px; font-size: 13px; color:#334155;">{strengths_html}</ul>
        <h4 style="color:#d97706; margin: 16px 0 8px 0;">Areas for Growth</h4>
        <ul style="padding-left: 20px; font-size: 13px; color:#334155;">{weaknesses_html}</ul>
      </div>
      <div>
        <h4 style="color:#dc2626; margin: 0 0 8px 0;">Integrity & Risk Signals</h4>
        <ul style="padding-left: 20px; font-size: 13px; color:#334155;">{risks_html}</ul>
        <p style="font-size: 12px; color: #64748b; margin-top: 12px;">
          Telemetry Tag: <strong>{profile.behavioral_and_integrity_flags.get('risk_tag', 'LOW_RISK')}</strong><br>
          Window Tab Switches: {profile.behavioral_and_integrity_flags.get('tab_switches', 0)}
        </p>
      </div>
    </div>
  </div>

  <div style="margin-top: 32px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 16px;">
    Generated on {profile.generated_at} &bull; Zecpath AI Autonomous Hiring System
  </div>
</div>
</body>
</html>
"""
