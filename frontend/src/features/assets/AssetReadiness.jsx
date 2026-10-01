import React,{useEffect,useState} from 'react';
import './assetReadiness.css';

export default function AssetReadiness({api}){
  const [data,setData]=useState(null),[loading,setLoading]=useState(true),[error,setError]=useState('');
  const load=async()=>{setLoading(true);setError('');try{const r=await api.get('/career-assets/readiness/');setData(r.data)}catch(e){setError(e.response?.data?.detail||'Could not load career asset readiness.')}finally{setLoading(false)}};
  useEffect(()=>{load()},[]);
  if(loading)return <div className="workspace"><div className="page-head"><div><span className="eyebrow">CAREER ASSETS</span><h2>Asset readiness</h2></div></div><div className="asset-loading"><i/><i/></div></div>;
  if(error)return <div className="workspace"><div className="alert error">{error}</div><button className="primary" onClick={load}>Try again</button></div>;
  const summary=data.summary||{};
  return <div className="workspace asset-readiness"><div className="page-head"><div><span className="eyebrow">CAREER ASSETS</span><h2>Asset readiness</h2><p className="muted">Check the reusable profile and resume information behind your application workflow.</p></div><button className="secondary" onClick={load}>↻ Refresh</button></div>
    <div className="asset-metrics"><Metric label="Profile" value={summary.profile_score+'%'}/><Metric label="Resumes" value={summary.resume_count}/><Metric label="Best resume" value={summary.best_resume_score+'%'}/><Metric label="JD coverage" value={summary.application_coverage.coverage_rate+'%'}/></div>
    <div className="asset-columns"><section className="asset-panel"><h3>Profile completeness</h3>{data.profile.exists?<><div className="asset-progress"><i style={{width:data.profile.score+'%'}}/></div><strong>{data.profile.score}% complete</strong><div className="asset-checks">{Object.entries(data.profile.checks||{}).map(([key,value])=><div key={key} className={value?'complete':''}><span>{value?'✓':'○'}</span>{key.replaceAll('_',' ')}</div>)}</div></>:<div className="asset-empty">No career profile exists yet.</div>}</section>
    <section className="asset-panel"><h3>Resumes</h3><div className="resume-list">{data.resumes.map(item=><div key={item.id}><div><strong>{item.name}</strong><span>v{item.version} · {item.status}</span></div><b>{item.score}%</b></div>)}{!data.resumes.length&&<div className="asset-empty">No resumes recorded.</div>}</div></section></div>
    <section className="asset-panel"><h3>Next improvements</h3><div className="asset-recommendations">{data.recommendations.map((item,index)=><div key={item.type+'-'+index}><span>{item.priority}</span><div><strong>{item.title}</strong><p>{item.detail}</p></div></div>)}{!data.recommendations.length&&<div className="asset-empty">Your reusable assets have no current recommendations.</div>}</div></section>
  </div>;
}
function Metric({label,value}){return <div className="asset-metric"><span>{label}</span><strong>{value}</strong></div>}
