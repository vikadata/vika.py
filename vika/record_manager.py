import time

from .const import MAX_COUNT_CREATE_RECORDS_ONCE, QPS
from .query_set import QuerySet
from .record import Record
from .utils import chunks, query_parse


class RecordManager:
    def __init__(self, dst: 'Datasheet'):
        self._dst = dst
        self._fetched_with = None
        self._fetched_by = None

    def check_data(self, **kwargs):
        """
        records.<不同查询方法> 链式调用的首次调用会查询数据。
        根据查询方法的不同，使用不同的应对策略，减小请求数量
        """
        # 客户端没有获取到表格完整数据前，独立查询的数据都会覆盖客户端数据集合。
        if self._fetched_by in ["get", "filter"] and not self._dst.has_fetched_all_data:
            # 将查询条件转化为 filterByFormula
            query_formula = query_parse(self._dst.field_key_map, **kwargs)
            kwargs = {"filterByFormula": query_formula}
            records = self._dst.vika.fetch_datasheet_all(self._dst.id, **kwargs)
            self._dst.client_set_records(records)
            self._dst.has_fetched_data = True
            self._fetched_with = kwargs
            return records

        if not self._dst.has_fetched_data or (
                self._fetched_by == "all" and kwargs != self._fetched_with
        ):
            _fieldKey = kwargs.get("fieldKey")
            if _fieldKey and _fieldKey != self._dst.field_key:
                # TODO: logger warning
                print(
                    f'It seems that you set field_key when init datasheet, all(filedKey="{_fieldKey}") wont work'
                )
            kwargs.update(fieldKey=self._dst.field_key)
            if 'pageSize' in kwargs or 'pageNum' in kwargs:
                resp = self._dst.vika.fetch_datasheet(self._dst.id, **kwargs)
                if resp.success:
                    records = resp.data.records
                else:
                    print(resp.data)
                    print(f"[{self._dst.id}] fetch data fail\n {resp.message}")
                    records = []
            else:
                records = self._dst.vika.fetch_datasheet_all(self._dst.id, **kwargs)
            self._dst.client_set_records(records)
            self._dst.has_fetched_data = True
            self._fetched_with = kwargs

    def bulk_create(self, data):
        """
        批量创建记录，每个请求只能创建 10 条记录
        """
        records = []
        for chunk in chunks(data, MAX_COUNT_CREATE_RECORDS_ONCE):
            resp = self._dst.create_records(chunk)
            if resp.success:
                records += resp.data.records
                time.sleep(1 / QPS)
        self._dst.client_append_records(records)
        if len(data) != len(records):
            print(f"Warning: {len(data) - len(records)} records create fail")
        return [Record(self._dst, record) for record in records]

    def create(self, data):
        """
        创建一条记录
        """
        resp = self._dst.create_records(data)
        if resp.success:
            records = resp.data.records
            self._dst.client_append_records(records)
            return Record(self._dst, records[0])
        return None

    def count(self):
        self.check_data()
        return QuerySet(self._dst, self._dst.raw_records).count()

    def all(self, **kwargs):
        """
        链式调用中，只有第一个 all 方法可以定制返回数据。
        * （选填）视图ID。默认为维格表中第一个视图。请求会返回视图中经过视图中筛选/排序后的结果，可以搭配使用fields参数过滤不需要的字段数据
        viewId: 'viewId1',
        * （选填）对指定维格表的记录进行排序。由多个“排序对象”组成的数组。支持顺序：'asc' 和 逆序：'desc'。注：此参数指定的排序条件将会覆盖视图里的排序条件。
        sort: [{ '列名称或者 ID': 'asc' }],
        * （选填）recordIds 数组。如果附带此参数，则返回参数中指定的records数组。 返回值按照传入数组的顺序排序。此时无视筛选、排序。无分页，每次最多查询 1000 条
        recordIds: ['recordId1', 'recordId2'],
        * （选填）指定要返回的字段（默认为字段名, 也可以通过 fieldKey 指定为字段 Id）。如果附带此参数，则返回的记录合集将会被过滤，只有指定的字段会返回。
        fields: ['标题', '详情', '引用次数'],
        * （选填）使用公式作为筛选条件，返回匹配的记录，访问 https://vika.cn/help/tutorial-getting-started-with-formulas/ 了解公式使用方式
        filterByFormula: '{引用次数} >  0',
        * （选填）限制返回记录的总数量。如果该值小于表中实际的记录总数，则返回的记录总数会被限制为该值。
        maxRecords: 5000,
        * （选填）单元格值类型，默认为 'json'，指定为 'string' 时所有值都将被自动转换为 string 格式。
        cellFormat: 'json',
        * （选填）指定 field 的查询和返回的 key。默认使用列名  'name' 。指定为 'id' 时将以 fieldId 作为查询和返回方式（使用 id 可以避免列名的修改导致代码失效问题）
        fieldKey: 'name',
        """
        self._fetched_by = "all"
        self.check_data(**kwargs)
        return QuerySet(self._dst, self._dst.raw_records)

    def get(self, **kwargs):
        """
        book = dst_books.records.get(ISBN="9787506341271")
        print(book.title)
        """
        self._fetched_by = "get"
        raw_records = self.check_data(**kwargs)
        return QuerySet(self._dst, raw_records).get(**kwargs)

    def filter(self, **kwargs):
        """
        songs = dst_songs.records.filter(artist="faye wong")
        for song in songs:
            print(song.title)
        """
        # 直接通过 filter 调用时候，将 filter 查询参数转化为
        self._fetched_by = "filter"
        raw_records = self.check_data(**kwargs)
        return QuerySet(self._dst, raw_records).filter(**kwargs)
