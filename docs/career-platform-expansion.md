# Career platform expansion

This branch adds tested domain helpers around lifecycle governance, duplicate review,
structured search, privacy review, and cohort analytics. The functions are intentionally
kept outside the HTTP layer so the existing Django API can call them without adding a
second backend or a second source of truth.

## Added modules

- \`backend/apps/jobs/workflow_policy.py\`: allowed status transitions, reason-required
  transitions, bulk-transition preflight, follow-up SLAs, reminder ordering, and history
  consistency checks.
- \`backend/apps/jobs/duplicate_resolution.py\`: URL canonicalization, employer/title
  normalization, explainable similarity features, candidate ranking, and a non-destructive
  merge preview.
- \`backend/apps/jobs/search_language.py\`: bounded search parser with quoted phrases,
  field filters, date filters, salary comparisons, exclusions, explainability, and ranking.
- \`backend/apps/jobs/privacy_lifecycle.py\`: export manifests, recursive secret/personal
  data redaction, retention review reports, and export-option validation.
- \`backend/apps/jobs/analytics_cohorts.py\`: application funnel summaries, weekly counts,
  response lag, source performance, salary summaries, company rollups, cohorts, and quality
  checks.
- \`backend/apps/jobs/tests/test_expansion_services.py\`: unit tests for domain edge cases.

## Safety and correctness boundaries

These services do not delete, merge, or change database rows. A caller must authorize the
user, check ownership, show a preview, and persist changes in a transaction only after an
explicit user action. Similarity scores are review aids, not proof that records are duplicates.
Search terms are parsed against an allowlist and never evaluated as Python or SQL text.
Retention decisions only mark records as eligible for review; they never automatically delete
personal data.

Analytics use the fields supplied by the caller. If the underlying schema does not record a
first-response timestamp or job source, the corresponding metrics will be incomplete or will
use a documented fallback. Salary summaries must not combine different currencies or pay
periods without conversion metadata.

## Run tests

From the backend directory:

\`\`\`bash
DJANGO_DB_ENGINE=sqlite pytest -q apps/jobs/tests/test_expansion_services.py
\`\`\`

The existing CI pipeline remains the authoritative integration check. These new pure helper
modules have not been deployed as new public API endpoints in this change.
