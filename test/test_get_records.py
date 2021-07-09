import unittest

from vika import Vika
from . import TEST_TABLE, TEST_API_BASE, TEST_API_TOKEN


class TestGetRecords(unittest.TestCase):
    def setUp(self):
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.dst = vika.datasheet(TEST_TABLE)

    def test_record_count(self):
        self.assertEqual(self.dst.records.all().count(), 1)

    def test_record_filter_get(self):
        self.assertEqual(self.dst.records.filter(title="无人生还").get().title, "无人生还")

    def test_record_all(self):
        # 不存在的视图返回空记录
        self.assertEqual(self.dst.records.all(viewId="viw6oKVVbMynt").count(), 0)

    # FXIME: 现在 rest api 返回有问题，先不加这条
    # def test_record_all_with_params(self):
    #     # 不存在的分页返回空记录
    #     self.assertEqual(self.dst.records.all(pageNum=2).count(), 0)


if __name__ == '__main__':
    unittest.main()
