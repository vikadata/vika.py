from enum import Enum
from typing import List, Optional, Union, Any

from pydantic import BaseModel
from typing import ForwardRef


class MemberEnum(str, Enum):
    Member = 'Member'
    Team = 'Team'


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
    String = 'String'
    Boolean = 'Boolean'
    Number = 'Number'
    Array = 'Array'
    DateTime = 'DateTime'


# field property
class SingleTextFieldProperty(BaseModel):
    defaultValue: Optional[str] = None


class NumberFieldProperty(BaseModel):
    defaultValue: Optional[str] = None
    precision: int


class CurrencyFieldProperty(NumberFieldProperty):
    symbol: str


class PercentFieldProperty(NumberFieldProperty):
    pass


class SelectOptionColor(BaseModel):
    name: str
    value: str


class SelectOption(BaseModel):
    id: str
    name: str
    color: SelectOptionColor


class SingleSelectFieldProperty(BaseModel):
    options: List[SelectOption]


class MultiSelectFieldProperty(SingleSelectFieldProperty):
    pass


class MemberOption(BaseModel):
    id: str
    name: str
    type: MemberEnum
    avatar: Optional[str] = None


class MemberFieldProperty(BaseModel):
    options: List[MemberOption]


class UserOption(BaseModel):
    id: str
    name: str
    avatar: str


class CreatedByFieldProperty(BaseModel):
    options: List[UserOption]


class LastModifiedByFieldProperty(CreatedByFieldProperty):
    pass


class CheckboxFieldProperty(BaseModel):
    icon: str


class RatingFieldProperty(BaseModel):
    icon: str
    max: int


class DateTimeFieldProperty(BaseModel):
    format: str
    autoFill: bool = False
    includeTime: bool = False


class CreatedTimeFieldProperty(DateTimeFieldProperty):
    pass


class LastModifiedTimeFieldProperty(DateTimeFieldProperty):
    pass


class MagicLinkFieldProperty(BaseModel):
    foreignDatasheetId: str
    brotherFieldId: Optional[str] = ""  # No brother field when it links itself


class FieldPropertyWithDstId(BaseModel):
    datasheetId: str
    field: ForwardRef("MetaField")


class MagicLookupFieldProperty(BaseModel):
    relatedLinkFieldId: str
    targetFieldId: str
    hasError: Optional[bool] = None
    entityField: Optional[FieldPropertyWithDstId] = None
    rollupFunction: RollUpFunctionEnum
    valueType: Optional[ComputeValueTypeEnum] = ComputeValueTypeEnum.String


class FormulaFieldProperty(BaseModel):
    expression: Optional[str] = None
    valueType: Optional[ComputeValueTypeEnum] = ComputeValueTypeEnum.String
    hasError: Optional[bool] = None


FieldProperty = Union[
    NumberFieldProperty,
    SingleTextFieldProperty,
    CurrencyFieldProperty,
    PercentFieldProperty,
    SingleSelectFieldProperty,
    MultiSelectFieldProperty,
    MemberFieldProperty,
    CreatedByFieldProperty,
    LastModifiedByFieldProperty,
    CheckboxFieldProperty,
    RatingFieldProperty,
    DateTimeFieldProperty,
    CreatedTimeFieldProperty,
    LastModifiedTimeFieldProperty,
    MagicLinkFieldProperty,
    MagicLookupFieldProperty,
    FormulaFieldProperty,
]


# field item
class MetaField(BaseModel):
    id: str
    name: str
    type: str
    isPrimary: Optional[bool] = False
    desc: Optional[str] = None
    editable: Optional[bool] = None

    # Union Types is not parsed correctly, here is the manual parsing of Any.
    # fuck https://github.com/samuelcolvin/pydantic/issues/2941
    property: Any = None

    def __init__(self, property=None, **data) -> None:
        property_model = self.get_property_by_type(data['type'])
        _property = property_model(**property) if property_model else property
        super().__init__(property=_property, **data)

    @staticmethod
    def get_property_by_type(type):
        type_property_map = {
            "SingleText": SingleTextFieldProperty,
            "Text": None,
            "SingleSelect": SingleSelectFieldProperty,
            "MultiSelect": MultiSelectFieldProperty,
            "Number": NumberFieldProperty,
            "Currency": CurrencyFieldProperty,
            "Percent": PercentFieldProperty,
            "DateTime": DateTimeFieldProperty,
            "Attachment": None,
            "Member": MemberFieldProperty,
            "Checkbox": CheckboxFieldProperty,
            "Rating": RatingFieldProperty,
            "URL": None,
            "Phone": None,
            "Email": None,
            "MagicLink": MagicLinkFieldProperty,
            "MagicLookUp": MagicLookupFieldProperty,
            "Formula": FormulaFieldProperty,
            "AutoNumber": None,
            "CreatedTime": CreatedTimeFieldProperty,
            "LastModifiedTime": LastModifiedTimeFieldProperty,
            "CreatedBy": CreatedByFieldProperty,
            "LastModifiedBy": LastModifiedByFieldProperty,
        }
        return type_property_map.get(type, None)


FieldPropertyWithDstId.model_rebuild()
