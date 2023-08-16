""" Unit tests for `core_linked_records.components.oai_data.access_control`.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_linked_records_app.components.oai_record import (
    access_control as oai_record_acl,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCanGetPidForData(TestCase):
    """Unit tests for `can_get_pid_for_data` function."""

    def setUp(self) -> None:
        mock_request = MagicMock()
        mock_request.user = create_mock_user("1")

        self.mock_kwargs = {
            "func": MagicMock(),
            "oai_record_id": "mock_oai_record_id",
            "request": mock_request,
        }

    @patch.object(oai_record_acl, "check_anonymous_access")
    def test_check_anonymous_access_called(self, mock_check_anonymous_access):
        """test_check_anonymous_access_called"""
        oai_record_acl.can_get_pid_for_data(**self.mock_kwargs)
        mock_check_anonymous_access.assert_called_with(
            self.mock_kwargs["request"].user
        )

    @patch.object(oai_record_acl, "check_anonymous_access")
    def test_check_anonymous_access_failure_raise_acl_error(
        self, mock_check_anonymous_access
    ):
        """test_check_anonymous_access_failure_raise_acl_error"""
        mock_check_anonymous_access.side_effect = AccessControlError(
            "mock_check_anonymous_access_mock_acl_error"
        )

        with self.assertRaises(AccessControlError):
            oai_record_acl.can_get_pid_for_data(**self.mock_kwargs)

    @patch.object(oai_record_acl, "check_anonymous_access")
    def test_successful_execution_returns_func_with_args(
        self,
        mock_check_anonymous_access,  # noqa, pylint: disable=unused-argument
    ):
        """test_successful_execution_returns_func_with_args"""
        self.assertEqual(
            oai_record_acl.can_get_pid_for_data(**self.mock_kwargs),
            self.mock_kwargs["func"](
                self.mock_kwargs["oai_record_id"], self.mock_kwargs["request"]
            ),
        )
