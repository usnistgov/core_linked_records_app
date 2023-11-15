""" Unit tests for core_linked_records_app.components.data.watch
"""
import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from rest_framework import status

from core_linked_records_app.components.data import watch as data_watch
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.data import api as data_system_api
from core_linked_records_app.system.pid_path import (
    api as pid_path_system_api,
)
from core_linked_records_app.utils import data as data_utils
from core_linked_records_app.utils import exceptions
from core_linked_records_app.utils import providers as providers_utils
from tests import mocks


class TestRegisterPidForDataId(TestCase):
    """Unit tests for `_register_pid_for_data_id` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_resolver_match = MagicMock()
        self.mock_resolver_match.view_name = (
            "core_linked_records_provider_record"
        )

        self.mock_provider = MagicMock()
        self.mock_provider.provider_lookup_url = "http://cdcs.handle.net"
        self.mock_provider.local_url = "http://cdcs.example.com/pid/rest"

        self.mock_prefix = "12.34567"
        self.mock_record = "mock_record"

        self.kwargs = {
            "provider_name": "mock_provider",
            "pid_value": f"{self.mock_provider.provider_lookup_url}/{self.mock_prefix}/"
            f"{self.mock_record}",
            "data_id": 42,
        }

    @patch.object(data_watch, "ProviderManager")
    def test_provider_manager_is_instantiated(self, mock_provider_manager):
        """test_provider_manager_is_instantiated"""
        with self.assertRaises(exceptions.PidResolverError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        mock_provider_manager.assert_called()

    @patch.object(data_watch, "ProviderManager")
    def test_default_provider_is_retrieved(self, mock_provider_manager):
        """test_default_provider_is_retrieved"""
        with self.assertRaises(exceptions.PidResolverError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        mock_provider_manager().get.assert_called_with(
            self.kwargs["provider_name"]
        )

    @patch.object(data_watch, "logger")
    @patch.object(data_watch, "resolve")
    @patch.object(data_watch, "ProviderManager")
    def test_resolver_error_is_logged_and_raises_core_error(
        self, mock_provider_manager, mock_resolve, mock_logger
    ):
        """test_resolver_error_is_logged_and_raises_core_error"""
        mock_provider_manager().get.return_value = self.mock_provider
        mock_resolve.side_effect = Exception("mock_resolve_exception")

        with self.assertRaises(exceptions.PidResolverError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        mock_logger.error.assert_called()

    @patch.object(data_watch, "logger")
    @patch.object(data_watch, "resolve")
    @patch.object(data_watch, "ProviderManager")
    def test_resolver_not_matching_correct_view_is_logged_and_raises_core_error(
        self, mock_provider_manager, mock_resolve, mock_logger
    ):
        """test_resolver_not_matching_correct_view_is_logged_and_raises_core_error"""
        mock_provider_manager().get.return_value = self.mock_provider
        mock_resolve.return_value = self.mock_resolver_match
        self.mock_resolver_match.view_name = "mock_incorrect_view_name"

        with self.assertRaises(exceptions.PidResolverError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        mock_logger.error.assert_called()

    @patch.object(data_watch, "logger")
    @patch.object(data_watch, "split_prefix_from_record")
    @patch.object(data_watch, "resolve")
    @patch.object(data_watch, "ProviderManager")
    def test_split_prefix_from_record_error_is_logged_and_raises_core_error(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
        mock_logger,
    ):
        """test_split_prefix_from_record_error_is_logged_and_raises_core_error"""
        mock_provider_manager().get.return_value = self.mock_provider
        mock_resolve.return_value = self.mock_resolver_match
        mock_split_prefix_from_record.side_effect = Exception(
            "mock_split_prefix_from_record_exception"
        )

        with self.assertRaises(exceptions.PidResolverError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        mock_logger.error.assert_called()

    @patch.object(data_watch, "data_system_api")
    @patch.object(data_watch, "split_prefix_from_record")
    @patch.object(data_watch, "resolve")
    @patch.object(data_watch, "ProviderManager")
    def test_provider_create_is_called(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
        mock_data_system_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_provider_create_is_called"""
        mock_provider_manager().get.return_value = self.mock_provider
        mock_resolve.return_value = self.mock_resolver_match
        mock_split_prefix_from_record.return_value = (
            self.mock_prefix,
            self.mock_record,
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        self.mock_provider.create.assert_called_with(
            self.mock_prefix, self.mock_record
        )

    @patch.object(data_watch, "logger")
    @patch.object(data_watch, "data_system_api")
    @patch.object(data_watch, "split_prefix_from_record")
    @patch.object(data_watch, "resolve")
    @patch.object(data_watch, "ProviderManager")
    def test_provider_create_unparsable_response_is_logged_and_raises_core_error(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
        mock_data_system_api,  # noqa, pylint: disable=unused-argument
        mock_logger,
    ):
        """test_provider_create_unparsable_response_is_logged_and_raises_core_error"""
        mock_provider_manager().get.return_value = self.mock_provider
        mock_resolve.return_value = self.mock_resolver_match
        mock_split_prefix_from_record.return_value = (
            self.mock_prefix,
            self.mock_record,
        )

        mock_provider_create_response = MagicMock()
        mock_provider_create_response.status_code = (
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        mock_provider_create_response.content = None
        self.mock_provider.create.return_value = mock_provider_create_response

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        mock_logger.error.assert_called()

    @patch.object(data_watch, "logger")
    @patch.object(data_watch, "data_system_api")
    @patch.object(data_watch, "split_prefix_from_record")
    @patch.object(data_watch, "resolve")
    @patch.object(data_watch, "ProviderManager")
    def test_provider_create_parsable_response_is_logged_and_raises_core_error(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
        mock_data_system_api,  # noqa, pylint: disable=unused-argument
        mock_logger,
    ):
        """test_provider_create_parsable_response_is_logged_and_raises_core_error"""
        mock_provider_manager().get.return_value = self.mock_provider
        mock_resolve.return_value = self.mock_resolver_match
        mock_split_prefix_from_record.return_value = (
            self.mock_prefix,
            self.mock_record,
        )

        mock_provider_create_response = MagicMock()
        mock_provider_create_response.status_code = (
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        mock_provider_create_response.content = json.dumps(
            {"message": "mock_error"}
        )
        self.mock_provider.create.return_value = mock_provider_create_response

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._register_pid_for_data_id(**self.kwargs)

        mock_logger.error.assert_called()

    @patch.object(data_watch, "data_system_api")
    @patch.object(data_watch, "split_prefix_from_record")
    @patch.object(data_watch, "resolve")
    @patch.object(data_watch, "ProviderManager")
    def test_succesful_execution_returns_record_url(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
        mock_data_system_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_succesful_execution_returns_record_url"""
        expected_result = "mock_record_url"

        mock_provider_manager().get.return_value = self.mock_provider
        mock_resolve.return_value = self.mock_resolver_match
        mock_split_prefix_from_record.return_value = (
            self.mock_prefix,
            self.mock_record,
        )

        mock_provider_create_response = MagicMock()
        mock_provider_create_response.status_code = status.HTTP_201_CREATED
        mock_provider_create_response.content = json.dumps(
            {"url": expected_result}
        )
        self.mock_provider.create.return_value = mock_provider_create_response

        result = data_watch._register_pid_for_data_id(**self.kwargs)

        self.assertEqual(result, expected_result)


class TestSetDataPid(TestCase):
    """Unit tests for `_set_data_pid` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"instance": mocks.MockData()}

    @patch.object(data_watch, "transaction")
    def test_transaction_on_commit_is_called(self, mock_transaction):
        """test_transaction_on_commit_is_called"""
        data_watch.set_data_pid(None, self.mock_kwargs["instance"])
        mock_transaction.on_commit.assert_called()

    @patch.object(PidSettings, "get")
    def test_pid_settings_get_failure_raises_pid_create_error(
        self, mock_pid_settings_get
    ):
        """test_pid_settings_get_failure_raises_core_error"""

        mock_pid_settings_get.side_effect = Exception(
            "mock_pid_settings_get_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_get_pid_path_by_template_failure_raises_pid_create_error(
        self, mock_pid_settings_get, mock_get_pid_path_by_template
    ):
        """test_get_pid_path_by_template_failure_raises_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.side_effect = Exception(
            "mock_get_pid_path_by_template_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_get_pid_value_for_data_failure_returns_none(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
    ):
        """test_get_pid_value_for_data_failure_returns_none"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.side_effect = Exception(
            "mock_get_pid_value_for_data_exception"
        )

        self.assertIsNone(data_watch._set_data_pid(**self.mock_kwargs))

    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_delete_pid_for_data_raises_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
    ):
        """test_delete_pid_for_data_raises_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = "mock_pid_value"
        mock_delete_pid_for_data.side_effect = Exception(
            "mock_delete_pid_for_data_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_retrieve_provider_name_failure_raise_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
    ):
        """test_retrieve_provider_name_failure_raise_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = "mock_pid_value"
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.side_effect = Exception(
            "mock_retrieve_provider_name_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_provider_manager_get_failure_raise_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
    ):
        """test_provider_manager_get_failure_raise_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(data_system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_is_pid_defined_failure_raise_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
    ):
        """test_is_pid_defined_failure_raise_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(data_system_api, "is_pid_defined_for_data")
    @patch.object(data_system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_is_pid_defined_for_data_failure_raise_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
    ):
        """test_is_pid_defined_for_data_failure_raise_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.side_effect = Exception(
            "mock_is_pid_defined_for_data_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(data_system_api, "is_pid_defined_for_data")
    @patch.object(data_system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_pid_already_defined_raise_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
    ):
        """test_pid_already_defined_raise_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.return_value = False

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(data_watch, "_register_pid_for_data_id")
    @patch.object(data_system_api, "is_pid_defined_for_data")
    @patch.object(data_system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_register_pid_for_data_id_failure_raise_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
        mock_register_pid_for_data_id,
    ):
        """test_register_pid_for_data_id_failure_raise_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.return_value = True
        mock_register_pid_for_data_id.side_effect = Exception(
            "mock_register_pid_for_data_id_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(data_utils, "set_pid_value_for_data")
    @patch.object(data_watch, "_register_pid_for_data_id")
    @patch.object(data_system_api, "is_pid_defined_for_data")
    @patch.object(data_system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_set_pid_value_for_data_failure_raise_pid_create_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
        mock_register_pid_for_data_id,
        mock_set_pid_value_for_data,
    ):
        """test_set_pid_value_for_data_failure_raise_pid_create_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.return_value = True
        mock_register_pid_for_data_id.return_value = "mock_pid_value"
        mock_set_pid_value_for_data.side_effect = Exception(
            "mock_set_pid_value_for_data_exception"
        )

        with self.assertRaises(exceptions.PidCreateError):
            data_watch._set_data_pid(**self.mock_kwargs)

    @patch.object(data_utils, "set_pid_value_for_data")
    @patch.object(data_watch, "_register_pid_for_data_id")
    @patch.object(data_system_api, "is_pid_defined_for_data")
    @patch.object(data_system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(data_system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(pid_path_system_api, "get_pid_path_by_template")
    @patch.object(PidSettings, "get")
    def test_default_execution_returns_none(
        self,
        mock_pid_settings_get,
        mock_get_pid_path_by_template,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
        mock_register_pid_for_data_id,
        mock_set_pid_value_for_data,
    ):
        """test_default_execution_returns_none"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_path_by_template.return_value = mocks.MockPidPath()
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.return_value = True
        mock_register_pid_for_data_id.return_value = "mock_pid_value"
        mock_set_pid_value_for_data.return_value = None

        self.assertIsNone(data_watch._set_data_pid(**self.mock_kwargs))


class TestDeleteDataPid(TestCase):
    """Unit tests for `detele_data_pid` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_data = mocks.MockDocument()

    @patch.object(data_system_api, "delete_pid_for_data")
    def test_delete_pid_for_data_is_called(self, mock_delete_pid_for_data):
        """test_delete_pid_for_data_is_called"""
        data_watch.delete_data_pid(None, self.mock_data)

        mock_delete_pid_for_data.assert_called_with(self.mock_data)

    @patch.object(data_watch, "logger")
    @patch.object(data_system_api, "delete_pid_for_data")
    def test_delete_pid_for_data_error_raise_warning(
        self, mock_delete_pid_for_data, mock_logger
    ):
        """test_delete_pid_for_data_error_raise_warning"""
        mock_delete_pid_for_data.side_effect = Exception(
            "mock_delete_pid_for_data_exception"
        )
        data_watch.delete_data_pid(None, self.mock_data)

        mock_logger.warning.assert_called()
