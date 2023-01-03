from apitable.node import NodeManager
from apitable.utils import get_dst_id, handle_response
from apitable.datasheet import Datasheet, DatasheetManager
from apitable.types.response import PostDatasheetMetaResponse
from urllib.parse import urljoin


class Space:
    def __init__(self, apitable: 'Apitable', space_id: str):
        self.apitable = apitable
        self.id = space_id

    @property
    def nodes(self):
        return NodeManager(self.apitable, space_id=self.id)

    @property
    def datasheets(self):
        return DatasheetManager(self)

    def datasheet(self, dst_id_or_url, **kwargs):
        """
        @param dst_id_or_url: Datasheet ID or URL
        @param kwargs:
            - field_key: 'id' or 'name' 
            - field_key_map: Field Mapping Dictionary. More info: https://github.com/apitable/apitable-sdks/tree/develop/apitable.py#Field-mapping
        @return:
        """
        dst_id = get_dst_id(dst_id_or_url)
        return Datasheet(self.apitable, dst_id, spc_id=self.id, **kwargs)

    def create_datasheet(self, data) -> PostDatasheetMetaResponse:
        """ 
            :param dic data: API request body, structure: {'name': 'table_name'}
            :return: Create form response data
            :raises ServerError:
            :raises ResponseBodyParserError: Failed to parse response body
            :raises Exception: Other error
        """
        if self.id is None:
            raise Exception('maybe: apitable.datasheet("dst_id") => apitable.space("spc_id").datasheet("dst_id")')
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/spaces/{self.id}/datasheets")
        resp = self.apitable.request.post(api_endpoint, json=data)
        return handle_response(resp, PostDatasheetMetaResponse)
