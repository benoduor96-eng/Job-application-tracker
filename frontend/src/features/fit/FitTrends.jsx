import React,{useEffect,useState} from 'react';
import './fit.css';

export default function FitTrends(){
 const [data,setData]=useState(null),[loading,setLoading]=useState(true),[error,setError]=useState('');
 useEffect(()=>{let live=true;(async()=>{try{const r=await fetch('/api/applications/fit-trends/',{headers:{Authorization:'Bearer '+localStorage.getItem('access_token')}});if(!r.ok)throw new Error();const body=await r.json();if(live)setData(body)}catch(e){if(live)setError('Fit trend analytics could not be loaded.')}finally{if(live)setLoading(false)}})();return()=>{live=false}},[]);
 if(loading)return <div className="workspace"><div className="panel fit-loading">Loading fit trends…</div></div>;
 if(error)return <div className="workspace"><div className="alert error">{error}</div></div>;
 const status=Object.entries(data?.by_status||{});const gaps=data?.common_skill_gaps||[];const maxGap=Math.max(1,...gaps.map(x=>x.count));
 return <div className="workspace"><div className="page-head"><div><span className="eyebrow">FIT TRENDS</span><h2>Fit trends</h2><p className="muted">See how application fit varies across your pipeline and where your skill gaps repeat.</p></div></div>
 <div className="metric-grid"><div className="metric"><span className="metric-icon">◎</span><div><span>Average fit</span><strong>{data?.average_score||0}</strong></div></div><div className="metric"><span className="metric-icon">↑</span><div><span>Highest fit</span><strong>{data?.highest_score||0}</strong></div></div><div className="metric"><span className="metric-icon">↓</span><div><span>Lowest fit</span><strong>{data?.lowest_score||0}</strong></div></div><div className="metric"><span className="metric-icon">▤</span><div><span>Applications</span><strong>{data?.count||0}</strong></div></div></div>
 <div className="two-col"><section className="panel"><div className="panel-head"><h3>Fit by pipeline status</h3></div><div className="trend-list">{status.map(([name,item])=><div className="trend-row" key={name}><div><strong>{name}</strong><span>{item.count} application{item.count===1?'':'s'}</span></div><div className="trend-score"><strong>{item.average_score}</strong><small>avg fit</small></div></div>)}{!status.length&&<div className="empty">No fit data yet.</div>}</div></section>
 <section className="panel"><div className="panel-head"><h3>Common skill gaps</h3></div><div className="gap-bars">{gaps.map(item=><div className="gap-bar" key={item.skill}><div><span>{item.skill}</span><strong>{item.count}</strong></div><i style={{width:(item.count/maxGap*100)+'%'}}/></div>)}{!gaps.length&&<div className="empty">No repeated required skill gaps found.</div>}</div></section></div>
 <section className="panel"><div className="panel-head"><h3>Application snapshots</h3><span className="muted">Current fit signals</span></div><div className="trend-table">{(data?.applications||[]).map(item=><div className="trend-app" key={item.application_id}><div><strong>{item.company}</strong><span>{item.role} · {item.status}</span></div><strong>{item.score}/100</strong></div>)}</div></section>
 </div>;
}
