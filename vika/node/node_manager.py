from urllib.parse import urljoin

from vika.types.response import (
    GETNodeListResponse,
    GETNodeDetailResponse,
    GETSearchNodeListResponse
)
from vika.utils import handle_response


class NodeManager:
    def __init__(self, apitable: 'Apitable', **kwargs):
        self.apitable = apitable
        self.space_id = kwargs.get('space_id', None)

    def _get_nodes(self, space_id: str) -> GETNodeListResponse:
        """
        Get field meta
        """
        node_list_resp = self.apitable.request.get(
            urljoin(self.apitable.api_base, f"/fusion/v1/spaces/{space_id}/nodes")
        )
        return handle_response(node_list_resp, GETNodeListResponse)

    def _get_node_detail(self, node_id: str) -> GETNodeDetailResponse:
        node_detail_resp = self.apitable.request.get(
            urljoin(self.apitable.api_base, f"/fusion/v1/nodes/{node_id}")
        )
        return handle_response(node_detail_resp, GETNodeDetailResponse)

    def _search_nodes(self, space_id: str, **kwargs) -> GETSearchNodeListResponse:
        search_node_list_resp = self.apitable.request.get(
            urljoin(self.apitable.api_base, f"/fusion/v2/spaces/{space_id}/nodes"),
            params=kwargs
        )
        return handle_response(search_node_list_resp, GETSearchNodeListResponse)
    
    def search(self, **kwargs):
        space_id = kwargs.get('spaceId', self.space_id)
        nodes_resp = self._search_nodes(space_id, **kwargs)
        return nodes_resp.data.nodes

    def all(self, **kwargs):
        """
        apitable.nodes.all(spaceId='spcxxxxxx') Get the list of files in the root of the specified space
        """
        space_id = kwargs.get('spaceId', self.space_id)
        nodes_resp = self._get_nodes(space_id)
        return nodes_resp.data.nodes

    def get(self, node_id: str):
        return self._get_node_detail(node_id).data
