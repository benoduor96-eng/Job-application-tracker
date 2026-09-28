import React from "react";

const ITEMS = [
  ["total", "Tracked"],
  ["active", "Active"],
  ["interviews", "Interviews"],
  ["offers", "Offers"],
];

export default function DashboardStats({ dashboard }) {
  if (!dashboard) return null;

  return (
    <section className="stats-grid" aria-label="Application statistics">
      {ITEMS.map(([key, label]) => (
        <article className="stat-card" key={key}>
          <span>{label}</span>
          <strong>{dashboard[key] ?? 0}</strong>
        </article>
      ))}
    </section>
  );
}
