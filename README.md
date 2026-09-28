# Job Application Tracker

A full-stack application for managing a personal job-search pipeline. It combines a Django REST API, PostgreSQL, a React/Vite interface, and a small Java/Spring Boot event service.

## What it does

- Create, update, delete, and review job applications.
- Track saved, applied, screening, interview, offer, rejected, and withdrawn stages.
- Search by company, role, location, or notes.
- Filter the pipeline by status.
- Record application dates, salary ranges, job links, notes, and next actions.
- Surface upcoming and overdue follow-ups.
- Calculate pipeline metrics such as interview and offer rates.
- Export application records through the API.
- Record application events through the Java service.
- Run backend, Java, and frontend checks in CI.

## Architecture

### Django API
The Python backend owns application data and authentication. The REST API is under `/api/`.

Important endpoints:

```text
GET    /api/health/
POST   /api/auth/register/
POST   /api/auth/token/
POST   /api/auth/token/refresh/
GET    /api/applications/
POST   /api/applications/
PATCH  /api/applications/<id>/
DELETE /api/applications/<id>/
GET    /api/applications/dashboard/
GET    /api/applications/health_metrics/
GET    /api/applications/export/
```

Application list requests support `q` and `status` query parameters.

### Java event service
The Spring Boot service provides a lightweight event boundary for application activity.

```text
POST /api/v1/events
GET  /api/v1/events/stats
GET  /api/v1/events/health
```

Events are validated and counted by event type.

### React frontend
The frontend is split into reusable components for the application form, application cards, and dashboard statistics. It supports responsive layouts, search, filtering, loading/error states, and deletion.

## Local development

### Docker Compose

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- Django API: http://localhost:8000
- Java service: http://localhost:8080
- PostgreSQL: localhost:5432

### Backend tests

```bash
cd backend
python -m pytest
```

### Java tests

```bash
cd java-service
./mvnw test
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Configuration

Copy `.env.example` to `.env` for local settings. Do not commit real credentials, tokens, or production secrets.

## Technology

- Python 3.13
- Django + Django REST Framework
- PostgreSQL
- Java 21
- Spring Boot
- React + Vite
- Axios
- Docker Compose
- GitHub Actions

## Project structure

```text
backend/       Django API, models, services, migrations, and tests
frontend/      React/Vite application
java-service/  Spring Boot event service and tests
.github/       CI workflow
docker-compose.yml
```

## Development history

The repository is intentionally maintained as incremental commits: domain logic, API behavior, validation, frontend components, UI integration, event-service behavior, and tests are committed separately so the development process is visible in Git history.
