import unittest
import warnings

from vika import Vika
from . import TEST_API_BASE, TEST_API_TOKEN


class TestGetSpaces(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.vika = vika

    def test_spaces_all(self):
        spaces = self.vika.spaces.all()
        self.assertIsInstance(spaces, list)
        first_space = spaces[0]
        self.assertIsNotNone(first_space.name)
        self.assertIsInstance(first_space.name, str)


if __name__ == '__main__':
    unittest.main()
