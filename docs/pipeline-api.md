# Pipeline board API

Both endpoints require a JWT (`Authorization: Bearer <token>`) and only ever see the caller's own applications.

## GET `/api/pipeline/board/`

Applications grouped into the seven pipeline stages, in order.

Query parameters:

- `q`: case-insensitive match on company, role or location.
- `stale_days`: integer >= 1, default 14. A waiting application (applied, screening or interview) is stale when it has not been updated for more than this many days.

Response:

```json
{
  "columns": [
    {
      "status": "applied", "label": "Applied", "count": 2,
      "avg_salary_min": 110000.0, "avg_salary_max": 140000.0, "stale_count": 1,
      "cards": [{"id": 7, "company": "Acme", "role": "Engineer", "status": "applied",
                 "salary_min": 100000.0, "salary_max": 140000.0, "stale": false,
                 "applied_date": "2026-09-28", "next_action": "Follow up",
                 "next_action_date": "2026-10-05", "location": "Remote"}]
    }
  ],
  "totals": {"applications": 12, "active": 9, "stale": 2}
}
```

Cards in a column are ordered by soonest `next_action_date`, then undated cards, then company name.

## POST `/api/pipeline/move/`

Move up to 100 applications to a new stage.

```json
{"ids": [3, 7], "status": "interview"}
```

Response: `{"moved": [3], "unchanged": [7], "missing": []}`.

- `unchanged`: already in that stage.
- `missing`: no such application, or it belongs to another user (never modified).
- Each moved application gets a `status_change` activity with `{"from", "to", "source": "pipeline_board"}` metadata.
- Moving to `applied` sets `applied_date` to today when it was empty.
- Invalid bodies return `400` with `{"detail": "..."}`.

## Validation

The move endpoint rejects invalid stage names, empty ID lists, non-integer IDs, and requests containing more than 100 application IDs.
