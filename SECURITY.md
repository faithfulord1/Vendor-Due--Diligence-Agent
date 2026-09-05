# Security Policy

TrustSphere is a portfolio and learning implementation of explainable third-party risk triage. It is not a production sanctions-screening service, onboarding platform, legal opinion, or automated compliance decision-maker.

## Security principles

- No secret keys or credentials belong in the repository.
- Assessment inputs should use synthetic or appropriately authorised data.
- The deterministic engine produces triage findings only.
- High or critical findings remain subject to authorised human review.
- A sanctions or PEP flag is treated as a reported signal requiring independent verification. The repository does not perform live sanctions screening.
- Production deployments should add authentication, role-based access control, audit logging, encrypted persistence, rate limiting, monitoring, and approved retention controls.

## Reporting a vulnerability

Please report security concerns privately to the repository owner rather than publishing sensitive exploit details in a public issue.
