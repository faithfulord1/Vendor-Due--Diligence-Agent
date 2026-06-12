"""
TrustSphere AI — Full End-to-End Demonstration
================================================
Scenario: OpenAI (GPT-4o) as a vendor AI system
------------------------------------------------
Demonstrates: vendor ingestion, scoring, governance, human review,
audit, DPIA, AI risk assessment, policy review, risk register,
and professional PDF report generation.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

# Ensure src is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.audit.logger import AuditLogger
from src.governance.controls import run_governance_gates, apply_override
from src.modules.ai_risk_assessment import (
    AIAssessmentRequest,
    AIDomain,
    HumanOversightLevel,
    assess_ai_risk,
)
from src.modules.dpia_assessment import (
    DPIARequest,
    DataCategory,
    ProcessingPurpose,
    assess_dpia,
)
from src.modules.policy_review import (
    PolicyDocument,
    PolicyDomain,
    review_policy,
)
from src.modules.risk_register import (
    ImpactLevel,
    Likelihood,
    RiskCategory,
    RiskRegister,
)
from src.questionnaire.intake import ingest_from_dict
from src.reports.pdf_generator import (
    generate_ai_risk_report,
    generate_combined_report,
    generate_dpia_report,
    generate_vendor_dd_report,
)
from src.review.approval import (
    Decision,
    HumanReviewService,
    ReviewDecision,
)
from src.risk_scoring.scorer import score_questionnaire


def build_openai_questionnaire() -> dict:
    """Simulate a realistic vendor questionnaire for OpenAI (GPT-4o)."""
    return {
        "supplier": {
            "vendor_id": "VND-OPENAI-2026",
            "name": "OpenAI",
            "legal_entity": "OpenAI, Inc.",
            "jurisdiction": "United States (Delaware)",
            "year_founded": 2015,
            "annual_revenue_usd": 3_700_000_000,
        },
        "security": {
            "has_soc2": True,
            "has_iso27001": True,
            "data_classification_policy": True,
            "encryption_at_rest": True,
            "encryption_in_transit": True,
            "breach_last_12_months": False,
            "access_control_policy": True,
            "mfa_enforced": True,
        },
        "financial": {
            "audited_financials_available": True,
            "audit_opinion": "unqualified",
            "cyber_insurance_limit_usd": 50_000_000,
            "debt_to_equity_ratio": 1.2,
            "profitable_last_3_years": False,
        },
        "compliance": {
            "gdpr_compliant": True,
            "ccpa_compliant": True,
            "hipaa_compliant": True,
            "sox_compliant": True,
            "active_regulatory_investigation": False,
            "sanctions_pep_match": False,
            "data_residency_requirements_met": True,
        },
        "operational": {
            "bcp_dr_plan_exists": True,
            "bcp_dr_tested_last_12_months": True,
            "sub_processors": ["Microsoft Azure", "GitHub Copilot", "Stripe"],
            "geographic_presence": ["US", "UK", "EU", "Singapore", "Japan"],
            "sla_uptime_percentage": 99.95,
            "critical_vendor": True,
        },
    }


def run_demo():
    print("=" * 72)
    print("  TRUSTSPHERE AI — END-TO-END DEMONSTRATION")
    print("  Scenario: OpenAI (GPT-4o) Vendor Risk Assessment")
    print("=" * 72)

    # ── Step 1: Ingest ──────────────────────────────────────────────────
    print("\n[1/9] Ingesting questionnaire data...")
    raw = build_openai_questionnaire()
    intake = ingest_from_dict(raw)
    assert intake.valid, f"Ingestion failed: {intake.errors}"
    q = intake.questionnaire
    print(f"  Vendor: {q.supplier.name} ({q.supplier.legal_entity})")
    print(f"  Jurisdiction: {q.supplier.jurisdiction}")

    # ── Step 2: Risk Scoring ────────────────────────────────────────────
    print("\n[2/9] Scoring vendor risk...")
    scorecard = score_questionnaire(q)
    print(f"  Aggregate Score: {scorecard.aggregate_score:.2f}/5.00")
    print(f"  Risk Tier: {scorecard.risk_tier.value}")
    print(f"  Elevated Flags: {scorecard.elevated_flags}")
    for domain, ds in scorecard.domain_breakdown.items():
        print(f"    {domain.capitalize():15s} {ds.score:.2f}  {ds.rationale[:60]}...")

    # ── Step 3: Governance Gates ────────────────────────────────────────
    print("\n[3/9] Running governance gates...")
    gov = run_governance_gates(q, scorecard)
    for g in gov.gates:
        print(f"  {g.gate_name:20s} {g.status.value.upper():5s}  {g.details}")
    apply_override(gov, scorecard.aggregate_score, 2.5,
                   "Manual review confirms controls", "compliance_lead",
                   two_person_approval_id="analyst-02")

    # ── Step 4: Audit Trail ─────────────────────────────────────────────
    print("\n[4/9] Logging to audit chain...")
    audit = AuditLogger()
    audit.log("scoring_completed",
              {"id": "system", "type": "ai_agent", "role": None},
              scorecard.vendor_id, "risk_assessment",
              f"ra-{scorecard.vendor_id}", "create",
              "AI score generated", state_after=scorecard.to_dict())
    audit.log("governance_completed",
              {"id": "compliance_lead", "type": "human", "role": "compliance_officer"},
              scorecard.vendor_id, "governance_review",
              f"gov-{scorecard.vendor_id}", "override",
              "Score overridden after 2-person approval",
              governance_context={"original": scorecard.aggregate_score, "new": 2.5})
    print(f"  Events logged: {len(audit.get_events())}")
    print(f"  Chain intact: {audit.verify_chain()}")

    # ── Step 5: Human Review ────────────────────────────────────────────
    print("\n[5/9] Human-in-the-loop review...")
    review_svc = HumanReviewService()
    record = review_svc.create_review(scorecard.vendor_id, scorecard.risk_tier, 2.5)
    decision = ReviewDecision(
        vendor_id=scorecard.vendor_id,
        decision=Decision.APPROVE,
        analyst_id="compliance_lead",
        comments="All controls verified. Vendor meets NHS DSP Toolkit standards.",
        override_score=2.5,
        two_person_approval_id="analyst-02",
    )
    review_svc.submit_decision(scorecard.vendor_id, decision)
    record = review_svc.get_review(scorecard.vendor_id)
    print(f"  Status: {record.status.value.upper()}")
    print(f"  Final Score: {record.final_score:.2f}")
    print(f"  Assigned Role: {record.assignment.assigned_role}")

    # ── Step 6: DPIA Assessment ─────────────────────────────────────────
    print("\n[6/9] Data Protection Impact Assessment...")
    dpia_req = DPIARequest(
        title="GPT-4o API Integration for Patient Data Processing",
        controller="OpenAI",
        processor="Microsoft Azure",
        processing_purpose=ProcessingPurpose.AI_TRAINING,
        data_categories=[DataCategory.PSEUDONYMOUS, DataCategory.PERSONAL],
        data_subjects=["Patients", "Clinical staff", "End users"],
        retention_period_days=90,
        third_country_transfer=True,
        automated_decision_making=True,
        vulnerable_subjects=True,
    )
    dpia_result = assess_dpia(dpia_req)
    print(f"  Overall Risk: {dpia_result.overall_risk.value.upper()}")
    print(f"  Impacts Assessed: {len(dpia_result.impacts)}")
    print(f"  DPO Consultation Required: {dpia_result.dpo_consultation_required}")
    print(f"  Prior Authority Required: {dpia_result.prior_authority_required}")
    print(f"  Recommendations: {len(dpia_result.recommendations)}")
    for r in dpia_result.recommendations[:3]:
        print(f"    \u2022 {r[:80]}...")

    # ── Step 7: AI Risk Assessment ──────────────────────────────────────
    print("\n[7/9] AI Risk Assessment (EU AI Act)...")
    ai_req = AIAssessmentRequest(
        system_name="GPT-4o API",
        domain=AIDomain.CUSTOMER_SERVICE,
        description="Large language model API for healthcare assistance, customer service, and content generation",
        involves_sensitive_data=True,
        automated_decision_making=True,
        profiling=True,
        affects_vulnerable_groups=True,
        public_facing=True,
        high_risk_third_party_integration=True,
        human_oversight=HumanOversightLevel.HUMAN_ON_THE_LOOP,
        training_data_description="Web text, code, licensed data up to 2023",
        model_type="Transformer-based LLM",
    )
    ai_result = assess_ai_risk(ai_req)
    print(f"  Risk Category: {ai_result.risk_category.value.upper()}")
    print(f"  Risk Score: {ai_result.risk_score}/5")
    print(f"  Risk Factors Present: {len([f for f in ai_result.risk_factors if f.present])}")
    print(f"  Governance Controls Required: {len([c for c in ai_result.governance_controls if c.required])}")
    print(f"  Requires DPIA: {ai_result.requires_dpia}")
    print(f"  Requires Human Review: {ai_result.requires_human_review}")
    print(f"  Recommended Oversight: {ai_result.recommended_oversight.value.replace('_', ' ').title()}")
    print(f"  Summary: {ai_result.summary[:120]}...")

    # ── Step 8: Risk Register ───────────────────────────────────────────
    print("\n[8/9] Populating risk register...")
    rr = RiskRegister()
    risks_data = [
        (RiskCategory.DATA_BREACH, "Patient data exposed via GPT-4o prompt leakage",
         ImpactLevel.CRITICAL, Likelihood.MEDIUM,
         "Deploy prompt filtering, input sanitisation, and data masking layer",
         "CISO", "GDPR Art. 32, NHS DSP Toolkit Std 2"),
        (RiskCategory.AI_HALLUCINATION, "LLM generates incorrect medical advice causing patient harm",
         ImpactLevel.CRITICAL, Likelihood.MEDIUM,
         "Mandatory human-in-the-loop review for all clinical outputs; confidence scoring",
         "Clinical Safety Officer", "EU AI Act Art. 14, NHS Clinical Safety"),
        (RiskCategory.REGULATORY_NONCOMPLIANCE, "AI system used for diagnosis without MHRA approval",
         ImpactLevel.HIGH, Likelihood.MEDIUM,
         "Complete conformity assessment before clinical deployment; engage MHRA",
         "DPO", "EU AI Act Art. 43, UK CA 2024"),
        (RiskCategory.BIAS_DISCRIMINATION, "GPT-4o shows demographic bias in patient triage recommendations",
         ImpactLevel.HIGH, Likelihood.MEDIUM,
         "Quarterly bias audits on protected characteristics; fairness dashboard",
         "AI Governance Lead", "Equality Act 2010, EU AI Act Art. 10"),
        (RiskCategory.THIRD_PARTY_FAILURE, "Microsoft Azure outage disrupts GPT-4o API availability",
         ImpactLevel.HIGH, Likelihood.LOW,
         "Multi-region deployment; documented DR plan with RTO 15min",
         "Head of IT", "DORA Art. 11, NHS DSP Std 7"),
        (RiskCategory.CYBER_ATTACK, "Jailbreak attack on GPT-4o exposes sensitive organisation data",
         ImpactLevel.CRITICAL, Likelihood.HIGH,
         "Deploy Guardrails layer; real-time monitoring; incident response SLA 1hr",
         "CISO", "DORA Art. 9-10"),
    ]
    for cat, desc, impact, likelihood, mitigation, owner, reg in risks_data:
        rr.add(cat, desc, impact, likelihood, mitigation, owner,
               vendor_id=scorecard.vendor_id, regulation_ref=reg)
    print(f"  Total Risks: {len(rr.risks)}")
    print(f"  Open: {len(rr.open_risks)}  |  Critical: {len(rr.critical_risks)}  |  High: {len(rr.high_risks)}")
    print(f"  Avg Inherent Score: {rr.summary['avg_inherent_score']}")

    # ── Step 9: PDF Reports ─────────────────────────────────────────────
    print("\n[9/9] Generating professional PDF reports...")
    report_paths = []
    p1 = generate_vendor_dd_report(q, scorecard, gov, record, audit, rr.risks)
    report_paths.append(("Vendor Due Diligence", p1))
    print(f"  [OK] Vendor DD Report: {os.path.basename(p1)}")

    p2 = generate_dpia_report(dpia_req, dpia_result)
    report_paths.append(("DPIA Assessment", p2))
    print(f"  [OK] DPIA Report: {os.path.basename(p2)}")

    p3 = generate_ai_risk_report(ai_result)
    report_paths.append(("AI Risk Assessment", p3))
    print(f"  [OK] AI Risk Report: {os.path.basename(p3)}")

    p4 = generate_combined_report(
        vendor_name="OpenAI", scorecard=scorecard,
        dpia_result=dpia_result, ai_risk_result=ai_result,
        review=record, audit=audit, risks=rr.risks,
        filename="integrated_openai_governance_report.pdf",
    )
    report_paths.append(("Integrated Governance", p4))
    print(f"  [OK] Combined Report: {os.path.basename(p4)}")

    # ── Summary ─────────────────────────────────────────────────────────
    print("\n" + "=" * 72)
    print("  DEMO COMPLETE — OpenAI Assessment Summary")
    print("=" * 72)
    print(f"""
  Vendor:               OpenAI (GPT-4o API)
  Risk Score:           {scorecard.aggregate_score:.2f}/5.00
  Risk Tier:            {scorecard.risk_tier.value}
  Elevated Flags:       {len(scorecard.elevated_flags)}
  Governance Gates:     {'PASSED' if gov.all_passed() else 'FAILED'}

  DPIA Result:          {'REQUIRED' if dpia_result.dpo_consultation_required else 'NOT REQUIRED'}
  DPIA Overall Risk:    {dpia_result.overall_risk.value.upper()}
  GDPR Articles:        {len(dpia_result.gdpr_articles_applicable)}
  DPIA Recommendations: {len(dpia_result.recommendations)}

  AI Risk Rating:       {ai_result.risk_category.value.upper()}
  AI Risk Score:        {ai_result.risk_score}/5
  AI Risk Factors:      {len([f for f in ai_result.risk_factors if f.present])}
  Controls Required:    {len([c for c in ai_result.governance_controls if c.required])}
  Requires Conformity:  {'YES' if ai_result.requires_conformity_assessment else 'NO'}

  Approval Status:      {record.status.value.upper()}
  Review Role:          {record.assignment.assigned_role}
  Final Score:          {record.final_score:.2f}

  Risk Register:        {len(rr.risks)} items ({len(rr.open_risks)} open)
  Audit Chain:          {'INTACT' if audit.verify_chain() else 'COMPROMISED'}
  Audit Events:         {len(audit.get_events())}

  Reports Generated:    {len(report_paths)}
""")

    for name, path in report_paths:
        size_kb = os.path.getsize(path) // 1024
        print(f"  [{size_kb:>3d} KB] {name:25s} {os.path.basename(path)}")

    print("\n" + "=" * 72)
    print("  Reports saved to:", os.path.dirname(report_paths[0][1]))
    print("=" * 72)

    return {
        "scorecard": scorecard,
        "gov": gov,
        "dpia_result": dpia_result,
        "ai_result": ai_result,
        "review": record,
        "audit": audit,
        "risks": rr.risks,
        "report_paths": report_paths,
    }


if __name__ == "__main__":
    run_demo()
