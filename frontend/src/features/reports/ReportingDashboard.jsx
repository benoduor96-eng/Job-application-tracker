import React, { useEffect, useState } from "react";
import {
  createFollowUpSequence,
  getFollowUpSequence,
  getInterviewPreparation,
  getReportingDashboard,
  percentage,
} from "./reportingApi";

function Stat({ label, value }) {
  return (
    <div className="report-stat">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default function ReportingDashboard({ applicationId }) {
  const [report, setReport] = useState(null);
  const [interview, setInterview] = useState(null);
  const [sequence, setSequence] = useState(null);
  const [error, setError] = useState("");

  async function refresh() {
    try {
      setError("");
      const dashboard = await getReportingDashboard();
      setReport(dashboard);
      if (applicationId) {
        const [prep, followUp] = await Promise.all([
          getInterviewPreparation(applicationId),
          getFollowUpSequence(applicationId),
        ]);
        setInterview(prep);
        setSequence(followUp);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load reports.");
    }
  }

  useEffect(() => {
    refresh();
  }, [applicationId]);

  async function generateSequence() {
    try {
      await createFollowUpSequence(applicationId);
      setSequence(await getFollowUpSequence(applicationId));
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to create follow-ups.");
    }
  }

  if (error) return <div className="intelligence-error">{error}</div>;
  if (!report) return <div className="reporting-dashboard"><p>Loading reports...</p></div>;

  const funnel = report.funnel || {};
  const salary = report.salary || {};

  return (
    <section className="reporting-dashboard">
      <div className="intelligence-heading">
        <div>
          <p className="eyebrow">Reporting</p>
          <h2>Application performance</h2>
          <p className="muted">Understand pipeline movement and work that needs attention.</p>
        </div>
        <button className="btn-secondary" onClick={refresh}>Refresh reports</button>
      </div>

      <div className="report-stats">
        <Stat label="Applications" value={report.status.total} />
        <Stat label="Interview rate" value={percentage(funnel.interview_rate)} />
        <Stat label="Offer rate" value={percentage(funnel.offer_rate)} />
        <Stat label="Stale applications" value={report.stale.length} />
      </div>

      <div className="report-grid">
        <article className="intelligence-panel">
          <h3>Pipeline funnel</h3>
          <div className="funnel-rows">
            {[
              ["Saved", funnel.saved],
              ["Applied", funnel.applied],
              ["Interview", funnel.interview],
              ["Offer", funnel.offer],
            ].map(([label, value]) => (
              <div className="funnel-row" key={label}>
                <span>{label}</span>
                <strong>{value}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="intelligence-panel">
          <h3>Salary snapshot</h3>
          <div className="report-stats compact">
            <Stat label="Minimum" value={salary.minimum ?? "—"} />
            <Stat label="Maximum" value={salary.maximum ?? "—"} />
            <Stat label="Average min" value={salary.average_min?.toFixed?.(0) ?? "—"} />
            <Stat label="Average max" value={salary.average_max?.toFixed?.(0) ?? "—"} />
          </div>
        </article>

        <article className="intelligence-panel">
          <h3>Companies</h3>
          <div className="company-report">
            {report.companies.slice(0, 10).map((item) => (
              <div className="company-row" key={item.company}>
                <span>{item.company}</span>
                <strong>{item.applications}</strong>
              </div>
            ))}
          </div>
        </article>

        <article className="intelligence-panel">
          <h3>Stale pipeline</h3>
          {report.stale.length ? (
            <div className="company-report">
              {report.stale.slice(0, 10).map((item) => (
                <div className="company-row" key={item.id}>
                  <span>{item.company} · {item.role}</span>
                  <strong>{item.status}</strong>
                </div>
              ))}
            </div>
          ) : (
            <p className="muted">No stale applications detected.</p>
          )}
        </article>
      </div>

      {applicationId && (
        <div className="report-grid">
          <article className="intelligence-panel">
            <h3>Interview preparation</h3>
            {interview ? (
              <>
                <div className="report-stats compact">
                  <Stat label="Questions" value={interview.readiness.question_count} />
                  <Stat label="Interviews" value={interview.readiness.interview_count} />
                  <Stat label="Completed" value={interview.readiness.completed_count} />
                </div>
                <div className="question-list">
                  {interview.questions.slice(0, 8).map((item) => (
                    <div className="question-card" key={item.question}>
                      <strong>{item.category}</strong>
                      <p>{item.question}</p>
                      <small>{item.preparation_hint}</small>
                    </div>
                  ))}
                </div>
              </>
            ) : <p>Loading preparation...</p>}
          </article>

          <article className="intelligence-panel">
            <h3>Follow-up sequence</h3>
            {sequence && (
              <>
                <p className="muted">
                  {sequence.summary.open} open · {sequence.summary.completed} completed
                </p>
                <div className="question-list">
                  {sequence.plan.map((item) => (
                    <div className="question-card" key={item.title}>
                      <strong>{item.title}</strong>
                      <p>{item.reason}</p>
                      <small>{item.due_date} · {item.priority}</small>
                    </div>
                  ))}
                </div>
                <button className="btn-primary" onClick={generateSequence}>
                  Create sequence tasks
                </button>
              </>
            )}
          </article>
        </div>
      )}
    </section>
  );
}
