from typing import List

from apitable.const import MAX_GET_RECORDS_PRE_REQ, MAX_WRITE_RECORDS_PRE_REQ
from apitable.datasheet.query_set import QuerySet
from apitable.datasheet.record import Record
from apitable.exceptions import RecordDoesNotExist
from apitable.types import GETRecordResponse
from apitable.utils import query_parse, trans_data


class RecordManager:

    def __init__(self, dst: 'Datasheet'):
        self._dst = dst
        self._fetched_with = None
        self._fetched_by = None

    def bulk_create(self, data) -> List[Record]:
        """
        Create records in batches, only 10 records can be created per request dst.records.bulk_create([{"title": "hello apitable"}])
        @param data: list of record objects [{ "fieldKey": fieldValue }, { "fieldKey": fieldValue2 }]
        @return: List[Record]
        """
        if len(data) > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception(f'The number of records created by a single request cannot be greater than {MAX_WRITE_RECORDS_PRE_REQ}')
        resp = self._dst.create_records(data)
        return [Record(self._dst, record) for record in resp.data.records]

    def bulk_update(self, data) -> List[Record]:
        """
        Batch update records, same as raw API request
        @param data: record object list [{ "recordId": "recxxxx", "fields": {"fieldKey": fieldValue} }]
        @return Boolean
        """
        if len(data) > MAX_WRITE_RECORDS_PRE_REQ:
            raise Exception(f'The number of records to be updated in a single request cannot be greater than {MAX_WRITE_RECORDS_PRE_REQ}')
        for record in data:
            record['fields'] = trans_data(self._dst.field_key_map,
                                          record['fields'])
        updated_records = self._dst.update_records(data)
        return [Record(self._dst, record) for record in updated_records]

    def create(self, data) -> Record:
        """
        Create a record dst.records.create({"title": "hello apitable"})
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
        Filter records by query conditions, see get records query params https://developers.apitable.com/api-reference#operation/get-records
        @param kwargs:
            - viewId: 'viewId1',View ID. Defaults to the first view in the Apitable. The request will return the filtered/sorted results in the view, and you can use the fields parameter to filter unwanted field data
            - sort: [{ 'Field name or ID': 'asc' }] sorts the records of the specified dimensional grid. An array of multiple "sort objects". Support order: 'asc' and reverse order: 'desc'. Note: The sorting conditions specified by this parameter will override the sorting conditions in the view.
            - recordIds: ['recordId1', 'recordId2'], array of recordIds. If this parameter is included, the records array specified in the parameter is returned. The returned values are sorted in the order passed in the array. Filtering and sorting are ignored at this time. No paging, at most 1000 items per query
            - fields: ['title', 'detail', 'Citations'], specify the field to be returned (the default is the field name, or it can be specified as the field Id through fieldKey). If this parameter is included, the returned record collection will be filtered, and only the specified fields will be returned.
            - filterByFormula: '{Citations} >  0', use formulas as filter conditions to return matching records, visit https://help.apitable.com/docs/guide/tutorial-getting-started-with-formulas to learn how to use formulas
            - maxRecords: 5000, limits the total number of records returned. If this value is less than the actual total number of records in the table, the total number of records returned is limited to this value.
            - cellFormat: 'json', cell value type, the default is 'json', when specified as 'string', all values will be automatically converted to string format.
            - fieldKey: 'name', specifies the field's query and returned key. The column name 'name' is used by default. When specified as 'id', fieldId will be used as the query and return method (using id can avoid the problem of code failure caused by modification of column names)
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
        Query a single record that meets the conditions, suitable for querying using a uniquely identified field
        1. Specify record id to query records
        dst_books.records.get("recxxxxxx")
        2. Query records by condition
        dst_books.records.get(ISBN="9787506341271")
        @param args:
        @param kwargs:
        @return:
        """
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
        Find a single record by the given kwargs criteria, and create a record if no matching record exists.
        eg: dst.records.get_or_create(defaults={"done":False}, task="Find apitable") If a record with "task" as "Find apitable" is not found, create one with "done" of "False"
        @param defaults Dictionary (field key, field value), when the record does not exist, create the default value of the record.
        @param kwargs Query conditions
        @return (record,created) Returns the record and whether it was created
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
        Find a single record by the given kwargs criteria, and create a record if no matching record exists. If found, update the record with the value in defaults.
        @param defaults Dictionary (field key, field value), when the record does not exist, create the default value of the record.
        @param kwargs Query conditions
        @return (record,created) Returns the record and whether it was created
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
        Through the query conditions, query the recordsets that meet the conditions
        songs = dst_songs.records.filter(artist="faye wong")
        for song in songs:
            print(song.title)
        @param kwargs:
        @return: QuerySet
        """
        # When calling directly through filter, convert the filter query parameter into filterByFormula, and use the server to calculate the result
        records = self._query_records(**kwargs)
        return QuerySet(self._dst, records)

    def _query_records(self, **kwargs):
        # Convert the query conditions into filterByFormula, and use the server to calculate the query record set
        query_formula = query_parse(self._dst.field_key_map, **kwargs)
        kwargs = {
            "filterByFormula": query_formula,
            "pageSize": MAX_GET_RECORDS_PRE_REQ
        }
        return self._dst.get_records_all(**kwargs)
