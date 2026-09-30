import React, { useEffect, useState } from "react";
import axios from "axios";
import "./notifications.css";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
});

export default function NotificationPlanner() {
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function loadPlan() {
    setLoading(true);
    setMessage("");
    try {
      const response = await api.get("/notifications/plan/");
      setPlan(response.data);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Unable to load notification plan.");
    } finally {
      setLoading(false);
    }
  }

  async function createTasks() {
    setLoading(true);
    setMessage("");
    try {
      const response = await api.post("/notifications/plan/");
      setPlan(response.data);
      setMessage(`${response.data.task_ids.length} follow-up tasks are ready.`);
    } catch (error) {
      setMessage(error.response?.data?.detail || "Unable to create follow-up tasks.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadPlan();
  }, []);

  return (
    <section className="notification-planner">
      <div className="notification-heading">
        <div>
          <p className="eyebrow">Workflow automation</p>
          <h2>Follow-up planner</h2>
          <p className="muted">
            Turn active applications into dated follow-up tasks without creating duplicates.
          </p>
        </div>
        <div className="notification-actions">
          <button className="btn-secondary" onClick={loadPlan} disabled={loading}>
            Refresh
          </button>
          <button className="btn-primary" onClick={createTasks} disabled={loading}>
            Create tasks
          </button>
        </div>
      </div>

      {message && <div className="notification-message">{message}</div>}

      {plan && (
        <>
          <div className="notification-summary">
            <div>
              <strong>{plan.summary.count}</strong>
              <span>planned actions</span>
            </div>
            <div>
              <strong>{plan.summary.by_priority?.high || 0}</strong>
              <span>high priority</span>
            </div>
            <div>
              <strong>{plan.summary.by_priority?.medium || 0}</strong>
              <span>medium priority</span>
            </div>
          </div>

          <div className="notification-list">
            {plan.plans.length === 0 ? (
              <p className="muted">No follow-up actions are currently due.</p>
            ) : (
              plan.plans.map((item) => (
                <article className="notification-item" key={`${item.application_id}-${item.due_at}`}>
                  <div>
                    <strong>{item.action}</strong>
                    <p>{item.reason}</p>
                  </div>
                  <div className={`notification-priority ${item.priority}`}>
                    {item.priority}
                  </div>
                  <time dateTime={item.due_at}>
                    {new Date(item.due_at).toLocaleString()}
                  </time>
                </article>
              ))
            )}
          </div>
        </>
      )}
    </section>
  );
}
