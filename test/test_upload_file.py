import os
import time
import unittest

from vika import Vika

from . import TEST_API_BASE, TEST_API_TOKEN, TEST_TABLE


class TestUploadFile(unittest.TestCase):
    def setUp(self):
        self.vika = Vika(TEST_API_TOKEN)
        self.vika.set_api_base(TEST_API_BASE)
        self.dst = self.vika.datasheet(TEST_TABLE)

    def test_upload_file(self):
        test_url = "https://img9.doubanio.com/view/subject/s/public/s26849345.jpg"
        test_file = self.dst.upload_file(test_url)
        self.record = self.dst.records.filter(title="无人生还").get()
        self.record.cover = [test_file]
        self.assertIsNotNone(test_file.get("token"))

        time.sleep(2)

        test_local_file = "vikaji.png"
        filepath = os.path.join(os.path.dirname(__file__), test_local_file)
        test_file = self.dst.upload_file(filepath)
        self.assertEqual(test_file.get("mimeType"), "image/png")

    # def test_upload_file_auto(self):
    #     time.sleep(2)
    #     # 显式地传入附件字段，直接为附件字段赋值网络地址，可以自动上传文件。
    #     self.dst = self.vika.datasheet(TEST_TABLE, attachment_fields=["cover"])
    #     self.record = self.dst.records.filter(title="无人生还").get()
    #     test_url = "https://img9.doubanio.com/view/subject/s/public/s26849345.jpg"
    #     self.record.cover = [test_url]

    def tearDown(self):
        self.record.cover = None


if __name__ == "__main__":
    unittest.main()
