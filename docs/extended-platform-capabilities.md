# Extended platform capabilities

This change supplements existing application management, reporting, interview
preparation, contacts, career assets, planning, matching, and CSV import/export.
It adds distinct tools rather than duplicating those modules.

## New capabilities

- **Career assistant:** a local, deterministic resume checklist, role-based
  interview question builder, and transparent skill keyword comparison.
- **Job listing adapters:** normalization for generic records and common
  Greenhouse-shaped and Lever-shaped public payloads.
- **Import preflight:** CSV validation with row-level errors and limits. Preview
  is deliberately separate from persisting an application.
- **Personal data export:** authenticated JSON export for the signed-in user's
  applications, interviews, contacts, profile, resumes, tasks, descriptions,
  activity records, and saved searches.
- **React Career Toolkit:** UI for resume/job review, interview questions, CSV
  preview, and data export.
- **Tests:** unit and API tests cover input validation, adapters, authentication,
  import preflight, and export scoping.

## API endpoints

- POST /api/career-assistant/analyze/
  - JSON body can include resume_text, job_description, and a list of skills.
- POST /api/career-assistant/interview-kit/
  - JSON body can include role, skills, and count (1–20).
- POST /api/integrations/jobs/normalize/
  - Supply job for one record or csv for CSV preview.
- GET /api/account/export/
  - Downloads the authenticated user's tracked career data as JSON.

All endpoints require authentication. Resume and job text limits are enforced.
Export responses use Cache-Control: no-store.

## Safety and limitations

- Career assistance is deterministic and local. It does not contact an AI vendor,
  claim to predict hiring outcomes, or save the submitted resume text.
- Adapters normalize payloads supplied by the user or an authorized integration.
  They do not crawl job boards, bypass authentication, or fetch arbitrary URLs.
- Import preflight does not silently create applications; a user-reviewed
  persistence step and duplicate resolution can be added separately.
- Personal export is scoped to the authenticated user. Account deletion is a
  separate operation requiring explicit confirmation and retention disclosures.
- These changes do not by themselves establish a 30,000-line count. Use the
  repository's line-count workflow and the target submission platform's own
  counting rules to verify the measured total.

## Remaining roadmap

Existing modules already cover a large portion of job tracking, analytics,
interviews, resumes, reminders, contacts, reporting, pipeline health, planning,
and application comparison. Remaining substantial work should focus on tested
email/calendar provider integrations, end-to-end browser workflows, accessibility
and localization audits, deployment/monitoring/backup documentation, import
conflict resolution, and optional provider-backed AI with explicit consent,
credentials, quotas, and retention controls.
