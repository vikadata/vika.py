from apitable.types.response import PostDatasheetMetaResponseData


class DatasheetManager:
    """

    """
    def __init__(self, spc: 'Space'):
        self.spc = spc

    def create(self, data) -> PostDatasheetMetaResponseData:
        """ Create Field  https://developers.apitable.com/api/reference/#operation/create-datasheets

            :param dict data: 
            :return: datasheet id, Creation timestamp, field id and field name
            :raises ServerError
            :raises ResponseBodyParserError: Failed to parse response body
            :raises Exception: Other error

            :example:
            >>> apitable = Apitable('YOUR_API_TOKEN')
            >>> req_data = {'name': 'table_name'}
             >>> dst_meta = apitable.space('YOUR_SPACE_ID').datasheets.create(req_data)
        """
        resp = self.spc.create_datasheet(data)
        return resp.data
