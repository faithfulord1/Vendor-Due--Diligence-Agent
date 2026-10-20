"""Exercise FastAPI routing and serialization without sockets or extra packages."""
import asyncio
import json
import unittest

from main import app
from api.index import app as serverless_app


async def request(application, method, path, payload=None, raw_body=None):
    """Minimal one-request ASGI transport, not a real HTTP server."""
    body = raw_body if raw_body is not None else (
        json.dumps(payload).encode("utf-8") if payload is not None else b""
    )
    messages = []
    consumed = False

    async def receive():
        nonlocal consumed
        if not consumed:
            consumed = True
            return {"type": "http.request", "body": body, "more_body": False}
        return {"type": "http.disconnect"}

    async def send(message):
        messages.append(message)

    scope = {
        "type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": "1.1", "method": method, "scheme": "http",
        "path": path, "raw_path": path.encode("ascii"), "query_string": b"",
        "root_path": "", "headers": [(b"content-type", b"application/json")],
        "server": ("test.invalid", 80), "client": ("127.0.0.1", 12345),
    }
    await asyncio.wait_for(application(scope, receive, send), timeout=5)
    starts = [m for m in messages if m["type"] == "http.response.start"]
    if len(starts) != 1:
        raise AssertionError("Expected exactly one ASGI response")
    start = starts[0]
    response_body = b"".join(
        m.get("body", b"") for m in messages if m["type"] == "http.response.body"
    )
    return (
        start["status"],
        {key.decode("latin-1"): value.decode("latin-1")
         for key, value in start["headers"]},
        response_body,
    )


class ApiContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_health_and_serverless_entrypoint(self):
        for application in (app, serverless_app):
            with self.subTest(entrypoint=application.title):
                status, headers, body = await request(application, "GET", "/health")
                self.assertEqual(status, 200)
                self.assertEqual(json.loads(body)["status"], "ok")
                self.assertIn("application/json", headers["content-type"])

    async def test_json_assessment_preserves_human_escalation(self):
        status, headers, body = await request(app, "POST", "/assess", {
            "vendor_name": "Fictional Supplier", "sanctions_or_pep_match": True,
        })
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers["content-type"])
        result = json.loads(body)
        self.assertTrue(result["human_review_required"])
        self.assertIn("TPRM-SAN-001", result["critical_blockers"])
        self.assertIn("does not approve", result["governance"])

    async def test_report_is_private_download_with_utf8_and_pending_decision(self):
        status, headers, body = await request(serverless_app, "POST", "/assess/report", {
            "vendor_name": "Fictional Ìmọ̀ Supplier", "sanctions_or_pep_match": True,
        })
        self.assertEqual(status, 200)
        self.assertEqual(headers["cache-control"], "no-store")
        self.assertEqual(headers["x-content-type-options"], "nosniff")
        self.assertEqual(headers["content-disposition"],
                         'attachment; filename="vendor-evidence-plan.md"')
        self.assertIn("text/markdown", headers["content-type"])
        self.assertEqual(int(headers["content-length"]), len(body))
        report = body.decode("utf-8")
        for expected in ("Ìmọ̀", "UNVERIFIED", "TPRM-SAN-001",
                         "PENDING AUTHORISED HUMAN REVIEW"):
            self.assertIn(expected, report)

    async def test_report_neutralises_questionnaire_markup_over_api(self):
        status, _, body = await request(app, "POST", "/assess/report", {
            "vendor_name": "Fake\n# APPROVED <script>x</script> [go](https://example.invalid)",
        })
        self.assertEqual(status, 200)
        report = body.decode("utf-8")
        for forbidden in ("\n# APPROVED", "<script>", "[go]("):
            self.assertNotIn(forbidden, report)
        self.assertIn("PENDING AUTHORISED HUMAN REVIEW", report)

    async def test_missing_short_null_and_invalid_flag_are_rejected(self):
        for path in ("/assess", "/assess/report"):
            for payload in ({}, {"vendor_name": "X"}, {"vendor_name": None},
                            {"vendor_name": "Fictional", "mfa_enforced": "unknown"}):
                with self.subTest(path=path, payload=payload):
                    status, headers, body = await request(app, "POST", path, payload)
                    self.assertEqual(status, 422)
                    self.assertIn("application/json", headers["content-type"])
                    self.assertIn("detail", json.loads(body))
                    self.assertNotIn("content-disposition", headers)

    async def test_malformed_json_does_not_create_report(self):
        for path in ("/assess", "/assess/report"):
            with self.subTest(path=path):
                status, headers, body = await request(
                    app, "POST", path, raw_body=b'{"vendor_name":'
                )
                self.assertEqual(status, 422)
                self.assertEqual(json.loads(body)["detail"][0]["type"], "json_invalid")
                self.assertNotIn("content-disposition", headers)

    async def test_get_cannot_generate_assessment_or_report(self):
        for path in ("/assess", "/assess/report"):
            with self.subTest(path=path):
                status, headers, _ = await request(app, "GET", path)
                self.assertEqual(status, 405)
                self.assertIn("POST", headers["allow"])
                self.assertNotIn("content-disposition", headers)

    async def test_openapi_documents_both_response_formats(self):
        status, _, body = await request(serverless_app, "GET", "/openapi.json")
        self.assertEqual(status, 200)
        paths = json.loads(body)["paths"]
        self.assertIn("application/json", paths["/assess"]["post"]["responses"]["200"]["content"])
        self.assertIn("text/markdown", paths["/assess/report"]["post"]["responses"]["200"]["content"])


if __name__ == "__main__":
    unittest.main()
