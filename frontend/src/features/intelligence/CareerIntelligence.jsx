import React, { useEffect, useMemo, useState } from "react";
import {
  formatScore,
  generateFollowUps,
  getCareerSummary,
  getPipelinePriority,
  matchSkills,
  previewJobDescription,
  scoreTone,
} from "./intelligenceApi";

const EMPTY_MATCH = {
  score: null,
  required_score: null,
  preferred_score: null,
  profile_score: null,
  salary_score: null,
  location_score: null,
  matched_required: [],
  missing_required: [],
  matched_preferred: [],
  recommendations: [],
};

function Metric({ label, value, hint }) {
  return (
    <article className="intelligence-metric">
      <span className="intelligence-metric-label">{label}</span>
      <strong className="intelligence-metric-value">{value}</strong>
      {hint && <small>{hint}</small>}
    </article>
  );
}

function SkillList({ title, items, empty = "None identified" }) {
  return (
    <section className="skill-list">
      <h4>{title}</h4>
      {items.length ? (
        <div className="skill-chips">
          {items.map((item) => (
            <span className="skill-chip" key={item}>{item}</span>
          ))}
        </div>
      ) : (
        <p className="muted">{empty}</p>
      )}
    </section>
  );
}

export default function CareerIntelligence() {
  const [summary, setSummary] = useState(null);
  const [priority, setPriority] = useState([]);
  const [description, setDescription] = useState("");
  const [preview, setPreview] = useState(null);
  const [match, setMatch] = useState(EMPTY_MATCH);
  const [requiredSkills, setRequiredSkills] = useState("");
  const [preferredSkills, setPreferredSkills] = useState("");
  const [role, setRole] = useState("");
  const [location, setLocation] = useState("");
  const [salaryMin, setSalaryMin] = useState("");
  const [salaryMax, setSalaryMax] = useState("");
  const [loading, setLoading] = useState(false);
  const [followUpResult, setFollowUpResult] = useState(null);
  const [error, setError] = useState("");

  async function loadDashboard() {
    setError("");
    try {
      const [summaryData, priorityData] = await Promise.all([
        getCareerSummary(),
        getPipelinePriority(),
      ]);
      setSummary(summaryData);
      setPriority(priorityData);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load career intelligence.");
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  const topPriority = useMemo(() => priority.slice(0, 5), [priority]);

  async function handlePreview(event) {
    event.preventDefault();
    if (description.trim().length < 20) {
      setError("Paste at least 20 characters of a job description.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const data = await previewJobDescription(description);
      setPreview(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not analyze the description.");
    } finally {
      setLoading(false);
    }
  }

  async function handleMatch(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await matchSkills({
        required_skills: requiredSkills
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        preferred_skills: preferredSkills
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        role,
        location,
        salary_min: salaryMin || null,
        salary_max: salaryMax || null,
      });
      setMatch(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not calculate the match.");
    } finally {
      setLoading(false);
    }
  }

  async function handleFollowUps(create) {
    setLoading(true);
    setError("");
    try {
      const data = await generateFollowUps([], create);
      setFollowUpResult(data);
      await loadDashboard();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not generate follow-ups.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="career-intelligence">
      <div className="intelligence-heading">
        <div>
          <p className="eyebrow">Career intelligence</p>
          <h2>Turn your job-search data into actionable work</h2>
          <p className="muted">
            Analyze job descriptions, compare requirements with your profile,
            and keep follow-ups visible.
          </p>
        </div>
        <button className="btn-secondary" onClick={loadDashboard} disabled={loading}>
          Refresh
        </button>
      </div>

      {error && <div className="intelligence-error" role="alert">{error}</div>}

      {summary && (
        <div className="intelligence-metrics">
          <Metric label="Applications" value={summary.total_applications} />
          <Metric label="Active pipeline" value={summary.active_applications} />
          <Metric label="Priority items" value={summary.priority_items.length} />
          <Metric
            label="Interview stage"
            value={summary.status_counts?.interview || 0}
            hint="Current pipeline"
          />
        </div>
      )}

      <div className="intelligence-grid">
        <article className="intelligence-panel">
          <div className="panel-heading">
            <div>
              <h3>Job description analyzer</h3>
              <p className="muted">Extract common technical and professional skills.</p>
            </div>
          </div>
          <form onSubmit={handlePreview}>
            <textarea
              className="intelligence-textarea"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Paste a job description here..."
              rows={9}
            />
            <div className="panel-actions">
              <button className="btn-primary" disabled={loading}>
                {loading ? "Analyzing..." : "Analyze description"}
              </button>
            </div>
          </form>
          {preview && (
            <div className="analysis-result">
              <div className="analysis-counts">
                <Metric label="Skills" value={preview.skill_count} />
                <Metric label="Keywords" value={preview.keyword_count} />
              </div>
              <SkillList title="Detected skills" items={preview.skills} />
              <SkillList title="Keywords" items={preview.keywords.slice(0, 20)} />
            </div>
          )}
        </article>

        <article className="intelligence-panel">
          <div className="panel-heading">
            <div>
              <h3>Candidate match</h3>
              <p className="muted">Compare a role against your saved career profile.</p>
            </div>
          </div>
          <form onSubmit={handleMatch} className="match-form">
            <label>
              Role
              <input value={role} onChange={(event) => setRole(event.target.value)} placeholder="Backend Engineer" />
            </label>
            <label>
              Location
              <input value={location} onChange={(event) => setLocation(event.target.value)} placeholder="Remote / Nairobi" />
            </label>
            <label>
              Required skills
              <input value={requiredSkills} onChange={(event) => setRequiredSkills(event.target.value)} placeholder="Python, Django, PostgreSQL" />
            </label>
            <label>
              Preferred skills
              <input value={preferredSkills} onChange={(event) => setPreferredSkills(event.target.value)} placeholder="Docker, AWS, Redis" />
            </label>
            <div className="form-row">
              <label>
                Minimum salary
                <input type="number" value={salaryMin} onChange={(event) => setSalaryMin(event.target.value)} />
              </label>
              <label>
                Maximum salary
                <input type="number" value={salaryMax} onChange={(event) => setSalaryMax(event.target.value)} />
              </label>
            </div>
            <button className="btn-primary" disabled={loading}>Calculate match</button>
          </form>

          {match.score !== null && (
            <div className={`match-result ${scoreTone(match.score)}`}>
              <div className="match-score">
                <span>Overall match</span>
                <strong>{formatScore(match.score)}</strong>
              </div>
              <div className="match-breakdown">
                <Metric label="Required" value={formatScore(match.required_score)} />
                <Metric label="Preferred" value={formatScore(match.preferred_score)} />
                <Metric label="Profile" value={formatScore(match.profile_score)} />
                <Metric label="Salary" value={formatScore(match.salary_score)} />
                <Metric label="Location" value={formatScore(match.location_score)} />
              </div>
              <SkillList title="Matched required skills" items={match.matched_required} />
              <SkillList title="Missing required skills" items={match.missing_required} />
              <SkillList title="Recommendations" items={match.recommendations} />
            </div>
          )}
        </article>
      </div>

      <div className="intelligence-grid lower-grid">
        <article className="intelligence-panel">
          <div className="panel-heading">
            <div>
              <h3>Pipeline priority</h3>
              <p className="muted">A transparent action score based on application state and due dates.</p>
            </div>
          </div>
          {topPriority.length ? (
            <div className="priority-list">
              {topPriority.map((item) => (
                <div className="priority-item" key={item.application_id}>
                  <div>
                    <strong>Application #{item.application_id}</strong>
                    <small>{item.reasons.join(" · ")}</small>
                  </div>
                  <span className={`priority-badge ${item.urgency}`}>
                    {item.urgency} · {item.score}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">No active applications to prioritize.</p>
          )}
        </article>

        <article className="intelligence-panel">
          <div className="panel-heading">
            <div>
              <h3>Follow-up planner</h3>
              <p className="muted">Generate suggested next actions from the current pipeline.</p>
            </div>
          </div>
          <div className="panel-actions">
            <button className="btn-secondary" onClick={() => handleFollowUps(false)} disabled={loading}>
              Preview follow-ups
            </button>
            <button className="btn-primary" onClick={() => handleFollowUps(true)} disabled={loading}>
              Create tasks
            </button>
          </div>
          {followUpResult && (
            <div className="follow-up-result">
              <strong>{followUpResult.plans.length} follow-up plan(s)</strong>
              <span>{followUpResult.created} task(s) created.</span>
              {followUpResult.plans.slice(0, 6).map((plan) => (
                <div key={`${plan.application_id}-${plan.action}`} className="follow-up-row">
                  <span>{plan.action}</span>
                  <small>{plan.due_date} · {plan.priority}</small>
                </div>
              ))}
            </div>
          )}
        </article>
      </div>
    </section>
  );
}
