import React from "react";

const STATUS_LABELS = {
  saved: "Saved", applied: "Applied", screening: "Screening",
  interview: "Interview", offer: "Offer", rejected: "Rejected", withdrawn: "Withdrawn",
};

export default function ApplicationCard({ application, onDelete }) {
  const status = STATUS_LABELS[application.status] || application.status;
  const actionDate = application.next_action_date
    ? new Date(application.next_action_date + "T00:00:00").toLocaleDateString()
    : "No date";

  return (
    <article className="job">
      <div className="job-main">
        <div className="job-title-row">
          <h3>{application.role}</h3>
          <span className={"status status-" + application.status}>{status}</span>
        </div>
        <strong>{application.company}</strong>
        <div className="job-meta">
          <span>{application.location || "Location not set"}</span>
          {application.applied_date && <span>Applied {application.applied_date}</span>}
          {application.job_url && (
            <a href={application.job_url} target="_blank" rel="noreferrer">Job post ↗</a>
          )}
        </div>
        {application.notes && <p className="job-notes">{application.notes}</p>}
      </div>
      <aside className="next-action">
        <small>Next action</small>
        <b>{application.next_action || "Nothing scheduled"}</b>
        <span>{application.next_action ? actionDate : "Keep this record updated"}</span>
        {onDelete && (
          <button className="delete-button" onClick={() => onDelete(application)}>Delete</button>
        )}
      </aside>
    </article>
  );
}
