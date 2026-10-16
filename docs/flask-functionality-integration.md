# Integrating the Flask job tracker into Django + React

## Decision

The supplied Flask/SQLAlchemy example is integrated into the existing Django REST Framework API and React client rather than deployed as a second backend. The repository already has a `JobApplication` model, authenticated CRUD endpoints, a React create/edit form, status filtering, and search. A parallel Flask service or a second SQLite database would duplicate the source of truth and introduce synchronization and authorization risks.

## Feature mapping

| Flask example | Existing application |
| --- | --- |
| SQLAlchemy `Job` model | `apps.jobs.models.JobApplication` (Django ORM) |
| `GET /api/jobs` | `GET /api/applications/` |
| `POST /api/jobs` | `POST /api/applications/` |
| `PUT /api/jobs/<id>` | `PUT` or `PATCH /api/applications/<id>/` |
| `DELETE /api/jobs/<id>` | `DELETE /api/applications/<id>/` |
| SQLite persistence | Configured Django database (PostgreSQL in normal deployment; SQLite for CI) |
| HTML form and fetch calls | React/Vite form and Axios API client |

The Django model includes the supplied fields (`company`, `role`, `location`, `status`, `job_url`, `applied_date`, and `notes`) plus salary ranges, follow-up actions, timestamps, and interview relationships. The API keeps each user's applications private by scoping queries to the authenticated user.

## Authentication

Application endpoints require a valid JWT access token. The React API client attaches it as `Authorization: Bearer <access_token>`. Obtain tokens through `POST /api/auth/token/`; do not expose the API anonymously just to mirror the original Flask sample.

## Example requests

List applications, optionally filtered by status or search text:

```http
GET /api/applications/?status=interview&q=engineer
Authorization: Bearer <access_token>
```

Create an application:

```http
POST /api/applications/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "company": "Northwind",
  "role": "Data Analyst",
  "location": "Nairobi",
  "status": "applied",
  "job_url": "https://example.com/jobs/123",
  "applied_date": "2026-10-01",
  "notes": "Follow up next week"
}
```

Use `PATCH /api/applications/<id>/` for a partial update, `PUT` for a full replacement, and `DELETE` to remove an application. A missing or another user's application returns `404` so the endpoint does not disclose that user's record.

## Validation and regression coverage

The serializer now rejects inconsistent salary ranges where `salary_min` is greater than `salary_max`, including partial updates that would make an existing range invalid. Endpoint tests cover the supplied fields through create/read/update/delete, status filtering, salary validation, and cross-user access protection.

Run the backend suite locally:

```bash
cd backend
DJANGO_DB_ENGINE=sqlite pytest -q
```

## About the 30,000-line target

The target should be met through reviewed product functionality, maintainable modules, tests, migrations, and documentation—not generated filler, duplicated endpoints, or repeated boilerplate. This pull request integrates and tests the supplied CRUD behavior; it does not claim to independently add 30,000 lines. Measure the repository's qualifying source lines with the submission platform or a documented source-line counter before asserting that threshold.
