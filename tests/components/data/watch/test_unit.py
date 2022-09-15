""" Unit tests for core_linked_records_app.components.data.watch
"""
from unittest import TestCase
from unittest.mock import patch

from core_main_app.commons import exceptions
from core_linked_records_app.components.data import watch as data_watch
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.system import api as system_api
from core_linked_records_app.utils import data as data_utils
from core_linked_records_app.utils import providers as providers_utils
from tests import mocks


class TestSetDataPid(TestCase):
    """Test Set Data Pid"""

    def setUp(self):
        """setUp"""

        mock_sender = None
        mock_document = mocks.MockData()

        self.mock_kwargs = {"sender": mock_sender, "instance": mock_document}

    @patch.object(pid_settings_api, "get")
    def test_pid_settings_get_failure_raises_core_error(self, mock_pid_settings_get):
        """test_pid_settings_get_failure_raises_core_error"""

        mock_pid_settings_get.side_effect = Exception("mock_pid_settings_get_exception")

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_get_pid_xpath_by_template_failure_raises_core_error(
        self, mock_pid_settings_get, mock_get_pid_xpath_by_template
    ):
        """test_get_pid_xpath_by_template_failure_raises_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.side_effect = Exception(
            "mock_get_pid_xpath_by_template_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_get_xpath_from_dot_notation_failure_raises_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
    ):
        """test_get_xpath_from_dot_notation_failure_raises_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.side_effect = Exception(
            "mock_get_xpath_from_dot_notation_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_get_xpath_with_target_namespace_failure_raises_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
    ):
        """test_get_xpath_with_target_namespace_failure_raises_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.side_effect = Exception(
            "mock_get_xpath_with_target_namespace_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_get_pid_value_for_data_failure_returns_none(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
    ):
        """test_get_pid_value_for_data_failure_returns_none"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.side_effect = Exception(
            "mock_get_pid_value_for_data_exception"
        )

        self.assertIsNone(data_watch.set_data_pid(**self.mock_kwargs))

    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_delete_pid_for_data_raises_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
    ):
        """test_delete_pid_for_data_raises_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = "mock_pid_value"
        mock_delete_pid_for_data.side_effect = Exception(
            "mock_delete_pid_for_data_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_retrieve_provider_name_failure_raise_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
    ):
        """test_retrieve_provider_name_failure_raise_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = "mock_pid_value"
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.side_effect = Exception(
            "mock_retrieve_provider_name_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_provider_manager_get_failure_raise_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
    ):
        """test_provider_manager_get_failure_raise_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_is_pid_defined_failure_raise_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
    ):
        """test_is_pid_defined_failure_raise_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(system_api, "is_pid_defined_for_data")
    @patch.object(system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_is_pid_defined_for_data_failure_raise_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
    ):
        """test_is_pid_defined_for_data_failure_raise_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.side_effect = Exception(
            "mock_is_pid_defined_for_data_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(system_api, "is_pid_defined_for_data")
    @patch.object(system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_pid_already_defined_raise_model_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
    ):
        """test_pid_already_defined_raise_model_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.return_value = False

        with self.assertRaises(exceptions.ModelError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(providers_utils, "register_pid_for_data_id")
    @patch.object(system_api, "is_pid_defined_for_data")
    @patch.object(system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_register_pid_for_data_id_failure_raise_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
        mock_register_pid_for_data_id,
    ):
        """test_register_pid_for_data_id_failure_raise_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.return_value = True
        mock_register_pid_for_data_id.side_effect = Exception(
            "mock_register_pid_for_data_id_exception"
        )

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(data_utils, "set_pid_value_for_data")
    @patch.object(providers_utils, "register_pid_for_data_id")
    @patch.object(system_api, "is_pid_defined_for_data")
    @patch.object(system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_set_pid_value_for_data_failure_raise_core_error(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
        mock_get_pid_value_for_data,
        mock_delete_pid_for_data,
        mock_retrieve_provider_name,
        mock_provider_manager_get,
        mock_is_pid_defined,
        mock_is_pid_defined_for_data,
        mock_register_pid_for_data_id,
        mock_set_pid_value_for_data,
    ):
        """test_set_pid_value_for_data_failure_raise_core_error"""

        mock_pid_settings_get.return_value = mocks.MockPidSettings()
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
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

        with self.assertRaises(exceptions.CoreError):
            data_watch.set_data_pid(**self.mock_kwargs)

    @patch.object(data_utils, "set_pid_value_for_data")
    @patch.object(providers_utils, "register_pid_for_data_id")
    @patch.object(system_api, "is_pid_defined_for_data")
    @patch.object(system_api, "is_pid_defined")
    @patch.object(providers_utils.ProviderManager, "get")
    @patch.object(providers_utils, "retrieve_provider_name")
    @patch.object(system_api, "delete_pid_for_data")
    @patch.object(data_utils, "get_pid_value_for_data")
    @patch.object(data_watch, "get_xpath_with_target_namespace")
    @patch.object(data_watch, "get_xpath_from_dot_notation")
    @patch.object(system_api, "get_pid_xpath_by_template")
    @patch.object(pid_settings_api, "get")
    def test_default_execution_returns_none(
        self,
        mock_pid_settings_get,
        mock_get_pid_xpath_by_template,
        mock_get_xpath_from_dot_notation,
        mock_get_xpath_with_target_namespace,
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
        mock_get_pid_xpath_by_template.return_value = mocks.MockPidXpath()
        mock_get_xpath_from_dot_notation.return_value = "mock_pid_xpath"
        mock_get_xpath_with_target_namespace.return_value = "mock_pid_xpath"
        mock_get_pid_value_for_data.return_value = None
        mock_delete_pid_for_data.return_value = None
        mock_retrieve_provider_name.return_value = "mock_provider_name"
        mock_provider_manager_get.return_value = mocks.MockProviderManager()
        mock_is_pid_defined.return_value = True
        mock_is_pid_defined_for_data.return_value = True
        mock_register_pid_for_data_id.return_value = "mock_pid_value"
        mock_set_pid_value_for_data.return_value = None

        self.assertIsNone(data_watch.set_data_pid(**self.mock_kwargs))
