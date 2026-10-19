# Evidence review export — 19 October 2026

## Scope and operational problem

Inspected existing MIT-licensed Palm92/TrustSphere repository at
`14865fe7298dc5084412b8821be2acb817cdba62`. No AGENTS.md was tracked and no
open pull requests were returned at inspection. Existing README identifies
fragmented spreadsheets, email chains and checklists as the vendor-review problem.
The working API supplied JSON findings but no downloadable reviewer handoff.

This change reuses the deterministic engine to create a Markdown evidence plan.
`POST /assess/report` accepts the existing VendorAssessment questionnaire. It
does not add tools for approval, onboarding, external screening or outbound calls.
No scoring, severity, default questionnaire values or escalation rules change.

## Data flow and governance

Questionnaire -> existing assess_vendor -> text-safe Markdown -> attachment.
Each finding retains its control ID, severity, evidence request and uncollected /
unverified status. The reviewer gets source/scope/date/expiry/gap prompts and a
pending human-decision handoff. No findings does not become verified assurance.
Vendor-provided names are flattened to one line and escaped for Markdown/HTML.
The filename is fixed; responses use no-store and nosniff headers.

The endpoint does not write assessment data or evidence to disk. Downloaded files
still require approved access controls and retention. Authentication and production
governance remain prerequisites for confidential real-vendor use. Existing omitted
boolean defaults can hide unknowns; the report explicitly calls for completeness
review and does not reinterpret those defaults as independently verified facts.

## Verification executed

- Python 3.12.14; isolated environment using existing requirements.
- `python verify.py`: all original low-risk, high-risk and sanctions checks passed.
- `python -m unittest discover -s tests -v`: **7 passed, 0 failed**.
- Checks cover low-risk uncertainty, finding-specific requests/control IDs,
  Markdown/HTML injection, Unicode/repeatability, download/privacy headers,
  unchanged scoring data and OpenAPI routes.
- Local uvicorn HTTP smoke: health 200; report 200 with Markdown, attachment and
  no-store; original JSON route 200 with human escalation; missing name 422.
- `from api.index import app` succeeded for the existing serverless entry point.
- `git diff --check` passed.
- CI now invokes the unittest command. Remote CI results are not claimed here.

Only fictional questionnaire data was used. No third-party screening, model,
credential, real vendor record or external communication was used in these checks.
No deployment or merge was performed.

## Plan A, Plan B and status

Free-first Plan A: existing FastAPI runtime with the new download route after
review/merge approval. Plan B, verified locally: call assess_vendor and
render_evidence_report in Python without an HTTP server. Neither requires a
new dependency, datastore or paid provider. Hosting failover was not tested.

DONE: implement reviewer export, tests, documentation and CI test step.
WAITING: draft review and merge/deployment approval.
NEXT: review the download with a fictional vendor pilot; separately specify
unknown-answer handling and evidence provenance verification before real use.
