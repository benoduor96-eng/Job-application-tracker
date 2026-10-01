import React,{useEffect,useState} from 'react';
import './workspaceHealth.css';

export default function WorkspaceHealth({api}){
  const [checks,setChecks]=useState([]),[loading,setLoading]=useState(true);
  const endpoints=[
    ['API health','/health/','status'],
    ['Review workspace','/review/workspace/','overview'],
    ['Dashboard snapshot','/dashboard/snapshot/','counts'],
    ['Task analytics','/tasks/analytics/','summary'],
    ['Asset readiness','/career-assets/readiness/','summary'],
    ['Search insights','/search-insights/','coverage'],
    ['Timeline','/timeline/dashboard/','counts'],
  ];
  useEffect(()=>{
    let alive=true;
    Promise.all(endpoints.map(async([label,path,key])=>{
      try{const response=await api.get(path);return {label,ok:response.data&&response.data[key]!==undefined}}
      catch{return {label,ok:false}}
    })).then(rows=>{if(alive)setChecks(rows)}).finally(()=>{if(alive)setLoading(false)});
    return()=>{alive=false};
  },[]);
  const passing=checks.filter(item=>item.ok).length;
  return <div className="workspace workspace-health"><div className="page-head"><div><span className="eyebrow">SYSTEM CHECK</span><h2>Workspace health</h2><p className="muted">Confirm that the main career intelligence workspaces can be reached from the current session.</p></div></div>
    <section className="workspace-health-panel"><div className="health-summary"><strong>{loading?'—':passing+'/'+checks.length}</strong><span>{loading?'Checking workspaces…':'workspaces responding'}</span></div><div className="workspace-checks">{checks.map(item=><div key={item.label}><span className={item.ok?'online':'offline'}/><strong>{item.label}</strong><em>{item.ok?'Ready':'Unavailable'}</em></div>)}{loading&&<div className="health-placeholder">Running workspace checks…</div>}</div></section>
  </div>;
}
