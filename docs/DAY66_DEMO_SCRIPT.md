# Day 66 — Live Demonstration Script & Speaker Notes

## 1. Demo Overview
- **Duration:** 15–20 minutes
- **Audience:** Stakeholders, Recruiters, and Technical Leadership
- **Objective:** Showcase the complete candidate journey from initial application to final hiring recommendation with live telemetry and audit logging.

---

## 2. Speaker Script & Turn-by-Turn Actions

### Part 1: Introduction & System Vision (2 Minutes)
- **Speaker:** "Welcome everyone. Today we are demonstrating the Zecpath AI Recruitment System—an autonomous hiring intelligence platform designed to replace fragmented recruiting tools with a unified, objective, and auditable talent pipeline."
- **Action:** Display Slide 1–3 of Presentation Deck.

### Part 2: Resume Ingestion & Semantic ATS Scoring (3 Minutes)
- **Speaker:** "We begin at the top of the funnel. A candidate submits their resume in PDF or DOCX format. Watch as our parser immediately extracts skills, calculates experience relevance, and checks minimum qualifications."
- **Action:** Execute ATS scoring API (`/api/scoring/evaluate`) with `CAND-DEMO-01` (Dr. Sarah Chen).
- **Expected Output:**
  - Skill Match: 92.0%
  - Experience Alignment: 6.5 Years
  - Status: `SHORTLISTED_FOR_SCREENING`

### Part 3: Conversational Screening AI (3 Minutes)
- **Speaker:** "Rather than scheduling a 30-minute phone call, our conversational AI interacts with the candidate, evaluating role alignment and communication fluency in real time."
- **Action:** Show dialogue response evaluation for architecture question.
- **Expected Output:** Intent classified as `CONFIRM_ARCHITECTURE_EXPERIENCE`; Communication score: 94.0%.

### Part 4: HR Behavioral & Technical Machine Test (4 Minutes)
- **Speaker:** "Next is the dual interview stage. We evaluate both technical problem solving through live code AST analysis and behavioral leadership through structured STAR scoring."
- **Action:** Show LRU Cache code submission evaluation and behavioral conflict resolution response.
- **Integrity Telemetry Highlight:** Show real-time monitoring of tab switches and clipboard actions. Demonstrate how `CAND-DEMO-04` was flagged with a `CRITICAL_RISK` tag for pasting 100 lines of code.

### Part 5: Cross-Round Unified Decision & Executive Scorecard (3 Minutes)
- **Speaker:** "Finally, our Unified Decision Engine consolidates scores across all rounds using calibrated weights, enforcing strict integrity guardrails."
- **Action:** Display the Executive Recruiter Scorecard generated via `export_recruiter_card()`.
- **Expected Output:**
  - Fit Tier: `EXCEPTIONAL`
  - Overall Fit Score: 88.5%
  - Recommendation: `HIRE`
  - Action: "Extend formal job offer"
  - Cryptographic Hash: Verified SHA-256 string.

### Part 6: Q&A & Wrap-Up (3 Minutes)
- **Speaker:** "In summary, Zecpath AI delivers 70% faster hiring, zero tolerance for malpractice, and complete compliance auditability. We are now open for questions."
