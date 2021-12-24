from urllib.parse import urljoin

from vika.types.response import (
    GETNodeListResponse,
    GETNodeDetailResponse
)
from vika.utils import handle_response


class NodeManager:
    def __init__(self, vika: 'Vika', **kwargs):
        self.vika = vika
        self.space_id = kwargs.get('space_id', None)

    def _get_nodes(self, space_id: str) -> GETNodeListResponse:
        """
        获取 field meta
        """
        node_list_resp = self.vika.request.get(
            urljoin(self.vika.api_base, f"/fusion/v1/spaces/{space_id}/nodes")
        )
        return handle_response(node_list_resp, GETNodeListResponse)

    def _get_node_detail(self, node_id: str) -> GETNodeDetailResponse:
        node_detail_resp = self.vika.request.get(
            urljoin(self.vika.api_base, f"/fusion/v1/nodes/{node_id}")
        )
        return handle_response(node_detail_resp, GETNodeDetailResponse)

    def all(self, **kwargs):
        """
        vika.nodes.all(spaceId='spcxxxxxx') 获取指定空间站的根目录文件列表
        """
        space_id = kwargs.get('spaceId', self.space_id)
        nodes_resp = self._get_nodes(space_id)
        return nodes_resp.data.nodes

    def get(self, node_id: str):
        return self._get_node_detail(node_id).data
