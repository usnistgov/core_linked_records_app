""" Unit tests for core_linked_records_app.components.pid_settings.api
"""
from unittest import TestCase

from unittest.mock import patch

from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_main_app.commons.exceptions import ApiError


class TestUpsert(TestCase):
    def setUp(self) -> None:
        self.mock_pid_settings = PidSettings()

    @patch.object(PidSettings, "save")
    def test_save_failure_raises_api_error(self, mock_save):
        mock_save.side_effect = Exception("mock_save_exception")

        with self.assertRaises(ApiError):
            pid_settings_api.upsert(self.mock_pid_settings)

    @patch.object(PidSettings, "save")
    def test_returns_save_method_output(self, mock_save):
        expected_result = "mock_save"
        mock_save.return_value = expected_result

        self.assertEquals(
            pid_settings_api.upsert(self.mock_pid_settings), expected_result
        )


class TestGet(TestCase):
    @patch.object(PidSettings, "get")
    def test_save_failure_raises_api_error(self, mock_get):
        mock_get.side_effect = Exception("mock_get_exception")

        with self.assertRaises(ApiError):
            pid_settings_api.get()

    @patch.object(PidSettings, "get")
    def test_returns_save_method_output(self, mock_get):
        expected_result = "mock_get"
        mock_get.return_value = expected_result

        self.assertEquals(pid_settings_api.get(), expected_result)
