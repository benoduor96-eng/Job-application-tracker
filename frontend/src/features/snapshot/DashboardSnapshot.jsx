import React, { useEffect, useMemo, useState } from 'react';
import './snapshot.css';

const pretty = value => String(value || '').replaceAll('_',' ');
const dateLabel = value => value ? new Date(value).toLocaleDateString(undefined,{month:'short',day:'numeric'}) : '—';

export default function DashboardSnapshot({ api }) {
  const [data,setData]=useState(null);
  const [tab,setTab]=useState('focus');
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');

  const load=async()=>{
    setLoading(true);setError('');
    try{const response=await api.get('/dashboard/snapshot/');setData(response.data)}
    catch(e){setError(e.response?.data?.detail||'Could not load the dashboard snapshot.')}
    finally{setLoading(false)}
  };
  useEffect(()=>{load()},[]);

  const counts=data?.counts||{};
  const focus=useMemo(()=>data?.focus||[],[data]);
  if(loading)return <div className="workspace"><div className="page-head"><div><span className="eyebrow">OPERATIONS</span><h2>Dashboard snapshot</h2></div></div><div className="snapshot-loading"><i/><i/><i/></div></div>;
  if(error)return <div className="workspace"><div className="alert error">{error}</div><button className="primary" onClick={load}>Try again</button></div>;

  return <div className="workspace snapshot">
    <div className="page-head"><div><span className="eyebrow">OPERATIONS</span><h2>Dashboard snapshot</h2><p className="muted">A compact operating view of your applications, deadlines, workload and response activity.</p></div><button className="secondary" onClick={load}>↻ Refresh</button></div>
    <div className="snapshot-metrics">
      <Metric label="Applications" value={counts.applications}/><Metric label="Active" value={counts.active}/><Metric label="Interviews" value={counts.interview}/><Metric label="Offers" value={counts.offer}/><Metric label="Open tasks" value={counts.open_tasks}/><Metric label="Contacts" value={counts.contacts}/>
    </div>
    <div className="snapshot-tabs">{[['focus','Focus'],['activity','Activity'],['salary','Salary'],['companies','Companies']].map(([id,label])=><button key={id} className={tab===id?'active':''} onClick={()=>setTab(id)}>{label}</button>)}</div>

    {tab==='focus'&&<div className="snapshot-columns"><Panel title="Focus queue" subtitle="Items ordered by operational priority"><div className="focus-list">{focus.map((item,index)=><div className="focus-row" key={item.type+'-'+(item.application_id||index)}><span className="focus-score">{item.priority}</span><div><strong>{item.title}</strong><span>{item.company||'Career task'}{item.role?' · '+item.role:''}</span><small>{item.detail}</small></div><em>{pretty(item.type)}</em></div>)}{!focus.length&&<Empty text="No priority items are waiting."/>}</div></Panel><Panel title="Response metrics"><div className="response-list"><Row label="Applications with dates" value={data.response.applied_with_date}/><Row label="Reached interview" value={data.response.applications_reaching_interview}/><Row label="Interview rate" value={data.response.interview_rate+'%'}/><Row label="Avg days to interview" value={data.response.average_days_to_interview==null?'—':data.response.average_days_to_interview}/></div></Panel></div>}

    {tab==='activity'&&<div className="snapshot-columns"><Panel title="Activity window" subtitle="Last 30 days"><div className="response-list"><Row label="Total activities" value={data.activity.total}/>{Object.entries(data.activity.by_type||{}).map(([key,value])=><Row key={key} label={pretty(key)} value={value}/>)}</div><div className="activity-bars">{(data.activity.daily||[]).map(item=><div key={item.date} title={item.date}><i style={{height:Math.max(6,Math.min(100,item.count*14))+'%'}}/><span>{dateLabel(item.date)}</span></div>)}</div></Panel><Panel title="Velocity"><div className="velocity"><strong>{data.velocity.daily_average}</strong><span>applications/day</span><small>{data.velocity.change>0?'+':''}{data.velocity.change} compared with the previous window</small><b>{pretty(data.velocity.direction)}</b></div></Panel></div>}

    {tab==='salary'&&<Panel title="Salary snapshot" subtitle="Values recorded on your applications"><div className="salary-grid"><Metric label="With salary" value={data.salary.applications_with_salary}/><Metric label="Average midpoint" value={data.salary.average_midpoint||'—'}/><Metric label="Minimum midpoint" value={data.salary.minimum||'—'}/><Metric label="Maximum midpoint" value={data.salary.maximum||'—'}/></div></Panel>}

    {tab==='companies'&&<Panel title="Company leaderboard" subtitle="Active pipeline volume and interview/offer counts"><div className="company-table">{(data.companies||[]).map(row=><div className="company-line" key={row.company}><strong>{row.company}</strong><span>{row.applications} applications</span><span>{row.active} active</span><span>{row.interviews} interviews</span><span>{row.offers} offers</span></div>)}</div></Panel>}
  </div>;
}

function Metric({label,value}){return <div className="snapshot-metric"><span>{label}</span><strong>{value==null?'—':value}</strong></div>}
function Panel({title,subtitle,children}){return <section className="snapshot-panel"><div className="snapshot-panel-head"><div><h3>{title}</h3>{subtitle&&<p>{subtitle}</p>}</div></div>{children}</section>}
function Row({label,value}){return <div className="snapshot-row"><span>{label}</span><strong>{value}</strong></div>}
function Empty({text}){return <div className="snapshot-empty">{text}</div>}
