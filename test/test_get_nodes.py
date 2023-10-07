import unittest
import warnings

from vika import Vika

from . import TOKEN, DOMAIN, SPACE_ID, FOLDER_ID


class TestGetNodes(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        apitable = Vika(TOKEN)
        apitable.set_api_base(DOMAIN)
        self.apitable = apitable

    def test_space_root_nodes_all(self):
        space_root_nodes = self.apitable.space(SPACE_ID).nodes.all()
        self.assertIsInstance(space_root_nodes, list)
        first_node = space_root_nodes[0]
        self.assertIn(first_node.type, ["Datasheet", "Folder", "Mirror", "Form", "ERROR NODE TYPE"])

    def test_get_node_detail(self):
        node = self.apitable.nodes.get(FOLDER_ID)
        self.assertEqual(node.id, FOLDER_ID)
        self.assertIsNotNone(node.children)

    def test_search_nodes(self):
        nodes = self.apitable.nodes.search(spaceId=SPACE_ID, type='Folder')
        self.assertIsInstance(nodes, list)

if __name__ == "__main__":
    unittest.main()
