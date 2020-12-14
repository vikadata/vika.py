import time

from .const import MAX_COUNT_CREATE_RECORDS_ONCE, QPS
from .record import Record
from .utils import chunks
from .exceptions import RecordDoesNotExist


class QuerySet:
    def __init__(self, dst, records):
        self._dst = dst
        self._records = records

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        for record in iter(self._records):
            record = Record(self._dst, record)
            yield record

    def __getitem__(self, index):
        return Record(self._dst, self._records[index])

    def last(self):
        return Record(self._dst, self._records[-1])

    def first(self):
        return Record(self._dst, self._records[0])

    def delete(self) -> bool:
        is_del_success = self._dst.delete_records([rec._id for rec in self])
        if is_del_success:
            self._dst.remove_records(self._records)
        return is_del_success

    def _clone(self):
        return QuerySet(self._dst, self._records)

    def update(self, **kwargs) -> int:
        """
        dst.records.filter(title=None).update(status="Pending")
        """
        patch_update_records_data = []
        for record in iter(self._records):
            data = {"recordId": record.id, "fields": kwargs}
            patch_update_records_data.append(data)
        if patch_update_records_data:
            update_success_count = self._dst.update_records(patch_update_records_data)
            return update_success_count
        return 0

    def count(self):
        return len(self)

    def get(self, **kwargs):
        if kwargs.keys():
            return self.filter(**kwargs).get()
        if self._records:
            return Record(self._dst, self._records[0])

        raise RecordDoesNotExist()

    def all(self):
        return QuerySet(self._dst, self._dst._records)

    def filter(self, **kwargs):
        """
        songs = dst_songs.filter(artist="faye wong")
        for song in songs:
            print(song.title)
        """
        kwargs = {self._dst.trans_key(k): v for k, v in kwargs.items()}

        def filter_record(record) -> bool:
            return all(
                [
                    record.id == v
                    if k in ["recordId", "_id"]
                    else record.data.get(k) == v
                    for k, v in kwargs.items()
                ]
            )

        found_records = list(filter(filter_record, self._records))
        return QuerySet(self._dst, found_records)


class RecordManager:
    def __init__(self, dst):
        self._dst = dst
        self._fetched_with = None
        self._fetched_by = None

    def check_data(self, **kwargs):
        if not self._dst._has_fetched_data or (
            self._fetched_by == "all" and kwargs != self._fetched_with
        ):
            _fieldKey = kwargs.get("fieldKey")
            if _fieldKey and _fieldKey != self._dst.field_key:
                # TODO: logger warning
                print(
                    f'It seems that you set field_key when you init datasheet, all(filedKey="{_fieldKey}") wont work'
                )
            kwargs.update(fieldKey=self._dst.field_key)
            records = self._dst.vika.fetch_datasheet(self._dst.id, **kwargs)
            self._dst.set_records(records)
            self._dst.has_fetched_data = True
            self._fetched_with = kwargs

    def bulk_create(self, data):
        records = []
        for chunk in chunks(data, MAX_COUNT_CREATE_RECORDS_ONCE):
            resp = self._dst.create_records(chunk)
            if resp.success:
                records += resp.data.records
                time.sleep(1 / QPS)
        self._dst.append_records(records)
        if len(data) != len(records):
            print(f"Warning: {len(data)-len(records)} records create fail")
        return [Record(self._dst, record) for record in records]

    def create(self, data):
        resp = self._dst.create_records(data)
        if resp.success:
            records = resp.data.records
            self._dst.append_records(records)
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
        self.check_data()
        return QuerySet(self._dst, self._dst.raw_records).get(**kwargs)

    def filter(self, **kwargs):
        """
        songs = dst_songs.records.filter(artist="faye wong")
        for song in songs:
            print(song.title)
        """
        self._fetched_by = "filter"
        self.check_data()
        return QuerySet(self._dst, self._dst.raw_records).filter(**kwargs)
