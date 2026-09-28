# Architecture Overview

## System Design

Job Application Tracker follows a layered architecture with clear separation of concerns across frontend, backend, and event service components.

## Components

### 1. Frontend Layer (React + Vite)

**Purpose**: Provide user interface for job search management

**Key Features**:
- Real-time dashboard with metrics
- Search and filter functionality
- Modal-based forms for CRUD operations
- Responsive design for mobile and desktop
- Status visualization with color coding

**Technology**:
- React 18 with functional components
- Axios for HTTP communication
- CSS3 Grid and Flexbox for layout

### 2. Backend API (Django + DRF)

**Purpose**: Handle business logic, data persistence, and API endpoints

**Key Layers**:

#### Models Layer
- `JobApplication`: Core entity for job postings
- `Interview`: Related entity for interview tracking
- Database schema with proper indexing

#### Service Layer
- `JobApplicationService`: Business logic for applications
- Handles searches, filtering, analytics
- Salary statistics and pipeline health calculations
- Timeline generation from events

#### API Layer
- `JobApplicationViewSet`: CRUD operations for applications
- `InterviewViewSet`: Interview management
- Custom actions for dashboard, metrics, export
- JWT authentication on all protected endpoints

**Technology**:
- Django 6.1 with PostgreSQL
- Django REST Framework for APIs
- Simple JWT for authentication

### 3. Event Service (Java + Spring Boot)

**Purpose**: Log application events and provide metrics

**Key Features**:
- Event persistence to database
- Event filtering and aggregation
- Timeline generation per application
- Metrics endpoint for system health

**Technology**:
- Spring Boot 4.0 with Spring Data JPA
- PostgreSQL driver for data access
- Spring Actuator for health checks

### 4. Data Layer (PostgreSQL)

**Purpose**: Persistent data storage

**Tables**:
- `jobs_jobapplication`: Job application records
- `jobs_interview`: Interview records
- `application_events`: Event log entries
- Django auth tables for users

**Indexing**:
- Composite index on (user_id, updated_at)
- Index on (user_id, status)
- Index on (application_id, outcome)
- Index on scheduled_date

## Data Flow

### Create Application
```
Frontend Form
    ↓
Axios POST /api/applications/
    ↓
Django Views.perform_create()
    ↓
JobApplicationService.create()
    ↓
Model.save() → Database
    ↓
Java Event Service records "application_created" event
    ↓
Frontend refreshes dashboard
```

### View Dashboard
```
Frontend mounted
    ↓
Axios GET /api/applications/dashboard/
    ↓
Django Views.dashboard()
    ↓
JobApplicationService.dashboard()
    ↓
Aggregates data from database
    ↓
Returns metrics + upcoming/overdue items
    ↓
Frontend renders metric cards and tables
```

### View Pipeline Health
```
Axios GET /api/applications/health_metrics/
    ↓
Django Views.health_metrics()
    ↓
JobApplicationService.pipeline_health()
    ↓
Calculates conversion rates from status counts
    ↓
Returns percentages and metrics
```

## API Request/Response Flow

### Authenticated Request
```
1. Frontend sends request with Authorization header
   GET /api/applications/ HTTP/1.1
   Authorization: Bearer <JWT_TOKEN>

2. Django middleware validates JWT token
   
3. Permission classes check if user is authenticated
   
4. ViewSet processes request with user context
   
5. Service layer executes business logic
   
6. Database query executes
   
7. Serializer converts model to JSON
   
8. Response sent to frontend
   HTTP/1.1 200 OK
   Content-Type: application/json
   
   [{"id": 1, "company": "...", ...}]
```

## Search and Filter Architecture

```
User Input (Company Name)
    ↓
Frontend API call with query params
GET /api/applications/?q=acme&status=applied
    ↓
ViewSet.get_queryset() with filters
    ↓
Service.search(query, status)
    ↓
Django ORM with Q objects:
  (company__icontains='acme' OR role__icontains='acme' 
   OR location__icontains='acme' OR notes__icontains='acme')
  AND status='applied'
    ↓
Database executes filtered query
    ↓
Results returned and serialized
```

## Performance Considerations

### Database Optimization
- Indexes on frequently filtered fields
- `select_related()` for foreign key joins
- `prefetch_related()` for reverse relations
- Query result caching where applicable

### Frontend Optimization
- Component memoization to prevent re-renders
- Lazy loading of data
- Client-side filtering for cached data
- Debounced search input

### API Optimization
- Response serialization filtering
- Pagination support for large datasets
- ETag headers for caching
- Gzip compression for responses

## Error Handling

### Backend
- Validation errors return 400 Bad Request
- Authentication errors return 401 Unauthorized
- Permission errors return 403 Forbidden
- Not found errors return 404 Not Found
- Server errors return 500 with error message

### Frontend
- Try/catch blocks around API calls
- User-friendly error messages
- Automatic retry for network failures
- Error logging to console

## Security Architecture

### Authentication
- JWT tokens issued on login
- Tokens include user ID in payload
- Frontend stores token in memory (not localStorage)
- Token refresh endpoint for expiration

### Authorization
- User-scoped querysets (filter by current user)
- Permission checks in views
- Service layer validates ownership
- CORS configuration restricts origins

### Data Protection
- Passwords hashed with Django's PBKDF2
- SQL injection prevention through ORM
- CSRF protection on Django views
- Environment variables for secrets

## Scalability Strategy

### Current Architecture
- Single Django instance suitable for ~1000 concurrent users
- PostgreSQL handles moderate database load
- React frontend runs in browser (stateless)

### Future Scaling
- Load balancer in front of Django instances
- Database read replicas for analytics queries
- Redis caching layer for frequently accessed data
- Celery task queue for async operations
- CDN for static frontend assets
- API rate limiting per user

## Monitoring and Logging

### What to Monitor
- API response times
- Database query performance
- Authentication success rate
- Error rates by endpoint
- Disk usage and backups

### Logging Strategy
- Django logging to file/console
- Java Spring Boot logging
- Application event logging in database
- Frontend error tracking (optional)

## Deployment Architecture

### Development
- Docker Compose with all services
- Hot reloading for code changes
- In-memory database for speed

### Staging
- Similar to production but scaled down
- Real PostgreSQL database
- TLS certificates (self-signed ok)
- Full test suite runs

### Production
- Kubernetes or Docker Swarm orchestration
- Database backups and replication
- Load balancing across instances
- Monitoring and alerting
- Rolling deployments with zero downtime
