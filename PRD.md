# Product Requirements Document (PRD)

**Project Name:** Zecpath – AI-Powered Job Portal & Automated Hiring Assistant  
**Version:** 1.0 – 6.0 (Phases 1 – 100 Complete)  
**Prepared For:** Zecpath Product & Engineering Team  
**Prepared By:** Zecpath  

---

## 1. Project Overview
Zecpath is an AI-powered job portal designed to automate and streamline the hiring process for companies across industries and job roles (e.g., MERN Stack Developer, UI/UX Designer, Sales Executive, AI Engineer, etc.).
The platform uses AI-based ATS (Applicant Tracking System), automated AI voice calls, multilingual natural-sounding conversations, smart interview scheduling, autonomous technical evaluations, machine testing, salary negotiation, and automated offer management to reduce recruiter workload and improve hiring efficiency.

## 2. Goals & Objectives
- Reduce manual CV screening using AI ATS
- Automate initial candidate screening via AI voice calls
- Enable multilingual, gender-based AI voice selection
- Schedule interviews automatically based on role and availability
- Improve candidate experience with natural-sounding AI conversations
- Support scalable hiring for multiple companies and positions

## 3. Target Users
### 3.1 Companies / Recruiters
- HR Managers
- Recruiters
- Startup Founders
- Enterprises & Staffing Agencies
### 3.2 Candidates
- Freshers
- Experienced Professionals
- Technical & Non-Technical Job Seekers
### 3.3 Admin
- Zecpath platform administrators

## 4. Core Features Summary
- Job posting & role management
- AI-based ATS resume parsing & ranking
- Automated AI voice calling system
- Multilingual & gender-based AI voices
- Smart interview scheduling & notifications
- Email & call reminders
- Admin monitoring & analytics

---

## 5. 100-Phase Product Development Plan

### PART 1: Core Portal, ATS & Voice Screening (Phases 1–10)

#### Phase 1: Job Portal Foundation
- Company registration & verification
- Recruiter dashboard
- Job posting with role-based requirements
- Candidate registration & profile creation
- Resume upload (PDF, DOC, DOCX)
- *Output:* Functional job portal with company & candidate onboarding

#### Phase 2: AI-Powered ATS (Resume Screening)
- AI resume parsing (skills, experience, education)
- Role-based resume scoring & ranking
- Keyword matching (e.g., MERN, React, Node.js)
- Experience & qualification filtering
- Shortlisting & rejection automation
- NLP-based resume understanding & bias-reduced candidate scoring
- *Output:* Automatically shortlisted candidate list per job

#### Phase 3: Candidate Eligibility & Call Trigger Engine
- Define eligibility criteria per job role
- Auto-trigger AI calls only for shortlisted candidates
- Office-time call window configuration (e.g., 10 AM – 6 PM)
- Retry logic if call not attended (retry after 1 hour, max retry attempts configurable)

#### Phase 4: AI Voice Calling System
- Automated outbound AI calls
- Gender-based voice selection (Male / Female)
- Language selection (English, Hindi, Malayalam, Tamil, etc.)
- Natural human-like conversation, slang-friendly & polite tone
- Recruiter voice type selection per job, adjustable speaking speed & tone

#### Phase 5: AI Screening Conversation Flow
- Common AI Questions: Self introduction, Educational qualification, Total experience, Relevant skills, Current location, Notice period, Expected salary
- Voice-to-text conversion, AI answer analysis & scoring, Candidate response storage
- *Output:* AI screening report per candidate

#### Phase 6: AI Interview Scheduling Engine
- Auto-generate interview date & time
- Position-based scheduling rules
- Time-slot conflict handling (Calendar integration)
- Auto-send interview schedule email (job role, date, time & meeting details)

#### Phase 7: Interview Reminder AI Calls
- Morning-of-interview AI reminder calls
- Natural language reminder: "Today is your interview for the [Role] position. Please join on time."
- Gender & language consistency with initial call
- Timing rules: Call before office hours or recruiter-defined time

#### Phase 8: Notification & Communication System
- Channels: Email notifications, AI voice calls, SMS/WhatsApp (future scope)
- Triggers: Shortlisting confirmation, Call attempt status, Interview scheduled, Interview reminder

