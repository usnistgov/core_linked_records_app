""" Unit tests for core_linked_records_app.components.pid_settings.watch
"""
from unittest import TestCase

from unittest.mock import patch

from core_linked_records_app.components.pid_settings import api as pid_settings_api
from core_linked_records_app.components.pid_settings import watch as pid_settings_watch
from core_linked_records_app.components.pid_settings.models import PidSettings
from core_main_app.commons.exceptions import CoreError


class TestInit(TestCase):
    @patch.object(PidSettings, "get")
    def test_pid_settings_get_failure_raises_core_error(self, mock_pid_settings_get):
        mock_pid_settings_get.side_effect = Exception("mock_pid_settings_get_exception")

        with self.assertRaises(CoreError):
            pid_settings_watch.init()

    @patch.object(PidSettings, "get")
    def test_pid_settings_get_true_returns_none(self, mock_pid_settings_get):
        mock_pid_settings_get.return_value = True

        self.assertIsNone(pid_settings_watch.init())

    @patch.object(PidSettings, "__init__")
    @patch.object(PidSettings, "get")
    def test_pid_settings_init_raises_core_error(
        self, mock_pid_settings_get, mock_pid_settings_init
    ):
        mock_pid_settings_get.return_value = False
        mock_pid_settings_init.side_effect = Exception(
            "mock_pid_settings_init_exception"
        )

        with self.assertRaises(CoreError):
            pid_settings_watch.init()

    @patch.object(pid_settings_api, "upsert")
    @patch.object(PidSettings, "__init__")
    @patch.object(PidSettings, "get")
    def test_pid_settings_upsert_failure_raises_core_error(
        self, mock_pid_settings_get, mock_pid_settings_init, mock_pid_settings_upsert
    ):
        mock_pid_settings_get.return_value = False
        mock_pid_settings_init.return_value = None
        mock_pid_settings_upsert.side_effect = Exception(
            "mock_pid_settings_upsert_exception"
        )

        with self.assertRaises(CoreError):
            pid_settings_watch.init()

    @patch.object(pid_settings_api, "upsert")
    @patch.object(PidSettings, "__init__")
    @patch.object(PidSettings, "get")
    def test_pid_settings_get_false_returns_none(
        self, mock_pid_settings_get, mock_pid_settings_init, mock_pid_settings_upsert
    ):
        mock_pid_settings_get.return_value = False
        mock_pid_settings_init.return_value = None
        mock_pid_settings_upsert.return_value = None

        self.assertIsNone(pid_settings_watch.init())
