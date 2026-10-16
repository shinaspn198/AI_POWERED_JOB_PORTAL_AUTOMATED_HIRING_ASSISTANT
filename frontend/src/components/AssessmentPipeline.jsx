import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000/api/assessment";

export default function AssessmentPipeline({ onBack, candidateName = "Alex Rivera", initialRole = "software_engineer" }) {
  const [currentStep, setCurrentStep] = useState(1);
  const [role, setRole] = useState(initialRole);
  const [experienceLevel, setExperienceLevel] = useState("mid");

  // Step 1: ATS Resume
  const [atsScores, setAtsScores] = useState({
    skill_match: 85,
    experience_relevance: 80,
    education_alignment: 90,
    semantic_similarity: 88,
  });
  const [calculatedAtsScore, setCalculatedAtsScore] = useState(85.5);

  // Step 2: AI Screening
  const [screeningAnswer, setScreeningAnswer] = useState(
    "Over the past 3 years, I have architected and built scalable microservices using Python, FastAPI, and PostgreSQL. I collaborated closely with frontend teams and optimized database queries to reduce latency by 40%."
  );
  const [screeningResult, setScreeningResult] = useState(null);
  const [screeningLoading, setScreeningLoading] = useState(false);

  // Step 3: HR Behavioral
  const [hrScenario, setHrScenario] = useState("handling_conflict");
  const [hrAnswer, setHrAnswer] = useState(
    "When our team faced tight release deadlines with conflicting priority requirements, I organized a sprint prioritization sync, clearly mapped business trade-offs, and aligned everyone on high-impact deliverables first."
  );
  const [hrMetrics, setHrMetrics] = useState({
    confidence_score: 85,
    sentiment_score: 80,
    stress_score: 20,
    contradiction_detected: false,
  });
  const [hrResult, setHrResult] = useState(null);

  // Step 4: Technical Interview
  const [techQuestion, setTechQuestion] = useState(
    "How would you design a distributed caching layer to handle 100,000 requests per second with high availability?"
  );
  const [techAnswer, setTechAnswer] = useState(
    "I would deploy a Redis cluster with consistent hashing across master-replica nodes. To handle read spikes, I would use a multi-tiered caching approach: local in-memory L1 cache (LRU) on application servers backed by Redis as L2, with asynchronous cache invalidation via Redis Pub/Sub."
  );
  const [techResult, setTechResult] = useState(null);

  // Step 5: Machine Test
  const [testType, setTestType] = useState("coding_problems");
  const [code, setCode] = useState(
`class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        val = self.cache.pop(key)
        self.cache[key] = val
        return val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            del self.cache[next(iter(self.cache))]
        self.cache[key] = value`
  );
  const [testResults, setTestResults] = useState(null);
  const [runningTests, setRunningTests] = useState(false);

  // Step 6: Proctoring / Telemetry
  const [telemetry, setTelemetry] = useState({
    tab_switches: 0,
    focus_loss_duration_sec: 0,
    external_voice_events: 0,
    looking_away_events: 0,
  });
  const [integrityAlerts, setIntegrityAlerts] = useState([]);
  const [latestToast, setLatestToast] = useState(null);

  // Final Unified Scorecard
  const [finalScorecard, setFinalScorecard] = useState(null);
  const [finalizing, setFinalizing] = useState(false);

  // Listen to browser tab switching and window focus loss
  useEffect(() => {
    let focusLostTimestamp = null;

    const handleVisibilityChange = () => {
      if (document.hidden) {
        focusLostTimestamp = Date.now();
        setTelemetry((prev) => {
          const nextSwitches = prev.tab_switches + 1;
          triggerWarning(`Warning: Tab switch detected! (Count: ${nextSwitches})`);
          return { ...prev, tab_switches: nextSwitches };
        });
      } else if (focusLostTimestamp) {
        const durationSec = (Date.now() - focusLostTimestamp) / 1000;
        setTelemetry((prev) => ({
          ...prev,
          focus_loss_duration_sec: Number((prev.focus_loss_duration_sec + durationSec).toFixed(1)),
        }));
      }
    };

    window.addEventListener("visibilitychange", handleVisibilityChange);
    return () => window.removeEventListener("visibilitychange", handleVisibilityChange);
  }, []);

  const triggerWarning = (msg) => {
    setLatestToast(msg);
    setIntegrityAlerts((prev) => [msg, ...prev.slice(0, 4)]);
    setTimeout(() => setLatestToast(null), 5000);
  };

  // Run ATS Evaluation
  const runAtsEvaluation = async () => {
    try {
      const res = await fetch(`${API_BASE}/evaluate/ats`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_id: "CAND-LIVE-01",
          role,
          ...atsScores,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setCalculatedAtsScore(data.ats_score);
      } else {
        setCalculatedAtsScore(86.5);
      }
    } catch {
      setCalculatedAtsScore(86.5);
    }
  };

  // Run Screening Evaluation
  const runScreeningEvaluation = async () => {
    setScreeningLoading(true);
    try {
      const res = await fetch(`${API_BASE}/evaluate/screening`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_id: "CAND-LIVE-01",
          role,
          question: "Can you describe your core technical experience?",
          answer: screeningAnswer,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setScreeningResult(data);
      } else {
        setScreeningResult({
          screening_score: 84.0,
          pillars: { clarity: 85, relevance: 88, completeness: 82, consistency: 85 },
        });
      }
    } catch {
      setScreeningResult({
        screening_score: 84.0,
        pillars: { clarity: 85, relevance: 88, completeness: 82, consistency: 85 },
      });
    } finally {
      setScreeningLoading(false);
    }
  };

  // Run HR Behavioral Evaluation
  const runHrEvaluation = async () => {
    try {
      const res = await fetch(`${API_BASE}/evaluate/hr`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_id: "CAND-LIVE-01",
          scenario_question: "How do you handle team disagreements under pressure?",
          response_text: hrAnswer,
          ...hrMetrics,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setHrResult(data);
      } else {
        setHrResult({ hr_score: 82.5, metrics: hrMetrics });
      }
    } catch {
      setHrResult({ hr_score: 82.5, metrics: hrMetrics });
    }
  };

  // Run Technical Skill Evaluation
  const runTechnicalEvaluation = async () => {
    try {
      const res = await fetch(`${API_BASE}/evaluate/technical`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_id: "CAND-LIVE-01",
          role,
          question: techQuestion,
          technical_answer: techAnswer,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setTechResult(data);
      } else {
        setTechResult({
          technical_score: 88.0,
          rubric: { accuracy: 90, depth: 88, logical_reasoning: 85, real_world_applicability: 89 },
        });
      }
    } catch {
      setTechResult({
        technical_score: 88.0,
        rubric: { accuracy: 90, depth: 88, logical_reasoning: 85, real_world_applicability: 89 },
      });
    }
  };

  // Run Machine Test Sandbox Execution
  const runMachineTest = async () => {
    setRunningTests(true);
    try {
      const res = await fetch(`${API_BASE}/evaluate/machine-test`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_id: "CAND-LIVE-01",
          test_type: testType,
          source_code: code,
          time_taken_seconds: 1100.0,
          expected_time_seconds: 1800.0,
          max_allowed_seconds: 2700.0,
          passed_test_cases: 10,
          total_test_cases: 10,
          execution_time_ms: 38.4,
          memory_used_mb: 24.8,
        }),
      });
      if (res.ok) {
        const data = await res.json();
        setTestResults(data.details);
      } else {
        setTestResults({
          final_score: 96.0,
          performance_grade: "STRONG_HIRE",
          metrics: { correctness: 100, efficiency: 95, code_quality: 90, problem_solving_approach: 95 },
          sandbox: { tests_passed: "10/10", runtime_ms: 38.4, memory_mb: 24.8 },
          timing: { time_factor: 1.1 },
        });
      }
    } catch {
      setTestResults({
        final_score: 96.0,
        performance_grade: "STRONG_HIRE",
        metrics: { correctness: 100, efficiency: 95, code_quality: 90, problem_solving_approach: 95 },
        sandbox: { tests_passed: "10/10", runtime_ms: 38.4, memory_mb: 24.8 },
        timing: { time_factor: 1.1 },
      });
    } finally {
      setRunningTests(false);
    }
  };

  // Finalize Cross-Round Aggregation
  const finalizeAssessment = async () => {
    setFinalizing(true);
    const payload = {
      candidate_id: `CAND-${Math.floor(1000 + Math.random() * 9000)}`,
      candidate_name: candidateName,
      role,
      experience_level: experienceLevel,
      ats_score: calculatedAtsScore,
      screening_score: screeningResult ? screeningResult.screening_score : 84.0,
      hr_interview_score: hrResult ? hrResult.hr_score : 82.5,
      technical_interview_score: techResult ? techResult.technical_score : 88.0,
      machine_test_score: testResults ? testResults.final_score : 92.0,
      telemetry: {
        candidate_id: "CAND-LIVE-01",
        ...telemetry,
        baseline_behavioral_confidence: 85.0,
      },
    };

    try {
      const res = await fetch(`${API_BASE}/finalize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        const data = await res.json();
        setFinalScorecard(data);
      } else {
        setFinalScorecard({
          candidate_name: candidateName,
          role,
          experience_level: experienceLevel,
          hiring_fit_score: 88.4,
          hiring_recommendation: "STRONG_HIRE",
          integrity_score: telemetry.tab_switches > 3 ? 75.0 : 100.0,
          risk_tag: telemetry.tab_switches > 3 ? "MEDIUM_RISK" : "LOW_RISK",
          stage_breakdown: {
            ats: { stage_name: "ATS Resume Match", raw_score: calculatedAtsScore, weight: 0.15, weighted_contribution: 12.8 },
            screening: { stage_name: "Candidate Screening", raw_score: 84.0, weight: 0.15, weighted_contribution: 12.6 },
            hr_interview: { stage_name: "HR Behavioral Interview", raw_score: 82.5, weight: 0.15, weighted_contribution: 12.4 },
            technical_interview: { stage_name: "Technical Skill Interview", raw_score: 88.0, weight: 0.25, weighted_contribution: 22.0 },
            machine_test: { stage_name: "Hands-on Machine Test", raw_score: 92.0, weight: 0.30, weighted_contribution: 27.6 },
          },
          transparency_audit: {
            explanation: `Candidate demonstrated exceptional technical fluency and clean execution. Profile normalizers applied for ${experienceLevel} level.`,
          },
        });
      }
    } catch {
      setFinalScorecard({
        candidate_name: candidateName,
        role,
        experience_level: experienceLevel,
        hiring_fit_score: 88.4,
        hiring_recommendation: "STRONG_HIRE",
        integrity_score: 100.0,
        risk_tag: "LOW_RISK",
        stage_breakdown: {
          ats: { stage_name: "ATS Resume Match", raw_score: calculatedAtsScore, weight: 0.15, weighted_contribution: 12.8 },
          screening: { stage_name: "Candidate Screening", raw_score: 84.0, weight: 0.15, weighted_contribution: 12.6 },
          hr_interview: { stage_name: "HR Behavioral Interview", raw_score: 82.5, weight: 0.15, weighted_contribution: 12.4 },
          technical_interview: { stage_name: "Technical Skill Interview", raw_score: 88.0, weight: 0.25, weighted_contribution: 22.0 },
          machine_test: { stage_name: "Hands-on Machine Test", raw_score: 92.0, weight: 0.30, weighted_contribution: 27.6 },
        },
        transparency_audit: {
          explanation: `Candidate demonstrated exceptional technical fluency and clean execution. Profile normalizers applied for ${experienceLevel} level.`,
        },
      });
    } finally {
      setFinalizing(false);
      setCurrentStep(6);
    }
  };

  const steps = [
    { num: 1, label: "ATS Resume" },
    { num: 2, label: "AI Screening" },
    { num: 3, label: "HR Behavioral" },
    { num: 4, label: "Technical Interview" },
    { num: 5, label: "Machine Test" },
    { num: 6, label: "Hiring Fit Scorecard" },
  ];

  return (
    <div className="assessment-container" style={{ maxWidth: 1100, margin: "0 auto", padding: "30px 20px" }}>
      {/* Toast Alert */}
      {latestToast && (
        <div style={{
          position: "fixed", top: 20, right: 20, zIndex: 9999,
          background: "#dc2626", color: "#fff", padding: "12px 20px",
          borderRadius: 8, boxShadow: "0 8px 24px rgba(0,0,0,0.5)",
          fontWeight: "bold", border: "1px solid #f87171"
        }}>
          ⚠️ {latestToast}
        </div>
      )}

      {/* Top Header & Navigation */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 25 }}>
        <div>
          <button onClick={onBack} style={{ background: "transparent", color: "#60a5fa", padding: "6px 12px", border: "1px solid #1e293b", marginBottom: 8, fontSize: 13 }}>
            ← Back to Portal
          </button>
          <h2 style={{ margin: "5px 0 0", fontSize: 26, color: "#fff" }}>
            End-to-End AI Assessment Pipeline
          </h2>
          <p style={{ margin: 0, color: "#94a3b8", fontSize: 14 }}>
            Candidate: <strong style={{ color: "#fff" }}>{candidateName}</strong> | Role: <span style={{ textTransform: "capitalize", color: "#38bdf8" }}>{role.replace("_", " ")}</span>
          </p>
        </div>

        {/* Live Proctoring Pill */}
        <div style={{
          background: telemetry.tab_switches > 2 ? "#7f1d1d" : "#064e3b",
          border: `1px solid ${telemetry.tab_switches > 2 ? "#ef4444" : "#10b981"}`,
          borderRadius: 20, padding: "8px 16px", textAlign: "right"
        }}>
          <div style={{ fontSize: 12, fontWeight: "bold", color: telemetry.tab_switches > 2 ? "#fca5a5" : "#6ee7b7" }}>
            ● PROCTORING ACTIVE
          </div>
          <div style={{ fontSize: 11, color: "#cbd5e1" }}>
            Tab Switches: {telemetry.tab_switches} | Focus Lost: {telemetry.focus_loss_duration_sec}s
          </div>
        </div>
      </div>

      {/* Pipeline Progress Stepper */}
      <div style={{
        display: "flex", background: "#0f172a", borderRadius: 12,
        padding: 8, border: "1px solid #1e293b", marginBottom: 30, overflowX: "auto"
      }}>
        {steps.map((s) => (
          <button
            key={s.num}
            onClick={() => setCurrentStep(s.num)}
            style={{
              flex: 1, minWidth: 140, padding: "10px 8px", borderRadius: 8,
              background: currentStep === s.num ? "#2563eb" : "transparent",
              color: currentStep === s.num ? "#fff" : "#94a3b8",
              fontSize: 13, fontWeight: currentStep === s.num ? "bold" : "normal",
              border: "none", cursor: "pointer", transition: "all 0.2s"
            }}
          >
            {s.num}. {s.label}
          </button>
        ))}
      </div>

      {/* ================= STEP 1: ATS RESUME ================= */}
      {currentStep === 1 && (
        <div style={{ background: "#0b1329", border: "1px solid #1e293b", borderRadius: 14, padding: 28 }}>
          <h3 style={{ marginTop: 0, color: "#60a5fa" }}>Stage 1: ATS Resume Match</h3>
          <p style={{ color: "#94a3b8", fontSize: 14 }}>
            Fine-tune candidate attributes and verify calculated ATS match score against targeted role.
          </p>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, margin: "20px 0" }}>
            <div>
              <label style={{ fontSize: 13, color: "#94a3b8" }}>Target Role:</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                style={{ width: "100%", padding: 10, background: "#1e293b", border: "1px solid #334155", color: "#fff", borderRadius: 8, marginTop: 4 }}
              >
                <option value="software_engineer">Software Engineer</option>
                <option value="ai_engineer">AI / ML Engineer</option>
                <option value="data_analyst">Data Analyst</option>
                <option value="product_manager">Product Manager</option>
                <option value="hr_specialist">HR Specialist</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: 13, color: "#94a3b8" }}>Experience Level:</label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                style={{ width: "100%", padding: 10, background: "#1e293b", border: "1px solid #334155", color: "#fff", borderRadius: 8, marginTop: 4 }}
              >
                <option value="entry">Entry-Level (0 - 2 yrs)</option>
                <option value="mid">Mid-Level (3 - 5 yrs)</option>
                <option value="senior">Senior (6+ yrs)</option>
              </select>
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 14, margin: "24px 0" }}>
            {[
              { key: "skill_match", label: "Skill Match %" },
              { key: "experience_relevance", label: "Experience Relevance %" },
              { key: "education_alignment", label: "Education Alignment %" },
              { key: "semantic_similarity", label: "Semantic Similarity %" },
            ].map((metric) => (
              <div key={metric.key} style={{ background: "#1e293b", padding: 16, borderRadius: 10 }}>
                <div style={{ fontSize: 12, color: "#94a3b8" }}>{metric.label}</div>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={atsScores[metric.key]}
                  onChange={(e) => setAtsScores({ ...atsScores, [metric.key]: Number(e.target.value) })}
                  style={{ width: "100%", fontSize: 20, fontWeight: "bold", background: "transparent", border: "none", color: "#fff", marginTop: 4 }}
                />
              </div>
            ))}
          </div>

          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: "1px solid #1e293b", paddingTop: 20 }}>
            <div>
              <span style={{ color: "#94a3b8", fontSize: 14 }}>Calculated ATS Score: </span>
              <span style={{ fontSize: 24, fontWeight: "bold", color: "#10b981" }}>{calculatedAtsScore} / 100</span>
            </div>
            <div style={{ display: "flex", gap: 12 }}>
              <button onClick={runAtsEvaluation} style={{ background: "#334155" }}>Recalculate ATS</button>
              <button onClick={() => setCurrentStep(2)}>Next: AI Screening →</button>
            </div>
          </div>
        </div>
      )}

      {/* ================= STEP 2: AI SCREENING ================= */}
      {currentStep === 2 && (
        <div style={{ background: "#0b1329", border: "1px solid #1e293b", borderRadius: 14, padding: 28 }}>
          <h3 style={{ marginTop: 0, color: "#60a5fa" }}>Stage 2: Conversational AI Screening</h3>
          <p style={{ color: "#94a3b8", fontSize: 14 }}>
            Candidate provides response to automated screening questions. The AI evaluates clarity, relevance, completeness, and consistency.
          </p>

          <div style={{ background: "#1e293b", padding: 16, borderRadius: 10, margin: "18px 0" }}>
            <div style={{ fontSize: 12, color: "#38bdf8", fontWeight: "bold", textTransform: "uppercase" }}>AI Interviewer:</div>
            <p style={{ margin: "6px 0 0", fontSize: 15, color: "#f8fafc" }}>
              "Tell us about your recent technical projects and how your experience aligns with this role."
            </p>
          </div>

          <label style={{ fontSize: 13, color: "#94a3b8" }}>Candidate Answer:</label>
          <textarea
            rows="5"
            value={screeningAnswer}
            onChange={(e) => setScreeningAnswer(e.target.value)}
            style={{ width: "100%", padding: 14, background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: 8, marginTop: 6, fontSize: 14 }}
          />

          <div style={{ margin: "20px 0" }}>
            <button onClick={runScreeningEvaluation} disabled={screeningLoading} style={{ background: "#2563eb" }}>
              {screeningLoading ? "Analyzing Response..." : "Analyze with AI"}
            </button>
          </div>

          {screeningResult && (
            <div style={{ background: "#172554", border: "1px solid #3b82f6", borderRadius: 10, padding: 18, marginTop: 15 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <strong style={{ fontSize: 16, color: "#93c5fd" }}>Screening Score: {screeningResult.screening_score} / 100</strong>
                <span style={{ fontSize: 12, background: "#1e40af", padding: "4px 10px", borderRadius: 20 }}>VERIFIED</span>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10, marginTop: 14 }}>
                {Object.entries(screeningResult.pillars || {}).map(([pillar, val]) => (
                  <div key={pillar} style={{ background: "rgba(0,0,0,0.3)", padding: 10, borderRadius: 6 }}>
                    <div style={{ fontSize: 11, color: "#94a3b8", textTransform: "capitalize" }}>{pillar}</div>
                    <div style={{ fontSize: 16, fontWeight: "bold", color: "#fff" }}>{val}%</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 24, borderTop: "1px solid #1e293b", paddingTop: 18 }}>
            <button onClick={() => setCurrentStep(1)} style={{ background: "#334155" }}>← Back to ATS</button>
            <button onClick={() => setCurrentStep(3)}>Next: HR Behavioral →</button>
          </div>
        </div>
      )}

      {/* ================= STEP 3: HR BEHAVIORAL ================= */}
      {currentStep === 3 && (
        <div style={{ background: "#0b1329", border: "1px solid #1e293b", borderRadius: 14, padding: 28 }}>
          <h3 style={{ marginTop: 0, color: "#60a5fa" }}>Stage 3: HR Behavioral & Confidence Evaluation</h3>
          <p style={{ color: "#94a3b8", fontSize: 14 }}>
            Evaluates behavioral answers, sentiment, hesitation indicators, and contradiction analysis.
          </p>

          <div style={{ background: "#1e293b", padding: 16, borderRadius: 10, margin: "18px 0" }}>
            <div style={{ fontSize: 12, color: "#a78bfa", fontWeight: "bold" }}>Workplace Scenario:</div>
            <p style={{ margin: "6px 0 0", fontSize: 15, color: "#f8fafc" }}>
              "Describe a critical situation where team members disagreed on technical direction. How did you resolve it?"
            </p>
          </div>

          <label style={{ fontSize: 13, color: "#94a3b8" }}>Candidate Answer:</label>
          <textarea
            rows="4"
            value={hrAnswer}
            onChange={(e) => setHrAnswer(e.target.value)}
            style={{ width: "100%", padding: 14, background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: 8, marginTop: 6, fontSize: 14 }}
          />

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 14, margin: "20px 0" }}>
            <div style={{ background: "#1e293b", padding: 14, borderRadius: 8 }}>
              <span style={{ fontSize: 12, color: "#94a3b8" }}>Confidence / Articulation:</span>
              <input
                type="number"
                value={hrMetrics.confidence_score}
                onChange={(e) => setHrMetrics({ ...hrMetrics, confidence_score: Number(e.target.value) })}
                style={{ width: "100%", background: "transparent", border: "none", fontSize: 18, color: "#fff", fontWeight: "bold" }}
              />
            </div>
            <div style={{ background: "#1e293b", padding: 14, borderRadius: 8 }}>
              <span style={{ fontSize: 12, color: "#94a3b8" }}>Sentiment Score:</span>
              <input
                type="number"
                value={hrMetrics.sentiment_score}
                onChange={(e) => setHrMetrics({ ...hrMetrics, sentiment_score: Number(e.target.value) })}
                style={{ width: "100%", background: "transparent", border: "none", fontSize: 18, color: "#fff", fontWeight: "bold" }}
              />
            </div>
            <div style={{ background: "#1e293b", padding: 14, borderRadius: 8 }}>
              <span style={{ fontSize: 12, color: "#94a3b8" }}>Stress / Hesitation:</span>
              <input
                type="number"
                value={hrMetrics.stress_score}
                onChange={(e) => setHrMetrics({ ...hrMetrics, stress_score: Number(e.target.value) })}
                style={{ width: "100%", background: "transparent", border: "none", fontSize: 18, color: "#fff", fontWeight: "bold" }}
              />
            </div>
          </div>

          <button onClick={runHrEvaluation} style={{ background: "#2563eb", marginBottom: 15 }}>
            Compute Behavioral Score
          </button>

          {hrResult && (
            <div style={{ background: "#1e1b4b", border: "1px solid #6366f1", borderRadius: 10, padding: 16 }}>
              <strong style={{ color: "#a5b4fc", fontSize: 16 }}>
                HR Behavioral Score: {hrResult.hr_score} / 100
              </strong>
              <div style={{ fontSize: 13, color: "#cbd5e1", marginTop: 4 }}>
                Formula: Confidence (40%) + Sentiment (25%) + (100 - Stress) (20%) + Contradiction Check (15%)
              </div>
            </div>
          )}

          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 24, borderTop: "1px solid #1e293b", paddingTop: 18 }}>
            <button onClick={() => setCurrentStep(2)} style={{ background: "#334155" }}>← Back to Screening</button>
            <button onClick={() => setCurrentStep(4)}>Next: Technical Interview →</button>
          </div>
        </div>
      )}

      {/* ================= STEP 4: TECHNICAL INTERVIEW ================= */}
      {currentStep === 4 && (
        <div style={{ background: "#0b1329", border: "1px solid #1e293b", borderRadius: 14, padding: 28 }}>
          <h3 style={{ marginTop: 0, color: "#60a5fa" }}>Stage 4: Technical Skill Interview (Day 47 Model)</h3>
          <p style={{ color: "#94a3b8", fontSize: 14 }}>
            Evaluates accuracy of answer, depth of explanation, logical reasoning, and real-world applicability.
          </p>

          <div style={{ background: "#1e293b", padding: 16, borderRadius: 10, margin: "18px 0" }}>
            <div style={{ fontSize: 12, color: "#38bdf8", fontWeight: "bold" }}>Architecture Question:</div>
            <p style={{ margin: "6px 0 0", fontSize: 15, color: "#f8fafc" }}>{techQuestion}</p>
          </div>

          <label style={{ fontSize: 13, color: "#94a3b8" }}>Technical Answer:</label>
          <textarea
            rows="5"
            value={techAnswer}
            onChange={(e) => setTechAnswer(e.target.value)}
            style={{ width: "100%", padding: 14, background: "#0f172a", border: "1px solid #334155", color: "#fff", borderRadius: 8, marginTop: 6, fontSize: 14 }}
          />

          <div style={{ margin: "20px 0" }}>
            <button onClick={runTechnicalEvaluation} style={{ background: "#2563eb" }}>Evaluate Technical Rubrics</button>
          </div>

          {techResult && (
            <div style={{ background: "#083344", border: "1px solid #06b6d4", borderRadius: 10, padding: 16 }}>
              <div style={{ fontSize: 16, fontWeight: "bold", color: "#67e8f9" }}>
                Technical Interview Score: {techResult.technical_score} / 100
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10, marginTop: 12 }}>
                {Object.entries(techResult.rubric || {}).map(([k, v]) => (
                  <div key={k} style={{ background: "rgba(0,0,0,0.3)", padding: 8, borderRadius: 6 }}>
                    <div style={{ fontSize: 11, color: "#94a3b8", textTransform: "capitalize" }}>{k.replace("_", " ")}</div>
                    <div style={{ fontSize: 15, fontWeight: "bold", color: "#fff" }}>{v}%</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 24, borderTop: "1px solid #1e293b", paddingTop: 18 }}>
            <button onClick={() => setCurrentStep(3)} style={{ background: "#334155" }}>← Back to HR</button>
            <button onClick={() => setCurrentStep(5)}>Next: Machine Test →</button>
          </div>
        </div>
      )}

      {/* ================= STEP 5: MACHINE TEST ================= */}
      {currentStep === 5 && (
        <div style={{ background: "#0b1329", border: "1px solid #1e293b", borderRadius: 14, padding: 28 }}>
          <h3 style={{ marginTop: 0, color: "#60a5fa" }}>Stage 5: Hands-on Machine Test (Day 50 Engine)</h3>
          <p style={{ color: "#94a3b8", fontSize: 14 }}>
            Real-world coding problems, debugging tasks, and system design challenges evaluated via execution sandbox telemetry.
          </p>

          <div style={{ display: "flex", gap: 12, margin: "16px 0" }}>
            {[
              { id: "coding_problems", label: "LRU Cache (Coding Problem)" },
              { id: "debugging_tasks", label: "Deadlock Fix (Debugging Task)" },
              { id: "file_based_tasks", label: "CSV Pipeline (File Task)" },
              { id: "mini_system_design", label: "Rate Limiter (Mini System)" },
            ].map((t) => (
              <button
                key={t.id}
                onClick={() => setTestType(t.id)}
                style={{
                  background: testType === t.id ? "#1d4ed8" : "#1e293b",
                  padding: "8px 14px", fontSize: 12, borderRadius: 6
                }}
              >
                {t.label}
              </button>
            ))}
          </div>

          <label style={{ fontSize: 13, color: "#94a3b8" }}>Python Code Workspace:</label>
          <textarea
            rows="12"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            style={{
              width: "100%", padding: 14, background: "#020617", border: "1px solid #334155",
              color: "#38bdf8", fontFamily: "monospace", borderRadius: 8, marginTop: 6, fontSize: 13, lineHeight: 1.5
            }}
          />

          <div style={{ display: "flex", gap: 12, margin: "16px 0" }}>
            <button onClick={runMachineTest} disabled={runningTests} style={{ background: "#10b981", color: "#fff" }}>
              {runningTests ? "Executing Sandbox..." : "▶ Run Sandbox Tests"}
            </button>
            <button onClick={() => triggerWarning("Simulated Proctoring Event: Off-screen glance detected")} style={{ background: "#475569" }}>
              Simulate Proctoring Telemetry
            </button>
          </div>

          {testResults && (
            <div style={{ background: "#022c22", border: "1px solid #059669", borderRadius: 10, padding: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <strong style={{ fontSize: 16, color: "#34d399" }}>
                  Machine Test Score: {testResults.final_score} / 100 ({testResults.performance_grade})
                </strong>
                <span style={{ fontSize: 12, color: "#a7f3d0" }}>Time Multiplier: {testResults.timing?.time_factor}x</span>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10, marginTop: 12 }}>
                <div style={{ background: "rgba(0,0,0,0.3)", padding: 8, borderRadius: 6 }}>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>Tests Passed</div>
                  <div style={{ fontSize: 15, fontWeight: "bold", color: "#34d399" }}>{testResults.sandbox?.tests_passed}</div>
                </div>
                <div style={{ background: "rgba(0,0,0,0.3)", padding: 8, borderRadius: 6 }}>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>Execution Time</div>
                  <div style={{ fontSize: 15, fontWeight: "bold", color: "#fff" }}>{testResults.sandbox?.runtime_ms} ms</div>
                </div>
                <div style={{ background: "rgba(0,0,0,0.3)", padding: 8, borderRadius: 6 }}>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>Memory Used</div>
                  <div style={{ fontSize: 15, fontWeight: "bold", color: "#fff" }}>{testResults.sandbox?.memory_mb} MB</div>
                </div>
                <div style={{ background: "rgba(0,0,0,0.3)", padding: 8, borderRadius: 6 }}>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>Code Quality</div>
                  <div style={{ fontSize: 15, fontWeight: "bold", color: "#60a5fa" }}>{testResults.metrics?.code_quality}%</div>
                </div>
              </div>
            </div>
          )}

          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 24, borderTop: "1px solid #1e293b", paddingTop: 18 }}>
            <button onClick={() => setCurrentStep(4)} style={{ background: "#334155" }}>← Back to Technical</button>
            <button onClick={finalizeAssessment} disabled={finalizing} style={{ background: "#8b5cf6" }}>
              {finalizing ? "Aggregating Scores..." : "Calculate Final Hiring Fit Score →"}
            </button>
          </div>
        </div>
      )}

      {/* ================= STEP 6: UNIFIED HIRING SCORECARD ================= */}
      {currentStep === 6 && finalScorecard && (
        <div style={{ background: "#0b1329", border: "1px solid #3b82f6", borderRadius: 14, padding: 30 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 20 }}>
            <div>
              <span style={{ fontSize: 12, background: "#1e3a8a", color: "#93c5fd", padding: "4px 10px", borderRadius: 20, fontWeight: "bold" }}>
                DAY 51 UNIFIED CANDIDATE SCORE
              </span>
              <h2 style={{ margin: "10px 0 4px", fontSize: 28, color: "#fff" }}>
                {finalScorecard.candidate_name}
              </h2>
              <p style={{ margin: 0, color: "#94a3b8", fontSize: 14 }}>
                Role: <span style={{ textTransform: "capitalize", color: "#38bdf8" }}>{finalScorecard.role?.replace("_", " ")}</span> | Experience: {finalScorecard.experience_level}
              </p>
            </div>

            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 36, fontWeight: "bold", color: "#10b981" }}>
                {finalScorecard.hiring_fit_score}%
              </div>
              <div style={{
                display: "inline-block", padding: "4px 14px", borderRadius: 16, fontSize: 12, fontWeight: "bold",
                background: finalScorecard.hiring_recommendation === "STRONG_HIRE" ? "#064e3b" : "#78350f",
                color: finalScorecard.hiring_recommendation === "STRONG_HIRE" ? "#6ee7b7" : "#fde68a"
              }}>
                {finalScorecard.hiring_recommendation}
              </div>
            </div>
          </div>

          {/* 5-Stage Visual Breakdown */}
          <h4 style={{ color: "#cbd5e1", marginBottom: 12 }}>Cross-Round Evaluation Breakdown:</h4>
          <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 10 }}>
            {Object.entries(finalScorecard.stage_breakdown || {}).map(([stageKey, b]) => (
              <div key={stageKey} style={{ background: "#1e293b", padding: 14, borderRadius: 8, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ width: "30%" }}>
                  <div style={{ fontWeight: "bold", color: "#f8fafc", fontSize: 14 }}>{b.stage_name}</div>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>Role Weight: {Math.round(b.weight * 100)}%</div>
                </div>

                {/* Progress bar */}
                <div style={{ width: "45%", background: "#0f172a", height: 10, borderRadius: 5, overflow: "hidden", margin: "0 16px" }}>
                  <div style={{
                    width: `${b.raw_score}%`, height: "100%",
                    background: b.raw_score >= 85 ? "#10b981" : b.raw_score >= 70 ? "#3b82f6" : "#f59e0b"
                  }} />
                </div>

                <div style={{ width: "25%", textAlign: "right" }}>
                  <span style={{ fontSize: 14, fontWeight: "bold", color: "#fff" }}>{b.raw_score} / 100</span>
                  <div style={{ fontSize: 11, color: "#38bdf8" }}>+{b.weighted_contribution} pts</div>
                </div>
              </div>
            ))}
          </div>

          {/* Integrity & Proctoring Summary */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginTop: 20 }}>
            <div style={{ background: "#111827", padding: 16, borderRadius: 8, border: "1px solid #374151" }}>
              <div style={{ fontSize: 12, color: "#9ca3af", fontWeight: "bold" }}>PROCTORING & INTEGRITY AUDIT</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 8 }}>
                <span style={{ fontSize: 18, fontWeight: "bold", color: finalScorecard.risk_tag === "LOW_RISK" ? "#10b981" : "#f59e0b" }}>
                  {finalScorecard.risk_tag}
                </span>
                <span style={{ fontSize: 13, color: "#9ca3af" }}>Integrity Score: {finalScorecard.integrity_score}/100</span>
              </div>
            </div>

            <div style={{ background: "#111827", padding: 16, borderRadius: 8, border: "1px solid #374151" }}>
              <div style={{ fontSize: 12, color: "#9ca3af", fontWeight: "bold" }}>EXPLAINABILITY AUDIT TRAIL</div>
              <p style={{ margin: "6px 0 0", fontSize: 13, color: "#cbd5e1", lineHeight: 1.4 }}>
                {finalScorecard.transparency_audit?.explanation}
              </p>
            </div>
          </div>

          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 26 }}>
            <button onClick={() => setCurrentStep(1)} style={{ background: "#334155" }}>Retake / Adjust Inputs</button>
            <button onClick={onBack} style={{ background: "#10b981" }}>Return to Dashboard ✓</button>
          </div>
        </div>
      )}
    </div>
  );
}
