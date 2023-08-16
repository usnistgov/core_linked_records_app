""" Unit tests for `core_linked_records_app.components.blob.api`.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.blob import access_control as blob_acl
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.system.local_id import api as local_id_system_api
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests import mocks


class TestGetBlobByPid(TestCase):
    """Unit tests for `get_blob_by_pid` function."""

    def setUp(self):
        """setUp"""
        self.user = create_mock_user("1")

    @patch.object(local_id_system_api, "get_by_name")
    def test_get_by_name_error_raises_api_error(self, mock_get_by_name):
        """test_get_by_name_error_raises_api_error"""

        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")
        mock_valid_pid = "https://websi.te/provider/record"

        with self.assertRaises(exceptions.ApiError):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(local_id_system_api, "get_by_name")
    def test_undefined_classpath_raises_does_not_exist(self, mock_get_by_name):
        """test_undefined_classpath_raises_does_not_exist"""

        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(record_name=mock_valid_pid)

        with self.assertRaises(exceptions.DoesNotExist):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    def test_failed_import_raises_api_error(
        self,
        mock_get_by_name,
        mock_import_module,
    ):
        """test_failed_import_raises_api_error"""
        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(
            record_name=mock_valid_pid,
            record_object_class="mock_record_object_class",
            record_object_id="mock_record_object_id",
        )
        mock_import_module.side_effect = Exception(
            "mock_import_module_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    def test_get_by_id_exception_raises_api_error(
        self,
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_get_by_id_exception_raises_api_error"""
        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(
            record_name=mock_valid_pid,
            record_object_class="mock_record_object_class",
            record_object_id="mock_record_object_id",
        )
        mock_import_module.return_value = None
        mock_getattr.side_effect = Exception("mock_getattr_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    def test_get_by_id_acl_error_raises_acl_error(
        self,
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_get_by_id_acl_error_raises_acl_error"""
        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(
            record_name=mock_valid_pid,
            record_object_class="mock_record_object_class",
            record_object_id="mock_record_object_id",
        )
        mock_import_module.return_value = None
        mock_getattr.side_effect = AccessControlError(
            "mock_getattr_access_control_error"
        )

        with self.assertRaises(AccessControlError):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_system_api, "get_by_name")
    def test_returns_expected_get_by_id_output(
        self,
        mock_get_by_name,
        mock_import_module,
        mock_getattr,
    ):
        """test_returns_expected_get_by_id_output"""
        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(
            record_name=mock_valid_pid,
            record_object_class="mock_record_object_class",
            record_object_id="mock_record_object_id",
        )
        mock_import_module.return_value = None

        mock_blob = mocks.MockDocument()
        mock_blob.user_id = self.user.id
        mock_blob_module = mocks.MockModule()
        mock_blob_module.get_by_id_return_value = mock_blob
        mock_getattr.return_value = mock_blob_module

        result = blob_api.get_blob_by_pid(mock_valid_pid, self.user)
        self.assertEqual(result, mock_blob)


class TestGetPidForBlob(TestCase):
    """Unit tests for `get_pid_for_blob` function."""

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_get_pid_for_blob_called(
        self,
        mock_blob,
        mock_check_can_read_document,
        mock_blob_system_api,
    ):
        """test_get_pid_for_blob_called"""
        mock_blob_id = "mock_blob_id"
        mock_blob.get_by_id.return_value = MagicMock()
        mock_check_can_read_document.return_value = True

        blob_api.get_pid_for_blob(mock_blob_id, create_mock_user("1"))
        mock_blob_system_api.get_pid_for_blob.assert_called_with(mock_blob_id)

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_success_returns_system_get_pid_for_blob_output(
        self,
        mock_blob,
        mock_check_can_read_document,
        mock_blob_system_api,
    ):
        """test_success_returns_system_get_pid_for_blob_output"""
        mock_blob_id = "mock_blob_id"
        mock_blob.get_by_id.return_value = MagicMock()
        mock_check_can_read_document.return_value = True

        expected_result = "mock_blob_pid"
        mock_blob_system_api.get_pid_for_blob.return_value = expected_result

        self.assertEqual(
            blob_api.get_pid_for_blob(mock_blob_id, create_mock_user("1")),
            expected_result,
        )


class TestSetPidForBlob(TestCase):
    """Unit tests for `set_pid_for_blob` function."""

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_set_pid_for_blob_called(
        self,
        mock_blob,
        mock_check_can_read_document,
        mock_blob_system_api,
    ):
        """test_set_pid_for_blob_called"""
        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_blob.get_by_id.return_value = MagicMock()
        mock_check_can_read_document.return_value = True

        blob_api.set_pid_for_blob(
            mock_blob_id, mock_blob_pid, create_mock_user("1")
        )
        mock_blob_system_api.set_pid_for_blob.assert_called_with(
            mock_blob_id, mock_blob_pid
        )

    @patch.object(blob_api, "blob_system_api")
    @patch.object(blob_acl, "check_can_read_document")
    @patch.object(blob_acl, "Blob")
    def test_success_returns_system_set_pid_for_blob_output(
        self,
        mock_blob,
        mock_check_can_read_document,
        mock_blob_system_api,
    ):
        """test_success_returns_system_set_pid_for_blob_output"""
        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_blob.get_by_id.return_value = MagicMock()
        mock_check_can_read_document.return_value = True

        expected_results = "mock_blob_pid"
        mock_blob_system_api.set_pid_for_blob.return_value = expected_results

        self.assertEqual(
            blob_api.set_pid_for_blob(
                mock_blob_id, mock_blob_pid, create_mock_user("1")
            ),
            expected_results,
        )
