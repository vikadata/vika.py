from typing import Dict, Any, List, Optional

from vika.types.node import NodeListItem, NodeDetail
from vika.types.space import SpaceListItem
from vika.types.record import RawRecord
from vika.types.view import MetaView
from vika.types.field import MetaField
from pydantic import BaseModel


class ResponseBase(BaseModel):
    """
    REST API 返回的统一响应体格式
    """
    code: int
    success: bool
    message: str
    data: Optional[Any]


Records = List[RawRecord]


class RecordsData(BaseModel):
    records: Records


class GETResponseBase(BaseModel):
    total: int
    pageNum: int
    pageSize: int


class GETRecordResponseData(GETResponseBase, RecordsData):
    pass


class GETRecordResponse(ResponseBase):
    """
    获取记录返回结果
    """
    data: GETRecordResponseData


class PatchRecordResponse(ResponseBase):
    """
    更新记录返回结果
    """
    data: RecordsData


class PostRecordResponse(ResponseBase):
    """
    创建记录返回结果
    """
    data: RecordsData


class DeleteRecordResponse(ResponseBase):
    """
    删除记录返回结果
    """
    pass


class UploadFileResponse(ResponseBase):
    """
    上传文件返回结果
    """
    data: Dict[str, Any]


# meta field
class GETMetaFieldResponseData(BaseModel):
    items: List[MetaField]

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1250
        fields = {
            "items": "fields",  # 服务端返回的数据为 fields，此字段为 pydantic 保留字段。
        }


class GETMetaFieldResponse(ResponseBase):
    """
    获取 meta field 返回数据
    """
    data: GETMetaFieldResponseData


# meta view
class GETMetaViewResponseData(BaseModel):
    views: List[MetaView]


class GETMetaViewResponse(ResponseBase):
    """
    获取 meta view 返回数据
    """
    data: GETMetaViewResponseData


# space
class GETSpaceListResponseData(BaseModel):
    spaces: List[SpaceListItem]


class GETSpaceListResponse(ResponseBase):
    """
    获取「空间站列表」返回的数据
    """
    data: GETSpaceListResponseData


# node
class GETNodeListResponseData(BaseModel):
    nodes: List[NodeListItem]


class GETNodeListResponse(ResponseBase):
    """
    获取「文件列表」返回的数据
    """
    data: GETNodeListResponseData


class GETNodeDetailResponse(ResponseBase):
    """
    获取「文件详情」返回的数据
    """
    data: NodeDetail
