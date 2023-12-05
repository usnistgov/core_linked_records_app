""" Unit tests for core_linked_records_app.components.blob.api
"""
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.system.blob import api as blob_system_api
from core_linked_records_app.system.local_id import api as local_id_system_api
from core_linked_records_app.utils.path import get_api_path_from_object
from core_main_app.commons import exceptions
from core_main_app.components.blob.models import Blob
from tests import mocks


class TestGetPidForBlob(TestCase):
    """Test Get Pid For Blob"""

    @patch.object(blob_system_api, "get_api_path_from_object")
    def test_get_api_path_from_object_exception_raises_api_error(
        self, mock_get_api_path_from_object
    ):
        """test_get_api_path_from_object_exception_raises_api_error"""

        mock_get_api_path_from_object.side_effect = Exception(
            "mock_get_api_path_from_object_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.get_pid_for_blob("mock_blob_id")

    @patch.object(local_id_system_api, "get_by_class_and_id")
    @patch.object(blob_system_api, "get_api_path_from_object")
    def test_get_by_class_and_id_exception_raises_api_error(
        self, mock_get_api_path_from_object, mock_get_by_class_and_id
    ):
        """test_get_by_class_and_id_exception_raises_api_error"""

        mock_get_api_path_from_object.return_value = ""
        mock_get_by_class_and_id.side_effect = Exception(
            "mock_get_by_class_and_id_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.get_pid_for_blob("mock_blob_id")

    @patch.object(local_id_system_api, "get_by_class_and_id")
    @patch.object(blob_system_api, "get_api_path_from_object")
    def test_get_by_class_and_id_does_not_exist_raises_does_not_exists_error(
        self, mock_get_api_path_from_object, mock_get_by_class_and_id
    ):
        """test_get_by_class_and_id_does_not_exist_raises_does_not_exists_error"""
        mock_get_api_path_from_object.return_value = ""
        mock_get_by_class_and_id.side_effect = exceptions.DoesNotExist(
            "mock_get_by_class_and_id_does_not_exist"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            blob_system_api.get_pid_for_blob("mock_blob_id")

    @patch.object(local_id_system_api, "get_by_class_and_id")
    @patch.object(blob_system_api, "get_api_path_from_object")
    def test_returns_get_by_class_and_id_output(
        self, mock_get_api_path_from_object, mock_get_by_class_and_id
    ):
        """test_returns_get_by_class_and_id_output"""

        mock_pid_value = "mock_pid_value"
        mock_get_api_path_from_object.return_value = ""
        mock_get_by_class_and_id.return_value = mock_pid_value

        result = blob_system_api.get_pid_for_blob("mock_blob_id")
        self.assertEqual(result, mock_pid_value)


class TestSetPidForBlob(TestCase):
    """Test Set Pid For Blob"""

    @patch.object(blob_system_api, "get_pid_for_blob")
    def test_get_pid_for_blob_exception_raises_api_error(
        self, mock_get_pid_for_blob
    ):
        """test_get_pid_for_blob_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = Exception(
            "mock_get_pid_for_blob_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(blob_system_api, "get_pid_for_blob")
    def test_get_by_name_exception_raises_api_error(
        self, mock_get_pid_for_blob, mock_get_by_name
    ):
        """test_get_by_name_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_by_name.side_effect = Exception("mock_get_by_name_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(blob_system_api, "get_api_path_from_object")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(blob_system_api, "get_pid_for_blob")
    def test_new_local_id_get_api_path_from_object_exception_raises_api_error(
        self,
        mock_get_pid_for_blob,
        mock_get_by_name,
        mock_get_api_path_from_object,
    ):
        """test_new_local_id_get_api_path_from_object_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_api_path_from_object.side_effect = Exception(
            "mock_get_api_path_from_object_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(blob_system_api, "get_api_path_from_object")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(blob_system_api, "get_pid_for_blob")
    def test_edit_local_id_get_api_path_from_object_exception_raises_api_error(
        self,
        mock_get_pid_for_blob,
        mock_get_by_name,
        mock_get_api_path_from_object,
    ):
        """test_edit_local_id_get_api_path_from_object_exception_raises_api_error"""

        mock_blob_id = "mock_blob_id"
        mock_blob_pid = "mock_blob_pid"
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_by_name.return_value = mocks.MockLocalId()
        mock_get_api_path_from_object.side_effect = Exception(
            "mock_get_api_path_from_object_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_system_api, "insert")
    @patch.object(blob_system_api, "get_api_path_from_object")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(blob_system_api, "get_pid_for_blob")
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
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.side_effect = Exception("mock_side_effect_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_system_api, "insert")
    @patch.object(blob_system_api, "get_api_path_from_object")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(blob_system_api, "get_pid_for_blob")
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
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_by_name.return_value = mocks.MockLocalId()
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.side_effect = Exception("mock_side_effect_exception")

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)

    @patch.object(local_id_system_api, "insert")
    @patch.object(blob_system_api, "get_api_path_from_object")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(blob_system_api, "get_pid_for_blob")
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
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_by_name.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.return_value = mock_insert_result

        result = blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)
        self.assertEqual(result, mock_insert_result)

    @patch.object(local_id_system_api, "insert")
    @patch.object(blob_system_api, "get_api_path_from_object")
    @patch.object(local_id_system_api, "get_by_name")
    @patch.object(blob_system_api, "get_pid_for_blob")
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
        mock_get_pid_for_blob.side_effect = exceptions.DoesNotExist(
            "does_not_exist"
        )
        mock_get_by_name.return_value = mocks.MockLocalId()
        mock_get_api_path_from_object.return_value = "mock_api_path"
        mock_insert.return_value = mock_insert_result

        result = blob_system_api.set_pid_for_blob(mock_blob_id, mock_blob_pid)
        self.assertEqual(result, mock_insert_result)


class TestDeletePidForBlob(TestCase):
    """Test delete_pid_for_blob"""

    def setUp(self) -> None:
        self.blob = Mock(spec=Blob)

    @patch.object(blob_system_api, "delete_record_from_provider")
    @patch.object(local_id_system_api, "get_by_class_and_id")
    def test_get_by_class_and_id_called(
        self,
        mock_get_by_class_and_id,
        mock_delete_record_from_provider,  # noqa, pylint: disable=unused-argument
    ):
        """test_get_by_class_and_id_called"""
        blob_system_api.delete_pid_for_blob(self.blob)
        mock_get_by_class_and_id.assert_called_with(
            get_api_path_from_object(Blob()), self.blob.pk
        )

    @patch.object(blob_system_api, "logger")
    @patch.object(local_id_system_api, "get_by_class_and_id")
    def test_does_not_exist_is_logged(
        self, mock_get_by_class_and_id, mock_logger
    ):
        """test_does_not_exist_is_logged"""
        mock_get_by_class_and_id.side_effect = exceptions.DoesNotExist(
            "mock_get_by_class_and_id_does_not_exist"
        )

        blob_system_api.delete_pid_for_blob(self.blob)
        mock_logger.info.assert_called()

    @patch.object(blob_system_api, "delete_record_from_provider")
    @patch.object(local_id_system_api, "get_by_class_and_id")
    def test_delete_from_record_name_called(
        self, mock_get_by_class_and_id, mock_delete_record_from_provider
    ):
        """test_delete_from_record_name_called"""
        mock_local_id = Mock(spec=LocalId)
        mock_get_by_class_and_id.return_value = mock_local_id
        blob_system_api.delete_pid_for_blob(self.blob)
        mock_delete_record_from_provider.assert_called_with(
            mock_local_id.record_name
        )


class TestGetBlobByPid(TestCase):
    """Unit tests for `get_blob_by_pid` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"pid": MagicMock()}

    @patch.object(blob_system_api, "local_id_system_api")
    def test_get_by_name_called(self, mock_local_id_system_api):
        """test_get_by_name_called"""
        with self.assertRaises(exceptions.ApiError):
            blob_system_api.get_blob_by_pid(**self.mock_kwargs)

        mock_local_id_system_api.get_by_name.assert_called_with(
            "/".join(self.mock_kwargs["pid"].split("/")[-2:])
        )

    @patch.object(blob_system_api, "local_id_system_api")
    def test_get_by_name_exception_raises_api_error(
        self, mock_local_id_system_api
    ):
        """test_get_by_name_exception_raises_api_error"""
        mock_local_id_system_api.get_by_name.side_effect = Exception(
            "mock_local_id_system_api_get_by_name_exception"
        )

        with self.assertRaises(exceptions.ApiError):
            blob_system_api.get_blob_by_pid(**self.mock_kwargs)

    @patch.object(blob_system_api, "local_id_system_api")
    def test_local_id_object_empty_raises_does_not_exists_exception(
        self, mock_local_id_system_api
    ):
        """test_local_id_object_empty_raises_does_not_exists_exception"""
        mock_local_id_object = MagicMock()
        mock_local_id_object.record_object_class = None
        mock_local_id_object.record_object_id = None
        mock_local_id_system_api.get_by_name.return_value = (
            mock_local_id_object
        )

        with self.assertRaises(exceptions.DoesNotExist):
            blob_system_api.get_blob_by_pid(**self.mock_kwargs)

    @patch.object(blob_system_api, "blob_system_api")
    @patch.object(blob_system_api, "local_id_system_api")
    def test_get_by_id_called(
        self, mock_local_id_system_api, mock_blob_system_api
    ):
        """test_get_by_id_called"""
        mock_local_id_object_record_id = MagicMock()
        mock_local_id_object = MagicMock()
        mock_local_id_object.record_object_class = MagicMock()
        mock_local_id_object.record_object_id = mock_local_id_object_record_id
        mock_local_id_system_api.get_by_name.return_value = (
            mock_local_id_object
        )

        blob_system_api.get_blob_by_pid(**self.mock_kwargs)
        mock_blob_system_api.get_by_id.assert_called_with(
            mock_local_id_object_record_id
        )

    @patch.object(blob_system_api, "blob_system_api")
    @patch.object(blob_system_api, "local_id_system_api")
    def test_get_by_id_does_not_exists_raises_does_not_exist(
        self, mock_local_id_system_api, mock_blob_system_api
    ):
        """test_get_by_id_does_not_exists_raises_does_not_exist"""
        mock_local_id_system_api.get_by_name.return_value = MagicMock()
        mock_blob_system_api.get_by_id.side_effect = exceptions.DoesNotExist(
            "mock_get_by_id_exception"
        )

        with self.assertRaises(exceptions.DoesNotExist):
            blob_system_api.get_blob_by_pid(**self.mock_kwargs)

    @patch.object(blob_system_api, "blob_system_api")
    @patch.object(blob_system_api, "local_id_system_api")
    def test_successful_execution_returns_get_by_id(
        self, mock_local_id_system_api, mock_blob_system_api
    ):
        """test_successful_execution_returns_get_by_id"""
        mock_local_id_system_api.get_by_name.return_value = MagicMock()
        mock_blob = MagicMock()
        mock_blob_system_api.get_by_id.return_value = mock_blob

        self.assertEqual(
            blob_system_api.get_blob_by_pid(**self.mock_kwargs), mock_blob
        )
