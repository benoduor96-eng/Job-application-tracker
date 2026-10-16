import React, { useState } from 'react';

const panelStyle = { background: 'var(--panel, #fff)', border: '1px solid var(--border, #ddd)', borderRadius: 12, padding: 18, minWidth: 0 };
const fieldStyle = { width: '100%', boxSizing: 'border-box', padding: 10, borderRadius: 8, border: '1px solid #bbb', font: 'inherit' };

export default function CareerTools({ api }) {
  const [resume, setResume] = useState('');
  const [description, setDescription] = useState('');
  const [skills, setSkills] = useState('');
  const [role, setRole] = useState('');
  const [csv, setCsv] = useState('company,title,url\nExample Co,Data Analyst,https://jobs.example/role');
  const [analysis, setAnalysis] = useState(null);
  const [questions, setQuestions] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState('');

  const run = async (key, fn) => {
    setBusy(key); setError('');
    try { await fn(); } catch (e) {
      setError(e.response?.data?.detail || 'The request failed. Check that you are signed in and the backend is running.');
    } finally { setBusy(''); }
  };
  const analyze = () => run('analysis', async () => {
    const r = await api.post('/career-assistant/analyze/', {
      resume_text: resume, job_description: description,
      skills: skills.split(',').map(s => s.trim()).filter(Boolean)
    });
    setAnalysis(r.data);
  });
  const makeQuestions = () => run('questions', async () => {
    const r = await api.post('/career-assistant/interview-kit/', {
      role, skills: skills.split(',').map(s => s.trim()).filter(Boolean), count: 12
    });
    setQuestions(r.data);
  });
  const previewJobs = () => run('preview', async () => {
    const r = await api.post('/integrations/jobs/normalize/', { csv });
    setPreview(r.data);
  });
  const exportData = () => run('export', async () => {
    const r = await api.get('/account/export/', { responseType: 'blob' });
    const url = URL.createObjectURL(r.data);
    const anchor = document.createElement('a');
    anchor.href = url; anchor.download = 'job-tracker-personal-data.json';
    document.body.appendChild(anchor); anchor.click(); anchor.remove(); URL.revokeObjectURL(url);
  });

  return <div className="workspace">
    <div className="page-head"><div><span className="eyebrow">CAREER TOOLKIT</span><h2>Career assistant & integrations</h2>
      <p className="muted">Review your resume, prepare for interviews, preview job imports, and export your data.</p></div></div>
    {error && <div className="alert error" role="alert">{error}</div>}
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(280px,1fr))', gap: 16 }}>
      <section style={panelStyle} aria-labelledby="career-review-title">
        <h3 id="career-review-title">Resume and job-fit review</h3>
        <label>Resume text<textarea style={fieldStyle} rows={5} value={resume} onChange={e=>setResume(e.target.value)} placeholder="Paste resume text for a local checklist."/></label>
        <label style={{display:'block',marginTop:12}}>Job description<textarea style={fieldStyle} rows={5} value={description} onChange={e=>setDescription(e.target.value)} placeholder="Paste a job description to review skill keywords."/></label>
        <label style={{display:'block',marginTop:12}}>Your skills (comma-separated)<input style={fieldStyle} value={skills} onChange={e=>setSkills(e.target.value)} placeholder="Python, SQL, customer support"/></label>
        <button style={{marginTop:12}} disabled={!!busy || (!resume.trim() && !description.trim())} onClick={analyze}>{busy==='analysis'?'Reviewing…':'Review text'}</button>
        {analysis && <div style={{marginTop:16}} aria-live="polite">
          {analysis.resume_review && <><h4>Resume checklist</h4><p>{analysis.resume_review.word_count} words · {analysis.resume_review.bullet_count} bullets</p><ul>{analysis.resume_review.suggestions.map(s=><li key={s}>{s}</li>)}</ul></>}
          {analysis.job_fit_review && <><h4>Skill overlap</h4><p>Coverage: {analysis.job_fit_review.required_coverage_percent ?? 'Not available'}%</p><p>Matched: {analysis.job_fit_review.required_matches.join(', ') || 'None identified'}</p><p>Potential gaps: {analysis.job_fit_review.missing_required.join(', ') || 'No gaps identified by keyword comparison'}</p></>}
          <small>{analysis.limitations}</small>
        </div>}
      </section>
      <section style={panelStyle} aria-labelledby="interview-kit-title">
        <h3 id="interview-kit-title">Interview question builder</h3>
        <label>Target role<input style={fieldStyle} value={role} onChange={e=>setRole(e.target.value)} placeholder="e.g. Junior Data Analyst"/></label>
        <p className="muted">Uses the skills entered in the review panel above.</p>
        <button disabled={!!busy} onClick={makeQuestions}>{busy==='questions'?'Preparing…':'Generate practice questions'}</button>
        {questions && <ol style={{paddingLeft:22}}>{questions.questions.map((q,i)=><li key={q.category+'-'+i} style={{margin:'10px 0'}}><strong>{q.category}</strong>: {q.question}</li>)}</ol>}
      </section>
      <section style={panelStyle} aria-labelledby="job-import-title">
        <h3 id="job-import-title">Job import preview</h3>
        <p className="muted">Paste CSV text with company, title, and url columns. This validates rows only; it does not create applications automatically.</p>
        <textarea style={fieldStyle} rows={6} value={csv} onChange={e=>setCsv(e.target.value)} aria-label="Job listings CSV"/>
        <button style={{marginTop:12}} disabled={!!busy || !csv.trim()} onClick={previewJobs}>{busy==='preview'?'Validating…':'Validate CSV'}</button>
        {preview && <div aria-live="polite"><p>Accepted: {preview.accepted} · Rejected: {preview.rejected}</p>{preview.errors?.length>0&&<ul>{preview.errors.map(e=><li key={e.line}>Line {e.line}: {e.error}</li>)}</ul>}<ul>{preview.records?.map(r=><li key={r.line}>{r.job.company} — {r.job.role}</li>)}</ul></div>}
      </section>
      <section style={panelStyle} aria-labelledby="privacy-export-title">
        <h3 id="privacy-export-title">Your data</h3>
        <p>Export the applications, interviews, contacts, resumes, tasks, job descriptions, activity history and saved searches associated with your account.</p>
        <button disabled={!!busy} onClick={exportData}>{busy==='export'?'Preparing export…':'Export my data (JSON)'}</button>
        <p className="muted" style={{fontSize:13}}>Review the exported file before sharing it. It may contain personal and job-search information.</p>
      </section>
    </div>
    <p className="muted" style={{marginTop:16}}>Career reviews are rule-based guidance, not hiring predictions. Text is processed locally by the backend helpers and is not sent to an external AI provider.</p>
  </div>;
}
