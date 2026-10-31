# Vendor input contract, 31 October 2026

Confirmed on unchanged main: a whitespace-only vendor name was accepted and a
misspelled `sanction_or_pep_match` field was silently discarded, leaving the
actual sanctions flag false. This is an input-integrity defect, not a claim
that sanctions screening is performed.

The assessment model now strips surrounding string whitespace and rejects
unknown fields. Both assessment and report endpoints share the model. Existing
boolean coercion and scoring are unchanged. Three new tests cover blank/short
names, misspelled risk flags returning 422 without an attachment, and correct
flags still requiring human review.

18 local unittest tests and the original verify.py checks passed. No hosting,
credentials, external screening or deployment was used. Compatibility change:
clients sending extra fields must remove or correct them rather than relying on
silent discard. Plan A: CI and review before merge. Plan B: the same in-process
ASGI tests run locally without network hosting.
