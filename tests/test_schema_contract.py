"""Ensure generated API docs preserve the strict merged client contract."""
import unittest

from main import VendorAssessment, app


class SchemaContractTests(unittest.TestCase):
    def test_openapi_rejects_undeclared_client_fields(self):
        schema = app.openapi()['components']['schemas']['VendorAssessment']
        self.assertIs(schema['additionalProperties'], False)
        self.assertEqual(schema['required'], ['vendor_name'])

    def test_every_risk_flag_survives_validation_without_renaming(self):
        fields = VendorAssessment.model_fields
        flags = {name for name in fields if name != 'vendor_name'}
        self.assertEqual(len(flags), 12)
        for name in sorted(flags):
            for value in (False, True):
                with self.subTest(flag=name, value=value):
                    model = VendorAssessment.model_validate({'vendor_name':'Fictional Supplier', name:value})
                    self.assertIs(model.model_dump()[name], value)

    def test_openapi_and_model_expose_the_same_field_names(self):
        documented = app.openapi()['components']['schemas']['VendorAssessment']['properties']
        self.assertEqual(set(documented), set(VendorAssessment.model_fields))
        for name, field in documented.items():
            if name != 'vendor_name':
                self.assertEqual(field['type'], 'boolean')
                self.assertIs(field['default'], False)
