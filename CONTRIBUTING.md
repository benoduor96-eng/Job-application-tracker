# Contributing

## Development workflow

1. Create a focused branch.
2. Make one coherent feature or fix.
3. Add or update automated tests.
4. Run backend, Java, and frontend checks.
5. Update documentation when behavior changes.
6. Open a pull request describing the design and verification steps.

## Quality expectations

- Keep business logic testable and separated from HTTP concerns.
- Preserve user-level data isolation.
- Validate external input.
- Avoid committing secrets or generated dependency artifacts.
- Prefer small, reviewable commits over bulk changes.
