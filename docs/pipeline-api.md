# Pipeline board API

Both endpoints require a JWT (Authorization: Bearer <token>) and only ever see the caller's own applications.

## GET /api/pipeline/board/

Applications grouped into the seven pipeline stages, in order.

Query parameters:

- q: case-insensitive match on company, role or location.
- stale_days: integer >= 1, default 14. A waiting application (applied, screening or interview) is stale when it has not been updated for more than this many days.

Cards are ordered by soonest next_action_date, then undated cards, then company name.

## POST /api/pipeline/move/

Move up to 100 applications to a new stage.

Example request:

{"ids": [3, 7], "status": "interview"}

The response contains moved, unchanged, and missing IDs. Missing applications include IDs that do not exist or belong to another user and are never modified.

Each moved application gets a status_change activity with {"from", "to", "source": "pipeline_board"} metadata. Moving to applied sets applied_date to today when it is empty.

Invalid bodies return 400 with {"detail": "..."}.
