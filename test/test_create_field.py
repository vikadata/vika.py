import unittest
import warnings
from vika import Vika
from . import TEST_TABLE, TEST_API_BASE, TEST_API_TOKEN, TEST_SPACE_ID


class TestCreateFields(unittest.TestCase):
    """VIKA Python SDK 创建字段测试类
        - 字段创建SDK测试
    """

    def setUp(self):
        """创建字段测试类 对象初始hook：
            - 与资源使用相关的警告忽略
            - 初始化Vika对象
            - 获取操作表
        """
        warnings.simplefilter('ignore', ResourceWarning)
        vika = Vika(TEST_API_TOKEN)
        vika.set_api_base(TEST_API_BASE)
        self.dst = vika.space(TEST_SPACE_ID).datasheet(TEST_TABLE)

    def test_field_create(self):
        """字段创建SDK测试

        """
        req_data = {'type': 'SingleText', 'name': '标题', 'property': {'defaultValue': '默认文本'}}
        self.field = self.dst.fields.create(req_data)
        self.assertIsNotNone(self.field.id)
        self.assertEqual(self.field.name, '标题')

    def tearDown(self):
        """创建字段测试类 对象销毁hook：
            - 删除测试创建的字段
        """
        self.dst.fields.delete(self.field.id)


if __name__ == '__main__':
    unittest.main()
