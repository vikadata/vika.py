from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel


# enum
class PermissionLevelEnum(str, Enum):
    edit = 'edit'
    read = 'read'


class MemberEnum(str, Enum):
    member = 'member'
    team = 'team'


class RollUpFunctionEnum(str, Enum):
    VALUES = 'VALUES'
    AVERAGE = 'AVERAGE'
    COUNT = 'COUNT'
    COUNTA = 'COUNTA'
    COUNTALL = 'COUNTALL'
    SUM = 'SUM'
    MIN = 'MIN'
    MAX = 'MAX'
    AND = 'AND'
    OR = 'OR'
    XOR = 'XOR'
    CONCATENATE = 'CONCATENATE'
    ARRAYJOIN = 'ARRAYJOIN'
    ARRAYUNIQUE = 'ARRAYUNIQUE'
    ARRAYCOMPACT = 'ARRAYCOMPACT'


class ComputeValueTypeEnum(str, Enum):
    string = 'string'
    boolean = 'boolean'
    number = 'number'
    array = 'array'


# field property
class SingleTextFieldProperty:
    defaultValue: Optional[str]


class NumberFieldProperty:
    defaultValue: Optional[str]
    precision: int


class CurrencyFieldProperty(NumberFieldProperty):
    symbol: str


class PercentFieldProperty(NumberFieldProperty):
    pass


class SelectOptionColor:
    name: str
    value: str


class SelectOption:
    id: str
    name: str
    color: SelectOptionColor


class SingleSelectFieldProperty:
    options: List[SelectOption]


class MultiSelectFieldProperty(SingleSelectFieldProperty):
    pass


class MemberOption:
    id: str
    name: str
    type: MemberEnum
    avatar: Optional[str]


class MemberFieldProperty:
    options: List[MemberOption]


class UserOption:
    id: str
    name: str
    avatar: str


class CreateByFieldProperty:
    options: List[UserOption]


class LastModifiedByFieldProperty(CreateByFieldProperty):
    pass


class CheckboxFieldProperty:
    icon: str


class RatingFieldProperty:
    icon: str
    max: int


class DateTimeFieldProperty:
    format: str
    autoFill: bool
    includeTime: bool


class CreatedTimeFieldProperty(DateTimeFieldProperty):
    pass


class LastModifiedTimeFieldProperty(DateTimeFieldProperty):
    pass


class LinkFieldProperty:
    foreignDatasheetId: str
    brotherFieldId: str


class FieldPropertyWithDstId:
    datasheetId: str
    field: "MetaField"


class LookupFieldProperty:
    relatedLinkFieldId: str
    targetField: FieldPropertyWithDstId
    hasError: Optional[bool]
    entityField: Optional[FieldPropertyWithDstId]
    rollupFunction: RollUpFunctionEnum
    valueType: ComputeValueTypeEnum


class FormulaFieldProperty:
    expression: Optional[str]  # 一定会有公式表达式吗
    valueType: ComputeValueTypeEnum
    hasError: Optional[bool]


FieldProperty = Union[
    SingleTextFieldProperty,
    NumberFieldProperty,
    CurrencyFieldProperty,
    PercentFieldProperty,
    SingleSelectFieldProperty,
    MultiSelectFieldProperty,
    MemberFieldProperty,
    CreateByFieldProperty,
    LastModifiedByFieldProperty,
    CheckboxFieldProperty,
    RatingFieldProperty,
    DateTimeFieldProperty,
    DateTimeFieldProperty,
    CreatedTimeFieldProperty,
    LastModifiedTimeFieldProperty,
    LinkFieldProperty,
    LookupFieldProperty,
    FormulaFieldProperty,
]


# field item
class MetaField(BaseModel):
    id: str
    name: str
    type: str
    isPrimary: Optional[bool]
    desc: Optional[str]
    property: Optional[FieldProperty]
    permissionLevel: Optional[PermissionLevelEnum]
