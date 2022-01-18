from typing import Optional, List
from vika.types.field import MetaField
from vika.utils import trans_key


class FieldManager:

    def __init__(self, dst: 'Datasheet'):
        self.dst = dst
        self._is_fetched = False

        # 获取的 fields 信息全部的获取一次就缓存起来
        self._fields = []
        # 辅助数据
        self._meta_field_id_map = {}
        self._meta_field_name_map = {}

    def refresh(self):
        """
        刷新字段 meta 缓存，默认缓存 5 分钟，可以手动刷新。
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
        field_key 是否在 dst.fields 中
        @param item: field_key，字段名
        @return: bool
        """
        self._check_meta()
        if isinstance(item, MetaField):
            return item in self._fields
        field_key = trans_key(self.dst.field_key_map, item)
        return field_key in self._meta_field_id_map or field_key in self._meta_field_name_map

    def all(self, **kwargs) -> List[MetaField]:
        """
        获取当前维格表的全部字段信息
        @param kwargs:
            - viewId: 'viewId' 获取指定视图的字段信息，视图下隐藏的字段不会返回。
        @return:
        """
        # 获取指定视图的字段信息，一次性的不缓存。其实也可以缓存下来？
        if kwargs:
            fields_resp_via_view_id = self.dst.get_fields(**kwargs)
            return fields_resp_via_view_id.data.items
        self._check_meta()
        return self._fields

    def get(self, field_key: str, **kwargs) -> Optional[MetaField]:
        """
        通过 field_key 获取, 维格表内字段不能重名， id 和 name 都是唯一标识
        dst.fields.get('fldxxxxxxxx')
        dst.fields.get('title')
        @param field_key: 字段标识
        @param kwargs:
        @return: MetaField
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
        self._check_meta()
        return self._fields[index]
