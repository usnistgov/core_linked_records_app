""" Unit tests for `core_linked_records.components.pid_path.access_control`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.pid_path import (
    access_control as pid_path_acl,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCanGetByTemplate(TestCase):
    """Unit tests for `can_get_by_template` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_kwargs = {
            "func": MagicMock(),
            "template": MagicMock(),
            "user": create_mock_user("1"),
        }

    @patch.object(pid_path_acl, "check_can_read_template")
    def test_check_can_read_template_called(
        self, mock_check_can_read_template
    ):
        """test_check_can_read_template_called"""
        pid_path_acl.can_get_by_template(**self.mock_kwargs)

        mock_check_can_read_template.assert_called_with(
            self.mock_kwargs["template"], self.mock_kwargs["user"]
        )

    @patch.object(pid_path_acl, "check_can_read_template")
    def test_check_can_read_template_failure_raises_acl_error(
        self, mock_check_can_read_template
    ):
        """test_check_can_read_template_failure_raises_acl_error"""
        mock_check_can_read_template.side_effect = AccessControlError(
            "mock_check_can_read_template_acl_error"
        )

        with self.assertRaises(AccessControlError):
            pid_path_acl.can_get_by_template(**self.mock_kwargs)

    @patch.object(pid_path_acl, "check_can_read_template")
    def test_successful_execution_returns_func_with_args(
        self,
        mock_check_can_read_template,  # noqa, pylint: disable=unused-argument
    ):
        """test_successful_execution_returns_func_with_args"""
        self.assertEqual(
            pid_path_acl.can_get_by_template(**self.mock_kwargs),
            self.mock_kwargs["func"](
                self.mock_kwargs["template"], self.mock_kwargs["user"]
            ),
        )
