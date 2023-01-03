class DatasheetDoesNotExist(Exception):
    """
    Datasheet does not exist
    """
    pass


class RecordDoesNotExist(Exception):
    """
    Record does not exist
    """
    pass


class FieldDoesNotExist(Exception):
    """
    Field does not exist
    """

    pass


class RecordWasDeleted(Exception):
    """
    After the record is deleted, an error will be reported when accessing the properties of this record again.
    """

    pass


class ErrorFieldKey(Exception):
    """
    Wrong fieldKey
    """

    pass


class ErrorSortParams(Exception):
    """
    Wrong sorting rules
    """
    pass


class UploadFileError(Exception):
    """
    Failed to upload attachment
    """
    pass


class JSONDecodeError(Exception):
    """
    JSON parsing error
    """
    pass


class ResponseBodyParserError(Exception):
    """
    Failed to analyze the response body
    """
    pass


class ServerError(Exception):
    """
    Server error
    """
    pass
