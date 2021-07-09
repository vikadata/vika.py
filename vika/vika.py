import requests

from .const import API_BASE
from .datasheet import Datasheet
from .node import NodeManager
from .space import Space, SpaceManager
from .utils import get_dst_id


class Vika:
    def __init__(self, token: str, **kwargs):
        """
        @param token: API Token, 用户的开发者令牌
        @param kwargs:
            - api_base: api 接口地址，默认是 "https://vika.cn"
        """
        self.request = requests.session()
        self._auth(token)
        self._api_base = kwargs.get('api_base', API_BASE)

    def _auth(self, token):
        self.request.headers.update({"Authorization": f"Bearer {token}"})

    @property
    def api_base(self):
        """
        当前 API 基础地址，区分环境
        """
        return self._api_base

    def set_api_base(self, api_base):
        """
        设置 api_base
        @param api_base:
        @return:
        """
        self._api_base = api_base

    def space(self, space_id: str):
        """
        指定空间站资源
        @param space_id: 空间站 id
        @return: Space
        """
        return Space(self, space_id)

    @property
    def spaces(self):
        """
        空间站资源管理
        @return: SpaceManager
        """
        return SpaceManager(self)

    @property
    def nodes(self):
        """
        文件节点资源管理
        @return: NodeManager
        """
        return NodeManager(self)

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
        return Datasheet(self, dst_id, records=[], **kwargs)
