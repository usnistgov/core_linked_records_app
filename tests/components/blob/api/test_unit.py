""" Unit tests for core_linked_records_app.components.blob.api
"""
from unittest import TestCase
from unittest.mock import patch

from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_linked_records_app.components.blob import api as blob_api
from core_linked_records_app.components.local_id import api as local_id_api
from core_linked_records_app.components.local_id.models import LocalId
from tests import mocks


class TestGetBlobByPid(TestCase):
    """Test Get Blob By Pid"""

    def setUp(self):
        """setUp"""
        self.user = create_mock_user("1")

    @patch.object(local_id_api, "get_by_name")
    def test_get_by_name_error_raises_api_error(self, mock_get_by_name):
        """test_get_by_name_error_raises_api_error"""

        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")
        mock_valid_pid = "https://websi.te/provider/record"

        with self.assertRaises(exceptions.ApiError):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(local_id_api, "get_by_name")
    def test_undefined_classpath_raises_does_not_exist(self, mock_get_by_name):
        """test_undefined_classpath_raises_does_not_exist"""

        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(record_name=mock_valid_pid)

        with self.assertRaises(exceptions.DoesNotExist):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(blob_api, "import_module")
    @patch.object(local_id_api, "get_by_name")
    def test_failed_import_raises_api_error(self, mock_get_by_name, mock_import_module):
        """test_failed_import_raises_api_error"""

        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(
            record_name=mock_valid_pid,
            record_object_class="mock_record_object_class",
            record_object_id="mock_record_object_id",
        )
        mock_import_module.side_effect = Exception("mock_import_module_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_api.get_blob_by_pid(mock_valid_pid, self.user)

    @patch.object(blob_api, "getattr")
    @patch.object(blob_api, "import_module")
    @patch.object(local_id_api, "get_by_name")
    def test_get_by_id_exception_raises_api_error(
        self, mock_get_by_name, mock_import_module, mock_getattr
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
    @patch.object(local_id_api, "get_by_name")
    def test_returns_expected_get_by_id_output(
        self, mock_get_by_name, mock_import_module, mock_getattr
    ):
        """test_returns_expected_get_by_id_output"""

        mock_valid_pid = "https://websi.te/provider/record"
        mock_get_by_name.return_value = LocalId(
            record_name=mock_valid_pid,
            record_object_class="mock_record_object_class",
            record_object_id="mock_record_object_id",
        )
        mock_import_module.return_value = None
        mock_getattr.return_value = mocks.MockModule()

        result = blob_api.get_blob_by_pid(mock_valid_pid, self.user)
        self.assertEqual(result, mocks.MockModule().get_by_id())


class TestGetPidForBlob(TestCase):
    """Test Get Pid For Blob"""

    @patch.object(blob_api, "get_api_path_from_object")
    def test_get_api_path_from_object_exception_raises_api_error(
        self, mock_get_api_path_from_object
    ):
        """test_get_api_path_from_object_exception_raises_api_error"""

        mock_get_api_path_from_object.side_effect = Exception(
            "mock_get_api_path_from_object_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_api.get_pid_for_blob("mock_blob_id")

    @patch.object(local_id_api, "get_by_class_and_id")
    @patch.object(blob_api, "get_api_path_from_object")
    def test_get_by_class_and_id_exception_raises_api_error(
        self, mock_get_api_path_from_object, mock_get_by_class_and_id
    ):
        """test_get_by_class_and_id_exception_raises_api_error"""

        mock_get_api_path_from_object.return_value = ""
        mock_get_by_class_and_id.side_effect = Exception(
            "mock_get_by_class_and_id_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_api.get_pid_for_blob("mock_blob_id")

    @patch.object(local_id_api, "get_by_class_and_id")
    @patch.object(blob_api, "get_api_path_from_object")
    def test_returns_get_by_class_and_id_output(
        self, mock_get_api_path_from_object, mock_get_by_class_and_id
    ):
        """test_returns_get_by_class_and_id_output"""

        mock_pid_value = "mock_pid_value"
        mock_get_api_path_from_object.return_value = ""
        mock_get_by_class_and_id.return_value = mock_pid_value

        result = blob_api.get_pid_for_blob("mock_blob_id")
        self.assertEqual(result, mock_pid_value)


class TestSetPidForBlob(TestCase):
    """Test Set Pid For Blob"""

    @patch.object(blob_api, "get_pid_for_blob")
    def test_get_pid_for_blob_exception_raises_api_error(self, mock_get_pid_for_blob):
        """test_get_pid_for_blob_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = Exception("mock_get_pid_for_blob_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_api, "get_by_name")
    @patch.object(blob_api, "get_pid_for_blob")
    def test_get_by_name_exception_raises_api_error(
        self, mock_get_pid_for_blob, mock_get_by_name
    ):
        """test_get_by_name_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(blob_api, "get_api_path_from_object")
    @patch.object(local_id_api, "get_by_name")
    @patch.object(blob_api, "get_pid_for_blob")
    def test_new_local_id_get_api_path_from_object_exception_raises_api_error(
        self, mock_get_pid_for_blob, mock_get_by_name, mock_get_api_path_from_object
    ):
        """test_new_local_id_get_api_path_from_object_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_by_name.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_api_path_from_object.side_effect = Exception(
            "mock_get_api_path_from_object_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(blob_api, "get_api_path_from_object")
    @patch.object(local_id_api, "get_by_name")
    @patch.object(blob_api, "get_pid_for_blob")
    def test_edit_local_id_get_api_path_from_object_exception_raises_api_error(
        self, mock_get_pid_for_blob, mock_get_by_name, mock_get_api_path_from_object
    ):
        """test_edit_local_id_get_api_path_from_object_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_by_name.return_value = mocks.MockLocalId()
        mock_get_api_path_from_object.side_effect = Exception(
            "mock_get_api_path_from_object_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_api, "insert")
    @patch.object(blob_api, "get_api_path_from_object")
    @patch.object(local_id_api, "get_by_name")
    @patch.object(blob_api, "get_pid_for_blob")
    def test_new_local_id_insert_exception_raises_api_error(
        self,
        mock_get_pid_for_blob,
        mock_get_by_name,
        mock_get_api_path_from_object,
        mock_insert,
    ):
        """test_new_local_id_insert_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_by_name.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.side_effect = Exception("mock_side_effect_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_api, "insert")
    @patch.object(blob_api, "get_api_path_from_object")
    @patch.object(local_id_api, "get_by_name")
    @patch.object(blob_api, "get_pid_for_blob")
    def test_edit_local_id_insert_exception_raises_api_error(
        self,
        mock_get_pid_for_blob,
        mock_get_by_name,
        mock_get_api_path_from_object,
        mock_insert,
    ):
        """test_edit_local_id_insert_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_by_name.return_value = mocks.MockLocalId()
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.side_effect = Exception("mock_side_effect_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_api, "insert")
    @patch.object(blob_api, "get_api_path_from_object")
    @patch.object(local_id_api, "get_by_name")
    @patch.object(blob_api, "get_pid_for_blob")
    def test_new_local_id_returns_insert_output(
        self,
        mock_get_pid_for_blob,
        mock_get_by_name,
        mock_get_api_path_from_object,
        mock_insert,
    ):
        """test_new_local_id_returns_insert_output"""

        mock_insert_result = "mock_local_id_object"
        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_by_name.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.return_value = mock_insert_result

        result = blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)
        self.assertEqual(result, mock_insert_result)

    @patch.object(local_id_api, "insert")
    @patch.object(blob_api, "get_api_path_from_object")
    @patch.object(local_id_api, "get_by_name")
    @patch.object(blob_api, "get_pid_for_blob")
    def test_edit_local_id_returns_insert_output(
        self,
        mock_get_pid_for_blob,
        mock_get_by_name,
        mock_get_api_path_from_object,
        mock_insert,
    ):
        """test_edit_local_id_returns_insert_output"""

        mock_insert_result = "mock_local_id_object"
        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist("does_not_exist")
        mock_get_by_name.return_value = mocks.MockLocalId()
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.return_value = mock_insert_result

        result = blob_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)
        self.assertEqual(result, mock_insert_result)
