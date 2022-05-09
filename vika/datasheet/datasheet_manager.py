from vika.types.response import PostDatasheetMetaResponseData


class DatasheetManager:
    """

    """
    def __init__(self, spc: 'Space'):
        self.spc = spc

    def create(self, data) -> PostDatasheetMetaResponseData:
        """ 字段创建  https://vika.cn/developers/api/reference/#operation/create-datasheets

            :param dict data:  新建表格属性
            :return: 新建表格id、创建时间戳和字段id、name信息
            :raises ServerError: 服务端错误
            :raises ResponseBodyParserError: 解析响应体失败
            :raises Exception: 其他异常

            :example:
            >>> vika = Vika('YOUR_API_TOKEN')
            >>> req_data = {'name': 'table_name'}
             >>> dst_meta = vika.space('YOUR_SPACE_ID').datasheets.create(req_data)
        """
        resp = self.spc.create_datasheet(data)
        return resp.data
