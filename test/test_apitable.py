import unittest
from unittest.mock import patch

from vika.space import Space


class TestApitable(unittest.TestCase):
    """
    base test class.
    """

    def setUp(self):
        """
        set up.
        """
        with patch('vika.apitable') as mock_apitable:
            self._apitable = mock_apitable
            self._space = Space(self._apitable, 'test_space_id')
