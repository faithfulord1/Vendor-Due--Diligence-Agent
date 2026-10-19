"""Render a reviewer handoff; no screening, approvals or persistence."""
import html
import re


def _text(value: str) -> str:
    # Keep questionnaire names as text, not headings, links or embedded HTML.
    single_line = " ".join(str(value).split())
    escaped = html.escape(single_line, quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+!|>~])", r"\\\1", escaped)


def render_evidence_report(assessment: dict) -> str:
    lines = [
        "# Vendor evidence review plan",
        "",
        f"Vendor: {_text(assessment['vendor_name'])}",
        "",
        "Status: UNVERIFIED questionnaire claims; evidence collection is outstanding.",
        "This is deterministic triage, not a verified compliance verdict or vendor approval.",
        "",
        f"Triage score: {assessment['risk_score']}/100",
        f"Triage tier: {assessment['risk_tier']}",
        f"Escalated human review required: {'Yes' if assessment['human_review_required'] else 'No'}",
        "Normal human due-diligence approval is still required in every case.",
        "",
        "## Reviewer actions",
        "",
        "- [ ] Confirm questionnaire scope, completeness and source with the vendor.",
        "- [ ] Collect evidence and record its source, scope, date and expiry where applicable.",
        "- [ ] Independently verify reported sanctions, PEP or regulatory signals where relevant.",
        "- [ ] Record gaps, a named risk owner, a review date and the authorised human decision.",
        "",
        "## Finding-specific evidence requests",
        "",
    ]
    if not assessment["findings"]:
        lines += [
            "No rule findings were triggered by the supplied answers.",
            "This does not prove controls are effective or the vendor is safe.",
            "Verify the claims and apply your organisation's full due-diligence policy.",
            "",
        ]
    for finding in assessment["findings"]:
        lines += [
            f"### {_text(finding['control_id'])}",
            "",
            f"Severity: {_text(finding['severity'])}",
            f"Reported finding: {_text(finding['finding'])}",
            f"Evidence requested: {_text(finding['evidence_needed'])}",
            "Evidence status: NOT COLLECTED / NOT VERIFIED",
            "Reviewer / source / evidence date / scope / expiry / gap: to be recorded",
            "",
        ]
    lines += [
        "## Decision handoff",
        "",
        _text(assessment["recommended_next_action"]),
        "Decision: PENDING AUTHORISED HUMAN REVIEW",
        "Risk owner / reviewer / decision date / next review date: to be recorded",
        "",
        "## Limits and handling",
        "",
        "Questionnaire answers are self-reported; omitted flags use the API's existing defaults.",
        "This export does not fetch sources, verify certificates, screen sanctions or onboard vendors.",
        "No audit record or evidence is saved by this endpoint. Save the downloaded file only in an approved location.",
        "Authentication, access controls and retention policy are required before confidential production use.",
        "",
        "AI investigates. Humans decide.",
        "",
    ]
    return "\n".join(lines)
