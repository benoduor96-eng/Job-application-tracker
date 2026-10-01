# Job Application Tracker

A full-stack job search command center for tracking applications, pipeline status, interviews, follow-ups, offers, notes, and next actions.

## Overview

Job Application Tracker is a comprehensive platform for job seekers to organize, monitor, and analyze their job search pipeline. It provides real-time dashboards, interview tracking, salary analysis, and automated reminders to keep your search on track.

## Features

### Application Management
- Create, read, update, delete job applications
- Track company, role, location, and job URL
- Monitor application status across 7 pipeline stages
- Record salary ranges and compensation details
- Add notes and custom follow-up actions
- Set follow-up reminders with target dates

### Interview Tracking
- Log multiple interviews per application
- Track interview type (phone, technical, behavioral, panel, etc.)
- Record interviewer details and feedback
- Monitor interview outcomes (pending, passed, failed)
- View interview timeline per application

### Analytics & Insights
- Real-time dashboard with key metrics
- Pipeline health metrics
- Salary statistics and range analysis
- Active pipeline visualization
- Upcoming follow-ups and overdue actions
- Application timeline with event tracking

### Career Intelligence & Planning
- Application-to-resume matching and job-fit scoring
- Interview preparation and cover-letter support
- Follow-up sequences and notification planning
- Contact management, career goals and resume versions
- Duplicate-application review and data import/export

### User Experience
- Responsive React dashboard
- Search and filter applications in real time
- Modal forms for CRUD operations
- Status badges and visual pipeline indicators
- Export application data
- Mobile-friendly responsive design

## Tech Stack

- **Backend:** Python 3.13, Django 6.1, Django REST Framework, PostgreSQL, JWT
- **Frontend:** React 18, Vite, Axios, CSS3
- **Event Service:** Java 21, Spring Boot 4, Spring Data JPA
- **Infrastructure:** Docker, Docker Compose, PostgreSQL 17, GitHub Actions

## Architecture

```
Frontend (React + Vite)
        |
        +------------------+
        |                  |
   Django API        Java Event Service
   Port 8000          Port 8080
        |                  |
        +--------+---------+
                 |
          PostgreSQL 17
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.13
- Node.js 22+
- Java 21

### Docker Compose

```bash
git clone https://github.com/benoduor96-eng/Job-application-tracker.git
cd Job-application-tracker
cp .env.example .env
docker compose up --build
```

Services:
- Frontend: `http://localhost:5173`
- Django API: `http://localhost:8000/api/`
- Django Admin: `http://localhost:8000/admin/`
- Java events: `http://localhost:8080/api/v1/events/health`

### Local Development

Backend:

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Java service:

```bash
cd java-service
mvn spring-boot:run
```

## API Examples

### Authentication

```http
POST /api/auth/register/
POST /api/auth/token/
```

### Applications

```http
GET    /api/applications/
POST   /api/applications/
PUT    /api/applications/{id}/
DELETE /api/applications/{id}/
```

### Reporting

The backend includes reporting services for dashboard summaries, pipeline health, salary statistics, application timelines, response lag, top companies and roles, recent activity, weekly application counts, and market signals.

### Java Events

```http
POST /api/v1/events
GET  /api/v1/events/metrics
GET  /api/v1/events/application/{applicationId}
```

## Pipeline Stages

1. **Saved** — Job posting saved for later consideration
2. **Applied** — Application submitted
3. **Screening** — Recruiter or HR screening
4. **Interview** — Interview process
5. **Offer** — Offer received
6. **Rejected** — Application rejected
7. **Withdrawn** — Application withdrawn

## Testing

Backend tests use the same SQLite configuration as CI:

```bash
cd backend
DJANGO_DB_ENGINE=sqlite pytest -q
```

Coverage:

```bash
DJANGO_DB_ENGINE=sqlite coverage run -m pytest -q
coverage report
```

Java:

```bash
cd java-service
mvn test
```

Frontend:

```bash
cd frontend
npm install
npm run build
```

## Project Structure

```
Job-application-tracker/
├── backend/
│   ├── apps/
│   │   ├── jobs/
│   │   └── api/
│   └── config/
├── frontend/
│   └── src/
├── java-service/
├── docs/
├── .github/workflows/
├── docker-compose.yml
└── README.md
```

## Environment Variables

Create `.env` from `.env.example` and configure:

```text
DJANGO_SECRET_KEY=
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=5432
VITE_API_URL=http://localhost:8000/api
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Never commit real credentials, tokens, passwords, or private keys.

## CI

GitHub Actions checks:
- Django system checks and backend tests
- Backend coverage reporting
- Java tests
- Frontend production build
- Qualifying source-line measurement
- Verified Git bundle generation

## License

MIT License. See [LICENSE](LICENSE).

## Roadmap

- Email notifications for follow-ups
- Job-board integrations
- Advanced analytics and visualizations
- Interview question database
- Salary negotiation tools
- Team collaboration
- Mobile application
- AI-assisted job-search insights
