import React, { useState } from "react";

const STATUSES = ["saved", "applied", "screening", "interview", "offer", "rejected", "withdrawn"];
const EMPTY_FORM = {
  company: "", role: "", location: "", status: "saved", job_url: "",
  salary_min: "", salary_max: "", applied_date: "",
  next_action: "", next_action_date: "", notes: "",
};

function Field({ label, name, value, onChange, type = "text", required = false }) {
  return (
    <label className="field">
      <span>{label}</span>
      <input name={name} type={type} value={value} required={required}
        onChange={onChange} placeholder={label} />
    </label>
  );
}

export default function ApplicationForm({ onCreated, api }) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const update = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const payload = { ...form };
      ["salary_min", "salary_max"].forEach((key) => {
        if (payload[key] === "") delete payload[key];
      });
      Object.keys(payload).forEach((key) => {
        if (payload[key] === "") payload[key] = null;
      });
      const result = await api.post("/applications/", payload);
      onCreated(result.data);
      setForm(EMPTY_FORM);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not save the application.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <form className="card application-form" onSubmit={submit}>
      <div className="card-heading">
        <div><p className="section-kicker">NEW RECORD</p><h2>Add application</h2></div>
        <span className="form-dot" aria-hidden="true" />
      </div>
      {error && <p className="form-error">{error}</p>}
      <Field label="Company" name="company" value={form.company} onChange={update} required />
      <Field label="Role" name="role" value={form.role} onChange={update} required />
      <Field label="Location" name="location" value={form.location} onChange={update} />
      <Field label="Job URL" name="job_url" value={form.job_url} onChange={update} type="url" />
      <div className="two-fields">
        <Field label="Salary min" name="salary_min" value={form.salary_min} onChange={update} type="number" />
        <Field label="Salary max" name="salary_max" value={form.salary_max} onChange={update} type="number" />
      </div>
      <div className="two-fields">
        <Field label="Applied date" name="applied_date" value={form.applied_date} onChange={update} type="date" />
        <label className="field"><span>Status</span><select name="status" value={form.status} onChange={update}>
          {STATUSES.map((status) => <option key={status} value={status}>{status}</option>)}
        </select></label>
      </div>
      <Field label="Next action" name="next_action" value={form.next_action} onChange={update} />
      <Field label="Next action date" name="next_action_date" value={form.next_action_date} onChange={update} type="date" />
      <label className="field"><span>Notes</span><textarea name="notes" value={form.notes}
        onChange={update} placeholder="Interview notes, contacts, reminders..." /></label>
      <button disabled={saving}>{saving ? "Saving..." : "Add application"}</button>
    </form>
  );
}
