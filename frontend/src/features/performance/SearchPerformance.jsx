import React, { useEffect, useMemo, useState } from 'react';
import './SearchPerformance.css';

const formatDate = value => value ? new Date(value).toLocaleDateString(undefined, {month:'short', day:'numeric'}) : 'No date';

function Metric({label, value, detail}) {
  return <article className="performance-metric"><span>{label}</span><strong>{value}</strong><small>{detail}</small></article>;
}
function Bar({value, max, label, caption}) {
  const width = max ? Math.max(4, Math.round((value / max) * 100)) : 4;
  return <div className="performance-bar-row"><div className="performance-bar-label"><span>{label}</span><strong>{value}</strong></div><div className="performance-bar-track"><i style={{width: width + '%'}} /></div><small>{caption}</small></div>;
}
export default function SearchPerformance({api}) {
  const [performance, setPerformance] = useState(null), [activity, setActivity] = useState(null), [loading, setLoading] = useState(true), [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    Promise.all([api.get('/search-performance/?weeks=12'), api.get('/search-performance/activity/')])
      .then(([first, second]) => { if (active) { setPerformance(first.data); setActivity(second.data); setError(''); } })
      .catch(() => active && setError('Performance data could not be loaded.'))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [api]);
  const peak = useMemo(() => Math.max(1, ...(performance?.weekly || []).map(x => x.applications)), [performance]);
  if (loading) return <section className="performance-page"><div className="panel performance-loading">Loading search performance...</div></section>;
  if (error) return <section className="performance-page"><div className="global-error">{error}</div></section>;
  const r = performance?.responses || {};
  return <section className="performance-page">
    <div className="performance-header"><div><span className="eyebrow">SEARCH OPERATIONS</span><h1>Search performance</h1><p>Measure application pace, pipeline conversion and upcoming work.</p></div><span className="performance-period">Last {performance.period_weeks} weeks</span></div>
    <div className="performance-grid">
      <Metric label="Applications" value={r.applied} detail={r.total + ' tracked records'} />
      <Metric label="Active pipeline" value={r.active} detail="Applied through offer" />
      <Metric label="Interview rate" value={r.application_to_interview + '%'} detail="Applications to interviews" />
      <Metric label="Offer rate" value={r.application_to_offer + '%'} detail="Applications to offers" />
    </div>
    <div className="performance-columns">
      <article className="panel performance-panel"><div className="panel-heading"><div><h2>Weekly application pace</h2><span>Applications recorded by week</span></div></div><div className="weekly-bars">{performance.weekly.map(item=><div className="weekly-column" key={item.week}><div className="weekly-value">{item.applications}</div><div className="weekly-track"><i style={{height: Math.max(5, Math.round(item.applications / peak * 100)) + '%'}} /></div><small>{item.label}</small></div>)}</div></article>
      <article className="panel performance-panel"><div className="panel-heading"><div><h2>Pipeline mix</h2><span>Current status distribution</span></div></div>{performance.statuses.map(item=><Bar key={item.status} value={item.count} max={Math.max(1, r.total)} label={item.label} caption={item.share + '% of tracked applications'}/>)}</article>
    </div>
    <div className="performance-columns">
      <article className="panel performance-panel"><div className="panel-heading"><div><h2>Conversion snapshot</h2><span>Stage-to-stage movement</span></div></div><div className="conversion-list"><div><span>Application to interview</span><strong>{r.application_to_interview}%</strong></div><div><span>Application to offer</span><strong>{r.application_to_offer}%</strong></div><div><span>Interview to offer</span><strong>{r.interview_to_offer}%</strong></div></div></article>
      <article className="panel performance-panel"><div className="panel-heading"><div><h2>Next 30 days</h2><span>Scheduled work</span></div></div><div className="upcoming-list">{(activity?.upcoming_interviews || []).map(item=><div className="upcoming-item" key={'i-' + item.id}><b>Interview</b><div><strong>{item.company} · {item.role}</strong><span>{item.type} · {formatDate(item.date)}</span></div></div>)}{(activity?.upcoming_tasks || []).map(item=><div className="upcoming-item" key={'t-' + item.id}><b>Task</b><div><strong>{item.title}</strong><span>{item.company} · {formatDate(item.due)}</span></div></div>)}{!activity?.upcoming_interviews?.length && !activity?.upcoming_tasks?.length && <p className="empty-state">No upcoming interviews or tasks in the next 30 days.</p>}</div></article>
    </div>
    {activity?.next_application && <div className="panel next-action"><span className="eyebrow">NEXT APPLICATION ACTION</span><strong>{activity.next_application.company} · {activity.next_application.role}</strong><span>{activity.next_application.next_action || 'Follow up'} · {formatDate(activity.next_application.next_action_date)}</span></div>}
  </section>;
}
