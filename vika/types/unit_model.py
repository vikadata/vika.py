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
    email: Optional[str] = None
    mobile: Mobile = Optional[Mobile]
    status: int
    type: MemberTypeEnum
    teams: List[RawTeam]
    roles: List[RawRole]


class ModifyMemberRequest(BaseModel):
    name: Optional[str] = None
    teams: Optional[List[str]] = None
    roles: Optional[List[str]] = None


class CreateRoleRequest(BaseModel):
    name: str
    sequence: Optional[int] = None


class ModifyRoleRequest(BaseModel):
    name: Optional[str] = None
    sequence: Optional[int] = None


class CreateTeamRequest(BaseModel):
    name: str
    sequence: Optional[int] = None
    # default "0" means root team
    parentUnitId: Optional[str] = None
    roles: Optional[List[str]] = None


class ModifyTeamRequest(BaseModel):
    name: Optional[str] = None
    sequence: Optional[int] = None
    parentUnitId: Optional[str] = None
    roles: Optional[List[str]] = None


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
