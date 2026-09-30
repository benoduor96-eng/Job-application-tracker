# Career Intelligence API

The career intelligence module is deterministic and operates on information
already stored in the authenticated user's tracker.

## Job description analysis

### Preview

`POST /api/intelligence/descriptions/preview/`

Request:

```json
{
  "raw_text": "Senior Python engineer using Django, PostgreSQL and Docker"
}
```

Returns detected skills and ranked keywords without creating a record.

### Create

`POST /api/intelligence/descriptions/`

Creates a user-owned job description and analyzes it immediately.

### Re-analyze

`POST /api/intelligence/descriptions/{id}/analyze/`

Rebuilds extracted skills and keywords from the stored source text.

## Matching

### Advanced skill match

`POST /api/intelligence/skill-match/advanced/`

Example:

```json
{
  "required_skills": ["python", "django"],
  "preferred_skills": ["docker", "aws"],
  "role": "Backend Engineer",
  "location": "Remote",
  "salary_min": "60000",
  "salary_max": "90000"
}
```

The response contains separate required, preferred, profile, salary, and
location components. The overall score is a transparent weighted calculation,
not a model-generated claim.

### Description match

`GET /api/intelligence/descriptions/{id}/match/`

Compares a stored job description with the authenticated user's career profile.

### Resume targeting

`GET /api/intelligence/descriptions/{id}/resume_targeting/`

Returns matched skills, missing required skills, and factual tailoring notes.

## Pipeline intelligence

### Summary

`GET /api/intelligence/summary/`

Returns application totals, active pipeline totals, status counts, and the
highest-priority work items.

### Priority

`GET /api/intelligence/pipeline-priority/`

Prioritizes applications using status, next-action dates, and pending
interviews. The calculation is deterministic and can be inspected through the
returned reasons.

### Follow-ups

`POST /api/intelligence/follow-ups/`

Preview:

```json
{
  "create": false
}
```

Create tasks:

```json
{
  "create": true,
  "application_ids": [12, 15]
}
```

Existing open duplicate tasks are skipped.

## Cover letters

### Generate

`POST /api/intelligence/cover-letter/`

The endpoint can accept an application ID, optional description ID, optional
resume ID, and recipient name.

It builds a structured draft from stored profile, resume, application, and job
description data. It does not invent employers, qualifications, dates, or
achievements.

The response includes warnings when source material is missing.

## Ownership and isolation

All endpoints require authentication. Objects are filtered by the current
user before retrieval. A valid object belonging to another user therefore
appears as not found rather than being exposed.

## Testing

The intelligence layer is covered by:

- service-level skill normalization tests
- matching and salary/location scoring tests
- job-description analyzer tests
- follow-up planner tests
- pipeline prioritization tests
- cover-letter builder tests
- authenticated API endpoint tests
- cross-user isolation tests
