from typing import Dict, Any, List, Optional

from apitable.types.embedlink import EmbedLinkThemeEnum, EmbedLinkPayload
from apitable.types.node import NodeListItem, NodeDetail
from apitable.types.space import SpaceListItem
from apitable.types.record import RawRecord
from apitable.types.view import MetaView
from apitable.types.field import MetaField
from pydantic import BaseModel


class ResponseBase(BaseModel):
    """
    Unified response body format returned by REST API
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
    data: GETRecordResponseData


class PatchRecordResponse(ResponseBase):
    data: RecordsData


class PostRecordResponse(ResponseBase):
    data: RecordsData


class DeleteRecordResponse(ResponseBase):
    pass


class UploadFileResponse(ResponseBase):
    data: Dict[str, Any]


# meta field
class GETMetaFieldResponseData(BaseModel):
    items: List[MetaField]

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1250
        fields = {
            "items": "fields",  # The data returned by the server is fields, which are reserved for pydantic.
        }


class GETMetaFieldResponse(ResponseBase):
    data: GETMetaFieldResponseData


class PostMetaFieldResponseData(BaseModel):
    id: str
    name: str


class PostMetaFieldResponse(ResponseBase):
    data: PostMetaFieldResponseData


class DeleteFieldResponse(ResponseBase):
    pass


# meta view
class GETMetaViewResponseData(BaseModel):
    views: List[MetaView]


class GETMetaViewResponse(ResponseBase):
    data: GETMetaViewResponseData


# space
class GETSpaceListResponseData(BaseModel):
    spaces: List[SpaceListItem]


class GETSpaceListResponse(ResponseBase):
    data: GETSpaceListResponseData


# node
class GETNodeListResponseData(BaseModel):
    nodes: List[NodeListItem]


class GETNodeListResponse(ResponseBase):
    data: GETNodeListResponseData


class GETNodeDetailResponse(ResponseBase):
    data: NodeDetail


class PostDatasheetMetaResponseData(BaseModel):
    id: str
    createdAt: int
    items: List[PostMetaFieldResponseData]

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1250
        fields = {
            "items": "fields",  # The data returned by the server is fields, which are reserved for pydantic.
        }


class PostDatasheetMetaResponse(ResponseBase):
    data: PostDatasheetMetaResponseData


class PostEmbedLinkResponseData(BaseModel):
    payload: Optional[EmbedLinkPayload]
    theme: Optional[EmbedLinkThemeEnum]
    linkId: str
    url: str


class PostEmbedLinkResponse(ResponseBase):
    data: PostEmbedLinkResponseData


GetEmbedLinkResponseData = PostEmbedLinkResponseData


class GetEmbedLinkResponse(ResponseBase):
    data: List[GetEmbedLinkResponseData]


class DeleteEmbedLinkResponse(ResponseBase):
    pass
