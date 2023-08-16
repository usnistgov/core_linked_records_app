""" Unit tests for core_linked_records_app.system.pid_settings.api
"""

from unittest import TestCase
from unittest.mock import patch

from core_linked_records_app.components.pid_settings import (
    access_control as pid_settings_acl,
)
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.pid_settings import (
    api as pid_settings_system_api,
)
from core_main_app.commons.exceptions import ApiError


class TestUpsert(TestCase):
    """Unit tests for `upsert` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_pid_settings = PidSettings()

    @patch.object(PidSettings, "save")
    def test_save_failure_raises_api_error(self, mock_save):
        """test_save_failure_raises_api_error"""

        mock_save.side_effect = Exception("mock_save_exception")

        with self.assertRaises(ApiError):
            pid_settings_system_api.upsert(self.mock_pid_settings)

    @patch.object(PidSettings, "save")
    def test_returns_save_method_output(self, mock_save):
        """test_returns_save_method_output"""

        mock_save.return_value = None

        self.assertEqual(
            pid_settings_system_api.upsert(self.mock_pid_settings),
            self.mock_pid_settings,
        )


class TestGet(TestCase):
    """Unit tests for `get` function."""

    @patch.object(PidSettings, "get")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_save_failure_raises_api_error(
        self, mock_check_has_perm, mock_get
    ):
        """test_save_failure_raises_api_error"""
        mock_check_has_perm.return_value = True
        mock_get.side_effect = Exception("mock_get_exception")

        with self.assertRaises(ApiError):
            pid_settings_system_api.get()

    @patch.object(PidSettings, "get")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_returns_save_method_output(self, mock_check_has_perm, mock_get):
        """test_returns_save_method_output"""
        mock_check_has_perm.return_value = True
        expected_result = "mock_get"
        mock_get.return_value = expected_result

        self.assertEqual(pid_settings_system_api.get(), expected_result)
