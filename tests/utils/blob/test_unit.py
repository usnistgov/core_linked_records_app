""" Unit tests for core_linked_records_app.utils.blob
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.utils import blob as blob_utils


class TestGetBlobDownloadRegex(TestCase):
    """Test Get Blob Download Regex"""

    @patch.object(blob_utils, "blob_system_api")
    @patch.object(blob_utils, "local_id_system_api")
    @patch.object(blob_utils, "re")
    @patch.object(blob_utils, "reverse")
    def test_reverse_called(
        self,
        mock_reverse,
        mock_regex_module,  # noqa, pylint: disable=unused-argument
        mock_local_id_system_api,  # noqa, pylint: disable=unused-argument
        mock_blob_system_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_reverse_called"""
        blob_utils.get_blob_download_regex("mock_xml_string")

        mock_reverse.assert_called_with(
            "core_linked_records_provider_record",
            kwargs={"provider": "mock_string", "record": "mock_string"},
        )

    @patch.object(blob_utils, "blob_system_api")
    @patch.object(blob_utils, "local_id_system_api")
    @patch.object(blob_utils, "re")
    @patch.object(blob_utils, "reverse")
    def test_local_id_get_by_name_called(
        self,
        mock_reverse,  # noqa, pylint: disable=unused-argument
        mock_regex_module,
        mock_local_id_system_api,
        mock_blob_system_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_local_id_get_by_name_called"""
        mock_regex_module.findall.return_value = [MagicMock()]

        blob_utils.get_blob_download_regex("mock_xml_string")

        mock_local_id_system_api.get_by_name.assert_called()

    @patch.object(blob_utils, "blob_system_api")
    @patch.object(blob_utils, "local_id_system_api")
    @patch.object(blob_utils, "re")
    @patch.object(blob_utils, "reverse")
    @patch.object(blob_utils, "logger")
    def test_local_id_get_by_name_error_is_logged(
        self,
        mock_logger,
        mock_reverse,  # noqa, pylint: disable=unused-argument
        mock_regex_module,
        mock_local_id_system_api,
        mock_blob_system_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_local_id_get_by_name_error_is_logged"""
        mock_regex_module.findall.return_value = [MagicMock()]
        mock_local_id_system_api.get_by_name.side_effect = Exception(
            "mock_get_by_name_exception"
        )

        blob_utils.get_blob_download_regex("mock_xml_string")
        mock_logger.warning.assert_called()

    @patch.object(blob_utils, "blob_system_api")
    @patch.object(blob_utils, "local_id_system_api")
    @patch.object(blob_utils, "re")
    @patch.object(blob_utils, "reverse")
    def test_get_pid_for_blob_called(
        self,
        mock_reverse,  # noqa, pylint: disable=unused-argument
        mock_regex_module,
        mock_local_id_system_api,
        mock_blob_system_api,
    ):
        """test_get_pid_for_blob_called"""
        mock_record_object = MagicMock()
        mock_regex_module.findall.return_value = [MagicMock()]
        mock_local_id_system_api.get_by_name.return_value = mock_record_object

        blob_utils.get_blob_download_regex("mock_xml_string")
        mock_blob_system_api.get_pid_for_blob.assert_called_with(
            mock_record_object.record_object_id
        )

    @patch.object(blob_utils, "blob_system_api")
    @patch.object(blob_utils, "local_id_system_api")
    @patch.object(blob_utils, "re")
    @patch.object(blob_utils, "reverse")
    @patch.object(blob_utils, "logger")
    def test_get_pid_for_blob_error_is_logged(
        self,
        mock_logger,
        mock_reverse,  # noqa, pylint: disable=unused-argument
        mock_regex_module,
        mock_local_id_system_api,  # noqa, pylint: disable=unused-argument
        mock_blob_system_api,
    ):
        """test_get_pid_for_blob_error_is_logged"""
        mock_regex_module.findall.return_value = [MagicMock()]
        mock_blob_system_api.get_pid_for_blob.side_effect = Exception(
            "mock_get_pid_for_blob_exception"
        )

        blob_utils.get_blob_download_regex("mock_xml_string")
        mock_logger.warning.assert_called()

    @patch.object(blob_utils, "blob_system_api")
    @patch.object(blob_utils, "local_id_system_api")
    @patch.object(blob_utils, "re")
    @patch.object(blob_utils, "reverse")
    def test_successful_execution_returns_blob_url_list(
        self,
        mock_reverse,  # noqa, pylint: disable=unused-argument
        mock_regex_module,
        mock_local_id_system_api,  # noqa, pylint: disable=unused-argument
        mock_blob_system_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_successful_execution_returns_blob_url_list"""
        mock_document_list = [MagicMock()]
        mock_regex_module.findall.return_value = mock_document_list

        self.assertEqual(
            blob_utils.get_blob_download_regex("mock_xml_string"),
            mock_document_list,
        )
