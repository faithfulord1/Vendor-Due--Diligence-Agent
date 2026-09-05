from __future__ import annotations

from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="TrustSphere Vendor Due Diligence Agent",
    version="1.0.0",
    description="Explainable third-party risk triage with human-governed decisions.",
)


class VendorAssessment(BaseModel):
    vendor_name: str = Field(min_length=2)
    critical_vendor: bool = False
    handles_personal_data: bool = False
    handles_special_category_data: bool = False
    has_iso27001: bool = False
    has_soc2: bool = False
    mfa_enforced: bool = False
    encryption_at_rest: bool = False
    encryption_in_transit: bool = False
    bcp_tested_last_12_months: bool = False
    breach_last_12_months: bool = False
    active_regulatory_investigation: bool = False
    sanctions_or_pep_match: bool = False


class ControlFinding(BaseModel):
    control_id: str
    severity: Literal["low", "medium", "high", "critical"]
    finding: str
    evidence_needed: str


def assess_vendor(vendor: VendorAssessment) -> dict:
    score = 0
    findings: list[ControlFinding] = []

    def add(control_id: str, points: int, severity: str, finding: str, evidence: str):
        nonlocal score
        score += points
        findings.append(ControlFinding(
            control_id=control_id,
            severity=severity,
            finding=finding,
            evidence_needed=evidence,
        ))

    if vendor.sanctions_or_pep_match:
        add("TPRM-SAN-001", 40, "critical", "A sanctions or PEP match is reported.", "Independent sanctions screening result and authorised compliance review")
    if vendor.active_regulatory_investigation:
        add("TPRM-REG-001", 25, "high", "An active regulatory investigation is reported.", "Investigation scope, regulator correspondence and legal/compliance assessment")
    if vendor.breach_last_12_months:
        add("TPRM-SEC-001", 20, "high", "A security breach occurred in the last 12 months.", "Incident report, root-cause analysis and remediation evidence")
    if not vendor.mfa_enforced:
        add("TPRM-IAM-001", 12, "high" if vendor.critical_vendor else "medium", "MFA is not confirmed as enforced.", "Identity policy and MFA enforcement evidence")
    if not vendor.encryption_at_rest or not vendor.encryption_in_transit:
        add("TPRM-ENC-001", 12, "high" if vendor.handles_special_category_data else "medium", "Encryption controls are incomplete or unverified.", "Encryption standards, key-management evidence and transport security configuration")
    if vendor.critical_vendor and not vendor.bcp_tested_last_12_months:
        add("TPRM-RES-001", 12, "high", "Critical vendor resilience testing is not current.", "BCP/DR test report, RTO/RPO results and remediation actions")
    if vendor.handles_personal_data and not (vendor.has_iso27001 or vendor.has_soc2):
        add("TPRM-ASS-001", 10, "medium", "Independent security assurance is not confirmed.", "Current ISO 27001 certificate, SOC 2 report or equivalent independent assurance")
    if vendor.handles_special_category_data:
        add("TPRM-DPIA-001", 8, "medium", "Special-category data increases privacy impact.", "DPIA, data-flow map, lawful basis and retention schedule")

    score = min(score, 100)
    if score >= 70:
        tier = "critical"
    elif score >= 45:
        tier = "high"
    elif score >= 20:
        tier = "medium"
    else:
        tier = "low"

    blockers = [f.control_id for f in findings if f.severity == "critical"]
    human_review_required = tier in {"high", "critical"} or vendor.critical_vendor or bool(blockers)

    return {
        "vendor_name": vendor.vendor_name,
        "risk_score": score,
        "risk_tier": tier,
        "findings": [f.model_dump() for f in findings],
        "critical_blockers": blockers,
        "human_review_required": human_review_required,
        "recommended_next_action": (
            "Escalate to authorised compliance review before onboarding or renewal."
            if human_review_required
            else "Collect outstanding evidence and complete normal human due-diligence approval."
        ),
        "governance": "This engine triages evidence. It does not approve, reject, sanction-screen or onboard a vendor automatically.",
    }


@app.get("/")
def home():
    return {
        "status": "live",
        "project": "TrustSphere Vendor Due Diligence Agent",
        "purpose": "Explainable third-party risk triage with human approval",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/assess")
def assess(payload: VendorAssessment):
    return assess_vendor(payload)
