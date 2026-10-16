import { useState, useEffect } from "react";

const API_BASE = "http://localhost:8000/api/assessment";

export default function RecruiterDashboard({ onBack }) {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRole, setSelectedRole] = useState("all");
  const [selectedFilter, setSelectedFilter] = useState("all");
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [updatingStatus, setUpdatingStatus] = useState(false);

  // Load evaluated candidates from API
  useEffect(() => {
    fetchCandidates();
  }, [selectedRole]);

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const url = selectedRole === "all" ? `${API_BASE}/candidates` : `${API_BASE}/candidates?role=${selectedRole}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setCandidates(data);
      } else {
        setCandidates(getDefaultCandidates());
      }
    } catch {
      setCandidates(getDefaultCandidates());
    } finally {
      setLoading(false);
    }
  };

  const getDefaultCandidates = () => [
    {
      candidate_id: "CAND-101",
      candidate_name: "Alex Rivera",
      role: "ai_engineer",
      experience_level: "senior",
      hiring_fit_score: 90.27,
      hiring_recommendation: "STRONG_HIRE",
      integrity_score: 100.0,
      risk_tag: "LOW_RISK",
      status: "shortlisted",
      scores: { ats: 88, screening: 85, hr: 90, technical: 94, machine_test: 92 },
      audit_notes: "Strong machine test performance and domain-relevant architectural reasoning.",
    },
    {
      candidate_id: "CAND-102",
      candidate_name: "Priya Sharma",
      role: "software_engineer",
      experience_level: "entry",
      hiring_fit_score: 87.87,
      hiring_recommendation: "STRONG_HIRE",
      integrity_score: 100.0,
      risk_tag: "LOW_RISK",
      status: "shortlisted",
      scores: { ats: 74, screening: 82, hr: 80, technical: 88, machine_test: 95 },
      audit_notes: "Exemplary machine test score (95%) balanced entry-level resume profile.",
    },
    {
      candidate_id: "CAND-103",
      candidate_name: "Marcus Vance",
      role: "software_engineer",
      experience_level: "mid",
      hiring_fit_score: 60.7,
      hiring_recommendation: "BORDERLINE_REVIEW",
      integrity_score: 55.0,
      risk_tag: "HIGH_RISK",
      status: "review",
      scores: { ats: 68, screening: 62, hr: 58, technical: 64, machine_test: 55 },
      audit_notes: "Multiple tab switches and off-screen glances during technical questions.",
    },
    {
      candidate_id: "CAND-104",
      candidate_name: "Elena Rostova",
      role: "data_analyst",
      experience_level: "mid",
      hiring_fit_score: 82.2,
      hiring_recommendation: "HIRE",
      integrity_score: 95.0,
      risk_tag: "LOW_RISK",
      status: "shortlisted",
      scores: { ats: 82, screening: 78, hr: 84, technical: 80, machine_test: 86 },
      audit_notes: "Solid statistical analysis capabilities and structured communication.",
    },
  ];

  const handleUpdateStatus = async (candidateId, newStatus) => {
    setUpdatingStatus(true);
    try {
      await fetch(`${API_BASE}/candidate/${candidateId}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
      setCandidates((prev) =>
        prev.map((c) => (c.candidate_id === candidateId ? { ...c, status: newStatus } : c))
      );
      if (selectedCandidate && selectedCandidate.candidate_id === candidateId) {
        setSelectedCandidate({ ...selectedCandidate, status: newStatus });
      }
    } catch {
      // Optimistic update
      setCandidates((prev) =>
        prev.map((c) => (c.candidate_id === candidateId ? { ...c, status: newStatus } : c))
      );
    } finally {
      setUpdatingStatus(false);
    }
  };

  const filteredCandidates = candidates.filter((c) => {
    if (selectedFilter === "all") return true;
    return c.hiring_recommendation === selectedFilter || c.status === selectedFilter;
  });

  return (
    <div style={{ maxWidth: 1200, margin: "0 auto", padding: "30px 20px" }}>
      {/* Top Bar */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 25 }}>
        <div>
          <button onClick={onBack} style={{ background: "transparent", color: "#60a5fa", padding: "6px 12px", border: "1px solid #1e293b", marginBottom: 8, fontSize: 13 }}>
            ← Back to Recruiter Portal
          </button>
          <h2 style={{ margin: "5px 0 0", fontSize: 28, color: "#fff" }}>
            Cross-Round Candidate Intelligence
          </h2>
          <p style={{ margin: 0, color: "#94a3b8", fontSize: 14 }}>
            Aggregating ATS, Screening, HR Behavioral, Technical, and Machine Test Scores with Proctoring Audits
          </p>
        </div>

        <button onClick={fetchCandidates} style={{ background: "#2563eb", fontSize: 13, padding: "10px 18px" }}>
          🔄 Refresh Feed
        </button>
      </div>

      {/* KPI Stat Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 25 }}>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 18 }}>
          <div style={{ fontSize: 12, color: "#94a3b8" }}>Total Assessed</div>
          <div style={{ fontSize: 26, fontWeight: "bold", color: "#fff", marginTop: 4 }}>{candidates.length}</div>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 18 }}>
          <div style={{ fontSize: 12, color: "#94a3b8" }}>Strong Hire Candidates</div>
          <div style={{ fontSize: 26, fontWeight: "bold", color: "#10b981", marginTop: 4 }}>
            {candidates.filter((c) => c.hiring_recommendation === "STRONG_HIRE").length}
          </div>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 18 }}>
          <div style={{ fontSize: 12, color: "#94a3b8" }}>Proctoring High-Risk Flags</div>
          <div style={{ fontSize: 26, fontWeight: "bold", color: "#ef4444", marginTop: 4 }}>
            {candidates.filter((c) => c.risk_tag === "HIGH_RISK" || c.risk_tag === "CRITICAL_RISK").length}
          </div>
        </div>
        <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, padding: 18 }}>
          <div style={{ fontSize: 12, color: "#94a3b8" }}>Average Fit Score</div>
          <div style={{ fontSize: 26, fontWeight: "bold", color: "#38bdf8", marginTop: 4 }}>
            {candidates.length ? (candidates.reduce((acc, c) => acc + c.hiring_fit_score, 0) / candidates.length).toFixed(1) : 0}%
          </div>
        </div>
      </div>

      {/* Filter Row */}
      <div style={{ display: "flex", gap: 14, marginBottom: 20 }}>
        <select
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
          style={{ padding: "8px 14px", background: "#1e293b", border: "1px solid #334155", color: "#fff", borderRadius: 8, fontSize: 13 }}
        >
          <option value="all">All Roles</option>
          <option value="software_engineer">Software Engineer</option>
          <option value="ai_engineer">AI Engineer</option>
          <option value="data_analyst">Data Analyst</option>
        </select>

        <select
          value={selectedFilter}
          onChange={(e) => setSelectedFilter(e.target.value)}
          style={{ padding: "8px 14px", background: "#1e293b", border: "1px solid #334155", color: "#fff", borderRadius: 8, fontSize: 13 }}
        >
          <option value="all">All Statuses & Recommendations</option>
          <option value="STRONG_HIRE">Strong Hire Only</option>
          <option value="HIRE">Hire Only</option>
          <option value="BORDERLINE_REVIEW">Borderline Only</option>
          <option value="shortlisted">Shortlisted Status</option>
        </select>
      </div>

      {/* Candidate Table */}
      <div style={{ background: "#0f172a", border: "1px solid #1e293b", borderRadius: 12, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: 14 }}>
          <thead>
            <tr style={{ background: "#1e293b", color: "#94a3b8", fontSize: 12, textTransform: "uppercase" }}>
              <th style={{ padding: "14px 18px" }}>Candidate</th>
              <th style={{ padding: "14px 18px" }}>Role & Tier</th>
              <th style={{ padding: "14px 18px" }}>Cross-Round Scores</th>
              <th style={{ padding: "14px 18px" }}>Hiring Fit %</th>
              <th style={{ padding: "14px 18px" }}>Proctor Risk</th>
              <th style={{ padding: "14px 18px" }}>Status</th>
              <th style={{ padding: "14px 18px" }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredCandidates.map((c) => (
              <tr key={c.candidate_id} style={{ borderBottom: "1px solid #1e293b" }}>
                <td style={{ padding: "14px 18px" }}>
                  <div style={{ fontWeight: "bold", color: "#fff" }}>{c.candidate_name}</div>
                  <div style={{ fontSize: 12, color: "#64748b" }}>{c.candidate_id}</div>
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <div style={{ textTransform: "capitalize", color: "#e2e8f0" }}>{c.role?.replace("_", " ")}</div>
                  <div style={{ fontSize: 12, color: "#94a3b8" }}>{c.experience_level}</div>
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <div style={{ display: "flex", gap: 6 }}>
                    <span title="ATS" style={{ fontSize: 11, background: "#1e293b", padding: "2px 6px", borderRadius: 4 }}>
                      ATS: {c.scores?.ats}
                    </span>
                    <span title="Tech" style={{ fontSize: 11, background: "#1e293b", padding: "2px 6px", borderRadius: 4 }}>
                      Tech: {c.scores?.technical}
                    </span>
                    <span title="Machine Test" style={{ fontSize: 11, background: "#1e293b", padding: "2px 6px", borderRadius: 4, color: "#38bdf8" }}>
                      Code: {c.scores?.machine_test}
                    </span>
                  </div>
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <div style={{ fontSize: 18, fontWeight: "bold", color: c.hiring_fit_score >= 85 ? "#10b981" : "#f59e0b" }}>
                    {c.hiring_fit_score}%
                  </div>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>{c.hiring_recommendation}</div>
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <span style={{
                    fontSize: 11, padding: "3px 8px", borderRadius: 12, fontWeight: "bold",
                    background: c.risk_tag === "LOW_RISK" ? "#064e3b" : "#7f1d1d",
                    color: c.risk_tag === "LOW_RISK" ? "#6ee7b7" : "#fca5a5",
                  }}>
                    {c.risk_tag}
                  </span>
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <span style={{
                    fontSize: 12, padding: "3px 8px", borderRadius: 6, textTransform: "capitalize",
                    background: c.status === "shortlisted" ? "#1e3a8a" : "#334155",
                    color: c.status === "shortlisted" ? "#93c5fd" : "#cbd5e1"
                  }}>
                    {c.status}
                  </span>
                </td>
                <td style={{ padding: "14px 18px" }}>
                  <button
                    onClick={() => setSelectedCandidate(c)}
                    style={{ background: "#334155", fontSize: 12, padding: "6px 12px", borderRadius: 6 }}
                  >
                    View Scorecard
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Deep-Dive Scorecard Drawer / Modal */}
      {selectedCandidate && (
        <div style={{
          position: "fixed", top: 0, left: 0, right: 0, bottom: 0,
          background: "rgba(0,0,0,0.75)", display: "flex", justifyContent: "center",
          alignItems: "center", zIndex: 1000, padding: 20
        }}>
          <div style={{
            background: "#0b1329", border: "1px solid #334155", borderRadius: 14,
            width: "100%", maxWidth: 800, maxHeight: "90vh", overflowY: "auto", padding: 28
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 20 }}>
              <div>
                <h3 style={{ margin: 0, fontSize: 24, color: "#fff" }}>{selectedCandidate.candidate_name}</h3>
                <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 4 }}>
                  ID: {selectedCandidate.candidate_id} | Role: {selectedCandidate.role?.replace("_", " ")}
                </div>
              </div>
              <button onClick={() => setSelectedCandidate(null)} style={{ background: "transparent", color: "#94a3b8", fontSize: 24, border: "none", cursor: "pointer" }}>
                ×
              </button>
            </div>

            {/* Score Highlights */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 20 }}>
              <div style={{ background: "#1e293b", padding: 16, borderRadius: 10 }}>
                <div style={{ fontSize: 12, color: "#94a3b8" }}>Unified Hiring Fit</div>
                <div style={{ fontSize: 32, fontWeight: "bold", color: "#10b981", marginTop: 4 }}>
                  {selectedCandidate.hiring_fit_score}%
                </div>
                <div style={{ fontSize: 12, color: "#60a5fa" }}>{selectedCandidate.hiring_recommendation}</div>
              </div>

              <div style={{ background: "#1e293b", padding: 16, borderRadius: 10 }}>
                <div style={{ fontSize: 12, color: "#94a3b8" }}>Proctoring Integrity Audit</div>
                <div style={{ fontSize: 32, fontWeight: "bold", color: selectedCandidate.risk_tag === "LOW_RISK" ? "#10b981" : "#ef4444", marginTop: 4 }}>
                  {selectedCandidate.risk_tag}
                </div>
                <div style={{ fontSize: 12, color: "#94a3b8" }}>Integrity Score: {selectedCandidate.integrity_score}/100</div>
              </div>
            </div>

            {/* Stage Scores Breakdown */}
            <h4 style={{ color: "#cbd5e1", marginBottom: 10 }}>Five Stage Performance:</h4>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 10, marginBottom: 20 }}>
              {[
                { label: "ATS Match", score: selectedCandidate.scores?.ats },
                { label: "Screening", score: selectedCandidate.scores?.screening },
                { label: "HR Behavioral", score: selectedCandidate.scores?.hr },
                { label: "Technical", score: selectedCandidate.scores?.technical },
                { label: "Machine Test", score: selectedCandidate.scores?.machine_test },
              ].map((s) => (
                <div key={s.label} style={{ background: "#111827", padding: 10, borderRadius: 8, textAlign: "center" }}>
                  <div style={{ fontSize: 11, color: "#94a3b8" }}>{s.label}</div>
                  <div style={{ fontSize: 18, fontWeight: "bold", color: "#38bdf8", marginTop: 4 }}>{s.score}</div>
                </div>
              ))}
            </div>

            <div style={{ background: "#111827", padding: 14, borderRadius: 8, marginBottom: 20 }}>
              <div style={{ fontSize: 12, color: "#94a3b8", fontWeight: "bold" }}>TRANSPARENCY AUDIT NOTES:</div>
              <p style={{ margin: "6px 0 0", fontSize: 13, color: "#cbd5e1" }}>
                {selectedCandidate.audit_notes || "All evaluation rounds verified by automated AI scoring models."}
              </p>
            </div>

            {/* Recruiter Actions */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: "1px solid #1e293b", paddingTop: 18 }}>
              <div style={{ fontSize: 13, color: "#94a3b8" }}>
                Current Status: <strong style={{ color: "#fff", textTransform: "capitalize" }}>{selectedCandidate.status}</strong>
              </div>

              <div style={{ display: "flex", gap: 10 }}>
                <button
                  onClick={() => handleUpdateStatus(selectedCandidate.candidate_id, "rejected")}
                  disabled={updatingStatus}
                  style={{ background: "#dc2626", fontSize: 13, padding: "8px 16px" }}
                >
                  Reject
                </button>
                <button
                  onClick={() => handleUpdateStatus(selectedCandidate.candidate_id, "shortlisted")}
                  disabled={updatingStatus}
                  style={{ background: "#2563eb", fontSize: 13, padding: "8px 16px" }}
                >
                  Shortlist
                </button>
                <button
                  onClick={() => handleUpdateStatus(selectedCandidate.candidate_id, "hired")}
                  disabled={updatingStatus}
                  style={{ background: "#10b981", fontSize: 13, padding: "8px 16px" }}
                >
                  Hire Candidate ✓
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
