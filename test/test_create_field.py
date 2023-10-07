import unittest
import warnings
from vika import Vika
from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestCreateFields(unittest.TestCase):
    """Apitable Python SDK create field test class
    - Field Creation SDK Test
    """

    def setUp(self):
        """Create a field test class object initial hook:
        - Warnings related to resource usage are ignored
        - Initialize the Apitable object
        - Get action sheet
        """
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)
        self.field = None

    def test_field_create(self):
        """Field Creation SDK Test"""
        req_data = {
            "type": "SingleText",
            "name": "test_field_create",
            "property": {"defaultValue": "hello apitable"},
        }
        self.field = self.dst.fields.create(req_data)
        self.assertIsNotNone(self.field.id)
        self.assertEqual(self.field.name, "test_field_create")

    def tearDown(self):
        """Create a field test class object to destroy the hook:
        - Delete test created fields
        """
        self.dst.fields.delete(self.field.id)


if __name__ == "__main__":
    unittest.main()
