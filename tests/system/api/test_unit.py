""" Unit tests for core_linked_records_app.system.api
"""
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock
from django.test import tag, override_settings

from core_linked_records_app.components.pid_xpath.models import PidXpath
from core_linked_records_app.system.api import (
    delete_pid_for_data,
    get_pid_xpath_by_template,
    is_pid_defined_for_data,
    get_data_by_pid,
)
from core_linked_records_app.utils.providers import AbstractIdProvider
from core_main_app.commons.exceptions import DoesNotExist, ApiError
from core_main_app.components.data.models import Data
from tests.mocks import MockResponse


class TestIsPidDefinedForDocumentPsql(TestCase):
    """Test Is Pid Defined For Document"""

    @patch("core_linked_records_app.system.api.Data.get_by_id")
    def test_wrong_document_id_raise_error(self, mock_data_get_by_id):
        """test_wrong_document_id_raise_error"""
        mock_data_get_by_id.side_effect = DoesNotExist("mock_does_not_exist")

        with self.assertRaises(Exception):
            is_pid_defined_for_data("mock_pid", "mock_document_id")

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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            is_pid_defined_for_data("mock_pid", "mock_document_id")
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
            get_data_by_pid("mock_pid")

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
            get_data_by_pid("mock_pid")

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

        self.assertEquals(get_data_by_pid("mock_pid"), "mock_data")


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
            get_data_by_pid("mock_pid")

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
            get_data_by_pid("mock_pid")

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

        self.assertEquals(get_data_by_pid("mock_pid"), "mock_data")


class TestGetPidForData(TestCase):
    """Test Get Pid For Data"""

    def test_not_existing_pid_returns_none(self):
        """test_not_existing_pid_returns_none"""

        pass

    def test_existing_pid_returns_pid(self):
        """test_existing_pid_returns_pid"""

        pass


class TestGetPidXpathByTemplate(TestCase):
    """Test get_pid_xpath_by_template method"""

    @patch("core_linked_records_app.system.api.PidXpath.get_by_template")
    def test_get_by_template_is_called(self, mock_get_by_template):
        """Test get_by_template is called"""
        mock_template = "mock_template"

        get_pid_xpath_by_template(mock_template)
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

        result = get_pid_xpath_by_template("mock_template")
        self.assertEqual(result, expected_result)

    @patch("core_linked_records_app.system.api.PidXpath.get_by_template")
    def test_returns_get_by_template_if_not_none(self, mock_get_by_template):
        """If get_by_template is not None, the PidXpath returned is get_by_template."""
        expected_result = "mock_result"
        mock_get_by_template.return_value = expected_result

        result = get_pid_xpath_by_template("mock_template")
        self.assertEqual(result, expected_result)


class TestDeletePidForData(TestCase):
    """Test delete_pid_for_data"""

    @classmethod
    def setUpClass(cls) -> None:
        mock_data = Mock(spec=Data)
        mock_data.pk = "mock_pk"

        cls.mock_data = mock_data

        cls.mock_provider = Mock(spec=AbstractIdProvider)

    @patch("core_linked_records_app.utils.providers.ProviderManager.get")
    @patch("core_linked_records_app.system.api.get_pid_for_data")
    def test_empty_pid_is_not_deleted(
        self, mock_get_pid_for_data, mock_provider_manager_get
    ):
        """test_empty_pid_is_not_deleted"""
        mock_get_pid_for_data.return_value = None
        mock_provider_manager_get.return_value = self.mock_provider

        delete_pid_for_data(self.mock_data)
        self.mock_provider.delete.assert_not_called()

    @patch("core_linked_records_app.utils.providers.ProviderManager.get")
    @patch("core_linked_records_app.system.api.get_pid_for_data")
    def test_provider_delete_called(
        self, mock_get_pid_for_data, mock_provider_manager_get
    ):
        """test_provider_delete_called"""
        mock_pid = "mock_pid"
        mock_get_pid_for_data.return_value = mock_pid
        mock_provider_manager_get.return_value = self.mock_provider

        delete_pid_for_data(self.mock_data)
        self.mock_provider.delete.assert_called_with(mock_pid)

    @patch("core_linked_records_app.utils.providers.ProviderManager.get")
    @patch("core_linked_records_app.system.api.get_pid_for_data")
    def test_pid_delete_failure_exits(
        self, mock_get_pid_for_data, mock_provider_manager_get
    ):
        """test_pid_delete_failure_exits"""
        mock_pid = "mock_pid"
        mock_get_pid_for_data.return_value = mock_pid
        mock_provider_manager_get.return_value = self.mock_provider

        self.mock_provider.delete.return_value = MockResponse(status_code=500)

        delete_pid_for_data(self.mock_data)

    @patch("core_linked_records_app.utils.providers.ProviderManager.get")
    @patch("core_linked_records_app.system.api.get_pid_for_data")
    def test_pid_delete_success_works(
        self, mock_get_pid_for_data, mock_provider_manager_get
    ):
        """test_pid_delete_success_works"""
        mock_pid = "mock_pid"
        mock_get_pid_for_data.return_value = mock_pid
        mock_provider_manager_get.return_value = self.mock_provider

        self.mock_provider.delete.return_value = MockResponse(status_code=200)

        delete_pid_for_data(self.mock_data)
