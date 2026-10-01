import React,{useEffect,useState} from 'react';
import './taskAnalytics.css';

export default function TaskAnalytics({api}){
  const [data,setData]=useState(null),[loading,setLoading]=useState(true),[error,setError]=useState('');
  const load=async()=>{setLoading(true);setError('');try{const r=await api.get('/tasks/analytics/');setData(r.data)}catch(e){setError(e.response?.data?.detail||'Could not load task analytics.')}finally{setLoading(false)}};
  useEffect(()=>{load()},[]);
  if(loading)return <div className="workspace"><div className="page-head"><div><span className="eyebrow">TASK ANALYTICS</span><h2>Task workload</h2></div></div><div className="task-analytics-loading"><i/><i/></div></div>;
  if(error)return <div className="workspace"><div className="alert error">{error}</div><button className="primary" onClick={load}>Try again</button></div>;
  const s=data.summary||{};
  return <div className="workspace task-analytics"><div className="page-head"><div><span className="eyebrow">TASK ANALYTICS</span><h2>Task workload</h2><p className="muted">See workload, deadlines, priorities and tags across your career tasks.</p></div><button className="secondary" onClick={load}>↻ Refresh</button></div>
    <div className="task-metrics"><Metric label="Open" value={s.open}/><Metric label="Overdue" value={s.overdue}/><Metric label="Due today" value={s.due_today}/><Metric label="Completion" value={s.completion_rate+'%'}/></div>
    <div className="task-analytics-columns"><Panel title="Priority breakdown"><div className="priority-bars">{data.priorities.map(row=><div key={row.priority}><span>{row.priority}</span><div><i style={{width:Math.min(100,row.count*20)+'%'}}/></div><strong>{row.count}</strong></div>)}</div></Panel><Panel title="Due next 14 days"><div className="task-list">{data.due_window.map(item=><div key={item.id}><strong>{item.title}</strong><span>{item.priority} · {new Date(item.due_date).toLocaleDateString()}</span></div>)}{!data.due_window.length&&<Empty text="No upcoming tasks."/>}</div></Panel></div>
    <Panel title="Overdue tasks"><div className="task-list">{data.overdue.map(item=><div key={item.id}><strong>{item.title}</strong><span>{item.priority} · {item.due_date?new Date(item.due_date).toLocaleDateString():'No date'}</span></div>)}{!data.overdue.length&&<Empty text="No overdue tasks."/>}</div></Panel>
    <Panel title="Tags"><div className="task-tags">{data.tags.map(item=><span key={item.tag}>{item.tag} · {item.count}</span>)}{!data.tags.length&&<Empty text="No task tags yet."/>}</div></Panel>
  </div>;
}
function Metric({label,value}){return <div className="task-metric"><span>{label}</span><strong>{value||0}</strong></div>}
function Panel({title,children}){return <section className="task-panel"><h3>{title}</h3>{children}</section>}
function Empty({text}){return <div className="task-empty">{text}</div>}
