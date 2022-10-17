""" Unit tests for core_linked_records_app.components.pid_settings.models
"""
from unittest import TestCase
from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist

from core_linked_records_app.components.pid_settings.models import PidSettings
from core_main_app.commons import exceptions


class TestPidSettingsGet(TestCase):
    """Test Pid Settings Get"""

    @patch.object(PidSettings, "objects")
    def test_pid_settings_first_does_not_exist_returns_none(
        self, mock_pid_settings
    ):
        """test_pid_settings_first_does_not_exist_returns_none"""
        mock_pid_settings.first.side_effect = ObjectDoesNotExist()

        self.assertIsNone(PidSettings.get())

    @patch.object(PidSettings, "objects")
    def test_pid_settings_first_failure_raises_model_error(
        self, mock_pid_settings
    ):
        """test_pid_settings_first_failure_raises_model_error"""
        mock_pid_settings.first.side_effect = Exception(
            "mock_pid_settings_first_exception"
        )

        with self.assertRaises(exceptions.ModelError):
            PidSettings.get()

    @patch.object(PidSettings, "objects")
    def test_returns_pid_settings_first_output(self, mock_pid_settings):
        """test_returns_pid_settings_first_output"""
        expected_result = "mock_pid_settings"
        mock_pid_settings.first.return_value = expected_result

        self.assertEqual(PidSettings.get(), expected_result)
