import unittest
import warnings
from vika import Vika
from . import TEST_API_BASE, TEST_API_TOKEN, TEST_SPACE_ID


class TestCreateFields(unittest.TestCase):
    """VIKA Python SDK 创建表格测试类
        - 表格创建SDK测试
    """

    def setUp(self):
        """创建表格测试类 对象初始hook：

        """
        warnings.simplefilter('ignore', ResourceWarning)
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.spc = vika.space(TEST_SPACE_ID)

    def test_datasheet_create(self):
        """表格创建SDK测试

        """
        req_data = {'name': 'table_name'}
        self.datasheet = self.spc.datasheets.create(req_data)
        self.assertIsNotNone(self.datasheet.id)

    def tearDown(self):
        """创建表格测试类 对象销毁hook：

        """


if __name__ == '__main__':
    unittest.main()

