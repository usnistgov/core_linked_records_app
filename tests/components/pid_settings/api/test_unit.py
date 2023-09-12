""" Unit tests for core_linked_records_app.components.pid_settings.api.
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from core_linked_records_app.components.pid_settings import (
    api as pid_settings_api,
    access_control as pid_settings_acl,
)
from core_linked_records_app.system.pid_settings import (
    api as pid_settings_system_api,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestUpsert(TestCase):
    """Unit tests for `upsert` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_kwargs = {
            "pid_settings_object": MagicMock(),
            "user": create_mock_user("1", is_superuser=True),
        }

    @patch.object(pid_settings_system_api, "upsert")
    def test_pid_settings_system_api_upsert_called(self, mock_system_upsert):
        """test_pid_settings_system_api_upsert_called"""

        pid_settings_api.upsert(**self.mock_kwargs)
        mock_system_upsert.assert_called_with(
            self.mock_kwargs["pid_settings_object"]
        )

    @patch.object(pid_settings_system_api, "upsert")
    def test_returns_pid_settings_system_api_upsert_value(
        self, mock_system_upsert
    ):
        """test_returns_pid_settings_system_api_upsert_value"""
        expected_result = "mock_upsert"
        mock_system_upsert.return_value = expected_result

        self.assertEqual(
            pid_settings_api.upsert(**self.mock_kwargs), expected_result
        )


class TestGet(TestCase):
    """Unit tests for `get` function."""

    def setUp(self) -> None:
        """setUp"""
        self.mock_user = create_mock_user("1")

    @patch.object(pid_settings_system_api, "get")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_pid_settings_system_api_get_called(
        self, mock_check_has_perm, mock_system_get
    ):
        """test_pid_settings_system_api_get_called"""
        mock_check_has_perm.return_value = True

        pid_settings_api.get(self.mock_user)
        mock_system_get.assert_called()

    @patch.object(pid_settings_system_api, "get")
    @patch.object(pid_settings_acl, "check_has_perm")
    def test_returns_pid_settings_system_api_get_value(
        self, mock_check_has_perm, mock_system_get
    ):
        """test_returns_pid_settings_system_api_get_value"""
        mock_check_has_perm.return_value = True
        expected_result = "mock_get"
        mock_system_get.return_value = expected_result

        self.assertEqual(pid_settings_api.get(self.mock_user), expected_result)
