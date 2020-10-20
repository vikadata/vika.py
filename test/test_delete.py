import time
import unittest

from vika import Vika

from . import TEST_API_BASE, TEST_API_TOKEN, TEST_TABLE


class TestDelete(unittest.TestCase):
    def setUp(self):
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.dst = vika.datasheet(TEST_TABLE)

    def test_record_delete(self):
        record = self.dst.records.get(title="无人生还")
        time.sleep(2)
        r = record.delete()
        self.assertTrue(r)

        time.sleep(2)
        record_id = "recnotexist"
        r = self.dst.delete_records([record_id])
        self.assertFalse(r)

    def tearDown(self):
        time.sleep(2)
        self.dst.records.create({"title": "无人生还"})


if __name__ == "__main__":
    unittest.main()
