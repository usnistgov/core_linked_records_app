""" Unit tests for `core_linked_records.components.data.access_control`.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_linked_records_app.components.data import access_control as data_acl
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCanGetDataByPid(TestCase):
    """Unit tests for `can_get_data_by_pid` function."""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MagicMock()
        mock_request.user = create_mock_user("1")

        self.mock_kwargs = {
            "func": MagicMock(),
            "pid": "mock_pid",
            "request": mock_request,
        }

    @patch.object(data_acl, "check_can_read_document")
    def test_func_with_args_called(
        self,
        mock_check_can_read_document,  # noqa, pylint: disable=unused-argument
    ):
        """test_func_with_args_called"""
        data_acl.can_get_data_by_pid(**self.mock_kwargs)

        self.mock_kwargs["func"].assert_called_with(
            self.mock_kwargs["pid"],
            self.mock_kwargs["request"],
        )

    @patch.object(data_acl, "check_can_read_document")
    def test_check_can_read_document_not_called_for_superuser(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_not_called_for_superuser"""
        self.mock_kwargs["request"].user = create_mock_user(
            "1", is_superuser=True
        )
        data_acl.can_get_data_by_pid(**self.mock_kwargs)

        mock_check_can_read_document.assert_not_called()

    @patch.object(data_acl, "check_can_read_document")
    def test_check_can_read_document_called(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_called"""
        data_acl.can_get_data_by_pid(**self.mock_kwargs)

        mock_check_can_read_document.assert_called_with(
            self.mock_kwargs["func"](
                self.mock_kwargs["pid"],
                self.mock_kwargs["request"],
            ),
            self.mock_kwargs["request"].user,
        )

    @patch.object(data_acl, "check_can_read_document")
    def test_check_can_read_document_acl_error_fails(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_called"""
        mock_check_can_read_document.side_effect = AccessControlError(
            "mock_check_can_read_document_acl_error"
        )

        with self.assertRaises(AccessControlError):
            data_acl.can_get_data_by_pid(**self.mock_kwargs)

    @patch.object(data_acl, "check_can_read_document")
    def test_succesful_operation_returns_data(
        self,
        mock_check_can_read_document,  # noqa, pylint: disable=unused-argument
    ):
        """test_succesful_operation_returns_data"""
        self.assertEqual(
            data_acl.can_get_data_by_pid(**self.mock_kwargs),
            self.mock_kwargs["func"](
                self.mock_kwargs["pid"],
                self.mock_kwargs["request"],
            ),
        )


class TestCanGetPidForData(TestCase):
    """Unit tests for `can_get_pid_for_data` function."""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MagicMock()
        mock_request.user = create_mock_user("1")

        self.mock_kwargs = {
            "func": MagicMock(),
            "data_id": "mock_data_id",
            "request": mock_request,
        }

    @patch.object(data_acl, "check_can_read_document")
    @patch.object(data_acl, "Data")
    def test_check_can_read_document_called(
        self,
        mock_data,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_called"""
        mock_data_object = MagicMock()

        mock_data.get_by_id.return_value = mock_data_object
        data_acl.can_get_pid_for_data(**self.mock_kwargs)

        mock_check_can_read_document.assert_called_with(
            mock_data_object, self.mock_kwargs["request"].user
        )

    @patch.object(data_acl, "check_can_read_document")
    def test_check_can_read_document_not_called_for_superuser(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_not_called_for_superuser"""
        self.mock_kwargs["request"].user = create_mock_user(
            "1", is_superuser=True
        )
        data_acl.can_get_pid_for_data(**self.mock_kwargs)

        mock_check_can_read_document.assert_not_called()

    @patch.object(data_acl, "check_can_read_document")
    @patch.object(data_acl, "Data")
    def test_check_can_read_document_acl_error_fails(
        self,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_called"""
        mock_check_can_read_document.side_effect = AccessControlError(
            "mock_check_can_read_document_acl_error"
        )

        with self.assertRaises(AccessControlError):
            data_acl.can_get_pid_for_data(**self.mock_kwargs)

    @patch.object(data_acl, "check_can_read_document")
    @patch.object(data_acl, "Data")
    def test_succesful_operation_returns_func_with_args(
        self,
        mock_data,  # noqa, pylint: disable=unused-argument
        mock_check_can_read_document,  # noqa, pylint: disable=unused-argument
    ):
        """test_succesful_operation_returns_func_with_args"""
        self.assertEqual(
            data_acl.can_get_pid_for_data(**self.mock_kwargs),
            self.mock_kwargs["func"](
                self.mock_kwargs["data_id"],
                self.mock_kwargs["request"],
            ),
        )
