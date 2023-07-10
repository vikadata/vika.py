import unittest
import warnings

from vika import Vika
from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID_FOR_GET, VIEW_ID


class TestGetRecords(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID_FOR_GET)

    def test_record_count(self):
        self.assertEqual(self.dst.records.all().count(), 1)

    def test_record_filter_get(self):
        self.assertEqual(
            self.dst.records.filter(title="apitable").get().title, "apitable"
        )

    def test_record_all(self):
        self.assertEqual(
            self.dst.records.all(viewId=VIEW_ID).count(), 1)

    def test_get_or_create(self):
        # Ger record
        record, created = self.dst.records.get_or_create(title="apitable")
        self.assertFalse(created)

        # Create record
        record, created = self.dst.records.get_or_create(title="nonexistent record")
        record.delete()
        self.assertEqual(record.title, "nonexistent record")
        self.assertTrue(created)

    # FXIME: Now there is a problem with the return of the rest api, so don't add this first
    # def test_record_all_with_params(self):
    #     # Nonexistent pagination returns empty records
    #     self.assertEqual(self.dst.records.all(pageNum=2).count(), 0)


if __name__ == "__main__":
    unittest.main()
