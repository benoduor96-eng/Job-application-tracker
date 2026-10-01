import React, { useEffect, useMemo, useState } from 'react';
import './review.css';

const formatDate = value => value ? new Date(value).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : '—';
const number = value => new Intl.NumberFormat().format(value || 0);

function Metric({ label, value, detail }) {
  return <div className="review-metric"><span>{label}</span><strong>{number(value)}</strong>{detail && <small>{detail}</small>}</div>;
}
function Section({ title, subtitle, children, action }) {
  return <section className="review-section"><div className="review-section-head"><div><h3>{title}</h3>{subtitle && <p>{subtitle}</p>}</div>{action}</div>{children}</section>;
}
function Empty({ text }) { return <div className="review-empty">{text}</div>; }

export default function ReviewWorkspace({ api }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [tab, setTab] = useState('overview');
  const [limit, setLimit] = useState(20);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.get('/review/workspace/');
      setData(response.data);
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not load the review workspace.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const actions = useMemo(() => data?.action_queue || [], [data]);
  if (loading) return <div className="workspace"><div className="page-head"><div><span className="eyebrow">WEEKLY REVIEW</span><h2>Career review</h2></div></div><div className="review-loading"><span/><span/><span/></div></div>;
  if (error) return <div className="workspace"><div className="alert error">{error}</div><button className="primary" onClick={load}>Try again</button></div>;

  const overview = data.overview || {};
  const totals = overview.totals || {};
  const attention = overview.attention || {};
  const funnel = data.funnel || {};
  const health = data.contact_health || {};
  const task = data.task_health || {};

  return <div className="workspace review-workspace">
    <div className="page-head">
      <div><span className="eyebrow">WEEKLY REVIEW</span><h2>Career review</h2><p className="muted">A practical review of what needs attention across your job search.</p></div>
      <button className="secondary" onClick={load}>↻ Refresh review</button>
    </div>
    <div className="review-tabs">
      {[['overview','Overview'],['actions','Action queue'],['funnel','Funnel'],['companies','Companies'],['calendar','Interviews']].map(([id,label]) => <button className={tab === id ? 'active' : ''} key={id} onClick={() => setTab(id)}>{label}</button>)}
    </div>

    {tab === 'overview' && <>
      <div className="review-metrics">
        <Metric label="Applications" value={totals.applications}/><Metric label="Active pipeline" value={totals.active}/>
        <Metric label="Due today" value={attention.due_today}/><Metric label="Overdue" value={attention.overdue_followups}/>
        <Metric label="Interviews" value={totals.interviews_next_14_days}/><Metric label="Open tasks" value={totals.open_tasks}/>
      </div>
      <div className="review-columns">
        <Section title="Momentum" subtitle="Last seven days compared with the prior week">
          <div className="momentum-grid">
            <div><span>Applications</span><strong>{number(overview.momentum?.applications_this_week)}</strong><small>{overview.momentum?.application_change > 0 ? '+' : ''}{overview.momentum?.application_change || 0} vs prior week</small></div>
            <div><span>Activities</span><strong>{number(overview.momentum?.activities_this_week)}</strong><small>{overview.momentum?.activity_change > 0 ? '+' : ''}{overview.momentum?.activity_change || 0} vs prior week</small></div>
            <div><span>Direction</span><strong className="capitalize">{overview.momentum?.direction || 'steady'}</strong></div>
          </div>
        </Section>
        <Section title="Attention" subtitle="Items that can slow down the pipeline">
          <div className="attention-list"><Attention label="Overdue follow-ups" value={attention.overdue_followups}/><Attention label="Applications due today" value={attention.due_today}/><Attention label="Missing next action" value={attention.applications_without_next_action}/><Attention label="No notes" value={attention.applications_without_notes}/></div>
        </Section>
      </div>
      <div className="review-columns">
        <Section title="Contact health"><HealthRows data={health} labels={{total:'Total contacts',never_contacted:'Never contacted',stale:'Stale contacts',overdue_followups:'Overdue follow-ups',with_application:'Linked to applications'}}/></Section>
        <Section title="Task health"><HealthRows data={task} labels={{total:'Total tasks',open:'Open tasks',overdue:'Overdue',completed:'Completed',cancelled:'Cancelled'}}/></Section>
      </div>
    </>}

    {tab === 'actions' && <Section title="Action queue" subtitle="Prioritized from dates, status, age and open tasks." action={<select value={limit} onChange={e => setLimit(Number(e.target.value))}><option value="10">10 items</option><option value="20">20 items</option><option value="30">30 items</option></select>}><ActionList actions={actions.slice(0, limit)}/></Section>}

    {tab === 'funnel' && <div className="review-columns">
      <Section title="Pipeline funnel"><div className="funnel-list">{[['saved','Saved'],['applied','Applied'],['screening','Screening'],['interview','Interview'],['offer','Offer']].map(([key,label]) => {
        const width = Math.max(funnel[key] ? 4 : 0, Math.min(100, (funnel[key] || 0) / (funnel.applied || 1) * 100));
        return <div className="funnel-row" key={key}><span>{label}</span><strong>{number(funnel[key])}</strong><div><i style={{width: width + '%'}}/></div></div>;
      })}</div></Section>
      <Section title="Conversion rates"><div className="rate-list">{Object.entries(funnel.conversion_rates || {}).map(([key,value]) => <div key={key}><span>{key.replaceAll('_',' ')}</span><strong>{value}%</strong></div>)}</div></Section>
    </div>}

    {tab === 'companies' && <Section title="Company activity" subtitle="Repeated applications and follow-up load by company.">
      <div className="company-list">{(data.companies || []).map(company => <div className="company-row" key={company.company}><div><strong>{company.company}</strong><span>{company.roles.join(' · ')}</span></div><div className="company-stats"><span>{company.applications} applications</span><span>{company.active} active</span><span>{company.follow_ups_due} due</span></div></div>)}{!data.companies?.length && <Empty text="No companies yet."/>}</div>
    </Section>}

    {tab === 'calendar' && <Section title="Upcoming interviews" subtitle="Scheduled interviews from the next 30 days.">
      <div className="interview-list">{(data.interviews || []).map(item => <div className="interview-row" key={item.id}><div className="date-block"><strong>{formatDate(item.scheduled_date)}</strong><span>{item.type}</span></div><div><strong>{item.company}</strong><span>{item.role}</span><small>{item.interviewer || 'Interviewer not recorded'}</small></div><span className="badge" data-status={item.outcome}>{item.outcome}</span></div>)}{!data.interviews?.length && <Empty text="No upcoming interviews in this window."/>}</div>
    </Section>}
  </div>;
}

function Attention({ label, value }) { return <div><span>{label}</span><strong>{number(value)}</strong></div>; }
function HealthRows({ data, labels }) { return <div className="health-rows">{Object.entries(labels).map(([key,label]) => <div key={key}><span>{label}</span><strong>{number(data[key])}</strong></div>)}</div>; }
function ActionList({ actions }) {
  if (!actions.length) return <Empty text="Nothing urgent is waiting. Keep the pipeline moving." />;
  return <div className="action-list">{actions.map((item,index) => <div className="action-row" key={item.kind + '-' + (item.application_id || item.task_id) + '-' + index}>
    <div className="priority" data-level={item.priority >= 90 ? 'high' : item.priority >= 60 ? 'medium' : 'low'}>{item.priority}</div>
    <div className="action-main"><strong>{item.title}</strong><span>{item.company || item.description || 'Career task'}{item.role ? ' · ' + item.role : ''}</span></div>
    <div className="action-meta"><span>{item.kind.replaceAll('_',' ')}</span><small>{formatDate(item.due_date)}</small></div>
  </div>)}</div>;
}