#### Phase 9: Recruiter Dashboard & Analytics
- Candidate pipeline view
- ATS score & AI call results
- Call status tracking (Answered / Missed / Retried)
- Interview schedule tracking
- Hiring funnel analytics & reports (job-wise performance, candidate conversion rate)

#### Phase 10: Admin Panel, Security & Compliance
- User & company management
- Call logs & AI activity monitoring
- Voice & language configuration control
- Subscription & usage tracking
- Data encryption, GDPR-style consent management, call recording compliance, secure cloud storage

---

### PART 2: Advanced AI HR Video Interview & Recruiter Monetization (Phases 11–25)

#### Phase 11: AI Video Interview Infrastructure
- Browser-based AI video interview (no app required)
- WebRTC-based secure video calling
- Mandatory camera & microphone permission
- Candidate identity validation (face presence)
- Rules: Interview cannot start unless camera is ON; Auto-disconnect if camera turned OFF repeatedly

#### Phase 12: AI Camera & Environment Validation
- Face detection before interview start
- Eye detection & gaze tracking
- Multiple face detection prevention
- Lighting & background suitability check
- AI checks: Candidate is alone, camera is stable, face clearly visible

#### Phase 13: AI Interview Instructions Engine
- AI instructions (Voice + Text): Close unnecessary tabs, Close messaging apps, Close file managers & IDEs, Do not use mobile phone, Maintain eye contact with camera
- Compliance monitoring: Tab-switch detection, Screen focus tracking

#### Phase 14: AI HR Interviewer (Voice Personality System)
- AI HR interviewer (Male / Female)
- Natural human-like voice, multilingual support
- Custom voice upload (specific person voice cloning – consent based)
- Tone: Friendly, professional, natural slang

#### Phase 15: AI HR Interview Question Engine
- Question Categories: Self introduction, Career background, Role-specific HR questions, Strengths & weaknesses, Teamwork & culture fit, Availability & commitment
- Dynamic follow-up questions & adaptive questioning based on responses

#### Phase 16: Communication Skills Analysis
- Metrics: Fluency & clarity, Confidence level, Grammar & vocabulary, Response relevance, Speech pace & tone
- *Output:* Communication skill score (0–100)

#### Phase 17: Aptitude & Cognitive Skill Assessment
- Assessment areas: Logical thinking, Problem understanding, Situational judgement, Basic aptitude questions (role-based)
- Methods: Verbal reasoning questions, Scenario-based HR cases

#### Phase 18: Facial Expression & Behavior Analysis
- AI monitoring: Eye movement & focus, Head movement, Nervous gestures, Facial expressions (confidence, stress)
- Purpose: Detect distraction or malpractice, Behavioral insights for recruiters

#### Phase 19: Malpractice & Integrity Detection
- Checks: Repeated tab switching, Looking away frequently, External voice detection, Mobile usage detection
- Actions: Warning prompts, Auto-flag interview

#### Phase 20: AI Scoring & Decision Engine
- Scoring parameters: HR answers, Communication skills, Aptitude score, Behavioral score, ATS score (from Phase 2)
- Decision types: Selected for next round, Hold / Review, Rejected

#### Phase 21: Automated Selection / Rejection Communication
- Auto-generated selection email & rejection email
- Next round details (if selected)
- Customization: Role-based templates, company branding

#### Phase 22: Interview Recording & Secure Storage
- Recorded data: Video recording, Audio transcript, AI notes & highlights, Timestamped events
- Storage: Encrypted storage, role-based access

#### Phase 23: Recruiter Paid Access System
- Access model: Recruiters pay to unlock interview details
- Preview limited data (basic score only), full access after payment
- Unlocked data: Full interview video, AI scores & remarks, Behavioral analysis

#### Phase 24: Recruiter Interview Review Dashboard
- Candidate-wise interview playback, AI-generated summary, Strengths & risk flags, Download reports (PDF)
- Filters: Job role, Score range, Interview status

#### Phase 25: Compliance, Consent & Legal Safeguards
- Candidate consent for AI interview & recording
- Voice cloning consent
- Data retention policy & GDPR-style compliance
- Security: Audit logs, Access tracking, Secure payments

---

### PART 3: Second Round AI Calls & Technical Video Interviews (Phases 26–50)

