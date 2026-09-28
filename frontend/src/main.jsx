import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import axios from "axios";
import ApplicationCard from "./components/ApplicationCard";
import ApplicationForm from "./components/ApplicationForm";
import DashboardStats from "./components/DashboardStats";
import "./styles.css";

const STATUSES = ["saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"];

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

function App() {
  const [jobs, setJobs] = useState([]);
  const [dashboard, setDashboard] = useState(null);
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [applications, summary] = await Promise.all([
        api.get("/applications/", { params: { q: search, status: filter === "all" ? undefined : filter } }),
        api.get("/applications/dashboard/"),
      ]);
      setJobs(applications.data);
      setDashboard(summary.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load applications.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [filter]);

  const filteredJobs = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return jobs;
    return jobs.filter((job) =>
      [job.company, job.role, job.location, job.notes].some(
        (value) => value && value.toLowerCase().includes(query)
      )
    );
  }, [jobs, search]);

  const addApplication = (application) => {
    setJobs((current) => [application, ...current]);
    setDashboard((current) => current ? { ...current, total: current.total + 1 } : current);
  };

  const deleteApplication = async (application) => {
    if (!window.confirm("Delete this application?")) return;
    try {
      await api.delete("/applications/" + application.id + "/");
      setJobs((current) => current.filter((item) => item.id !== application.id));
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete the application.");
    }
  };

  return (
    <main>
      <header>
        <div>
          <p className="eyebrow">CAREER COMMAND CENTER</p>
          <h1>Job Application Tracker</h1>
          <p>Track applications, interviews, follow-ups and offers from one dashboard.</p>
        </div>
        <div className="header-actions">
          <span className="live-dot">LIVE PIPELINE</span>
          <button className="refresh-button" onClick={load} disabled={loading}>
            {loading ? "Refreshing..." : "Refresh"}
          </button>
        </div>
      </header>

      <DashboardStats dashboard={dashboard} />

      {error && <div className="alert" role="alert">{error}</div>}

      <section className="grid">
        <ApplicationForm api={api} onCreated={addApplication} />
        <section className="card pipeline-card">
          <div className="toolbar">
            <div>
              <p className="section-kicker">APPLICATION PIPELINE</p>
              <h2>Your applications</h2>
            </div>
            <select value={filter} onChange={(event) => setFilter(event.target.value)}>
              <option value="all">All statuses</option>
              {STATUSES.map((status) => <option key={status} value={status}>{status}</option>)}
            </select>
          </div>

          <label className="search-box">
            <span>Search</span>
            <input value={search} onChange={(event) => setSearch(event.target.value)}
              onKeyDown={(event) => event.key === "Enter" && load()}
              placeholder="Company, role, location or notes" />
          </label>

          {loading ? (
            <p className="empty">Loading your pipeline...</p>
          ) : filteredJobs.length ? (
            <div className="list">
              {filteredJobs.map((job) => (
                <ApplicationCard key={job.id} application={job} onDelete={deleteApplication} />
              ))}
            </div>
          ) : (
            <div className="empty">
              <strong>No applications found.</strong>
              <p>Try another search or add your first application.</p>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
