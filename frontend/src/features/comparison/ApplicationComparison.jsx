import React, { useEffect, useState } from 'react';
import './comparison.css';

export default function ApplicationComparison({ api }) {
  const [summary,setSummary]=useState(null);
  const [left,setLeft]=useState('');
  const [right,setRight]=useState('');
  const [comparison,setComparison]=useState(null);
  const [error,setError]=useState('');
  const [loading,setLoading]=useState(true);

  const load=async()=>{
    setLoading(true);setError('');
    try{const response=await api.get('/applications/compare/summary/');setSummary(response.data)}
    catch(e){setError(e.response?.data?.detail||'Could not load comparison data.')}
    finally{setLoading(false)}
  };
  useEffect(()=>{load()},[]);

  const compare=async()=>{
    if(!left||!right||left===right){setError('Select two different applications to compare.');return}
    setError('');
    try{const response=await api.get('/applications/compare/?left='+encodeURIComponent(left)+'&right='+encodeURIComponent(right));setComparison(response.data)}
    catch(e){setError(e.response?.data?.detail||'Could not compare those applications.')}
  };

  if(loading)return <div className="workspace"><div className="page-head"><div><span className="eyebrow">COMPARE</span><h2>Application comparison</h2></div></div><div className="comparison-loading"><i/><i/></div></div>;
  const options=summary?.shortlist||[];
  return <div className="workspace comparison">
    <div className="page-head"><div><span className="eyebrow">COMPARE</span><h2>Application comparison</h2><p className="muted">Place two tracked opportunities side by side using the data you have already recorded.</p></div></div>
    {error&&<div className="alert error">{error}</div>}
    <section className="compare-selector"><label>First application<select value={left} onChange={e=>setLeft(e.target.value)}><option value="">Choose…</option>{options.map(item=><option value={item.id} key={item.id}>{item.company} · {item.role}</option>)}</select></label><span className="versus">VS</span><label>Second application<select value={right} onChange={e=>setRight(e.target.value)}><option value="">Choose…</option>{options.map(item=><option value={item.id} key={item.id}>{item.company} · {item.role}</option>)}</select></label><button className="primary" onClick={compare}>Compare</button></section>

    {comparison&&<><div className="comparison-head"><CardTitle item={comparison.left}/><div className="versus-large">VS</div><CardTitle item={comparison.right}/></div><section className="comparison-panel"><div className="comparison-panel-head"><h3>Dimensions</h3><p>These values are descriptive measurements from the stored records.</p></div><div className="dimension-list">{comparison.dimensions.map(item=><div className="dimension" key={item.label}><span>{item.label}</span><strong>{item.left??'—'}</strong><i data-relation={item.relation}>{item.relation}</i><strong>{item.right??'—'}</strong></div>)}</div></section><div className="comparison-columns"><section className="comparison-panel"><h3>Shared skills</h3><SkillList values={comparison.differences.shared_skills}/></section><section className="comparison-panel"><h3>Distinct skills</h3><div className="skill-columns"><div><small>First</small><SkillList values={comparison.differences.left_only_skills}/></div><div><small>Second</small><SkillList values={comparison.differences.right_only_skills}/></div></div></section></div></>}
    {!comparison&&<section className="comparison-panel comparison-empty"><h3>Choose two applications</h3><p>The comparison will show salary, skill, interview, activity and status differences.</p></section>}
  </div>;
}
function CardTitle({item}){return <div className="compare-card"><span>{item.status}</span><strong>{item.company}</strong><p>{item.role}</p><small>{item.location||'Location not recorded'}</small></div>}
function SkillList({values}){return values?.length?<div className="skill-list">{values.map(value=><span key={value}>{value}</span>)}</div>:<p className="muted">None recorded</p>}
