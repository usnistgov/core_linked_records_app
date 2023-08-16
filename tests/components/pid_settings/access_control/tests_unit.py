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


class TestCanGetDataByPid(TestCase):
    """Unit tests for `can_get_data_by_pid` function."""

    def setUp(self) -> None:
        self.mock_kwargs = {
            "func": MagicMock(),
            "user": create_mock_user("1"),
        }

    @patch.object(pid_settings_acl, "check_has_perm")
    def test_check_has_perm_called(self, mock_check_has_perm):
        """test_check_has_perm_called"""
        pid_settings_acl.can_get_pid_settings(**self.mock_kwargs)
        mock_check_has_perm.assert_called_with(
            self.mock_kwargs["user"], rights.CAN_READ_PID_SETTINGS
        )

    @patch.object(pid_settings_acl, "check_has_perm")
    def test_check_has_perm_fail_raises_acl_error(self, mock_check_has_perm):
        """test_check_has_perm_fail_raises_acl_error"""
        mock_check_has_perm.side_effect = AccessControlError(
            "test_check_has_perm_fail_raises_acl_error"
        )

        with self.assertRaises(AccessControlError):
            pid_settings_acl.can_get_pid_settings(**self.mock_kwargs)

    @patch.object(pid_settings_acl, "check_has_perm")
    def test_successful_execution_returns_func_with_args(
        self, mock_check_has_perm  # noqa, pylint: disable=unused-argument
    ):
        """test_successful_execution_returns_func_with_args"""
        self.assertEqual(
            pid_settings_acl.can_get_pid_settings(**self.mock_kwargs),
            self.mock_kwargs["func"](self.mock_kwargs["user"]),
        )
