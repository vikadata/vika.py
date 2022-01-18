import unittest
import warnings

from vika import Vika

from .env import TEST_API_BASE, TEST_API_TOKEN, TEST_SPACE_ID, TEST_FOLDER_ID


class TestGetNodes(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.vika = vika

    def test_space_root_nodes_all(self):
        space_root_nodes = self.vika.space(TEST_SPACE_ID).nodes.all()
        self.assertIsInstance(space_root_nodes, list)
        first_node = space_root_nodes[0]
        self.assertEqual(first_node.type, 'Folder')

    def test_get_node_detail(self):
        node = self.vika.nodes.get(TEST_FOLDER_ID)
        self.assertEqual(node.id, TEST_FOLDER_ID)
        self.assertIsNotNone(node.children)


if __name__ == '__main__':
    unittest.main()
