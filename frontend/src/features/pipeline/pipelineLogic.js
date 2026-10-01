// Pure helpers for the Kanban pipeline board. No React or network code here,
// so everything in this file can be unit tested with `node --test`.

export const STATUSES = [
  'saved', 'applied', 'screening', 'interview', 'offer', 'rejected', 'withdrawn',
];

export const STATUS_LABELS = {
  saved: 'Saved',
  applied: 'Applied',
  screening: 'Screening',
  interview: 'Interview',
  offer: 'Offer',
  rejected: 'Rejected',
  withdrawn: 'Withdrawn',
};

export const TERMINAL_STATUSES = ['rejected', 'withdrawn'];
export const WAITING_STATUSES = ['applied', 'screening', 'interview'];

const MS_PER_DAY = 24 * 60 * 60 * 1000;

export function groupByStatus(applications, statuses = STATUSES) {
  const groups = Object.fromEntries(statuses.map((s) => [s, []]));
  for (const app of applications || []) {
    if (groups[app.status]) groups[app.status].push(app);
  }
  return groups;
}

export function moveApplication(applications, id, newStatus) {
  if (!STATUSES.includes(newStatus)) return applications;
  let changed = false;
  const next = applications.map((app) => {
    if (app.id === id && app.status !== newStatus) {
      changed = true;
      return { ...app, status: newStatus };
    }
    return app;
  });
  return changed ? next : applications;
}

export function daysSince(dateString, today = new Date()) {
  if (!dateString) return null;
  const date = new Date(`${dateString}T00:00:00`);
  if (Number.isNaN(date.getTime())) return null;
  const start = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  return Math.round((start - date) / MS_PER_DAY);
}

export function isStale(application, today = new Date(), thresholdDays = 14) {
  if (!WAITING_STATUSES.includes(application.status)) return false;
  const days = daysSince(application.applied_date, today);
  return days !== null && days > thresholdDays;
}

function toNumber(value) {
  if (value === null || value === undefined || value === '') return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function average(values) {
  return values.length ? values.reduce((a, b) => a + b, 0) / values.length : null;
}

export function columnSummary(applications) {
  const mins = applications.map((a) => toNumber(a.salary_min)).filter((n) => n !== null);
  const maxes = applications.map((a) => toNumber(a.salary_max)).filter((n) => n !== null);
  return {
    count: applications.length,
    avgSalaryMin: average(mins),
    avgSalaryMax: average(maxes),
  };
}

export function filterApplications(applications, query) {
  const q = (query || '').trim().toLowerCase();
  if (!q) return applications;
  return applications.filter((a) =>
    `${a.company || ''} ${a.role || ''} ${a.location || ''}`.toLowerCase().includes(q),
  );
}

function shortNumber(n) {
  return n >= 1000 ? `${Math.round(n / 1000)}k` : String(Math.round(n));
}

export function formatSalaryRange(min, max) {
  const lo = toNumber(min);
  const hi = toNumber(max);
  if (lo !== null && hi !== null) return `${shortNumber(lo)}–${shortNumber(hi)}`;
  if (lo !== null) return `${shortNumber(lo)}+`;
  if (hi !== null) return `up to ${shortNumber(hi)}`;
  return '';
}
