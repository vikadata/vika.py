import os
import time
import unittest
import warnings

from vika import Vika

from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestUploadFile(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)

    def test_upload_file(self):
        test_url = "https://i0.wp.com/apitable.com/wp-content/uploads/2022/11/IT.png"
        test_file = self.dst.upload_attachment(test_url)
        self.assertIsNotNone(test_file.get("token"))

        time.sleep(2)

        test_local_file = "test.png"
        filepath = os.path.join(os.path.dirname(__file__), test_local_file)
        test_file = self.dst.upload_file(filepath)
        self.assertEqual(test_file.get("mimeType"), "image/png")


if __name__ == "__main__":
    unittest.main()
