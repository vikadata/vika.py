import time
import unittest
import warnings

from vika import Vika

from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestDeleteRecords(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)

    def test_record_delete(self):
        self.dst.records.create({"title": "apitable"})
        time.sleep(1)
        record = self.dst.records.get(title="apitable")
        time.sleep(1 / 5)
        r = record.delete()
        self.assertTrue(r)

        time.sleep(1 / 5)
        record_id = "recnotexist"
        with self.assertRaises(Exception) as e:
            self.dst.delete_records([record_id])
        self.assertIsNotNone(e)

    def tearDown(self):
        time.sleep(1)
        self.dst.records.create({"title": "apitable"})


if __name__ == "__main__":
    unittest.main()
