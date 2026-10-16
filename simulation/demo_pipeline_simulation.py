"""
Day 63 — Realistic Demo Pipeline Simulation Engine
Loads the Day 63 demo dataset and executes end-to-end recruitment evaluation:
Resume -> ATS -> Screening -> HR -> Technical -> Integrity -> Final Recommendation & Decision Audit.
"""

import json
import os
import time
from typing import Dict, List, Any, Tuple
from performance.ai_monitoring import ai_monitor
from unified_scoring.recommendation_ai import RecommendationAIEngine


class DemoPipelineSimulation:
    def __init__(
        self,
        candidates_path: str = "data/demo_dataset/demo_candidates.json",
        jobs_path: str = "data/demo_dataset/job_descriptions.json"
    ):
        self.candidates_path = candidates_path
        self.jobs_path = jobs_path
        self.recommendation_engine = RecommendationAIEngine()

    def load_data(self) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, Any]]]:
        with open(self.candidates_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)
        with open(self.jobs_path, "r", encoding="utf-8") as f:
            jobs_list = json.load(f)
        jobs_map = {j["job_id"]: j for j in jobs_list}
        return candidates, jobs_map

    def evaluate_ats(self, candidate_resume: Dict[str, Any], job: Dict[str, Any]) -> float:
        """Deterministic ATS scoring based on skill overlap, experience, and education."""
        req_skills = set(s.lower() for s in job.get("required_skills", []))
        cand_skills = set(s.lower() for s in candidate_resume.get("skills", []))
        
        # 1. Skill overlap (40%)
        overlap = len(req_skills.intersection(cand_skills))
        skill_score = (overlap / len(req_skills) * 100.0) if req_skills else 50.0

        # 2. Experience alignment (35%)
        req_exp = job.get("min_experience_years", 1)
        cand_exp = candidate_resume.get("years_of_experience", 0)
        exp_score = min(100.0, (cand_exp / req_exp) * 85.0) if cand_exp >= req_exp else (cand_exp / req_exp * 50.0)

        # 3. Education / baseline (25%)
        edu_score = 90.0 if "computer science" in str(candidate_resume.get("education", [])).lower() else 65.0

        total_ats = 0.40 * skill_score + 0.35 * exp_score + 0.25 * edu_score
        return round(total_ats, 2)

    def run_simulation(self) -> List[Dict[str, Any]]:
        """Run all candidates through the multi-stage pipeline."""
        candidates, jobs_map = self.load_data()
        results = []

        for cand in candidates:
            cand_id = cand["candidate_id"]
            name = cand["name"]
            job_id = cand["target_job_id"]
            job = jobs_map.get(job_id, {})

            # 1. ATS Scoring
            ats_score = self.evaluate_ats(cand["resume"], job)
            
            # 2. Screening
            screening_score = cand["screening"]["communication_score"]

            # 3. HR Behavioral
            hr_score = (cand["hr_interview"]["behavioral_score"] + cand["hr_interview"]["culture_fit_score"]) / 2.0

            # 4. Technical / Coding
            tech_score = (cand["technical_interview"]["correctness_score"] + cand["technical_interview"]["code_quality_score"]) / 2.0

            # 5. Integrity & Proctoring
            integrity_score = cand["integrity"]["integrity_score"]
            risk_level = cand["integrity"]["risk_level"]
            tab_switches = cand["integrity"]["tab_switches"]
            has_contradiction = risk_level == "HIGH_RISK" or tab_switches >= 5

            # 6. Recommendation AI Decision
            stage_scores = {
                "ats": ats_score,
                "screening": screening_score,
                "hr": hr_score,
                "technical": tech_score,
                "machine_test": tech_score
            }

            composite_fit = (
                0.25 * ats_score +
                0.20 * screening_score +
                0.25 * tech_score +
                0.20 * hr_score +
                0.10 * integrity_score
            )

            rec_output = self.recommendation_engine.evaluate_decision(
                candidate_id=cand_id,
                candidate_name=name,
                role=job.get("title", "Software Engineer"),
                hiring_fit_score=composite_fit,
                scores=stage_scores,
                integrity_score=integrity_score,
                risk_tag=risk_level,
                contradiction_detected=has_contradiction
            )

            # Map category to standard verdict string
            verdict_str = rec_output.decision.value  # "Selected", "Hold / Review", "Rejected"
            if verdict_str == "Selected":
                final_verdict = "HIRE"
            elif verdict_str == "Hold / Review":
                final_verdict = "SHORTLIST"
            else:
                final_verdict = "REJECT"

            # 7. Record Decision Audit in Observability Ledger
            audit_entry = ai_monitor.record_decision_audit(
                candidate_id=cand_id,
                job_id=job_id,
                stage="FINAL_DECISION",
                scores=stage_scores,
                verdict=final_verdict,
                model_version="1.0.0",
                operator="DEMO_PIPELINE_ENGINE"
            )

            record = {
                "candidate_id": cand_id,
                "name": name,
                "profile_tier": cand["profile_tier"],
                "target_job": job.get("title"),
                "ats_score": ats_score,
                "screening_score": screening_score,
                "hr_score": hr_score,
                "technical_score": tech_score,
                "integrity_score": integrity_score,
                "hiring_fit_score": rec_output.hiring_fit_score,
                "ai_decision": final_verdict,
                "decision_category": verdict_str,
                "expected_verdict": cand["expected_verdict"],
                "integrity_hash": audit_entry["integrity_hash"],
                "key_strengths": rec_output.key_strengths,
                "risk_factors": rec_output.risk_factors
            }
            results.append(record)

        return results


# Type alias helper
from typing import Tuple

if __name__ == "__main__":
    sim = DemoPipelineSimulation()
    results = sim.run_simulation()
    print("\n=== ZECPATH AI DEMO RECRUITMENT PIPELINE SIMULATION RESULTS ===")
    for r in results:
        print(f"[{r['candidate_id']}] {r['name']} ({r['profile_tier']}): Fit Score={r['hiring_fit_score']} | AI Verdict={r['ai_decision']} | Expected={r['expected_verdict']}")
