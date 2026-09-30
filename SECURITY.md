# Security

## Reporting

Please report suspected security vulnerabilities privately rather than opening a public issue with exploit details.

Include:
- affected endpoint or component
- reproducible steps
- expected and observed behavior
- impact assessment
- relevant logs without credentials or personal data

## Data boundaries

Application, resume, contact, profile, task, activity, and job-intelligence records are scoped to the authenticated user. API tests cover cross-user access boundaries.

## Secrets

Environment variables are used for deployment secrets. Production credentials, tokens, private keys, and local environment files must not be committed.
