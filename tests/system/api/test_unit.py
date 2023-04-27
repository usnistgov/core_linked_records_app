""" Unit tests for core_linked_records_app.system.api
"""
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from django.test import tag, override_settings

from core_linked_records_app.components.local_id.models import LocalId
from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_linked_records_app.components.local_id import api as local_id_api
from core_linked_records_app.system import api as system_api
from core_linked_records_app.utils.path import get_api_path_from_object
from core_linked_records_app.utils.providers import AbstractIdProvider
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.blob.models import Blob
from core_main_app.components.data.models import Data
from tests.mocks import MockResponse


class TestIsPidDefinedForDocumentPsql(TestCase):
    """Test Is Pid Defined For Document"""

    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_wrong_document_id_raise_error(self, mock_data_get_by_id):
        """test_wrong_document_id_raise_error"""
        mock_data_get_by_id.side_effect = DoesNotExist("mock_does_not_exist")

        with self.assertRaises(Exception):
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.api.Data.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_undefined_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_undefined_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = []

        self.assertFalse(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.api.Data.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_duplicate_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_duplicate_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = [MagicMock(), MagicMock()]

        self.assertFalse(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.api.Data.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_defined_pid_for_other_document_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_other_document_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id_other"
        mock_data_execute_query.return_value = [mock_result]

        self.assertFalse(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.api.Data.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_defined_pid_for_current_document_returns_true(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_current_document_returns_true"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id"
        mock_data_execute_query.return_value = [mock_result]

        self.assertTrue(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )


class TestIsPidDefinedForDocumentMongo(TestCase):
    """Test Is Pid Defined For Document"""

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_undefined_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_undefined_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = []

        self.assertFalse(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_duplicate_pid_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_duplicate_pid_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_data_execute_query.return_value = [MagicMock(), MagicMock()]

        self.assertFalse(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_defined_pid_for_other_document_returns_false(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_other_document_returns_false"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id_other"
        mock_data_execute_query.return_value = [mock_result]

        self.assertFalse(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_defined_pid_for_current_document_returns_true(
        self,
        mock_data_get_by_id,
        mock_get_pid_xpath_by_template,
        mock_data_execute_query,
    ):
        """test_defined_pid_for_current_document_returns_true"""
        mock_data_get_by_id.return_value = MagicMock()
        mock_get_pid_xpath_by_template.return_value = MagicMock()
        mock_result = MagicMock()
        mock_result.pk = "mock_document_id"
        mock_data_execute_query.return_value = [mock_result]

        self.assertTrue(
            system_api.is_pid_defined_for_data("mock_pid", "mock_document_id")
        )


class TestIsPidDefined(TestCase):
    """Test Is Pid Defined"""

    def test_get_data_by_pid_fails_with_unexpected_error_raises_error(self):
        """test_get_data_by_pid_fails_with_unexpected_error_raises_error"""

        pass

    def test_get_data_by_pid_fails_with_expected_error_returns_false(self):
        """test_get_data_by_pid_fails_with_expected_error_returns_false"""

        pass

    def test_get_data_by_pid_succeeds_return_true(self):
        """test_get_data_by_pid_succeeds_return_true"""

        pass


class TestGetDataByPidPsql(TestCase):
    """Test Get Data By Pid"""

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.api.Data.execute_query")
    @patch("core_linked_records_app.system.api.PidXpath.get_all")
    def test_query_returns_no_results_raises_error(
        self, mock_pid_xpath_get_all, mock_execute_query
    ):
        """test_query_returns_no_results_raises_error"""
        mock_pid_xpath_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 0
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(DoesNotExist):
            system_api.get_data_by_pid("mock_pid")

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.api.Data.execute_query")
    @patch("core_linked_records_app.system.api.PidXpath.get_all")
    def test_query_returns_several_results_raises_error(
        self, mock_pid_xpath_get_all, mock_execute_query
    ):
        """test_query_returns_several_results_raises_error"""
        mock_pid_xpath_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 2
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(ApiError):
            system_api.get_data_by_pid("mock_pid")

    @override_settings(MONGODB_INDEXING=False)
    @patch("core_linked_records_app.system.api.Data.execute_query")
    @patch("core_linked_records_app.system.api.PidXpath.get_all")
    def test_query_returns_single_result_returns_result(
        self, mock_pid_xpath_get_all, mock_execute_query
    ):
        """test_query_returns_single_result_returns_result"""
        mock_pid_xpath_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__getitem__.return_value = "mock_data"
        mock_execute_query.return_value = mock_queryset

        self.assertEquals(system_api.get_data_by_pid("mock_pid"), "mock_data")


class TestGetDataByPidMongo(TestCase):
    """Test Get Data By Pid"""

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.api.PidXpath.get_all")
    def test_query_returns_no_results_raises_error(
        self, mock_pid_xpath_get_all, mock_execute_query
    ):
        """test_query_returns_no_results_raises_error"""
        mock_pid_xpath_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 0
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(DoesNotExist):
            system_api.get_data_by_pid("mock_pid")

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.api.PidXpath.get_all")
    def test_query_returns_several_results_raises_error(
        self, mock_pid_xpath_get_all, mock_execute_query
    ):
        """test_query_returns_several_results_raises_error"""
        mock_pid_xpath_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 2
        mock_execute_query.return_value = mock_queryset

        with self.assertRaises(ApiError):
            system_api.get_data_by_pid("mock_pid")

    @tag("mongodb")
    @override_settings(MONGODB_INDEXING=True)
    @patch("core_main_app.components.mongo.models.MongoData.execute_query")
    @patch("core_linked_records_app.system.api.PidXpath.get_all")
    def test_query_returns_single_result_returns_result(
        self, mock_pid_xpath_get_all, mock_execute_query
    ):
        """test_query_returns_single_result_returns_result"""
        mock_pid_xpath_get_all.return_value = [MagicMock()]
        mock_queryset = MagicMock()
        mock_queryset.count.return_value = 1
        mock_queryset.__getitem__.return_value = "mock_data"
        mock_execute_query.return_value = mock_queryset

        self.assertEquals(system_api.get_data_by_pid("mock_pid"), "mock_data")


class TestGetPidXpathByTemplate(TestCase):
    """Test get_pid_xpath_by_template method"""

    @patch("core_linked_records_app.system.api.PidXpath.get_by_template")
    def test_get_by_template_is_called(self, mock_get_by_template):
        """Test get_by_template is called"""
        mock_template = "mock_template"

        system_api.get_pid_xpath_by_template(mock_template)
        mock_get_by_template.assert_called_with(mock_template)

    @patch("core_linked_records_app.system.api.PidXpath.__new__")
    @patch("core_linked_records_app.system.api.PidXpath.get_by_template")
    def test_get_by_template_none_returns_pid_xpath(
        self, mock_get_by_template, mock_pid_xpath
    ):
        """If get_by_template returns None, the PidXpath returned is the default one."""
        expected_result = Mock(spec=PidXpath)
        mock_get_by_template.return_value = None
        mock_pid_xpath.return_value = expected_result

        result = system_api.get_pid_xpath_by_template("mock_template")
        self.assertEqual(result, expected_result)

    @patch("core_linked_records_app.system.api.PidXpath.get_by_template")
    def test_returns_get_by_template_if_not_none(self, mock_get_by_template):
        """If get_by_template is not None, the PidXpath returned is get_by_template."""
        expected_result = "mock_result"
        mock_get_by_template.return_value = expected_result

        result = system_api.get_pid_xpath_by_template("mock_template")
        self.assertEqual(result, expected_result)


class TestDeletePidFromRecordName(TestCase):
    """Test delete_pid_from_record_name"""

    @patch.object(system_api, "ProviderManager")
    def test_provider_delete_is_called(self, mock_provider_manager):
        """test_provider_delete_is_called"""
        mock_provider = Mock()
        mock_record = "mock_record"

        mock_provider_manager().get.return_value = mock_provider
        mock_provider.delete.return_value = MockResponse()

        system_api.delete_pid_from_record_name(mock_record)
        mock_provider.delete.assert_called_with(mock_record)

    @patch.object(system_api, "logger")
    @patch.object(system_api, "ProviderManager")
    def test_provider_delete_failure_raises_api_error(
        self, mock_provider_manager, mock_logger
    ):
        """test_provider_delete_failure_is_logged"""
        mock_provider = Mock()
        mock_provider.delete.return_value = MockResponse(status_code=500)
        mock_record = "mock_record"

        mock_provider_manager().get.return_value = mock_provider

        with self.assertRaises(ApiError):
            system_api.delete_pid_from_record_name(mock_record)


class TestDeletePidForData(TestCase):
    """Test delete_pid_for_data"""

    @classmethod
    def setUpClass(cls) -> None:
        mock_data = Mock(spec=Data)
        mock_data.pk = "mock_pk"

        cls.mock_data = mock_data

        cls.mock_provider = Mock(spec=AbstractIdProvider)

    @patch("core_linked_records_app.system.api.delete_pid_from_record_name")
    @patch("core_linked_records_app.system.api.get_value_from_dot_notation")
    @patch("core_linked_records_app.system.api.xml_utils.raw_xml_to_dict")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    def test_get_dict_content_failure_calls_raw_xml_to_dict_utils(
        self,
        mock_get_pid_xpath_by_template,
        mock_raw_xml_to_dict,
        mock_get_value_from_dot_notation,
        mock_delete_pid_from_record_name,
    ):
        """test_get_dict_content_failure_calls_raw_xml_to_dict_utils"""
        self.mock_data.get_dict_content.side_effect = Exception(
            "mock_get_dict_content_exception"
        )
        mock_get_value_from_dot_notation.return_value = None

        system_api.delete_pid_for_data(self.mock_data)
        mock_raw_xml_to_dict.assert_called()

    @patch("core_linked_records_app.system.api.delete_pid_from_record_name")
    @patch("core_linked_records_app.system.api.get_value_from_dot_notation")
    @patch("core_linked_records_app.system.api.xml_utils.raw_xml_to_dict")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    def test_raw_xml_to_dict_failure_raises_api_error(
        self,
        mock_get_pid_xpath_by_template,
        mock_raw_xml_to_dict,
        mock_get_value_from_dot_notation,
        mock_delete_pid_from_record_name,
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
            system_api.delete_pid_for_data(self.mock_data)

    @patch("core_linked_records_app.system.api.delete_pid_from_record_name")
    @patch("core_linked_records_app.system.api.get_value_from_dot_notation")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    def test_empty_pid_is_not_deleted(
        self,
        mock_get_pid_xpath_by_template,
        mock_get_value_from_dot_notation,
        mock_delete_pid_from_record_name,
    ):
        """test_empty_pid_is_not_deleted"""
        mock_get_value_from_dot_notation.return_value = None

        system_api.delete_pid_for_data(self.mock_data)
        mock_delete_pid_from_record_name.assert_not_called()

    @patch("core_linked_records_app.system.api.delete_pid_from_record_name")
    @patch("core_linked_records_app.system.api.get_value_from_dot_notation")
    @patch("core_linked_records_app.system.api.get_pid_xpath_by_template")
    def test_delete_pid_from_record_called_when_pid_exists(
        self,
        mock_get_pid_xpath_by_template,
        mock_get_value_from_dot_notation,
        mock_delete_pid_from_record_name,
    ):
        """test_delete_pid_from_record_called"""
        mock_pid = "mock_pid"
        mock_get_value_from_dot_notation.return_value = mock_pid

        system_api.delete_pid_for_data(self.mock_data)
        mock_delete_pid_from_record_name.assert_called_with(mock_pid)


class TestDeletePidForBlob(TestCase):
    """Test delete_pid_for_blob"""

    def setUp(self) -> None:
        self.blob = Mock(spec=Blob)

    @patch.object(system_api, "delete_pid_from_record_name")
    @patch.object(local_id_api, "get_by_class_and_id")
    def test_get_by_class_and_id_called(
        self, mock_get_by_class_and_id, mock_delete_pid_from_record_name
    ):
        """test_get_by_class_and_id_called"""
        system_api.delete_pid_for_blob(self.blob)
        mock_get_by_class_and_id.assert_called_with(
            get_api_path_from_object(Blob()), self.blob.pk
        )

    @patch.object(system_api, "logger")
    @patch.object(local_id_api, "get_by_class_and_id")
    def test_does_not_exist_is_logged(
        self, mock_get_by_class_and_id, mock_logger
    ):
        """test_does_not_exist_is_logged"""
        mock_get_by_class_and_id.side_effect = DoesNotExist(
            "mock_get_by_class_and_id_does_not_exist"
        )

        system_api.delete_pid_for_blob(self.blob)
        mock_logger.info.assert_called()

    @patch.object(system_api, "delete_pid_from_record_name")
    @patch.object(local_id_api, "get_by_class_and_id")
    def test_delete_from_record_name_called(
        self, mock_get_by_class_and_id, mock_delete_pid_from_record_name
    ):
        """test_delete_from_record_name_called"""
        mock_local_id = Mock(spec=LocalId)
        mock_get_by_class_and_id.return_value = mock_local_id
        system_api.delete_pid_for_blob(self.blob)
        mock_delete_pid_from_record_name.assert_called_with(
            mock_local_id.record_name
        )
