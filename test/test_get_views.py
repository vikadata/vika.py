import unittest
import warnings

from vika import Vika
from . import TOKEN, DOMAIN, SPACE_ID, DATASHEET_ID


class TestGetViews(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.dst = apitable.space(SPACE_ID).datasheet(DATASHEET_ID)

    def test_views_all(self):
        views = self.dst.views.all()
        self.assertIsInstance(views, list)
        first_view = views[0]
        self.assertEqual(first_view.name, "Grid View")
        self.assertEqual(first_view.type, "Grid")


if __name__ == "__main__":
    unittest.main()
