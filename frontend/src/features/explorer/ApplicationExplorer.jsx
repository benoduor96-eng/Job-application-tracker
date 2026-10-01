import React,{useEffect,useState} from 'react';
import './applicationExplorer.css';

export default function ApplicationExplorer({api}){
  const [data,setData]=useState(null),[q,setQ]=useState(''),[status,setStatus]=useState(''),[active,setActive]=useState(false),[salary,setSalary]=useState(false),[loading,setLoading]=useState(true);
  const load=async()=>{
    setLoading(true);
    const params=new URLSearchParams();
    if(q)params.set('q',q);if(status)params.set('status',status);if(active)params.set('active','true');if(salary)params.set('salary','true');
    try{const r=await api.get('/applications/explorer/?'+params.toString());setData(r.data)}finally{setLoading(false)}
  };
  useEffect(()=>{load()},[q,status,active,salary]);
  return <div className="workspace application-explorer"><div className="page-head"><div><span className="eyebrow">EXPLORER</span><h2>Application explorer</h2><p className="muted">Combine search, status, activity and salary filters across your own pipeline.</p></div></div>
    <div className="explorer-toolbar"><input placeholder="Search company, role, location or notes…" value={q} onChange={e=>setQ(e.target.value)}/><select value={status} onChange={e=>setStatus(e.target.value)}><option value="">All statuses</option>{(data?.facets?.statuses||[]).map(item=><option key={item}>{item}</option>)}</select><label><input type="checkbox" checked={active} onChange={e=>setActive(e.target.checked)}/> Active</label><label><input type="checkbox" checked={salary} onChange={e=>setSalary(e.target.checked)}/> Has salary</label></div>
    <div className="explorer-counts"><Metric label="Matches" value={data?.counts?.total}/><Metric label="Active" value={data?.counts?.active}/><Metric label="Salary" value={data?.counts?.with_salary}/><Metric label="Follow-ups" value={data?.counts?.with_follow_up}/></div>
    <section className="explorer-panel">{loading?<div className="explorer-empty">Loading…</div>:<div className="explorer-table">{(data?.applications||[]).map(item=><div className="explorer-row" key={item.id}><div><strong>{item.company}</strong><span>{item.role}</span></div><span className="badge" data-status={item.status}>{item.status}</span><span>{item.location||'—'}</span><span>{item.next_action_date||'—'}</span></div>)}{!data?.applications?.length&&<div className="explorer-empty">No applications match the current filters.</div>}</div>}</section>
  </div>;
}
function Metric({label,value}){return <div><span>{label}</span><strong>{value||0}</strong></div>}
