class DatasheetDoesNotExist(Exception):
    """"""

    pass


class RecordDoesNotExist(Exception):
    """
    查询的即记录不存在
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
