import React, { useEffect, useState } from 'react';
import './PipelineRisk.css';

const statusLabel = value => ({saved:'Saved',applied:'Applied',screening:'Screening',interview:'Interview',offer:'Offer'})[value] || value;

function RiskItem({item}) {
  return <div className="risk-item"><div className="risk-score"><strong>{item.risk}</strong><span>risk</span></div><div className="risk-main"><strong>{item.company} · {item.role}</strong><span>{statusLabel(item.status)} · updated {new Date(item.updated_at).toLocaleDateString()}</span><div className="risk-reasons">{item.reasons.map(reason => <small key={reason}>{reason}</small>)}</div></div></div>;
}

export default function PipelineRisk({api}) {
  const [risk,setRisk]=useState(null),[health,setHealth]=useState(null),[relationships,setRelationships]=useState(null),[error,setError]=useState('');
  useEffect(()=>{Promise.all([api.get('/pipeline-risk/'),api.get('/pipeline-health/'),api.get('/relationship-health/')]).then(([a,b,c])=>{setRisk(a.data);setHealth(b.data);setRelationships(c.data);}).catch(()=>setError('Pipeline health could not be loaded.'));},[api]);
  if(error)return <section className="risk-page"><div className="global-error">{error}</div></section>;
  if(!risk||!health||!relationships)return <section className="risk-page"><div className="panel performance-loading">Loading pipeline health...</div></section>;
  return <section className="risk-page"><header className="risk-header"><div><span className="eyebrow">PIPELINE CONTROL</span><h1>Pipeline health</h1><p>Identify records that need attention and review relationship coverage.</p></div></header>
    <div className="risk-metrics"><div className="panel"><span>Active applications</span><strong>{health.active}</strong><small>{health.total} total records</small></div><div className="panel"><span>Action coverage</span><strong>{health.action_coverage}%</strong><small>Records with next action dates</small></div><div className="panel"><span>Stale active</span><strong>{health.stale_active}</strong><small>14+ days without update</small></div><div className="panel"><span>Contacts</span><strong>{relationships.total}</strong><small>{relationships.applications_with_contacts} applications linked</small></div></div>
    <div className="risk-layout"><article className="panel"><div className="panel-heading"><div><h2>Attention queue</h2><span>{risk.total_risk_items} records with calculated risk signals</span></div></div>{risk.items.length?risk.items.map(item=><RiskItem item={item} key={item.id}/>):<p className="empty-state">No current risk signals.</p>}</article><aside className="panel relationship-panel"><h2>Relationship coverage</h2><div className="relationship-stat"><span>Contacts with email</span><strong>{relationships.with_email}</strong></div><div className="relationship-stat"><span>Contacts with follow-up</span><strong>{relationships.with_follow_up}</strong></div><div className="relationship-stat"><span>Interview records</span><strong>{relationships.interviews}</strong></div><h3>Contact recency</h3>{Object.entries(relationships.follow_up_buckets).map(([key,value])=><div className="bucket" key={key}><span>{key.replace('_',' ')}</span><strong>{value}</strong></div>)}</aside></div>
  </section>;
}
