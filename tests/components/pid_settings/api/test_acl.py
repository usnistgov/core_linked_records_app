""" ACL tests for `core_linked_records.components.pid_settings.api`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.pid_settings import (
    api as pid_settings_api,
    access_control as pid_settings_acl,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestGet(TestCase):
    """ACL tests for `get` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_pid_settings = MagicMock()

    @patch.object(pid_settings_api, "pid_settings_system_api")
    def test_superuser_can_access(self, mock_pid_settings_system_api):
        """test_superuser_can_access"""
        user = create_mock_user("1", is_superuser=True)
        mock_pid_settings_system_api.get.return_value = self.mock_pid_settings

        self.assertEqual(pid_settings_api.get(user), self.mock_pid_settings)

    @patch.object(pid_settings_api, "pid_settings_system_api")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_registered_user_without_perm_cannot_access(
        self, mock_check_has_perm, mock_pid_settings_system_api
    ):
        """test_registered_user_without_perm_cannot_access"""
        user = create_mock_user("1")
        mock_check_has_perm.side_effect = AccessControlError(
            "mock_check_has_perm_acl_error"
        )
        mock_pid_settings_system_api.get.return_value = self.mock_pid_settings

        with self.assertRaises(AccessControlError):
            pid_settings_api.get(user)

    @patch.object(pid_settings_api, "pid_settings_system_api")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_registered_user_with_perm_can_access(
        self,
        mock_check_has_perm,  # noqa, pylint: disable=unused-argument
        mock_pid_settings_system_api,
    ):
        """test_registered_user_with_perm_can_access"""
        user = create_mock_user("1")
        mock_pid_settings_system_api.get.return_value = self.mock_pid_settings

        self.assertEqual(pid_settings_api.get(user), self.mock_pid_settings)

    @patch.object(pid_settings_api, "pid_settings_system_api")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_anonymous_user_without_perm_cannot_access(
        self, mock_check_has_perm, mock_pid_settings_system_api
    ):
        """test_anonymous_user_without_perm_cannot_access"""
        user = create_mock_user("1", is_anonymous=True)
        mock_check_has_perm.side_effect = AccessControlError(
            "mock_check_has_perm_acl_error"
        )
        mock_pid_settings_system_api.get.return_value = self.mock_pid_settings

        with self.assertRaises(AccessControlError):
            pid_settings_api.get(user)

    @patch.object(pid_settings_api, "pid_settings_system_api")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_anonymous_user_with_perm_can_access(
        self,
        mock_check_has_perm,  # noqa, pylint: disable=unused-argument
        mock_pid_settings_system_api,
    ):
        """test_anonymous_user_with_perm_can_access"""
        user = create_mock_user("1", is_anonymous=True)
        mock_pid_settings_system_api.get.return_value = self.mock_pid_settings

        self.assertEqual(pid_settings_api.get(user), self.mock_pid_settings)
