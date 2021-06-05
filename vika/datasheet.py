import io
import mimetypes
from typing import List
from urllib.parse import urljoin

import requests

from .exceptions import RecordDoesNotExist
from .field_manager import FieldManager
from .record import Record
from .record_manager import RecordManager
from .types.response import (
    GETMetaFieldResponse,
    PatchRecordResponse,
    PostRecordResponse,
    DeleteRecordResponse,
    UploadFileResponse,
    RawRecord,
    Records,
    MetaField,
    GETMetaViewResponse,
)
from .utils import FieldKeyMap
from .view_manager import ViewManager


class Datasheet:
    def __init__(self, vika: 'Vika', dst_id: str, records: Records, **kwargs):
        self.vika = vika
        self.id = dst_id
        self.client_set_records(records)
        self.has_fetched_data = False
        self.has_fetched_all_data = False
        field_key = kwargs.get("field_key", "name")
        if field_key not in ["name", "id"]:
            raise Exception("Error field_key, plz use「name」 or 「id」")
        self.field_key = field_key
        field_key_map = kwargs.get("field_key_map", None)
        self.field_key_map: FieldKeyMap = field_key_map
        # 本地存储数据
        self.meta_fields = []
        self.meta_field_id_map = {}
        self.meta_field_name_map = {}
        self._record_ids = []
        self._records_map = {}

    # client_x 管理客户端 datasheet 数据
    def client_append_records(self, records):
        for record in records:
            self._record_ids.append(record.id)
            self._records_map[record.id] = record.data

    def client_remove_records(self, records):
        for record in records:
            if record.id in self._record_ids:
                self._record_ids.remove(record.id)
                del self._records_map[record.id]

    def client_set_meta_fields(self, fields: List[MetaField]):
        self.meta_fields = fields
        self.meta_field_id_map = {}
        self.meta_field_name_map = {}
        for field in fields:
            self.meta_field_id_map[field.id] = field
            self.meta_field_id_map[field.name] = field

    def client_set_records(self, records):
        _record_ids = []
        _records_map = {}
        for record in records:
            _record_ids.append(record.id)
            _records_map[record.id] = record.data
        self._record_ids = _record_ids
        self._records_map = _records_map

    def get_record_by_id(self, _record_id: str):
        if _record_id in self._records_map:
            return RawRecord(
                **{"recordId": _record_id, "fields": self._records_map[_record_id]}
            )
        else:
            return RecordDoesNotExist()

    def client_update_record_data_via_id(self, record_id, data) -> bool:
        try:
            record_data = self._records_map.get(record_id)
            record_data.update(data)
            return True
        except Exception:
            return False

    def client_update_records(self, records: Records) -> int:
        success_count = 0
        for record in records:
            r = self.client_update_record_data_via_id(record.id, record.data)
            if r:
                success_count += 1
        return success_count

    def refresh(self):
        """
        TODO refetch datasheet
        """
        pass

    @property
    def record_api_endpoint(self):
        return urljoin(self.vika.api_base, f"/fusion/v1/datasheets/{self.id}/records")

    @property
    def raw_records(self):
        return [
            RawRecord(
                **{
                    "recordId": record_id,
                    "fields": self._records_map.get(record_id, {}),
                }
            )
            for record_id in self._record_ids
        ]

    @property
    def fields(self):
        return FieldManager(self)

    @property
    def views(self):
        return ViewManager(self)

    @property
    def records(self):
        return RecordManager(self)

    def field_check(self, field):
        """
        TODO wait for meta
        """
        pass

    def trans_key(self, key):
        """
        存在字段映射时，将映射的 key 转为实际的 key
        """
        field_key_map = self.field_key_map
        if key in ["_id", "recordId"]:
            return key
        if field_key_map:
            _key = field_key_map.get(key, key)
            return _key
        return key

    def trans_data(self, data):
        field_key_map = self.field_key_map
        if field_key_map:
            _data = {}
            for k, v in data.items():
                _k = field_key_map.get(k, k)
                _data[_k] = v
            return _data
        return data

    # 下面是数表管理的请求
    # 字段相关
    def get_fields(self):
        """
        获取 field meta
        """
        api_endpoint = urljoin(
            self.vika.api_base, f"/fusion/v1/datasheets/{self.id}/fields"
        )
        r = self.vika.request.get(api_endpoint).json()
        r = GETMetaFieldResponse(**r)
        if r.success:
            return r.data.fields
        raise Exception(r.message)

    def get_views(self):
        """
        获取 view meta
        """
        api_endpoint = urljoin(
            self.vika.api_base, f"/fusion/v1/datasheets/{self.id}/views"
        )
        r = self.vika.request.get(api_endpoint).json()
        r = GETMetaViewResponse(**r)
        if r.success:
            return r.data.views
        raise Exception(r.message)

    # 记录相关请求
    def create_records(self, data) -> PostRecordResponse:
        """
        添加记录
        """
        if type(data) is list:
            data = {
                "records": [{"fields": self.trans_data(item)} for item in data],
                "fieldKey": self.field_key,
            }
        else:
            data = {
                "records": [{"fields": self.trans_data(data)}],
                "fieldKey": self.field_key,
            }
        r = self.vika.request.post(self.record_api_endpoint, json=data).json()
        if r["success"]:
            r = PostRecordResponse(**r)
            return r
        else:
            raise Exception(r["message"])

    def delete_records(self, rec_list) -> bool:
        """
        删除记录
        """
        api_endpoint = urljoin(
            self.vika.api_base, f"/fusion/v1/datasheets/{self.id}/records"
        )
        if type(rec_list) is list:
            ids = [rec._id if type(rec) is Record else rec for rec in rec_list]
        else:
            rec = rec_list
            ids = rec._id if type(rec) is Record else rec
        r = self.vika.request.delete(api_endpoint, params={"recordIds": ids}).json()
        r = DeleteRecordResponse(**r)
        return r.success

    def update_records(self, data) -> int:
        """
        更新记录
        """
        if type(data) is list:
            data = {"records": data, "fieldKey": self.field_key}
        else:
            data = {"records": [data], "fieldKey": self.field_key}
        r = self.vika.request.patch(self.record_api_endpoint, json=data).json()
        if r["success"]:
            r = PatchRecordResponse(**r)
            return self.client_update_records(r.data.records)
        else:
            raise Exception(r["message"])

    # 附件
    def upload_file(self, file_url):
        """
        dst.upload_file("")
        """
        api_endpoint = urljoin(
            self.vika.api_base, f"/fusion/v1/datasheets/{self.id}/attachments"
        )

        is_web_file = type(file_url) is str and file_url.startswith("http")

        if is_web_file:
            r = requests.get(file_url)
            file_mimetype = r.headers["content-type"]
            with io.BytesIO() as buf:
                buf.write(r.content)
                buf.seek(0)
                _file = ("image", io.BufferedReader(buf), file_mimetype)
                r = self.vika.request.post(
                    api_endpoint,
                    files={"files": _file},
                    stream=False,
                ).json()
                r = UploadFileResponse(**r)
                if r.success:
                    return r.data
        else:
            with open(file_url, "rb") as upload_file:
                r = self.vika.request.post(
                    api_endpoint,
                    files={
                        "files": (
                            file_url,
                            upload_file,
                            mimetypes.guess_type(file_url)[0],
                        )
                    },
                ).json()
                r = UploadFileResponse(**r)
                if r.success:
                    return r.data
