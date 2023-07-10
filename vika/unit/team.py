"""
Unit of team instance.
"""
from vika.types.unit_model import CreateTeamRequest, RawTeam, ModifyTeamRequest, PaginationTeam, PaginationMember
from vika.unit import Unit


class Team(Unit):
    def create(self, data: CreateTeamRequest) -> RawTeam:
        """
        Add a team to the specified space.
        @param data: team information
        @return: RawTeam
        """
        r = self._space.apitable.request.post(self._team_endpoint,
                                              json=dict(data)).json()
        if r["success"]:
            return RawTeam(**r['data']['team'])
        else:
            raise Exception(r['message'])

    def update(self, unit_id: str, data: ModifyTeamRequest) -> RawTeam:
        """
        Update team's information roles information.
        @param data: team information
        @param unit_id: team's unit id
        @return: RawTeam
        """
        r = self._space.apitable.request.put(self._describe_team_endpoint(unit_id),
                                             json=dict(data)).json()
        if r["success"]:
            return RawTeam(**r['data']['team'])
        else:
            raise Exception(r["message"])

    def delete(self, unit_id: str) -> bool:
        """
        Remove a team from the specified space, notice: Only empty team can be deleted，
        @param unit_id: team's unit id
        @return: bool
        """
        r = self._space.apitable.request.delete(self._describe_team_endpoint(unit_id)).json()
        return r['success']

    def list_sub_teams(self, unit_id: str, page_num=1, page_size=100) -> PaginationTeam:
        """
        Paging to get the sub list of teams.
        @param unit_id: parent team’s unitId, root team id is "0"
        @param page_num: the page number of the pagination
        @param page_size: this parameter only accepts integers from 1-1000
        """
        r = self._space.apitable.request.get(self._list_sub_team_endpoint(unit_id),
                                             params={
                                                 'pageNum': page_num,
                                                 'pageSize': page_size
                                             }).json()
        if r["success"]:
            return PaginationTeam(**r['data'])
        else:
            raise Exception(r["message"])

    def list_members(self, unit_id: str, sensitive_data=False, page_num=1, page_size=100) -> PaginationMember:
        """
        List members under the team.
        @param sensitive_data: fill in “true“ to return member’s sensitive data, includes mobile number and email
        @param unit_id: current team’s unitId, root team id is "0"
        @param page_num: the page number of the pagination
        @param page_size: this parameter only accepts integers from 1-1000
        """
        r = self._space.apitable.request.get(self._list_team_member_endpoint(unit_id),
                                             params={
                                                 "sensitiveData": sensitive_data,
                                                 'pageNum': page_num,
                                                 'pageSize': page_size
                                             }).json()
        if r["success"]:
            return PaginationMember(**r['data'])
        else:
            raise Exception(r["message"])
