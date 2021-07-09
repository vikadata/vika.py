from enum import Enum

from pydantic import BaseModel


class ViewTypeEnum(str, Enum):
    Grid = 'Grid'
    Gallery = 'Gallery'
    Kanban = 'Kanban'
    Gantt = 'Gantt'


class MetaView(BaseModel):
    id: str
    name: str
    type: ViewTypeEnum
