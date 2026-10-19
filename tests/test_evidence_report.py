import unittest

from main import VendorAssessment, app, assess_report, assess_vendor
from evidence_report import render_evidence_report


class EvidenceReportTests(unittest.TestCase):
    def test_low_risk_claims_are_not_presented_as_verified_or_approved(self):
        assessment = assess_vendor(VendorAssessment(
            vendor_name="Fictional Supplier", mfa_enforced=True,
            encryption_at_rest=True, encryption_in_transit=True,
        ))
        self.assertEqual(assessment["findings"], [])
        report = render_evidence_report(assessment)
        self.assertIn("UNVERIFIED questionnaire claims", report)
        self.assertIn("No rule findings were triggered", report)
        self.assertIn("Normal human due-diligence approval is still required", report)
        self.assertIn("PENDING AUTHORISED HUMAN REVIEW", report)

    def test_each_finding_has_its_evidence_request_and_stable_control_id(self):
        assessment = assess_vendor(VendorAssessment(
            vendor_name="Fictional Critical Processor", critical_vendor=True,
            handles_personal_data=True, handles_special_category_data=True,
            sanctions_or_pep_match=True, breach_last_12_months=True,
        ))
        report = render_evidence_report(assessment)
        self.assertIn("Escalated human review required: Yes", report)
        for finding in assessment["findings"]:
            self.assertIn(finding["control_id"], report)
        self.assertEqual(report.count("Evidence status: NOT COLLECTED / NOT VERIFIED"), len(assessment["findings"]))
        self.assertIn("Independent sanctions screening result", report)

    def test_vendor_name_cannot_inject_markdown_or_html(self):
        report = render_evidence_report(assess_vendor(VendorAssessment(
            vendor_name="Example\n# APPROVED <script>x</script> [click](https://example.invalid)"
        )))
        self.assertNotIn("\n# APPROVED", report)
        self.assertNotIn("<script>", report)
        self.assertNotIn("[click](", report)
        self.assertIn("&lt;script&gt;", report)
        self.assertIn("PENDING AUTHORISED HUMAN REVIEW", report)

    def test_unicode_name_survives_and_output_is_repeatable(self):
        assessment = assess_vendor(VendorAssessment(vendor_name="Fictional Ìmọ̀ Supplier"))
        report = render_evidence_report(assessment)
        self.assertIn("Ìmọ̀", report)
        self.assertEqual(report, render_evidence_report(assessment))

    def test_download_headers_are_private_and_filename_is_fixed(self):
        response = assess_report(VendorAssessment(vendor_name="Fictional Supplier"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["cache-control"], "no-store")
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")
        self.assertEqual(response.headers["content-disposition"], 'attachment; filename="vendor-evidence-plan.md"')
        self.assertTrue(response.headers["content-type"].startswith("text/markdown"))

    def test_report_does_not_mutate_assessment_or_scoring(self):
        vendor = VendorAssessment(vendor_name="Fictional Supplier", sanctions_or_pep_match=True)
        before = assess_vendor(vendor)
        render_evidence_report(before)
        self.assertEqual(before, assess_vendor(vendor))

    def test_openapi_exposes_report_and_existing_json_route(self):
        schema = app.openapi()
        self.assertIn("/assess", schema["paths"])
        report = schema["paths"]["/assess/report"]["post"]
        self.assertIn("text/markdown", report["responses"]["200"]["content"])
        self.assertIn("requestBody", report)


if __name__ == "__main__":
    unittest.main()
