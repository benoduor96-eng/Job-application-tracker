import React,{useEffect,useMemo,useState} from 'react';
import './ActivityCalendar.css';

export default function ActivityCalendar({api}) {
  const [data,setData]=useState(null),[error,setError]=useState('');
  useEffect(()=>{api.get('/activity-calendar/').then(r=>setData(r.data)).catch(()=>setError('Calendar data could not be loaded.'));},[api]);
  const dates=useMemo(()=>{
    if(!data)return [];
    const out=[],d=new Date(data.range.start+'T00:00:00'),end=new Date(data.range.end+'T00:00:00');
    while(d<=end){out.push(new Date(d));d.setDate(d.getDate()+1)}
    return out;
  },[data]);
  if(error)return <section className="calendar-page"><div className="global-error">{error}</div></section>;
  if(!data)return <section className="calendar-page"><div className="panel calendar-loading">Loading activity calendar...</div></section>;
  return <section className="calendar-page">
    <header><span className="eyebrow">ACTIVITY CALENDAR</span><h1>Job search calendar</h1><p>Applications, interviews and career tasks in one chronological workspace.</p></header>
    <div className="calendar-metrics">{Object.entries(data.totals).map(([k,v])=><div className="panel" key={k}><span>{k}</span><strong>{v}</strong></div>)}</div>
    <div className="calendar-grid">{dates.map(date=>{const key=date.toISOString().slice(0,10),items=data.days[key]||[];return <article className={'calendar-day '+(key===data.today?'today':'')} key={key}><div className="day-head"><strong>{date.toLocaleDateString(undefined,{weekday:'short'})}</strong><span>{date.getDate()}</span></div>{items.map((item,i)=><div className={'calendar-event '+item.type} key={item.type+item.id+i}><small>{item.type}</small><strong>{item.title}</strong><span>{item.status}</span></div>)}{!items.length&&<em>No activity</em>}</article>})}</div>
  </section>;
}
