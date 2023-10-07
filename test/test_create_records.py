from typing import List
import unittest
import time
import warnings

from vika.datasheet.record import Record
from vika import Vika
from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestCreateRecords(unittest.TestCase):


    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)
        self.created_records: List[Record] = []

    def test_record_create(self):
        time.sleep(1)
        record = self.dst.records.create({"title": "Advanced Mathematics"})
        time.sleep(1)
        self.assertIsNotNone(record._id)
        records = self.dst.records.bulk_create(
            [{"title": "Discrete Mathematics"}, {"title": "Linear Algebra"}]
        )
        self.created_records = records + [record]
        for rec in records:
            self.assertIsNotNone(rec._id)

    def tearDown(self):
        self.dst.delete_records(self.created_records)


if __name__ == "__main__":
    unittest.main()
