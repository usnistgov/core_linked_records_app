""" Unit tests for core_linked_records_app.utils.pid
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from core_linked_records_app.utils import pid as pid_utils
from core_linked_records_app.utils.providers import (
    AbstractIdProvider,
)
from tests import test_settings


class TestIsValidPidValue(TestCase):
    """Tests for is_valid_pid_value function"""

    @classmethod
    def setUpClass(cls) -> None:
        """Create test case global variables"""
        cls.mock_pid_provider_name = "mock_pid_provider_name"
        cls.mock_provider_url = "mock_provider_url"

        cls.mock_provider = Mock(spec=AbstractIdProvider)
        cls.mock_provider.provider_lookup_url = cls.mock_provider_url

        cls.mock_pid_format = r"[a-z]+"

    def test_pid_value_none_returns_false(self):
        """Test pid_value None returns False"""
        self.assertFalse(
            pid_utils.is_valid_pid_value(
                None, self.mock_pid_provider_name, self.mock_pid_format
            )
        )

    def test_pid_value_empty_string_returns_false(self):
        """Test pid_value empty returns False"""
        self.assertFalse(
            pid_utils.is_valid_pid_value(
                "", self.mock_pid_provider_name, self.mock_pid_format
            )
        )

    @patch("core_linked_records_app.utils.providers.ProviderManager.get")
    def test_pid_value_not_match_returns_false(
        self, mock_provider_manager_get
    ):
        """Test pid_value not matching returns False"""
        mock_provider_manager_get.return_value = self.mock_provider

        self.assertFalse(
            pid_utils.is_valid_pid_value(
                "wrong_pid", self.mock_pid_provider_name, self.mock_pid_format
            )
        )

    @patch("core_linked_records_app.utils.providers.ProviderManager.get")
    def test_pid_value_match_returns_true(self, mock_provider_manager_get):
        """Test pid_value matching returns True"""
        mock_provider_manager_get.return_value = self.mock_provider

        mock_pid = f"{self.mock_provider_url}/{test_settings.ID_PROVIDER_PREFIXES[0]}/mockpid"

        self.assertTrue(
            pid_utils.is_valid_pid_value(
                mock_pid, self.mock_pid_provider_name, self.mock_pid_format
            )
        )
