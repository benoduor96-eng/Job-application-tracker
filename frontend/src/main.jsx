import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';
import './styles.css';
import LifecyclePanel from './features/lifecycle/LifecyclePanel.jsx';
import FitPanel from './features/fit/FitPanel.jsx';
import FitDashboard from './features/fit/FitDashboard.jsx';
import FitTrends from './features/fit/FitTrends.jsx';
import ApplicationHealth from './features/health/ApplicationHealth.jsx';
import CompensationDashboard from './features/compensation/CompensationDashboard.jsx';
import ContactIntelligence from './features/contacts/ContactIntelligence.jsx';
import ReviewWorkspace from './features/review/ReviewWorkspace.jsx';
import SearchInsights from './features/search/SearchInsights.jsx';
import InterviewPrep from './features/interviews/InterviewPrep.jsx';
import DashboardSnapshot from './features/snapshot/DashboardSnapshot.jsx';
import ApplicationComparison from './features/comparison/ApplicationComparison.jsx';
import ApplicationTimeline from './features/timeline/ApplicationTimeline.jsx';
import TaskAnalytics from './features/tasks/TaskAnalytics.jsx';
import AssetReadiness from './features/assets/AssetReadiness.jsx';
import ApplicationExplorer from './features/explorer/ApplicationExplorer.jsx';
import WorkspaceHealth from './features/health/WorkspaceHealth.jsx';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

const STATUSES = ['saved','applied','screening','interview','offer','rejected','withdrawn'];

function useAuth() {
  const [authenticated, setAuthenticated] = useState(Boolean(localStorage.getItem('access_token')));
  const login = (token, refresh) => {
    localStorage.setItem('access_token', token);
    if (refresh) localStorage.setItem('refresh_token', refresh);
    setAuthenticated(true);
  };
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setAuthenticated(false);
  };
  return { authenticated, login, logout };
}

function AuthScreen({ onLogin }) {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({ username:'', password:'', email:'', first_name:'', last_name:'' });
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault(); setBusy(true); setError('');
    try {
      if (mode === 'register') {
        await api.post('/auth/register/', form);
      }
      const r = await api.post('/auth/token/', { username: form.username, password: form.password });
      onLogin(r.data.access, r.data.refresh);
    } catch (err) {
      setError(err.response?.data?.detail || Object.values(err.response?.data || {}).flat().join(' ') || 'Authentication failed.');
    } finally { setBusy(false); }
  };

  return <div className="auth-shell">
    <div className="auth-card">
      <div className="brand-mark">JT</div>
      <span className="eyebrow">CAREER WORKSPACE</span>
      <h1>{mode === 'login' ? 'Welcome back' : 'Create your workspace'}</h1>
      <p className="muted">Track applications, interviews, follow-ups and career intelligence in one place.</p>
      {error && <div className="alert error">{error}</div>}
      <form onSubmit={submit} className="stack">
        {mode === 'register' && <div className="form-grid">
          <input placeholder="First name" value={form.first_name} onChange={e=>setForm({...form,first_name:e.target.value})}/>
          <input placeholder="Last name" value={form.last_name} onChange={e=>setForm({...form,last_name:e.target.value})}/>
          <input className="full" type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/>
        </div>}
        <input required placeholder="Username" value={form.username} onChange={e=>setForm({...form,username:e.target.value})}/>
        <input required type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/>
        <button className="primary wide" disabled={busy}>{busy ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Create account'}</button>
      </form>
      <button className="link-button" onClick={()=>{setMode(mode==='login'?'register':'login');setError('')}}>
        {mode === 'login' ? 'Create a new account' : 'Already have an account? Sign in'}
      </button>
    </div>
  </div>;
}

function Modal({ title, onClose, children }) {
  return <div className="overlay" onMouseDown={onClose}><div className="modal" onMouseDown={e=>e.stopPropagation()}><div className="modal-head"><h2>{title}</h2><button className="icon-button" onClick={onClose}>×</button></div>{children}</div></div>;
}

