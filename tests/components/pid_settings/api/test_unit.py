""" Unit tests for core_linked_records_app.components.pid_settings.api
"""
from unittest import TestCase
from unittest.mock import patch

from core_main_app.commons.exceptions import ApiError
from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.components.pid_settings.models import PidSettings


class TestUpsert(TestCase):
    """Test Upsert"""

    def setUp(self) -> None:
        self.mock_pid_settings = PidSettings()

    @patch.object(PidSettings, "save")
    def test_save_failure_raises_api_error(self, mock_save):
        """test_save_failure_raises_api_error"""

        mock_save.side_effect = Exception("mock_save_exception")

        with self.assertRaises(ApiError):
            pid_settings_api.upsert(self.mock_pid_settings)

    @patch.object(PidSettings, "save")
    def test_returns_save_method_output(self, mock_save):
        """test_returns_save_method_output"""

        mock_save.return_value = None

        self.assertEqual(
            pid_settings_api.upsert(self.mock_pid_settings), self.mock_pid_settings
        )


class TestGet(TestCase):
    """Test Get"""

    @patch.object(PidSettings, "get")
    def test_save_failure_raises_api_error(self, mock_get):
        """test_save_failure_raises_api_error"""

        mock_get.side_effect = Exception("mock_get_exception")

        with self.assertRaises(ApiError):
            pid_settings_api.get()

    @patch.object(PidSettings, "get")
    def test_returns_save_method_output(self, mock_get):
        """test_returns_save_method_output"""

        expected_result = "mock_get"
        mock_get.return_value = expected_result

        self.assertEqual(pid_settings_api.get(), expected_result)
