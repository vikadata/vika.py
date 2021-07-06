from urllib.parse import urlparse

from .const import API_BASE
from .datasheet import Datasheet
import requests


class Vika:
    def __init__(self, token, **kwargs):
        self.request = requests.session()
        self._auth(token)
        self._api_base = API_BASE

    @property
    def api_base(self):
        """
        当前 API 基础地址，区分环境
        """
        return self._api_base

    def set_api_base(self, api_base):
        self._api_base = api_base

    def set_request(self, config):
        # TODO  配置 request 请求（timeout）
        pass

    def _auth(self, token):
        self.request.headers.update({"Authorization": f"Bearer {token}"})

    def datasheet(self, dst_id_or_url, **kwargs):
        """
        实例化数表
        """
        if dst_id_or_url.startswith("dst"):
            dst_id = dst_id_or_url
        elif dst_id_or_url.startswith("http"):
            url = urlparse(dst_id_or_url)
            url_path_list = url.path.split("/")
            dst_id = url_path_list[-2]
            view_id = url_path_list[-1]
            if view_id and view_id.startswith("viw"):
                kwargs.update({"viewId": view_id})
        else:
            raise Exception("Bad URL")
        return Datasheet(self, dst_id, records=[], **kwargs)

    @staticmethod
    def check_sort_params(sort):
        if not isinstance(sort, list):
            return False
        return all([('field' in i and 'order' in i) for i in sort])
