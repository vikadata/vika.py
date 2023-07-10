import os

from apitable import Apitable
from apitable.types.unit import RawRole, PaginationRole, ModifyRoleRequest, RawMember, ModifyMemberRequest, RawTeam, \
    CreateTeamRequest, ModifyTeamRequest, PaginationTeam, PaginationMember


class UnitExample:
    def __init__(self):
        apitable = Apitable(os.getenv('TOKEN'))
        apitable.set_api_base(os.getenv('HOST'))
        self._space = apitable.space(os.getenv('SPACE_ID'))


class UnitRoleExample(UnitExample):
    def create_role(self, name: str, sequence: int) -> RawRole:
        return self._space.role.create({
            "name": name,
            "sequence": sequence
        })

    def list_role(self) -> PaginationRole:
        return self._space.role.list()

    def delete_role(self, unit_id: str):
        self._space.role.delete(unit_id)

    def update_role(self, unit_id: str, name: str, sequence: int) -> RawRole:
        request = ModifyRoleRequest(name=name, sequence=sequence)
        return self._space.role.update(unit_id, request)

    def run(self):
        roles = []
        for i in range(0, 2):
            role = self.create_role('test_role' + str(i), i * 2000)
            roles.append(role.unitId)

        units = self.list_role()
        for item in units.roles:
            print("roleName: " + item.name + "\n")

        for index, unitId in enumerate(roles):
            role = self.update_role(unitId, 'test_role' + str(index + 2), (index + 2) * 3000)
            print("updateRoleName: " + role.name + "\n")
            self.delete_role(unitId)


class UnitMemberExample(UnitExample):
    def get_member(self, unit_id: str) -> RawMember:
        return self._space.member.get(unit_id)

    def update_member(self, unit_id: str, name: str) -> RawMember:
        request = ModifyMemberRequest(name=name)
        return self._space.member.update(unit_id, request)

    def update_member_team(self, unit_id: str, team_unit_d: str) -> RawMember:
        request = ModifyMemberRequest(teams=[team_unit_d])
        return self._space.member.update(unit_id, request)

    def run(self):
        unitId = os.getenv("MEMBER_UNIT_ID")
        member = self.get_member(unitId)
        print("memberName: " + member.name + "\n")
        newMember = self.update_member(unitId, "newMemberName")
        print("newMemberName: " + newMember.name + "\n")


class UnitTeamExample(UnitExample):

    def create_team(self, name: str, parent_unit_id: str, sequence: int, roles: list[str]) -> RawTeam:
        request = CreateTeamRequest(name=name, sequence=sequence, parentUnitId=parent_unit_id, roles=roles)
        return self._space.team.create(request)

    def update_team(self, unit_id: str, parent_unit_id: str) -> RawTeam:
        request = ModifyTeamRequest(parentUnitId=parent_unit_id)
        return self._space.team.update(unit_id, request)

    def delete_team(self, unit_id: str) -> RawTeam:
        return self._space.team.delete(unit_id)

    def list_sub_teams(self, unit_id: str) -> PaginationTeam:
        return self._space.team.list_sub_teams(unit_id)

    def list_members(self, unit_id: str) -> PaginationMember:
        return self._space.team.list_members(unit_id)

    def get_sub_teams(self, unit_id: str) -> list[RawTeam]:
        result = self.list_sub_teams(unit_id)
        for x in result.teams:
            print("teamName: " + x.name + "\n")
            self.get_sub_teams(x.unitId)

    def run(self):
        role = roleExample.create_role("test_role", 1000)
        teams = []
        for i in range(0, 2):
            team = self.create_team("test_team_" + str(i), "0", i, [role.unitId])
            teams.append(team.unitId)
        # get all, notice you should teke care of the page information
        self.get_sub_teams("0")
        # move the second team under the first team
        self.update_team(teams[1], teams[0])
        # change member team
        memberExample.update_member_team(os.getenv("MEMBER_UNIT_ID"), teams[1])
        # get team member
        members = self.list_members(teams[1])
        for member in members.members:
            print("memberName: " + member.name)
        memberExample.update_member_team(os.getenv("MEMBER_UNIT_ID"), "0")
        self.delete_team(teams[1])
        self.delete_team(teams[0])
        roleExample.delete_role(role.unitId)


if __name__ == "__main__":
    roleExample = UnitRoleExample()
    # roleExample.run()

    memberExample = UnitMemberExample()
    # memberExample.run()

    teamExample = UnitTeamExample()
    teamExample.run()