function ApplicationModal({ job, onClose, onSaved }) {
  const [form,setForm]=useState(job || {company:'',role:'',location:'',job_url:'',status:'saved',salary_min:'',salary_max:'',applied_date:'',next_action:'',next_action_date:'',notes:''});
  const [busy,setBusy]=useState(false); const [error,setError]=useState('');
  const submit=async e=>{e.preventDefault();setBusy(true);setError('');try{const r=job?await api.put(`/applications/${job.id}/`,form):await api.post('/applications/',form);onSaved(r.data)}catch(err){setError('Could not save this application. Check the fields and try again.')}finally{setBusy(false)}};
  const set=(k,v)=>setForm({...form,[k]:v});
  return <Modal title={job?'Edit application':'Add application'} onClose={onClose}>
    {error&&<div className="alert error">{error}</div>}
    <form className="form-grid" onSubmit={submit}>
      <label>Company<input required value={form.company} onChange={e=>set('company',e.target.value)}/></label>
      <label>Role<input required value={form.role} onChange={e=>set('role',e.target.value)}/></label>
      <label>Location<input value={form.location||''} onChange={e=>set('location',e.target.value)}/></label>
      <label>Status<select value={form.status} onChange={e=>set('status',e.target.value)}>{STATUSES.map(s=><option key={s}>{s}</option>)}</select></label>
      <label className="full">Job URL<input type="url" value={form.job_url||''} onChange={e=>set('job_url',e.target.value)}/></label>
      <label>Salary min<input type="number" value={form.salary_min||''} onChange={e=>set('salary_min',e.target.value)}/></label>
      <label>Salary max<input type="number" value={form.salary_max||''} onChange={e=>set('salary_max',e.target.value)}/></label>
      <label>Applied date<input type="date" value={form.applied_date||''} onChange={e=>set('applied_date',e.target.value)}/></label>
      <label>Follow-up date<input type="date" value={form.next_action_date||''} onChange={e=>set('next_action_date',e.target.value)}/></label>
      <label className="full">Next action<input value={form.next_action||''} onChange={e=>set('next_action',e.target.value)}/></label>
      <label className="full">Notes<textarea rows="4" value={form.notes||''} onChange={e=>set('notes',e.target.value)}/></label>
      <div className="form-actions full"><button type="button" className="secondary" onClick={onClose}>Cancel</button><button className="primary" disabled={busy}>{busy?'Saving…':'Save application'}</button></div>
    </form>
  </Modal>;
}

