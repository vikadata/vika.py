from enum import Enum

from typing import List, Optional
from pydantic import BaseModel


class NodeTypeEnum(str, Enum):
    Datasheet = 'Datasheet'
    Folder = 'Folder'
    Form = 'Form'
    Dashboard = 'Dashboard'


class NodeListItem(BaseModel):
    id: str
    name: str
    type: NodeTypeEnum
    icon: str
    isFav: bool


class NodeDetail(NodeListItem):
    type = NodeTypeEnum.Folder
    children: Optional[List[NodeListItem]]
