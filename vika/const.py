import os

try:
    MAX_WRITE_RECORDS_PRE_REQ = int(os.environ['APITABLE_MAX_WRITE_RECORDS_PRE_REQ'])
except KeyError:
    MAX_WRITE_RECORDS_PRE_REQ = 10

API_BASE = "https://vika.cn"

API_ENDPOINT_DATASHEET = "/fusion/v1/datasheets"

MAX_GET_RECORDS_PRE_REQ = 1000

API_GET_DATASHEET_QS_SET = {
    "viewId",
    "pageNum",
    "pageSize",
    "sort",
    "recordIds",
    "fields",
    "filterByFormula",
    "maxRecords",
    "cellFormat",
    "fieldKey",
}

DEFAULT_PAGE_SIZE = 1000

QPS = 5
