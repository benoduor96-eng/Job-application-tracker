import React, { useEffect, useMemo, useState } from "react";
import "./ApplicationAudit.css";

const API = "/api/application-audit/";

function severityClass(value) {
  return String(value || "info").toLowerCase();
}

export default function ApplicationAudit() {
  const [data, setData] = useState(null);
  const [limit, setLimit] = useState(50);
  const [severity, setSeverity] = useState("all");
  const [category, setCategory] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(API + "?limit=" + limit);
      if (!response.ok) throw new Error("Audit request failed");
      setData(await response.json());
    } catch (err) {
      setError(err.message || "Unable to load audit");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, [limit]);

  const findings = useMemo(() => {
    if (!data) return [];
    return data.findings.filter(item => {
      const severityOk = severity === "all" || item.severity === severity;
      const categoryOk = category === "all" || item.code === category;
      return severityOk && categoryOk;
    });
  }, [data, severity, category]);

  const categories = useMemo(() => {
    if (!data) return [];
    return Object.keys(data.summary.by_category || {}).sort();
  }, [data]);

  if (loading) return <section className="audit-page"><div className="audit-empty">Loading application audit…</div></section>;
  if (error) return <section className="audit-page"><div className="audit-error">{error}<button onClick={load}>Retry</button></div></section>;

  const summary = data.summary;
  return (
    <section className="audit-page">
      <header className="audit-header">
        <div>
          <span className="audit-eyebrow">DATA QUALITY</span>
          <h1>Application Audit</h1>
          <p>Review missing, stale, inconsistent, and incomplete job-search records.</p>
        </div>
        <div className="audit-score">
          <strong>{summary.score}</strong>
          <span>health score</span>
        </div>
      </header>

      <div className="audit-stats">
        <div><strong>{summary.total_findings}</strong><span>Findings</span></div>
        <div><strong>{summary.by_severity.high || 0}</strong><span>High priority</span></div>
        <div><strong>{summary.by_severity.medium || 0}</strong><span>Medium</span></div>
        <div><strong>{summary.active_applications}</strong><span>Active applications</span></div>
        <div><strong>{summary.job_descriptions}</strong><span>Job descriptions</span></div>
        <div><strong>{summary.resumes}</strong><span>Resumes</span></div>
      </div>

      <div className="audit-controls">
        <label>Severity
          <select value={severity} onChange={e => setSeverity(e.target.value)}>
            <option value="all">All</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </label>
        <label>Category
          <select value={category} onChange={e => setCategory(e.target.value)}>
            <option value="all">All categories</option>
            {categories.map(item => <option key={item} value={item}>{item.replaceAll("_", " ")}</option>)}
          </select>
        </label>
        <label>Rows
          <select value={limit} onChange={e => setLimit(Number(e.target.value))}>
            <option value="25">25</option>
            <option value="50">50</option>
            <option value="100">100</option>
            <option value="200">200</option>
          </select>
        </label>
      </div>

      <div className="audit-grid">
        <div className="audit-panel">
          <div className="audit-panel-heading"><h2>Findings</h2><span>{findings.length}</span></div>
          {findings.length === 0 ? <div className="audit-empty">No findings match the selected filters.</div> :
            <div className="audit-list">{findings.map((item, index) => (
              <article className="audit-item" key={item.code + "-" + item.application_id + "-" + index}>
                <div className={"audit-severity " + severityClass(item.severity)}>{item.severity}</div>
                <div className="audit-item-body">
                  <h3>{item.title}</h3>
                  <p>{item.detail}</p>
                  {item.company && <small>{item.company} · {item.role}</small>}
                </div>
              </article>
            ))}</div>}
        </div>

        <div className="audit-panel">
          <div className="audit-panel-heading"><h2>Recommendations</h2></div>
          <div className="audit-recommendations">
            {data.recommendations.map((item, index) => (
              <article key={item.title + index}>
                <span className={"audit-severity " + severityClass(item.priority)}>{item.priority}</span>
                <h3>{item.title}</h3>
                <p>{item.detail}</p>
              </article>
            ))}
            {!data.recommendations.length && <div className="audit-empty">No immediate recommendations.</div>}
          </div>
        </div>
      </div>

      <div className="audit-panel">
        <div className="audit-panel-heading"><h2>Application quality</h2></div>
        <div className="audit-table-wrap">
          <table><thead><tr><th>Company</th><th>Role</th><th>Status</th><th>Score</th><th>Findings</th></tr></thead>
          <tbody>{data.applications.map(row => (
            <tr key={row.application_id}>
              <td>{row.company}</td><td>{row.role}</td><td>{row.status}</td>
              <td><strong>{row.score}</strong></td><td>{row.finding_count}</td>
            </tr>
          ))}</tbody></table>
        </div>
      </div>
    </section>
  );
}
