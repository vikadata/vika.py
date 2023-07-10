"""
Unit of member instance.
"""

from vika.types.unit_model import ModifyMemberRequest, RawMember
from vika.unit.unit import Unit


class Member(Unit):
    """
    Member object.
    """

    def update(self, unit_id: str, data: ModifyMemberRequest) -> RawMember:
        """
        Update member's name, teams and roles information.
        @param data: one or multipart property of name,teams,roles.
        @param unit_id: role's unit id
        @return: RawMember
        """
        r = self._space.apitable.request.put(self._describe_member_endpoint(unit_id),
                                             json=dict(data)).json()
        if r["success"]:
            return RawMember(**r['data']['member'])
        else:
            raise Exception(r["message"])

    def get(self, unit_id: str) -> RawMember:
        """
        Update member's name, teams and roles information.
        @param unit_id: role's unit id
        @return: RawMember
        """
        r = self._space.apitable.request.get(self._describe_member_endpoint(unit_id)).json()
        if r["success"]:
            return RawMember(**r['data']['member'])
        else:
            raise Exception(r["message"])

    def delete(self, unit_id: str) -> bool:
        """
        Remove a member from the specified space
        @param unit_id: role's unit id
        @return: bool
        """
        r = self._space.apitable.request.delete(self._describe_member_endpoint(unit_id)).json()
        return r['success']
