import time
import unittest
import warnings

from vika import Vika

from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestUpdateRecords(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)

    def test_record_update(self):
        # Update a single field
        record = self.dst.records.get(title="apitable")
        record.title = "apitable_py"
        self.assertEqual(record.title, "apitable_py")
        time.sleep(1 / 5)

        # Update multiple fields
        record = self.dst.records.get(title="apitable_py")
        r = record.update({"title": "apitable_api", "comment": "apitable rest api"})
        self.assertEqual(r.title, "apitable_api")
        self.assertEqual(r.comment, "apitable rest api")
        time.sleep(1 / 5)

        # Update multiple records
        self.dst.records.filter(title="apitable_api").update(title="apitable_widget")
        record = self.dst.records.get(title="apitable_widget")
        self.assertEqual(record.title, "apitable_widget")
        time.sleep(1 / 5)

    def test_bulk_update(self):
        records = self.dst.records.bulk_create(
            [
                {"title": "apitable_py"},
                {"title": "apitable_api"},
                {"title": "apitable_widget"},
            ]
        )
        update_data = [
            {"recordId": rec._id, "fields": {"title": "new" + rec.title}}
            for rec in records
        ]
        updated_records = self.dst.records.bulk_update(update_data)
        self.assertEqual(updated_records[0].title, "new" + records[0].title)
        self.dst.delete_records(records)

    def test_update_or_create(self):
        record, created = self.dst.records.update_or_create(
            title="apitable_api",
            defaults={"title": "apitable_widget", "comment": "apitable widget sdk"},
        )
        self.assertTrue(created)
        self.assertEqual(record.comment, "apitable widget sdk")
        time.sleep(1 / 5)
        # Create a record
        record, created = self.dst.records.update_or_create(
            title="test_record", defaults={"comment": "apitable rest api"}
        )
        self.assertTrue(created)
        self.assertEqual(record.comment, "apitable rest api")
        self.assertEqual(record.title, "test_record")
        self.dst.records.filter(title="test_record").delete()
        self.dst.records.filter(title="apitable_widget").delete()


if __name__ == "__main__":
    unittest.main()
