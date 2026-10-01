import React, { useEffect, useState } from 'react';
import './interviewPrep.css';

const formatDate = value => value ? new Date(value).toLocaleString(undefined, { month:'short', day:'numeric', hour:'numeric', minute:'2-digit' }) : 'Not scheduled';

export default function InterviewPrep({ api }) {
  const [data,setData]=useState(null);
  const [selected,setSelected]=useState(null);
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');

  const load=async()=>{
    setLoading(true); setError('');
    try{
      const response=await api.get('/interview-prep/');
      setData(response.data);
      if(response.data?.packets?.length && !selected)setSelected(response.data.packets[0].interview.id);
    }catch(e){setError(e.response?.data?.detail||'Could not load interview preparation.')}
    finally{setLoading(false)}
  };
  useEffect(()=>{load()},[]);
  if(loading)return <div className="workspace"><div className="page-head"><div><span className="eyebrow">INTERVIEW PREP</span><h2>Interview preparation</h2></div></div><div className="prep-loading"><i/><i/><i/></div></div>;
  if(error)return <div className="workspace"><div className="alert error">{error}</div><button className="primary" onClick={load}>Try again</button></div>;

  const packets=data?.packets||[];
  const current=packets.find(item=>item.interview.id===selected)||packets[0];
  return <div className="workspace interview-prep">
    <div className="page-head"><div><span className="eyebrow">INTERVIEW PREP</span><h2>Interview preparation</h2><p className="muted">Review the information already captured for each upcoming interview.</p></div><button className="secondary" onClick={load}>↻ Refresh</button></div>
    <div className="prep-summary"><Summary label="Upcoming" value={data?.summary?.interviews}/><Summary label="Prepared" value={data?.summary?.prepared}/><Summary label="Needs work" value={data?.summary?.needs_preparation}/><Summary label="Average score" value={(data?.summary?.average_score||0)+'%'}/></div>
    <div className="prep-layout">
      <aside className="prep-list">{packets.map(item=><button className={current?.interview.id===item.interview.id?'selected':''} key={item.interview.id} onClick={()=>setSelected(item.interview.id)}><div><strong>{item.application.company}</strong><span>{item.application.role}</span><small>{formatDate(item.interview.scheduled_date)}</small></div><b>{item.preparation.score}%</b></button>)}{!packets.length&&<div className="prep-empty">No upcoming interviews are scheduled.</div>}</aside>
      {current&&<main className="prep-detail">
        <section className="prep-card prep-hero"><div><span className="eyebrow">{current.interview.type}</span><h3>{current.application.company}</h3><p>{current.application.role}</p><span>{formatDate(current.interview.scheduled_date)}</span></div><div className="prep-score"><strong>{current.preparation.score}%</strong><span>prepared</span></div></section>
        <section className="prep-card"><div className="prep-card-head"><h3>Preparation checklist</h3><span>{current.preparation.checks.filter(item=>item.complete).length}/{current.preparation.checks.length} complete</span></div><div className="prep-checks">{current.preparation.checks.map(item=><div key={item.key} className={item.complete?'complete':''}><span>{item.complete?'✓':'○'}</span><strong>{item.label}</strong></div>)}</div></section>
        <section className="prep-card"><div className="prep-card-head"><h3>Interview details</h3></div><div className="detail-grid"><Detail label="Interviewer" value={current.interview.interviewer||'Not recorded'}/><Detail label="Title" value={current.interview.interviewer_title||'Not recorded'}/><Detail label="Outcome" value={current.interview.outcome}/><Detail label="Application status" value={current.application.status}/></div></section>
        <section className="prep-card"><div className="prep-card-head"><h3>What is already captured</h3></div><div className="captured-grid"><Captured label="Job description" value={current.application.company + ' · ' + current.application.role}/><Captured label="Required skills" value={(current.job_description.required_skills||[]).join(', ')||'None recorded'}/><Captured label="Preferred skills" value={(current.job_description.preferred_skills||[]).join(', ')||'None recorded'}/><Captured label="Responsibilities" value={(current.job_description.responsibilities||[]).join(' · ')||'None recorded'}/></div></section>
      </main>}
    </div>
  </div>;
}
function Summary({label,value}){return <div className="prep-summary-card"><span>{label}</span><strong>{value}</strong></div>}
function Detail({label,value}){return <div><span>{label}</span><strong>{value}</strong></div>}
function Captured({label,value}){return <div><span>{label}</span><p>{value}</p></div>}
