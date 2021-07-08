from typing import Optional

from pydantic import BaseModel


class SpaceListItem(BaseModel):
    id: str
    name: str
    isAdmin: Optional[bool]
