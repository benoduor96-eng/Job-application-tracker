# Job Application Tracker

A full-stack job search command center for tracking applications, pipeline status, interviews, follow-ups, offers, notes, and next actions.

## Overview

Job Application Tracker is a comprehensive platform for job seekers to organize, monitor, and analyze their job search pipeline. It provides real-time dashboards, interview tracking, salary analysis, and automated reminders to keep your search on track.

## Features

### Application Management
- Create, read, update, and delete job applications
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
- Pipeline health metrics (screening rate, interview rate, offer rate)
- Salary statistics and range analysis
- Active pipeline visualization
- Upcoming follow-ups and overdue actions
- Application timeline with event tracking

### User Experience
- Responsive React dashboard with modern UI
- Search and filter applications in real-time
- Modal forms for easy CRUD operations
- Status badges with visual color coding
- Export application data for external analysis
- Mobile-friendly responsive design

## Tech Stack

### Backend
- **Python 3.13** with Django 6.1
- **Django REST Framework** for API
- **PostgreSQL** for data persistence
- **JWT authentication** with django-rest-framework-simplejwt
- **Celery/Redis** foundation for async tasks

### Frontend
- **React 18** with modern hooks
- **Vite** for fast development and optimized builds
- **Axios** for API communication
- **CSS3** with responsive grid and flexbox layouts

### Event Service
- **Java 21** with Spring Boot 4.0
- **Spring Data JPA** for ORM
- **PostgreSQL driver** for database connectivity
- **Spring Actuator** for health and metrics endpoints

### DevOps
- **Docker & Docker Compose** for containerization
- **GitHub Actions** for CI/CD pipeline
- **PostgreSQL 17** database container

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                 │
│              Dashboard, Forms, Analytics UI                 │
└────────────────────┬────────────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
┌─────────▼──────────┐ ┌────────▼──────────┐
│   Django API       │ │  Java Service     │
│  (Port 8000)       │ │ (Port 8080)       │
│                    │ │                   │
│ - Auth             │ │ - Event Logger    │
│ - Applications     │ │ - Metrics         │
│ - Interviews       │ │ - Timeline        │
│ - Analytics        │ │ - Health Check    │
└─────────┬──────────┘ └────────┬──────────┘
          │                     │
          └──────────┬──────────┘
                     │
         ┌───────────▼───────────┐
         │   PostgreSQL 17       │
         │   (Port 5432)         │
         │                       │
         │ - Applications        │
         │ - Interviews          │
         │ - Events              │
         └───────────────────────┘
```

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.13 (for local development)
- Node.js 22+ (for frontend development)
- Java 21 (for Java service development)

### Using Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/benoduor96-eng/Job-application-tracker.git
cd Job-application-tracker

# Copy environment file
cp .env.example .env

# Start all services
docker compose up --build
```

**Access the application:**
- Frontend: http://localhost:5173
- Django API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/ (login: admin/admin)
- Java Events: http://localhost:8080/api/v1/events/health

### Local Development

#### Backend (Django)

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

#### Java Service

```bash
cd java-service
mvn spring-boot:run
```

## API Documentation

### Authentication

**Register**
```bash
POST /api/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123"
}
```

**Get Token**
```bash
POST /api/auth/token/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password_123"
}
```

### Applications

**List Applications**
```bash
GET /api/applications/
Authorization: Bearer {token}

# Query parameters:
# ?q=search_query     - Search by company, role, location, notes
# ?status=applied     - Filter by status
```

**Create Application**
```bash
POST /api/applications/
Authorization: Bearer {token}
Content-Type: application/json

{
  "company": "Acme Corp",
  "role": "Senior Backend Engineer",
  "location": "San Francisco",
  "job_url": "https://example.com/jobs/123",
  "status": "applied",
  "salary_min": 150000,
  "salary_max": 200000,
  "applied_date": "2026-09-28",
  "next_action": "Follow up with recruiter",
  "next_action_date": "2026-10-05",
  "notes": "Great company culture"
}
```

**Update Application**
```bash
PUT /api/applications/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "interview",
  "next_action": "Prepare for technical interview"
}
```

**Delete Application**
```bash
DELETE /api/applications/{id}/
Authorization: Bearer {token}
```

### Dashboard

**Get Dashboard Metrics**
```bash
GET /api/applications/dashboard/
Authorization: Bearer {token}

Response:
{
  "total": 25,
  "active": 12,
  "interviews": 4,
  "offers": 1,
  "by_status": {...},
  "upcoming": [...],
  "overdue": [...]
}
```

**Get Pipeline Health**
```bash
GET /api/applications/health_metrics/
Authorization: Bearer {token}

Response:
{
  "screening_rate": 45.5,
  "interview_rate": 22.3,
  "offer_rate": 5.2,
  "total_tracked": 25
}
```

