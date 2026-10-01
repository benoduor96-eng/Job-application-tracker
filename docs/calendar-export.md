# Calendar export

GET /api/calendar/export/ downloads an iCalendar (.ics) file containing:

- every interview that has a scheduled_date (default length 60 minutes), and
- an all-day follow-up event for each application with a next_action_date.

Rejected and withdrawn applications are skipped.

Requires a JWT (Authorization: Bearer <token>) and only includes the caller's own data.

Query parameters:

- duration: interview length in minutes, 15 to 480 (default 60).
- include_past: true to include events that started before today (default false).

Invalid values return 400 with {"detail": "..."}.

Event UIDs are stable (interview-<id>@jobtracker.local and follow-up-<id>@jobtracker.local), so re-importing the file into a calendar app updates existing events instead of duplicating them.

A browser link cannot send the JWT header. The React app should request the file with the authenticated axios instance using responseType: "blob" and save it.
