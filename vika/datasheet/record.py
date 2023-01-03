from apitable.exceptions import RecordWasDeleted, ErrorFieldKey
from apitable.types import RawRecord
from apitable.utils import trans_key, trans_data


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
        # The data can be obtained, indicating that it has returned
        if transformed_key in self._record.data:
            return self._record.data.get(transformed_key)
        # I can't get it in the data, but this field exists. Indicates that the field value is empty
        if key in self._datasheet.fields:
            return None
        # Field does not exist
        raise ErrorFieldKey(f"'{key}' does not exist")

    def delete(self) -> bool:
        """
        @return: bool Whether the deletion is successful, the deletion exception will also throw an error
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
        # FIXME: Fill in the empty value field, use the original data, or use the mapped field name as the key
        record_data = dict(self._record.data)
        return record_data

    def _make_update_body(self, data):
        _data = trans_data(self._datasheet.field_key_map, data)
        data = {"recordId": self._id, "fields": _data}
        return data

    def update(self, data=None, **kwargs):
        """
       Update multiple fields, support two writing methods. You can pass a single dict, or you can pass in **kwargs
        @param data: dict The key-value pair that needs to be updated
        @param kwargs: The key-value pair that needs to be updated
        """
        self._check_record_status()
        update_data = {}
        if data:
            update_data.update(data)
        if kwargs:
            update_data.update(kwargs)
        # Update multiple fields of a single record, returning only one record
        update_data = self._make_update_body(update_data)
        self._record = self._datasheet.update_records(update_data)[0]
        return self
