import unittest
import time
import warnings
from vika import Vika
from . import TEST_TABLE, TEST_API_BASE, TEST_API_TOKEN


class TestCreateRecords(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.dst = vika.datasheet(TEST_TABLE)

    def test_record_create(self):
        time.sleep(1)
        record = self.dst.records.create({"title": "高等数学"})
        time.sleep(1)
        self.assertIsNotNone(record._id)
        records = self.dst.records.bulk_create([{
            "title": "离散数学"
        }, {
            "title": "线性代数"
        }])
        self.created_records = records + [record]
        for rec in records:
            self.assertIsNotNone(rec._id)

    def tearDown(self):
        self.dst.delete_records(self.created_records)


if __name__ == '__main__':
    unittest.main()
