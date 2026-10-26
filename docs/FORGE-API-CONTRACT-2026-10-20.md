# API contract verification: 20 October 2026

## Scope and coordination

Existing MIT-licensed Vendor Due Diligence Agent, base commit
9a3e9787c3b64db83f63e877ec0f9cfaa59d7aa5.
The GitHub open-PR search returned no open PR for this repository at inspection.
Other Palm92 repositories have open work; none of those branches was changed.
The previous local working directory contains uncommitted work and was left intact.
Source files for this check were fetched at the immutable base commit through
the GitHub connector into a separate local directory; direct git clone stalled
and was stopped. No AGENTS.md was found at the repository root at that ref.

Operational need: the reviewer download added in PR #3 had seven function-level
tests, while routing, request parsing, validation and serialization had only
a previously recorded manual HTTP smoke test. These are now repeatable in CI.

## Change and acceptance evidence

Added tests/test_api_contract.py with eight asynchronous unittest tests.
They exercise the real FastAPI ASGI application and the api.index serverless
export, including routing, Pydantic validation, response serialization and
download headers. The transport is an in-process, single-request ASGI helper.
It uses the standard library and existing dependencies, without httpx, sockets,
paid services, credentials or real supplier data.

Validated:
- Health responses through both import paths.
- JSON assessment preserves sanctions blocker and human escalation.
- Markdown export has no-store, nosniff, a fixed attachment filename, correct
  UTF-8 content length and a pending human decision.
- User-provided Markdown/HTML is neutralised over the API.
- Missing, too-short and null vendor names and an invalid boolean return 422.
- Malformed JSON returns 422 without producing a report attachment.
- GET requests cannot generate an assessment or report (405).
- OpenAPI retains the JSON and Markdown response contracts.

Commands executed locally:
- python -m unittest discover -s tests -v: 15 tests passed, zero failures.
- python verify.py: all existing TrustSphere verification checks passed.
- python -m pip check: no broken requirements found.

Environment: Python 3.12; fresh isolated installation from unchanged requirements.
Resolved FastAPI 0.151.0, Pydantic 2.14.1 and Starlette 1.9.0.
Versions describe this run only, not a lockfile or minimum-version test matrix.

Negative control: a temporary copied app changed Cache-Control from no-store
to public. The new API suite failed on that exact header expectation, as intended.
The real source was not modified by this experiment.

The existing CI command already discovers tests/test_api_contract.py. No workflow,
application logic, dependencies, authentication, scoring or approval rules change.
Remote CI status is separate from these local results.

## Privacy, deployment and next action

Fictional questionnaire inputs only. No tokens, provider calls, persistence,
outbound messages, public service deployment or access grants were involved.
This checks specific safeguards; it is not a complete security audit.

Free-first Plan A: run the existing CI test discovery on this draft branch, review
and merge, then smoke-test the authorised deployed service with fictional data.
Free-first Plan B verified here: run the same ASGI contract suite locally when a
host, socket connection or deployment account is unavailable. This is not proof
of network, TLS, reverse-proxy, hosting failover or deployed endpoint behaviour.

Current production blocker: authentication/access controls and the live hosting
configuration remain unverified. These tests do not remove that blocker.
Next: review this draft and verify the deployed route only after the target
hosting project and authorised configuration are identified.