#### Phase 26: Second-Round Candidate Shortlisting Engine
- Auto-identify candidates selected from HR round
- Job-role and score-based filtering, Configurable cutoff scores
- *Output:* Eligible candidates list for second round

#### Phase 27: AI Second-Round Call Trigger System
- Automated AI outbound calls for second-round selected candidates
- Role-based call scripts; Office-time calling only, Configurable working hours

#### Phase 28: Multilingual & Gender-Based AI Calling
- Male / Female AI voice selection, Language selection per job role, Natural slang-based speech
- Recruiter-defined voice & language

#### Phase 29: AI Call Retry & Attendance Logic
- If candidate does not attend -> retry after 1 hour, Max retry attempts configurable
- Call status tracking (Answered / Missed / Failed)

#### Phase 30: AI Interview Schedule Confirmation Call
- AI informs interview date & time, confirms candidate availability, updates interview calendar automatically

#### Phase 31: Automated Interview Schedule Email
- Job role & level, interview date & time, video interview link, system & camera requirements

#### Phase 32: Interview-Day Reminder AI Call
- Morning reminder call ("Today is your technical interview. Please join on time.")
- Voice & language continuity

#### Phase 33: Technical Video Interview Infrastructure
- Browser-based video interview, mandatory camera & mic access, secure WebRTC communication
- Rules: Interview cannot start unless camera is ON

#### Phase 34: AI Camera Validation & Identity Check
- AI checks: Face detection, Eye visibility, Single-person verification
- Actions: Auto-warning if camera turned OFF

#### Phase 35: AI Pre-Interview Technical Instructions
- Voice + Text instructions: Close unused browser tabs, Close chat applications, Close file managers & IDEs, Do not use mobile phone

#### Phase 36: AI Technical Interviewer Personality System
- AI Technical Interviewer (Male / Female), Natural human-like voice, Multilingual, Custom voice cloning (consent-based)

#### Phase 37: Experience-Based Question Generation Engine
- Questions based on years of experience, Role-specific (MERN, Java, DevOps, etc.), Difficulty scaling (Basic -> Advanced)

#### Phase 38: Theoretical Technical Question Module
- Question types: Core concept questions, Architecture & design basics, Best practices, Real-world scenarios

#### Phase 39: Adaptive Follow-Up Questioning
- Real-time answer analysis, generate deeper follow-up questions, adjust difficulty dynamically

#### Phase 40: Technical Skill Evaluation Engine
- Evaluation areas: Concept clarity, Problem understanding, Technical depth, Logical explanation ability
- *Output:* Skill-wise technical score

#### Phase 41: Behavioral & Movement Analysis (Technical Round)
- AI monitoring: Eye movement & gaze tracking, Head movement, Facial expressions, Distraction detection

#### Phase 42: Malpractice & Assistance Detection
- Checks: Repeated tab switching, External voice detection, Screen focus loss, Mobile usage detection

#### Phase 43: Technical Interview Recording System
- Full video & audio, AI-generated transcript, Question-wise timestamps, Encrypted storage

#### Phase 44: AI Technical Scoring & Weightage Engine
- Scoring parameters: Technical accuracy, Depth of explanation, Confidence, Behavioral integrity
- Weightage configurable per role

#### Phase 45: AI Final Recommendation Engine
- Decision outputs: Selected for next round, Hold / Review, Rejected
- Logic: Combines ATS + HR + Technical scores

#### Phase 46: Automated Selection / Rejection Email System
- Auto-send technical round result, Next-round details if selected, Polite rejection messaging

#### Phase 47: Candidate Interview Summary Generation
- Summary includes: Strengths, Weaknesses, Technical gaps, AI recommendation

#### Phase 48: Paid Recruiter Access Control
- Access model: Recruiters view basic score preview, full access unlocked after payment

#### Phase 49: Recruiter Technical Review Dashboard
- Interview video playback, Technical score breakdown, AI comments & flags, Exportable reports

#### Phase 50: Compliance, Audit & Data Retention
- Candidate consent for AI technical interviews, Voice cloning consent, Secure payment compliance
- Audit: Activity logs, Access history

---

### PART 4: Machine Test & Advanced Technical Evaluation (Phases 51–75)

#### Phase 51: Machine Test Candidate Shortlisting Engine
- Auto-select candidates cleared in technical theory round
- Score-based eligibility rules, Role-specific thresholds
- *Output:* Machine-test eligible candidate list

