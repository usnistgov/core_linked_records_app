""" Unit tests for `core_linked_records.components.blob.access_control`.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_linked_records_app.components.blob import access_control as blob_acl
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCanGetBlobByPid(TestCase):
    """Unit tests for `can_get_blob_by_pid` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_func = MagicMock()
        self.mock_func_retval = "mock_blob"

        self.mock_func.return_value = self.mock_func_retval
        self.mock_kwargs = {
            "func": self.mock_func,
            "pid": "mock_pid_value",
            "user": create_mock_user("1"),
        }

    @patch.object(blob_acl, "check_can_read_document")
    def test_input_function_called(
        self,
        mock_check_can_read_document,  # noqa, pylint: disable=unused-argument
    ):
        """test_input_function_called"""
        blob_acl.can_get_blob_by_pid(**self.mock_kwargs)
        self.mock_func.assert_called_with(
            self.mock_kwargs["pid"], self.mock_kwargs["user"]
        )

    @patch.object(blob_acl, "check_can_read_document")
    def test_check_can_read_document_not_called_for_superuser(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_not_called_for_superuser"""
        self.mock_kwargs["user"] = create_mock_user("1", is_superuser=True)
        blob_acl.can_get_blob_by_pid(**self.mock_kwargs)
        mock_check_can_read_document.assert_not_called()

    @patch.object(blob_acl, "check_can_read_document")
    def test_check_can_read_document_called(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_called"""
        blob_acl.can_get_blob_by_pid(**self.mock_kwargs)
        mock_check_can_read_document.assert_called_with(
            self.mock_func_retval, self.mock_kwargs["user"]
        )

    @patch.object(blob_acl, "check_can_read_document")
    def test_check_can_read_document_exception_fails(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_exception_fails"""
        mock_check_can_read_document.side_effect = AccessControlError(
            "mock_check_can_read_document_acl_error"
        )

        with self.assertRaises(AccessControlError):
            blob_acl.can_get_blob_by_pid(**self.mock_kwargs)

    @patch.object(blob_acl, "check_can_read_document")
    def test_success_returns_function_output(
        self,
        mock_check_can_read_document,  # noqa, pylint: disable=unused-argument
    ):
        """test_success_returns_function_output"""
        self.assertEqual(
            blob_acl.can_get_blob_by_pid(**self.mock_kwargs),
            self.mock_func_retval,
        )


class TestCanGetPidForBlob(TestCase):
    """Unit tests for `can_get_pid_for_blob` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_blob_object = "mock_blob_object"
        self.mock_func_retval = "mock_func_retval"

        mock_func = MagicMock()
        mock_func.return_value = self.mock_func_retval

        self.mock_kwargs = {
            "func": mock_func,
            "blob_id": "mock_blob_id",
            "user": create_mock_user("1"),
        }

    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_check_can_read_document_called(
        self,
        mock_blob,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_called"""
        mock_blob.get_by_id.return_value = self.mock_blob_object
        blob_acl.can_get_pid_for_blob(**self.mock_kwargs)
        mock_check_can_read_document.assert_called_with(
            self.mock_blob_object, self.mock_kwargs["user"]
        )

    @patch.object(blob_acl, "check_can_read_document")
    def test_check_can_read_document_not_called_for_superuser(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_not_called_for_superuser"""
        self.mock_kwargs["user"] = create_mock_user("1", is_superuser=True)
        blob_acl.can_get_pid_for_blob(**self.mock_kwargs)
        mock_check_can_read_document.assert_not_called()

    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_check_can_read_document_exception_fails(
        self,
        mock_blob,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_exception_fails"""
        mock_blob.get_by_id.return_value = self.mock_blob_object
        mock_check_can_read_document.side_effect = AccessControlError(
            "mock_check_can_read_document_acl_error"
        )

        with self.assertRaises(AccessControlError):
            blob_acl.can_get_pid_for_blob(**self.mock_kwargs)

    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_success_returns_function_output(
        self,
        mock_blob,
        mock_check_can_read_document,  # noqa, pylint: disable=unused-argument
    ):
        """test_success_returns_function_output"""
        mock_blob.get_by_id.return_value = self.mock_blob_object

        self.assertEqual(
            blob_acl.can_get_pid_for_blob(**self.mock_kwargs),
            self.mock_func_retval,
        )
        self.mock_kwargs["func"].assert_called_with(
            self.mock_kwargs["blob_id"], self.mock_kwargs["user"]
        )


class TestCanSetPidForBlob(TestCase):
    """Unit tests for `can_set_pid_for_blob` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_blob_object = "mock_blob_object"
        self.mock_func_retval = "mock_func_retval"

        mock_func = MagicMock()
        mock_func.return_value = self.mock_func_retval

        self.mock_kwargs = {
            "func": mock_func,
            "blob_id": "mock_blob_id",
            "blob_pid": "mock_blob_pid",
            "user": create_mock_user("1"),
        }

    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_check_can_read_document_called(
        self,
        mock_blob,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_called"""
        mock_blob.get_by_id.return_value = self.mock_blob_object
        blob_acl.can_set_pid_for_blob(**self.mock_kwargs)
        mock_check_can_read_document.assert_called_with(
            self.mock_blob_object, self.mock_kwargs["user"]
        )

    @patch.object(blob_acl, "check_can_read_document")
    def test_check_can_read_document_not_called_for_superuser(
        self,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_not_called_for_superuser"""
        self.mock_kwargs["user"] = create_mock_user("1", is_superuser=True)
        blob_acl.can_set_pid_for_blob(**self.mock_kwargs)
        mock_check_can_read_document.assert_not_called()

    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_check_can_read_document_exception_fails(
        self,
        mock_blob,
        mock_check_can_read_document,
    ):
        """test_check_can_read_document_exception_fails"""
        mock_blob.get_by_id.return_value = self.mock_blob_object
        mock_check_can_read_document.side_effect = AccessControlError(
            "mock_check_can_read_document_acl_error"
        )

        with self.assertRaises(AccessControlError):
            blob_acl.can_set_pid_for_blob(**self.mock_kwargs)

    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_success_returns_function_output(
        self,
        mock_blob,
        mock_check_can_read_document,  # noqa, pylint: disable=unused-argument
    ):
        """test_success_returns_function_output"""
        mock_blob.get_by_id.return_value = self.mock_blob_object

        self.assertEqual(
            blob_acl.can_set_pid_for_blob(**self.mock_kwargs),
            self.mock_func_retval,
        )
        self.mock_kwargs["func"].assert_called_with(
            self.mock_kwargs["blob_id"],
            self.mock_kwargs["blob_pid"],
            self.mock_kwargs["user"],
        )
