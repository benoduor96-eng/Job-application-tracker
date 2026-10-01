import React,{useEffect,useState} from 'react';

export default function ContactIntelligence({api}){
 const [data,setData]=useState(null),[loading,setLoading]=useState(true),[error,setError]=useState('');
 const load=async()=>{try{setLoading(true);const r=await api.get('/contacts/intelligence/');setData(r.data);setError('')}catch(e){setError('Contact intelligence could not be loaded.')}finally{setLoading(false)}};
 useEffect(()=>{load()},[]);
 if(loading)return <div className="workspace"><div className="panel">Loading networking workspace…</div></div>;
 if(error)return <div className="workspace"><div className="alert error">{error}</div></div>;
 const typeLabels={recruiter:'Recruiters',hiring_manager:'Hiring managers',referral:'Referrals',interviewer:'Interviewers',career_coach:'Career coaches',other:'Other'};
 return <div className="workspace">
  <div className="page-head"><div><span className="eyebrow">NETWORK</span><h2>Contact intelligence</h2><p className="muted">Track recruiter and professional relationships alongside your application pipeline.</p></div><button className="secondary" onClick={load}>Refresh</button></div>
  <div className="metric-grid">
   <div className="metric"><span className="metric-icon">◎</span><div><span>Total contacts</span><strong>{data?.total||0}</strong></div></div>
   <div className="metric"><span className="metric-icon">!</span><div><span>Overdue follow-ups</span><strong>{data?.overdue||0}</strong></div></div>
   <div className="metric"><span className="metric-icon">◷</span><div><span>Next 7 days</span><strong>{data?.upcoming||0}</strong></div></div>
   <div className="metric"><span className="metric-icon">↗</span><div><span>Linked to applications</span><strong>{data?.linked_to_application||0}</strong></div></div>
  </div>
  <div className="two-col">
   <section className="panel"><div className="panel-head"><h3>Action queue</h3><span className="muted">{data?.never_contacted||0} never contacted</span></div>
    <div className="contact-actions">{(data?.actions||[]).map(item=><div className="contact-action" key={item.contact_id+'-'+item.action}><div><strong>{item.name}</strong><span>{item.company||'No company'} · {item.action}</span><small>{item.reason}</small></div><b data-priority={item.priority}>{item.priority}</b></div>)}{!data?.actions?.length&&<div className="empty">No networking actions need attention.</div>}</div>
   </section>
   <section className="panel"><div className="panel-head"><h3>Network mix</h3></div>
    <div className="contact-types">{Object.entries(data?.by_type||{}).map(([type,count])=><div className="contact-type" key={type}><span>{typeLabels[type]||type.replaceAll('_',' ')}</span><strong>{count}</strong></div>)}</div>
    <div className="panel-head contact-company-head"><h3>Top companies</h3></div>
    <div className="contact-types">{Object.entries(data?.by_company||{}).map(([company,count])=><div className="contact-type" key={company}><span>{company}</span><strong>{count}</strong></div>)}</div>
   </section>
  </div>
 </div>;
}
