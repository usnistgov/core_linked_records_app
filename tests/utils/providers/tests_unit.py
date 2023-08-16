""" Unit tests for core_linked_records_app.utils.providers.__init__.
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from core_linked_records_app.utils import providers
from core_main_app.commons.exceptions import CoreError
from tests.mocks import MockResponse


class TestDeleteRecordFromProvider(TestCase):
    """Unit tests for `delete_record_from_provider` function."""

    @patch.object(providers, "ProviderManager")
    def test_provider_delete_is_called(self, mock_provider_manager):
        """test_provider_delete_is_called"""
        mock_provider = Mock()
        mock_record = "mock_record"

        mock_provider_manager().get.return_value = mock_provider
        mock_provider.delete.return_value = MockResponse()

        providers.delete_record_from_provider(mock_record)
        mock_provider.delete.assert_called_with(mock_record)

    @patch.object(providers, "logger")
    @patch.object(providers, "ProviderManager")
    def test_provider_delete_failure_raises_api_error(
        self,
        mock_provider_manager,
        mock_logger,  # noqa, pylint: disable=unused-argument
    ):
        """test_provider_delete_failure_is_logged"""
        mock_provider = Mock()
        mock_provider.delete.return_value = MockResponse(status_code=500)
        mock_record = "mock_record"

        mock_provider_manager().get.return_value = mock_provider

        with self.assertRaises(CoreError):
            providers.delete_record_from_provider(mock_record)
