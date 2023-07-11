import unittest
from unittest import mock
from unittest.mock import MagicMock

from vika.types import CreateRoleRequest, ModifyRoleRequest, RawRole
from test.test_apitable import TestApitable


class TestUnit(TestApitable):

    def test_create_role_with_name_exist(self):
        # space = Space(mock_apitable, "mock_space")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "message": 'A role with the same name exists',
            "code": 1509
        }
        self._apitable.request.post.return_value = mock_response
        self._space.role._role_endpoint = mock.Mock(return_vaule='/test_endpoint')
        with self.assertRaises(Exception) as context:
            self._space.role.create(CreateRoleRequest(name="test_role"))
            self.assertEquals(context.exception.__str__(), 'A role with the same name exists')

    def test_create_role_with_no_permission(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "message": 'This API is only available for the primary admin and sub-admins who can manage roles',
            "code": 1508
        }
        self._apitable.request.post.return_value = mock_response
        self._space.role._role_endpoint = mock.Mock(return_vaule='/test_endpoint')
        with self.assertRaises(Exception) as ct:
            self._space.role.create(CreateRoleRequest(name="test_role"))
            self.assertEquals(ct.exception.__str__(),
                              'This API is only available for the primary admin and sub-admins who can manage roles')

    def test_create_role_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "success": True,
            "message": 'SUCCESS',
            "code": 200,
            "data": {
                "role": {
                    "unitId": 'test_unit_id',
                    "name": 'test_role',
                    "sequence": 2000
                }
            }
        }
        self._apitable.request.post.return_value = mock_response
        self._space.role._role_endpoint = mock.Mock(return_vaule='/test_endpoint')
        role = self._space.role.create(CreateRoleRequest(name="test_role"))
        self.assertEqual(role, RawRole(**mock_response.json.return_value['data']['role']))

    def test_request_role_api_server_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "success": False,
            "message": 'Server error',
            "code": 500
        }
        self._apitable.request.post.return_value = mock_response
        self._space.role._role_endpoint = mock.Mock(return_vaule='/test_endpoint')
        with self.assertRaises(Exception) as ct:
            self._space.role.create(CreateRoleRequest(name="test_role"))
            self.assertEquals(ct.exception.__str__(), 'Server error')

    def test_update_role_with_not_exist(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "message": 'The unit specified by the unit ID does not exist',
            "code": 400
        }
        self._apitable.request.post.return_value = mock_response
        self._space.role._describe_role_endpoint = mock.Mock(return_vaule='/test_endpoint')
        with self.assertRaises(Exception) as ct:
            self._space.role.update('test_role', ModifyRoleRequest(name="test_role"))
            self.assertEquals(ct.exception.__str__(), 'The unit specified by the unit ID does not exist')


if __name__ == "__main__":
    unittest.main()
