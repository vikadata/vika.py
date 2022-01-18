from typing import List

from vika.const import MAX_GET_RECORDS_PRE_REQ, MAX_WRITE_RECORDS_PRE_REQ
from vika.datasheet.query_set import QuerySet
from vika.datasheet.record import Record
from vika.exceptions import RecordDoesNotExist
from vika.types import GETRecordResponse
from vika.utils import query_parse, trans_data


class RecordManager:

    def __init__(self, dst: 'Datasheet'):
        self._dst = dst
        self._fetched_with = None
        self._fetched_by = None

    def bulk_create(self, data) -> List[Record]:
        """
        批量创建记录，每个请求只能创建 10 条记录 dst.records.bulk_create([{"标题": "hello vika"}])
        @param data: 记录对象列表 [{ "fieldKey": fieldValue }, { "fieldKey": fieldValue2 }]
        @return: List[Record]
        """
        if len(data) > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception(f'单个请求创建记录数量不得大于 {MAX_WRITE_RECORDS_PRE_REQ} 条')
        resp = self._dst.create_records(data)
        return [Record(self._dst, record) for record in resp.data.records]

    def bulk_update(self, data) -> List[Record]:
        """
        批量更新记录，和原始的 API 请求一样
        @param data: 记录对象列表 [{ "recordId": "recxxxx", "fields": {"fieldKey": fieldValue} }]
        @return Boolean
        """
        if len(data) > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception(f'单个请求更新记录数量不得大于 {MAX_WRITE_RECORDS_PRE_REQ} 条')
        for record in data:
            record['fields'] = trans_data(self._dst.field_key_map,
                                          record['fields'])
        updated_records = self._dst.update_records(data)
        return [Record(self._dst, record) for record in updated_records]

    def create(self, data) -> Record:
        """
        创建一条记录 dst.records.create({"标题": "hello vika"})
        @param data: dict {"fieldKey": fieldValue}
        @return: Record
        """
        resp = self._dst.create_records(data)
        if resp.success:
            records = resp.data.records
            return Record(self._dst, records[0])
        raise Exception(resp.message)

    def all(self, **kwargs):
        """
        按查询条件过滤记录，参见获取记录 query params https://vika.cn/developers/api-reference#operation/get-records
        @param kwargs:
            - viewId: 'viewId1', 视图ID。默认为维格表中第一个视图。请求会返回视图中经过视图中筛选/排序后的结果，可以搭配使用fields参数过滤不需要的字段数据
            - sort: [{ '列名称或者 ID': 'asc' }] 对指定维格表的记录进行排序。由多个“排序对象”组成的数组。支持顺序：'asc' 和 逆序：'desc'。注：此参数指定的排序条件将会覆盖视图里的排序条件。
            - recordIds: ['recordId1', 'recordId2'],recordIds 数组。如果附带此参数，则返回参数中指定的records数组。 返回值按照传入数组的顺序排序。此时无视筛选、排序。无分页，每次最多查询 1000 条
            - fields: ['标题', '详情', '引用次数'], 指定要返回的字段（默认为字段名, 也可以通过 fieldKey 指定为字段 Id）。如果附带此参数，则返回的记录合集将会被过滤，只有指定的字段会返回。
            - filterByFormula: '{引用次数} >  0', 使用公式作为筛选条件，返回匹配的记录，访问 https://vika.cn/help/tutorial-getting-started-with-formulas/ 了解公式使用方式
            - maxRecords: 5000, 限制返回记录的总数量。如果该值小于表中实际的记录总数，则返回的记录总数会被限制为该值。
            - cellFormat: 'json', 单元格值类型，默认为 'json'，指定为 'string' 时所有值都将被自动转换为 string 格式。
            - fieldKey: 'name', 指定 field 的查询和返回的 key。默认使用列名  'name' 。指定为 'id' 时将以 fieldId 作为查询和返回方式（使用 id 可以避免列名的修改导致代码失效问题）
        @return:
        """
        _fieldKey = kwargs.get("fieldKey")
        if _fieldKey and _fieldKey != self._dst.field_key:
            # TODO: logger warning
            print(
                f'It seems that you set field_key when init datasheet, all(filedKey="{_fieldKey}") wont work'
            )
        kwargs.update(fieldKey=self._dst.field_key)
        if 'pageSize' in kwargs or 'pageNum' in kwargs:
            resp: GETRecordResponse = self._dst.get_records(**kwargs)
            if resp.success:
                records = resp.data.records
            else:
                print(f"[{self._dst.id}] fetch data fail\n {resp.message}")
                records = []
        else:
            records = self._dst.get_records_all(**kwargs)
        return QuerySet(self._dst, records)

    def get(self, *args, **kwargs):
        """
        查询出符合条件的单条记录，适合使用唯一标识的字段做查询
        1. 指定 record id 查询记录
        dst_books.records.get("recxxxxxx")
        2. 按条件查询记录
        dst_books.records.get(ISBN="9787506341271")
        @param args:
        @param kwargs:
        @return:
        """
        # 按 id 查找
        if args:
            record_id = args[0]
            kwargs = {"recordIds": [record_id]}
        elif kwargs:
            query_formula = query_parse(self._dst.field_key_map, **kwargs)
            kwargs = {"filterByFormula": query_formula}
        resp: GETRecordResponse = self._dst.get_records(**kwargs)
        if resp.data.records:
            return Record(self._dst, resp.data.records[0])
        raise RecordDoesNotExist()

    def get_or_create(self, defaults=None, **kwargs):
        """
        按给定的 kwargs 条件查找单条记录，如果没有符合的记录，则创建记录。
        eg: dst.records.get_or_create(defaults={"done":False}, task="今天早起") 如果找不到 「task 为「今天早起」的记录，则创建一条，且的「done」是「False」
        @param defaults 字典（字段key,字段值），当记录不存在时，创建记录的默认值。
        @param kwargs 查询条件
        @return (record,created) 返回记录和是否是创建
        """
        created = False
        record = None
        data = {}
        try:
            record = self.get(**kwargs)
        except RecordDoesNotExist:
            created = True
            if kwargs:
                data.update(kwargs)
            if defaults:
                data.update(defaults)
            record = self.create(data)
        return (record, created)

    def update_or_create(self, defaults=None, **kwargs):
        """
        按给定的 kwargs 条件查找单条记录，如果没有符合的记录，则创建记录。如果找到了，就以 defaults 中的值更记录。
        @param defaults 字典（字段key,字段值），当记录不存在时，创建记录的默认值。
        @param kwargs 查询条件
        @return (record,created) 返回记录和是否是创建
        """
        created = False
        record = None
        data = {}
        try:
            record = self.get(**kwargs).update(defaults)
        except RecordDoesNotExist:
            created = True
            if kwargs:
                data.update(kwargs)
            if defaults:
                data.update(defaults)
            record = self.create(data)
        return (record, created)

    def filter(self, **kwargs):
        """
        通过查询条件，查询出符合条件的记录集
        songs = dst_songs.records.filter(artist="faye wong")
        for song in songs:
            print(song.title)
        @param kwargs:
        @return: QuerySet
        """
        # 直接通过 filter 调用时候，将 filter 查询参数转化为 filterByFormula，使用服务端计算结果
        records = self._query_records(**kwargs)
        return QuerySet(self._dst, records)

    def _query_records(self, **kwargs):
        # 将查询条件转化为 filterByFormula， 利用服务端计算查询记录集
        query_formula = query_parse(self._dst.field_key_map, **kwargs)
        kwargs = {
            "filterByFormula": query_formula,
            "pageSize": MAX_GET_RECORDS_PRE_REQ
        }
        resp: GETRecordResponse = self._dst.get_records(**kwargs)
        if resp.data.pageNum * resp.data.pageSize < resp.data.total:
            return resp.data.records + self._dst.get_records(
                pageNum=resp.data.pageNum + 1, **kwargs)
        return resp.data.records
