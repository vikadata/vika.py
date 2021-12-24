from urllib.parse import urljoin

from vika.types.response import (
    GETSpaceListResponse
)
from vika.utils import handle_response


class SpaceManager:
    def __init__(self, vika: 'Vika', **kwargs):
        self.vika = vika

    @property
    def _api_endpoint(self):
        return urljoin(self.vika.api_base, f"/fusion/v1/spaces")

    def _get_spaces(self) -> GETSpaceListResponse:
        """
        获取 field meta
        """
        resp = self.vika.request.get(self._api_endpoint)
        return handle_response(resp, GETSpaceListResponse)

    def all(self):
        """
        获取当前用户的空间站列表
        @return: List[SpaceListItem]
        """
        spaces_resp = self._get_spaces()
        return spaces_resp.data.spaces

    def get(self, space_id: str):
        """
        获取指定空间站信息
        @param space_id: 空间站 ID
        @return:
        """
        pass
