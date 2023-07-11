"""
Unit of member instance.
"""
from urllib.parse import urljoin


class Unit:
    """
    Unit object including member,team and role.
    """

    def __init__(self, space: 'Space'):
        self._space = space

    def _describe_member_endpoint(self, unit_id: str):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/members/{unit_id}")

    def _role_endpoint(self):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/roles")

    def _describe_role_endpoint(self, unit_id: str):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/roles/{unit_id}")

    def _list_role_unit_endpoint(self, unit_id: str):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/roles/{unit_id}/units")

    def _team_endpoint(self):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/teams")

    def _describe_team_endpoint(self, unit_id: str):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/teams/{unit_id}")

    def _list_sub_team_endpoint(self, unit_id: str):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/teams/{unit_id}/children")

    def _list_team_member_endpoint(self, unit_id: str):
        return urljoin(self._space.apitable.api_base,
                       f"/fusion/v1/spaces/{self._space.id}/teams/{unit_id}/members")
