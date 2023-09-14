""" Unit tests for `core_linked_records.components.data.access_control`.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_linked_records_app.access_control import rights
from core_linked_records_app.components.pid_settings import (
    access_control as pid_settings_acl,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCanUpsertPidSetting(TestCase):
    """Unit tests for `can_upsert_pid_settings` function."""

    def setUp(self) -> None:
        """setUp"""
        self.user = create_mock_user("1")
        self.mock_kwargs = {
            "func": MagicMock(),
            "pid_settings_object": MagicMock(),
            "user": self.user,
        }

    def test_superuser_returns_func(self):
        """test_superuser_returns_func"""
        self.user.is_superuser = True

        pid_settings_acl.can_upsert_pid_settings(**self.mock_kwargs)
        self.mock_kwargs["func"].assert_called_with(
            self.mock_kwargs["pid_settings_object"], self.mock_kwargs["user"]
        )

    def test_not_superuser_raises_acl_error(self):
        """test_not_superuser_raises_acl_error"""
        with self.assertRaises(AccessControlError):
            pid_settings_acl.can_upsert_pid_settings(**self.mock_kwargs)


class TestCanGetPidSetting(TestCase):
    """Unit tests for `can_get_pid_settings` function."""

    def setUp(self) -> None:
        self.mock_kwargs = {
            "func": MagicMock(),
            "user": create_mock_user("1"),
        }

    @patch.object(pid_settings_acl, "check_has_perm")
    @patch.object(pid_settings_acl, "settings")
    def test_check_has_perm_not_called_when_public(
        self, mock_settings, mock_check_has_perm
    ):
        """test_check_has_perm_not_called_when_public"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True
        pid_settings_acl.can_get_pid_settings(**self.mock_kwargs)
        mock_check_has_perm.assert_not_called()

    @patch.object(pid_settings_acl, "check_has_perm")
    @patch.object(pid_settings_acl, "settings")
    def test_check_has_perm_called_when_private(
        self, mock_settings, mock_check_has_perm
    ):
        """test_check_has_perm_called_when_private"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        pid_settings_acl.can_get_pid_settings(**self.mock_kwargs)
        mock_check_has_perm.assert_called_with(
            self.mock_kwargs["user"], rights.CAN_READ_PID_SETTINGS
        )

    @patch.object(pid_settings_acl, "check_has_perm")
    @patch.object(pid_settings_acl, "settings")
    def test_check_has_perm_fail_raises_acl_error(
        self, mock_settings, mock_check_has_perm
    ):
        """test_check_has_perm_fail_raises_acl_error"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        mock_check_has_perm.side_effect = AccessControlError(
            "test_check_has_perm_fail_raises_acl_error"
        )

        with self.assertRaises(AccessControlError):
            pid_settings_acl.can_get_pid_settings(**self.mock_kwargs)

    @patch.object(pid_settings_acl, "check_has_perm")
    @patch.object(pid_settings_acl, "settings")
    def test_successful_execution_returns_func_with_args(
        self,
        mock_settings,
        mock_check_has_perm,  # noqa, pylint: disable=unused-argument
    ):
        """test_successful_execution_returns_func_with_args"""
        mock_settings.CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = False
        self.assertEqual(
            pid_settings_acl.can_get_pid_settings(**self.mock_kwargs),
            self.mock_kwargs["func"](self.mock_kwargs["user"]),
        )
