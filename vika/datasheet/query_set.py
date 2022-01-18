from typing import List

from vika.const import MAX_WRITE_RECORDS_PRE_REQ
from vika.datasheet.record import Record
from vika.exceptions import RecordDoesNotExist
from vika.types import RawRecord
from vika.utils import chunks, trans_key


class QuerySet:

    def __init__(self, dst, records: List[RawRecord]):
        self._dst = dst
        self._records = records[:]

    def __len__(self):
        return len(self._records)

    def __iter__(self):
        for record in iter(self._records):
            record = Record(self._dst, record)
            yield record

    def __str__(self):
        return f"(QuerySet: {self.count()} records)"

    __repr__ = __str__

    def __getitem__(self, index):
        return Record(self._dst, self._records[index])

    def chunks(self):
        """
        将当前 QuerySet 拆分成多个最大记录数为 10 的 QuerySet
        @return: iter[QuerySet] 迭代返回最大记录数为 10 的子 QuerySet
        """
        for chunk in chunks(self._records, MAX_WRITE_RECORDS_PRE_REQ):
            yield QuerySet(self._dst, chunk)

    def last(self):
        """
        获取最后一条记录
        @return: Record
        """
        return Record(self._dst, self._records[-1])

    def first(self):
        """
        获取第一条记录
        @return: Record
        """
        return Record(self._dst, self._records[0])

    def delete(self, delete_all=False) -> bool:
        """
        delete 批量删除当前记录集的所有记录，按 10 条一批次删除。记录集数量大于 10 条则报错
        @return:
        """
        if not delete_all and self.count() > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception('不能批量操作大于 10 条记录，请使用 chunks 方法，分批操作。')
        return self._dst.delete_records([rec.id for rec in self._records])

    def clone(self):
        """
        返回当前记录集的克隆副本
        @return: QuerySet
        """
        return QuerySet(self._dst, self._records[:])

    def update(self, **kwargs) -> bool:
        """
        dst.records.filter(title=None).update(status="Pending")
        """
        if self.count() > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception('不能批量操作大于 10 条记录，请使用 chunks 方法，分批操作')
        patch_update_records_data = []
        for record in iter(self._records):
            data = {"recordId": record.id, "fields": kwargs}
            patch_update_records_data.append(data)
        self._records = self._dst.update_records(patch_update_records_data)
        return True

    def count(self):
        """
        返回当前记录集的总记录数量
        @return: int
        """
        return len(self)

    def get(self, **kwargs):
        if kwargs:
            return self.filter(**kwargs).first()
        if self._records:
            return Record(self._dst, self._records[0])
        raise RecordDoesNotExist()

    def filter(self, *args, **kwargs):
        """
        songs = dst_songs.filter(artist="faye wong")
        songs = dst_songs.filter('{artist}="faye wong" OR {artist}="someone"')
        for song in songs:
            print(song.title)
        """
        if args and kwargs:
            #
            print()
        # if filter_func_or_key:
        #     # 如果是函数
        #     if isinstance(filter_func_or_key, FunctionType):
        #         if kwargs:
        #             raise Exception("function filter can't be used with key-value filter")
        kwargs = {
            trans_key(self._dst.field_key_map, k): v
            for k, v in kwargs.items()
        }

        def filter_record(record) -> bool:
            return all([
                record.id == v
                if k in ["recordId", "_id"] else record.data.get(k) == v
                for k, v in kwargs.items()
            ])

        found_records = list(filter(filter_record, self._records))
        return QuerySet(self._dst, found_records)
