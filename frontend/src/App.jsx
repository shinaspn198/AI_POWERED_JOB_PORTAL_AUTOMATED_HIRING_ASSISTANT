import { useState } from "react";
import "./App.css";


// ======================================================
// AUTH MODAL
// ======================================================

function AuthModal({
  setShowAuthModal,
  setRole,
  setAuthPage,
}) {
  return (
    <div className="auth-modal-overlay">

      <div className="auth-modal">

        <button
          className="auth-close"
          onClick={() => setShowAuthModal(false)}
        >
          ×
        </button>


        <h2>
          Welcome to Zecpath AI
        </h2>


        <p>
          Login or create your account to continue.
        </p>


        <input
          type="text"
          className="auth-input"
          placeholder="Email or phone number"
        />


        <button className="auth-continue">
          Continue
        </button>


        <div className="auth-divider">

          <span>
            Continue as
          </span>

        </div>


        <div className="role-options">

          {/* JOB SEEKER */}

          <button
            className="role-card"
            onClick={() => {

              setRole("jobseeker");

              setShowAuthModal(false);

              setAuthPage("signup");

            }}
          >

            <span className="role-icon">
              👤
            </span>

            <strong>
              Job Seeker
            </strong>

            <small>
              Find opportunities and build your career.
            </small>

          </button>


          {/* RECRUITER */}

          <button
            className="role-card"
            onClick={() => {

              setRole("recruiter");

              setShowAuthModal(false);

              setAuthPage("signup");

            }}
          >

            <span className="role-icon">
              🏢
            </span>

            <strong>
              Recruiter
            </strong>

            <small>
              Find candidates and manage hiring.
            </small>

          </button>

        </div>


        <p className="login-text">

          Already have an account?

          <button
            className="login-link"
            onClick={() => {

              setShowAuthModal(false);

              setAuthPage("login");

            }}
          >
            Login
          </button>

        </p>

      </div>

    </div>
  );
}



// ======================================================
// MAIN APP
// ======================================================

