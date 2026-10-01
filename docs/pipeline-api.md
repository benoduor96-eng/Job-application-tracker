# Pipeline board API

Both endpoints require a JWT and only expose the authenticated user's applications.

## GET /api/pipeline/board/

Returns applications grouped into the seven pipeline stages. Query parameters:

- `q`: case-insensitive match on company, role, or location.
- `stale_days`: integer >= 1; default 14.

## POST /api/pipeline/move/

Moves up to 100 applications. Example request:

```json
{"ids": [3, 7], "status": "interview"}
```

The response contains `moved`, `unchanged`, and `missing` IDs. Applications moved by the endpoint receive a `status_change` activity with `from`, `to`, and `source: pipeline_board` metadata. Moving to `applied` fills an empty `applied_date` with today's date.
