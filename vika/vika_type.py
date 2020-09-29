from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class RawResponse(BaseModel):
    """
    REST API 返回的统一相应体格式
    """

    code: int
    success: bool
    message: str
    data: Optional[Any]


class RawRecord(BaseModel):
    """
    REST API 返回的 record 原始类型
    """

    id: str
    data: Dict[str, Any]

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1250
        fields = {
            "data": "fields",  # 服务端返回的数据为 fields，此字段为 pydantic 保留字段。
            "id": "recordId",  # 服务端返回的数据为 recordId，这里映射成 id
        }


# class RawUploadFile(BaseModel):
#     id: str,
#     name: str,
#     size: int,
#     mimeType: str,
#     token: str,
#     width: int,
#     height: int,
#     url: str


class RawRecords(BaseModel):
    records: List[RawRecord]


class RawGETResponseBase(BaseModel):
    total: int
    pageNum: int
    pageSize: int


class RawGETResponseData(RawGETResponseBase, RawRecords):
    pass


class RawGETResponse(RawResponse):
    data: RawGETResponseData


class RawPatchResponse(RawResponse):
    data: RawRecords


class RawPostResponse(RawResponse):
    data: RawRecords


class RawDeleteResponse(RawResponse):
    pass


class RawUploadFileResponse(RawResponse):
    """
    一次只能上传一个文件，返回一个文件对象。
    """

    data: Dict[str, Any]
