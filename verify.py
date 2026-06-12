import sys
sys.path.insert(0, ".")

from src.questionnaire.intake import ingest_from_dict
from src.risk_scoring.scorer import score_questionnaire, RiskTier
from src.governance.controls import run_governance_gates, apply_override
from src.review.approval import HumanReviewService, ReviewDecision, Decision
from src.audit.logger import AuditLogger

data = {
    "supplier": {
        "vendor_id": "VND-001", "name": "TestCorp", "legal_entity": "TestCorp Inc",
        "jurisdiction": "US", "year_founded": 2010,
    },
    "security": {
        "has_soc2": False, "has_iso27001": True, "data_classification_policy": True,
        "encryption_at_rest": True, "encryption_in_transit": True,
        "breach_last_12_months": True, "access_control_policy": True, "mfa_enforced": False,
    },
    "financial": {
        "audited_financials_available": True, "audit_opinion": "unqualified",
        "cyber_insurance_limit_usd": 5_000_000, "profitable_last_3_years": True,
    },
    "compliance": {
        "gdpr_compliant": True, "ccpa_compliant": True, "hipaa_compliant": False,
        "sox_compliant": True, "active_regulatory_investigation": False,
        "sanctions_pep_match": False, "data_residency_requirements_met": True,
    },
    "operational": {
        "bcp_dr_plan_exists": True, "bcp_dr_tested_last_12_months": False,
        "critical_vendor": True,
    },
}

result = ingest_from_dict(data)
assert result.valid, f"Ingestion failed: {result.errors}"
print("PASS  Ingest")

card = score_questionnaire(result.questionnaire)
assert 1.0 <= card.aggregate_score <= 5.0
print(f"PASS  Score: {card.risk_tier.value} ({card.aggregate_score:.2f})")

gov = run_governance_gates(result.questionnaire, card)
print(f"PASS  Governance: all_passed={gov.all_passed()}")

apply_override(gov, card.aggregate_score, 2.0, "Comp controls", "analyst-42", "approver-7")
assert gov.override is not None
print(f"PASS  Override: new_score={gov.override['new_score']}")

svc = HumanReviewService()
svc.create_review("VND-001", card.risk_tier, card.aggregate_score)
d = ReviewDecision("VND-001", Decision.APPROVE, "analyst-1", "ok")
record = svc.submit_decision("VND-001", d)
assert record.status.value == "approved"
print(f"PASS  Review: {record.status.value}")

log = AuditLogger()
for i in range(3):
    log.log(
        event_type="test", actor={"id": "t"}, vendor_id=f"VND-{i:03d}",
        resource_type="t", resource_id=str(i), action="c", change_reason="x",
    )
assert log.verify_chain()
print(f"PASS  Audit: chain intact ({len(log._chain)} events)")

log._chain[0].change_reason = "tampered"
assert not log.verify_chain()
print("PASS  Audit: tamper detected")

print("\nAll checks passed.")
