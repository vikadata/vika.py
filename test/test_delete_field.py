import unittest
import warnings
from vika import Vika
from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestDeleteFields(unittest.TestCase):
    """Apitable Python SDK Field delete test class
    - Field delete SDK test
    """

    def setUp(self):
        """Create a field test class object initial hook:
        - Warnings related to resource usage are ignored
        - Initialize the Apitable object
        - Get action sheet
        - add fields
        """
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)
        req_data = {
            "type": "SingleText",
            "name": "test_field_delete",
            "property": {"defaultValue": "hello apitable"},
        }
        self.field = self.dst.fields.create(req_data)

    def test_field_delete(self):
        """Field delete SDK test:"""
        is_true = self.dst.fields.delete(self.field.id)
        self.assertTrue(is_true)


if __name__ == "__main__":
    unittest.main()
