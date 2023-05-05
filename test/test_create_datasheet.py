import unittest
import warnings
from vika import Vika
from . import DOMAIN, TOKEN, SPACE_ID, FOLDER_ID


class TestCreateDatasheet(unittest.TestCase):
    """Apitable Python SDK create datasheet test class
    - Datasheet Creation SDK Test
    """

    def setUp(self):
        """Create a datasheet test class object initial hook:"""
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.spc = apitable.space(SPACE_ID)

    def test_datasheet_create(self):
        """Datasheet Creation SDK Test"""
        req_data = {"name": "python_test_datasheet_create", "folderId": FOLDER_ID}
        self.datasheet = self.spc.datasheets.create(req_data)
        self.assertIsNotNone(self.datasheet.id)

    def tearDown(self):
        """Create a Datasheet test class object destroy hook:"""


if __name__ == "__main__":
    unittest.main()
