import time
from typing import List

from .const import MAX_COUNT_CREATE_RECORDS_ONCE, QPS
from .exceptions import RecordDoesNotExist
from .record import Record
from .types import RawRecord
from .utils import chunks


class QuerySet:
    def __init__(self, dst, records: List[RawRecord], filter_by_formula=None):
        self._dst = dst
        self._records = records
        # qs 组装成的查询语句，使用服务端计算，减少请求。
        self.filter_by_formula = filter_by_formula

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

    def last(self):
        return Record(self._dst, self._records[-1])

    def first(self):
        return Record(self._dst, self._records[0])

    def delete(self) -> bool:
        del_res = []
        all_count = len(self._records)
        failed_records = []
        for chunk in chunks(self._records, MAX_COUNT_CREATE_RECORDS_ONCE):
            try:
                is_del_success = self._dst.delete_records([rec.id for rec in chunk])
                if is_del_success:
                    self._dst.client_remove_records(chunk)
                    del_res.append(is_del_success)
                else:
                    failed_records += chunk
                    del_res.append(is_del_success)
                time.sleep(1 / QPS)
            except Exception as e:
                print(e)
        res = all(del_res)
        if not res:
            print(
                f"WARNING: part of records delete failed, all: {all_count}, success:{all_count - len(failed_records)},"
                f" failed: {len(failed_records)}")
        return res

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
        this_batch_records_len = len(patch_update_records_data)
        has_failed = False
        if patch_update_records_data:
            update_success_count = 0
            for chunk in chunks(patch_update_records_data, MAX_COUNT_CREATE_RECORDS_ONCE):
                try:
                    update_success_count += self._dst.update_records(chunk)
                    time.sleep(1 / QPS)
                except Exception as e:
                    print(e)
                    has_failed = True
            if has_failed:
                failed_count = this_batch_records_len - update_success_count
                print(f"{failed_count} records update failed")
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
        return QuerySet(self._dst, self._dst.raw_records)

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