#### Phase 52: AI Machine Test Call Trigger System
- Automated AI outbound calls for machine test round, Office-hour calling enforcement, Job-role-based call flow

#### Phase 53: Multilingual & Gender-Based AI Call Voice
- Male / Female AI voice, Language selection per candidate, Natural slang, Recruiter-defined voice profile

#### Phase 54: AI Call Retry & Scheduling Logic
- If call not answered -> retry after 1 hour, Configurable retry limits, Auto-update call attempt status

#### Phase 55: AI Machine Test Interview Confirmation Call
- AI confirms test date & time, explains machine test nature, captures candidate confirmation

#### Phase 56: Automated Machine Test Schedule Email
- Job role & experience level, Machine test date & time, Test environment instructions, Camera & system requirements

#### Phase 57: Machine Test Reminder AI Call
- Morning reminder AI call ("Today is your machine test interview. Please join on time.")

#### Phase 58: Machine Test Video Interview Infrastructure
- Browser-based secure environment, Mandatory camera & microphone ON, Screen-sharing permission enforcement

#### Phase 59: AI Camera, Face & Identity Validation
- Face presence & clarity, Eye detection & gaze tracking, Single-person verification

#### Phase 60: AI Pre-Test Instructions & Compliance Engine
- Close unused tabs & applications, Disable messaging apps, Do not use mobile phone, Follow AI instructions strictly

#### Phase 61: AI Technical Interviewer (Machine Test)
- AI Technical Evaluator (Male / Female), Natural multilingual voice, Custom uploaded human voice (consent clone)

#### Phase 62: Experience-Based Machine Test Generation
- Tests based on experience level, Role-specific tasks (coding, design, ops), Difficulty scaling (Basic -> Advanced)

#### Phase 63: Live Coding / Task Execution Environment
- Supported tests: Live coding editor, File-based tasks, Debugging exercises, System design mini tasks

#### Phase 64: AI Real-Time Guidance & Clarification
- AI explains task requirements, Clarifies doubts (non-leading), Time reminders

#### Phase 65: Technical Skill Validation Engine
- Evaluation areas: Logic & correctness, Code quality / task accuracy, Efficiency & best practices, Problem-solving approach

#### Phase 66: Behavior & Focus Monitoring (Machine Test)
- AI monitoring: Eye movement & gaze, Screen focus, Repeated distractions

#### Phase 67: Malpractice & External Assistance Detection
- Checks: Tab switching, External voice detection, Copy-paste abuse, Secondary device usage

#### Phase 68: Machine Test Recording & Evidence Capture
- Video & audio, Screen recording, Code/task snapshots, Time-stamped events

#### Phase 69: AI Machine Test Scoring Engine
- Scoring metrics: Task completion, Accuracy, Optimization, Behavioral integrity

#### Phase 70: Cross-Round Score Aggregation Engine
- Combines: ATS score, HR round score, Technical theory score, Machine test score

#### Phase 71: AI Final Selection Recommendation Engine
- Decisions: Final selected, On hold, Rejected; Confidence score: Hiring fit percentage

#### Phase 72: Automated Selection / Rejection Communication
- Final selection email, Next steps or offer pipeline, Polite rejection email

#### Phase 73: Recruiter Paid Access – Machine Test Insights
- Access model: Preview overall score & status, Paid unlock for full recordings & AI analysis

#### Phase 74: Recruiter Advanced Review Dashboard
- Replay machine test sessions, Code/task review, AI comments & red flags, Downloadable reports

#### Phase 75: Compliance, Audit & Data Retention (Machine Test)
- Explicit consent for recording & monitoring, Voice cloning consent, Secure payment compliance, Activity logs & access tracking

---

### PART 5: Fourth Round & Salary Negotiation (Phases 76–90)

#### Phase 76: Fourth-Round Candidate Eligibility Engine
- Auto-select candidates cleared in machine test round, Final-round eligibility score threshold, Position & budget-based filtering
- *Output:* Fourth-round eligible candidate list

#### Phase 77: AI Fourth-Round Call Trigger System
- Automated AI outbound calls, Office-time enforcement, Role-based negotiation call script

