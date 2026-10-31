import json
import unittest

from main import VendorAssessment, app
from pydantic import ValidationError
from test_api_contract import request


class InputContractTests(unittest.IsolatedAsyncioTestCase):
    def test_whitespace_is_not_a_vendor_identity(self):
        for name in ('  ', '\n\t', ' A '):
            with self.subTest(name=name), self.assertRaises(ValidationError):
                VendorAssessment(vendor_name=name)
        self.assertEqual(VendorAssessment(vendor_name=' Fictional Supplier ').vendor_name,
                         'Fictional Supplier')

    async def test_misspelled_risk_flag_is_not_silently_ignored(self):
        for path in ('/assess', '/assess/report'):
            status, headers, body = await request(app, 'POST', path, {
                'vendor_name': 'Fictional Supplier', 'sanction_or_pep_match': True,
            })
            self.assertEqual(status, 422)
            self.assertEqual(json.loads(body)['detail'][0]['type'], 'extra_forbidden')
            self.assertNotIn('content-disposition', headers)

    async def test_valid_risk_flag_still_reaches_human_review(self):
        status, _, body = await request(app, 'POST', '/assess', {
            'vendor_name': 'Fictional Supplier', 'sanctions_or_pep_match': True,
        })
        self.assertEqual(status, 200)
        self.assertTrue(json.loads(body)['human_review_required'])
