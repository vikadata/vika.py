from typing import List

from apitable.const import MAX_WRITE_RECORDS_PRE_REQ
from apitable.datasheet.record import Record
from apitable.exceptions import RecordDoesNotExist
from apitable.types import RawRecord
from apitable.utils import chunks, trans_key


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
        Split the current QuerySet into multiple QuerySets with a maximum number of records of 10
        @return: iter[QuerySet] iteratively returns a sub-QuerySet with a maximum number of records of 10
        """
        for chunk in chunks(self._records, MAX_WRITE_RECORDS_PRE_REQ):
            yield QuerySet(self._dst, chunk)

    def last(self):
        """
        Get the last record
        @return: Record
        """
        return Record(self._dst, self._records[-1])

    def first(self):
        """
        Get the first record
        @return: Record
        """
        return Record(self._dst, self._records[0])

    def delete(self, delete_all=False) -> bool:
        """
        delete Delete all records in the current record set in batches, delete in batches of 10 records. If the number of recordsets is greater than 10, an error will be reported
        @return:
        """
        if not delete_all and self.count() > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception('You cannot operate more than 10 records in batches, please use the chunks method to operate in batches.')
        return self._dst.delete_records([rec.id for rec in self._records])

    def clone(self):
        """
        Returns a cloned copy of the current recordset
        @return: QuerySet
        """
        return QuerySet(self._dst, self._records[:])

    def update(self, **kwargs) -> bool:
        """
        dst.records.filter(title=None).update(status="Pending")
        """
        if self.count() > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception('You cannot operate more than 10 records in batches, please use the chunks method to operate in batches')
        patch_update_records_data = []
        for record in iter(self._records):
            data = {"recordId": record.id, "fields": kwargs}
            patch_update_records_data.append(data)
        self._records = self._dst.update_records(patch_update_records_data)
        return True

    def count(self):
        """
        Returns the total number of records in the current recordset
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
