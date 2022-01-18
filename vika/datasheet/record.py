from vika.exceptions import RecordWasDeleted, ErrorFieldKey
from vika.types import RawRecord
from vika.utils import trans_key, trans_data


class Record:

    def __init__(self, datasheet: 'Datasheet', record: RawRecord):
        self._datasheet = datasheet
        self._id = record.id
        self._record = record
        self._is_del = False

    def _get_field(self, field_key: str):
        return self._datasheet.fields.get(field_key)

    def _check_record_status(self):
        if self._is_del:
            raise RecordWasDeleted()
        return None

    def __str__(self):
        return f"(Record: {self._id})"

    __repr__ = __str__

    def __getattr__(self, key):
        transformed_key = trans_key(self._datasheet.field_key_map, key)
        if not transformed_key:
            raise Exception(f"record has no field:[{key}]")
        # 数据里面能拿到，表示返回了
        if transformed_key in self._record.data:
            return self._record.data.get(transformed_key)
        # 数据里面拿不到，但存在这个字段。表示字段值为空
        if key in self._datasheet.fields:
            return None
        # 错误的字段
        raise ErrorFieldKey(f"'{key}' does not exist")

    def delete(self) -> bool:
        """
        删除此记录
        @return: bool 是否成功删除, 删除异常也会抛错
        """
        self._check_record_status()
        return self._datasheet.delete_records([self._id])

    def __setattr__(self, _key, value):
        if _key.startswith("_"):
            super().__setattr__(_key, value)
        elif _key in self._datasheet.fields:
            key = trans_key(self._datasheet.field_key_map, _key)
            data = {"recordId": self._id, "fields": {key: value}}
            updated_records = self._datasheet.update_records(data)
            if updated_records:
                self._record.data[key] = value
        else:
            raise ErrorFieldKey(f"'{_key}' does not exist")

    def json(self):
        self._check_record_status()
        # FIXME: 补全空值字段, 使用原始数据，还是使用映射的字段名做 key
        record_data = dict(self._record.data)
        return record_data

    def _make_update_body(self, data):
        _data = trans_data(self._datasheet.field_key_map, data)
        data = {"recordId": self._id, "fields": _data}
        return data

    def update(self, data=None, **kwargs):
        """
        更新多个字段，支持两种写法。可以传单个 dict，也可以传入 **kwargs
        @param data: dict 需要更新的键值对
        @param kwargs: 需要更新的键值对
        """
        self._check_record_status()
        update_data = {}
        if data:
            update_data.update(data)
        if kwargs:
            update_data.update(kwargs)
        # 更新单个记录的多个字段，只返回一条记录
        update_data = self._make_update_body(update_data)
        self._record = self._datasheet.update_records(update_data)[0]
        return self
