from typing import Optional, List
from .types.field import MetaField
from .utils import trans_key


class FieldManager:
    def __init__(self, dst: 'Datasheet'):
        self.dst = dst
        self._is_fetched = False

    def _check_meta(self, **kwargs):
        if not self._is_fetched:
            fields_resp = self.dst.get_fields(**kwargs)
            self._set_meta_fields(fields_resp.data.items)
            self._is_fetched = True

    def _set_meta_fields(self, fields: List[MetaField]):
        self._meta_fields = fields
        self._meta_field_id_map = {}
        self._meta_field_name_map = {}
        for field in fields:
            self._meta_field_id_map[field.id] = field
            self._meta_field_name_map[field.name] = field

    def __contains__(self, item):
        """
        field_key 是否在 dst.fields 中
        """
        self._check_meta()
        field_key = trans_key(self.dst.field_key_map, item)
        return field_key in self._meta_field_id_map or field_key in self._meta_field_name_map

    def all(self, **kwargs) -> List[Optional[MetaField]]:
        self._check_meta(**kwargs)
        return self._meta_fields

    def get(self, field_key: str) -> Optional[MetaField]:
        """
        按字段名称或者id 获取字段。
        """
        field_key = trans_key(self.dst.field_key_map, field_key)
        # 没获取过 meta 先请求 meta
        self._check_meta()
        # 获取过 meta 直接返回字段
        if self.dst.field_key == "id":
            return self._meta_field_id_map.get(field_key, None)
        if self.dst.field_key == "name":
            return self._meta_field_name_map.get(field_key, None)
        # 找不到字段
        return None

    def __getitem__(self, index):
        return self.dst.meta_fields[index]
