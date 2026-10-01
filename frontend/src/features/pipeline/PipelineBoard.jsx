import React, { useEffect, useMemo, useState } from 'react';
import {
  STATUSES,
  STATUS_LABELS,
  groupByStatus,
  moveApplication,
  columnSummary,
  filterApplications,
  isStale,
  formatSalaryRange,
} from './pipelineLogic.js';
import './pipeline.css';

/**
 * Kanban board for the application pipeline.
 *
 * Props:
 *   jobs      - array of applications from GET /applications/
 *   api       - the authenticated axios instance from main.jsx
 *   onChanged - called after a successful status change (e.g. reload data)
 *   onEdit    - called with an application when its Edit button is clicked
 */
export default function PipelineBoard({ jobs, api, onChanged, onEdit }) {
  const [items, setItems] = useState(jobs || []);
  const [query, setQuery] = useState('');
  const [dragId, setDragId] = useState(null);
  const [overColumn, setOverColumn] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => { setItems(jobs || []); }, [jobs]);

  const today = useMemo(() => new Date(), []);
  const groups = useMemo(
    () => groupByStatus(filterApplications(items, query)),
    [items, query],
  );

  async function changeStatus(id, newStatus) {
    const previous = items;
    const next = moveApplication(items, id, newStatus);
    if (next === previous) return;
    setItems(next);
    setError('');
    try {
      await api.patch(`/applications/${id}/`, { status: newStatus });
      if (onChanged) onChanged();
    } catch (err) {
      setItems(previous);
      setError('Could not move that application. Your change was reverted.');
    }
  }

  function handleDrop(event, status) {
    event.preventDefault();
    const id = Number(event.dataTransfer.getData('text/plain')) || dragId;
    setOverColumn(null);
    setDragId(null);
    if (id) changeStatus(id, status);
  }

  return (
    <div className="workspace pipeline-board">
      <div className="page-head">
        <div>
          <span className="eyebrow">PIPELINE</span>
          <h2>Pipeline board</h2>
          <p className="muted">Drag cards between stages, or use the menu on each card.</p>
        </div>
        <input
          className="search"
          placeholder="Filter by company, role or location…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Filter applications"
        />
      </div>

      {error && <div className="alert error" role="alert">{error}</div>}

      <div className="board-scroll">
        <div className="board">
          {STATUSES.map((status) => {
            const cards = groups[status];
            const summary = columnSummary(cards);
            const salary = formatSalaryRange(summary.avgSalaryMin, summary.avgSalaryMax);
            return (
              <section
                key={status}
                className={`board-column${overColumn === status ? ' is-over' : ''}`}
                onDragOver={(e) => { e.preventDefault(); setOverColumn(status); }}
                onDragLeave={() => setOverColumn((c) => (c === status ? null : c))}
                onDrop={(e) => handleDrop(e, status)}
                aria-label={`${STATUS_LABELS[status]} column`}
              >
                <header className="column-head">
                  <span className="status-dot" data-status={status} />
                  <h3>{STATUS_LABELS[status]}</h3>
                  <span className="column-count">{summary.count}</span>
                </header>
                {salary && <div className="column-meta">Avg salary {salary}</div>}

                <div className="column-cards">
                  {cards.map((app) => (
                    <article
                      key={app.id}
                      className={`board-card${dragId === app.id ? ' is-dragging' : ''}`}
                      draggable
                      onDragStart={(e) => {
                        e.dataTransfer.setData('text/plain', String(app.id));
                        e.dataTransfer.effectAllowed = 'move';
                        setDragId(app.id);
                      }}
                      onDragEnd={() => { setDragId(null); setOverColumn(null); }}
                    >
                      <strong>{app.role}</strong>
                      <span className="card-company">{app.company}</span>
                      {formatSalaryRange(app.salary_min, app.salary_max) && (
                        <span className="card-salary">
                          {formatSalaryRange(app.salary_min, app.salary_max)}
                        </span>
                      )}
                      {app.next_action_date && (
                        <span className="card-next">
                          Next: {app.next_action || 'follow up'} · {app.next_action_date}
                        </span>
                      )}
                      {isStale(app, today) && <span className="stale-badge">Needs follow-up</span>}
                      <div className="card-actions">
                        <select
                          value={app.status}
                          onChange={(e) => changeStatus(app.id, e.target.value)}
                          aria-label={`Move ${app.role} at ${app.company}`}
                        >
                          {STATUSES.map((s) => (
                            <option key={s} value={s}>{STATUS_LABELS[s]}</option>
                          ))}
                        </select>
                        {onEdit && <button onClick={() => onEdit(app)}>Edit</button>}
                      </div>
                    </article>
                  ))}
                  {!cards.length && <div className="column-empty">Nothing here</div>}
                </div>
              </section>
            );
          })}
        </div>
      </div>
    </div>
  );
}
