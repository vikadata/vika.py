"""
Unit type
"""
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class RawUnit(BaseModel):
    unitId: str
    name: str


class RawRole(RawUnit):
    sequence: int


class RawTeam(RawUnit):
    sequence: int
    parentUnitId: str
    roles: List[RawRole]


class Mobile(BaseModel):
    areaCode: str
    number: str


class MemberTypeEnum(str, Enum):
    """
    Member's type.
    PrimaryAdmin: the owner of the space
    SubAdmin: the team,member,role manager
    Member: ordinary member
    """
    PrimaryAdmin = 'PrimaryAdmin'
    SubAdmin = 'SubAdmin'
    Member = 'Member'


class RawMember(RawUnit):
    avatar: str
    email: Optional[str]
    mobile: Mobile = Optional[Mobile]
    status: int
    type: MemberTypeEnum
    teams: List[RawTeam]
    roles: List[RawRole]


class ModifyMemberRequest(BaseModel):
    name: Optional[str]
    teams: Optional[List[str]]
    roles: Optional[List[str]]


class CreateRoleRequest(BaseModel):
    name: str
    sequence: Optional[int]


class ModifyRoleRequest(BaseModel):
    name: Optional[str]
    sequence: Optional[int]


class CreateTeamRequest(BaseModel):
    name: str
    sequence: Optional[int]
    # default "0" means root team
    parentUnitId: Optional[str]
    roles: Optional[List[str]]


class ModifyTeamRequest(BaseModel):
    name: Optional[str]
    sequence: Optional[int]
    parentUnitId: Optional[str]
    roles: Optional[List[str]]


class RoleUnit(BaseModel):
    teams: List[RawTeam]
    members: List[RawMember]


class PaginationUnit(BaseModel):
    pageSize: int
    pageNum: int
    total: int


class PaginationRole(PaginationUnit):
    roles: List[RawRole]


class PaginationTeam(PaginationUnit):
    teams: List[RawTeam]


class PaginationMember(PaginationUnit):
    members: List[RawMember]