function Overview({ dashboard, stats, jobs, onAdd }) {
  const counts=useMemo(()=>STATUSES.map(status=>({status,count:jobs.filter(j=>j.status===status).length})),[jobs]);
  return <div className="workspace">
    <div className="page-head"><div><span className="eyebrow">OVERVIEW</span><h2>Your job search at a glance</h2><p className="muted">A focused view of your current pipeline and next actions.</p></div><button className="primary" onClick={onAdd}>+ Add application</button></div>
    <div className="metric-grid">
      <Metric label="Applications" value={dashboard?.total ?? jobs.length} icon="◎"/>
      <Metric label="Active pipeline" value={dashboard?.active ?? jobs.filter(j=>!['rejected','withdrawn'].includes(j.status)).length} icon="↗"/>
      <Metric label="Interviews" value={dashboard?.interviews ?? jobs.filter(j=>j.status==='interview').length} icon="◷"/>
      <Metric label="Offers" value={dashboard?.offers ?? jobs.filter(j=>j.status==='offer').length} icon="★"/>
    </div>
    <div className="two-col">
      <section className="panel"><div className="panel-head"><h3>Pipeline</h3><span className="muted">Current applications</span></div>
        <div className="pipeline">{counts.map(x=><div className="pipeline-row" key={x.status}><span className="status-dot" data-status={x.status}/><span>{x.status}</span><strong>{x.count}</strong><div className="bar"><i style={{width:`${jobs.length?Math.max(4,x.count/jobs.length*100):0}%`}}/></div></div>)}</div>
      </section>
      <section className="panel"><div className="panel-head"><h3>Pipeline health</h3></div>
        <div className="health-grid"><Health label="Screening rate" value={stats?.screening_rate}/><Health label="Interview rate" value={stats?.interview_rate}/><Health label="Offer rate" value={stats?.offer_rate}/></div>
        <div className="tip"><span>✦</span><div><strong>Stay consistent</strong><p>Use follow-up dates and tasks to keep active applications moving.</p></div></div>
      </section>
    </div>
    <section className="panel"><div className="panel-head"><h3>Upcoming follow-ups</h3></div>{(dashboard?.upcoming||[]).length?<div className="upcoming">{dashboard.upcoming.map(x=><div className="upcoming-row" key={x.id}><div className="date-chip">{x.next_action_date?.slice(5,10)||'—'}</div><div><strong>{x.company}</strong><span>{x.role}</span><small>{x.next_action||'Follow up'}</small></div></div>)}</div>:<Empty text="No upcoming follow-ups yet."/>}</section>
  </div>;
}
const Metric=({label,value,icon})=><div className="metric"><span className="metric-icon">{icon}</span><div><span>{label}</span><strong>{value}</strong></div></div>;
const Health=({label,value})=><div className="health"><strong>{value==null?'—':`${value}%`}</strong><span>{label}</span></div>;
const Empty=({text})=><div className="empty">{text}</div>;

function Applications({jobs,onAdd,onEdit,onDelete,onFit,onManage}) {
  const [query,setQuery]=useState(''); const [status,setStatus]=useState('all');
  const filtered=jobs.filter(j=>(status==='all'||j.status===status)&&[`${j.company} ${j.role} ${j.location||''}`].toLowerCase().includes(query.toLowerCase()));
  return <div className="workspace"><div className="page-head"><div><span className="eyebrow">PIPELINE</span><h2>Applications</h2><p className="muted">Search, update and organize every opportunity.</p></div><button className="primary" onClick={onAdd}>+ Add application</button></div>
    <div className="toolbar"><input className="search" placeholder="Search company, role or location…" value={query} onChange={e=>setQuery(e.target.value)}/><select value={status} onChange={e=>setStatus(e.target.value)}><option value="all">All statuses</option>{STATUSES.map(s=><option key={s}>{s}</option>)}</select></div>
    <section className="panel table-panel"><div className="table-wrap"><table><thead><tr><th>Company</th><th>Role</th><th>Status</th><th>Location</th><th>Follow-up</th><th></th></tr></thead><tbody>{filtered.map(j=><tr key={j.id}><td><strong>{j.company}</strong></td><td>{j.role}</td><td><span className="badge" data-status={j.status}>{j.status}</span></td><td>{j.location||'—'}</td><td>{j.next_action_date||'—'}</td><td className="actions"><button onClick={()=>onManage(j)}>Manage</button><button onClick={()=>onFit(j)}>Fit</button><button onClick={()=>onEdit(j)}>Edit</button><button className="danger-text" onClick={()=>onDelete(j.id)}>Delete</button></td></tr>)}</tbody></table>{!filtered.length&&<Empty text="No applications match your filters."/>}</div></section>
  </div>;
}

function SimpleWorkspace({ title, eyebrow, description, endpoint, actionLabel, render }) {
  const [data,setData]=useState(null); const [loading,setLoading]=useState(true); const [error,setError]=useState('');
  useEffect(()=>{let alive=true;(async()=>{try{const r=await api.get(endpoint);if(alive)setData(r.data)}catch(e){if(alive)setError('This workspace is available, but the API did not return data yet.')}finally{if(alive)setLoading(false)}})();return()=>{alive=false}},[endpoint]);
  return <div className="workspace"><div className="page-head"><div><span className="eyebrow">{eyebrow}</span><h2>{title}</h2><p className="muted">{description}</p></div>{actionLabel&&<button className="secondary">{actionLabel}</button>}</div>{error&&<div className="alert">{error}</div>}{loading?<div className="panel"><div className="skeleton"/></div>:render(data)}</div>;
}

