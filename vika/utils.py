from typing import Dict, Any

FieldKeyMap = Dict[str, str]


def chunks(_list, chunk_size):
    for i in range(0, len(_list), chunk_size):
        yield _list[i: i + chunk_size]


def trans_key(field_key_map: FieldKeyMap, key: str):
    """
    存在字段映射时，将映射的 key 转为实际的 key
    """
    if key in ["_id", "recordId"]:
        return key
    if field_key_map:
        _key = field_key_map.get(key, key)
        return _key
    return key


def trans_data(field_key_map: FieldKeyMap, data: Dict[str, Any]):
    """
    配置字段映射关系后，将传入的 record 数据转化为 API 理解的数据
    """
    if field_key_map:
        _data = {}
        for k, v in data.items():
            _k = field_key_map.get(k, k)
            _data[_k] = v
        return _data
    return data


def query_parse(field_key_map: FieldKeyMap, **kwargs):
    """
    将查询条件转化为 filterByFormula
    records.filter(title="hello", subtitle="world") => '{title}="hello" AND {subtitle}="world"'
    1. 通过 filter 和 get 参数查询到的只能转化为 and 条件。
    """
    query_str = ""
    for k, v in kwargs.items():
        if query_str:
            query_str += " AND "
        query_str += f"{{{trans_key(field_key_map, k)}}}={v}"
    return query_str
