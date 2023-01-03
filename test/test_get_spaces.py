import unittest
import warnings

from vika import Vika

from . import TOKEN, DOMAIN


class TestGetSpaces(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.apitable = apitable

    def test_spaces_all(self):
        spaces = self.apitable.spaces.all()
        self.assertIsInstance(spaces, list)
        first_space = spaces[0]
        self.assertIsNotNone(first_space.name)
        self.assertIsInstance(first_space.name, str)


if __name__ == "__main__":
    unittest.main()
