from typing import Optional
from .types.field import MetaField
from .utils import trans_key


class FieldManager:
    def __init__(self, dst: 'Datasheet'):
        self.dst = dst
        self._is_fetched = False

    def _check_meta(self):
        if not self._is_fetched:
            fields = self.dst.get_fields()
            self.dst.client_set_meta_fields(fields)
            self._is_fetched = True

    def get(self, field_key: str) -> Optional[MetaField]:
        """
        按字段名称或者id 获取字段。
        """
        field_key = trans_key(self.dst.field_key_map, field_key)
        # 没获取过 meta 先请求 meta
        self._check_meta()
        # 获取过 meta 直接返回字段
        if self.dst.field_key == "id":
            return self.dst.meta_field_id_map.get(field_key, None)
        if self.dst.field_key == "name":
            return self.dst.meta_field_name_map.get(field_key, None)
        # 找不到字段
        return None

    def __getitem__(self, index):
        return self.dst.meta_fields[index]
