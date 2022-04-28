from vika.node import NodeManager
from vika.utils import get_dst_id, handle_response
from vika.datasheet import Datasheet, DatasheetManager
from vika.types.response import PostDatasheetMetaResponse
from urllib.parse import urljoin


class Space:
    def __init__(self, vika: 'Vika', space_id: str):
        self.vika = vika
        self.id = space_id

    @property
    def nodes(self):
        return NodeManager(self.vika, space_id=self.id)

    @property
    def datasheets(self):
        return DatasheetManager(self)

    def datasheet(self, dst_id_or_url, **kwargs):
        """
        指定维格表资源
        @param dst_id_or_url: 维格表 ID 或者 维格表 URL
        @param kwargs:
            - field_key: 'id' or 'name' 按字段ID或字段名处理 records
            - field_key_map: 字段映射字典。参见：https://github.com/vikadata/vika.py#%E5%AD%97%E6%AE%B5%E6%98%A0%E5%B0%84
        @return:
        """
        dst_id = get_dst_id(dst_id_or_url)
        return Datasheet(self.vika, dst_id, spc_id=self.id, **kwargs)

    def create_datasheet(self, data) -> PostDatasheetMetaResponse:
        """ 表格创建

            :param dic data: api请求体，结构：{'name': 'table_name'}
            :return: 创建表格响应数据
            :raises ServerError: 服务端错误
            :raises ResponseBodyParserError: 解析响应体失败
            :raises Exception: 其他异常
        """
        if self.id is None:
            raise Exception('maybe: vika.datasheet("dst_id") => vika.space("spc_id").datasheet("dst_id")')
        api_endpoint = urljoin(self.vika.api_base,
                               f"/fusion/v1/spaces/{self.id}/datasheets")
        resp = self.vika.request.post(api_endpoint, json=data)
        return handle_response(resp, PostDatasheetMetaResponse)
