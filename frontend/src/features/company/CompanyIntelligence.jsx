import React, { useEffect, useMemo, useState } from "react";
import "./CompanyIntelligence.css";

export default function CompanyIntelligence() {
  const [data,setData]=useState(null),[selected,setSelected]=useState(null),[detail,setDetail]=useState(null),[query,setQuery]=useState(""),[error,setError]=useState("");
  async function load(){try{const r=await fetch("/api/company-intelligence/?limit=100");if(!r.ok)throw Error("Unable to load company intelligence");setData(await r.json())}catch(e){setError(e.message)}}
  async function openCompany(company){setSelected(company);try{const r=await fetch("/api/company-intelligence/?company="+encodeURIComponent(company));if(!r.ok)throw Error("Unable to load company detail");setDetail(await r.json())}catch(e){setError(e.message)}}
  useEffect(()=>{load()},[]);
  const companies=useMemo(()=>data?data.companies.filter(x=>x.company.toLowerCase().includes(query.toLowerCase())):[],[data,query]);
  if(!data)return <div className="company-page"><div className="company-empty">{error||"Loading company intelligence…"}</div></div>;
  return <div className="company-page">
    <header className="company-header"><div><span className="company-eyebrow">COMPANY INTELLIGENCE</span><h1>Company workspace</h1><p>Review pipeline, relationships, interviews and action gaps by company.</p></div><button onClick={load}>Refresh</button></header>
    <div className="company-kpis">{[[data.totals.companies,"Companies"],[data.totals.applications,"Applications"],[data.totals.active_applications,"Active"],[data.totals.interviews,"Interviews"],[data.totals.contacts,"Contacts"]].map(x=><div key={x[1]}><strong>{x[0]}</strong><span>{x[1]}</span></div>)}</div>
    <div className="company-layout">
      <section className="company-panel"><div className="company-panel-head"><h2>Companies</h2><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Filter companies"/></div>
      <div className="company-list">{companies.map(row=><button key={row.company} className={selected===row.company?"selected":""} onClick={()=>openCompany(row.company)}><span><strong>{row.company}</strong><small>{row.applications} applications · {row.roles} roles</small></span><span className="company-row-meta"><b>{row.active}</b> active · {row.interviews} interviews</span></button>)}</div></section>
      <section className="company-panel">{!detail?<div className="company-empty">Select a company to inspect its pipeline.</div>:<div className="company-detail">
        <div className="company-detail-head"><div><h2>{detail.company}</h2><p>{detail.roles.join(" · ")}</p></div><button onClick={()=>{setSelected(null);setDetail(null)}}>Clear</button></div>
        <div className="detail-kpis">{[[detail.active_applications,"Active"],[detail.interviews,"Interviews"],[detail.offers,"Offers"],[detail.contacts,"Contacts"]].map(x=><div key={x[1]}><strong>{x[0]}</strong><span>{x[1]}</span></div>)}</div>
        <div className="detail-section"><h3>Relationship</h3><p>{detail.relationship.contacts} contacts · {detail.relationship.recent_contacts} recent · {detail.relationship.overdue_followups} overdue follow-ups</p></div>
        <div className="detail-section"><h3>Salary signal</h3><p>{detail.salary.count?detail.salary.minimum+" – "+detail.salary.maximum+" · avg "+detail.salary.average:"No salary data recorded."}</p></div>
        <div className="detail-section"><h3>Attention</h3>{detail.attention.length?detail.attention.map((x,i)=><div className="attention-row" key={x.type+i}><b>{x.priority}</b><span>{x.title}</span></div>):<p>No immediate attention items.</p>}</div>
        <div className="detail-section"><h3>Applications</h3><div className="mini-table">{detail.applications_detail.map(x=><div key={x.id}><span><b>{x.role}</b><small>{x.location||"Location not recorded"}</small></span><em>{x.status}</em></div>)}</div></div>
      </div>}</section>
    </div>
    <section className="company-panel"><div className="company-panel-head"><h2>Relationship gaps</h2></div>{data.relationship_gaps.length?data.relationship_gaps.map((x,i)=><div className="gap-row" key={x.company+i}><b>{x.priority}</b><span><strong>{x.company}</strong>{x.reason}</span></div>):<div className="company-empty">No relationship gaps detected.</div>}</section>
  </div>
}
