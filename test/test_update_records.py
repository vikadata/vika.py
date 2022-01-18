import time
import unittest
import warnings

from vika import Vika

from . import TEST_API_BASE, TEST_API_TOKEN, TEST_TABLE


class TestUpdateRecords(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.dst = vika.datasheet(TEST_TABLE)

    def test_record_update(self):
        # 更新单个字段
        record = self.dst.records.get(title="无人生还")
        record.title = "无人生还2"
        self.assertEqual(record.title, "无人生还2")
        time.sleep(1 / 5)

        # 更新多个字段
        record = self.dst.records.get(title="无人生还2")
        r = record.update({"title": '无人生还3', "comment": '真好看'})
        self.assertEqual(r.title, "无人生还3")
        self.assertEqual(r.comment, "真好看")
        time.sleep(1 / 5)

        # 更新多条记录
        self.dst.records.filter(title="无人生还3").update(title="无人生还4")
        record = self.dst.records.get(title="无人生还4")
        self.assertEqual(record.title, "无人生还4")
        time.sleep(1 / 5)

    def test_bulk_update(self):
        records = self.dst.records.bulk_create([{
            "title": "魔法书1"
        }, {
            "title": "魔法书2"
        }, {
            "title": "魔法书3"
        }])
        update_data = [{
            "recordId": rec._id,
            "fields": {
                "title": 'new' + rec.title
            }
        } for rec in records]
        updated_records = self.dst.records.bulk_update(update_data)
        self.assertEqual(updated_records[0].title, 'new' + records[0].title)
        self.dst.delete_records(records)

    def test_update_or_create(self):
        # 更新
        record, created = self.dst.records.update_or_create(title="无人生还4",
                                                            defaults={
                                                                "title":
                                                                "无人生还",
                                                                "comment":
                                                                "真好看1"
                                                            })
        self.assertFalse(created)
        self.assertEqual(record.comment, "真好看1")
        time.sleep(1 / 5)
        # 创建记录
        record, created = self.dst.records.update_or_create(
            title="不能存在的记录2", defaults={"comment": "真好看"})
        self.assertTrue(created)
        self.assertEqual(record.comment, "真好看")
        self.assertEqual(record.title, "不能存在的记录2")
        self.dst.records.filter(title="不能存在的记录2").delete()


if __name__ == '__main__':
    unittest.main()
