from enum import Enum

from typing import List, Optional
from pydantic import BaseModel


class NodeTypeEnum(str, Enum):
    Datasheet = 'Datasheet'
    Folder = 'Folder'
    Form = 'Form'
    Dashboard = 'Dashboard'
    Mirror = 'Mirror'
    Automation = 'Automation'
    ERROR = "ERROR NODE TYPE"


class NodeListItem(BaseModel):
    id: str
    name: str
    type: NodeTypeEnum
    icon: str
    isFav: bool


class NodeDetail(NodeListItem):
    type: NodeTypeEnum = NodeTypeEnum.Folder
    children: Optional[List[NodeListItem]] = None

class NodeSearchInfo(NodeListItem):
    permission: int
    parentId: Optional[str] = None