function Intelligence() {
  return <SimpleWorkspace title="Career intelligence" eyebrow="INTELLIGENCE" description="Turn your job data into practical, deterministic guidance." endpoint="/intelligence/summary/" render={data=><div className="two-col"><section className="panel"><div className="panel-head"><h3>Insights</h3></div><div className="insights">{Object.entries(data||{}).slice(0,12).map(([k,v])=><div className="insight" key={k}><span>{k.replaceAll('_',' ')}</span><strong>{typeof v==='object'?JSON.stringify(v):String(v)}</strong></div>)}</div></section><section className="panel"><div className="panel-head"><h3>How it works</h3></div><p className="muted">Matching uses the skills, salary, location and pipeline information stored in your applications and job descriptions. Results are deterministic and do not invent credentials.</p></section></div>}/>
}
function Reports() {
  return <SimpleWorkspace title="Reports & analytics" eyebrow="REPORTING" description="Understand your funnel, salary data, companies and stale applications." endpoint="/reports/dashboard/" render={data=><section className="panel"><div className="report-grid">{Object.entries(data||{}).map(([k,v])=><div className="report-card" key={k}><span>{k.replaceAll('_',' ')}</span><strong>{typeof v==='object'?JSON.stringify(v):String(v)}</strong></div>)}</div></section>}/>
}
function Notifications() {
  return <SimpleWorkspace title="Follow-up planner" eyebrow="NOTIFICATIONS" description="Plan consistent follow-ups from your active pipeline." endpoint="/notifications/plan/" render={data=><section className="panel"><div className="report-grid">{Object.entries(data||{}).map(([k,v])=><div className="report-card" key={k}><span>{k.replaceAll('_',' ')}</span><strong>{typeof v==='object'?JSON.stringify(v):String(v)}</strong></div>)}</div></section>}/>
}
function Tasks() {
  return <SimpleWorkspace title="Career tasks" eyebrow="TASKS" description="Keep resumes, outreach, interviews and follow-ups organized." endpoint="/tasks/" render={data=><section className="panel"><div className="task-list">{(Array.isArray(data)?data:data?.results||[]).map(t=><div className="task" key={t.id}><div><strong>{t.title}</strong><span>{t.description||'No description'}</span></div><span className="badge" data-status={t.status}>{t.priority||t.status}</span></div>)}</div></section>}/>
}

