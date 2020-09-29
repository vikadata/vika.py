import time
import unittest

from vika import Vika

from . import TEST_API_BASE, TEST_API_TOKEN, TEST_TABLE


class TestUpdate(unittest.TestCase):
    def setUp(self):
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.dst = vika.datasheet(TEST_TABLE)

    def test_record_update(self):
        # 更新单个字段
        record = self.dst.records.get(title="无人生还")
        record.title = "无人生还2"
        self.assertEqual(record.title, "无人生还2")
        time.sleep(1)

        # 更新多个字段
        record = self.dst.records.get(title="无人生还2")
        r = record.update({
            "title": '无人生还3',
            "comment": '真好看'
        })
        self.assertEqual(r, 1)
        self.assertEqual(record.title, "无人生还3")
        self.assertEqual(record.comment, "真好看")
        time.sleep(1)

        # 更新多条记录
        self.dst.records.filter(
            title="无人生还3").update(title="无人生还4")
        record = self.dst.records.get(title="无人生还4")
        self.assertEqual(record.title, "无人生还4")
        time.sleep(1)

    def tearDown(self):
        self.dst.records.filter(title="无人生还4").update(title="无人生还")


if __name__ == '__main__':
    unittest.main()
