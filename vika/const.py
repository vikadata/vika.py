API_BASE = "https://vika.cn"

API_ENDPOINT_DATASHEET = "/fusion/v1/datasheets"

MAX_WRITE_RECORDS_PRE_REQ = 10

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
