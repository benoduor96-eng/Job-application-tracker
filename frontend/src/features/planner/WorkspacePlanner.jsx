import React, { useCallback, useEffect, useMemo, useState } from "react";
import "./workspacePlanner.css";

const labels = {
  saved: "Saved", applied: "Applied", screening: "Screening",
  interview: "Interview", offer: "Offer", rejected: "Rejected", withdrawn: "Withdrawn",
};

const formatDate = (value) => {
  if (!value) return "No date";
  return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric" })
    .format(new Date(value + "T00:00:00"));
};

function Stat({ label, value, detail }) {
  return <article className="planner-stat">
    <span>{label}</span><strong>{value}</strong><small>{detail}</small>
  </article>;
}

function Priority({ value }) {
  return <span className={"planner-priority planner-" + value}>{value}</span>;
}

function QueueItem({ item, onOpen }) {
  return <button className="planner-queue-item" onClick={() => onOpen && onOpen(item.id)}>
    <div>
      <div className="planner-item-title"><strong>{item.company}</strong><Priority value={item.priority}/></div>
      <span>{item.role}</span>
      <small>{item.reasons.join(" • ")}</small>
    </div>
    <aside><strong>{item.score}</strong><small>{item.next_action_date ? formatDate(item.next_action_date) : "No date"}</small></aside>
  </button>;
}

function Day({ day }) {
  return <div className="planner-day">
    <header><strong>{day.weekday.slice(0, 3)}</strong><span>{formatDate(day.date)}</span></header>
    {day.items.length ? day.items.map((item, index) =>
      <div className="planner-event" key={item.type + "-" + item.id + "-" + index}>
        <i/><div><strong>{item.title}</strong><small>{item.company || item.priority || item.type}</small></div>
      </div>
    ) : <small className="planner-none">No planned work</small>}
  </div>;
}

export default function WorkspacePlanner({ api, onOpenApplication }) {
  const [summary, setSummary] = useState(null);
  const [queue, setQueue] = useState([]);
  const [week, setWeek] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const results = await Promise.all([
        api.get("/workspace/summary/"),
        api.get("/workspace/priority/?limit=12"),
        api.get("/workspace/week/"),
        api.get("/workspace/recommendations/"),
        api.get("/workspace/companies/"),
      ]);
      setSummary(results[0].data);
      setQueue(results[1].data.items || []);
      setWeek(results[2].data);
      setRecommendations(results[3].data.recommendations || []);
      setCompanies(results[4].data.companies || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load the workspace planner.");
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => { load(); }, [load]);

  const topCompanies = useMemo(() => companies.slice(0, 6), [companies]);

  if (loading) return <div className="workspace planner-workspace"><div className="planner-loading">Loading planning workspace…</div></div>;

  return <div className="workspace planner-workspace">
    <div className="page-head">
      <div><span className="eyebrow">WORKSPACE PLANNER</span><h2>Plan the next seven days</h2>
        <p className="muted">Applications, interviews, tasks and follow-ups that need attention.</p></div>
      <button className="secondary" onClick={load}>Refresh plan</button>
    </div>

    {error && <div className="alert error">{error}</div>}

    <section className="planner-stat-grid">
      <Stat label="Active applications" value={summary?.active_applications || 0} detail={(summary?.total_applications || 0) + " total"}/>
      <Stat label="Overdue" value={summary?.attention?.overdue_followups || 0} detail="follow-ups to review"/>
      <Stat label="Interviews" value={summary?.attention?.upcoming_interviews || 0} detail="next 14 days"/>
      <Stat label="Open tasks" value={summary?.attention?.open_tasks || 0} detail={(summary?.attention?.completed_tasks || 0) + " completed"}/>
    </section>

    <div className="planner-two-column">
      <section className="panel">
        <div className="panel-head"><div><h3>Priority queue</h3><span className="muted">Ranked actions from your pipeline.</span></div><strong>{queue.length}</strong></div>
        <div>{queue.length ? queue.map(item => <QueueItem key={item.id} item={item} onOpen={onOpenApplication}/>) : <div className="empty">No priority actions.</div>}</div>
      </section>

      <section className="panel">
        <div className="panel-head"><div><h3>Conversion snapshot</h3><span className="muted">Current pipeline movement.</span></div></div>
        <div className="planner-rates">
          <div><strong>{summary?.conversion?.applied_rate || 0}%</strong><span>Applied</span></div>
          <div><strong>{summary?.conversion?.interview_rate || 0}%</strong><span>Interview</span></div>
          <div><strong>{summary?.conversion?.offer_rate || 0}%</strong><span>Offer</span></div>
        </div>
        <div className="planner-status-list">{Object.entries(summary?.status_counts || {}).map(([key, value]) =>
          <div key={key}><span>{labels[key] || key}</span><strong>{value}</strong></div>)}</div>
      </section>
    </div>

    <section className="panel">
      <div className="panel-head"><div><h3>Seven-day calendar</h3><span className="muted">{week?.total_items || 0} planned items</span></div></div>
      <div className="planner-week">{(week?.days || []).map(day => <Day key={day.date} day={day}/>)}</div>
    </section>

    <div className="planner-two-column">
      <section className="panel">
        <div className="panel-head"><div><h3>Recommended actions</h3><span className="muted">Based on your saved application data.</span></div></div>
        <div className="planner-recommendations">
          {recommendations.length ? recommendations.slice(0, 8).map((item, index) =>
            <article className="planner-recommendation" key={item.kind + "-" + index}>
              <strong>{item.title}</strong><Priority value={item.priority}/><p>{item.detail}</p>
            </article>
          ) : <div className="empty">No recommendations.</div>}
        </div>
      </section>

      <section className="panel">
        <div className="panel-head"><div><h3>Company activity</h3><span className="muted">Where your pipeline is concentrated.</span></div></div>
        <div className="planner-companies">{topCompanies.length ? topCompanies.map(company =>
          <div key={company.company}><div><strong>{company.company}</strong><small>{company.active} active · {company.interviews} interviews</small></div><strong>{company.total}</strong></div>
        ) : <div className="empty">Add applications to see company activity.</div>}</div>
      </section>
    </div>
  </div>;
}
