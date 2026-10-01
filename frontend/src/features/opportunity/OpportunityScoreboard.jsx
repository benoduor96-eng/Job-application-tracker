import React, { useEffect, useState } from 'react';
import './OpportunityScoreboard.css';

function Score({value}) {
  return <div className="opportunity-score"><strong>{value}</strong><span>/100</span></div>;
}

export default function OpportunityScoreboard({api}) {
  const [data,setData]=useState(null),[error,setError]=useState('');
  useEffect(()=>{api.get('/opportunity-scoreboard/').then(r=>setData(r.data)).catch(()=>setError('Opportunity data could not be loaded.'));},[api]);
  if(error)return <section className="opportunity-page"><div className="global-error">{error}</div></section>;
  if(!data)return <section className="opportunity-page"><div className="panel opportunity-loading">Loading opportunity scoreboard...</div></section>;
  return <section className="opportunity-page">
    <header className="opportunity-header"><div><span className="eyebrow">OPPORTUNITY INTELLIGENCE</span><h1>Opportunity scoreboard</h1><p>See which tracked applications have the strongest documented pipeline signals.</p></div></header>
    <div className="opportunity-metrics"><div className="panel"><span>Average score</span><strong>{data.average_score}</strong><small>Across {data.total} applications</small></div><div className="panel"><span>High signal</span><strong>{data.distribution.high||0}</strong><small>75–100</small></div><div className="panel"><span>Medium signal</span><strong>{data.distribution.medium||0}</strong><small>50–74</small></div><div className="panel"><span>Low signal</span><strong>{data.distribution.low||0}</strong><small>Below 50</small></div></div>
    <article className="panel opportunity-table"><div className="panel-heading"><div><h2>Tracked opportunities</h2><span>Scores are based only on fields stored in your workspace.</span></div></div>{data.opportunities.map(item=><div className="opportunity-row" key={item.id}><Score value={item.score}/><div className="opportunity-main"><strong>{item.company} · {item.role}</strong><span>{item.status} · updated {new Date(item.updated_at).toLocaleDateString()}</span><div className="opportunity-signals">{item.signals.map(signal=><small key={signal}>{signal}</small>)}</div></div></div>)}{!data.opportunities.length&&<p className="empty-state">Add applications to populate the scoreboard.</p>}</article>
  </section>;
}
