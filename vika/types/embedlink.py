from enum import Enum
from pydantic import BaseModel
from typing import Optional


class EmbedLinkThemeEnum(str, Enum):
    Light = 'light'
    DARK = 'dark'


class EmbedLinkPermissionType(str, Enum):
    READ_ONLY = 'readOnly'
    PUBLIC_EDIT = 'publicEdit'
    PRIVATE_EDIT = 'privateEdit'


class EmbedLinkPayloadSideBar(BaseModel):
    collapsed: Optional[bool] = None


class EmbedLinkPayloadViewToolBar(BaseModel):
    basicTools: Optional[bool] = None
    shareBtn: Optional[bool] = None
    widgetBtn: Optional[bool] = None
    apiBtn: Optional[bool] = None
    formBtn: Optional[bool] = None
    historyBtn: Optional[bool] = None
    robotBtn: Optional[bool] = None


class EmbedLinkPayloadViewControl(BaseModel):
    viewId: Optional[str] = None
    tabBar: Optional[bool] = None
    toolBar: Optional[EmbedLinkPayloadViewToolBar] = None
    collapsed: Optional[bool] = None


class EmbedLinkPayload(BaseModel):
    primarySideBar: Optional[EmbedLinkPayloadSideBar] = None
    viewControl: Optional[EmbedLinkPayloadViewControl] = None
    collapsed: Optional[bool] = None
    permissionType: Optional[EmbedLinkPermissionType] = None


class EmbedLinkCreateRo(BaseModel):
    payload: Optional[EmbedLinkPayload] = None
    theme: Optional[EmbedLinkThemeEnum] = None