#### Phase 78: Multilingual & Gender-Based AI Calling Voice
- Male / Female voice selection, Candidate-preferred language, Natural slang & human tone, Recruiter-defined voice profile

#### Phase 79: AI Call Retry & Attendance Rules
- If candidate does not attend -> retry after 1 hour, Configurable retry limits, Call status & logs

#### Phase 80: AI Interview Schedule Confirmation & Email
- AI confirms final interview date & time, Auto-sends schedule email with role & salary discussion note

#### Phase 81: Interview-Day Reminder AI Call
- Morning reminder call ("Today is your final interview. Please join on time.")

#### Phase 82: Final Video Interview Infrastructure
- Secure browser-based video interview, Mandatory camera & microphone ON, Interview lock if camera disabled

#### Phase 83: AI Camera, Face & Focus Validation
- AI checks: Face & eye tracking, Single-person verification, Distraction detection

#### Phase 84: AI Pre-Negotiation Instructions Engine
- Close unused tabs & applications, Disable messaging apps, Maintain focus & eye contact

#### Phase 85: AI Final Interviewer & Salary Negotiator
- AI interviewer (Male / Female), Natural multilingual voice, Custom uploaded voice (consent-based)
- Role: Conduct final discussion, Lead salary negotiation

#### Phase 86: Salary Negotiation Intelligence Engine
- Inputs: Company budget range, Candidate experience & skills, Previous round scores, Market salary benchmarks
- Capabilities: Dynamic offer suggestion, Counter-offer handling, Fair & compliant negotiation

#### Phase 87: Behavioral & Integrity Analysis (Final Round)
- AI monitoring: Facial expressions, Eye movement, Confidence & stress indicators
- Purpose: Assess negotiation confidence & honesty

#### Phase 88: Final Scoring & Hiring Decision Engine
- Scoring includes: Technical competency, Behavioral consistency, Negotiation outcome, Budget alignment
- Decision outputs: Offer recommended, Hold / Review, Rejected

#### Phase 89: Automated Final Communication System
- Offer discussion email, Selection confirmation email, Rejection email (polite & branded)

#### Phase 90: Recording, Paid Recruiter Access & Compliance
- Recorded data: Video & audio, Negotiation transcript, AI scoring & recommendations
- Recruiter preview (basic outcome), full access after payment
- Explicit consent for recording & negotiation, Secure data retention & audit logs

---

### PART 6: Final Selection, Offer Letter & Onboarding Automation (Phases 91–100)

#### Phase 91: Final Candidate Selection Lock Engine
- Auto-lock candidates marked as "Final Selected"
- Prevent further evaluation changes
- Position-based selection mapping
- *Output:* Final selected candidate list per job role

#### Phase 92: AI Final Selection Call Trigger System
- Automated AI outbound selection calls, Office-time calling only, Role-based congratulatory call scripts

#### Phase 93: Multilingual & Gender-Based AI Selection Voice
- Male / Female AI voice selection, Candidate-preferred language, Natural polite congratulatory tone, Recruiter-selected voice profile

#### Phase 94: AI Call Retry & Attendance Handling
- If candidate does not attend -> retry after 1 hour, Configurable retry limits, Call status logging (Answered / Missed)

#### Phase 95: AI Verbal Offer Confirmation Call
- AI call content: Congratulate candidate on selection, Confirm job position & location, Confirm joining interest, Inform about offer letter email

#### Phase 96: Automated Selection Confirmation Email
- Email includes: Selection confirmation, Job role & department, Salary summary, Joining date & time, Next steps instructions

#### Phase 97: AI Offer Letter Generation Engine
- Features: Auto-generate offer letter (PDF), Company logo & seal embedded, Position-based offer template, Joining date, time & location, Compensation & terms, Company-specific templates

#### Phase 98: Offer Letter Approval & Dispatch System
- Recruiter review (optional), Auto-send offer letter via email, Download & e-signature support (future scope)

#### Phase 99: Offer Acceptance Tracking & Joining Confirmation
- Candidate offer acceptance tracking, AI reminder emails/calls for acceptance, Joining confirmation status update

#### Phase 100: Paid Recruiter Access, Audit & Completion
- Access model: Recruiters preview basic outcome; Full access after payment: Offer letter, Selection call recording, Final AI decision report
- Compliance & Audit: Consent records, Access logs, Secure data retention
