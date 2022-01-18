from functools import lru_cache, wraps
from json import JSONDecodeError
from time import monotonic
from typing import Any, Dict, Generic, TypeVar
from urllib.parse import urlparse

from vika.exceptions import ResponseBodyParserError, ServerError

T = TypeVar('T')

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
        # 处理空值
        if v is None:
            v = 'BLANK()'
        # 处理字符串
        if isinstance(v, str):
            v = f'"{v}"'
        if isinstance(v, bool):
            v = 'TRUE()' if v else 'FALSE()'
        # 处理数组类型的值，多选，成员？
        if isinstance(v, list):
            v = f'"{", ".join(v)}"'
        query_str += f'{{{trans_key(field_key_map, k)}}}={v}'
    return query_str


def handle_response(resp, resp_class: Generic[T]) -> T:
    if resp.status_code >= 500:
        raise ServerError(f"API Server Error: {resp.status_code}")
    try:
        r = resp.json()
        if r["success"]:
            try:
                return resp_class(**r)
            except:
                raise ResponseBodyParserError(f"Response Body Parser Error: {resp.text}")
        raise Exception(r['message'])
    except JSONDecodeError:
        raise Exception(f"JSON Parser Error: {resp.text}")


def check_sort_params(sort):
    if not isinstance(sort, list):
        return False
    return all([('field' in i and 'order' in i) for i in sort])


def get_dst_id(dst_id_or_url: str):
    if dst_id_or_url.startswith("dst"):
        return dst_id_or_url
    elif dst_id_or_url.startswith("http"):
        url = urlparse(dst_id_or_url)
        url_path_list = url.path.split("/")
        dst_id = url_path_list[-2]
        return dst_id
    else:
        raise Exception('Bad Datasheet Id or URL')


def timed_lru_cache(
    _func=None, *, seconds: int = 600, maxsize: int = 128, typed: bool = False
):
    """Extension of functools lru_cache with a timeout
    https://gist.github.com/Morreski/c1d08a3afa4040815eafd3891e16b945#gistcomment-3521580
    Parameters:
    seconds (int): Timeout in seconds to clear the WHOLE cache, default = 10 minutes
    maxsize (int): Maximum Size of the Cache
    typed (bool): Same value of different type will be a different entry

    """

    def wrapper_cache(f):
        f = lru_cache(maxsize=maxsize, typed=typed)(f)
        f.delta = seconds
        f.expiration = monotonic() + f.delta

        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if monotonic() >= f.expiration:
                f.cache_clear()
                f.expiration = monotonic() + f.delta
            return f(*args, **kwargs)

        wrapped_f.cache_info = f.cache_info
        wrapped_f.cache_clear = f.cache_clear
        return wrapped_f

    # To allow decorator to be used without arguments
    if _func is None:
        return wrapper_cache
    else:
        return wrapper_cache(_func)
