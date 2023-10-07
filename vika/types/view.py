from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ViewTypeEnum(str, Enum):
    Grid = 'Grid'
    Gallery = 'Gallery'
    Kanban = 'Kanban'
    Gantt = 'Gantt'
    Calendar = 'Calendar'
    Architecture = 'Architecture'


class MetaView(BaseModel):
    id: str
    name: str
    type: Optional[ViewTypeEnum] = None
