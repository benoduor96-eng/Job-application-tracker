import React, { useEffect, useMemo, useState } from 'react';
import './searchInsights.css';

const pretty = value => String(value || '').replaceAll('_', ' ');
const pct = value => Number(value || 0).toFixed(1) + '%';

export default function SearchInsights({ api }) {
  const [data, setData] = useState(null);
  const [tab, setTab] = useState('searches');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await api.get('/search-insights/');
      setData(response.data);
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not load saved search insights.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const activeRecommendations = useMemo(() => data?.recommendations || [], [data]);
  if (loading) return <div className="workspace"><div className="page-head"><div><span className="eyebrow">SEARCH INSIGHTS</span><h2>Search intelligence</h2></div></div><div className="search-loading"><i/><i/><i/></div></div>;
  if (error) return <div className="workspace"><div className="alert error">{error}</div><button className="primary" onClick={load}>Try again</button></div>;

  const coverage = data.coverage || {};
  return <div className="workspace search-insights">
    <div className="page-head"><div><span className="eyebrow">SEARCH INSIGHTS</span><h2>Search intelligence</h2><p className="muted">See how saved-search preferences connect with the applications in your pipeline.</p></div><button className="secondary" onClick={load}>↻ Refresh</button></div>
    <div className="search-summary-grid">
      <Stat label="Saved searches" value={coverage.saved_searches}/>
      <Stat label="Applications" value={coverage.applications}/>
      <Stat label="Covered" value={coverage.covered_applications}/>
      <Stat label="Coverage" value={pct(coverage.coverage_rate)}/>
    </div>
    <div className="search-tabs">{[['searches','Saved searches'],['roles','Role clusters'],['locations','Locations'],['recommendations','Recommendations']].map(([id,label]) => <button key={id} className={tab === id ? 'active' : ''} onClick={() => setTab(id)}>{label}</button>)}</div>

    {tab === 'searches' && <section className="search-panel"><div className="search-panel-head"><div><h3>Saved search coverage</h3><p>Tracked applications matching each saved-search definition.</p></div></div><div className="saved-search-list">{(data.searches || []).map(item => <div className="saved-search-row" key={item.id}><div className="search-name"><strong>{item.name}</strong><span>{item.query || 'Any role'}{item.location ? ' · ' + item.location : ''}</span></div><div className="search-filters">{item.min_salary && <span>Min {item.min_salary}</span>}{item.max_salary && <span>Max {item.max_salary}</span>}{item.status && <span>{pretty(item.status)}</span>}</div><div className="search-count"><strong>{item.applications}</strong><span>matches</span></div><div className="search-count"><strong>{item.active_applications}</strong><span>active</span></div></div>)}{!data.searches?.length && <Empty text="Create a saved search to see coverage here."/>}</div></section>}

    {tab === 'roles' && <ClusterList title="Role clusters" rows={data.role_clusters || []} labelKey="role_key"/>}
    {tab === 'locations' && <ClusterList title="Location clusters" rows={data.location_clusters || []} labelKey="location"/>}
    {tab === 'recommendations' && <section className="search-panel"><div className="recommendation-list">{activeRecommendations.map((item,index) => <div className="recommendation-row" key={item.type + '-' + (item.search_id || index)}><span className="recommendation-priority" data-priority={item.priority}>{item.priority}</span><div><strong>{item.title}</strong><p>{item.detail}</p></div></div>)}{!activeRecommendations.length && <Empty text="No search recommendations right now."/>}</div></section>}
  </div>;
}

function Stat({ label, value }) { return <div className="search-stat"><span>{label}</span><strong>{value}</strong></div>; }
function Empty({ text }) { return <div className="search-empty">{text}</div>; }
function ClusterList({ title, rows, labelKey }) {
  return <section className="search-panel"><div className="search-panel-head"><div><h3>{title}</h3><p>Patterns found in your tracked applications.</p></div></div><div className="cluster-list">{rows.map(row => <div className="cluster-row" key={row[labelKey]}><div><strong>{row[labelKey]}</strong>{row.companies && <span>{row.companies.join(' · ')}</span>}</div><div><strong>{row.applications}</strong><span>applications</span></div><div><strong>{row.active}</strong><span>active</span></div></div>)}{!rows.length && <Empty text="No application patterns yet."/>}</div></section>;
}
