from main import VendorAssessment, assess_vendor


def run_checks():
    low = assess_vendor(VendorAssessment(
        vendor_name="Example Secure Supplier",
        has_iso27001=True,
        mfa_enforced=True,
        encryption_at_rest=True,
        encryption_in_transit=True,
        bcp_tested_last_12_months=True,
    ))
    assert low["risk_tier"] == "low"
    assert low["human_review_required"] is False

    high = assess_vendor(VendorAssessment(
        vendor_name="Critical Health Processor",
        critical_vendor=True,
        handles_personal_data=True,
        handles_special_category_data=True,
        mfa_enforced=False,
        encryption_at_rest=True,
        encryption_in_transit=False,
        bcp_tested_last_12_months=False,
        breach_last_12_months=True,
    ))
    assert high["risk_tier"] in {"high", "critical"}
    assert high["human_review_required"] is True
    assert any(item["control_id"] == "TPRM-SEC-001" for item in high["findings"])
    assert any(item["control_id"] == "TPRM-DPIA-001" for item in high["findings"])

    sanctions = assess_vendor(VendorAssessment(
        vendor_name="Screening Example",
        sanctions_or_pep_match=True,
    ))
    assert "TPRM-SAN-001" in sanctions["critical_blockers"]
    assert sanctions["human_review_required"] is True

    print("All TrustSphere verification checks passed.")


if __name__ == "__main__":
    run_checks()
