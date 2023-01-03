import io
import json
import mimetypes
from typing import List
from urllib.parse import urljoin

import requests

from apitable.const import API_GET_DATASHEET_QS_SET, DEFAULT_PAGE_SIZE
from apitable.exceptions import ErrorSortParams
from apitable.datasheet.field_manager import FieldManager
from apitable.datasheet.record import Record
from apitable.datasheet.record_manager import RecordManager
from apitable.types import EmbedLinkCreateRo
from apitable.types.response import (
    GETMetaFieldResponse,
    PostMetaFieldResponse,
    PatchRecordResponse,
    PostRecordResponse,
    DeleteRecordResponse,
    UploadFileResponse,
    RawRecord,
    GETMetaViewResponse,
    GETRecordResponse,
    DeleteFieldResponse,
    PostEmbedLinkResponse,
    GetEmbedLinkResponse,
    PostEmbedLinkResponseData,
    GetEmbedLinkResponseData,
    DeleteEmbedLinkResponse,
)
from apitable.utils import FieldKeyMap, handle_response, check_sort_params, trans_data, timed_lru_cache
from apitable.datasheet.view_manager import ViewManager


class Datasheet:

    def __init__(self, apitable: 'Apitable', dst_id: str, spc_id=None, **kwargs):
        self.apitable = apitable
        self.id = dst_id
        self.spc_id = spc_id
        field_key = kwargs.get("field_key", "name")
        if field_key not in ["name", "id"]:
            raise Exception("Error field_key, plz use「name」 or 「id」")
        self.field_key = field_key
        field_key_map = kwargs.get("field_key_map", None)
        self.field_key_map: FieldKeyMap = field_key_map

    def refresh(self):
        """
        TODO refetch datasheet
        """
        pass

    @property
    def _record_api_endpoint(self):
        return urljoin(self.apitable.api_base,
                       f"/fusion/v1/datasheets/{self.id}/records")

    @property
    @timed_lru_cache(seconds=300)
    def fields(self):
        return FieldManager(self)

    @property
    def primary_field(self):
        return self.fields.all()[0]

    @property
    def views(self):
        return ViewManager(self)

    @property
    def records(self):
        return RecordManager(self)

    # The following is a request for datasheet management
    # Field
    def get_fields(self, **kwargs):
        """
        Get field meta
        @param kwargs:
            - viewId: 'viewId'
        @return:
        """
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/datasheets/{self.id}/fields")
        resp = self.apitable.request.get(api_endpoint, params=kwargs)
        return handle_response(resp, GETMetaFieldResponse)

    def create_field(self, data) -> PostMetaFieldResponse:
        """ 
            :param dic data: {'type': str, 'name': str, 'property': obj}
            :return: Field creation api returns result
            :raises ServerError
            :raises ResponseBodyParserError: Failed to parse response body
            :raises Exception: Other error, such as: field duplicate name
        """
        if self.spc_id is None:
            raise Exception('maybe: apitable.datasheet("dst_id") => apitable.space("spc_id").datasheet("dst_id")')
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/spaces/{self.spc_id}/datasheets/{self.id}/fields")
        resp = self.apitable.request.post(api_endpoint, json=data)
        return handle_response(resp, PostMetaFieldResponse)

    def delete_field(self, field_id: str) -> bool:
        """ 
            :param str field_id
            :return: Whether the field was deleted successfully
            :raises ServerError
            :raises ResponseBodyParserError: Failed to parse response body
            :raises Exception: Other error
        """
        if self.spc_id is None:
            raise Exception('maybe: apitable.datasheet("dst_id") => apitable.space("spc_id").datasheet("dst_id")')
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/spaces/{self.spc_id}/datasheets/{self.id}/fields/{field_id}")
        resp = self.apitable.request.delete(api_endpoint)
        r = handle_response(resp, DeleteFieldResponse)
        return r.success

    # View
    def get_views(self):
        """
        Get view meta
        """
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/datasheets/{self.id}/views")
        r = self.apitable.request.get(api_endpoint).json()
        r = GETMetaViewResponse(**r)
        if r.success:
            return r.data.views
        raise Exception(r.message)

    # Record
    def get_records(self, **kwargs):
        """
        Paginate to get data
        """
        params = {}
        for key in kwargs:
            if key in API_GET_DATASHEET_QS_SET:
                params_value = kwargs.get(key)
                if key == 'sort':
                    if check_sort_params(params_value):
                        params_value = [json.dumps(i) for i in params_value]
                    else:
                        raise ErrorSortParams('The format of the sort parameter is incorrect')
                params.update({key: params_value})
        resp = self.apitable.request.get(self._record_api_endpoint, params=params)
        return handle_response(resp, GETRecordResponse)

    def get_records_all(self, **kwargs) -> List[RawRecord]:
        """
        When pageSize and pageNum are not actively passed in, all records will be loaded.
        """
        page_size = kwargs.get("pageSize", DEFAULT_PAGE_SIZE)
        page_num = kwargs.get("pageNum", 1)
        page_params = {"pageSize": page_size, "pageNum": page_num}
        kwargs.update(page_params)
        records = []
        resp = self.get_records(**kwargs)
        if resp.success:
            records += resp.data.records
            current_total = page_size * page_num
            if current_total < resp.data.total:
                kwargs.update({"pageNum": page_num + 1})
                records += self.get_records_all(**kwargs)
        else:
            print(f"[{self.id}] get page:{page_num} fail\n {resp.message}")
        return records

    def create_records(self, data) -> PostRecordResponse:
        if type(data) is list:
            data = {
                "records": [{
                    "fields": trans_data(self.field_key_map, item)
                } for item in data],
                "fieldKey":
                    self.field_key,
            }
        else:
            data = {
                "records": [{
                    "fields": trans_data(self.field_key_map, data)
                }],
                "fieldKey": self.field_key,
            }
        resp = self.apitable.request.post(self._record_api_endpoint, json=data)
        return handle_response(resp, PostRecordResponse)

    def delete_records(self, rec_list) -> bool:
        api_endpoint = self._record_api_endpoint
        if type(rec_list) is list:
            ids = [rec._id if type(rec) is Record else rec for rec in rec_list]
        else:
            rec = rec_list
            ids = rec._id if type(rec) is Record else rec
        resp = self.apitable.request.delete(api_endpoint,
                                            params={"recordIds": ids})
        r = handle_response(resp, DeleteRecordResponse)
        return r.success

    def update_records(self, data) -> List[RawRecord]:
        if type(data) is list:
            data = {"records": data, "fieldKey": self.field_key}
        else:
            data = {"records": [data], "fieldKey": self.field_key}
        r = self.apitable.request.patch(self._record_api_endpoint,
                                        json=data).json()
        if r["success"]:
            r = PatchRecordResponse(**r)
            return r.data.records
        else:
            raise Exception(r["message"])

    def upload_attachment(self, file_url):
        """
        Upload attachments, support local or url.
        attachment = dst.upload_attachment("/path/to/your/file")
        record.attachment = [attachment]
        """
        return self.upload_file(file_url)

    def upload_file(self, file_url):
        """
        @deprecated
        pload attachments, support local or url.(Please use upload_attachment instead, this method may be deprecated)
        dst.upload_file("/path/to/your/file")
        """
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/datasheets/{self.id}/attachments")
        is_web_file = type(file_url) is str and file_url.startswith("http")

        if is_web_file:
            r = requests.get(file_url)
            file_mimetype = r.headers["content-type"]
            with io.BytesIO() as buf:
                buf.write(r.content)
                buf.seek(0)
                _file = ("image", io.BufferedReader(buf), file_mimetype)
                r = self.apitable.request.post(
                    api_endpoint,
                    files={"files": _file},
                    stream=False,
                )
        else:
            with open(file_url, "rb") as upload_file:
                r = self.apitable.request.post(
                    api_endpoint,
                    files={
                        "files": (
                            file_url,
                            upload_file,
                            mimetypes.guess_type(file_url)[0],
                        )
                    },
                )
        up_file_resp = handle_response(r, UploadFileResponse)
        if up_file_resp.success:
            return up_file_resp.data

    def create_embed_link(self, data: EmbedLinkCreateRo = None) -> PostEmbedLinkResponseData:
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/spaces/{self.spc_id}/nodes/{self.id}/embedlinks")
        resp = self.apitable.request.post(api_endpoint, json=data)
        return handle_response(resp, PostEmbedLinkResponse).data

    def get_embed_links(self) -> List[GetEmbedLinkResponseData]:
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/spaces/{self.spc_id}/nodes/{self.id}/embedlinks")
        resp = self.apitable.request.get(api_endpoint)
        return handle_response(resp, GetEmbedLinkResponse).data

    def delete_embed_link(self, link_id: str) -> bool:
        api_endpoint = urljoin(self.apitable.api_base,
                               f"/fusion/v1/spaces/{self.spc_id}/nodes/{self.id}/embedlinks/{link_id}")
        resp = self.apitable.request.delete(api_endpoint)
        r = handle_response(resp, DeleteEmbedLinkResponse)
        return r.success
