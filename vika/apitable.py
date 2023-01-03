import requests

from .const import API_BASE
from .datasheet import Datasheet
from .node import NodeManager
from .space import Space, SpaceManager
from .utils import get_dst_id


class Vika:
    def __init__(self, token: str, **kwargs):
        """
        @param token: API Token, User's developer token
        @param kwargs:
            - api_base: api url，default is "https://vika.cn"
        """
        self.request = requests.session()
        self._auth(token)
        self._api_base = kwargs.get('api_base', API_BASE)

    def _auth(self, token):
        self.request.headers.update({"Authorization": f"Bearer {token}"})

    @property
    def api_base(self):
        """
        Current API base address, distinguishing between environments
        """
        return self._api_base

    def set_api_base(self, api_base):
        """
        set api_base
        @param api_base:
        @return:
        """
        self._api_base = api_base

    def space(self, space_id: str):
        """
        Specify space
        @param space_id
        @return: Space
        """
        return Space(self, space_id)

    @property
    def spaces(self):
        """
        Space Resource Management
        @return: SpaceManager
        """
        return SpaceManager(self)

    @property
    def nodes(self):
        """
        Node Resource Management
        @return: NodeManager
        """
        return NodeManager(self)

    def datasheet(self, dst_id_or_url, **kwargs):
        """
        Specifying a Datasheet in Apitable
        @param dst_id_or_url: Datasheet ID or URL
        @param kwargs:
            - field_key: 'id' or 'name'
            - field_key_map: Field mapping. More info: https://github.com/apitable/apitable-sdks/tree/develop/apitable.py#Field-mapping
        @return:
        """
        dst_id = get_dst_id(dst_id_or_url)
        return Datasheet(self, dst_id, records=[], **kwargs)