function App() {
  const {authenticated,login,logout}=useAuth();
  const [view,setView]=useState('overview'),[jobs,setJobs]=useState([]),[dashboard,setDashboard]=useState(null),[stats,setStats]=useState(null),[modal,setModal]=useState(null),[error,setError]=useState('');
  const load=async()=>{try{const [j,d,s]=await Promise.all([api.get('/applications/'),api.get('/applications/dashboard/'),api.get('/applications/health_metrics/')]);setJobs(Array.isArray(j.data)?j.data:j.data.results||[]);setDashboard(d.data);setStats(s.data);setError('')}catch(e){if(e.response?.status===401)logout();else setError('Could not connect to the backend. Make sure Django is running.')}};
  useEffect(()=>{if(authenticated)load()},[authenticated]);
  if(!authenticated)return <AuthScreen onLogin={login}/>;
  const nav=[['overview','Overview','⌂'],['applications','Applications','▤'],['fit','Job Fit','◈'],['fit-trends','Fit Trends','⌁'],['health','App Health','◉'],['compensation','Compensation','$'],['contacts','Contacts','◎'],['intelligence','Intelligence','✦'],['reports','Reports','◒'],['tasks','Tasks','✓'],['notifications','Follow-ups','◷'],['review','Weekly Review','✓'],['search-insights','Search Insights','⌕'],['interview-prep','Interview Prep','◷'],['snapshot','Operations','▥'],['comparison','Compare','⇄'],['timeline','Timeline','⌁'],['task-analytics','Task Analytics','▦'],['assets','Asset Readiness','◇'],['explorer','Explorer','⌕'],['workspace-health','Workspace Health','✓']];
  const remove=async id=>{if(confirm('Delete this application?')){await api.delete('/applications/' + id + '/');load()}};
  const save=()=>{setModal(null);load()};
  return <div className="app-shell"><aside className="sidebar"><div className="logo"><span>JT</span><div><strong>JobTrack</strong><small>Career workspace</small></div></div><nav>{nav.map(([id,label,icon])=><button className={view===id?'active':''} key={id} onClick={()=>setView(id)}><span>{icon}</span>{label}</button>)}</nav><div className="sidebar-bottom"><div className="user-mini"><div className="avatar">U</div><div><strong>My workspace</strong><small>Signed in</small></div></div><button className="logout" onClick={logout}>Sign out</button></div></aside>
  <main className="main"><header className="topbar"><div className="mobile-brand">JobTrack</div><div className="connection"><i/> API connected</div><button className="refresh" onClick={load}>↻ Refresh</button></header>{error&&<div className="global-error">{error}</div>}
  {view==='overview'&&<Overview dashboard={dashboard} stats={stats} jobs={jobs} onAdd={()=>setModal({type:'add'})}/>}
  {view==='applications'&&<Applications jobs={jobs} onAdd={()=>setModal({type:'add'})} onEdit={job=>setModal({type:'edit',job})} onDelete={remove} onFit={job=>setModal({type:'fit',job})} onManage={job=>setModal({type:'lifecycle',job})}/>}
  {view==='fit'&&<FitDashboard onOpen={id=>{const job=jobs.find(x=>x.id===id);if(job)setModal({type:'fit',job})}}/>}
  {view==='fit-trends'&&<FitTrends api={api}/>}
  {view==='health'&&<ApplicationHealth api={api}/>}
  {view==='compensation'&&<CompensationDashboard api={api}/>}
  {view==='contacts'&&<ContactIntelligence api={api}/>}
  {view==='intelligence'&&<Intelligence/>}{view==='reports'&&<Reports/>}{view==='review'&&<ReviewWorkspace api={api}/>} {view==='search-insights'&&<SearchInsights api={api}/>} {view==='interview-prep'&&<InterviewPrep api={api}/>} {view==='snapshot'&&<DashboardSnapshot api={api}/>} {view==='comparison'&&<ApplicationComparison api={api}/>} {view==='timeline'&&<ApplicationTimeline api={api}/>} {view==='task-analytics'&&<TaskAnalytics api={api}/>} {view==='assets'&&<AssetReadiness api={api}/>} {view==='explorer'&&<ApplicationExplorer api={api}/>} {view==='workspace-health'&&<WorkspaceHealth api={api}/>}{view==='tasks'&&<Tasks/>}{view==='notifications'&&<Notifications/>}
  </main>
  {modal?.type==='lifecycle'&&<Modal title="Manage application" onClose={()=>setModal(null)}><LifecyclePanel application={modal.job} api={api} onClose={()=>setModal(null)} onChanged={async()=>{setModal(null);await load()}}/></Modal>}
  {modal?.type==='fit'&&<Modal title="Application fit" onClose={()=>setModal(null)}><FitPanel application={modal.job} api={api} onClose={()=>setModal(null)}/></Modal>}
  {modal&&(modal.type==='add'||modal.type==='edit')&&<ApplicationModal job={modal.job} onClose={()=>setModal(null)} onSaved={save}/>}
  </div>;
}
createRoot(document.getElementById('app')).render(<App/>);
