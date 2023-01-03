import unittest
import warnings

from vika import Vika
from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestGetFields(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)

    def test_fields_all(self):
        fields = self.dst.fields.all()
        self.assertIsInstance(fields, list)
        primary_field = fields[0]
        self.assertTrue(primary_field.isPrimary)
        self.assertEqual(primary_field.name, "title")
        self.assertEqual(primary_field.type, "SingleText")

    def test_field_get(self):
        primary_field = self.dst.fields.get("title")
        self.assertTrue(primary_field.isPrimary)
        self.assertEqual(primary_field.name, "title")
        self.assertEqual(primary_field.type, "SingleText")


if __name__ == "__main__":
    unittest.main()