**Get Salary Statistics**
```bash
GET /api/applications/salary_stats/
Authorization: Bearer {token}

Response:
{
  "count": 15,
  "avg_min": 120000,
  "avg_max": 160000,
  "highest_min": 200000,
  "lowest_max": 80000
}
```

**Export Applications**
```bash
GET /api/applications/export/
Authorization: Bearer {token}

Response: [Array of application objects with all fields]
```

### Interviews

**List Interviews**
```bash
GET /api/interviews/
Authorization: Bearer {token}
```

**Create Interview**
```bash
POST /api/interviews/
Authorization: Bearer {token}
Content-Type: application/json

{
  "application": 1,
  "interview_type": "technical",
  "scheduled_date": "2026-10-10T14:00:00Z",
  "outcome": "pending",
  "interviewer_name": "Jane Smith",
  "interviewer_title": "Engineering Manager",
  "feedback": "",
  "notes": "Focus on system design questions"
}
```

**Get Interview Summary for Application**
```bash
GET /api/applications/{id}/interviews_summary/
Authorization: Bearer {token}

Response:
{
  "total": 2,
  "pending": 1,
  "passed": 1,
  "failed": 0,
  "interviews": [...]
}
```

### Event Service (Java)

**Record Event**
```bash
POST /api/v1/events
Content-Type: application/json

{
  "application_id": "123",
  "event_type": "applied",
  "note": "Applied to position"
}
```

**Get Event Metrics**
```bash
GET /api/v1/events/metrics

Response:
{
  "total_events": 150,
  "applied_events": 75,
  "interview_events": 30,
  "offer_events": 5,
  "rejection_events": 15
}
```

**Get Application Timeline**
```bash
GET /api/v1/events/application/{applicationId}

Response:
{
  "application_id": "123",
  "event_count": 4,
  "events": [...]
}
```

## Pipeline Stages

1. **Saved** - Job posting saved for later consideration
2. **Applied** - Application submitted to company
3. **Screening** - Recruiter/HR initial screening
4. **Interview** - In interview process (phone, technical, etc.)
5. **Offer** - Offer received from company
6. **Rejected** - Application rejected by company
7. **Withdrawn** - Application withdrawn by candidate

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest apps/api/tests.py -v

# Java tests
cd java-service
mvn test
```

### Code Structure

```
Job-application-tracker/
├── backend/                    # Django application
│   ├── apps/
│   │   ├── jobs/              # Job models and business logic
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── migrations/
│   │   └── api/               # API views and serializers
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── tests.py
│   ├── config/                # Django settings
│   └── manage.py
├── frontend/                  # React application
│   ├── src/
│   │   ├── main.jsx          # Dashboard component
│   │   └── styles.css        # Global styles
│   ├── package.json
│   └── vite.config.js
├── java-service/              # Spring Boot event service
│   ├── src/
│   │   ├── main/java/com/benoduor/jobtracker/
│   │   │   ├── model/        # Entity classes
│   │   │   ├── repository/   # Data access layer
│   │   │   ├── service/      # Business logic
│   │   │   └── controller/   # REST endpoints
│   │   └── test/
│   ├── pom.xml
│   └── Dockerfile
├── docker-compose.yml
├── .github/workflows/         # CI/CD configuration
└── README.md
```

## Environment Variables

Create `.env` file from `.env.example`:

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=jobs
POSTGRES_USER=jobs
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Frontend
VITE_API_URL=http://localhost:8000/api

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=false` in Django settings
- [ ] Use strong `DJANGO_SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with production domain
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure PostgreSQL with strong password
- [ ] Set up proper logging and monitoring
- [ ] Run Django migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Use a production WSGI server (Gunicorn, uWSGI)

### Docker Production Build

```bash
docker compose -f docker-compose.yml up -d
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Performance Optimization

- Database queries are optimized with proper indexing
- Frontend uses React hooks for efficient rendering
- Pagination support for large datasets
- Caching headers configured for static assets

## Security

- JWT authentication for all protected endpoints
- CORS configuration to prevent unauthorized cross-origin requests
- SQL injection prevention through ORM usage
- CSRF protection in Django
- Password hashing with Django's built-in tools

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation for common problems

## Roadmap

- [ ] Email notifications for follow-ups
- [ ] Integration with LinkedIn/Indeed APIs
- [ ] Advanced analytics and visualizations
- [ ] Interview question database
- [ ] Salary negotiation guides
- [ ] Team collaboration features
- [ ] Mobile native app
- [ ] AI-powered insights and recommendations

## Version History

### v0.2.0 (Current)
- Added interview tracking
- Added pipeline health metrics
- Added event persistence service
- Enhanced frontend with modals and forms
- Improved API endpoints

### v0.1.0
- Initial project scaffold
- Basic CRUD for applications
- Dashboard with metrics
- JWT authentication
