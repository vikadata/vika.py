from urllib.parse import urljoin, urlparse

import requests

from .const import API_BASE, API_GET_DATASHEET_QS_SET, DEFAULT_PAGE_SIZE
from .datasheet import Datasheet
from .vika_type import RawGETResponse


class Vika:
    def __init__(self, token, **kwargs):
        self.request = requests.Session()
        self.auth(token)
        self._api_base = API_BASE

    @property
    def api_base(self):
        return self._api_base

    def set_api_base(self, api_base):
        self._api_base = api_base

    def set_request(self, config):
        # TODO  配置 request 请求（timeout）
        pass

    def auth(self, token):
        self.request.headers.update({"Authorization": f"Bearer {token}"})

    def datasheet(self, dst_id_or_url, **kwargs):
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

    def fetch_datasheet(self, dst_id, **kwargs):
        # kwargs.update(fieldKey=self.field_key)
        page_size = kwargs.get("pageSize", DEFAULT_PAGE_SIZE)
        page_num = kwargs.get("pageNum", 1)
        current_total = page_size * page_num
        params = {"pageSize": page_size}
        for key in kwargs:
            if key in API_GET_DATASHEET_QS_SET:
                params.update({key: kwargs.get(key)})
        resp = self.request.get(
            urljoin(self.api_base, f"/fusion/v1/datasheets/{dst_id}/records"),
            params=params,
        ).json()
        resp = RawGETResponse(**resp)
        records = []
        if resp.success:
            records += resp.data.records
            if current_total < resp.data.total:
                kwargs.update({"pageNum": page_num + 1})
                records += self.fetch_datasheet(dst_id, **kwargs)
        else:
            print(f"[{dst_id}] get page:{page_num} fail\n {resp.message}")
        return records
