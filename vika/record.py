from .exceptions import RecordWasDeleted


class Record:
    def __init__(self, datasheet, record: str):
        self._datasheet = datasheet
        self._id = record.id
        self._is_del = False

    @property
    def _record(self):
        return self._datasheet.get_record_by_id(self._id)

    def _check_record_status(self):
        if self._is_del:
            return RecordWasDeleted()

    def __str__(self):
        return f"{self._id}"

    def __getattr__(self, key):
        if key in self._record.data:
            return self._record.data.get(key)
        else:
            # FIXME 因为目前缺少  Meta， 这里返回 None。后续可以通过 meta 判断是否是合法的 key
            # return Exception(f"record has no field:[{key}]")
            return None

    def delete(self) -> bool:
        self._check_record_status()
        r = self._datasheet.delete_records([self._id])
        if r:
            self._datasheet.remove_records([self._record])
            self._is_del = True
        return r

    def _is_attachment_field(self, field_name):
        return field_name in self._datasheet.attachment_fields

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            if self._is_attachment_field(key) and type(value) is not dict:
                if type(value) is list:
                    value = [self._datasheet.upload_file(url) for url in value]
                if not value:
                    value = None
            data = {"recordId": self._id, "fields": {key: value}}
            r = self._datasheet.update_records(data)
            if r == 1:
                self._record.data[key] = value

    def json(self):
        self._check_record_status()
        return self._record.data

    def make_update_body(self, data):
        data = {"recordId": self._id, "fields": data}
        return data

    def update(self, data):
        """
        更新多个字段
        """
        self._check_record_status()
        # 更新单个记录的多个字段，只返回一条记录
        data = self.make_update_body(data)
        return self._datasheet.update_records(data)
