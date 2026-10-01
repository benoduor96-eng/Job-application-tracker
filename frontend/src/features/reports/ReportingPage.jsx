import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ReportingPage() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get("/api/reporting/dashboard/", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token") || ""}`,
          },
        });
        setSummary(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div>Loading report...</div>;
  if (!summary) return <div>No report available.</div>;

  return (
    <div className="reporting-page">
      <h2>Application Reporting</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <label>Total</label>
          <strong>{summary.total_applications}</strong>
        </div>
        <div className="stat-card">
          <label>Active</label>
          <strong>{summary.active_applications}</strong>
        </div>
        <div className="stat-card">
          <label>Interviews</label>
          <strong>{summary.interviews}</strong>
        </div>
        <div className="stat-card">
          <label>Offers</label>
          <strong>{summary.offers}</strong>
        </div>
      </div>

      <div className="status-table">
        {summary.by_status?.map((item) => (
          <div key={item.status} className="status-row">
            <span>{item.status}</span>
            <strong>{item.total}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}
