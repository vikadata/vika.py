class DatasheetDoesNotExist(Exception):
    """
    数表不存在
    """
    pass


class RecordDoesNotExist(Exception):
    """
    记录不存在
    """
    pass


class FieldDoesNotExist(Exception):
    """
    字段不存在
    """

    pass


class RecordWasDeleted(Exception):
    """
    主动删除记录后，再访问此记录的属性会报错
    """

    pass


class ErrorFieldKey(Exception):
    """
    错误的 fieldKey
    """

    pass


class ErrorSortParams(Exception):
    """
    错误的排序规则
    """
    pass


class UploadFileError(Exception):
    """
    上传附件失败
    """
    pass


class JSONDecodeError(Exception):
    """
    JSON 解析错误
    """
    pass


class ResponseBodyParserError(Exception):
    """
    解析响应体失败
    """
    pass


class ServerError(Exception):
    """
    服务器错误
    """
    pass
