"""
Unit of role instance.
"""
from vika.types.unit_model import ModifyRoleRequest, RawRole, PaginationRole, CreateRoleRequest, RoleUnit
from vika.unit import Unit


class Role(Unit):

    def create(self, data: CreateRoleRequest) -> RawRole:
        """
        Add a role to the specified space.
        @param data: one or multipart property of name,sequence
        @return: RawRole
        """
        r = self._space.apitable.request.post(self._role_endpoint,
                                              json=dict(data)).json()
        if r["success"]:
            return RawRole(**r['data']['role'])
        else:
            raise Exception(r['message'])

    def update(self, unit_id: str, data: ModifyRoleRequest) -> RawRole:
        """
        Update role's name, sequence and roles information.
        @param data: one or multipart property of name,sequence
        @param unit_id: role's unit id
        @return: RawRole
        """
        r = self._space.apitable.request.put(self._describe_role_endpoint(unit_id),
                                             json=dict(data)).json()
        if r["success"]:
            return RawRole(**r['data']['role'])
        else:
            raise Exception(r["message"])

    def delete(self, unit_id: str) -> bool:
        """
        Remove a role from the specified space, notice: Only empty roles can be deleted，
        @param unit_id: role's unit id
        @return: bool
        """
        r = self._space.apitable.request.delete(self._describe_role_endpoint(unit_id)).json()
        return r['success']

    def list(self, page_num=1, page_size=100) -> PaginationRole:
        """
        Paging to get the list of roles.
        @param page_num: the page number of the pagination
        @param page_size: this parameter only accepts integers from 1-1000
        """
        r = self._space.apitable.request.get(self._role_endpoint,
                                             params={
                                                 'pageNum': page_num,
                                                 'pageSize': page_size
                                             }).json()
        if r["success"]:
            return PaginationRole(**r['data'])
        else:
            raise Exception(r["message"])

    def list_unit(self, unit_id: str) -> RoleUnit:
        """
        Get the organizational units under the specified role unitId, the returned data includes teams and members.
        @param unit_id: role's unit id
        """
        r = self._space.apitable.request.get(self._list_role_unit_endpoint(unit_id)).json()
        if r["success"]:
            return RoleUnit(**r['data'])
        else:
            raise Exception(r["message"])
