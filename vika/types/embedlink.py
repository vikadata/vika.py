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
    collapsed: Optional[bool]


class EmbedLinkPayloadViewToolBar(BaseModel):
    basicTools: Optional[bool]
    shareBtn: Optional[bool]
    widgetBtn: Optional[bool]
    apiBtn: Optional[bool]
    formBtn: Optional[bool]
    historyBtn: Optional[bool]
    robotBtn: Optional[bool]


class EmbedLinkPayloadViewControl(BaseModel):
    viewId: Optional[str]
    tabBar: Optional[bool]
    toolBar: Optional[EmbedLinkPayloadViewToolBar]
    collapsed: Optional[bool]


class EmbedLinkPayload(BaseModel):
    primarySideBar: Optional[EmbedLinkPayloadSideBar]
    viewControl: Optional[EmbedLinkPayloadViewControl]
    collapsed: Optional[bool]
    permissionType: Optional[EmbedLinkPermissionType]


class EmbedLinkCreateRo(BaseModel):
    payload: Optional[EmbedLinkPayload]
    theme: Optional[EmbedLinkThemeEnum]

