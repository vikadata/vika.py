from typing import Optional, List, Dict, Any
from apitable.types.field import MetaField
from apitable.utils import trans_key


class FieldManager:

    def __init__(self, dst: 'Datasheet'):
        self.dst = dst
        self._is_fetched = False

        # All acquired fields information is cached once acquired
        self._fields = []
        # Supplementary data
        self._meta_field_id_map = {}
        self._meta_field_name_map = {}

    def refresh(self):
        """
        Refresh the field meta cache, the default cache is 5 minutes, and can be refreshed manually.
        """
        self._is_fetched = False

    def _check_meta(self, **kwargs):
        if not self._is_fetched:
            fields_resp = self.dst.get_fields(**kwargs)
            self._set_meta_fields(fields_resp.data.items)
            self._is_fetched = True

    def _set_meta_fields(self, fields: List[MetaField]):
        self._fields = fields
        for field in fields:
            self._meta_field_id_map[field.id] = field
            self._meta_field_name_map[field.name] = field

    def __contains__(self, item):
        """
        Is field_key in dst.fields
        @param item: field_key
        @return: bool
        """
        self._check_meta()
        if isinstance(item, MetaField):
            return item in self._fields
        field_key = trans_key(self.dst.field_key_map, item)
        return field_key in self._meta_field_id_map or field_key in self._meta_field_name_map

    def all(self, **kwargs) -> List[MetaField]:
        """
        Get all the field information of the current datasheet
        @param kwargs:
            - viewId: 'viewId' Get the field information of the specified view, the hidden fields under the view will not be returned.
        @return:
        """
        # Get the field information of the specified view, one-time without caching. Can it actually be cached?
        if kwargs:
            fields_resp_via_view_id = self.dst.get_fields(**kwargs)
            return fields_resp_via_view_id.data.items
        self._check_meta()
        return self._fields

    def get(self, field_key: str, **kwargs) -> Optional[MetaField]:
        """
        Obtained by field_key, the fields in the Apitable cannot have the same name, id and name are both unique identifiers
        dst.fields.get('fldxxxxxxxx')
        dst.fields.get('title')
        @param field_key
        @param kwargs:
        @return: MetaField
        """
        field_key = trans_key(self.dst.field_key_map, field_key)
        # If you haven't obtained meta, first request meta
        self._check_meta()
        # Get the meta and return the field directly
        if self.dst.field_key == "id":
            return self._meta_field_id_map.get(field_key, None)
        if self.dst.field_key == "name":
            return self._meta_field_name_map.get(field_key, None)
        # Field not found
        return None

    def create(self, data) -> Optional[MetaField]:
        """ Field creation https://developers.apitable.com/api/reference/#operation/create-fields

            :param dict data:  New field property
            :return: New field id and name
            :raises ServerError
            :raises ResponseBodyParserError: Failed to parse response body
            :raises Exception: Other error, such as: field duplicate name

            :example:
            >>> apitable = Apitable('YOUR_API_TOKEN')
            >>> req_data = {'type': 'SingleText', 'name': 'title', 'property': {'defaultValue': 'hello apitable'}}
            >>> fld_meta = apitable.space('YOUR_SPACE_ID').datasheet('YOUR_TABLE').fields.create(req_data)
        """
        resp = self.dst.create_field(data)
        self.refresh()
        return resp.data

    def delete(self, fid_id: str) -> bool:
        """ Field deletion https://developers.apitable.com/api/reference/#operation/delete-fields

            :param str fid_id: Field information to delete
            :return: Delete successfully returns true
            :raises ServerError
            :raises ResponseBodyParserError: Failed to parse response body
            :raises Exception: Other error, such as: field id does not exist

            :example:
            >>> apitable = Apitable('YOUR_API_TOKEN')
            >>> is_true = apitable.space('YOUR_SPACE_ID').datasheet('YOUR_TABLE').fields.delete('fid_id')
            >>> is_true
            True
        """
        is_success = self.dst.delete_field(fid_id)
        self.refresh()
        return is_success

    def __getitem__(self, index):
        self._check_meta()
        return self._fields[index]
