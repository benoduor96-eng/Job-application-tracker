import React, { useEffect, useMemo, useState } from 'react';
import './timeline.css';

const dateTime=value=>value?new Date(value).toLocaleString(undefined,{month:'short',day:'numeric',hour:'numeric',minute:'2-digit'}):'—';
const pretty=value=>String(value||'').replaceAll('_',' ');

export default function ApplicationTimeline({api}){
  const [data,setData]=useState(null);
  const [kind,setKind]=useState('all');
  const [source,setSource]=useState('all');
  const [selected,setSelected]=useState('all');
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');

  const load=async()=>{
    setLoading(true);setError('');
    try{const r=await api.get('/timeline/dashboard/');setData(r.data)}
    catch(e){setError(e.response?.data?.detail||'Could not load application timeline.')}
    finally{setLoading(false)}
  };
  useEffect(()=>{load()},[]);
  const events=useMemo(()=>{
    let rows=data?.events||[];
    if(kind!=='all')rows=rows.filter(item=>item.kind===kind);
    if(source!=='all')rows=rows.filter(item=>item.source===source);
    if(selected!=='all')rows=rows.filter(item=>String(item.application_id)===String(selected));
    return rows;
  },[data,kind,source,selected]);

  if(loading)return <div className="workspace"><div className="page-head"><div><span className="eyebrow">TIMELINE</span><h2>Application timeline</h2></div></div><div className="timeline-loading"><i/><i/><i/></div></div>;
  if(error)return <div className="workspace"><div className="alert error">{error}</div><button className="primary" onClick={load}>Try again</button></div>;

  return <div className="workspace timeline-workspace">
    <div className="page-head"><div><span className="eyebrow">TIMELINE</span><h2>Application timeline</h2><p className="muted">Follow the recorded history of your applications, interviews, tasks and outreach.</p></div><button className="secondary" onClick={load}>↻ Refresh</button></div>
    <div className="timeline-metrics"><Metric label="Events" value={data?.counts?.total}/><Metric label="Activities" value={data?.counts?.by_source?.activity}/><Metric label="Interviews" value={data?.counts?.by_source?.interview}/><Metric label="Tasks" value={data?.counts?.by_source?.task}/></div>
    <div className="timeline-toolbar"><select value={selected} onChange={e=>setSelected(e.target.value)}><option value="all">All applications</option>{(data?.applications||[]).map(item=><option key={item.application_id} value={item.application_id}>{item.company} · {item.role}</option>)}</select><select value={source} onChange={e=>setSource(e.target.value)}><option value="all">All sources</option><option value="application">Application</option><option value="activity">Activity</option><option value="interview">Interview</option><option value="task">Task</option></select><select value={kind} onChange={e=>setKind(e.target.value)}><option value="all">All event types</option>{Object.keys(data?.counts?.by_kind||{}).map(item=><option key={item} value={item}>{pretty(item)}</option>)}</select><span>{events.length} shown</span></div>
    <section className="timeline-panel"><div className="timeline-list">{events.map(item=><article className="timeline-item" key={item.id}><div className="timeline-marker" data-source={item.source}/><div className="timeline-content"><div className="timeline-meta"><span>{dateTime(item.occurred_at)}</span><em>{pretty(item.source)}</em></div><h3>{item.title}</h3><p>{item.description||'No additional details recorded.'}</p><small>{item.company} · {item.role}</small></div></article>)}{!events.length&&<div className="timeline-empty">No events match the selected filters.</div>}</div></section>
  </div>;
}
function Metric({label,value}){return <div className="timeline-metric"><span>{label}</span><strong>{value||0}</strong></div>}
