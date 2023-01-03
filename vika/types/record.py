from typing import Dict, Any
from pydantic import BaseModel


# Avoid the same name as the Record class
class RawRecord(BaseModel):
    """
    The record primitive type returned by the REST API
    """

    id: str
    data: Dict[str, Any]
    # createdAt: int
    # updatedAt: int

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1250
        fields = {
            "data": "fields",  # The data returned by the server is fields, which are reserved for pydantic.
            "id": "recordId",  # The data returned by the server is recordId, which is mapped to id here
        }
