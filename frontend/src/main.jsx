import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';
import './styles.css';
import CareerIntelligence from './features/intelligence/CareerIntelligence';

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
  const [showModal, setShowModal] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [formData, setFormData] = useState({
    company: '',
    role: '',
    location: '',
    job_url: '',
    status: 'saved',
    salary_min: '',
    salary_max: '',
    applied_date: '',
    next_action: '',
    next_action_date: '',
    notes: ''
  });

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

  const handleOpenModal = (job = null) => {
    if (job) {
      setEditingJob(job);
      setFormData({ ...job });
    } else {
      setEditingJob(null);
      setFormData({
        company: '',
        role: '',
        location: '',
        job_url: '',
        status: 'saved',
        salary_min: '',
        salary_max: '',
        applied_date: '',
        next_action: '',
        next_action_date: '',
        notes: ''
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingJob(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingJob) {
        await api.put(`/applications/${editingJob.id}/`, formData);
      } else {
        await api.post('/applications/', formData);
      }
      handleCloseModal();
      fetchJobs();
      fetchDashboard();
    } catch (error) {
      console.error('Failed to save application', error);
    }
  };

  const handleDelete = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this application?')) {
      try {
        await api.delete(`/applications/${jobId}/`);
        fetchJobs();
        fetchDashboard();
      } catch (error) {
        console.error('Failed to delete application', error);
      }
    }
  };

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
        <button onClick={() => handleOpenModal()} className="btn-primary">+ Add Application</button>
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
              <div className="col-actions">Actions</div>
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
                <div className="col-actions">
                  <button onClick={() => handleOpenModal(job)} className="btn-small">Edit</button>
                  <button onClick={() => handleDelete(job.id)} className="btn-small btn-danger">Delete</button>
                </div>
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

      <CareerIntelligence />

      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingJob ? 'Edit Application' : 'Add New Application'}</h2>
              <button onClick={handleCloseModal} className="close-btn">×</button>
            </div>
            <form onSubmit={handleSubmit} className="modal-form">
              <div className="form-group">
                <label>Company *</label>
                <input type="text" name="company" value={formData.company} onChange={handleInputChange} required className="form-input" />
              </div>
              <div className="form-group">
                <label>Role *</label>
                <input type="text" name="role" value={formData.role} onChange={handleInputChange} required className="form-input" />
              </div>
              <div className="form-group">
                <label>Location</label>
                <input type="text" name="location" value={formData.location} onChange={handleInputChange} className="form-input" />
              </div>
              <div className="form-group">
                <label>Job URL</label>
                <input type="url" name="job_url" value={formData.job_url} onChange={handleInputChange} className="form-input" />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Status</label>
                  <select name="status" value={formData.status} onChange={handleInputChange} className="form-input">
                    <option value="saved">Saved</option>
                    <option value="applied">Applied</option>
                    <option value="screening">Screening</option>
                    <option value="interview">Interview</option>
                    <option value="offer">Offer</option>
                    <option value="rejected">Rejected</option>
                    <option value="withdrawn">Withdrawn</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Applied Date</label>
                  <input type="date" name="applied_date" value={formData.applied_date} onChange={handleInputChange} className="form-input" />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Salary Min</label>
                  <input type="number" name="salary_min" value={formData.salary_min} onChange={handleInputChange} className="form-input" />
                </div>
                <div className="form-group">
                  <label>Salary Max</label>
                  <input type="number" name="salary_max" value={formData.salary_max} onChange={handleInputChange} className="form-input" />
                </div>
              </div>
              <div className="form-group">
                <label>Next Action</label>
                <input type="text" name="next_action" value={formData.next_action} onChange={handleInputChange} className="form-input" />
              </div>
              <div className="form-group">
                <label>Follow-up Date</label>
                <input type="date" name="next_action_date" value={formData.next_action_date} onChange={handleInputChange} className="form-input" />
              </div>
              <div className="form-group">
                <label>Notes</label>
                <textarea name="notes" value={formData.notes} onChange={handleInputChange} className="form-textarea" rows="4" />
              </div>
              <div className="modal-footer">
                <button type="button" onClick={handleCloseModal} className="btn-secondary">Cancel</button>
                <button type="submit" className="btn-primary">Save Application</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

const root = createRoot(document.getElementById('app'));
root.render(<Dashboard />);
