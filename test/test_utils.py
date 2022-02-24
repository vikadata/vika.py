import unittest

from vika.utils import query_parse


class TestUtils(unittest.TestCase):

    def test_query_parse(self):
        field_key_map = {}
        self.assertEqual(query_parse(field_key_map, a=1), "{a}=1")
        self.assertEqual(query_parse(field_key_map, a=1, b=2),
                         "AND({a}=1,{b}=2)")
        self.assertEqual(query_parse(field_key_map, a="1", b=2),
                         'AND({a}="1",{b}=2)')
        self.assertEqual(query_parse(field_key_map, a=1, b=['B', 'C', 'D']),
                         'AND({a}=1,{b}="B, C, D")')
        self.assertEqual(query_parse(field_key_map, a=1, b=True),
                         "AND({a}=1,{b}=TRUE())")
        self.assertEqual(query_parse(field_key_map, a=1, b=False),
                         "AND({a}=1,{b}=FALSE())")
        self.assertEqual(query_parse(field_key_map, a=1, b=None),
                         "AND({a}=1,{b}=BLANK())")


if __name__ == "__main__":
    unittest.main()
