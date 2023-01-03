from urllib.parse import urljoin

from apitable.types.response import (
    GETSpaceListResponse
)
from apitable.utils import handle_response


class SpaceManager:
    def __init__(self, apitable: 'Apitable', **kwargs):
        self.apitable = apitable

    @property
    def _api_endpoint(self):
        return urljoin(self.apitable.api_base, f"/fusion/v1/spaces")

    def _get_spaces(self) -> GETSpaceListResponse:
        """
        Get field meta
        """
        resp = self.apitable.request.get(self._api_endpoint)
        return handle_response(resp, GETSpaceListResponse)

    def all(self):
        """
        Get the current user's space list
        @return: List[SpaceListItem]
        """
        spaces_resp = self._get_spaces()
        return spaces_resp.data.spaces

    def get(self, space_id: str):
        """
        Get the specified space information
        @param space_id
        @return:
        """
        pass
