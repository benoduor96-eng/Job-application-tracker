import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';
import './styles.css';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
});

function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchDashboard();
    fetchJobs();
    fetchStats();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await api.get('/applications/dashboard/');
      setDashboard(response.data);
    } catch (error) {
      console.error('Failed to fetch dashboard', error);
    }
  };

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const params = {};
      if (searchQuery) params.q = searchQuery;
      if (filter !== 'all') params.status = filter;
      const response = await api.get('/applications/', { params });
      setJobs(response.data);
    } catch (error) {
      console.error('Failed to fetch jobs', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await api.get('/applications/health_metrics/');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats', error);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [filter, searchQuery]);

  const getStatusColor = (status) => {
    const colors = {
      saved: '#9CA3AF',
      applied: '#3B82F6',
      screening: '#F59E0B',
      interview: '#8B5CF6',
      offer: '#10B981',
      rejected: '#EF4444',
      withdrawn: '#6B7280'
    };
    return colors[status] || '#6B7280';
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="dashboard">
      <header className="header">
        <h1>Job Application Tracker</h1>
        <p>Manage your job search pipeline</p>
      </header>

      {dashboard && (
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-value">{dashboard.total}</div>
            <div className="metric-label">Total Applications</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{dashboard.active}</div>
            <div className="metric-label">Active Pipeline</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{dashboard.interviews}</div>
            <div className="metric-label">Interviews</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{dashboard.offers}</div>
            <div className="metric-label">Offers</div>
          </div>
        </div>
      )}

      {stats && (
        <div className="stats-section">
          <h2>Pipeline Health</h2>
          <div className="stats-row">
            <div className="stat-item">
              <span className="stat-label">Interview Rate:</span>
              <span className="stat-value">{stats.interview_rate}%</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Offer Rate:</span>
              <span className="stat-value">{stats.offer_rate}%</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Screening Rate:</span>
              <span className="stat-value">{stats.screening_rate}%</span>
            </div>
          </div>
        </div>
      )}

      <div className="controls">
        <input
          type="text"
          placeholder="Search by company, role, or location..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-input"
        />
        <select value={filter} onChange={(e) => setFilter(e.target.value)} className="filter-select">
          <option value="all">All Statuses</option>
          <option value="saved">Saved</option>
          <option value="applied">Applied</option>
          <option value="screening">Screening</option>
          <option value="interview">Interview</option>
          <option value="offer">Offer</option>
          <option value="rejected">Rejected</option>
          <option value="withdrawn">Withdrawn</option>
        </select>
      </div>

      <div className="jobs-section">
        <h2>Applications</h2>
        {loading ? (
          <p className="loading">Loading...</p>
        ) : jobs.length === 0 ? (
          <p className="empty-state">No applications found</p>
        ) : (
          <div className="jobs-table">
            <div className="table-header">
              <div className="col-company">Company</div>
              <div className="col-role">Role</div>
              <div className="col-location">Location</div>
              <div className="col-status">Status</div>
              <div className="col-applied">Applied</div>
              <div className="col-followup">Follow-up</div>
            </div>
            {jobs.map((job) => (
              <div key={job.id} className="table-row">
                <div className="col-company">{job.company}</div>
                <div className="col-role">{job.role}</div>
                <div className="col-location">{job.location || '-'}</div>
                <div className="col-status">
                  <span className="status-badge" style={{ backgroundColor: getStatusColor(job.status) }}>
                    {job.status}
                  </span>
                </div>
                <div className="col-applied">{formatDate(job.applied_date)}</div>
                <div className="col-followup">{formatDate(job.next_action_date)}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {dashboard && dashboard.upcoming && dashboard.upcoming.length > 0 && (
        <div className="upcoming-section">
          <h2>Upcoming Follow-ups</h2>
          <div className="upcoming-list">
            {dashboard.upcoming.map((job) => (
              <div key={job.id} className="upcoming-item">
                <div className="upcoming-date">{formatDate(job.next_action_date)}</div>
                <div className="upcoming-details">
                  <strong>{job.company}</strong> - {job.role}
                  <p>{job.next_action}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const root = createRoot(document.getElementById('app'));
root.render(<Dashboard />);
