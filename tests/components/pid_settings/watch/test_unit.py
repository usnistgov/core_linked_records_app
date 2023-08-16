""" Unit tests for core_linked_records_app.components.pid_settings.watch
"""
from unittest import TestCase
from unittest.mock import patch

from core_linked_records_app.components.pid_settings import (
    watch as pid_settings_watch,
)
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_linked_records_app.system.pid_settings import (
    api as pid_settings_system_api,
)


class TestInit(TestCase):
    """Test Init"""

    @patch.object(PidSettings, "get")
    def test_pid_settings_get_failure_returns_none(
        self, mock_pid_settings_get
    ):
        """test_pid_settings_get_failure_returns_none"""

        mock_pid_settings_get.side_effect = Exception(
            "mock_pid_settings_get_exception"
        )

        self.assertIsNone(pid_settings_watch.init())

    @patch.object(PidSettings, "get")
    def test_pid_settings_get_true_returns_none(self, mock_pid_settings_get):
        """test_pid_settings_get_true_returns_none"""

        mock_pid_settings_get.return_value = True

        self.assertIsNone(pid_settings_watch.init())

    @patch.object(PidSettings, "__init__")
    @patch.object(PidSettings, "get")
    def test_pid_settings_init_failure_returns_none(
        self, mock_pid_settings_get, mock_pid_settings_init
    ):
        """test_pid_settings_init_failure_returns_none"""

        mock_pid_settings_get.return_value = False
        mock_pid_settings_init.side_effect = Exception(
            "mock_pid_settings_init_exception"
        )

        self.assertIsNone(pid_settings_watch.init())

    @patch.object(pid_settings_system_api, "upsert")
    @patch.object(PidSettings, "__init__")
    @patch.object(PidSettings, "get")
    def test_pid_settings_upsert_failure_returns_none(
        self,
        mock_pid_settings_get,
        mock_pid_settings_init,
        mock_pid_settings_upsert,
    ):
        """test_pid_settings_upsert_failure_returns_none"""

        mock_pid_settings_get.return_value = False
        mock_pid_settings_init.return_value = None
        mock_pid_settings_upsert.side_effect = Exception(
            "mock_pid_settings_upsert_exception"
        )

        self.assertIsNone(pid_settings_watch.init())

    @patch.object(pid_settings_system_api, "upsert")
    @patch.object(PidSettings, "__init__")
    @patch.object(PidSettings, "get")
    def test_pid_settings_get_false_returns_none(
        self,
        mock_pid_settings_get,
        mock_pid_settings_init,
        mock_pid_settings_upsert,
    ):
        """test_pid_settings_get_false_returns_none"""

        mock_pid_settings_get.return_value = False
        mock_pid_settings_init.return_value = None
        mock_pid_settings_upsert.return_value = None

        self.assertIsNone(pid_settings_watch.init())
