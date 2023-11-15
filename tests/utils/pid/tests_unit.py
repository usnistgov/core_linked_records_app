""" Unit tests for core_linked_records_app.utils.pid
"""
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from core_linked_records_app.utils import pid as pid_utils
from core_linked_records_app.utils.exceptions import (
    InvalidPrefixError,
    InvalidRecordError,
)
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
        cls.mock_provider.provider_lookup_url = cls.mock_provider_url  # noqa

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


class TestGetPidSettingsDict(TestCase):
    """Unit tests for `get_pid_settings_dict` function."""

    def test_returns_dict(self):
        """test_returns_dict"""
        result = pid_utils.get_pid_settings_dict(MagicMock())
        self.assertIsInstance(result, dict)

    def test_returns_expected_keys(self):
        """test_returns_expected_keys"""
        expected_keys = [
            "auto_set_pid",
            "path",
            "format",
            "system_name",
            "system_type",
            "prefixes",
        ]

        result = pid_utils.get_pid_settings_dict(MagicMock())
        self.assertEqual(sorted(result.keys()), sorted(expected_keys))


class TestSplitPrefixFromRecord(TestCase):
    """Unit tests for `split_prefix_from_record` function."""

    @patch.object(pid_utils, "settings")
    def test_no_record_provided_with_no_final_slash_sets_values_correctly(
        self, mock_settings
    ):
        """test_no_record_provided_with_no_final_slash_sets_values_correctly"""
        mock_prefix = "mock_prefix"
        mock_settings.ID_PROVIDER_PREFIXES = [mock_prefix]

        expected_results = (mock_prefix, None)
        results = pid_utils.split_prefix_from_record(mock_prefix)

        self.assertEqual(results, expected_results)

    @patch.object(pid_utils, "settings")
    def test_no_record_provided_with_final_slash_sets_values_correctly(
        self, mock_settings
    ):
        """test_no_record_provided_with_final_slash_sets_values_correctly"""
        mock_prefix = "mock_prefix/"
        mock_settings.ID_PROVIDER_PREFIXES = [mock_prefix[:-1]]

        expected_results = (mock_prefix[:-1], None)
        results = pid_utils.split_prefix_from_record(mock_prefix)

        self.assertEqual(results, expected_results)

    @patch.object(pid_utils, "settings")
    def test_prefix_and_record_provided_sets_values_correctly(
        self, mock_settings
    ):
        """test_prefix_and_record_provided_sets_values_correctly"""
        mock_prefix = "mock_prefix"
        mock_record = "mock_record"
        mock_settings.ID_PROVIDER_PREFIXES = [mock_prefix]
        mock_settings.PID_FORMAT = r"[a-z_]+"

        expected_results = (mock_prefix, mock_record)
        results = pid_utils.split_prefix_from_record(
            f"{mock_prefix}/{mock_record}"
        )

        self.assertEqual(results, expected_results)

    def test_empty_prefix_raises_invalid_prefix_error(self):
        """test_empty_prefix_raises_invalid_prefix_error"""
        mock_prefix = ""
        mock_record = "mock_record"

        with self.assertRaises(InvalidPrefixError):
            pid_utils.split_prefix_from_record(f"{mock_prefix}/{mock_record}")

    @patch.object(pid_utils, "settings")
    def test_invalid_prefix_raises_invalid_prefix_error(self, mock_settings):
        """test_invalid_prefix_raises_invalid_prefix_error"""
        mock_prefix = "mock_prefix"
        mock_record = "mock_record"
        mock_settings.ID_PROVIDER_PREFIXES = [mock_prefix + "_0"]

        with self.assertRaises(InvalidPrefixError):
            pid_utils.split_prefix_from_record(f"{mock_prefix}/{mock_record}")

    @patch.object(pid_utils, "settings")
    def test_invalid_record_raises_invalid_record_error(self, mock_settings):
        """test_invalid_record_raises_invalid_record_error"""
        mock_prefix = "mock_prefix"
        mock_record = "mock_record"
        mock_settings.ID_PROVIDER_PREFIXES = [mock_prefix]

        with self.assertRaises(InvalidRecordError):
            pid_utils.split_prefix_from_record(f"{mock_prefix}/{mock_record}")
