from typing import Dict, Any, Optional
from pydantic import ConfigDict, BaseModel, Field


# Avoid the same name as the Record class
class RawRecord(BaseModel):
    """
    The record primitive type returned by the REST API
    """

    id: Optional[str] = Field(alias="recordId")
    data: Dict[str, Any] = Field(alias="fields")
   