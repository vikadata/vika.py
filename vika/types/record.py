from typing import Dict, Any
from pydantic import BaseModel


# 避免和 Record class 重名
class RawRecord(BaseModel):
    """
    REST API 返回的 record 原始类型
    """

    id: str
    data: Dict[str, Any]
    # createdAt: int
    # updatedAt: int

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/1250
        fields = {
            "data": "fields",  # 服务端返回的数据为 fields，此字段为 pydantic 保留字段。
            "id": "recordId",  # 服务端返回的数据为 recordId，这里映射成 id
        }
