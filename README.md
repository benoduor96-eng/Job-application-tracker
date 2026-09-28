# Job Application Tracker

A full-stack job search command center for tracking applications, pipeline status, interviews, follow-ups, offers, notes, and next actions.

## Stack
- **Python / Django + Django REST Framework** — authenticated application API and dashboard metrics.
- **PostgreSQL** — durable application storage.
- **Java 21 / Spring Boot** — event service for application activity and integrations.
- **React + Vite** — responsive job-search dashboard.
- **Docker Compose** — local development stack.
- **GitHub Actions** — Python, Java and frontend CI.

## Features
- JWT authentication foundation and registration
- Create, update, delete and filter job applications
- Pipeline statuses: Saved, Applied, Screening, Interview, Offer, Rejected, Withdrawn
- Company, role, location and job URL tracking
- Salary range, notes and next-action tracking
- Upcoming follow-up dates
- Dashboard status aggregation
- Java activity-event endpoint for integrations

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:5173
- Django API: http://localhost:8000/api/
- Django admin: http://localhost:8000/admin/
- Java event service: http://localhost:8080/api/v1/events/health

## API highlights
- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `GET /api/applications/`
- `POST /api/applications/`
- `GET /api/applications/dashboard/`
- `PUT /api/applications/{id}/`
- `DELETE /api/applications/{id}/`
- `POST /api/v1/events`

## Development

Backend:
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Java:
```bash
cd java-service
mvn spring-boot:run
```

## Security
Use environment variables for production secrets. Never commit `.env`, credentials, API keys, or personal data.