function App() {

  const [role, setRole] = useState(null);

  const [showRoleSelection, setShowRoleSelection] =
    useState(false);

  const [isAuthenticated, setIsAuthenticated] =
    useState(false);

  const [jobSeekerPage, setJobSeekerPage] =
    useState("dashboard");

  const [authPage, setAuthPage] =
    useState(null);

  const [showAuthModal, setShowAuthModal] =
    useState(false);


  const [file, setFile] = useState(null);

  const [uploading, setUploading] =
    useState(false);

  const [parsing, setParsing] =
    useState(false);


  const [candidate, setCandidate] =
    useState(null);

  const [profile, setProfile] =
    useState(null);


  const [error, setError] =
    useState("");



  // ======================================================
  // UPLOAD RESUME
  // ======================================================

  const handleUpload = async () => {

    if (!file) {

      setError(
        "Please select a resume first."
      );

      return;
    }


    setUploading(true);

    setError("");

    setCandidate(null);

    setProfile(null);


    const formData = new FormData();

    formData.append(
      "resume",
      file
    );


    try {

      const response =
        await fetch(
          "http://127.0.0.1:8000/api/resume/upload",
          {
            method: "POST",
            body: formData,
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Resume upload failed."
        );

      }


      setCandidate(data);

    } catch (err) {

      setError(err.message);

    } finally {

      setUploading(false);

    }

  };



  // ======================================================
  // PARSE RESUME
  // ======================================================

  const handleParse = async () => {

    if (!candidate?.candidate_id) {

      setError(
        "Candidate ID is missing."
      );

      return;
    }


    setParsing(true);

    setError("");


    try {

      const response =
        await fetch(
          "http://127.0.0.1:8000/api/resume/parse",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              candidate_id:
                candidate.candidate_id,
            }),
          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Resume parsing failed."
        );

      }


      setProfile(
        data.profile
      );

    } catch (err) {

      setError(
        err.message
      );

    } finally {

      setParsing(false);

    }

  };



  // ======================================================
  // PUBLIC FIND JOBS PAGE
  // ======================================================

  if (
    jobSeekerPage === "jobs" &&
    !role
  ) {

    return (

      <div className="open-roles-page">


        {/* ================================================= */}
        {/* FIND JOBS HEADER */}
        {/* ================================================= */}

        <header className="open-roles-header">

          <div className="open-roles-header-inner">


            <div className="open-roles-brand">

              <svg
                className="open-roles-brand-mark"
                viewBox="0 0 26 26"
                fill="none"
              >

                <circle
                  cx="13"
                  cy="13"
                  r="12"
                  stroke="#F2A93B"
                  strokeWidth="1.6"
                />

                <path
                  d="M6 16 Q12 8 20 10"
                  stroke="#4FD1C5"
                  strokeWidth="1.6"
                  fill="none"
                  strokeLinecap="round"
                />

                <circle
                  cx="6"
                  cy="16"
                  r="1.8"
                  fill="#4FD1C5"
                />

                <circle
                  cx="20"
                  cy="10"
                  r="1.8"
                  fill="#F2A93B"
                />

              </svg>

              Zecpath AI

            </div>



            <nav className="open-roles-nav">

              <a href="#open-roles">
                Open roles
              </a>

              <a href="#companies">
                Companies
              </a>

              <a href="#candidates">
                For candidates
              </a>


              <button
                className="open-roles-post-btn"
                onClick={() =>
                  setShowAuthModal(true)
                }
              >
                Post a role
              </button>

            </nav>

          </div>

        </header>



        {/* ================================================= */}
        {/* HERO */}
        {/* ================================================= */}

        <section className="open-roles-hero">

          <div className="open-roles-hero-grid">


            {/* LEFT SIDE */}

            <div>

              <h1>
                Every great career is a path someone else can point you toward.
              </h1>


              <p className="open-roles-lede">

                Zecpath tracks the roles, skills and teams shaping AI hiring
                right now — so you spend less time searching and more time
                applying.

              </p>


              <div className="open-roles-search">

                <input
                  type="text"
                  placeholder='Try "FastAPI" or "Kochi"'
                />

                <button>
                  Search
                </button>

              </div>


              <div className="open-roles-stats">

                <div>

                  <b>
                    340+
                  </b>

                  <span>
                    Open roles
                  </span>

                </div>


                <div>

                  <b>
                    128
                  </b>

                  <span>
                    Hiring companies
                  </span>

                </div>


                <div>

                  <b>
                    62%
                  </b>

                  <span>
                    Remote-friendly
                  </span>

                </div>

              </div>

            </div>



            {/* RIGHT SIDE CAREER PATH */}

            <div className="open-roles-route">

              <svg
                viewBox="0 0 380 340"
                fill="none"
              >

                <path
                  d="M40 300 C 100 260, 60 190, 140 170 S 260 100, 240 50"
                  stroke="#232B45"
                  strokeWidth="2"
                  strokeDasharray="1 10"
                  strokeLinecap="round"
                />


                <path
                  d="M40 300 C 100 260, 60 190, 140 170 S 260 100, 240 50"
                  stroke="#4FD1C5"
                  strokeWidth="2"
                  strokeDasharray="6 320"
                  strokeLinecap="round"
                >

                  <animate
                    attributeName="stroke-dashoffset"
                    from="0"
                    to="-340"
                    dur="5s"
                    repeatCount="indefinite"
                  />

                </path>


                <circle
                  cx="40"
                  cy="300"
                  r="7"
                  fill="#151B30"
                  stroke="#232B45"
                  strokeWidth="1.5"
                />


                <circle
                  cx="140"
                  cy="170"
                  r="7"
                  fill="#151B30"
                  stroke="#4FD1C5"
                  strokeWidth="1.5"
                />


                <circle
                  cx="240"
                  cy="50"
                  r="9"
                  fill="#F2A93B"
                />

              </svg>


              <div className="open-roles-waypoint intern">
                Intern
              </div>


              <div className="open-roles-waypoint engineer">
                Engineer
              </div>


              <div className="open-roles-waypoint senior">
                Senior
              </div>

            </div>

          </div>



          {/* ================================================= */}
          {/* FILTERS */}
          {/* ================================================= */}

          <div className="open-roles-filters">

            <span className="filter-label">
              Filter:
            </span>


            <button className="filter-chip active">
              All roles
            </button>


            <button className="filter-chip">
              Full time
            </button>


            <button className="filter-chip">
              Internship
            </button>


            <button className="filter-chip">
              Remote
            </button>


            <button className="filter-chip">
              Python
            </button>

          </div>

        </section>



        {/* ================================================= */}
        {/* OPEN ROLES */}
        {/* ================================================= */}

        <section
          className="open-roles-list"
          id="open-roles"
        >

          <h2>
            Open roles
          </h2>


          <div className="open-roles-subtitle">
            Three new postings this week
          </div>


          <div className="open-roles-path-line"></div>



          {/* JOB 1 */}

          <div className="open-role-row">

            <div className="open-role-dot">
              🧠
            </div>


            <div className="open-role-card">

              <div className="open-role-main">

                <span className="open-role-type">
                  Full time
                </span>


                <h3>
                  AI Engineer
                </h3>


                <div className="open-role-company">
                  Tech Solutions Pvt Ltd
                </div>


                <div className="open-role-meta">
                  📍 Bangalore · Remote
                </div>


                <div className="open-role-tags">

                  <span>
                    Python
                  </span>

                  <span>
                    Machine Learning
                  </span>

                  <span>
                    FastAPI
                  </span>

                </div>

              </div>


              <div className="open-role-side">

                <button
                  className="open-role-apply"
                  onClick={() =>
                    setShowAuthModal(true)
                  }
                >
                  Apply now
                </button>


                <span>
                  Posted 2 days ago
                </span>

              </div>

            </div>

          </div>



          {/* JOB 2 */}

          <div className="open-role-row">

            <div className="open-role-dot">
              📊
            </div>


            <div className="open-role-card">

              <div className="open-role-main">

                <span className="open-role-type internship">
                  Internship
                </span>


                <h3>
                  Machine Learning Intern
                </h3>


                <div className="open-role-company">
                  AI Labs India
                </div>


                <div className="open-role-meta">
                  📍 Kochi · Hybrid
                </div>


                <div className="open-role-tags">

                  <span>
                    Python
                  </span>

                  <span>
                    Scikit-learn
                  </span>

                  <span>
                    Data Science
                  </span>

                </div>

              </div>


              <div className="open-role-side">

                <button
                  className="open-role-apply"
                  onClick={() =>
                    setShowAuthModal(true)
                  }
                >
                  Apply now
                </button>


                <span>
                  Posted 4 days ago
                </span>

              </div>

            </div>

          </div>



          {/* JOB 3 */}

          <div className="open-role-row">

            <div className="open-role-dot">
              ⚙️
            </div>


            <div className="open-role-card">

              <div className="open-role-main">

                <span className="open-role-type">
                  Full time
                </span>


                <h3>
                  Python Developer
                </h3>


                <div className="open-role-company">
                  Zecpath Technologies
                </div>


                <div className="open-role-meta">
                  📍 Remote
                </div>


                <div className="open-role-tags">

                  <span>
                    Python
                  </span>

                  <span>
                    FastAPI
                  </span>

                  <span>
                    SQL
                  </span>

                </div>

              </div>


              <div className="open-role-side">

                <button
                  className="open-role-apply"
                  onClick={() =>
                    setShowAuthModal(true)
                  }
                >
                  Apply now
                </button>


                <span>
                  Posted 1 week ago
                </span>

              </div>

            </div>

          </div>

        </section>



        {/* ================================================= */}
        {/* AUTH MODAL FOR PUBLIC JOB PAGE */}
        {/* ================================================= */}

        {showAuthModal && (

          <AuthModal
            setShowAuthModal={
              setShowAuthModal
            }
            setRole={setRole}
            setAuthPage={setAuthPage}
          />

        )}

      </div>

    );

  }



  // ======================================================
  // LANDING PAGE
  // ======================================================

  if (
    !role &&
    !showRoleSelection
  ) {

    return (

      <div className="landing-page">


        {/* ================================================= */}
        {/* NAVIGATION */}
        {/* ================================================= */}

        <nav className="landing-nav">


          <div className="brand">

            <div className="brand-mark">
              Z
            </div>


            <div>

              <span className="brand-name">
                Zecpath
              </span>

              <span className="brand-ai">
                AI
              </span>

            </div>

          </div>



          <div className="nav-links">

            <a href="#features">
              Intelligence
            </a>

            <a href="#journey">
              Journey
            </a>

            <a href="#matching">
              Matching
            </a>

          </div>



          <div className="nav-actions">

            <button
              className="nav-login"
              onClick={() =>
                setShowAuthModal(true)
              }
            >
              Sign In
            </button>


            <button
              className="nav-cta"
              onClick={() => {

                setRole(null);

                setJobSeekerPage("jobs");

              }}
            >
              💼 Find Jobs
            </button>

          </div>

        </nav>



        {/* ================================================= */}
        {/* AUTH MODAL */}
        {/* ================================================= */}

        {showAuthModal && (

          <AuthModal
            setShowAuthModal={
              setShowAuthModal
            }
            setRole={setRole}
            setAuthPage={setAuthPage}
          />

        )}



        {/* ================================================= */}
        {/* HERO */}
        {/* ================================================= */}

        <main>

          <section className="landing-hero">


            <div className="hero-content">

              <div className="hero-badge">

                <span className="status-dot"></span>

                AI-POWERED CAREER INTELLIGENCE

              </div>


              <h1>

                Your Career.

                <br />

                <span>
                  Powered by Intelligence.
                </span>

              </h1>


              <p>

                Zecpath understands your skills, experience and career
                potential — then connects you with opportunities that
                actually match.

              </p>


              <div className="hero-actions">

                <button
                  className="primary-cta"
                  onClick={() =>
                    setShowAuthModal(true)
                  }
                >

                  Start Your Journey

                  <span>
                    →
                  </span>

                </button>

              </div>


              <div className="hero-trust">

                <div>

                  <strong>
                    AI
                  </strong>

                  <span>
                    Powered Matching
                  </span>

                </div>


                <div>

                  <strong>
                    Resume
                  </strong>

                  <span>
                    Intelligence
                  </span>

                </div>


                <div>

                  <strong>
                    Smart
                  </strong>

                  <span>
                    Screening
                  </span>

                </div>

              </div>

            </div>



            {/* AI VISUAL */}

            <div className="hero-visual">

              <div className="orbit orbit-one"></div>

              <div className="orbit orbit-two"></div>


              <div className="ai-core">

                <div className="core-glow"></div>

                <span>
                  AI
                </span>

              </div>


              <div className="match-card match-card-top">

                <span className="mini-label">
                  CAREER MATCH
                </span>

                <strong>
                  94%
                </strong>

                <span className="match-positive">
                  Strong alignment
                </span>

              </div>


              <div className="match-card match-card-left">

                <span className="mini-label">
                  SKILLS
                </span>


                <div className="skill-line">

                  <span>
                    Python
                  </span>

                  <b>
                    98%
                  </b>

                </div>


                <div className="skill-line">

                  <span>
                    Machine Learning
                  </span>

                  <b>
                    94%
                  </b>

                </div>


                <div className="skill-line">

                  <span>
                    FastAPI
                  </span>

                  <b>
                    91%
                  </b>

                </div>

              </div>


              <div className="match-card match-card-right">

                <span className="mini-label">
                  OPPORTUNITY
                </span>

                <strong>
                  AI Engineer
                </strong>

                <span>
                  3 compatible roles
                </span>

              </div>

            </div>

          </section>



          {/* ================================================= */}
          {/* INTELLIGENCE */}
          {/* ================================================= */}

          <section
            className="landing-section"
            id="features"
          >

            <div className="section-heading">

              <span className="section-label">
                THE INTELLIGENCE SUITE
              </span>


              <h2>

                More Than a Job Portal.

                <br />

                <span>
                  Your Career Intelligence Layer.
                </span>

              </h2>


              <p>

                Zecpath transforms resumes, opportunities and candidate
                information into intelligent recruitment decisions.

              </p>

            </div>


            <div className="intelligence-grid">


              <div className="intelligence-card featured">

                <div className="feature-icon">
                  ✦
                </div>

                <span className="card-number">
                  01
                </span>

                <h3>
                  Resume Intelligence
                </h3>

                <p>

                  Convert your resume into structured career information
                  including skills, experience, education and projects.

                </p>

                <div className="card-link">
                  Understand your profile →
                </div>

              </div>



              <div className="intelligence-card">

                <div className="feature-icon">
                  ⌁
                </div>

                <span className="card-number">
                  02
                </span>

                <h3>
                  Opportunity Matching
                </h3>

                <p>

                  Discover roles by comparing your career profile with
                  recruiter requirements and job descriptions.

                </p>

                <div className="card-link">
                  Find relevant opportunities →
                </div>

              </div>



              <div className="intelligence-card">

                <div className="feature-icon">
                  ◉
                </div>

                <span className="card-number">
                  03
                </span>

                <h3>
                  AI Screening
                </h3>

                <p>

                  Structured AI-powered screening helps recruiters evaluate
                  candidate responses consistently.

                </p>

                <div className="card-link">
                  Explore intelligent screening →
                </div>

              </div>



              <div className="intelligence-card">

                <div className="feature-icon">
                  ↗
                </div>

                <span className="card-number">
                  04
                </span>

                <h3>
                  Recruitment Intelligence
                </h3>

                <p>

                  Give recruiters structured candidate information,
                  screening results and shortlisting insights.

                </p>

                <div className="card-link">
                  Make better decisions →
                </div>

              </div>

            </div>

          </section>



          {/* ================================================= */}
          {/* MATCHING */}
          {/* ================================================= */}

          <section
            className="matching-section"
            id="matching"
          >

            <div className="matching-content">

              <span className="section-label">
                INTELLIGENT MATCHING
              </span>


              <h2>

                Connect the right

                <br />

                <span>
                  people with the right opportunities.
                </span>

              </h2>


              <p>

                A recruiter's requirements and a candidate's experience
                shouldn't live in separate worlds. Zecpath creates the
                connection between them.

              </p>


              <div className="matching-flow">


                <div className="flow-item">

                  <span>
                    01
                  </span>

                  <strong>
                    Candidate Profile
                  </strong>

                  <small>
                    Skills • Experience • Education
                  </small>

                </div>


                <div className="flow-line"></div>


                <div className="flow-item active">

                  <span>
                    02
                  </span>

                  <strong>
                    AI Matching
                  </strong>

                  <small>
                    Semantic compatibility analysis
                  </small>

                </div>


                <div className="flow-line"></div>


                <div className="flow-item">

                  <span>
                    03
                  </span>

                  <strong>
                    Opportunity
                  </strong>

                  <small>
                    Relevant recruiter roles
                  </small>

                </div>

              </div>

            </div>

          </section>



          {/* ================================================= */}
          {/* JOURNEY */}
          {/* ================================================= */}

          <section
            className="landing-section"
            id="journey"
          >

            <div className="section-heading">

              <span className="section-label">
                THE ZECPATH JOURNEY
              </span>


              <h2>

                From Profile

                <br />

                <span>
                  to Opportunity.
                </span>

              </h2>

            </div>


            <div className="journey-grid">


              <div className="journey-card">

                <span>
                  01
                </span>

                <h3>
                  Build Your Profile
                </h3>

                <p>

                  Upload your resume and let Zecpath understand your
                  professional profile.

                </p>

              </div>



              <div className="journey-card">

                <span>
                  02
                </span>

                <h3>
                  Discover Matches
                </h3>

                <p>

                  Explore opportunities that align with your skills and
                  experience.

                </p>

              </div>



              <div className="journey-card">

                <span>
                  03
                </span>

                <h3>
                  AI Screening
                </h3>

                <p>

                  Complete structured AI-powered screening when required.

                </p>

              </div>



              <div className="journey-card">

                <span>
                  04
                </span>

                <h3>
                  Move Forward
                </h3>

                <p>

                  Connect your profile with the next stage of the hiring
                  journey.

                </p>

              </div>

            </div>

          </section>



          {/* ================================================= */}
          {/* FINAL CTA */}
          {/* ================================================= */}

          <section className="final-cta">

            <div className="cta-glow"></div>


            <span className="section-label">
              START WITH ZECPATH
            </span>


            <h2>

              Your next opportunity

              <br />

              <span>
                starts with your profile.
              </span>

            </h2>


            <p>

              Build your profile and let intelligent matching connect
              your potential with opportunity.

            </p>


            <button
              className="primary-cta"
              onClick={() =>
                setShowAuthModal(true)
              }
            >

              Build Your Profile

              <span>
                →
              </span>

            </button>

          </section>

        </main>



        {/* ================================================= */}
        {/* FOOTER */}
        {/* ================================================= */}

        <footer className="landing-footer">


          <div className="footer-brand">

            <div className="brand">

              <div className="brand-mark">
                Z
              </div>


              <div>

                <span className="brand-name">
                  Zecpath
                </span>

                <span className="brand-ai">
                  AI
                </span>

              </div>

            </div>


            <p>
              AI-powered intelligence for the modern hiring journey.
            </p>

          </div>



          <div className="footer-links">


            <div>

              <strong>
                Platform
              </strong>

              <span>
                Career Intelligence
              </span>

              <span>
                AI Matching
              </span>

              <span>
                AI Screening
              </span>

            </div>


            <div>

              <strong>
                Company
              </strong>

              <span>
                About Zecpath
              </span>

              <span>
                Contact
              </span>

              <span>
                Privacy
              </span>

            </div>

          </div>



          <div className="footer-bottom">

            © 2026 Zecpath AI. All rights reserved.

          </div>

        </footer>

      </div>

    );

  }



  // ======================================================
  // ROLE SELECTION
  // ======================================================

  if (
    !role &&
    showRoleSelection
  ) {

    return (

      <div className="app">

        <header className="header">

          <div>

            <h1>
              Zecpath AI
            </h1>

            <p>
              AI-Powered Job Portal & Hiring Assistant
            </p>

          </div>

        </header>


        <main className="main">

          <section className="hero signup-hero">

            <span className="badge">
              WELCOME TO ZECPATH AI
            </span>

            <h2>
              Choose Your Role
            </h2>

            <p>
              Select how you want to use the Zecpath AI recruitment platform.
            </p>

          </section>


          <section className="role-container">


            {/* JOB SEEKER */}

            <button
              className="role-card"
              onClick={() => {

                setRole("jobseeker");

                setAuthPage("signup");

              }}
            >

              <div className="role-icon">
                👤
              </div>

              <h3>
                Job Seeker
              </h3>

              <p>

                Find jobs, upload your resume, apply for opportunities
                and complete AI-powered screening.

              </p>

            </button>



            {/* RECRUITER */}

            <button
              className="role-card"
              onClick={() => {

                setRole("recruiter");

                setAuthPage("signup");

              }}
            >

              <div className="role-icon">
                🏢
              </div>

              <h3>
                Recruiter
              </h3>

              <p>

                Create jobs, evaluate candidates, conduct AI screening
                and manage shortlisting.

              </p>

            </button>

          </section>


          <button
            onClick={() => {

              setShowRoleSelection(false);

            }}
          >
            ← Back to Landing Page
          </button>

        </main>

      </div>

    );

  }



  // ======================================================
  // JOB SEEKER SIGNUP
  // ======================================================

  if (
    role === "jobseeker" &&
    authPage === "signup"
  ) {

    return (

      <div className="app signup-page">


        <header className="header signup-header">

          <div>

            <h1>
              Zecpath AI
            </h1>

            <p>
              Job Seeker Account
            </p>

          </div>

        </header>


        <main className="main signup-main">

          <section className="hero">

            <span className="badge">
              JOB SEEKER
            </span>

            <h2>
              Create Your Account
            </h2>

            <p>

              Build your Zecpath profile and discover opportunities
              that match your skills and experience.

            </p>

          </section>


          <section className="upload-card">

            <h3>
              Create Job Seeker Account
            </h3>


            <input
              type="text"
              placeholder="Full Name"
            />


            <input
              type="email"
              placeholder="Email Address"
            />


            <input
              type="password"
              placeholder="Password"
            />


            <input
              type="password"
              placeholder="Confirm Password"
            />


            <button
              onClick={() => {

                setIsAuthenticated(true);

                setAuthPage(null);

              }}
            >
              Create Account
            </button>


            <p>
              Already have an account?
            </p>


            <button
              onClick={() =>
                setAuthPage("login")
              }
            >
              Sign In
            </button>

          </section>

        </main>

      </div>

    );

  }



  // ======================================================
  // LOGIN
  // ======================================================

  if (
    authPage === "login"
  ) {

    return (

      <div className="app signup-page">

        <header className="header">

          <div>

            <h1>
              Zecpath AI
            </h1>

            <p>
              Secure Account Access
            </p>

          </div>

        </header>


        <main className="main signup-main">

          <section className="hero">

            <span className="badge">
              SIGN IN
            </span>

            <h2>
              Welcome Back
            </h2>

            <p>
              Sign in to continue to your Zecpath dashboard.
            </p>

          </section>


          <section className="upload-card">

            <h3>
              Sign In
            </h3>


            <input
              type="email"
              placeholder="Email Address"
            />


            <input
              type="password"
              placeholder="Password"
            />


            <button
              onClick={() => {

                setIsAuthenticated(true);

                if (!role) {
                  setRole("jobseeker");
                }

                setAuthPage(null);

                setJobSeekerPage("dashboard");

              }}
            >
              Sign In
            </button>


            <button
              onClick={() => {

                setAuthPage("signup");

                if (!role) {
                  setRole("jobseeker");
                }

              }}
            >
              Create Account
            </button>

          </section>

        </main>

      </div>

    );

  }



  // ======================================================
  // JOB SEEKER
  // ======================================================

  if (
    role === "jobseeker"
  ) {


    // ====================================================
    // RESUME INTELLIGENCE
    // ====================================================

    if (
      jobSeekerPage === "resume"
    ) {

      return (

        <div className="app">

          <header className="header">

            <div>

              <h1>
                Zecpath AI
              </h1>

              <p>
                Job Seeker Portal
              </p>

            </div>

          </header>


          <main className="main">

            <button
              onClick={() => {

                setJobSeekerPage(
                  "dashboard"
                );

                setError("");

              }}
            >
              ← Back to Job Seeker Dashboard
            </button>


            <section className="hero">

              <span className="badge">
                AI-POWERED RECRUITMENT
              </span>

              <h2>
                Resume Intelligence
              </h2>

              <p>

                Upload your resume and let Zecpath AI
                transform it into structured recruitment data.

              </p>

            </section>


            <section className="upload-card signup-card">


              <div className="upload-icon">
                📄
              </div>


              <h3>
                Upload Your Resume
              </h3>


              <p>
                Supported formats: PDF and DOCX
              </p>


              <input
                type="file"
                accept=".pdf,.docx"
                onChange={(event) => {

                  setFile(
                    event.target.files[0]
                  );

                  setError("");

                  setCandidate(null);

                  setProfile(null);

                }}
              />


              {file && (

                <div className="selected-file">

                  Selected:{" "}

                  <strong>
                    {file.name}
                  </strong>

                </div>

              )}


              <button
                onClick={handleUpload}
                disabled={uploading}
              >

                {uploading
                  ? "Uploading..."
                  : "Upload Resume"}

              </button>


              {candidate && (

                <div className="success">

                  <h3>
                    Resume Uploaded Successfully
                  </h3>


                  <p>

                    <strong>
                      Candidate ID:
                    </strong>{" "}

                    {candidate.candidate_id}

                  </p>


                  <p>

                    <strong>
                      Filename:
                    </strong>{" "}

                    {candidate.filename}

                  </p>


                  <p>

                    <strong>
                      Status:
                    </strong>{" "}

                    {candidate.status}

                  </p>


                  <button
                    onClick={handleParse}
                    disabled={parsing}
                  >

                    {parsing
                      ? "Parsing Resume..."
                      : "Parse Resume"}

                  </button>

                </div>

              )}


              {error && (

                <div className="error">

                  {error}

                </div>

              )}

            </section>



            {/* ================================================= */}
            {/* PROFILE */}
            {/* ================================================= */}

            {profile && (

              <section className="profile-card">


                <div className="profile-header">

                  <span className="badge">
                    RESUME PARSED
                  </span>

                  <h2>
                    Candidate Profile
                  </h2>

                  <p>

                    Structured candidate information extracted
                    from your uploaded resume.

                  </p>

                </div>



                {/* BASIC INFORMATION */}

                <div className="profile-section">

                  <h3>
                    👤 Basic Information
                  </h3>


                  <div className="profile-grid">


                    <div>

                      <span>
                        Name
                      </span>

                      <strong>
                        {profile.name ||
                          "Not detected"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Email
                      </span>

                      <strong>
                        {profile.email ||
                          "Not detected"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Phone
                      </span>

                      <strong>
                        {profile.phone ||
                          "Not detected"}
                      </strong>

                    </div>


                    <div>

                      <span>
                        Location
                      </span>

                      <strong>
                        {profile.location ||
                          "Not detected"}
                      </strong>

                    </div>

                  </div>

                </div>



                {/* SUMMARY */}

                {profile.summary && (

                  <div className="profile-section">

                    <h3>
                      📝 Summary
                    </h3>

                    <p className="profile-text">
                      {profile.summary}
                    </p>

                  </div>

                )}



                {/* SKILLS */}

                <div className="profile-section">

                  <h3>
                    🛠 Skills
                  </h3>


                  <div className="tag-container">

                    {profile.skills?.length > 0
                      ? profile.skills.map(
                          (skill, index) => (

                            <span
                              className="tag"
                              key={index}
                            >
                              {skill}
                            </span>

                          )
                        )
                      : (
                        <p>
                          No skills detected.
                        </p>
                      )}

                  </div>

                </div>



                {/* EXPERIENCE */}

                <div className="profile-section">

                  <h3>
                    💼 Experience
                  </h3>


                  {profile.experience?.length > 0
                    ? (

                      <ul>

                        {profile.experience.map(
                          (item, index) => (

                            <li key={index}>

                              {typeof item ===
                              "string"
                                ? item
                                : JSON.stringify(
                                    item
                                  )}

                            </li>

                          )
                        )}

                      </ul>

                    )
                    : (

                      <p>
                        No experience detected.
                      </p>

                    )}

                </div>



                {/* EDUCATION */}

                <div className="profile-section">

                  <h3>
                    🎓 Education
                  </h3>


                  {profile.education?.length > 0
                    ? (

                      <ul>

                        {profile.education.map(
                          (item, index) => (

                            <li key={index}>

                              {typeof item ===
                              "string"
                                ? item
                                : JSON.stringify(
                                    item
                                  )}

                            </li>

                          )
                        )}

                      </ul>

                    )
                    : (

                      <p>
                        No education information detected.
                      </p>

                    )}

                </div>



                {/* PROJECTS */}

                <div className="profile-section">

                  <h3>
                    🚀 Projects
                  </h3>


                  {profile.projects?.length > 0
                    ? (

                      <ul>

                        {profile.projects.map(
                          (item, index) => (

                            <li key={index}>

                              {typeof item ===
                              "string"
                                ? item
                                : JSON.stringify(
                                    item
                                  )}

                            </li>

                          )
                        )}

                      </ul>

                    )
                    : (

                      <p>
                        No projects detected.
                      </p>

                    )}

                </div>



                {/* CERTIFICATIONS */}

                <div className="profile-section">

                  <h3>
                    🏅 Certifications
                  </h3>


                  {profile.certifications?.length > 0
                    ? (

                      <ul>

                        {profile.certifications.map(
                          (item, index) => (

                            <li key={index}>

                              {typeof item ===
                              "string"
                                ? item
                                : JSON.stringify(
                                    item
                                  )}

                            </li>

                          )
                        )}

                      </ul>

                    )
                    : (

                      <p>
                        No certifications detected.
                      </p>

                    )}

                </div>



                {/* LANGUAGES */}

                <div className="profile-section">

                  <h3>
                    🌐 Languages
                  </h3>


                  {profile.languages?.length > 0
                    ? (

                      <div className="tag-container">

                        {profile.languages.map(
                          (language, index) => (

                            <span
                              className="tag"
                              key={index}
                            >
                              {language}
                            </span>

                          )
                        )}

                      </div>

                    )
                    : (

                      <p>
                        No languages detected.
                      </p>

                    )}

                </div>

              </section>

            )}

          </main>

        </div>

      );

    }



    // ====================================================
    // AUTHENTICATED JOB SEEKER JOBS PAGE
    // ====================================================

    if (
      jobSeekerPage === "jobs"
    ) {

      return (

        <div className="app">

          <header className="header">

            <div>

              <h1>
                Zecpath AI
              </h1>

              <p>
                Find your next opportunity
              </p>

            </div>


            <button
              onClick={() =>
                setJobSeekerPage(
                  "dashboard"
                )
              }
            >
              ← Back to Home
            </button>

          </header>


          <main className="main">

            <section className="hero">

              <span className="badge">
                JOB OPPORTUNITIES
              </span>

              <h2>
                Find Your Next Job
              </h2>

              <p>

                Explore opportunities that match your skills,
                experience, and career goals.

              </p>

            </section>


            <section className="jobs-grid">


              {/* JOB 1 */}

              <div className="job-card">

                <span className="job-type">
                  FULL TIME
                </span>

                <h3>
                  AI Engineer
                </h3>

                <p className="company">
                  Tech Solutions Pvt Ltd
                </p>

                <p>
                  📍 Bangalore • Remote
                </p>


                <div className="job-skills">

                  <span>
                    Python
                  </span>

                  <span>
                    Machine Learning
                  </span>

                  <span>
                    FastAPI
                  </span>

                </div>


                <button
                  className="apply-button"
                  onClick={() =>
                    setShowAuthModal(true)
                  }
                >
                  Apply Now
                </button>

              </div>



              {/* JOB 2 */}

              <div className="job-card">

                <span className="job-type">
                  INTERNSHIP
                </span>

                <h3>
                  Machine Learning Intern
                </h3>

                <p className="company">
                  AI Labs India
                </p>

                <p>
                  📍 Kochi • Hybrid
                </p>


                <div className="job-skills">

                  <span>
                    Python
                  </span>

                  <span>
                    Scikit-learn
                  </span>

                  <span>
                    Data Science
                  </span>

                </div>


                <button
                  className="apply-button"
                  onClick={() =>
                    setShowAuthModal(true)
                  }
                >
                  Apply Now
                </button>

              </div>



              {/* JOB 3 */}

              <div className="job-card">

                <span className="job-type">
                  FULL TIME
                </span>

                <h3>
                  Python Developer
                </h3>

                <p className="company">
                  Zecpath Technologies
                </p>

                <p>
                  📍 Remote
                </p>


                <div className="job-skills">

                  <span>
                    Python
                  </span>

                  <span>
                    FastAPI
                  </span>

                  <span>
                    SQL
                  </span>

                </div>


                <button
                  className="apply-button"
                  onClick={() =>
                    setShowAuthModal(true)
                  }
                >
                  Apply Now
                </button>

              </div>

            </section>

          </main>


          {showAuthModal && (

            <AuthModal
              setShowAuthModal={
                setShowAuthModal
              }
              setRole={setRole}
              setAuthPage={setAuthPage}
            />

          )}

        </div>

      );

    }



    // ====================================================
    // JOB SEEKER DASHBOARD
    // ====================================================

    return (

      <div className="app">


        <header className="header">

          <div>

            <h1>
              Zecpath AI
            </h1>

            <p>
              Job Seeker Portal
            </p>

          </div>

        </header>


        <main className="main">


          <section className="hero">

            <span className="badge">
              JOB SEEKER
            </span>


            <h2>
              Welcome to Zecpath AI 👋
            </h2>


            <p>

              Your AI-powered career assistant for discovering opportunities
              and building your career.

            </p>

          </section>



          <section className="role-container">


            {/* RESUME */}

            <button
              className="role-card"
              onClick={() =>
                setJobSeekerPage("resume")
              }
            >

              <div className="role-icon">
                📄
              </div>

              <h3>
                Resume Profile
              </h3>

              <p>
                Upload and manage your resume and candidate profile.
              </p>

            </button>



            {/* FIND JOBS */}

            <button
              className="role-card"
              onClick={() =>
                setJobSeekerPage("jobs")
              }
            >

              <div className="role-icon">
                🔍
              </div>

              <h3>
                Find Jobs
              </h3>

              <p>
                Explore available job opportunities.
              </p>

            </button>



            {/* APPLICATIONS */}

            <button className="role-card">

              <div className="role-icon">
                📝
              </div>

              <h3>
                My Applications
              </h3>

              <p>
                Track your job applications.
              </p>

            </button>



            {/* SCREENING */}

            <button className="role-card">

              <div className="role-icon">
                🤖
              </div>

              <h3>
                AI Screening
              </h3>

              <p>
                Complete AI-powered candidate screening.
              </p>

            </button>

          </section>



          <button
            onClick={() => {

              setRole(null);

              setJobSeekerPage(
                "dashboard"
              );

              setShowRoleSelection(
                true
              );

            }}
          >
            ← Back to Role Selection
          </button>

        </main>

      </div>

    );

  }



  // ======================================================
  // RECRUITER
  // ======================================================

  if (
    role === "recruiter"
  ) {

    return (

      <div className="app">


        <header className="header">

          <div>

            <h1>
              Zecpath AI
            </h1>

            <p>
              Recruiter Portal
            </p>

          </div>

        </header>


        <main className="main">


          <section className="hero">

            <span className="badge">
              RECRUITER
            </span>


            <h2>
              Welcome to Zecpath AI 👋
            </h2>


            <p>

              Your AI-powered hiring assistant for managing jobs,
              evaluating candidates and automating recruitment.

            </p>

          </section>



          <section className="role-container">


            {/* CREATE JOBS */}

            <button className="role-card">

              <div className="role-icon">
                💼
              </div>

              <h3>
                Create Jobs
              </h3>

              <p>
                Create and manage job opportunities.
              </p>

            </button>



            {/* CANDIDATES */}

            <button className="role-card">

              <div className="role-icon">
                👥
              </div>

              <h3>
                Candidates
              </h3>

              <p>
                View and manage candidates who apply for your jobs.
              </p>

            </button>



            {/* SCREENING */}

            <button className="role-card">

              <div className="role-icon">
                🤖
              </div>

              <h3>
                AI Screening
              </h3>

              <p>
                Use AI-powered screening to evaluate candidates.
              </p>

            </button>



            {/* SHORTLISTING */}

            <button className="role-card">

              <div className="role-icon">
                📊
              </div>

              <h3>
                Shortlisting
              </h3>

              <p>
                Review candidate scores and manage shortlisting.
              </p>

            </button>

          </section>



          <button
            onClick={() => {

              setRole(null);

              setShowRoleSelection(
                true
              );

            }}
          >
            ← Back to Role Selection
          </button>

        </main>

      </div>

    );

  }



  // ======================================================
  // FALLBACK
  // ======================================================

  return null;

}


export default App;