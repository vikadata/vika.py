import io
from urllib.parse import urljoin
import mimetypes
import requests

from .exceptions import RecordDoesNotExist, ErrorFieldKey
from .record import Record
from .record_manager import RecordManager
from .vika_type import (
    RawPatchResponse,
    RawPostResponse,
    RawDeleteResponse,
    RawUploadFileResponse,
    RawRecords,
    RawRecord,
)


class Datasheet:
    def __init__(self, vika, dst_id, records: RawRecords, **kwargs):
        self.vika = vika
        self.id = dst_id
        self._init_records(records)
        self._has_fetched_data = False
        field_key = kwargs.get("field_key", "name")
        if field_key not in ["name", "id"]:
            raise Exception("Error field_key, plz use「name」 or 「id」")
        self.field_key = field_key
        field_key_map = kwargs.get("field_key_map", None)
        self.field_key_map = field_key_map

    def _init_records(self, records: RawRecords):
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

    @property
    def _records(self):
        return self._make_records()

    def _make_records(self):
        return [
            RawRecord(
                **{
                    "recordId": record_id,
                    "fields": self._records_map.get(record_id, {}),
                }
            )
            for record_id in self._record_ids
        ]

    def set_records(self, records):
        self._init_records(records)

    def _update_record_data_via_id(self, record_id, data) -> bool:
        try:
            record_data = self._records_map.get(record_id)
            record_data.update(data)
            return True
        except Exception:
            return False

    def _update_records(self, records: RawRecords) -> int:
        success_count = 0
        for record in records:
            r = self._update_record_data_via_id(record.id, record.data)
            if r:
                success_count += 1
        return success_count

    def append_records(self, records):
        for record in records:
            self._record_ids.append(record.id)
            self._records_map[record.id] = record.data

    def remove_records(self, records):
        for record in records:
            if record.id in self._record_ids:
                self._record_ids.remove(record.id)
                del self._records_map[record.id]

    def refresh(self):
        """
        TODO refetch datasheet
        """
        pass

    @property
    def _api_endpoint(self):
        return urljoin(self.vika.api_base, f"/fusion/v1/datasheets/{self.id}/records")

    @property
    def raw_records(self):
        return self._records

    @property
    def records(self):
        return RecordManager(self)

    def update_records(self, data) -> int:
        """
        更新记录
        """
        if type(data) is list:
            data = {"records": data, "fieldKey": self.field_key}
        else:
            data = {"records": [data], "fieldKey": self.field_key}
        r = self.vika.request.patch(self._api_endpoint, json=data).json()
        if r["success"]:
            r = RawPatchResponse(**r)
            return self._update_records(r.data.records)
        else:
            raise Exception(r["message"])

    def field_check(self, field):
        """
        TODO wait for meta
        """
        pass

    def trans_key(self, key):
        field_key_map = self.field_key_map
        if key in ["_id", "recordId"]:
            return key
        if field_key_map:
            _key = field_key_map.get(key, None)
            return _key
        return key

    def trans_data(self, data):
        field_key_map = self.field_key_map
        if field_key_map:
            _data = {}
            for k, v in data.items():
                _k = field_key_map.get(k)
                if not _k:
                    return ErrorFieldKey()
                _data[_k] = v
            return _data
        return data

    def create_records(self, data) -> RawPostResponse:
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
        r = self.vika.request.post(self._api_endpoint, json=data).json()
        if r["success"]:
            r = RawPostResponse(**r)
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
        r = RawDeleteResponse(**r)
        return r.success

    def upload_file(self, file_url):
        """
        dst.upload_file("")
        """
        api_endpoint = api_endpoint = urljoin(
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
                r = RawUploadFileResponse(**r)
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
                r = RawUploadFileResponse(**r)
                if r.success:
                    return r.data
