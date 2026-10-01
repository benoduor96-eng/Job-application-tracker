import React,{useEffect,useState} from "react";
import "./InterviewPreparation.css";

export default function InterviewPreparation(){
 const [data,setData]=useState(null),[selected,setSelected]=useState(null),[error,setError]=useState("");
 async function load(){try{const r=await fetch("/api/interview-preparation/?days=45");if(!r.ok)throw Error("Unable to load interview preparation");setData(await r.json())}catch(e){setError(e.message)}}
 useEffect(()=>{load()},[]);
 if(!data)return <div className="prep-page"><div className="prep-empty">{error||"Loading interview preparation…"}</div></div>;
 const item=selected||data.upcoming[0];
 return <div className="prep-page"><header className="prep-header"><div><span>INTERVIEW PREPARATION</span><h1>Preparation hub</h1><p>Turn scheduled interviews into a structured preparation plan.</p></div><button onClick={load}>Refresh</button></header>
 <div className="prep-kpis">{[[data.stats.upcoming,"Upcoming"],[data.stats.next_7_days,"Next 7 days"],[data.stats.missing_interviewer,"Missing interviewer"],[data.stats.missing_notes,"Missing notes"],[data.stats.missing_description,"Missing job description"]].map(x=><div key={x[1]}><strong>{x[0]}</strong><small>{x[1]}</small></div>)}</div>
 <div className="prep-layout"><section className="prep-panel"><h2>Upcoming interviews</h2>{data.upcoming.length?data.upcoming.map(x=><button className={item?.id===x.id?"prep-row selected":"prep-row"} onClick={()=>setSelected(x)} key={x.id}><span><b>{x.company}</b><small>{x.role} · {x.type_label}</small></span><em>{x.days_until===0?"Today":x.days_until+"d"}</em></button>):<div className="prep-empty">No scheduled interviews in the next 45 days.</div>}</section>
 <section className="prep-panel">{item?<><h2>{item.company}</h2><p className="prep-role">{item.role} · {item.type_label}</p><div className="prep-date">{new Date(item.scheduled_date).toLocaleString()}</div><div className="prep-info"><span><b>{item.interviewer.name||"Not recorded"}</b><small>{item.interviewer.title||"Interviewer"}</small></span><span><b>{item.job_description_attached?"Attached":"Missing"}</b><small>Job description</small></span></div><h3>Checklist</h3><ul>{item.checklist.map((x,i)=><li key={i}>{x}</li>)}</ul></>:<div className="prep-empty">Select an interview to view its preparation checklist.</div>}</section></div></div>
}