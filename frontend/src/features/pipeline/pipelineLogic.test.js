import test from 'node:test';
import assert from 'node:assert/strict';
import {
  STATUSES, groupByStatus, moveApplication, daysSince, isStale,
  columnSummary, filterApplications, formatSalaryRange,
} from './pipelineLogic.js';

const TODAY = new Date(2026, 9, 1);

const apps = [
  { id: 1, company: 'Acme', role: 'Backend Engineer', location: 'Remote', status: 'applied', applied_date: '2026-09-10', salary_min: 120000, salary_max: 160000 },
  { id: 2, company: 'Globex', role: 'Data Analyst', location: 'Nairobi', status: 'interview', applied_date: '2026-09-28', salary_min: '90000', salary_max: '' },
  { id: 3, company: 'Initech', role: 'SRE', location: 'London', status: 'saved', applied_date: null, salary_min: null, salary_max: null },
  { id: 4, company: 'Hooli', role: 'Frontend Engineer', location: 'Remote', status: 'rejected', applied_date: '2026-08-01' },
];

test('groupByStatus creates every column and places applications', () => {
  const g = groupByStatus(apps);
  assert.deepEqual(Object.keys(g), STATUSES);
  assert.equal(g.applied.length, 1);
  assert.equal(g.offer.length, 0);
});

test('groupByStatus ignores unknown statuses and handles empty input', () => {
  const g = groupByStatus([{ id: 9, status: 'mystery' }]);
  assert.ok(Object.values(g).every((list) => list.length === 0));
  assert.equal(groupByStatus(undefined).saved.length, 0);
});

test('moveApplication returns a new list with the updated status', () => {
  const next = moveApplication(apps, 1, 'interview');
  assert.equal(next.find((a) => a.id === 1).status, 'interview');
  assert.equal(apps.find((a) => a.id === 1).status, 'applied');
});

test('moveApplication is a no-op for same status, bad status or unknown id', () => {
  assert.equal(moveApplication(apps, 1, 'applied'), apps);
  assert.equal(moveApplication(apps, 1, 'nonsense'), apps);
  assert.equal(moveApplication(apps, 999, 'offer'), apps);
});

test('daysSince counts whole days and rejects bad input', () => {
  assert.equal(daysSince('2026-09-21', TODAY), 10);
  assert.equal(daysSince('2026-10-01', TODAY), 0);
  assert.equal(daysSince(null, TODAY), null);
  assert.equal(daysSince('not-a-date', TODAY), null);
});

test('isStale only flags waiting applications past the threshold', () => {
  assert.equal(isStale(apps[0], TODAY), true);
  assert.equal(isStale(apps[1], TODAY), false);
  assert.equal(isStale(apps[2], TODAY), false);
  assert.equal(isStale(apps[3], TODAY), false);
  assert.equal(isStale(apps[0], TODAY, 30), false);
});

test('columnSummary averages salaries and ignores blanks', () => {
  const s = columnSummary([apps[0], apps[1]]);
  assert.equal(s.count, 2);
  assert.equal(s.avgSalaryMin, 105000);
  assert.equal(s.avgSalaryMax, 160000);
  const empty = columnSummary([]);
  assert.deepEqual(empty, { count: 0, avgSalaryMin: null, avgSalaryMax: null });
});

test('filterApplications matches company, role and location', () => {
  assert.equal(filterApplications(apps, 'remote').length, 2);
  assert.equal(filterApplications(apps, '  ACME ').length, 1);
  assert.equal(filterApplications(apps, '').length, apps.length);
  assert.equal(filterApplications(apps, 'zzz').length, 0);
});

test('formatSalaryRange handles full, partial and missing values', () => {
  assert.equal(formatSalaryRange(120000, 160000), '120k–160k');
  assert.equal(formatSalaryRange('90000', ''), '90k+');
  assert.equal(formatSalaryRange(null, 80000), 'up to 80k');
  assert.equal(formatSalaryRange(null, null), '');
  assert.equal(formatSalaryRange(500, 900), '500–900');
});
