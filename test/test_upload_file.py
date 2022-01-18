import os
import time
import unittest
import warnings

from vika import Vika

from . import TEST_API_BASE, TEST_API_TOKEN, TEST_TABLE


class TestUploadFile(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        self.vika = Vika(TEST_API_TOKEN)
        self.vika.set_api_base(TEST_API_BASE)
        self.dst = self.vika.datasheet(TEST_TABLE)

    def test_upload_file(self):
        test_url = "https://img9.doubanio.com/view/subject/s/public/s26849345.jpg"
        test_file = self.dst.upload_attachment(test_url)
        self.assertIsNotNone(test_file.get("token"))

        time.sleep(2)

        test_local_file = "vikaji.png"
        filepath = os.path.join(os.path.dirname(__file__), test_local_file)
        test_file = self.dst.upload_file(filepath)
        self.assertEqual(test_file.get("mimeType"), "image/png")


if __name__ == "__main__":
    unittest.main()
