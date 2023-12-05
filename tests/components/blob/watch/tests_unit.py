""" Unit tests for `core_linked_records_app.components.blob.watch` package.
"""
import json
from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.urls import Resolver404
from rest_framework import status

from core_linked_records_app.components.blob import watch as blob_watch
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.blob import api as blob_system_api
from core_linked_records_app.utils import exceptions as pid_exceptions
from core_main_app.commons import exceptions as main_exceptions
from tests import mocks


class TestRegisterPidForBlobId(TestCase):
    """Unit tests for `_register_pid_for_blob_id` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "provider_name": MagicMock(),
            "pid_value": MagicMock(),
            "blob_id": MagicMock(),
        }

    @patch.object(blob_watch, "ProviderManager")
    def test_provider_manager_init_error_raises_invalid_provider(
        self, mock_provider_manager
    ):
        """test_provider_manager_init_error_raises_invalid_provider"""
        mock_provider_manager.side_effect = Exception(
            "mock_provider_manager_exception"
        )

        with self.assertRaises(pid_exceptions.InvalidProviderError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

    @patch.object(blob_watch, "ProviderManager")
    def test_provider_manager_get_error_raises_invalid_provider(
        self, mock_provider_manager
    ):
        """test_provider_manager_get_error_raises_invalid_provider"""
        mock_provider_manager_object = MagicMock()
        mock_provider_manager_object.get.side_effect = Exception(
            "mock_provider_manager_get_exception"
        )
        mock_provider_manager.return_value = mock_provider_manager_object

        with self.assertRaises(pid_exceptions.InvalidProviderError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

    @patch.object(blob_watch, "ProviderManager")
    def test_pid_value_lookup_url_replaced_by_local_url(
        self, mock_provider_manager
    ):
        """test_pid_value_lookup_url_replaced_by_local_url"""
        mock_provider_manager_object = MagicMock()
        mock_provider = MagicMock()
        mock_provider_manager_object.get.return_value = mock_provider
        mock_provider_manager.return_value = mock_provider_manager_object

        with self.assertRaises(pid_exceptions.PidResolverError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

        self.mock_kwargs["pid_value"].replace.assert_called_with(
            mock_provider.provider_lookup_url, mock_provider.local_url
        )

    @patch.object(blob_watch, "resolve")
    @patch.object(blob_watch, "ProviderManager")
    def test_resolver_error_raises_pid_resolver_error(
        self,
        mock_provider_manager,  # noqa, pylint: disable=unused-argument
        mock_resolve,
    ):
        """test_resolver_error_raises_pid_resolver_error"""
        mock_resolve.side_effect = Resolver404()

        with self.assertRaises(pid_exceptions.PidResolverError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

    @patch.object(blob_watch, "resolve")
    @patch.object(blob_watch, "ProviderManager")
    def test_invalid_view_name_raises_pid_resolver_error(
        self,
        mock_provider_manager,  # noqa, pylint: disable=unused-argument
        mock_resolve,
    ):
        """test_invalid_view_name_raises_pid_resolver_error"""
        mock_resolver_match = MagicMock()
        mock_resolver_match.view_name = "invalid_view_name"
        mock_resolve.return_value = mock_resolver_match

        with self.assertRaises(pid_exceptions.PidResolverError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

    @patch.object(blob_watch, "split_prefix_from_record")
    @patch.object(blob_watch, "resolve")
    @patch.object(blob_watch, "ProviderManager")
    def test_split_prefix_from_record_invalid_prefix_raises_invalid_pid_error(
        self,
        mock_provider_manager,  # noqa, pylint: disable=unused-argument
        mock_resolve,
        mock_split_prefix_from_record,
    ):
        """test_split_prefix_from_record_invalid_prefix_raises_invalid_pid_error"""
        mock_resolver_match = MagicMock()
        mock_resolver_match.view_name = "core_linked_records_provider_record"
        mock_resolve.return_value = mock_resolver_match

        mock_split_prefix_from_record.side_effect = (
            pid_exceptions.InvalidPrefixError(
                "mock_split_prefix_from_record_invalid_prefix_error"
            )
        )

        with self.assertRaises(pid_exceptions.InvalidPidError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

    @patch.object(blob_watch, "split_prefix_from_record")
    @patch.object(blob_watch, "resolve")
    @patch.object(blob_watch, "ProviderManager")
    def test_split_prefix_from_record_invalid_record_raises_invalid_pid_error(
        self,
        mock_provider_manager,  # noqa, pylint: disable=unused-argument
        mock_resolve,
        mock_split_prefix_from_record,
    ):
        """test_split_prefix_from_record_invalid_record_raises_invalid_pid_error"""
        mock_resolver_match = MagicMock()
        mock_resolver_match.view_name = "core_linked_records_provider_record"
        mock_resolve.return_value = mock_resolver_match

        mock_split_prefix_from_record.side_effect = (
            pid_exceptions.InvalidRecordError(
                "mock_split_prefix_from_record_invalid_record_error"
            )
        )

        with self.assertRaises(pid_exceptions.InvalidPidError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

    @patch.object(blob_watch, "split_prefix_from_record")
    @patch.object(blob_watch, "resolve")
    @patch.object(blob_watch, "ProviderManager")
    def test_provider_create_called(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
    ):
        """test_provider_create_called"""
        mock_provider_manager_object = MagicMock()
        mock_provider = MagicMock()
        mock_provider_manager_object.get.return_value = mock_provider
        mock_provider_manager.return_value = mock_provider_manager_object
        mock_resolver_match = MagicMock()
        mock_resolver_match.view_name = "core_linked_records_provider_record"
        mock_resolve.return_value = mock_resolver_match

        mock_prefix = MagicMock()
        mock_record = MagicMock()
        mock_split_prefix_from_record.return_value = mock_prefix, mock_record

        with self.assertRaises(pid_exceptions.PidCreateError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

        mock_provider.create.assert_called_with(mock_prefix, mock_record)

    @patch.object(blob_watch, "blob_system_api")
    @patch.object(blob_watch, "split_prefix_from_record")
    @patch.object(blob_watch, "resolve")
    @patch.object(blob_watch, "ProviderManager")
    def test_invalid_provider_response_raises_pid_create_error(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
        mock_blob_system_api,
    ):
        """test_invalid_provider_response_raises_pid_create_error_with_content"""
        mock_provider_manager_object = MagicMock()
        mock_provider = MagicMock()
        mock_provider_manager_object.get.return_value = mock_provider
        mock_provider_manager.return_value = mock_provider_manager_object
        mock_resolver_match = MagicMock()
        mock_resolver_match.view_name = "core_linked_records_provider_record"
        mock_resolve.return_value = mock_resolver_match

        mock_split_prefix_from_record.return_value = MagicMock(), MagicMock()

        mock_provider_response = MagicMock()
        mock_provider_response.status_code = status.HTTP_400_BAD_REQUEST
        mock_provider_response.content = json.dumps(
            {"message": "mock_error_message"}
        )
        mock_provider.create.return_value = mock_provider_response

        mock_blob_system_api.get_blob_by_pid.return_value = MagicMock()

        with self.assertRaises(pid_exceptions.PidCreateError):
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs)

    @patch.object(blob_watch, "blob_system_api")
    @patch.object(blob_watch, "split_prefix_from_record")
    @patch.object(blob_watch, "resolve")
    @patch.object(blob_watch, "ProviderManager")
    def test_succesful_execution_returns_provider_response_url(
        self,
        mock_provider_manager,
        mock_resolve,
        mock_split_prefix_from_record,
        mock_blob_system_api,  # noqa, pylint: disable=unused-argument
    ):
        """test_succesful_execution_returns_provider_response_url"""
        mock_provider_manager_object = MagicMock()
        mock_provider = MagicMock()
        mock_provider_manager_object.get.return_value = mock_provider
        mock_provider_manager.return_value = mock_provider_manager_object
        mock_resolver_match = MagicMock()
        mock_resolver_match.view_name = "core_linked_records_provider_record"
        mock_resolve.return_value = mock_resolver_match

        mock_split_prefix_from_record.return_value = MagicMock(), MagicMock()

        mock_provider_response = MagicMock()
        mock_provider_response.status_code = status.HTTP_200_OK
        mock_provider_content = {"url": "mock_url"}
        mock_provider_response.content = json.dumps(mock_provider_content)
        mock_provider.create.return_value = mock_provider_response

        self.assertEqual(
            blob_watch._register_pid_for_blob_id(**self.mock_kwargs),
            mock_provider_content["url"],
        )


class TestSetBlobPid(TestCase):
    """Test Set Blob Pid"""

    def setUp(self):
        """setUp"""
        self.mock_document = mocks.MockDocument()

    @patch.object(blob_watch, "transaction")
    def test_transaction_on_commit_is_called(self, mock_transaction):
        """test_transaction_on_commit_is_called"""
        blob_watch.set_blob_pid(None, self.mock_document)
        mock_transaction.on_commit.assert_called()

    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(PidSettings, "get")
    def test_pid_setting_get_failure_raises_core_error(
        self, mock_get, mock_get_pid_for_blob
    ):
        """test_pid_setting_get_failure_raises_core_error"""

        mock_get_pid_for_blob.side_effect = main_exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_get.side_effect = Exception("mock_get_exception")

        with self.assertRaises(main_exceptions.CoreError):
            blob_watch._set_blob_pid(self.mock_document)

    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(PidSettings, "get")
    def test_get_pid_for_blob_failure_raises_core_error(
        self, mock_get, mock_get_pid_for_blob
    ):
        """test_get_pid_for_blob_failure_raises_core_error"""
        mock_get.return_value = MagicMock()
        mock_get_pid_for_blob.side_effect = Exception(
            "mock_get_pid_for_blob_exception"
        )

        with self.assertRaises(main_exceptions.CoreError):
            blob_watch._set_blob_pid(self.mock_document)

    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(blob_watch, "_register_pid_for_blob_id")
    @patch.object(PidSettings, "get")
    def test_register_pid_for_blob_failure_raises_core_error(
        self,
        mock_get,
        mock_register_pid_for_blob_id,
        mock_get_pid_for_blob,
    ):
        """test_register_pid_for_blob_failure_raises_core_error"""

        mock_get.return_value = mocks.MockPidSettings()
        mock_get_pid_for_blob.side_effect = main_exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_register_pid_for_blob_id.side_effect = Exception(
            "mock_register_pid_for_blob_id_exception"
        )

        with self.assertRaises(main_exceptions.CoreError):
            blob_watch._set_blob_pid(self.mock_document)

    @patch.object(blob_system_api, "set_pid_for_blob")
    @patch.object(blob_watch, "_register_pid_for_blob_id")
    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(PidSettings, "get")
    def test_set_pid_for_blob_failure_raises_core_error(
        self,
        mock_get,
        mock_get_pid_for_blob,
        mock_register_pid_for_blob_id,
        mock_set_pid_for_blob,
    ):
        """test_set_pid_for_blob_failure_raises_core_error"""

        mock_get_pid_for_blob.side_effect = main_exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_register_pid_for_blob_id.return_value = MagicMock()
        mock_get.return_value = mocks.MockPidSettings()
        mock_set_pid_for_blob.side_effect = Exception(
            "mock_set_pid_for_blob_exception"
        )

        with self.assertRaises(main_exceptions.CoreError):
            blob_watch._set_blob_pid(self.mock_document)

    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(blob_system_api, "set_pid_for_blob")
    @patch.object(PidSettings, "get")
    def test_auto_set_pid_false_does_not_assign_pid(
        self, mock_get, mock_set_pid_for_blob, mock_get_pid_for_blob
    ):
        """test_auto_set_pid_false_does_not_assign_pid"""

        mock_get_pid_for_blob.side_effect = main_exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_pid_settings = mocks.MockPidSettings()
        mock_pid_settings.auto_set_pid = False
        mock_get.return_value = mock_pid_settings

        blob_watch._set_blob_pid(self.mock_document)
        mock_set_pid_for_blob.assert_not_called()

    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(blob_system_api, "set_pid_for_blob")
    @patch.object(PidSettings, "get")
    def test_auto_set_pid_true_assign_pid(
        self,
        mock_get,
        mock_set_pid_for_blob,
        mock_get_pid_for_blob,
    ):
        """test_auto_set_pid_true_assign_pid"""

        mock_get_pid_for_blob.side_effect = main_exceptions.DoesNotExist(
            "pid_does_not_exist"
        )  # noqa
        mock_get.return_value = mocks.MockPidSettings()
        mock_set_pid_for_blob.return_value = None

        blob_watch._set_blob_pid(self.mock_document)
        mock_set_pid_for_blob.assert_called_once()

    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(PidSettings, "get")
    def test_auto_set_pid_false_returns_none(
        self, mock_get, mock_get_pid_for_blob
    ):
        """test_auto_set_pid_false_returns_none"""

        mock_get_pid_for_blob.side_effect = main_exceptions.DoesNotExist(
            "pid_does_not_exist"
        )
        mock_pid_settings = mocks.MockPidSettings()
        mock_pid_settings.auto_set_pid = False
        mock_get.return_value = mock_pid_settings

        self.assertIsNone(blob_watch._set_blob_pid(self.mock_document))

    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(blob_system_api, "set_pid_for_blob")
    @patch.object(PidSettings, "get")
    def test_auto_set_pid_true_returns_none(
        self,
        mock_get,
        mock_set_pid_for_blob,
        mock_get_pid_for_blob,
    ):
        """test_auto_set_pid_true_returns_none"""

        mock_get_pid_for_blob.side_effect = main_exceptions.DoesNotExist(
            "pid_does_not_exist"
        )  # noqa
        mock_get.return_value = mocks.MockPidSettings()
        mock_set_pid_for_blob.return_value = None

        self.assertIsNone(blob_watch._set_blob_pid(self.mock_document))

    @patch.object(PidSettings, "get")
    @patch.object(blob_system_api, "get_pid_for_blob")
    @patch.object(blob_system_api, "set_pid_for_blob")
    def test_pid_not_created_if_already_assigned(
        self, mock_set_pid_for_blob, mock_get_pid_for_blob, mock_settings_get
    ):
        """test_pid_not_created_if_already_assigned"""

        mock_get_pid_for_blob.return_value = "mock_pid"
        mock_settings_get.return_value = mocks.MockPidSettings()

        blob_watch._set_blob_pid(self.mock_document)
        mock_set_pid_for_blob.assert_not_called()


class TestDeleteBlobPid(TestCase):
    """Unit tests for detele_blob_pid function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_blob = mocks.MockDocument()

    @patch.object(blob_system_api, "delete_pid_for_blob")
    def test_delete_pid_for_blob_is_called(self, mock_delete_pid_for_blob):
        """test_delete_pid_for_blob_is_called"""
        blob_watch.delete_blob_pid(None, self.mock_blob)

        mock_delete_pid_for_blob.assert_called_with(self.mock_blob)

    @patch.object(blob_watch, "logger")
    @patch.object(blob_system_api, "delete_pid_for_blob")
    def test_delete_pid_for_blob_error_raise_warning(
        self, mock_delete_pid_for_blob, mock_logger
    ):
        """test_delete_pid_for_blob_error_raise_warning"""
        mock_delete_pid_for_blob.side_effect = Exception(
            "mock_delete_pid_for_blob_exception"
        )
        blob_watch.delete_blob_pid(None, self.mock_blob)

        mock_logger.warning.assert_called()
