""" Unit tests for core_linked_records_app.system.data.api
"""
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from django.test import tag, override_settings

from core_linked_records_app.system.data import api as data_system_api
from core_linked_records_app.utils.providers import AbstractIdProvider
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.data.models import Data


class TestIsPidDefinedForDataPsql(TestCase):
    """Test Is Pid Defined For Document"""

    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_wrong_document_id_raise_error(self, mock_data_get_by_id):
        """test_wrong_document_id_raise_error"""
        mock_data_get_by_id.side_effect = DoesNotExist("mock_does_not_exist")

        with self.assertRaises(Exception):
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.data.api.Data.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_undefined_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_undefined_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = []

        self.assertFalse(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.data.api.Data.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_duplicate_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_duplicate_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = [MagicMock(), MagicMock()]

        self.assertFalse(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.data.api.Data.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_defined_pid_for_other_document_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_other_document_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id_other"
        mock_data_execute_query.return_value = [mock_result]

        self.assertFalse(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.data.api.Data.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_defined_pid_for_current_document_returns_true(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_current_document_returns_true"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id"
        mock_data_execute_query.return_value = [mock_result]

        self.assertTrue(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )


class TestIsPidDefinedForDataMongo(TestCase):
    """Test Is Pid Defined For Document"""

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_undefined_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_undefined_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = []

        self.assertFalse(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_duplicate_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_duplicate_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = [MagicMock(), MagicMock()]

        self.assertFalse(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_defined_pid_for_other_document_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_other_document_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id_other"
        mock_data_execute_query.return_value = [mock_result]

        self.assertFalse(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    @patch("core_linked_records_app.system.data.api.Data.get_by_id")
    def test_defined_pid_for_current_document_returns_true(
        self,
        mock_data_get_by_id,
        mock_get_pid_path_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_current_document_returns_true"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_path_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id"
        mock_data_execute_query.return_value = [mock_result]

        self.assertTrue(
            data_system_api.is_pid_defined_for_data(
                "mock_pid", "mock_document_id"
            )
        )


class TestGetDataByPidPsql(TestCase):
    """Test Get Data By Pid"""

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.data.api.Data.execute_query")
    @patch("core_linked_records_app.system.data.api.PidPath.get_all")
    def test_query_returns_no_results_raises_error(
        self, mock_pid_path_get_all, mock_execute_query
    ):
        """test_query_returns_no_results_raises_error"""
        mock_pid_path_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 0
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(DoesNotExist):
            data_system_api.get_data_by_pid("mock_pid")

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.data.api.Data.execute_query")
    @patch("core_linked_records_app.system.data.api.PidPath.get_all")
    def test_query_returns_several_results_raises_error(
        self, mock_pid_path_get_all, mock_execute_query
    ):
        """test_query_returns_several_results_raises_error"""
        mock_pid_path_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 2
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(ApiError):
            data_system_api.get_data_by_pid("mock_pid")

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.data.api.Data.execute_query")
    @patch("core_linked_records_app.system.data.api.PidPath.get_all")
    def test_query_returns_single_result_returns_result(
        self, mock_pid_path_get_all, mock_execute_query
    ):
        """test_query_returns_single_result_returns_result"""
        mock_pid_path_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__getitem__.return_value = "mock_data"
        mock_execute_query.return_value = mock_queryset

        self.assertEqual(
            data_system_api.get_data_by_pid("mock_pid"), "mock_data"
        )


class TestGetDataByPidMongo(TestCase):
    """Test Get Data By Pid"""

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.data.api.PidPath.get_all")
    def test_query_returns_no_results_raises_error(
        self, mock_pid_path_get_all, mock_execute_query
    ):
        """test_query_returns_no_results_raises_error"""
        mock_pid_path_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 0
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(DoesNotExist):
            data_system_api.get_data_by_pid("mock_pid")

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.data.api.PidPath.get_all")
    def test_query_returns_several_results_raises_error(
        self, mock_pid_path_get_all, mock_execute_query
    ):
        """test_query_returns_several_results_raises_error"""
        mock_pid_path_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 2
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(ApiError):
            data_system_api.get_data_by_pid("mock_pid")

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.data.api.PidPath.get_all")
    def test_query_returns_single_result_returns_result(
        self, mock_pid_path_get_all, mock_execute_query
    ):
        """test_query_returns_single_result_returns_result"""
        mock_pid_path_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__getitem__.return_value = "mock_data"
        mock_execute_query.return_value = mock_queryset

        self.assertEqual(
            data_system_api.get_data_by_pid("mock_pid"), "mock_data"
        )


class TestDeletePidForData(TestCase):
    """Test delete_pid_for_data"""

    @classmethod
    def setUpClass(cls) -> None:
        mock_data = Mock(spec=Data)
        mock_data.pk = "mock_pk"

        cls.mock_data = mock_data
        cls.mock_provider = Mock(spec=AbstractIdProvider)

    @patch.object(data_system_api, "delete_record_from_provider")
    @patch(
        "core_linked_records_app.system.data.api.get_value_from_dot_notation"
    )
    @patch("core_linked_records_app.system.data.api.xml_utils.raw_xml_to_dict")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    def test_get_dict_content_failure_calls_raw_xml_to_dict_utils(
        self,
        mock_get_pid_path_by_template,  # noqa, pylint: disable=unused-argument
        mock_raw_xml_to_dict,
        mock_get_value_from_dot_notation,
        mock_delete_record_from_provider,  # noqa, pylint: disable=unused-argument
    ):
        """test_get_dict_content_failure_calls_raw_xml_to_dict_utils"""
        self.mock_data.get_dict_content.side_effect = Exception(
            "mock_get_dict_content_exception"
        )
        mock_get_value_from_dot_notation.return_value = None

        data_system_api.delete_pid_for_data(self.mock_data)
        mock_raw_xml_to_dict.assert_called()

    @patch.object(data_system_api, "delete_record_from_provider")
    @patch(
        "core_linked_records_app.system.data.api.get_value_from_dot_notation"
    )
    @patch("core_linked_records_app.system.data.api.xml_utils.raw_xml_to_dict")
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    def test_raw_xml_to_dict_failure_raises_api_error(
        self,
        mock_get_pid_path_by_template,  # noqa, pylint: disable=unused-argument
        mock_raw_xml_to_dict,
        mock_get_value_from_dot_notation,
        mock_delete_record_from_provider,  # noqa, pylint: disable=unused-argument
    ):
        """test_raw_xml_to_dict_failure_raises_api_error"""
        self.mock_data.get_dict_content.side_effect = Exception(
            "mock_get_dict_content_exception"
        )
        mock_raw_xml_to_dict.side_effect = Exception(
            "mock_raw_xml_to_dict_exception"
        )
        mock_get_value_from_dot_notation.return_value = None

        with self.assertRaises(ApiError):
            data_system_api.delete_pid_for_data(self.mock_data)

    @patch.object(data_system_api, "delete_record_from_provider")
    @patch(
        "core_linked_records_app.system.data.api.get_value_from_dot_notation"
    )
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    def test_empty_pid_is_not_deleted(
        self,
        mock_get_pid_path_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_delete_record_from_provider,
    ):
        """test_empty_pid_is_not_deleted"""
        mock_get_value_from_dot_notation.return_value = None

        data_system_api.delete_pid_for_data(self.mock_data)
        mock_delete_record_from_provider.assert_not_called()

    @patch.object(data_system_api, "delete_record_from_provider")
    @patch(
        "core_linked_records_app.system.data.api.get_value_from_dot_notation"
    )
    @patch("core_linked_records_app.system.data.api.get_pid_path_by_template")
    def test_delete_pid_from_record_called_when_pid_exists(
        self,
        mock_get_pid_path_by_template,  # noqa, pylint: disable=unused-argument
        mock_get_value_from_dot_notation,
        mock_delete_record_from_provider,
    ):
        """test_delete_pid_from_record_called"""
        mock_pid = "mock_pid"
        mock_get_value_from_dot_notation.return_value = mock_pid

        data_system_api.delete_pid_for_data(self.mock_data)
        mock_delete_record_from_provider.assert_called_with(mock_pid)
