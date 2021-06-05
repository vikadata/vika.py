# 客户端状态
from enum import Enum

from pydantic import BaseModel


class FetchDataEnum(str, Enum):
    ALL = 'ALL'
    ByView = "View"
    ByFormula = "ByFormula"
