""" Unit tests for core_linked_records_app.system.pid_path.api
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from core_linked_records_app.components.pid_path.models import PidPath
from core_linked_records_app.system.pid_path import (
    api as pid_path_system_api,
)


class TestGetPidPathByTemplate(TestCase):
    """Test get_pid_path_by_template method"""

    @patch(
        "core_linked_records_app.system.pid_path.api.PidPath.get_by_template"
    )
    def test_get_by_template_is_called(self, mock_get_by_template):
        """Test get_by_template is called"""
        mock_template = "mock_template"

        pid_path_system_api.get_pid_path_by_template(mock_template)
        mock_get_by_template.assert_called_with(mock_template)

    @patch("core_linked_records_app.system.pid_path.api.PidPath.__new__")
    @patch(
        "core_linked_records_app.system.pid_path.api.PidPath.get_by_template"
    )
    def test_get_by_template_none_returns_pid_path(
        self, mock_get_by_template, mock_pid_path
    ):
        """If get_by_template returns None, the PidPath returned is the default one."""
        expected_result = Mock(spec=PidPath)
        mock_get_by_template.return_value = None
        mock_pid_path.return_value = expected_result

        result = pid_path_system_api.get_pid_path_by_template("mock_template")
        self.assertEqual(result, expected_result)

    @patch(
        "core_linked_records_app.system.pid_path.api.PidPath.get_by_template"
    )
    def test_returns_get_by_template_if_not_none(self, mock_get_by_template):
        """If get_by_template is not None, the PidPath returned is get_by_template."""
        expected_result = "mock_result"
        mock_get_by_template.return_value = expected_result

        result = pid_path_system_api.get_pid_path_by_template("mock_template")
        self.assertEqual(result, expected_result)
